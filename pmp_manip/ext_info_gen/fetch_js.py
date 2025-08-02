from base64                 import b64decode
from os                     import path
from pathlib                import Path
from requests               import get as requests_get, RequestException
from validators             import url as validators_url

from pmp_manip.utility            import (
    PP_InvalidExtensionCodeSourceError, 
    PP_NetworkFetchError, PP_UnexpectedFetchError, PP_FileFetchError, 
)


def fetch_js_code(source: str, tolerate_file_path: bool) -> str:
    """
    Fetch the extension's JS code from a file path, HTTPS URL, or JavaScript Data URI

    Args:
        source: The file path, HTTPS URL, or data URI of the extension source code
        tolerate_file_path: wether to allow file paths as extension sources

    Raises:
        PP_InvalidExtensionCodeSourceError: If the source data URI, URL or file_path is invalid or if a file path is passed even tough tolerate_file_paths is False or if the passed value is an invalid source
        PP_NetworkFetchError: For any network-related error
        PP_UnexpectedFetchError: For any other unexpected error while fetching URL
        PP_FileNotFoundError: If the local file does not exist
        PP_FileFetchError: If the file cannot be read
    """
    if source.startswith("data:"):
        print("--> Fetching from data URI")
        try:
            meta, encoded = source.split(",", 1)
            if ";base64" in meta:
                return b64decode(encoded).decode()
            else:
                return unquote(encoded)
        except Exception as error:
            raise PP_InvalidExtensionCodeSourceError(f"Failed to decode data URI: {error}") from error

    elif source.startswith("http://") or source.startswith("https://"):
        print(f"--> Fetching from URL: {source}")
        
        if not validators_url(source):
            raise PP_InvalidExtensionCodeSourceError(f"Invalid URL: {source}")
        try:
            response = requests_get(source, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as error:
            raise PP_NetworkFetchError(f"Network error fetching {source}: {error}") from error
        except Exception as error:
            raise PP_UnexpectedFetchError(f"Unexpected error while fetching {source}: {error}") from error

    else:
        if not tolerate_file_path:
            raise PP_InvalidExtensionCodeSourceError(f"Fetching by a file path is forbidden: {source}")
        
        print(f"--> Reading from file: {source}")
        try:
            Path(source)  # Validates that the path can be created
        except (TypeError, ValueError) as error:
            raise PP_InvalidExtensionCodeSourceError(f"Invalid file path or extension source {source}: {error}") from error
        
        if not path.exists(source):
            raise PP_FileNotFoundError(f"File not found: {source}")
        try:
            return read_file_text(source)
        except Exception as error:
            raise PP_FileFetchError(f"Failed to read file {source}: {error}") from error


__all__ = ["fetch_js_code"]

