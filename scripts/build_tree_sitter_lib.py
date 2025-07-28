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
        Language.build_library(
            linux_output,
            [TS_JS_PATH]
        )
        print(f"✅ Built Linux library at {linux_output}")
    case "Windows":
        windows_output = path.join(OUTPUT_DIR, "tree_sitter_js_windows.dll")
        Language.build_library(
            windows_output,
            [TS_JS_PATH]
        )
        print(f"✅ Built Windows library at {windows_output}")
    case "Darwin":
        macos_output = os.path.join(OUTPUT_DIR, "tree_sitter_js_macos.dylib")
        Language.build_library(
            macos_output,
            [TS_JS_PATH]
        )
        print(f"✅ Built macOS library at {macos_output}")
    case _:
        raise Exception(f"❌ Unsupported OS: {system}")

sys_exit(0)
