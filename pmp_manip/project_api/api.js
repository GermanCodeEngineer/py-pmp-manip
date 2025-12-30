// Mostly stolen from
// https://github.com/PenguinMod/penguinmod.github.io/blob/develop/src/lib/project-fetcher-hoc.jsx

const {ArgumentParser} = require("argparse")
const JSZip = require("jszip")
const {protobufToJson} = require("pmp-protobuf")
const fs = require("fs")
const path = require("path")

function fetchProject(apiURL, projectId) {
    const projectUrl = `${apiURL}/projects/getprojectwrapper?safe=true&projectId=${projectId}`
    const promise = fetch(projectUrl)
        .then(async (response) => {
            if (!response.ok) {
                throw new Error(`Request returned status ${response.status} ${response.statusText}.`)
            }
            const project = await response.json()

            const projectJson = protobufToJson(new Uint8Array(project.project.data))

            // Now get the assets
            const zip = new JSZip()
            zip.file("project.json", JSON.stringify(projectJson))
            
            if (typeof project.assets !== "object") {
                throw new TypeError("Invalid type given inside the assets list.")
            }
            for (const asset of project.assets) {
                zip.file(asset.id, new Uint8Array(asset.buffer.data).buffer)
            }

            return await zip.generateAsync({ type: "nodebuffer" })
        })
        .then((buffer) => {
            // tw: If the project data appears to be HTML, then the result is probably an nginx 404 page,
            // and the "missing project" project should be loaded instead.
            // See: https://projects.scratch.mit.edu/9999999999999999999999
            if (buffer) {
                const firstChar = buffer[0]
                if (firstChar === "<" || firstChar === "<".charCodeAt(0)) {
                    throw new Error("Could not find project.")
                }
            }
            return buffer
        })
    return promise
}

// ---------- Entry point ----------

if (require.main === module) {
    const parser = new ArgumentParser({
        description: "Fetch PenguinMod projects"
    })
    
    parser.add_argument("api_url", {
        help: `The API URL`,
    })
    
    const subparsers = parser.add_subparsers({
        title: "commands",
        dest: "command",
        required: true
    })
        
    // Project command
    const projectParser = subparsers.add_parser("project", {
        help: "Fetch a project by ID and save as (.pmp) file"
    })
    projectParser.add_argument("project_id", {
        help: "The project ID to fetch (e.g., 0131435715)"
    })
    projectParser.add_argument("output_file", {
        help: "Output file path",
    })
    
    // Projects command (parallel fetching)
    const projectsParser = subparsers.add_parser("projects", {
        help: "Fetch multiple projects in parallel"
    })
    projectsParser.add_argument("project_ids", {
        nargs: "+",
        help: "Space-separated list of project IDs to fetch"
    })
    projectsParser.add_argument("-o", "--output-dir", {
        help: "Output directory (default: current directory)",
        dest: "output_dir",
        default: "."
    })
    projectsParser.add_argument("-p", "--prefix", {
        help: "Filename prefix (default: 'project_')",
        dest: "prefix",
        default: "project_"
    })
    
    const args = parser.parse_args()
    
    if (args.command === "project") {
        fetchProject(args.api_url, args.project_id)
            .then((buffer) => {
                if (buffer) {
                    const filename = args.output_file
                    fs.writeFileSync(filename, buffer)
                    console.log(`Project saved to ${filename}`)
                }
            })
            .catch((error) => {
                console.error("Error fetching project:", error.message)
                process.exitCode = 1
            })
    } else if (args.command === "projects") {
        // Fetch all projects in parallel
        const fetchPromises = args.project_ids.map(projectId => {
            return fetchProject(args.api_url, projectId)
                .then(buffer => ({
                    projectId,
                    buffer,
                    success: true
                }))
                .catch(error => ({
                    projectId,
                    error: error.message,
                    success: false
                }))
        })
        
        Promise.all(fetchPromises)
            .then(results => {
                let successCount = 0
                let failCount = 0
                
                results.forEach(result => {
                    if (result.success) {
                        const filename = path.join(
                            args.output_dir,
                            `${args.prefix}${result.projectId}.pmp`
                        )
                        fs.writeFileSync(filename, result.buffer)
                        console.log(`✓ Project ${result.projectId} saved to ${filename}`)
                        successCount++
                    } else {
                        console.error(`✗ Project ${result.projectId} failed: ${result.error}`)
                        failCount++
                    }
                })
                
                console.log(`\nCompleted: ${successCount} succeeded, ${failCount} failed`)
                if (failCount > 0) {
                    process.exitCode = 1
                }
            })
    }
}

module.exports = {fetchProject}
