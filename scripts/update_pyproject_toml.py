import argparse
import subprocess
import sys
from pathlib import Path
from tomlkit import parse, document, table, array, dumps

def run_pipreqs(path):
    """Run pipreqs and return a list of required packages."""
    result = subprocess.run(
        ["pipreqs", str(path), "--force", "--print"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("❌ pipreqs failed:", result.stderr)
        sys.exit(1)

    lines = result.stdout.strip().splitlines()
    packages = []
    for line in lines:
        if "==" in line:
            pkg, version = line.strip().split("==", 1)
            packages.append((pkg.strip(), version.strip()))
    return packages


def update_project_section(existing_toml, deps, project_name, version):
    """Update the [project] section, preserving other sections."""
    project = existing_toml["project"]

    if project_name:
        project["name"] = project_name
    if version:
        project["version"] = version

    deps_array = array().multiline(True)
    for pkg, version in sorted(deps):
        deps_array.append(f"{pkg}=={version}")
    project["dependencies"] = deps_array

    return existing_toml


def main():
    parser = argparse.ArgumentParser(
        description="Generate or update pyproject.toml with detected imports."
    )
    parser.add_argument(
        "--project-name", help="Override project name (default: current folder name)"
    )
    parser.add_argument("--version", default="0.1.0", help="Project version")
    parser.add_argument(
        "--project-root",
        default=".",
        help="Path to the Python project directory",
    )
    parser.add_argument(
        "--output",
        default="pyproject.toml",
        help="Output file (default: pyproject.toml)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print result to stdout instead of writing"
    )

    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    output_path = Path(args.output).resolve()

    print(f"🔍 Scanning Python files in: {project_root}")
    deps = run_pipreqs(project_root)
    if not deps:
        print("⚠️ No external dependencies found.")
        sys.exit(0)

    if output_path.exists():
        toml_text = output_path.read_text()
        toml_data = parse(toml_text)
    else:
        toml_data = document()

    project_name = args.project_name or project_root.name
    toml_data = update_project_section(toml_data, deps, project_name, args.version)

    output_text = dumps(toml_data)
    if args.dry_run:
        print(output_text)
    else:
        output_path.write_text(output_text)
        print(f"✅ Updated {output_path.relative_to(project_root)} with {len(deps)} dependencies.")


if __name__ == "__main__":
    main()