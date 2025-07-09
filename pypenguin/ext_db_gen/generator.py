import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))); del sys, os

from aenum      import extend_enum
from subprocess import run as run_subprocess
from typing     import Any
from json       import loads

from pypenguin.opcode_info.api import (
    OpcodeInfoGroup, OpcodeInfo, OpcodeType, 
    InputInfo, InputMode, InputType, BuiltinInputType, MenuInfo, 
    DropdownInfo, DropdownType, BuiltinDropdownType, DropdownTypeInfo
)
from pypenguin.utility         import grepr, DualKeyDict, ThanksError

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

def extract_getinfo(ext_file: str) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class.
    A node subprocess is run, which lets the outer code run and then calls and logs the return value of the getInfo method of the extension class.
    
    Args:
        the file path or https URL or JS Data URI of the extension code
    
    """
    result = run_subprocess(
        ["node", "pypenguin/ext_db_gen/extractor.js", ext_file],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return loads(result.stdout)
    # Returned properties:
    #     ["id", "name", "color1", "menuIconURI", "blocks", "menus"])
    # Of these:
    #     Irrelevant: ["id", "name", "color1", "menuIconURI"]
    #     Relevant:   ["blocks", "menus"]

def process_all_menus(menus: dict[str, dict[str, Any]]) -> tuple[type[InputType], type[DropdownType]]:
    # TODO: docstring
    class ExtensionInputType(InputType):
        pass
    class ExtensionDropdownType(DropdownType):
        pass

    menu_index = 0
    for menu_block_id, menu_info in menus.items():
        possible_values: list[str] = menu_info["items"]
        accept_reporters = menu_info.get("acceptReporters", False)
        dropdown_type_info = DropdownTypeInfo(
            direct_values     = possible_values,
            rules             = [], # we assume the possible menu values are static
            old_direct_values = possible_values,
            fallback          = None, # there can't be a fallback when the possible values are static
        )
        custom_dropdown_type = extend_enum(ExtensionDropdownType, name=menu_block_id, value=dropdown_type_info)

        if accept_reporters:
            #                 (InputMode                   , magic number, corresponding dropdown type, index     )
            input_type_info = (InputMode.BLOCK_AND_DROPDOWN, None        , custom_dropdown_type       , menu_index)
            custom_input_type = extend_enum(ExtensionInputType, name=menu_block_id, value=input_type_info)
        menu_index += 1
    return (ExtensionInputType, ExtensionDropdownType)

def generate_block_opcode_info(
        block_info: dict[str, Any], 
        menus: dict[str, dict[str, Any]],
        input_type_cls: type[InputType],
        dropdown_type_cls: type[DropdownType],
        extension_id: str,
    ) -> OpcodeInfo | None:
    # TODO: docstring
    print()
    print()
    print("CURRENT BLOCK", grepr(block_info))
    
    block_type: str = block_info["blockType"]
    arguments: dict[str, dict[str, Any]] = block_info["arguments"]
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
            raise NotImplementedError() # TODO: add a subscript at the end or smth
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
                    assert builitin_input_type is BuiltinInputType.TEXT, 'If "menu" exists, "type" should be Scratch.ArgumentType.STRING'
                    accept_reporters = menus[argument_menu].get("acceptReporters", False)

                    if accept_reporters:
                        input_info = InputInfo(
                            type=getattr(input_type_cls, argument_menu),
                            menu=MenuInfo(
                                opcode=argument_menu,
                                inner=argument_menu, # menu opcode seems to also be used as field name
                            ),
                        )
                    else:
                        dropdown_info = DropdownInfo(type=getattr(dropdown_type_cls, argument_menu)) # TODO: test
            case "variable"|"list":
                dropdown_type_cls = ARGUMENT_TYPE_TO_DROPDOWN_TYPE[argument_type]
            case "image":
                pass # not really an input or dropdown
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

    
    opcode_info = OpcodeInfo(
        opcode_type=opcode_type,
        inputs=inputs,
        dropdowns=dropdowns,
    )
    #    inputs: DualKeyDict[str, str, InputInfo] = field(default_factory=DualKeyDict)
    #    dropdowns: DualKeyDict[str, str, DropdownInfo] = field(default_factory=DualKeyDict)
    #    can_have_monitor: bool = False
    #    monitor_id_behaviour: MonitorIdBehaviour | None = None
    #    has_shadow: bool = None
    #    special_cases: dict[SpecialCaseType, SpecialCase] = field(default_factory=dict)
    #    old_mutation_cls: Type["FRMutation"] | None = field(init=False, default_factory=type(None))
    #    new_mutation_cls: Type["SRMutation"] | None = field(init=False, default_factory=type(None))
    print(opcode_info)
    raise Exception("HALT")

def generate_opcode_info_group(extension_info: dict[str, Any]) -> OpcodeInfoGroup:
    # TODO: docstring
    print(grepr(extension_info))
    info_group = OpcodeInfoGroup(
        name=extension_info["id"], # TODO: get correct name
        opcode_info=DualKeyDict(),
    )
    input_type_cls, dropdown_type_cls = process_all_menus(extension_info["menus"])

    for block_info in extension_info["blocks"]:
        generate_block_opcode_info(
            block_info, 
            menus=extension_info["menus"], 
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id=extension_info["id"],
        )

extension_info = extract_getinfo("pypenguin/ext_db_gen/example.js")
generate_opcode_info_group(extension_info)

