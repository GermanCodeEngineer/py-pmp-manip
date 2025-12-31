from io import BytesIO
from pathlib import Path
from pytest import raises, MonkeyPatch
from subprocess import CompletedProcess, TimeoutExpired, SubprocessError
from tempfile import TemporaryDirectory
from typing import Any
from unittest.mock import Mock, MagicMock
from requests import RequestException, HTTPError

from pmp_manip.project_api.api import (
    SCRATCH_API, PENGUINMOD_API,
    fetch_frontpage, fetch_projects,
)

from pmp_manip.utility import (
    MANIP_NoNodeJSInstalledError,
    MANIP_SubprocessTimeoutError,
    MANIP_UnexpectedSubprocessError,
)


# ============================================================================
# Test fetch_frontpage - Success cases
# ============================================================================

def test_fetch_frontpage_success_default_api(monkeypatch: MonkeyPatch):
    """Test fetching front page with default PenguinMod API"""
    expected_data = {
        "featured": ["123", "456"],
        "voted": ["789", "012"],
    }
    
    def mock_get(url, timeout=None):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_response.raise_for_status.return_value = None
        return mock_response
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "requests_get", mock_get)
    
    result = fetch_frontpage()
    assert result == expected_data


def test_fetch_frontpage_success_custom_api(monkeypatch: MonkeyPatch):
    """Test fetching front page with custom API URL"""
    custom_api = "https://custom.api.com/v1"
    expected_data = {"projects": ["abc", "def"]}
    
    def mock_get(url, timeout=None):
        assert url == f"{custom_api}/projects/frontPage"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_response.raise_for_status.return_value = None
        return mock_response
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "requests_get", mock_get)
    
    result = fetch_frontpage(api_url=custom_api)
    assert result == expected_data


def test_fetch_frontpage_success_custom_timeout(monkeypatch: MonkeyPatch):
    """Test fetching front page with custom timeout"""
    custom_timeout = 60
    
    def mock_get(url, timeout=None):
        assert timeout == custom_timeout
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        return mock_response
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "requests_get", mock_get)
    
    result = fetch_frontpage(timeout=custom_timeout)
    assert result == {}


# ============================================================================
# Test fetch_frontpage - Error cases
# ============================================================================

def test_fetch_frontpage_http_error(monkeypatch: MonkeyPatch):
    """Test fetch_frontpage with HTTP error"""
    def mock_get(url, timeout=None):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        return mock_response
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "requests_get", mock_get)
    
    with raises(RequestException, match="Failed to fetch front page"):
        fetch_frontpage()


def test_fetch_frontpage_network_error(monkeypatch: MonkeyPatch):
    """Test fetch_frontpage with network error"""
    def mock_get(url, timeout=None):
        raise RequestException("Connection error")
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "requests_get", mock_get)
    
    with raises(RequestException, match="Failed to fetch front page"):
        fetch_frontpage()


def test_fetch_frontpage_invalid_json(monkeypatch: MonkeyPatch):
    """Test fetch_frontpage with invalid JSON response"""
    def mock_get(url, timeout=None):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        return mock_response
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "requests_get", mock_get)
    
    with raises(ValueError, match="Invalid JSON response"):
        fetch_frontpage()


# ============================================================================
# Test fetch_projects - Success cases
# ============================================================================

def test_fetch_projects_single_success(monkeypatch: MonkeyPatch):
    """Test fetching a single project successfully"""
    project_id = "123456"
    project_data = b"PK\x03\x04project data here"
    
    def mock_run(cmd, **kwargs):
        # Verify command structure
        assert cmd[0] == "node"
        assert cmd[2] == PENGUINMOD_API
        assert cmd[3] == "projects"
        assert project_id in cmd
        
        # Create a fake project file in the temp directory
        temp_dir = cmd[-1]
        project_file = Path(temp_dir) / f"project_{project_id}.pmp"
        with open(project_file, "wb") as f:
            f.write(project_data)
        
        return CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="Success",
            stderr=""
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects([project_id])
    
    assert error is None
    assert project_id in results
    assert results[project_id].read() == project_data


def test_fetch_projects_multiple_success(monkeypatch: MonkeyPatch):
    """Test fetching multiple projects successfully"""
    project_ids = ["111", "222", "333"]
    project_data = {id: f"data_{id}".encode() for id in project_ids}
    
    def mock_run(cmd, **kwargs):
        temp_dir = cmd[-1]
        for pid in project_ids:
            project_file = Path(temp_dir) / f"project_{pid}.pmp"
            with open(project_file, "wb") as f:
                f.write(project_data[pid])
        
        return CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="Success",
            stderr=""
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects(project_ids)
    
    assert error is None
    assert len(results) == 3
    for pid in project_ids:
        assert pid in results
        assert results[pid].read() == project_data[pid]


