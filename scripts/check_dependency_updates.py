"""
Script to check if newer versions of dependencies are available on PyPI.
Reads dependencies from pyproject.toml and compares with latest versions.
Also displays currently installed versions.
"""
import sys
from pathlib import Path
from importlib import metadata

try:
    from tomlkit import parse
except ImportError:
    print("❌ tomlkit is required. Install it with: pip install tomlkit")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌ requests is required. Install it with: pip install requests")
    sys.exit(1)

def get_installed_version(package_name: str) -> str | None:
    """Get the currently installed version of a package."""
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return None


def get_latest_version_pypi(package_name: str) -> str | None:
    """Fetch the latest version of a package from PyPI."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["info"]["version"]
    except Exception as e:
        print(f"⚠️  Warning: Could not fetch version for {package_name}: {e}")
    return None


def parse_dependency(dep_string: str) -> tuple[str, str]:
    """Parse a dependency string like 'package==1.2.3' into (name, version)."""
    if "==" in dep_string:
        parts = dep_string.split("==")
        return parts[0].strip(), parts[1].strip()
    return dep_string.strip(), "unknown"


def compare_versions(current: str, latest: str) -> str:
    """Compare version strings and return status."""
    if current == latest:
        return "✅"
    
    # Simple version comparison (split by dots and compare)
    try:
        current_parts = [int(x) for x in current.split('.')]
        latest_parts = [int(x) for x in latest.split('.')]
        
        # Pad to same length
        max_len = max(len(current_parts), len(latest_parts))
        current_parts += [0] * (max_len - len(current_parts))
        latest_parts += [0] * (max_len - len(latest_parts))
        
        if current_parts < latest_parts:
            return "🔄"  # Update available
        elif current_parts > latest_parts:
            return "⚠️"  # Current is newer than PyPI (unusual)
        else:
            return "✅"
    except (ValueError, AttributeError):
        return "❓"


def check_dependencies(pyproject_path: Path) -> None:
    """Check all dependencies in pyproject.toml for updates."""
    if not pyproject_path.exists():
        print(f"❌ pyproject.toml not found at {pyproject_path}")
        sys.exit(1)
    
    with open(pyproject_path, 'r', encoding='utf-8') as f:
        toml_content = parse(f.read())
    
    project = toml_content.get("project", {})
    dependencies = project.get("dependencies", [])
    optional_deps = project.get("optional-dependencies", {})
    dev_deps = optional_deps.get("dev", [])
    
    print("=" * 105)
    print("🔍 Checking dependency versions against PyPI")
    print("=" * 105)
    
    # Check main dependencies
    if dependencies:
        print("\n📦 Runtime Dependencies:")
        print("-" * 105)
        print(f"{'Package':<25} {'pyproject.toml':<18} {'Installed':<18} {'Latest (PyPI)':<18} {'Status':<10}")
        print("-" * 105)
        
        updates_available = []
        not_installed = []
        for dep in dependencies:
            package_name, current_version = parse_dependency(dep)
            installed_version = get_installed_version(package_name)
            latest_version = get_latest_version_pypi(package_name)
            
            installed_str = installed_version if installed_version else "Not installed"
            latest_str = latest_version if latest_version else "N/A"
            
            if latest_version:
                status = compare_versions(current_version, latest_version)
                print(f"{package_name:<25} {current_version:<18} {installed_str:<18} {latest_str:<18} {status:<10}")
                
                if status == "🔄":
                    updates_available.append((package_name, current_version, latest_version))
                if not installed_version:
                    not_installed.append(package_name)
            else:
                print(f"{package_name:<25} {current_version:<18} {installed_str:<18} {latest_str:<18} {'❌':<10}")
    
    # Check dev dependencies
    if dev_deps:
        print("\n🛠️  Dev Dependencies:")
        print("-" * 105)
        print(f"{'Package':<25} {'pyproject.toml':<18} {'Installed':<18} {'Latest (PyPI)':<18} {'Status':<10}")
        print("-" * 105)
        
        dev_updates_available = []
        dev_not_installed = []
        for dep in dev_deps:
            package_name, current_version = parse_dependency(dep)
            installed_version = get_installed_version(package_name)
            latest_version = get_latest_version_pypi(package_name)
            
            installed_str = installed_version if installed_version else "Not installed"
            latest_str = latest_version if latest_version else "N/A"
            
            if latest_version:
                status = compare_versions(current_version, latest_version)
                print(f"{package_name:<25} {current_version:<18} {installed_str:<18} {latest_str:<18} {status:<10}")
                
                if status == "🔄":
                    dev_updates_available.append((package_name, current_version, latest_version))
                if not installed_version:
                    dev_not_installed.append(package_name)
            else:
                print(f"{package_name:<25} {current_version:<18} {installed_str:<18} {latest_str:<18} {'❌':<10}")
    
    # Summary
    print("\n" + "=" * 105)
    print("📊 Summary:")
    print("=" * 105)
    
    total_updates = len(updates_available) if dependencies else 0
    total_dev_updates = len(dev_updates_available) if dev_deps else 0
    
    if total_updates > 0:
        print(f"\n🔄 {total_updates} runtime dependency update(s) available:")
        for pkg, current, latest in updates_available:
            print(f"   • {pkg}: {current} → {latest}")
    
    if total_dev_updates > 0:
        print(f"\n🔄 {total_dev_updates} dev dependency update(s) available:")
        for pkg, current, latest in dev_updates_available:
            print(f"   • {pkg}: {current} → {latest}")
    
    if not_installed:
        print(f"\n⚠️  {len(not_installed)} runtime package(s) not installed:")
        for pkg in not_installed:
            print(f"   • {pkg}")
    
    if dev_not_installed:
        print(f"\n⚠️  {len(dev_not_installed)} dev package(s) not installed:")
        for pkg in dev_not_installed:
            print(f"   • {pkg}")
    
    if total_updates == 0 and total_dev_updates == 0:
        print("\n✅ All dependencies are up to date!")
    
    print("\n" + "=" * 105)
    print("Legend: ✅ Up to date  |  🔄 Update available  |  ⚠️ Ahead of PyPI  |  ❓ Cannot compare")
    print("=" * 105)


def main():
    """Main entry point."""
    # Find pyproject.toml in the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    pyproject_path = project_root / "pyproject.toml"
    
    print(f"📂 Project root: {project_root}")
    print(f"📄 Reading: {pyproject_path}\n")
    
    check_dependencies(pyproject_path)


if __name__ == "__main__":
    main()
