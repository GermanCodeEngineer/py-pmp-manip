from datetime     import datetime, timezone
from json         import loads, dumps, JSONDecodeError
from logging      import getLogger
from os           import path, makedirs
from typing       import Any

from pmp_manip.config          import get_config, init_config, get_default_config
from pmp_manip.utility         import (
    read_file_text, write_file_text, file_exists, enforce_argument_types, ContentFingerprint,
    MANIP_Error, MANIP_FailedFileReadError, MANIP_FailedFileWriteError, MANIP_ThanksError, MANIP_ExtensionFetchError,
    MANIP_DirectExtensionInfoExtractionError, MANIP_SafeExtensionInfoExtractionError,
    MANIP_NoNodeJSInstalledError, MANIP_ExtensionInfoConvertionError,
)

from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
from pmp_manip.ext_info_gen.fetch_js         import fetch_js_code
from pmp_manip.ext_info_gen.generator        import generate_opcode_info_group, generate_file_code
from pmp_manip.ext_info_gen.safe_extractor   import extract_extension_info_safely


CACHE_FILENAME  = "cache.json"
STATUS_KEEP     = "KEEP"
STATUS_CHECK_JS = "CHECK_JS"
STATUS_REGEN    = "REGEN"



def is_trusted_extension_origin(source: str) -> bool:
    """
    Evaluates if an extension from the `source` can be trusted and therefore executed directly

    Args:
        source: the file path or https URL or JS Data URI of the extension code
    """
    # based on PenguinMod's trusted origin list
    # taken from https://github.com/PenguinMod/penguinmod.github.io/blob/develop/src/containers/tw-security-manager.jsx#L26 (07.08.2025)
    if ( 
        # Always trust our official extension repostiory.
        source.startswith("https://extensions.turbowarp.org/") or
        source.startswith("https://extensions.penguinmod.com/") or
        source.startswith("https://penguinmod-extensions-gallery.vercel.app/") or

        # Trust other people's galleries. These can be removed in the future, they will just show a pop-up on load if they are.
        source.startswith("https://sharkpools-extensions.vercel.app/") or # SharkPool
        source.startswith("https://pen-group.github.io/") # Pen-Group / ObviousAlexC
    ):
        return True

    custom_is_trusted_handler = get_config().ext_info_gen.is_trusted_extension_origin_handler
    if (custom_is_trusted_handler is not None) and custom_is_trusted_handler(source):
        return True

    return False

def _consider_state(dest_file_name: str, dest_file_path: str, cache: dict[str, dict[str, Any]], js_fetch_expensive: bool) -> str:
    """
    Returns wether the extensions JavaScript should be fetched again and the python file should be (re-)generated

    Args:
        js_fetch_expensive: wether it is expensive to fetch the extension's JS code (wether it is loaded by URL)
    """
    if not file_exists(dest_file_path):
        return STATUS_REGEN
    if dest_file_name not in cache:
        return STATUS_REGEN
    try:
        python_code = read_file_text(dest_file_path)
    except MANIP_Error:
        return STATUS_REGEN # we can not know if python code has changed, so regenerate
    file_cache = cache[dest_file_name]
    try:
        py_fingerprint = ContentFingerprint.from_json(file_cache["pyFingerprint"])
    except (TypeError, KeyError):
        return STATUS_REGEN # we can not know if python code has changed, so regenerate
    
    if not py_fingerprint.matches(python_code): # if the python code was manipulated
        return STATUS_REGEN
    
    if not js_fetch_expensive:
        return STATUS_CHECK_JS
    
    try:
        last_update_time = datetime.fromisoformat(file_cache["lastUpdate"])
    except ValueError:
        return STATUS_CHECK_JS # we can not know if last fetch is too long ago, assume worst case
    
    timediff = (datetime.now(timezone.utc) - last_update_time)
    too_long_ago = (timediff > get_config().ext_info_gen.js_fetch_interval)
    # wether the last JS fetch is too long ago
    return STATUS_CHECK_JS if too_long_ago else STATUS_KEEP

def _get_cache(cache_file_path: str) -> dict[str, dict[str, Any]]:
    """
    Safely get the cache data stored in the cache file

    Args:
        cache_file_path: the full file path of the cache file
    """
    if not file_exists(cache_file_path):
        return {}
    try:
        return loads(read_file_text(cache_file_path))
    except (MANIP_FailedFileReadError, JSONDecodeError):
        return {}

def _update_cache(
        old_cache: dict[str, dict[str, Any]], cache_file_path: str, dest_file_name: str, 
        js_code: str | None, py_code: str | None,
) -> None:
    """
    Updates the cache file
    
    Args:
        old_cache: the cache data
        cache_file_path: the full file path of the cache file
        dest_file_name: the file name of the generated ext info file
        js_code: the extension's javascript code
        py_code: the generated python code
    
    Raises:
        MANIP_FailedFileWriteError: if the cache file could not be written
    """
    if dest_file_name in old_cache:
        old_cache[dest_file_name]["lastUpdate"] = datetime.now(timezone.utc).isoformat()
    else:
        old_cache[dest_file_name] = {
            "jsFingerprint": ContentFingerprint.from_value(js_code).to_json(),
            "pyFingerprint": ContentFingerprint.from_value(py_code).to_json(),
            "lastUpdate"   : datetime.now(timezone.utc).isoformat(),
        }
    cache = {"_": "Please DO NOT MESS WITH THIS FILE. If you want to be safe just delete it and it will be regenerated"} | old_cache
    cache_str = dumps(cache, indent=4)
    try:
        write_file_text(cache_file_path, cache_str)
    except MANIP_FailedFileWriteError as error:
        raise MANIP_FailedFileWriteError(f"Could not update cache at {cache_file_path!r}: {error}") from error

