from os          import makedirs, path
from platform    import system as get_system
from sys         import exit as sys_exit
from tree_sitter import Language


OUTPUT_DIR = "build"
makedirs(OUTPUT_DIR, exist_ok=True)

# Path to submodule grammar
TS_JS_PATH = "third_party/tree-sitter-javascript"

system = get_system()
match system:
    case "Linux":
        linux_output = path.join(OUTPUT_DIR, "tree_sitter_js_linux.so")
        try:
            Language.build_library(
                linux_output,
                [TS_JS_PATH]
            )
        except FileNotFoundError:
            raise RuntimeError("Missing submodules please run: \n\n    git submodule update --init --recursive")
        print(f"✅ Built Linux library at {linux_output}")
    case "Windows":
        windows_output = path.join(OUTPUT_DIR, "tree_sitter_js_windows.dll")
        try:
            Language.build_library(
                windows_output,
                [TS_JS_PATH]
            )
        except FileNotFoundError:
            raise RuntimeError("Missing submodules please run: \n\n    git submodule update --init --recursive")
        print(f"✅ Built Windows library at {windows_output}")
    case "Darwin":
        macos_output = path.join(OUTPUT_DIR, "tree_sitter_js_macos.dylib")
        try:
            Language.build_library(
                macos_output,
                [TS_JS_PATH]
            )
        except FileNotFoundError:
            raise RuntimeError("Missing submodules please run: \n\n    git submodule update --init --recursive")
        print(f"✅ Built macOS library at {macos_output}")
    case _:
        raise RuntimeError(f"❌ Unsupported OS: {system}")

sys_exit(0)
