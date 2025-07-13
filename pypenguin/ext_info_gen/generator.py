import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))); del sys, os

from aenum      import extend_enum, Enum
from subprocess import run as run_subprocess
from typing     import Any, Callable
from json       import loads

from pypenguin.opcode_info.api import (
    OpcodeInfoGroup, OpcodeInfo, OpcodeType, MonitorIdBehaviour,
    InputInfo, InputMode, InputType, BuiltinInputType, MenuInfo,
    DropdownInfo, DropdownType, BuiltinDropdownType, DropdownTypeInfo,
)
from pypenguin.utility         import grepr, DualKeyDict, ThanksError, PypenguinEnum

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


def extract_getinfo(extension: str) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class.
    A node subprocess is run, which lets the outer code run and then calls and logs the return value of the getInfo method of the extension class.
    
    Args:
        extension: the file path or https URL or JS Data URI of the extension code
    """
    result = run_subprocess(
        ["node", EXTRACTOR_PATH, extension],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    info = loads(result.stdout.splitlines()[-1]) # avoid error, when extension itself logs sth
    # Of the returned attributes:
    #     Irrelevant: ["name", "color1", "color2", "color3", "menuIconURI"]
    #     Relevant:   ["id", "blocks", "menus"]
    for attr in info.keys():
        if attr not in {"name", "color1", "color2", "color3", "menuIconURI", "isDynamic", "id", "blocks", "menus"}:
            raise Exception(attr)#ThanksError()
    return info

def process_all_menus(menus: dict[str, dict[str, Any]]) -> tuple[type[InputType], type[DropdownType]]:
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
        possible_values: list[str] = menu_info["items"]
        accept_reporters = menu_info.get("acceptReporters", False)
        dropdown_type_info = DropdownTypeInfo(
            direct_values     = possible_values,
            rules             = [], # we assume the possible menu values are static
            old_direct_values = possible_values,
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
    ) -> OpcodeInfo | None:
    """
    Generate the opcode information for one kind of block

    Args:
        block_info: the raw block information
        menus: the dict mapping menu id to menu information
        input_type_cls: the generated class containing the custom input types
        dropdown_type_cls: the generated class containing the custom dropdown types
        extension_id: the id of the extension
    """
    #print()
    #print()
    print("CURRENT BLOCK", grepr(block_info))
    
    block_type: str = block_info["blockType"]
    arguments: dict[str, dict[str, Any]] = block_info.get("arguments", {})
    branch_count: int = block_info.get("branchCount", 0)
    opcode_type: OpcodeType
    match block_type:
        case "command":
            opcode_type = OpcodeType.STATEMENT
        case "reporter":
            opcode_type = OpcodeType.STRING_REPORTER
        case "Boolean":
            opcode_type = OpcodeType.BOOLEAN_REPORTER
        case "hat" | "event":
            opcode_type = OpcodeType.HAT
        case "conditional" | "loop":
            opcode_type = OpcodeType.STATEMENT
            branch_count = max(branch_count, 1)
            #raise NotImplementedError() # TODO: add a subscript at the end or smth
        case "label" | "button":
            return None # not really block, but a label or button
        case "xml":
            raise NotImplementedError("XML blocks are NOT supported. It is pretty much impossible to translate them into a database entry.")
        case _:
            raise ValueError(f"Unknown value for blockType: {repr(block_type)}")
    
    inputs = DualKeyDict()
    dropdowns = DualKeyDict()

    for argument_id, argument_info in arguments.items():
        argument_type: str = argument_info["type"]
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
                    accept_reporters = menus[argument_menu].get("acceptReporters", False)

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
        else:
            raise Exception()
    
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
        if attr not in {"opcode", "blockType", "text", "arguments"}:
            raise Exception(attr)#ThanksError()

    opcode_info = OpcodeInfo(
        opcode_type=opcode_type,
        inputs=inputs,
        dropdowns=dropdowns,
        can_have_monitor=can_have_monitor,
        monitor_id_behaviour=monitor_id_hehaviour,
        has_variable_id=bool(dropdowns), # if there are any dropdowns
    )
    #print(opcode_info)
    #input()
    return opcode_info

def generate_opcode_info_group(extension_info: dict[str, Any]) -> tuple[OpcodeInfoGroup, type[InputType], type[DropdownType]]:
    """
    Generate a group of information about the blocks of the given extension and the classes containing the custom input and dropdown types

    Args:
        extension_info: the raw extension information
    """
    extension_id = extension_info["id"] # TODO: get correct name
    menus: dict[str, dict[str, Any]] = extension_info.get("menus", {})
    info_group = OpcodeInfoGroup(
        name=extension_id,
        opcode_info=DualKeyDict(),
    )
    input_type_cls, dropdown_type_cls = process_all_menus(menus)
    
    for block_info in extension_info.get("blocks", []):
        opcode_info = generate_block_opcode_info(
            block_info, 
            menus=menus, 
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id=extension_id,
        )
        if opcode_info is not None:
            opcode: str = f"{extension_id}_{block_info['opcode']}"
            info_group.add_opcode(
                old_opcode  = opcode,
                new_opcode  = opcode, # TODO: possibly base new opcode off "text"
                opcode_info = opcode_info,
            )
    
    for menu_opcode, menu_info in menus.items():
        menu_opcode = f"{extension_id}_menu_{menu_opcode}"
        opcode_info = OpcodeInfo(opcode_type=OpcodeType.MENU)
        info_group.add_opcode(menu_opcode, menu_opcode, opcode_info)
    return (info_group, input_type_cls, dropdown_type_cls)

def generate_file_code(info_group: OpcodeInfoGroup, input_type_cls: type[InputType], dropdown_type_cls: type[DropdownType]) -> str:
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

def generate_extension_info_py_file(extension: str, destination_gen: Callable[[str], str]) -> None:
    """
    Generate a python file, which stores information about the blocks of the given extension and is required for the core module

    Args:
        extension: the file path or https URL or JS Data URI of the extension code
        destination: the destination path for the generated python file
    """
    extension_info = extract_getinfo(extension)
    info_group, input_type_cls, dropdown_type_cls = generate_opcode_info_group(extension_info)
    file_code = generate_file_code(info_group, input_type_cls, dropdown_type_cls)
    destination = destination_gen(info_group.name)
    with open(destination, "w") as destination_file:
        destination_file.write(file_code)
        

for extension in [
    "example_extensions/js_extension/dumbExample.js",
    "https://extensions.turbowarp.org/true-fantom/base.js",
    "example_extensions/js_extension/pmControlsExpansion.js",
]:
    generate_extension_info_py_file(
        extension=extension,
        destination_gen=lambda extension_id: f"example_extensions/gen_opcode_info/{extension_id}.py"
    )

