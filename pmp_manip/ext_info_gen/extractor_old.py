from os           import remove as os_remove
from subprocess   import run as run_subprocess
from tempfile     import NamedTemporaryFile

#from pypenguin.utility         import (
#    grepr, read_file_text, write_file_text, DualKeyDict, PypenguinEnum, ContentFingerprint,
#    ThanksError, UnknownExtensionAttributeError,
#)

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
    """
    try:
        with NamedTemporaryFile(
            mode="w", suffix=".js", 
            encoding=code_encoding, delete=False,
        ) as temp_file:
            temp_js.write(js_code)
            temp_js_path = temp_js.name

    except UnicodeDecodeError as error:
        raise PP_FailedFileWriteError(f"Failed to create or write javascript code to temporary file because of encoding failure: {error}") from error
    except (FileNotFoundError, OSError, PermissionError, IsADirectoryError, Exception) as error:
        raise PP_FailedFileWriteError("Failed to create or write javascript code to temporary file") from error
    
    with NamedTemporaryFile(
        mode="w", suffix=".js", 
        encoding="utf-8", 
        delete=False
    ) as temp_js:
        temp_js.write(js_code)
        temp_js_path = temp_js.name

    try:
        print("--> Executing JavaScript via Node.js")
        result = run_subprocess(
            ["node", EXTRACTOR_PATH, temp_js_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=1, # usually seems to take around 0.10-0.14 seconds on windows
        )
    except FileNotFoundError as error: # when python can't find the node executable
        raise RuntimeError("Node.js is not installed or not found in PATH.") from error
    finally:
        os_remove(temp_js_path)

    if result.returncode != 0:
        raise RuntimeError(f"Error in sandboxed JS execution: {result.stderr}")

    try:
        extension_info = loads(result.stdout.strip().splitlines()[-1])  # last line = JSON
    except Exception as error:
        raise RuntimeError(f"Invalid JSON output from container: {error}") from error

    for attr in extension_info.keys():
        if attr not in {
            "name", "color1", "color2", "color3", "menuIconURI",
            "docsURI", "isDynamic", "id", "blocks", "menus"
        }:
            raise UnknownExtensionAttributeError(attr)

    return extension_info


__all__ = ["extract_getinfo"]


