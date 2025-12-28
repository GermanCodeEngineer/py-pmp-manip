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
            ["pipreqs", str(path), "--force", "--print", "--encoding", "utf-8"],
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

def format_version_spec(version):
    """Convert a full version to a compatible release specifier (~=).
    Example: '11.3.0' -> '11.3', '2.32.5' -> '2.32'
    """
    parts = version.split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return version

def parse_dependency_spec(dep_string):
    """Parse a dependency spec into (package, version_spec, operator)."""
    for op in ["~=", ">=", "<=", "==", "!="]:
        if op in dep_string:
            pkg, version = dep_string.split(op, 1)
            return pkg.strip(), version.strip(), op
    return dep_string.strip(), None, None


def compare_dependencies(current_deps, detected_deps, dep_type="runtime"):
    """Compare current vs detected dependencies and return analysis."""
    current_dict = {}
    for dep in current_deps:
        pkg, version, op = parse_dependency_spec(dep)
        current_dict[pkg.lower()] = (pkg, version, op, dep)
    
    detected_dict = {}
    for pkg, version in detected_deps:
        version_spec = format_version_spec(version)
        detected_dict[pkg.lower()] = (pkg, version_spec)
    
    missing = []  # In code but not in pyproject.toml
    extra = []    # In pyproject.toml but not detected in code
    version_changes = []  # Different versions
    
    for pkg_lower, (pkg, version_spec) in detected_dict.items():
        if pkg_lower not in current_dict:
            missing.append((pkg, version_spec))
        else:
            curr_pkg, curr_version, curr_op, _ = current_dict[pkg_lower]
            if curr_version != version_spec or curr_op != "~=":
                version_changes.append((curr_pkg, f"{curr_op}{curr_version}" if curr_op else "any", pkg, f"~={version_spec}"))
    
    for pkg_lower, (pkg, version, op, original) in current_dict.items():
        if pkg_lower not in detected_dict:
            extra.append((pkg, f"{op}{version}" if op else "any"))
    
    return missing, extra, version_changes


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
        version_spec = format_version_spec(version)
        deps_array.append(f"{pkg}~={version_spec}")
    project["dependencies"] = deps_array

    # dev dependencies under optional-dependencies.dev
    optional = project.get("optional-dependencies", table())
    dev_array = array().multiline(True)
    for pkg, version in sorted(dev_deps):
        version_spec = format_version_spec(version)
        dev_array.append(f"{pkg}~={version_spec}")
    optional["dev"] = dev_array
    project["optional-dependencies"] = optional

    existing_toml["project"] = project
    return existing_toml

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python imports and suggest pyproject.toml dependency updates."
    )
    parser.add_argument("--project-name", help="Override project name (default: current folder name)")
    parser.add_argument("--version", default=None, help="Project version (default: current version)")
    parser.add_argument("--project-root", default=".", help="Path to the Python project directory")
    parser.add_argument("--output", default="pyproject.toml", help="Output file (default: pyproject.toml)")
    parser.add_argument("--apply", action="store_true", help="Actually write changes to pyproject.toml (default: just show recommendations)")
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
        print("⚠️  No dependencies found.")
        sys.exit(0)

    # Read existing pyproject.toml
    if output_path.exists():
        toml_text = output_path.read_text(encoding="utf-8")
        toml_data = parse(toml_text)
        project = toml_data.get("project", {})
        current_runtime_deps = project.get("dependencies", [])
        optional_deps = project.get("optional-dependencies", {})
        current_dev_deps = optional_deps.get("dev", [])
    else:
        print("⚠️  pyproject.toml not found. Creating new file.")
        toml_data = document()
        current_runtime_deps = []
        current_dev_deps = []

    # Analyze differences
    print("\n" + "=" * 90)
    print("📊 DEPENDENCY ANALYSIS")
    print("=" * 90)

    # Runtime dependencies
    missing_runtime, extra_runtime, changed_runtime = compare_dependencies(
        current_runtime_deps, runtime_deps, "runtime"
    )

    if missing_runtime or extra_runtime or changed_runtime:
        print("\n📦 Runtime Dependencies:")
        print("-" * 90)
        
        if missing_runtime:
            print("\n❌ MISSING (detected in code but not in pyproject.toml):")
            for pkg, version_spec in missing_runtime:
                print(f"   + {pkg}~={version_spec}")
        
        if changed_runtime:
            print("\n🔄 VERSION UPDATES (detected different version or constraint):")
            for curr_pkg, curr_spec, new_pkg, new_spec in changed_runtime:
                print(f"   ~ {curr_pkg}{curr_spec} → {new_pkg}{new_spec}")
        
        if extra_runtime:
            print("\n⚠️  EXTRA (in pyproject.toml but not detected in code):")
            print("   (These might be optional dependencies or false negatives from pipreqs)")
            for pkg, spec in extra_runtime:
                print(f"   ? {pkg}{spec}")
    else:
        print("\n📦 Runtime Dependencies: ✅ All up to date!")

    # Dev dependencies
    missing_dev, extra_dev, changed_dev = compare_dependencies(
        current_dev_deps, dev_deps, "dev"
    )

    if missing_dev or extra_dev or changed_dev:
        print("\n🛠️  Dev Dependencies:")
        print("-" * 90)
        
        if missing_dev:
            print("\n❌ MISSING (detected in code but not in pyproject.toml):")
            for pkg, version_spec in missing_dev:
                print(f"   + {pkg}~={version_spec}")
        
        if changed_dev:
            print("\n🔄 VERSION UPDATES (detected different version or constraint):")
            for curr_pkg, curr_spec, new_pkg, new_spec in changed_dev:
                print(f"   ~ {curr_pkg}{curr_spec} → {new_pkg}{new_spec}")
        
        if extra_dev:
            print("\n⚠️  EXTRA (in pyproject.toml but not detected in code):")
            print("   (These might be optional dependencies or false negatives from pipreqs)")
            for pkg, spec in extra_dev:
                print(f"   ? {pkg}{spec}")
    else:
        print("\n🛠️  Dev Dependencies: ✅ All up to date!")

    print("\n" + "=" * 90)

    # Decide what to do
    has_changes = (missing_runtime or changed_runtime or missing_dev or changed_dev)
    
    if not has_changes:
        print("\n✅ No changes needed!")
        return

    if args.apply:
        print("\n⚙️  Applying changes to pyproject.toml...")
        project_name = args.project_name or project_root.name
        toml_data = update_project_section(toml_data, runtime_deps, dev_deps, project_name, args.version)
        output_text = dumps(toml_data)
        output_path.write_text(output_text, encoding="utf-8")
        print(f"✅ Updated {output_path.relative_to(project_root)}")
    else:
        print("\n💡 To apply these changes, run:")
        print(f"   python -m scripts.update_pyproject_toml --apply")
        if args.version:
            print(f"   python -m scripts.update_pyproject_toml --apply --version {args.version}")
        print("\n📝 Or edit pyproject.toml manually based on the recommendations above.")

if __name__ == "__main__":
    main()
