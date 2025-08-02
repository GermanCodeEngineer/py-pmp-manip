from json         import loads
from subprocess   import run as run_subprocess, TimeoutExpired, SubprocessError
from tempfile     import NamedTemporaryFile
from typing       import Any

from pmp_manip.config  import get_config
from pmp_manip.utility import (
    delete_file,
    PP_FailedFileWriteError, PP_FailedFileDeleteError, 
    PP_NoNodeJSInstalledError, 
    PP_ExtensionExecutionTimeoutError, PP_ExtensionExecutionErrorInJavascript, PP_UnexpectedExtensionExecutionError,
    PP_ExtensionJSONDecodeError, PP_UnknownExtensionAttributeError, 
)

EXTRACTOR_PATH = "pypenguin/ext_info_gen/extractor.js"
   

def extract_extension_info(js_code: str, code_encoding: str = "utf-8") -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class based on the extension's javascript code,
    A node subprocess is run, which lets the outer code run and then calls and logs the return value of the getInfo method of the extension class.
    ONLY USE THIS IF THE CODE IS FROM A TRUSTED SOURCE LIKE extensions.penguinmod.com/.
    OTHERWISE THE CODE CAN MESS WITH YOUR DEVICE
    
    Args:
        js_code: the full JS code of the extension.
        code_encoding: the text encoding of `js_code`

    Raises:
        PP_FailedFileWriteError: if the JS code couldn't be written to a temporary file (eg. OS Error or Unicode Error)
        PP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
        PP_ExtensionExecutionTimeoutError: if the Node.js execution subprocess took too long

    """
    try:
        with NamedTemporaryFile(
            mode="w", suffix=".js", 
            encoding=code_encoding, delete=False,
        ) as temp_file:
            temp_file.write(js_code)
            temp_js_path = temp_file.name

    except UnicodeDecodeError as error:
        raise PP_FailedFileWriteError(f"Failed to create or write javascript code to temporary file because of encoding failure: {error}") from error
    except (FileNotFoundError, OSError, PermissionError, IsADirectoryError, Exception) as error:
        raise PP_FailedFileWriteError(f"Failed to create or write javascript code to temporary file: {error}") from error
    
    try:
        print("--> Executing JavaScript via Node.js")
        result = run_subprocess(
            ["node", EXTRACTOR_PATH, temp_js_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=get_config().ext_info_gen.node_js_exec_timeout,
        )
    except FileNotFoundError as error: # when python can't find the node executable
        raise PP_NoNodeJSInstalledError(f"Node.js is not installed or not found in PATH: {error}") from error
    except TimeoutExpired as error:
        raise PP_ExtensionExecutionTimeoutError(f"Node.js subprocess trying to execute extension code took too long: {error}") from error
    except (SubprocessError, OSError, PermissionError, Exception) as error:
        # TODO: add detailed response handling
        raise PP_UnexpectedExtensionExecutionError(f"Failed to run Node.js subprocess (to execute extension code): {error}") from error
    finally:
        try:
            delete_file(temp_js_path)
        except PP_FailedFileDeleteError as error:
            raise PP_FailedFileWriteError(f"Failed to remove temporary javascript file at {repr(temp_js_path)}: {error}") from error

    if result.returncode != 0:
        raise PP_ExtensionExecutionErrorInJavascript(f"Error in javascript execution: {result.stderr}")

    try:
        extension_info = loads(result.stdout.strip().splitlines()[-1])  # last line = JSON
    except Exception as error:
        raise PP_ExtensionJSONDecodeError(f"Invalid JSON output from container: {error}") from error

    for attr in extension_info.keys():
        if attr not in {
            "name", "color1", "color2", "color3", "menuIconURI",
            "docsURI", "isDynamic", "id", "blocks", "menus"
        }:
            raise PP_UnknownExtensionAttributeError(attr)

    return extension_info


__all__ = ["extract_getinfo"]


