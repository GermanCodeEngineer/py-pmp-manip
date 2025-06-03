import os
import zipfile

from pypenguin.utility.errors import PathError


def read_all_files_of_zip(zip_path: str) -> dict[str, bytes]:
    zip_path = ensure_correct_path(zip_path)
    contents = {}
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file_ref:
                contents[file_name] = file_ref.read()
    return contents

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


__all__ = ["read_all_files_of_zip", "ensure_correct_path"]

