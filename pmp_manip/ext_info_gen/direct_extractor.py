from json         import loads, dumps
from os           import path
from subprocess   import run as run_subprocess, TimeoutExpired, SubprocessError
from tempfile     import TemporaryDirectory
from typing       import Any

from pmp_manip.config  import get_config
from pmp_manip.utility import (
    write_file_text, delete_directory,
    MANIP_ValueError, MANIP_FailedFileWriteError, MANIP_FailedFileDeleteError, 
    MANIP_NoNodeJSInstalledError, 
    MANIP_ExtensionExecutionTimeoutError, MANIP_ExtensionExecutionErrorInJavascript, MANIP_UnexpectedExtensionExecutionError,
    MANIP_ExtensionJSONDecodeError, 
)

EXTRACTOR_PATH = path.join(path.dirname(__file__), "direct_extractor.js")
   

def extract_extension_info_directly(
    js_files: dict[str, str],
    main_file_name: str = "index.js",
    code_encoding: str = "utf-8",
) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class based on the extension's javascript code,
    A node subprocess is run, which lets the outer code run and then calls and logs the return value of the getInfo method of the extension class.
    ONLY USE THIS IF THE CODE IS FROM A TRUSTED SOURCE LIKE extensions.penguinmod.com/.
    OTHERWISE THE CODE CAN MESS WITH YOUR DEVICE
    
    Args:
        js_files: all extension JS code file names and contents (only builtin extensions use multiple)
        main_file_name: the file name of the main JS code file in `js_file` 
        code_encoding: the text encoding of the code files

    Raises:
        MANIP_ValueError: if `main_file_name` is not a file name in `js_files`
        MANIP_FailedFileWriteError(unlikely): if the JS code could not be written to a temporary file (eg. OS Error or Unicode Error)
        MANIP_FailedFileDeleteError(unlikely): if the temporary Javscript file could not be deleted
        MANIP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
        MANIP_ExtensionExecutionTimeoutError: if the Node.js execution subprocess took too long
        MANIP_ExtensionExecutionErrorInJavascript: if an error occurs inside the actual extension code
        MANIP_UnexpectedExtensionExecutionError: if some other error raises during the subprocess call (eg. Permission or OS Error)
        MANIP_ExtensionJSONDecodeError(unlikely): if the json output of the subprocess is invalid
    """
    if main_file_name not in js_files:
        raise MANIP_ValueError(f"'main_file_name' {main_file_name!r} must be a file name in 'js_files'. Keys of js_files: {list(js_files.keys())}")
    try:
        with TemporaryDirectory(delete=False) as temp_dir_path:
        #temp_dir_path = "extension"; from os import makedirs
        #try: makedirs(temp_dir_path)
        #except: pass
        #if True:
            main_file_path = path.join(temp_dir_path, main_file_name)
            for file_name, content in js_files.items():
                write_file_text(path.join(temp_dir_path, file_name), content, encoding=code_encoding)

    except (FileNotFoundError, OSError, PermissionError, UnicodeEncodeError) as error:
        raise MANIP_FailedFileWriteError(f"Failed to create or write javascript code to temporary file: {error}") from error
    
    try:
        result = run_subprocess(
            ["node", EXTRACTOR_PATH, main_file_path],
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
            pass # CLEANUP #delete_directory(temp_dir_path)
        except MANIP_FailedFileDeleteError as error:
            raise MANIP_FailedFileDeleteError(f"Failed to remove temporary javascript file at {temp_dir_path!r}: {error}") from error

    if result.returncode != 0:
        if   result.returncode == 2:
            # Registration error
            raise MANIP_ExtensionExecutionErrorInJavascript(f"Extension was not registered or invalid value registered. This is the fault of the extension developer: {result.stderr}")
        else:  # result.returncode == 1 or others
            # Script execution error
            raise MANIP_ExtensionExecutionErrorInJavascript(f"Error in extension javascript execution: {result.stderr}")

    try:
        extension_info = loads(result.stdout.strip().splitlines()[-1])  # last line = JSON
    except Exception as error:
        raise MANIP_ExtensionJSONDecodeError(f"Invalid Extension Info JSON returned from Node.js subprocess: {error}") from error

    return extension_info


__all__ = ["extract_extension_info_directly"]