def test_fetch_projects_custom_api(monkeypatch: MonkeyPatch):
    """Test fetching projects with custom API URL"""
    custom_api = "https://custom.api.com/v1"
    project_id = "789"
    
    def mock_run(cmd, **kwargs):
        assert cmd[2] == custom_api
        temp_dir = cmd[-1]
        project_file = Path(temp_dir) / f"project_{project_id}.pmp"
        with open(project_file, "wb") as f:
            f.write(b"data")
        
        return CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="",
            stderr=""
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects([project_id], api_url=custom_api)
    assert error is None
    assert project_id in results


def test_fetch_projects_partial_success(monkeypatch: MonkeyPatch):
    """Test fetching projects where some succeed and some fail"""
    project_ids = ["111", "222", "333"]
    # Only create files for first two projects
    successful_ids = ["111", "222"]
    
    def mock_run(cmd, **kwargs):
        temp_dir = cmd[-1]
        for pid in successful_ids:
            project_file = Path(temp_dir) / f"project_{pid}.pmp"
            with open(project_file, "wb") as f:
                f.write(f"data_{pid}".encode())
        
        return CompletedProcess(
            args=cmd,
            returncode=1,
            stdout="",
            stderr="Error: Project 333 not found"
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects(project_ids)
    
    # Should return successful projects even if some failed
    assert len(results) == 2
    assert "111" in results
    assert "222" in results
    assert "333" not in results
    
    # Should return an error since returncode was 1
    assert error is not None
    assert isinstance(error, MANIP_UnexpectedSubprocessError)
    assert "Project 333 not found" in str(error)


def test_fetch_projects_custom_timeouts(monkeypatch: MonkeyPatch):
    """Test fetch_projects with custom timeout values"""
    project_ids = ["111", "222"]
    timeout_base = 60
    timeout_per_project = 20
    expected_timeout = timeout_base + (timeout_per_project * len(project_ids))
    
    def mock_run(cmd, timeout=None, **kwargs):
        assert timeout == expected_timeout
        temp_dir = cmd[-1]
        for pid in project_ids:
            project_file = Path(temp_dir) / f"project_{pid}.pmp"
            with open(project_file, "wb") as f:
                f.write(b"data")
        
        return CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="",
            stderr=""
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects(
        project_ids,
        timeout_base=timeout_base,
        timeout_per_project=timeout_per_project
    )
    assert error is None
    assert len(results) == 2


# ============================================================================
# Test fetch_projects - Error cases
# ============================================================================

def test_fetch_projects_no_nodejs(monkeypatch: MonkeyPatch):
    """Test fetch_projects when Node.js is not installed"""
    def mock_run(cmd, **kwargs):
        raise FileNotFoundError("node not found")
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    with raises(MANIP_NoNodeJSInstalledError, match="Node.js is not installed"):
        fetch_projects(["123"])


def test_fetch_projects_timeout(monkeypatch: MonkeyPatch):
    """Test fetch_projects when subprocess times out"""
    def mock_run(cmd, **kwargs):
        raise TimeoutExpired(cmd, timeout=30)
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    with raises(MANIP_SubprocessTimeoutError, match="Node.js subprocess took too long"):
        fetch_projects(["123"])


def test_fetch_projects_subprocess_error(monkeypatch: MonkeyPatch):
    """Test fetch_projects with subprocess error"""
    def mock_run(cmd, **kwargs):
        raise SubprocessError("Subprocess failed")
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    with raises(MANIP_UnexpectedSubprocessError, match="Failed to run Node.js subprocess"):
        fetch_projects(["123"])


def test_fetch_projects_os_error(monkeypatch: MonkeyPatch):
    """Test fetch_projects with OS error"""
    def mock_run(cmd, **kwargs):
        raise OSError("OS error occurred")
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    with raises(MANIP_UnexpectedSubprocessError, match="Failed to run Node.js subprocess"):
        fetch_projects(["123"])


def test_fetch_projects_permission_error(monkeypatch: MonkeyPatch):
    """Test fetch_projects with permission error"""
    def mock_run(cmd, **kwargs):
        raise PermissionError("Permission denied")
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    with raises(MANIP_UnexpectedSubprocessError, match="Failed to run Node.js subprocess"):
        fetch_projects(["123"])


def test_fetch_projects_all_failed(monkeypatch: MonkeyPatch):
    """Test fetch_projects when all projects fail to download"""
    project_ids = ["111", "222"]
    
    def mock_run(cmd, **kwargs):
        # Don't create any files (all downloads failed)
        return CompletedProcess(
            args=cmd,
            returncode=1,
            stdout="",
            stderr="All projects failed to download"
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects(project_ids)
    
    assert len(results) == 0
    assert error is not None
    assert isinstance(error, MANIP_UnexpectedSubprocessError)


def test_fetch_projects_file_read_error_oserror(monkeypatch: MonkeyPatch):
    """Test fetch_projects when a project file can't be read due to OSError"""
    project_ids = ["111", "222"]
    
    def mock_run(cmd, **kwargs):
        temp_dir = cmd[-1]
        # Create first file normally
        project_file1 = Path(temp_dir) / f"project_111.pmp"
        with open(project_file1, "wb") as f:
            f.write(b"data1")
        
        # Create second file to simulate existence
        project_file2 = Path(temp_dir) / f"project_222.pmp"
        project_file2.touch()
        
        return CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="",
            stderr=""
        )
    
    import pmp_manip.project_api.api as api_mod
    
    # Mock the open function to raise OSError for the second file
    original_open = open
    def mock_open(file, *args, **kwargs):
        if "project_222.pmp" in str(file):
            raise OSError("Disk read error")
        return original_open(file, *args, **kwargs)
    
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    monkeypatch.setattr("builtins.open", mock_open)
    
    results, error = fetch_projects(project_ids)
    
    # Should have only the readable project, the one with OSError should be skipped
    assert len(results) == 1
    assert "111" in results
    assert "222" not in results
    assert error is None


def test_fetch_projects_file_read_error_permission(monkeypatch: MonkeyPatch):
    """Test fetch_projects when a project file can't be read due to PermissionError"""
    project_ids = ["333", "444"]
    
    def mock_run(cmd, **kwargs):
        temp_dir = cmd[-1]
        # Create first file normally
        project_file1 = Path(temp_dir) / f"project_333.pmp"
        with open(project_file1, "wb") as f:
            f.write(b"data3")
        
        # Create second file to simulate existence
        project_file2 = Path(temp_dir) / f"project_444.pmp"
        project_file2.touch()
        
        return CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="",
            stderr=""
        )
    
    import pmp_manip.project_api.api as api_mod
    
    # Mock the open function to raise PermissionError for the second file
    original_open = open
    def mock_open(file, *args, **kwargs):
        if "project_444.pmp" in str(file):
            raise PermissionError("Access denied")
        return original_open(file, *args, **kwargs)
    
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    monkeypatch.setattr("builtins.open", mock_open)
    
    results, error = fetch_projects(project_ids)
    
    # Should have only the readable project, the one with PermissionError should be skipped
    assert len(results) == 1
    assert "333" in results
    assert "444" not in results
    assert error is None


