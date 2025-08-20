from json         import loads
from os           import path
from subprocess   import run as run_subprocess, TimeoutExpired, SubprocessError
from tempfile     import NamedTemporaryFile
from typing       import Any

from pmp_manip.config  import get_config
from pmp_manip.utility import (
    delete_file,
    MANIP_FailedFileWriteError, MANIP_FailedFileDeleteError, 
    MANIP_NoNodeJSInstalledError, 
    MANIP_ExtensionExecutionTimeoutError, MANIP_ExtensionExecutionErrorInJavascript, MANIP_UnexpectedExtensionExecutionError,
    MANIP_ExtensionJSONDecodeError, 
)

EXTRACTOR_PATH = path.join(path.dirname(__file__), "direct_extractor.js")
   

def extract_extension_info_directly(js_code: str, code_encoding: str = "utf-8") -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class based on the extension's javascript code,
    A node subprocess is run, which lets the outer code run and then calls and logs the return value of the getInfo method of the extension class.
    ONLY USE THIS IF THE CODE IS FROM A TRUSTED SOURCE LIKE extensions.penguinmod.com/.
    OTHERWISE THE CODE CAN MESS WITH YOUR DEVICE
    
    Args:
        js_code: the full JS code of the extension.
        code_encoding: the text encoding of `js_code`

    Raises:
        MANIP_FailedFileWriteError(unlikely): if the JS code could not be written to a temporary file (eg. OS Error or Unicode Error)
        MANIP_FailedFileDeleteError(unlikely): if the temporary Javscript file could not be deleted
        MANIP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
        MANIP_ExtensionExecutionTimeoutError: if the Node.js execution subprocess took too long
        MANIP_ExtensionExecutionErrorInJavascript: if an error occurs inside the actual extension code
        MANIP_UnexpectedExtensionExecutionError: if some other error raises during the subprocess call (eg. Permission or OS Error)
        MANIP_ExtensionJSONDecodeError(unlikely): if the json output of the subprocess is invalid
    """
    try:
        with NamedTemporaryFile(
            mode="w", suffix=".js", 
            encoding=code_encoding, delete=False,
        ) as temp_file:
            temp_file.write(js_code)
            temp_js_path = temp_file.name

    except (FileNotFoundError, OSError, PermissionError, UnicodeEncodeError) as error:
        raise MANIP_FailedFileWriteError(f"Failed to create or write javascript code to temporary file: {error}") from error
    
    try:
        result = run_subprocess(
            ["node", EXTRACTOR_PATH, temp_js_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=get_config().ext_info_gen.node_js_exec_timeout,
        )
    except FileNotFoundError as error: # when python can not find the node executable
        raise MANIP_NoNodeJSInstalledError(f"Node.js is not installed or not found in PATH: {error}") from error
    except TimeoutExpired as error:
        raise MANIP_ExtensionExecutionTimeoutError(f"Node.js subprocess trying to execute extension code took too long: {error}") from error
    except (SubprocessError, OSError, PermissionError) as error:
        raise MANIP_UnexpectedExtensionExecutionError(f"Failed to run Node.js subprocess (to execute extension code): {error}") from error
    finally:
        try:
            delete_file(temp_js_path)
        except MANIP_FailedFileDeleteError as error:
            raise MANIP_FailedFileDeleteError(f"Failed to remove temporary javascript file at {temp_js_path!r}: {error}") from error

    if result.returncode != 0:
        if   result.returncode == 1:
            # Registration error
            raise MANIP_ExtensionExecutionErrorInJavascript(f"Extension was not registered. This is the fault of the extension developer")
        else:  # result.returncode == 2 or others
            # Script execution error
            raise MANIP_ExtensionExecutionErrorInJavascript(f"Error in extension javascript execution: {result.stderr}")

    try:
        extension_info = loads(result.stdout.strip().splitlines()[-1])  # last line = JSON
    except Exception as error:
        raise MANIP_ExtensionJSONDecodeError(f"Invalid Extension Info JSON returned from Node.js subprocess: {error}") from error

    return extension_info


__all__ = ["extract_extension_info_directly"]


