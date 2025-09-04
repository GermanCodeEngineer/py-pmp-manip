import requests
from datetime import datetime, timezone

files_to_check = [
    (
        "2025-09-03", 
        "https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/extension-support/tw-extension-api-common.js",
        "Update the Scratch Object stub in pmp_manip/ext_info_gen/direct_extractor.js and safe_extractor.py",
    ),
    (
        "2025-09-04",
        "https://github.com/PenguinMod/penguinmod.github.io/blob/develop/src/containers/tw-security-manager.jsx",
        "Update pmp_manip/ext_info_gen/manager.py",
    ),
    (
        "2025-09-04",
        "https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/extension-support/extension-manager.js",
        "Update BUILTIN_EXT_TO_DIR in pmp_manip/opcode_info/api/main.py",
    ),
]

API_BASE = "https://api.github.com/repos"

def parse_github_url(url):
    """Extract owner, repo, branch, and file path from a GitHub file URL."""
    parts = url.split("github.com/")[1].split("/")
    owner, repo, blob, branch = parts[:4]
    filepath = "/".join(parts[4:])
    return owner, repo, branch, filepath

def get_last_commit_date(owner, repo, branch, filepath):
    """Get the last commit date for a file using GitHub API."""
    url = f"{API_BASE}/{owner}/{repo}/commits"
    params = {"path": filepath, "sha": branch, "per_page": 1}
    response = requests.get(url, params=params)
    response.raise_for_status()
    commits = response.json()
    if not commits:
        return None
    return commits[0]["commit"]["committer"]["date"]

def check_files(files) -> bool:
    for last_checked, url, todo_message in files:
        owner, repo, branch, filepath = parse_github_url(url)
        commit_date_str = get_last_commit_date(owner, repo, branch, filepath)
        if not commit_date_str:
            print(f"⚠️  No commits found for {url}")
            continue

        commit_date = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))
        # Make last_checked timezone-aware (UTC)
        last_checked_dt = datetime.fromisoformat(last_checked).replace(tzinfo=timezone.utc)

        if commit_date > last_checked_dt:
            print(f"🚨 {url} has changed since {last_checked} (last commit: {commit_date.date()})")
            print(f"🚨 Resulting TODO: {todo_message}")
            return False
    return True

if __name__ == "__main__":
    all_up_to_date = check_files(files_to_check)
    if all_up_to_date:
        print("✅ All files up-to-date!")
