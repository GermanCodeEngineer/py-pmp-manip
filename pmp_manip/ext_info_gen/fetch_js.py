from base64       import b64decode
from logging      import getLogger
from os           import path
from pathlib      import Path
from requests     import get as requests_get, RequestException
from urllib.parse import unquote
from validators   import url as validators_url

from pmp_manip.utility            import (
    read_file_text,
    MANIP_InvalidExtensionCodeSourceError, 
    MANIP_NetworkFetchError, MANIP_UnexpectedFetchError, MANIP_FileFetchError, MANIP_FileNotFoundError,
)


def fetch_js_code(source: str, tolerate_file_path: bool) -> str:
    """
    Fetch the extension's JS code from a file path, HTTPS URL, or JavaScript Data URI

    Args:
        source: The file path, HTTPS URL, or data URI of the extension source code
        tolerate_file_path: wether to allow file paths as extension sources

    Raises:
        MANIP_InvalidExtensionCodeSourceError: If the source data URI, URL or file_path is invalid or if a file path is passed even tough tolerate_file_paths is False or if the passed value is an invalid source
        MANIP_NetworkFetchError: For any network-related error (like 404 (not found))
        MANIP_UnexpectedFetchError: For any other unexpected error while fetching URL
        MANIP_FileNotFoundError: If the local file does not exist
        MANIP_FileFetchError: If the file cannot be read
    """
    logger = getLogger()
    if   isinstance(source, str) and source.startswith("data:"):
        logger.info("--> Fetching from data URI")
        try:
            meta, encoded = source.split(",", 1)
            if ";base64" in meta:
                return b64decode(encoded).decode()
            else:
                return unquote(encoded)
        except Exception as error:
            raise MANIP_InvalidExtensionCodeSourceError(f"Failed to decode data URI: {error}") from error

    elif isinstance(source, str) and (source.startswith("http://") or source.startswith("https://")):
        logger.info(f"--> Fetching from URL: {source}")
        
        if not validators_url(source):
            raise MANIP_InvalidExtensionCodeSourceError(f"Invalid URL: {source}")
        try:
            response = requests_get(source, timeout=10) # TODO: possibly make configurable?
            response.raise_for_status()
            return response.text
        except RequestException as error:
            raise MANIP_NetworkFetchError(f"Network error fetching {source!r}: {error}") from error
        except Exception as error:
            raise MANIP_UnexpectedFetchError(f"Unexpected error while fetching {source!r}: {error}") from error

    else:
        try:
            Path(source)  # Validates that the path can be created
        except (TypeError, ValueError) as error:
            raise MANIP_InvalidExtensionCodeSourceError(f"Invalid file path or other extension source {source!r}: {error}") from error
        
        logger.info(f"--> Reading from file: {source}")
        if not tolerate_file_path:
            raise MANIP_InvalidExtensionCodeSourceError(f"Fetching by a file path is forbidden: {source}")
        
        if not path.exists(source):
            raise MANIP_FileNotFoundError(f"File not found: {source}")
        try:
            return read_file_text(source)
        except Exception as error:
            raise MANIP_FileFetchError(f"Failed to read file {source!r}: {error}") from error


__all__ = ["fetch_js_code"]

