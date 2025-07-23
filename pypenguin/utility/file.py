import os
import zipfile

from pypenguin.utility.errors import PathError

def read_all_files_of_zip(zip_path: str) -> dict[str, bytes]:
    """
    Reads all files from a ZIP archive and returns their contents.

    Args:
        zip_path (str): Path to the ZIP file.

    Returns:
        dict[str, bytes]: An object mapping each file name
        in the archive to its corresponding file contents as bytes.

    Notes:
        - Only regular files are read; directories are skipped.
        - File names inside the archive are preserved as-is.

    Raises:
        FileNotFoundError: If the ZIP file does not exist.
        zipfile.BadZipFile: If the file is not a valid ZIP archive.
    """
    zip_path = ensure_correct_path(zip_path)
    contents = {}
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file_ref:
                contents[file_name] = file_ref.read()
    return contents

def read_file_text(file_path: str) -> str:
    """
    Read the text of a file.

    Args:
        file_path: file path of the file to read
    """
    with open(file_path, "r") as file:
        return file.read()

def write_file_text(file_path: str, text: str) -> None:
    """
    Write text to a file.

    Args:
        file_path: file path of the file to write to
        text: the text to write
    """
    with open(file_path, "w") as file:
        file.write(text)

def create_zip_file(zip_path: str, contents: dict[str, bytes]) -> None:
    """
    Creates a ZIP file at `zip_path` containing the given contents.

    Args:
        file_path: Destination path for the ZIP file.
        contents: A dictionary where keys are filenames (inside the ZIP)
                  and values are their corresponding file contents in bytes.
    """
    zip_path = ensure_correct_path(zip_path)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_out:
        for name, data in contents.items():
            zip_out.writestr(name, data)

def ensure_correct_path(_path: str, target_folder_name: str = "pypenguin") -> str:
    if target_folder_name is not None:
        initial_path = __file__
        current_path = os.path.normpath(initial_path)

        while True:
            base_name = os.path.basename(current_path)
            
            if base_name == target_folder_name and os.path.isdir(current_path):
                break
            
            parent_path = os.path.dirname(current_path)
            
            if parent_path == current_path:
                raise PathError(f"Target folder '{target_folder_name}' not found in the _path '{initial_path}'")
            
            current_path = parent_path

        final_path = os.path.join(current_path, _path)
        return final_path


__all__ = ["read_all_files_of_zip", "read_file_text", "write_file_text", "create_zip_file", "ensure_correct_path"]

