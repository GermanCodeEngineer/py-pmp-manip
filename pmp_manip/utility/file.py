import os
import zipfile

from pmp_manip.utility.errors import (
    MANIP_TypeError, MANIP_ValueError, 
    MANIP_OSError, MANIP_FileNotFoundError, MANIP_FailedFileWriteError, MANIP_FailedFileReadError, MANIP_FailedFileDeleteError,
)

def read_all_files_of_zip(zip_path: str) -> dict[str, bytes]:
    """
    Reads all files from a ZIP archive and returns their contents

    Args:
        zip_path (str): Path to the ZIP file

    Returns:
        dict[str, bytes]: An object mapping each file name
        in the archive to its corresponding file contents as bytes

    Notes:
        - Only regular files are read; directories are skipped
        - File names inside the archive are preserved as-is

    Raises:
        FileNotFoundError: If the ZIP file does not exist
        zipfile.BadZipFile: If the file is not a valid ZIP archive
    """
    #zip_path = ensure_correct_path(zip_path)
    contents = {}
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file_ref:
                contents[file_name] = file_ref.read()
    return contents

def read_file_text(file_path: str, encoding: str = "utf-8") -> str:
    """
    Read the text content of a file

    Args:
        file_path: path to the file to read
        encoding: encoding to use when reading the file. default is 'utf-8'

    Returns:
        str: The contents of the file.

    Raises:
        MANIP_TypeError: If an argument is of the wrong type
        MANIP_FileNotFoundError: If the file was not found
        MANIP_FailedFileReadError: For OS-related errors like, closed, permission denied, invalid path, or decoding failures
    """
    try:
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()

    except TypeError as error:
        raise MANIP_TypeError(str(error)) from error
    except FileNotFoundError as error:
        raise MANIP_FileNotFoundError(f"Failed to read, file does not exist: {error}") from error
    except (ValueError, PermissionError, IsADirectoryError,
            NotADirectoryError, UnicodeDecodeError, OSError) as error:
        raise MANIP_FailedFileReadError(f"Failed to read from {file_path!r}") from error

def write_file_text(file_path: str, text: str, encoding: str = "utf-8") -> None:

    """
    Write text to a file.

    Args:
        file_path: file path of the file to write to
        text: the text to write
        encoding: the text encoding to use
    
    Raises:
        MANIP_TypeError: If `text` is not a string or another type-related issue occurs
        MANIP_ValueError: If the file is in an invalid state or mode for writing
        MANIP_FailedFileWriteError: If an OS-level error occurs (e.g., file not found, permission denied,
                                 is a directory, or other I/O-related failure) or `text` is not compatible with `encoding`
    """
    if not isinstance(text, str):
        raise MANIP_TypeError(f"'text' argument must be a str, not {type(text).__name__!r}")

    try:
        with open(file_path, mode="w", encoding=encoding) as file:
            file.write(text)

    except TypeError as error:
        raise MANIP_TypeError(str(error)) from error
    except ValueError as error:
        raise MANIP_ValueError(str(error)) from error
    except UnicodeDecodeError as error:
        raise MANIP_FailedFileWriteError(f"Failed to write to {file_path!r} because of encoding failure: {error}") from error
    except (FileNotFoundError, OSError, PermissionError, IsADirectoryError) as error:
        raise MANIP_FailedFileWriteError(f"Failed to write to {file_path!r}") from error

def delete_file(file_path: str) -> None:
    """
    Delete a file from the filesystem

    Args:
        file_path: Path to the file to delete

    Raises:
        MANIP_TypeError: If `file_path` is not a string
        MANIP_ValueError: If `file_path` is invalid or not a proper file path
        MANIP_FailedFileDeleteError: If an OS-level error occurs (e.g., file not found, permission denied,
                                  is a directory, or other I/O-related failure)
    """
    if not isinstance(file_path, str):
        raise MANIP_TypeError(f"'file_path' must be a str, not {type(file_path).__name__!r}")

    try:
        os.remove(file_path)

    except TypeError as error:
        raise MANIP_TypeError(str(error)) from error
    except ValueError as error:
        raise MANIP_ValueError(str(error)) from error
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as error:
        raise MANIP_FailedFileDeleteError(f"Failed to delete file at {file_path!r}") from error

def create_zip_file(zip_path: str, contents: dict[str, bytes]) -> None:
    """
    Creates a ZIP file at `zip_path` containing the given contents

    Args:
        file_path: Destination path for the ZIP file
        contents: A dictionary where keys are filenames (inside the ZIP)
                  and values are their corresponding file contents in bytes
    """ # TODO: add good error handling
    #zip_path = ensure_correct_path(zip_path)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_out:
        for name, data in contents.items():
            zip_out.writestr(name, data)

def file_exists(file_path: str) -> bool:
    """
    Checks if a file exists at the specified path

    Args:
        file_path: the path to check
    """
    try:
        return os.path.exists(file_path)
    
    except TypeError as error:
        raise MANIP_TypeError(str(error)) from error
    except ValueError as error:
        raise MANIP_ValueError(str(error)) from error
    except OSError as error:
        raise MANIP_OSError(str(error)) from error


__all__ = ["read_all_files_of_zip", "read_file_text", "write_file_text", "delete_file", "create_zip_file", "file_exists"]

