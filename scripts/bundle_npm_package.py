import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def bundle_npm_package(
    package_name: str,
    output_dir: Path,
    output_name: str
) -> None:
    """
    Download an npm package, extract its main JS file, and copy it to the output directory as a single file.
    """
    print(f"Bundling npm package '{package_name}'...")
    with tempfile.TemporaryDirectory(prefix="npm_bundle_") as temp_dir_str:
        temp_dir = Path(temp_dir_str)

        # On Windows, use shell=True so npm is found in PATH
        is_windows = sys.platform.startswith("win")
        npm_init_cmd = "npm init -y" if is_windows else ["npm", "init", "-y"]
        npm_install_cmd = f"npm install {package_name}" if is_windows else ["npm", "install", package_name]

        subprocess.run(npm_init_cmd, cwd=str(temp_dir), check=True, shell=is_windows)
        subprocess.run(npm_install_cmd, cwd=str(temp_dir), check=True, shell=is_windows)

        # Locate the package.json for the installed package
        node_modules = temp_dir / "node_modules"
        package_dir = node_modules / package_name
        package_json_path = package_dir / "package.json"

        # Read the main entry point from package.json (default to index.js)
        with package_json_path.open(encoding="utf-8") as f:
            pkg_info = json.load(f)
        main_file = pkg_info.get("main", "index.js")
        main_path = package_dir / main_file

        # Detect file type
        if main_path.suffix == ".json":
            # Distribute as JSON
            data = main_path.read_bytes()
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / (output_name if output_name.endswith(".json") else output_name + ".json")
            output_path.write_bytes(data)
            print(f"Bundled JSON file saved to {output_path}")
        else:
            # Use esbuild to bundle JS and all dependencies
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = (output_dir / (output_name if output_name.endswith(".js") else output_name + ".js")).resolve()
            is_windows = sys.platform.startswith("win")
            esbuild_cmd = (
                f"npx esbuild {main_path} --bundle --platform=node --outfile={output_path}"
                if is_windows else
                ["npx", "esbuild", str(main_path), "--bundle", "--platform=node", f"--outfile={output_path}"]
            )
            print(f"Bundling with esbuild: {esbuild_cmd}")
            subprocess.run(esbuild_cmd, cwd=str(temp_dir), check=True, shell=is_windows)
            print(f"Bundled JS file (with deps) saved to {output_path}")

def main() -> None:

    parser = argparse.ArgumentParser(description="Bundle a single-file JS from an npm package for pip distribution.")
    subparsers = parser.add_subparsers(dest="command", required=False)

    # Default/manual subcommand
    parser_bundle = subparsers.add_parser("bundle", help="Bundle a specified npm package")
    parser_bundle.add_argument("package", help="NPM package name (e.g. lodash)")
    parser_bundle.add_argument("--output-dir", default=None, help="Output directory for bundled JS file")
    parser_bundle.add_argument("--output-name", default=None, help="Output JS file name (default: <package>.js)")

    # Predefined compile subcommand
    parser_compile = subparsers.add_parser("build-all", help="Bundle with predefined parameters")

    args = parser.parse_args()

    if (args.command == "build-all") or (args.command is None):
        # Example: add your predefined packages here
        all = [
            {"package": "scratch-translate-extension-languages"},
            {"package": "argparse"},
            {"package": "jszip"},
            {"package": "pmp-protobuf"},
        ]
        output_dir = Path("pmp_manip") / "minified_node_packages"
        for entry in all:
            bundle_npm_package(entry["package"], output_dir, entry["package"].replace('/', '_'))

    elif args.command == "bundle":
        # Default/manual mode
        package = args.package
        output_dir = args.output_dir if args.output_dir is not None else str(Path("pmp_manip") / "minified_node_packages")
        output_name = args.output_name if args.output_name is not None else f"{package.replace('/', '_')}"
        bundle_npm_package(package, Path(output_dir), output_name)

if __name__ == "__main__":
    main()
