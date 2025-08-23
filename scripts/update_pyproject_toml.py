import argparse
import subprocess
import sys
from pathlib import Path
from tomlkit import parse, document, table, array, dumps

def run_pipreqs(paths):
    """Run pipreqs on one or more paths and return a set of (pkg, version)."""
    packages = set()
    for path in paths:
        if not path.exists():
            continue
        result = subprocess.run(
            ["pipreqs", str(path), "--force", "--print"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ pipreqs failed for {path}:", result.stderr)
            sys.exit(1)
        for line in result.stdout.strip().splitlines():
            if "==" in line:
                pkg, version = line.strip().split("==", 1)
                packages.add((pkg.strip(), version.strip()))
    return packages

def update_project_section(existing_toml, runtime_deps, dev_deps, project_name, version):
    """Update the [project] section and optional [project.optional-dependencies]."""
    project = existing_toml.get("project", table())

    if project_name:
        project["name"] = project_name
    if version:
        project["version"] = version

    # runtime dependencies
    deps_array = array().multiline(True)
    for pkg, version in sorted(runtime_deps):
        deps_array.append(f"{pkg}=={version}")
    project["dependencies"] = deps_array

    # dev dependencies under optional-dependencies.dev
    optional = project.get("optional-dependencies", table())
    dev_array = array().multiline(True)
    for pkg, version in sorted(dev_deps):
        dev_array.append(f"{pkg}=={version}")
    optional["dev"] = dev_array
    project["optional-dependencies"] = optional

    existing_toml["project"] = project
    return existing_toml

def main():
    parser = argparse.ArgumentParser(
        description="Generate or update pyproject.toml with detected imports."
    )
    parser.add_argument("--project-name", help="Override project name (default: current folder name)")
    parser.add_argument("--version", default=None, help="Project version (default: current version)")
    parser.add_argument("--project-root", default=".", help="Path to the Python project directory")
    parser.add_argument("--output", default="pyproject.toml", help="Output file (default: pyproject.toml)")
    parser.add_argument("--dry-run", action="store_true", help="Print result instead of writing")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    output_path = Path(args.output).resolve()

    print(f"🔍 Scanning Python files in: {project_root}")

    # runtime dependencies: only the main project folder
    runtime_path = project_root / "pmp_manip"
    runtime_deps = run_pipreqs([runtime_path])

    # dev dependencies: scripts, tests, docs
    dev_paths = [project_root / "scripts", project_root / "tests", project_root / "docs"]
    dev_deps = run_pipreqs(dev_paths) - runtime_deps  # avoid duplicates

    if not runtime_deps and not dev_deps:
        print("⚠️ No dependencies found.")
        sys.exit(0)

    if output_path.exists():
        toml_text = output_path.read_text(encoding="utf-8")
        toml_data = parse(toml_text)
    else:
        toml_data = document()

    project_name = args.project_name or project_root.name
    toml_data = update_project_section(toml_data, runtime_deps, dev_deps, project_name, args.version)

    output_text = dumps(toml_data)
    if args.dry_run:
        print(output_text)
    else:
        output_path.write_text(output_text, encoding="utf-8")
        print(f"✅ Updated {output_path.relative_to(project_root)} with {len(runtime_deps)} runtime and {len(dev_deps)} dev dependencies.")

if __name__ == "__main__":
    main()