@enforce_argument_types
def generate_extension_info_py_file(
    source: str, extension_id: str, 
    tolerate_file_path: bool, bundle_errors: bool = True,
) -> str:
    """
    Generate a python file, which stores information about the blocks of the given extension and is required for the core module. If a cached version exist and is up to date, it will be kept. Returns the file path of the python file. Uses logging

    Args:
        source: the file path or https URL or JS Data URI of the extension code(if tolerate_file_paths)
        extension_id: the unique identifier of the extension 
        tolerate_file_path: wether to allow file paths as extension sources
        bundle_errors: wether to bundle similar errors for more compact handling (see Raises)
    
    Raises (if bundled):
        MANIP_NoNodeJSInstalledError(not bundled): if Node.js is not installed or not found in PATH
        MANIP_ExtensionFetchError: if the extension code could not be fetched for some reason
        MANIP_DirectExtensionInfoExtractionError: if the extension info could not be extracted through direct execution
        MANIP_SafeExtensionInfoExtractionError: if the extension info could not be extracted through safe analysis
        MANIP_ExtensionInfoConvertionError: if the extracted extension info could not be converted into the format of this project
        MANIP_ThanksError(unlikely, not bundled): if a block argument uses the mysterious Scratch.ArgumentType.SEPERATOR
        MANIP_FailedFileWriteError(unlikely): if the generated extension info file or cache file or their directory could not be written/created
    
    Raises (if NOT bundled):
        ### created here or not bundled anyway:
        MANIP_FailedFileWriteError(unlikely): if the cache file or generated extension info file or its directory could not be written/created
        MANIP_NoNodeJSInstalledError(not bundled): if Node.js is not installed or not found in PATH
        
        ### inherited from fetch_js => MANIP_ExtensionFetchError if bundled
        MANIP_InvalidExtensionCodeSourceError: If the source data URI, URL or file_path is invalid or if a file path is passed even tough tolerate_file_paths is False or if the passed value is an invalid source
        MANIP_NetworkFetchError: For any network-related error (like 404 (not found))
        MANIP_UnexpectedFetchError: For any other unexpected error while fetching URL
        MANIP_FileNotFoundError: If the local source file does not exist
        MANIP_FileFetchError: If the source file cannot be read
        
        ### inherited from extract_extension_info_directly => MANIP_DirectExtensionInfoExtractionError if bundled
        MANIP_FailedFileWriteError(unlikely): if the JS code could not be written to a temporary file (eg. OS Error or Unicode Error)
        MANIP_FailedFileDeleteError(unlikely): if the temporary Javscript file could not be deleted
        MANIP_NoNodeJSInstalledError(not bundled): if Node.js is not installed or not found in PATH
        MANIP_ExtensionExecutionTimeoutError: if the Node.js execution subprocess took too long
        MANIP_ExtensionExecutionErrorInJavascript: if an error occurs inside the actual extension code
        MANIP_UnexpectedExtensionExecutionError: if some other error raises during the subprocess call (eg. Permission or OS Error)
        MANIP_ExtensionJSONDecodeError(unlikely): if the json output of the subprocess is invalid

        ### inherited from extract_extension_info_safely => MANIP_SafeExtensionInfoExtractionError if bundled
        MANIP_InvalidExtensionCodeSyntaxError: if the extension code is syntactically invalid 
        MANIP_BadExtensionCodeFormatError: if the extension code is badly formatted, so that the extension information cannot be extracted
        MANIP_InvalidTranslationMessageError: if Scratch.translate is called with an invalid message
        
        ### inherited from generate_opcode_info_group => MANIP_ExtensionInfoConvertionError if bundled
        MANIP_UnknownExtensionAttributeError: if the extension or a block has an unknown attribute
        MANIP_InvalidCustomMenuError: if the information about a menu is invalid
        MANIP_InvalidCustomBlockError: if information of a block is invalid
        MANIP_NotImplementedError: if an XML block is included in the extension info
        MANIP_ThanksError(unlikely, not bundled): if a block argument uses the mysterious Scratch.ArgumentType.SEPERATOR

    Warnings:
        MANIP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed in the getInfo method of the extension code in safe analysis
        MANIP_UnexpectedNotPossibleFeatureWarning: if an impossible to implement feature is used (eg. ternary expr) in the getInfo method of the extension code in safe analysis
    """
    cfg = get_config()
    logger = getLogger(__name__)
    dest_file_name = f"{extension_id}.py"
    dest_file_path = path.join(cfg.ext_info_gen.gen_opcode_info_dir, dest_file_name)
    cache_file_path = path.join(cfg.ext_info_gen.gen_opcode_info_dir, CACHE_FILENAME)
    cache = _get_cache(cache_file_path)
    file_cache = cache.get(dest_file_name, None)
    
    status = _consider_state(
        dest_file_name, dest_file_path,
        cache, js_fetch_expensive=(source.startswith("http://") or source.startswith("https://")),
    )
    
    if status == STATUS_KEEP:
        logger.info(f"Extension {extension_id!r}: Python extension info file is still up to date")
        _update_cache(cache, cache_file_path, dest_file_name, js_code=None, py_code=None)
        return dest_file_path
    
    try:
        js_code = fetch_js_code(source, tolerate_file_path)
    except MANIP_Error as error:
        if bundle_errors:
            raise MANIP_ExtensionFetchError(f"Error in extension {extension_id!r}: Failed to fetch extension code: {error}") from error
        else:
            raise type(error)(f"Error in extension {extension_id!r}: {str(error)}") from error
    
    if (file_cache is not None) and (status == STATUS_CHECK_JS):
        try:
            js_fingerprint = ContentFingerprint.from_json(file_cache["jsFingerprint"])
        except (TypeError, KeyError):
            pass
        else:
            if js_fingerprint.matches(js_code):
                _update_cache(cache, cache_file_path, dest_file_name, js_code=None, py_code=None)
                logger.info(f"Extension {extension_id!r}: Python extension info file is still up to date as the extension code has not changed")
                return dest_file_path
    
    if is_trusted_extension_origin(source):
        logger.info(f"Extension {extension_id!r}: Extracting extension info through direct execution")
        try:
            extension_info = extract_extension_info_directly(js_code)
        except MANIP_NoNodeJSInstalledError:
            raise
        except MANIP_Error as error:
            if bundle_errors:
                raise MANIP_DirectExtensionInfoExtractionError(
                    f"Error in extension {extension_id!r}: Failed to extract extension info through direct execution: {error}"
                ) from error
            else:
                raise type(error)(f"Error in extension {extension_id!r}: {str(error)}") from error
    else:
        logger.info(f"Extension {extension_id!r}: Extracting extension info through safe static analysis")
        try:
            extension_info = extract_extension_info_safely(js_code)
        except MANIP_Error as error:
            if bundle_errors:
                raise MANIP_SafeExtensionInfoExtractionError(
                    f"Error in extension {extension_id!r}: Failed to extract extension info through safe analysis: {error}\n"
                    f"You can choose to let the code execute directly, which is more likely to work. "
                    f"See https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/handling_extensions.md"
                ) from error
            else:
                raise type(error)(f"Error in extension {extension_id!r}: {str(error)}") from error
    
    try:
        info_group, input_type_cls, dropdown_type_cls = generate_opcode_info_group(extension_info)
    except MANIP_ThanksError:
        raise
    except MANIP_Error as error:
        if bundle_errors:
            raise MANIP_ExtensionInfoConvertionError(
                f"Error in extension {extension_id!r}: Failed to convert extension info into required format: {error}"
            ) from error
        else:
            raise type(error)(f"Error in extension {extension_id!r}: {str(error)}") from error
    
    file_code = generate_file_code(info_group, input_type_cls, dropdown_type_cls)
    try:
        makedirs(cfg.ext_info_gen.gen_opcode_info_dir, exist_ok=True)
    except OSError as error:
        raise MANIP_FailedFileWriteError(
            f"Error in extension {extension_id!r}: Could not create directory of the extension info file at "
            f"{cfg.ext_info_gen.gen_opcode_info_dir!r}. Is your configuration correct?: {error}"
        ) from error

    try:
        write_file_text(dest_file_path, file_code)
    except MANIP_FailedFileWriteError as error:
        raise MANIP_FailedFileWriteError(
            f"Error in extension {extension_id!r}: Could not write extension info file to {cache_file_path!r}. "
            f"Is your configuration correct?: {error}"
        ) from error

    logger.info(f"Extension {extension_id!r}: Successfully (re-)generated python extension info file")
    _update_cache(cache, cache_file_path, dest_file_name, js_code, file_code)
    return dest_file_path


__all__ = ["generate_extension_info_py_file"]


if __name__ == "__main__": # pragma: no cover
    init_config(get_default_config()) # pragma: no cover
    for extension_id, extension in [ # pragma: no cover
        ("asyncexample",        "example_extensions/asyncexample.js"),
        ("dumbExample",         "example_extensions/dumbExample.js"),
        ("truefantombase",      "https://extensions.turbowarp.org/true-fantom/base.js"),
        ("pmControlsExpansion", "example_extensions/pmControlsExpansion.js"),
        ("gpusb3",              "https://extensions.penguinmod.com/extensions/derpygamer2142/gpusb3.js"),
        ("P7BoxPhys",           "https://extensions.penguinmod.com/extensions/pooiod/Box2D.js"),
        ("griffpatch",          "https://extensions.turbowarp.org/box2d.js"),
    ]:
        generate_extension_info_py_file(extension, extension_id, tolerate_file_path=True) # pragma: no cover
