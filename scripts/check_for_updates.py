import requests
from datetime import datetime, timezone

files_to_check = [
    (
        "2025-09-16", 
        "https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/extension-support/tw-extension-api-common.js",
        "Update the Scratch Object stub in pmp_manip/ext_info_gen/direct_extractor.js and safe_extractor.py",
    ),
    (
        "2025-09-04",
        "https://github.com/PenguinMod/penguinmod.github.io/blob/develop/src/containers/tw-security-manager.jsx",
        "Update handler for trusted sources in pmp_manip/ext_info_gen/manager.py",
    ),
    (
        "2025-10-04",
        "https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/extension-support/extension-manager.js",
        "Update BUILTIN_EXTENSIONS in pmp_manip/opcode_info/api/main.py",
    ),
    (
        "2025-09-07",
        "https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/extensions/",
        "Ensure all builtin extensions are still compatible",
    ),
    (
        "2025-09-04",
        "https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/util/",
        "Update util stub in overwritten require function",
    ),   
    (
        "2025-09-16",
        "https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/serialization/",
        "Ensure project deserialization still works reliably",
    ),
    (
        "2025-09-09",
        "https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/engine/runtime.js",
        "Update vm stub in pmp_manip/ext_info_gen/direct_extractor.js"
    ),
    (
        "2025-09-15",
        "https://github.com/PenguinMod/PenguinMod-Docs/blob/353d492f491ee7b1e7c7bf34e48f39d43fceea17/docs/development/extensions/api/blocks/basic.md",
        "Update KNOWN_BLOCK_INFO_ATTRS in pmp_manip/ext_info_gen/generator.py",
    ),
]

API_BASE = "https://api.github.com/repos"


def parse_github_url(url):
    """Extract owner, repo, branch, and file/directory path from a GitHub blob/tree URL."""
    parts = url.split("github.com/")[1].split("/")
    owner, repo, type_, branch = parts[:4]

    if type_ not in ("blob", "tree"):
        raise ValueError(f"Unsupported GitHub URL type: {type_}")

    path = "/".join(parts[4:])
    return owner, repo, branch, path


def get_last_commit_date(owner, repo, branch, path):
    """Get the last commit date for a file or directory using GitHub API."""
    url = f"{API_BASE}/{owner}/{repo}/commits"
    params = {"path": path, "sha": branch, "per_page": 1}
    response = requests.get(url, params=params)
    response.raise_for_status()
    commits = response.json()
    if not commits:
        return None
    return commits[0]["commit"]["committer"]["date"]


def check_files(files) -> bool:
    all_good = True
    for last_checked, url, todo_message in files:
        owner, repo, branch, path = parse_github_url(url)
        commit_date_str = get_last_commit_date(owner, repo, branch, path)
        if not commit_date_str:
            print(f"⚠️  No commits found for {url}")
            continue

        commit_date = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))
        last_checked_dt = datetime.fromisoformat(last_checked).replace(tzinfo=timezone.utc)

        if commit_date > last_checked_dt:
            print(f"🚨 {url} has changed since {last_checked} (last commit: {commit_date.date()})")
            print(f"🚨 Resulting TODO: {todo_message}")
            all_good = False
    return all_good


if __name__ == "__main__":
    all_up_to_date = check_files(files_to_check)
    if all_up_to_date:
        print("✅ All files/directories up-to-date!")
