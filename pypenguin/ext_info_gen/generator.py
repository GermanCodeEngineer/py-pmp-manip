from aenum        import extend_enum
from base64       import b64decode
from datetime     import datetime, timezone, timedelta
from json         import loads, dumps
from os           import remove as os_remove, makedirs, path
from requests     import get as requests_get, RequestException
from subprocess   import run as run_subprocess, TimeoutExpired
from tempfile     import NamedTemporaryFile
from types        import EllipsisType
from typing       import Any
from urllib.parse import unquote


from pypenguin.config          import get_config, init_config, get_default_config
from pypenguin.opcode_info.api import (
    OpcodeInfoGroup, OpcodeInfo, OpcodeType, MonitorIdBehaviour,
    InputInfo, InputMode, InputType, BuiltinInputType, MenuInfo,
    DropdownInfo, DropdownType, BuiltinDropdownType, DropdownTypeInfo,
    DropdownValueRule,
)
from pypenguin.utility         import (
    grepr, read_file_text, write_file_text, DualKeyDict, PypenguinEnum, ContentFingerprint,
    ThanksError, UnknownExtensionAttributeError,
)

ARGUMENT_TYPE_TO_INPUT_TYPE: dict[str, InputType] = {
    "string": BuiltinInputType.TEXT,
    "number": BuiltinInputType.NUMBER,
    "Boolean": BuiltinInputType.BOOLEAN,
    "color": BuiltinInputType.COLOR,
    "angle": BuiltinInputType.DIRECTION,
    "matrix": BuiltinInputType.MATRIX, # menu("matrix", "MATRIX")
    "note": BuiltinInputType.NOTE, # menu? maybe
    "costume": BuiltinInputType.COSTUME, # menu
    "sound": BuiltinInputType.SOUND, # menu
    "broadcast": BuiltinInputType.BROADCAST,
}
ARGUMENT_TYPE_TO_DROPDOWN_TYPE: dict[str, DropdownType] = {
    "variable": BuiltinDropdownType.VARIABLE,
    "list": BuiltinDropdownType.LIST,
}
INDENT = 4*" "
EXTRACTOR_PATH = "pypenguin/ext_info_gen/extractor.js"
CACHE_FILENAME = "cache.json"
   

