import os
import shutil
import zipfile, zlib

from pmp_manip.utility.decorators import enforce_argument_types
from pmp_manip.utility.errors     import (
    MANIP_TypeError, MANIP_ValueError, 
    MANIP_OSError, MANIP_FileNotFoundError, MANIP_FailedFileWriteError, MANIP_FailedFileReadError, MANIP_FailedFileDeleteError,
)

@enforce_argument_types
def read_all_files_of_zip(zip_path: str) -> dict[str, bytes]:
    """
    Reads all files from a ZIP archive and returns their contents

    Args:
        zip_path: Path to the ZIP file

    Returns:
        dict[str, bytes]: An object mapping each file name
        in the archive to its corresponding file contents as bytes

    Notes:
        - Only regular files are read; directories are skipped
        - File names inside the archive are preserved as-is

    Raises:
        MANIP_FileNotFoundError: If the ZIP file was not found
        MANIP_FailedFileReadError: For OS-related errors on the zip file or one its files like, closed, permission denied, invalid path, or decoding/unpacking failures
    """
    contents = {}
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for file_name in zip_ref.namelist():
                try:
                    with zip_ref.open(file_name) as file_ref:
                        contents[file_name] = file_ref.read()
                except (zlib.error, EOFError, MemoryError, OverflowError, KeyError,) as error:
                    raise MANIP_FailedFileReadError(
                        f"Failed to extract {file_name!r} from zip {zip_path!r}: {error}"
                    ) from error

    except FileNotFoundError as error:
        raise MANIP_FileNotFoundError(
            f"Failed to read, zip file does not exist: {error}"
        ) from error

    except (ValueError, PermissionError, IsADirectoryError,
            NotADirectoryError, UnicodeDecodeError, OSError,
            zipfile.BadZipFile, zipfile.LargeZipFile) as error:
        raise MANIP_FailedFileReadError(
            f"Failed to read from {zip_path!r}: {error}"
        ) from error

    return contents

@enforce_argument_types
def read_file_text(file_path: str, encoding: str = "utf-8") -> str:
    """
    Read the text content of a file

    Args:
        file_path: path to the file to read
        encoding: encoding to use when reading the file. default is 'utf-8'

    Returns:
        str: The contents of the file.

    Raises:
        MANIP_FileNotFoundError: If the file was not found
        MANIP_FailedFileReadError: For OS-related errors like, closed, permission denied, invalid path, or decoding failures
    """
    try:
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()

    except FileNotFoundError as error:
        raise MANIP_FileNotFoundError(f"Failed to read, file does not exist: {error}") from error
    except (ValueError, PermissionError, IsADirectoryError,
            NotADirectoryError, UnicodeDecodeError, OSError) as error:
        raise MANIP_FailedFileReadError(f"Failed to read from {file_path!r}: {error}") from error

@enforce_argument_types
def write_file_text(file_path: str, text: str, encoding: str = "utf-8") -> None:

    """
    Write text to a file.

    Args:
        file_path: file path of the file to write to
        text: the text to write
        encoding: the text encoding to use
    
    Raises:
        MANIP_ValueError: If the file is in an invalid state or mode for writing
        MANIP_FailedFileWriteError: If an OS-level error occurs (e.g., file not found, permission denied,
                                 is a directory, or other I/O-related failure) or `text` is not compatible with `encoding`
    """

    try:
        with open(file_path, mode="w", encoding=encoding) as file:
            file.write(text)

    except ValueError as error:
        raise MANIP_ValueError(str(error)) from error
    except UnicodeDecodeError as error:
        raise MANIP_FailedFileWriteError(f"Failed to write to {file_path!r} because of encoding failure: {error}") from error
    except (FileNotFoundError, OSError, PermissionError, IsADirectoryError) as error:
        raise MANIP_FailedFileWriteError(f"Failed to write to {file_path!r}: {error}") from error

@enforce_argument_types
def delete_file(file_path: str) -> None:
    """
    Delete a file from the filesystem

    Args:
        file_path: Path to the file to delete

    Raises:
        MANIP_ValueError: If `file_path` is invalid or not a proper file path
        MANIP_FailedFileDeleteError: If an OS-level error occurs (e.g., file not found, permission denied,
                                  is a directory, or other I/O-related failure)
    """

    try:
        os.remove(file_path)

    except ValueError as error:
        raise MANIP_ValueError(str(error)) from error
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as error:
        raise MANIP_FailedFileDeleteError(f"Failed to delete file at {file_path!r}: {error}") from error

@enforce_argument_types
def delete_directory(dir_path: str) -> None:
    """
    Delete a directory and all its contents from the filesystem

    Args:
        dir_path: Path to the directory to delete

    Raises:
        MANIP_ValueError: If `dir_path` is invalid or not a proper directory path
        MANIP_FailedFileDeleteError: If an OS-level error occurs (e.g., directory not found, permission denied,
                                      is a file, or other I/O-related failure)
    """
    try:
        shutil.rmtree(dir_path)
    
    except ValueError as error:
        raise MANIP_ValueError(str(error)) from error
    except (FileNotFoundError, PermissionError, NotADirectoryError, OSError) as error:
        raise MANIP_FailedFileDeleteError(f"Failed to delete directory at {dir_path!r}: {error}") from error

@enforce_argument_types
def create_zip_file(zip_path: str, contents: dict[str, bytes]) -> None:
    """
    Creates a ZIP file at `zip_path` containing the given contents

    Args:
        file_path: Destination path for the ZIP file
        contents: A dictionary where keys are filenames (inside the ZIP)
                  and values are their corresponding file contents in bytes
    """ # TODO: add good error handling
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_out:
        for name, data in contents.items():
            zip_out.writestr(name, data)

@enforce_argument_types
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


__all__ = [
    "read_all_files_of_zip", "read_file_text", "write_file_text", 
    "delete_file", "delete_directory", "create_zip_file", "file_exists",
]

