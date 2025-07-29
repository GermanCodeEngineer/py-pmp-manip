from os                                  import makedirs, path
from platform                            import system as get_system
from sys                                 import exit as sys_exit
from setuptools._distutils.ccompiler     import new_compiler
from setuptools._distutils.unixccompiler import UnixCCompiler
from tempfile                            import TemporaryDirectory


# Mostly stolen from    repo: tree-sitter/py-tree-sitter    branch: v0.20.1     file: tree_sitter/__init__.py
def build_library(output_path: str, repo_paths: list[str]) -> bool:
    """
    Build a dynamic library at the given path, based on the parser
    repositories at the given paths

    Returns `True` if the dynamic library was compiled and `False` if
    the library already existed and was modified more recently than
    any of the source files

    Raises:
        ValueError: If no language folders are provided
        FileNotFoundError: If required source files (e.g. parser.c) are missing in any repo
        OSError: If file system operations fail (e.g. permissions issues, I/O errors)
        DistutilsExecError: If the compiler fails to compile or link the sources
        CompileError: If compilation of source files fails
        LibError: If linking the shared library fails
    """
    output_mtime = path.getmtime(output_path) if path.exists(output_path) else 0

    if not repo_paths:
        raise ValueError("Must provide at least one language folder")

    cpp = False
    source_paths: list[str] = []
    for repo_path in repo_paths:
        src_path = path.join(repo_path, "src")
        source_paths.append(path.join(src_path, "parser.c"))
        if path.exists(path.join(src_path, "scanner.cc")):
            cpp = True
            source_paths.append(path.join(src_path, "scanner.cc"))
        elif path.exists(path.join(src_path, "scanner.c")):
            source_paths.append(path.join(src_path, "scanner.c"))
    source_mtimes = [path.getmtime(__file__)] + [
        path.getmtime(path_) for path_ in source_paths
    ]

    compiler = new_compiler()
    if isinstance(compiler, UnixCCompiler):
        compiler.compiler_cxx[0] = "c++"

    if max(source_mtimes) <= output_mtime:
        return False

    with TemporaryDirectory(suffix="tree_sitter_language") as out_dir:
        object_paths = []
        for source_path in source_paths:
            if get_system() == "Windows":
                flags = None
            else:
                flags = ["-fPIC"]
                if source_path.endswith(".c"):
                    flags.append("-std=c99")
            object_paths.append(
                compiler.compile(
                    [source_path],
                    output_dir=out_dir,
                    include_dirs=[path.dirname(source_path)],
                    extra_preargs=flags,
                )[0]
            )
        compiler.link_shared_object(
            object_paths,
            output_path,
            target_lang="c++" if cpp else "c",
        )
    return True

def handle_build(output_dir: str, tree_sitter_js_path: str) -> None:
    """
    Handle the building of a dynamic library at the given path for every supported platform

    Raises:
        RuntimeError: if the device's platform is not supported or the submodule initialization is required
    
        FileNotFoundError: If required source files (e.g. parser.c) are missing in any repo
        OSError: If file system operations fail (e.g. permissions issues, I/O errors)
        DistutilsExecError: If the compiler fails to compile or link the sources
        CompileError: If compilation of source files fails
        LibError: If linking the shared library fails
    """
    system = get_system()
    match system:
        case "Linux":
            output_path = path.join(output_dir, "tree_sitter_js_linux.so")
            completion_messsage = f"✅ Built Linux library at {output_path}"
        case "Windows":
            output_path = path.join(output_dir, "tree_sitter_js_windows.dll")
            completion_messsage = f"✅ Built Windows library at {output_path}"
        case "Darwin":
            output_path = path.join(output_dir, "tree_sitter_js_macos.dylib")
            completion_messsage = f"✅ Built macOS library at {output_path}"
        case _:
            raise RuntimeError(f"❌ Unsupported OS: {system}")

    makedirs(output_dir, exist_ok=True)
    try:
        was_built = build_library(
            output_path,
            [tree_sitter_js_path]
        )
    except FileNotFoundError as error:
        raise RuntimeError("Missing submodules please run: \n\n    git submodule update --init --recursive") from error
    
    if was_built:
        print(completion_messsage)
    else:
        print("ℹ️  Library already up to date")
    sys_exit(0)

if __name__ == "__main__":
    handle_build(
        output_dir="build",
        tree_sitter_js_path="third_party/tree-sitter-javascript",
    )
