from os          import path as os_path, environ as os_environ, makedirs
from platform    import system as get_system
from shutil      import copy2 as shutil_copy2
from tree_sitter import Language, Parser

from pypenguin.utility import PP_UnsupportedOSError, PP_SetupRequiredError


_js_parser: Parser | None = None

def load_tree_sitter_js() -> Language:
    """
    Load the compiled Tree-sitter JavaScript language parser

    Returns:
        Language: The loaded JavaScript language object

    Raises:
        PP_UnsupportedOSError: If the platform is not supported
        PP_SetupRequiredError: If the expected shared library does not exist
    """
    system = get_system()
    lib_name_map = {
        "Linux": "tree_sitter_js_linux.so",
        "Windows": "tree_sitter_js_windows.dll",
        "Darwin": "tree_sitter_js_macos.dylib",
    }

    lib_name = lib_name_map.get(system)
    if lib_name is None:
        raise PP_UnsupportedOSError(f"Unsupported platform: {system}")
        # Relative path inside the project
    project_dir = os_path.dirname(__file__)
    lib_source_path = os_path.abspath(os_path.join(project_dir, "..", "build", lib_name))

    if not os_path.exists(lib_source_path):
        raise PP_SetupRequiredError(
            f"Missing Tree-sitter shared library for JavaScript: {lib_source_path}\n"
            f"❌ You need to build it first by running:\n\n"
            f"    python scripts/build_tree_sitter_lib.py\n"
        )
    
    # For Termux, load from internal app-safe directory
    is_termux = "ANDROID_ROOT" in os_environ and "com.termux" in os_environ.get("PREFIX", "")
    if is_termux:
        safe_dir = os_path.expanduser("~/.pypenguin_tree_sitter/")
        makedirs(safe_dir, exist_ok=True)
        safe_lib_path = os_path.join(safe_dir, lib_name)

        # Copy only if needed
        if not os_path.exists(safe_lib_path) or (os_path.getmtime(safe_lib_path) < os_path.getmtime(lib_source_path)):
            shutil_copy2(lib_source_path, safe_lib_path)
        load_path = safe_lib_path
    else:
        load_path = lib_source_path
    
    return Language(load_path, "javascript") # TODO: find solution

def get_js_parser() -> Parser:
    """
    Returns the global tree sitter JavaScript Parser instance. Loads the Parser's Language from the built binary at first execution
    
    Raises:
        PP_UnsupportedOSError: If the platform is not supported
        PP_SetupRequiredError: If the expected shared library does not exist
    """
    global _js_parser
    if _js_parser is None:
        _js_parser = Parser(language=load_tree_sitter_js())
    return _js_parser


__all__ = ["get_js_parser"]


