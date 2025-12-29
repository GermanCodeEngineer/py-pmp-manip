// Mostly stolen from https://github.com/PenguinMod/penguinmod.github.io/blob/develop/src/lib/project-fetcher-hoc.jsx
const JSZip = require("jszip")
const {protobufToJson} = require("pmp-protobuf")
const fs = require("fs")

function fetchProject(projectId) {
    const projectUrl = `https://projects.penguinmod.com/api/v1/projects/getprojectwrapper?safe=true&projectId=${projectId}`
    const assetPromise = fetch(projectUrl)
        .then(async (response) => {
            if (!response.ok) {
                throw new Error(`Request returned status ${response.status}.`)
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
        .catch((error) => {
            console.error(error)
            process.exit(1)
        })
    return assetPromise
}

// ---------- Entry point ----------

if (require.main === module) {
    const projectId = process.argv[2] // e.g. 0131435715
    fetchProject(projectId)
        .then((buffer) => {
            if (buffer) {
                const filename = `project_${projectId}.pmp`
                fs.writeFileSync(filename, buffer)
                console.log(`Project saved to ${filename}`)
            }
            process.exit(0)
        })
}

module.exports = {fetchProject}