def fetch_js_code(extension: str) -> str:
    """
    Fetch the extension's JS code from a file path, HTTPS URL, or JavaScript Data URI.

    Args:
        extension: The file path, HTTPS URL, or data URI of the extension code.

    Raises:
        ValueError: If the data URI is invalid.
        FileNotFoundError: If the local file does not exist.
        OSError: If the file cannot be read.
        requests.RequestException: For any network-related error.
        requests.HTTPError: For HTTP error responses (4xx, 5xx).
    """
    if extension.startswith("data:"):
        print("--> Fetching from data URI")
        try:
            meta, encoded = extension.split(",", 1)
            if ";base64" in meta:
                return b64decode(encoded).decode()
            else:
                return unquote(encoded)
        except Exception as error:
            raise ValueError(f"Failed to decode data URI: {error}") from error

    elif extension.startswith("http://") or extension.startswith("https://"):
        print(f"--> Fetching from URL: {extension}")
        try:
            response = requests_get(extension, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as error:
            raise ConnectionError(f"Network error fetching {extension}") from error
        except Exception as error:
            raise RuntimeError(f"Unexpected error while fetching URL") from error

    else:
        print(f"--> Reading from file: {extension}")
        if not path.exists(extension):
            raise FileNotFoundError(f"File not found: {extension}")
        try:
            return read_file_text(extension)
        except OSError as error:
            raise OSError(f"Failed to read file {extension}") from error

from subprocess import run as run_subprocess, TimeoutExpired
from tempfile import NamedTemporaryFile
from os import remove as os_remove
from json import loads
from typing import Any
import uuid


def extract_getinfo(js_code: str) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class based on the extension's JS code,
    executed in a sandboxed Docker container for safety.

    Args:
        js_code: The full JS code of the extension.

    Raises:
        RuntimeError, UnknownExtensionAttributeError
    """
    # Create a temp file for the JS code
    with NamedTemporaryFile(mode="w", suffix=".js", encoding="utf-8", delete=False) as temp_js:
        temp_js.write(js_code)
        temp_path = temp_js.name

    try:
        print("--> Executing JavaScript in sandboxed Docker container")
        result = run_subprocess(
            [
                "docker", "run", "--rm",
                "-v", f"{temp_path}:/ext.js:ro",
                "pypenguin-js-sandbox", "/ext.js"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )
    except FileNotFoundError:
        raise RuntimeError("Docker is not installed or not found in PATH.")
    except TimeoutExpired:
        raise RuntimeError("Docker sandbox timed out while extracting getInfo().")
    finally:
        os_remove(temp_js_path)

    # Create a temp file for the JS code
    with NamedTemporaryFile(mode="w", suffix=".js", encoding="utf-8", delete=False) as temp_js:
        temp_js.write(js_code)
        temp_path = temp_js.name

    try:
        print("--> Executing JavaScript in sandboxed Docker container")
        result = run_subprocess(
            [
                "docker", "run", "--rm",
                "-v", f"{temp_path}:/ext.js:ro",
                "pypenguin-js-sandbox", "/ext.js"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )
    except FileNotFoundError:
        raise RuntimeError("Docker is not installed or not found in PATH.")
    except TimeoutExpired:
        raise RuntimeError("Docker sandbox timed out while extracting getInfo().")
    finally:
        os_remove(temp_path)

    if result.returncode != 0:
        raise RuntimeError(f"Error in sandboxed JS execution: {result.stderr}")

    try:
        extension_info = loads(result.stdout.strip().splitlines()[-1])  # last line = JSON
    except Exception as error:
        raise RuntimeError(f"Invalid JSON output from container: {error}") from error

    for attr in extension_info.keys():
        if attr not in {
            "name", "color1", "color2", "color3", "menuIconURI",
            "docsURI", "isDynamic", "id", "blocks", "menus"
        }:
            raise UnknownExtensionAttributeError(attr)

    return extension_info

def process_all_menus(menus: dict[str, dict[str, Any]|list]) -> tuple[type[InputType], type[DropdownType]]:
    """
    Process all menus of an extension. Returns two classes, which contain the dervied input and dropdown types
    
    Args:
        menus: the dict mapping menu id to menu information 
    """
    class ExtensionInputType(InputType):
        pass
    class ExtensionDropdownType(DropdownType):
        pass

    for menu_index, menu_block_id, menu_info in zip(range(len(menus)), menus.keys(), menus.values()):
        possible_values: list[str|dict[str, str]]
        rules: list[DropdownValueRule] = []
        accept_reporters: bool
        if   isinstance(menu_info, dict):
            possible_values = menu_info["items"]
            accept_reporters = menu_info.get("acceptReporters", False)
        elif isinstance(menu_info, list):
            possible_values = menu_info
            accept_reporters = False
        
        if   isinstance(possible_values, list): pass
        elif isinstance(possible_values, str):
            possible_values = []
            rules.append(DropdownValueRule.EXTENSION_UNPREDICTABLE)
        else: raise NotImplementedError()
        
        new_possible_values = []
        old_possible_values = []
        for possible_value in possible_values:
            if   isinstance(possible_value, str):
                new_possible_values.append(possible_value)
                old_possible_values.append(possible_value)
            elif isinstance(possible_value, dict):
                new_possible_values.append(possible_value["text"])
                old_possible_values.append(possible_value["value"])
        
        dropdown_type_info = DropdownTypeInfo(
            direct_values     = new_possible_values,
            rules             = rules, # we assume the possible menu values are static
            old_direct_values = old_possible_values,
            fallback          = None, # there can't be a fallback when the possible values are static
        )
        custom_dropdown_type = extend_enum(ExtensionDropdownType, menu_block_id, dropdown_type_info)

        if accept_reporters:
            input_type_info = (
                InputMode.BLOCK_AND_DROPDOWN, # InputMode
                None, # magic number
                custom_dropdown_type, # corresponding dropdown type,
                menu_index, # uniqueness index
            )
            custom_input_type = extend_enum(ExtensionInputType, menu_block_id, input_type_info)
    return (ExtensionInputType, ExtensionDropdownType)

def generate_block_opcode_info(
        block_info: dict[str, Any], 
        menus: dict[str, dict[str, Any]],
        input_type_cls: type[InputType],
        dropdown_type_cls: type[DropdownType],
        extension_id: str,
    ) -> tuple[OpcodeInfo, str] | tuple[None, None]:
    """
    Generate the opcode information for one kind of block and the block opcode in 'new style'

    Args:
        block_info: the raw block information
        menus: the dict mapping menu id to menu information
        input_type_cls: the generated class containing the custom input types
        dropdown_type_cls: the generated class containing the custom dropdown types
        extension_id: the id of the extension
    """
    #print()
    #print()
    #print("CURRENT BLOCK", grepr(block_info))
    
    block_type: str = block_info["blockType"]
    is_terminal: bool = block_info.get("isTerminal", False)
    arguments: dict[str, dict[str, Any]] = block_info.get("arguments", {})
    branch_count: int = block_info.get("branchCount", 0)
    opcode_type: OpcodeType
    if block_type != "command":
        assert not(is_terminal)
    match block_type:
        case "command":
            opcode_type = OpcodeType.ENDING_STATEMENT if is_terminal else OpcodeType.STATEMENT
        case "reporter":
            opcode_type = OpcodeType.STRING_REPORTER
        case "Boolean":
            opcode_type = OpcodeType.BOOLEAN_REPORTER
        case "hat" | "event":
            opcode_type = OpcodeType.HAT
        case "conditional" | "loop":
            opcode_type = OpcodeType.STATEMENT
            branch_count = max(branch_count, 1)
        case "label" | "button":
            return (None, None) # not really block, but a label or button, can just be skipped
        case "xml":
            raise NotImplementedError("XML blocks are NOT supported. It is pretty much impossible to translate one into a database entry.")
        case _:
            raise ValueError(f"Unknown value for blockType: {repr(block_type)}")
    
    inputs: DualKeyDict[str, str, InputInfo] = DualKeyDict()
    dropdowns: DualKeyDict[str, str, DropdownInfo] = DualKeyDict()

    for argument_id, argument_info in arguments.items():
        argument_type: str = argument_info.get("type", "string")
        argument_menu: str|None = argument_info.get("menu", None)
        input_info = None
        dropdown_info = None
        match argument_type:
            case "string"|"number"|"Boolean"|"color"|"angle"|"matrix"|"note"|"costume"|"sound"|"broadcast":
                builitin_input_type = ARGUMENT_TYPE_TO_INPUT_TYPE[argument_type]
                if argument_menu is None:
                    input_info = InputInfo(
                        type=builitin_input_type,
                        menu=None,
                    )
                else:
                    assert builitin_input_type is BuiltinInputType.TEXT, 'If "menu" exists, "type" should be Scratch.ArgumentType.STRING(="string")'
                    menu_info = menus[argument_menu]
                    if   isinstance(menu_info, dict):
                        accept_reporters = menu_info.get("acceptReporters", False)
                    else:
                        accept_reporters = False

                    if accept_reporters:
                        input_info = InputInfo(
                            type=getattr(input_type_cls, argument_menu),
                            menu=MenuInfo(
                                opcode=f"{extension_id}_menu_{argument_menu}",
                                inner=argument_menu, # menu opcode seems to also be used as field name
                            ),
                        )
                    else:
                        dropdown_info = DropdownInfo(type=getattr(dropdown_type_cls, argument_menu)) # TODO: test
            case "variable"|"list":
                builtin_dropdown_type = ARGUMENT_TYPE_TO_DROPDOWN_TYPE[argument_type]
                dropdown_info = DropdownInfo(type=builtin_dropdown_type)
            case "image":
                continue # not really an input or dropdown
            case "polygon":
                raise NotImplementedError() # TODO, only necessary for the few polygon blocks(pen ext)
            case "seperator":
                raise ThanksError() # I couldn't find out what thats used for
        
        if (input_info is not None) and (dropdown_info is None):
            inputs.set(key1=argument_id, key2=argument_id, value=input_info)
        elif (input_info is None) and (dropdown_info is not None):
            dropdowns.set(key1=argument_id, key2=argument_id, value=dropdown_info)
    
    for i in range(branch_count):
        input_id = "SUBSTACK" if i == 0 else f"SUBSTACK{i+1}"
        input_info = InputInfo(
            type=BuiltinInputType.SCRIPT,
            menu=None,
        )
        inputs.set(key1=input_id, key2=input_id, value=input_info)
    
    disable_monitor = block_info.get("disableMonitor", False)
    can_have_monitor = opcode_type.is_reporter and (not inputs) and (not disable_monitor)
    if can_have_monitor:
        if dropdowns:
            monitor_id_hehaviour = MonitorIdBehaviour.OPCFULL_PARAMS
        else:
            monitor_id_hehaviour = MonitorIdBehaviour.OPCFULL
    else:
        monitor_id_hehaviour = None
    
    for attr in block_info.keys():
        if attr not in {
            "opcode", "blockType", "text", "arguments", "branchCount", "isTerminal", "disableMonitor", 
            # irrelevant for my purpose:
            "alignments", "hideFromPalette", "filter",
            "shouldRestartExistingThreads", "isEdgeActivated",
        }:
            raise UnknownExtensionAttributeError(attr)

    opcode_info = OpcodeInfo(
        opcode_type=opcode_type,
        inputs=inputs,
        dropdowns=dropdowns,
        can_have_monitor=can_have_monitor,
        monitor_id_behaviour=monitor_id_hehaviour,
        has_variable_id=bool(dropdowns), # if there are any dropdowns
    )
    
    text: str | list[str] = block_info["text"]
    text_lines: list[str] = text if isinstance(text, list) else [text]
    new_opcode_segments = []
    for i, text_line in enumerate(text_lines):
        line_segments = text_line.split(" ")
        for line_segment in line_segments:
            if not line_segment:
                continue
            elif line_segment.startswith("[") and line_segment.endswith("]"):
                argument_name = line_segment.removeprefix("[").removesuffix("]")
                # because of the scatterbrainedness of some extension devs:
                # fun fact: scatterbrainedness (ger. Schusseligkeit)
                if argument_name in arguments:
                    argument_type: str = arguments[argument_name].get("type", "string")
                else:
                    argument_type = "string"
                    input_info = InputInfo(
                        type=BuiltinInputType.TEXT,
                        menu=None,
                    )
                    inputs.set(key1=argument_name, key2=argument_name, value=input_info)
                
                if   inputs.has_key1(argument_name):
                    input_type = inputs.get_by_key1(argument_name).type
                    match input_type.mode:
                        case InputMode.BLOCK_AND_TEXT:
                            opening, closing = "(", ")"
                        case (
                            InputMode.BLOCK_AND_DROPDOWN
                          | InputMode.BLOCK_AND_BROADCAST_DROPDOWN
                          | InputMode.BLOCK_AND_MENU_TEXT
                        ):
                            opening, closing = "([", "])"
                        case InputMode.BLOCK_ONLY:
                            match input_type:
                                case BuiltinInputType.BOOLEAN:
                                    opening, closing = "<", ">"
                                case BuiltinInputType.ROUND | InputType.EMBEDDED_MENU:
                                    opening, closing = "(", ")"
                        case InputMode.SCRIPT:
                            opening, closing = "{", "}"
                                
                elif dropdowns.has_key1(argument_name):
                    dropdown_info = dropdowns.get_by_key1(argument_name)
                    opening, closing = "[", "]"
                elif argument_type == "image":
                    continue
                new_opcode_segments.append(f"{opening}{argument_name}{closing}")
            else:
                new_opcode_segments.append(line_segment)
        new_opcode_segments.append("{SUBSTACK}" if i == 0 else f"{{SUBSTACK{i+1}}}")
        
    if   branch_count == len(text_lines):
        pass
    elif (branch_count + 1) == len(text_lines):
        new_opcode_segments.pop()
    else:
        raise ValueError("`branchCount` must be equal to or at most 1 bigger then the line count of `text`")
    new_opcode = f"{extension_id}::{" ".join(new_opcode_segments)}"
    
    #print(opcode_info)
    #print("NEWOPC", new_opcode)
    #input()
    return (opcode_info, new_opcode)

def generate_opcode_info_group(extension_info: dict[str, Any]) -> tuple[OpcodeInfoGroup, type[InputType], type[DropdownType]]:
    """
    Generate a group of information about the blocks of the given extension and the classes containing the custom insput and dropdown types

    Args:
        extension_info: the raw extension information
    """
    extension_id = extension_info["id"] # TODO: get correct name
    menus: dict[str, dict[str, Any]|list] = extension_info.get("menus", {})
    info_group = OpcodeInfoGroup(
        name=extension_id,
        opcode_info=DualKeyDict(),
    )
    input_type_cls, dropdown_type_cls = process_all_menus(menus)
    
    for block_info in extension_info.get("blocks", []):
        opcode_info, new_opcode = generate_block_opcode_info(
            block_info, 
            menus=menus, 
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id=extension_id,
        )
        if opcode_info is not None:
            old_opcode: str = f"{extension_id}_{block_info['opcode']}"
            info_group.add_opcode(
                old_opcode  = old_opcode,
                new_opcode  = new_opcode,
                opcode_info = opcode_info,
            )
    
    for menu_opcode in menus.keys():
        menu_opcode = f"{extension_id}_menu_{menu_opcode}"
        opcode_info = OpcodeInfo(opcode_type=OpcodeType.MENU)
        info_group.add_opcode(menu_opcode, menu_opcode, opcode_info)
    return (info_group, input_type_cls, dropdown_type_cls)

def generate_file_code(
        info_group: OpcodeInfoGroup, 
        input_type_cls: type[InputType], 
        dropdown_type_cls: type[DropdownType],
    ) -> str:
    """
    Generate the code of a python file, which stores information about the blocks of the given extension and is required for the core module

    Args:
        info_group: the group of information about the blocks of the given extension
        input_type_cls: the generated class containing the custom input types
        dropdown_type_cls: the generated class containing the custom dropdown types
    """
    def generate_enum_code(enum_cls: type[PypenguinEnum]) -> str:
        cls_code = f"class {enum_cls.__name__}({enum_cls.__bases__[0].__name__}):"
        if len(enum_cls) == 0:
            return cls_code + f"\n{INDENT}pass"
        for enum_item in enum_cls:
            enum_item: PypenguinEnum
            cls_code += f"\n{INDENT}{enum_item.name} = {grepr(enum_item.value, level_offset=1)}"
        return cls_code
    
    file_code = "\n\n".join((
        "from pypenguin.opcode_info.data_imports import *",
        generate_enum_code(dropdown_type_cls),
        generate_enum_code(input_type_cls),
        f"{info_group.name} = {grepr(info_group, safe_dkd=True)}",
    ))
    return file_code

def generate_extension_info_py_file(extension: str, extension_id: str) -> str:
    """
    Generate a python file, which stores information about the blocks of the given extension and is required for the core module. Returns the file path of the python file

    Args:
        extension: the file path or https URL or JS Data URI of the extension code
        extension_id: the unique identifier of the extension 
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
        last_update_time = datetime.fromisoformat(file_cache["lastUpdate"])
        
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


    should_continue = consider_state(by_url=(extension.startswith("http://") or extension.startswith("https://")))
    if should_continue is False: # neither True nor Ellipsis
        print("PY STILL UP TO DATE")
        file_cache["lastUpdate"] = datetime.now(timezone.utc).isoformat()
        update_cache(cache)
        return destination_file_path
    js_code = fetch_js_code(extension)
    if file_cache is not None:
        js_fingerprint = ContentFingerprint.from_json(file_cache["jsFingerprint"])
        if (should_continue is ...) and js_fingerprint.matches(js_code):
            file_cache["lastUpdate"] = datetime.now(timezone.utc).isoformat()
            update_cache(cache)
            print("PY & JS STILL UP TO DATE")
            return destination_file_path
    
    extension_info = extract_getinfo(js_code)
    info_group, input_type_cls, dropdown_type_cls = generate_opcode_info_group(extension_info)
    file_code = generate_file_code(info_group, input_type_cls, dropdown_type_cls)
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
        ("dumbExample",         "example_extensions/js_extension/dumbExample.js"),
#        ("truefantombase",      "https://extensions.turbowarp.org/true-fantom/base.js"),
#        ("pmControlsExpansion", "example_extensions/js_extension/pmControlsExpansion.js"),
#        ("gpusb3",              "https://extensions.penguinmod.com/extensions/derpygamer2142/gpusb3.js"),
#        ("P7BoxPhys",           "https://extensions.penguinmod.com/extensions/pooiod/Box2D.js"),
    ]:
        generate_extension_info_py_file(extension, extension_id)
