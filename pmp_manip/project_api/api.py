# Inspired by PangAPI:
# https://github.com/PenguinMod/PenguinMod-ExtensionsGallery/blob/main/static/extensions/SammerLOL/pangapi.js

from __future__ import annotations
from io         import BytesIO
from pathlib    import Path
from requests   import get as requests_get, RequestException
from subprocess import run as run_subprocess, TimeoutExpired, SubprocessError
from tempfile   import TemporaryDirectory
from typing     import Any

from pmp_manip.utility import (
    enforce_argument_types,
    MANIP_NoNodeJSInstalledError, MANIP_SubprocessTimeoutError, MANIP_UnexpectedSubprocessError
)

SCRATCH_API = "https://projects.scratch.mit.edu"
PENGUINMOD_API = "https://projects.penguinmod.com/api/v1"
API_JS_PATH = Path(__file__).parent / "api.js"

@enforce_argument_types
def fetch_frontpage(api_url: str = PENGUINMOD_API, timeout=30) -> dict[str, Any]:
    """
    Fetch the front page data from PenguinMod API.
    
    Args:
        api_url: the base API URL (the scratch API does NOT work here)
        timeout: timeout in seconds for the request

    Raises:
        RequestException: if the request fails
        ValueError: if the response is not valid JSON
    """
    url = f"{api_url}/projects/frontPage"
    
    try:
        response = requests_get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except RequestException as error:
        raise RequestException(f"Failed to fetch front page from {url}: {error}") from error
    except ValueError as error:
        raise ValueError(f"Invalid JSON response from front page endpoint: {error}") from error


@enforce_argument_types
def fetch_projects(
        project_ids: list[str], api_url: str = PENGUINMOD_API,
        timeout_base: int = 30, timeout_per_project: int = 10
    ) -> tuple[dict[str, BytesIO], MANIP_UnexpectedSubprocessError | None]:
    """
    Fetch multiple PenguinMod projects in parallel by ID using a Node.js subprocess.
    Returns a dictionary mapping project IDs to their bytes buffers.
    
    Args:
        project_ids: list of project IDs to fetch (e.g. ["0131435715", "9876543210"])
        api_url: the base API URL
        timeout_base: base timeout in seconds for the subprocess
        timeout_per_project: additional timeout in seconds per project

    Returns:
        Dictionary mapping project IDs to BytesIO objects for successfully fetched projects and an optional error if some projects failed.

    Raises:
        MANIP_FailedFileWriteError(unlikely): if the temporary directory could not be created
        MANIP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
        MANIP_SubprocessTimeoutError: if the Node.js subprocess took too long
        MANIP_UnexpectedSubprocessError: if some error occurs during the subprocess call
    """
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        cmd = ["node", str(API_JS_PATH), api_url, "projects", *project_ids, "-o", str(temp_path)]
        
        try:
            result = run_subprocess(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout_base + (timeout_per_project * len(project_ids)),
            )
        except FileNotFoundError as error:
            raise MANIP_NoNodeJSInstalledError(f"Node.js is not installed or not found in PATH: {error}") from error
        except TimeoutExpired as error:
            raise MANIP_SubprocessTimeoutError(f"Node.js subprocess took too long: {error}") from error
        except (SubprocessError, OSError, PermissionError) as error:
            raise MANIP_UnexpectedSubprocessError(f"Failed to run Node.js subprocess (to fetch projects): {error}") from error
        
        # Read all successfully fetched projects
        results = {}
        for project_id in project_ids:
            project_file = temp_path / f"project_{project_id}.pmp"
            if project_file.exists():
                try:
                    with open(project_file, "rb") as file:
                        results[project_id] = BytesIO(file.read())
                except (OSError, PermissionError) as error:
                    # Skip files that can't be read
                    pass
        
        if result.returncode == 0:
            return (results, None)
        else:
            return (results, MANIP_UnexpectedSubprocessError(f"Error while fetching project: {result.stderr}"))


__all__ = ["SCRATCH_API", "PENGUINMOD_API", "fetch_frontpage", "fetch_projects"]