# ============================================================================
# Test constants
# ============================================================================

def test_api_constants():
    """Test that API constants are defined correctly"""
    assert SCRATCH_API == "https://projects.scratch.mit.edu"
    assert PENGUINMOD_API == "https://projects.penguinmod.com/api/v1"


# ============================================================================
# Test edge cases
# ============================================================================

def test_fetch_projects_empty_list(monkeypatch: MonkeyPatch):
    """Test fetch_projects with empty project list"""
    def mock_run(cmd, **kwargs):
        return CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="",
            stderr=""
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects([])
    assert len(results) == 0
    assert error is None


def test_fetch_projects_bytesio_position_reset(monkeypatch: MonkeyPatch):
    """Test that BytesIO objects are at position 0 after creation"""
    project_id = "123"
    project_data = b"test data"
    
    def mock_run(cmd, **kwargs):
        temp_dir = cmd[-1]
        project_file = Path(temp_dir) / f"project_{project_id}.pmp"
        with open(project_file, "wb") as f:
            f.write(project_data)
        
        return CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="",
            stderr=""
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects([project_id])
    
    assert project_id in results
    # BytesIO should be at position 0, so read() should return all data
    assert results[project_id].read() == project_data
    # After reading, position should be at the end
    assert results[project_id].tell() == len(project_data)
    # Reset and read again
    results[project_id].seek(0)
    assert results[project_id].read() == project_data


# ============================================================================
# Integration-style tests (more comprehensive scenarios)
# ============================================================================

def test_fetch_projects_realistic_scenario(monkeypatch: MonkeyPatch):
    """Test a realistic scenario with multiple projects and mixed results"""
    project_ids = ["001", "002", "003", "004", "005"]
    successful_ids = ["001", "002", "004"]  # 003 and 005 will fail
    
    project_contents = {
        "001": b"PK\x03\x04small_project",
        "002": b"PK\x03\x04large_project_with_lots_of_data" * 100,
        "004": b"PK\x03\x04medium_project",
    }
    
    def mock_run(cmd, **kwargs):
        # Verify command structure
        assert cmd[0] == "node"
        assert len(cmd) >= 5
        assert cmd[3] == "projects"
        
        temp_dir = cmd[-1]
        for pid in successful_ids:
            project_file = Path(temp_dir) / f"project_{pid}.pmp"
            with open(project_file, "wb") as f:
                f.write(project_contents[pid])
        
        return CompletedProcess(
            args=cmd,
            returncode=1,
            stdout="3/5 projects downloaded",
            stderr="Failed to fetch projects 003, 005"
        )
    
    import pmp_manip.project_api.api as api_mod
    monkeypatch.setattr(api_mod, "run_subprocess", mock_run)
    
    results, error = fetch_projects(project_ids)
    
    # Check successful downloads
    assert len(results) == 3
    for pid in successful_ids:
        assert pid in results
        assert results[pid].read() == project_contents[pid]
    
    # Check failed projects are not in results
    assert "003" not in results
    assert "005" not in results
    
    # Check error is reported
    assert error is not None
    assert "Failed to fetch projects" in str(error)
