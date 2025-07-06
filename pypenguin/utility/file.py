import os
import zipfile

from pypenguin.utility.errors import PathError
from pypenguin.utility.repr   import KeyReprDict


def read_all_files_of_zip(zip_path: str) -> KeyReprDict[str, bytes]:
    """
    Reads all files from a ZIP archive and returns their contents.

    Args:
        zip_path (str): Path to the ZIP file.

    Returns:
        KeyReprDict[str, bytes]: A dictionary-like object mapping each file name
        in the archive to its corresponding file contents as bytes.

    Notes:
        - Only regular files are read; directories are skipped.
        - File names inside the archive are preserved as-is.
        - The returned KeyReprDict allows improved display or manipulation of keys, 
          depending on its implementation.

    Raises:
        FileNotFoundError: If the ZIP file does not exist.
        zipfile.BadZipFile: If the file is not a valid ZIP archive.
    """
    zip_path = ensure_correct_path(zip_path)
    contents = KeyReprDict()
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file_ref:
                contents[file_name] = file_ref.read()
    return contents

def create_zip_file(zip_path: str, contents: KeyReprDict[str, bytes]) -> None:
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


__all__ = ["read_all_files_of_zip", "create_zip_file", "ensure_correct_path"]

