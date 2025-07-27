from datetime     import datetime, timezone
from json         import loads, dumps
from os           import path, makedirs
from types        import EllipsisType
from typing       import Any

from pypenguin.config          import get_config, init_config, get_default_config
from pypenguin.utility         import (
    read_file_text, write_file_text, ContentFingerprint,
)

from pypenguin.ext_info_gen.extractor import fetch_js_code, extract_extension_info


CACHE_FILENAME = "cache.json"

    
def generate_extension_info_py_file(source: str, extension_id: str) -> str:
    """
    Generate a python file, which stores information about the blocks of the given extension and is required for the core module. Returns the file path of the python file

    Args:
        source: the file path or https URL or JS Data URI of the extension code
        extension_id: the unique identifier of the extension 
    
    Raises:
        
    """
    def consider_state(by_url: bool) -> bool|EllipsisType:
        """
        Returns wether the extensions JavaScript should be fetched again and the python file should be (re-)generated
        """
        if not path.exists(destination_file_path):
            return True
        
        if destination_file_name not in cache:
            return True
        
        py_fingerprint = ContentFingerprint.from_json(file_cache["pyFingerprint"])
        try:
            last_update_time = datetime.fromisoformat(file_cache["lastUpdate"])
        except ValueError as error:
            return ... # is_too_old would become True and ... would be returned anyway
        
        python_code = read_file_text(destination_file_path)
        if by_url:
            is_too_old = (datetime.now(timezone.utc) - last_update_time) > get_config().ext_info_gen.js_fetch_interval 
            # /\ wether the last JS fetch is too long ago
        else:
            is_too_old = True # fetching the JS is not expensive in this case
        if py_fingerprint.matches(python_code): # if the python code was NOT manipulated
            return ... if is_too_old else False
        else:
            return ...

    def update_cache(cache: dict[str, dict[str, Any]]):
        """
        Updates the cache file
        
        Args:
            cache: the cache data
        """
        cache_copy = {"_": "Please DO NOT TOUCH this file. If you want to be safe just delete it and it will be regenerated"}
        cache_copy |= cache
        write_file_text(cache_file_path, dumps(cache_copy, indent=4))

    cfg = get_config()
    destination_file_name = f"{extension_id}.py"
    destination_file_path = path.join(cfg.ext_info_gen.gen_opcode_info_dir, destination_file_name)
    cache_file_path = path.join(cfg.ext_info_gen.gen_opcode_info_dir, CACHE_FILENAME)
    cache: dict[str, dict[str, Any]]
    if path.exists(cache_file_path):
        cache = loads(read_file_text(cache_file_path))
    else:
        cache = {}
    file_cache = cache.get(destination_file_name, None)

    should_continue = consider_state(by_url=(source.startswith("http://") or source.startswith("https://")))
    if should_continue is False: # neither True nor Ellipsis
        print("PY STILL UP TO DATE")
        file_cache["lastUpdate"] = datetime.now(timezone.utc).isoformat()
        update_cache(cache)
        return destination_file_path
    js_code = fetch_js_code(source)
    if file_cache is not None:
        js_fingerprint = ContentFingerprint.from_json(file_cache["jsFingerprint"])
        if (should_continue is ...) and js_fingerprint.matches(js_code):
            file_cache["lastUpdate"] = datetime.now(timezone.utc).isoformat()
            update_cache(cache)
            print("PY & JS STILL UP TO DATE")
            return destination_file_path
    
    extension_info = extract_extension_info(js_code)
    info_group, input_type_cls, dropdown_type_cls = generate_opcode_info_group(extension_info)
    file_code = generate_file_code(info_group, input_type_cls, dropdown_type_cls)
    makedirs(cfg.ext_info_gen.gen_opcode_info_dir, exist_ok=True)
    write_file_text(destination_file_path, file_code)
    
    cache[destination_file_name] = {
        "jsFingerprint": ContentFingerprint.from_value(js_code).to_json(),
        "pyFingerprint": ContentFingerprint.from_value(file_code).to_json(),
        "lastUpdate": datetime.now(timezone.utc).isoformat(),
    }
    update_cache(cache)
    print("(RE-)GENERATED PY")
    return destination_file_path


__all__ = ["generate_extension_info_py_file"]


if __name__ == "__main__":
    init_config(get_default_config())
    for extension_id, extension in [
        ("asyncexample",         "example_extensions/js_extension/asyncexample.js"),
        ("dumbExample",         "example_extensions/js_extension/dumbExample.js"),
#        ("truefantombase",      "https://extensions.turbowarp.org/true-fantom/base.js"),
#        ("pmControlsExpansion", "example_extensions/js_extension/pmControlsExpansion.js"),
#        ("gpusb3",              "https://extensions.penguinmod.com/extensions/derpygamer2142/gpusb3.js"),
#        ("P7BoxPhys",           "https://extensions.penguinmod.com/extensions/pooiod/Box2D.js"),
    ]:
        generate_extension_info_py_file(extension, extension_id)
