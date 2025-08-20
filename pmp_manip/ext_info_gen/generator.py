from aenum        import extend_enum
from typing       import Any

from pmp_manip.opcode_info.api import (
    OpcodeInfoGroup, OpcodeInfo, OpcodeType, MonitorIdBehaviour,
    InputInfo, InputMode, InputType, BuiltinInputType, MenuInfo,
    DropdownInfo, DropdownType, BuiltinDropdownType, DropdownTypeInfo,
    DropdownValueRule,
)
from pmp_manip.utility         import (
    grepr, DualKeyDict, GEnum,
    MANIP_ThanksError, MANIP_TempNotImplementedError, MANIP_NotImplementedError,
    MANIP_InvalidCustomMenuError, MANIP_InvalidCustomBlockError,
    MANIP_UnknownExtensionAttributeError, 
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
DATA_IMPORTS_IMPORT_PATH = "pmp_manip.opcode_info.data_imports"

    
def process_all_menus(menus: dict[str, dict[str, Any]|list]) -> tuple[type[InputType], type[DropdownType]]:
    """
    Process all menus of an extension. Returns two classes, which contain the dervied input and dropdown types
    
    Args:
        menus: the dict mapping menu id to menu information
    
    Raises:
        MANIP_InvalidCustomMenuError: if the information about a menu is invalid 
    """
    class ExtensionInputType(InputType):
        pass
    class ExtensionDropdownType(DropdownType):
        pass

    for menu_index, menu_block_id, menu_info in zip(range(len(menus)), menus.keys(), menus.values()):
        possible_values: list[str|dict[str, str]]
        rules: list[DropdownValueRule] = []
        accept_reporters: bool
        try:
            assert isinstance(menu_info, (dict, list))
            if   isinstance(menu_info, dict):
                if "items" not in menu_info:
                    raise MANIP_InvalidCustomMenuError(f"Invalid custom menu {menu_block_id!r} is missing attribute 'items'")
                possible_values = menu_info["items"]
                accept_reporters = menu_info.get("acceptReporters", False)
            elif isinstance(menu_info, list):
                possible_values = menu_info
                accept_reporters = False
        
            assert isinstance(possible_values, (list, str))
            if   isinstance(possible_values, list): pass
            elif isinstance(possible_values, str):
                possible_values = []
                rules.append(DropdownValueRule.EXTENSION_UNPREDICTABLE)
            
            new_possible_values = []
            old_possible_values = []
            for i, possible_value in enumerate(possible_values):
                assert isinstance(possible_value, (str, dict))
                if   isinstance(possible_value, str):
                    new_possible_values.append(possible_value)
                    old_possible_values.append(possible_value)
                elif isinstance(possible_value, dict):
                    if "text" not in possible_value:
                        raise MANIP_InvalidCustomMenuError(f"Invalid custom menu {menu_block_id!r}: item {i} is missing attribute 'text'")
                    if "value" not in possible_value:
                        raise MANIP_InvalidCustomMenuError(f"Invalid custom menu {menu_block_id!r}: item {i} is missing attribute 'value'")
                    new_possible_values.append(possible_value["text"])
                    old_possible_values.append(possible_value["value"])
            
            dropdown_type_info = DropdownTypeInfo(
                direct_values     = new_possible_values,
                rules             = rules, # we assume the possible menu values are static
                old_direct_values = old_possible_values,
                fallback          = None, # there can not be a fallback when the possible values are static
            )
            custom_dropdown_type = extend_enum(ExtensionDropdownType, menu_block_id, dropdown_type_info)
    
            if accept_reporters:
                input_type_info = (
                    InputMode.BLOCK_AND_DROPDOWN, # InputMode
                    None, # magic number
                    custom_dropdown_type, # corresponding dropdown type,
                    menu_index, # uniqueness index
                )
                extend_enum(ExtensionInputType, menu_block_id, input_type_info)
        except AssertionError as error:
            raise MANIP_InvalidCustomMenuError(f"Invalid custom menu {repr(menu_block_id)}: {menu_info}") from error
    return (ExtensionInputType, ExtensionDropdownType)

def generate_block_opcode_info(
        block_info: dict[str, Any], 
        menus: dict[str, dict[str, Any] | list],
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
    
    Raises:
        MANIP_InvalidCustomBlockError: if the block information is invalid
        MANIP_NotImplementedError: if an XML block is given to this function
        MANIP_UnknownExtensionAttributeError: if the block has an unknown attribute
        MANIP_ThanksError: if an argument uses the mysterious Scratch.ArgumentType.SEPERATOR
    """
    def process_arguments(
            arguments: dict[str, dict[str, Any]], 
            menus: dict[str, dict|list],
            input_type_cls: type[InputType],
            dropdown_type_cls: type[DropdownType],
   ) -> tuple[DualKeyDict[str, str, InputInfo], DualKeyDict[str, str, DropdownInfo]]:
        """
        Process the argument information into input and field information
        
        Args:
            arguments: the argument information
            menus: the dict mapping menu id to menu information
            input_type_cls: the generated class containing the custom input types
            dropdown_type_cls: the generated class containing the custom dropdown types
        
        Raises:
            ValueError: if a non-existant menu is referenced or a menu link is combined with a not matching argument type
            MANIP_TempNotImplementedError: ...
            MANIP_ThanksError: if the mysterious Scratch.ArgumentType.SEPERATOR is used
        """
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
                        if argument_menu not in menus:
                            raise ValueError(f"Argument {repr(argument_id)}: 'menu' must refer to an existing menu")
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
                    continue # not really an input or dropdown, should be skipped
                case "polygon": # pragma: no cover
                    raise MANIP_TempNotImplementedError() # TODO, only necessary for the few polygon blocks(pen ext) # pragma: no cover
                case "seperator":
                    raise MANIP_ThanksError() # I could not find out what thats used for
            
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
        return (inputs, dropdowns)
    
    def generate_new_opcode(
        text: str | list[str], 
        arguments: dict[str, dict[Any]],
        inputs: DualKeyDict[str, str, InputInfo],
        dropdowns: DualKeyDict[str, str, DropdownInfo],
        branch_count: int,
    ) -> str:
        """
        Generate the new opcode of a block based on the text field. Might modify inputs
        
        Args:
            text: the text attribute of the block info
            arguments: the argument information
            branch_count: the count of substacks the block has
        
        Raises:
            ValueError: if 'branchCount' and 'text' do not match    
        """
        
        def get_input_argument_brackets(input_type: InputType) -> tuple[str, str]:
            """
            Get the bracket formatting of an input required for new opcodes
            
            Args:
                input_type: the type of input
            """
            match input_type.mode: # pragma: no cover
                case InputMode.BLOCK_AND_TEXT: # pragma: no cover
                    return "(", ")" # pragma: no cover
                case (
                    InputMode.BLOCK_AND_DROPDOWN
                  | InputMode.BLOCK_AND_BROADCAST_DROPDOWN
                  | InputMode.BLOCK_AND_MENU_TEXT
                ): # pragma: no cover
                    return "([", "])" # pragma: no cover
                case InputMode.BLOCK_AND_BOOL: # pragma: no cover
                     match input_type: # pragma: no cover
                        case BuiltinInputType.BOOLEAN: # pragma: no cover
                            return "<", ">" # pragma: no cover
                case InputMode.BLOCK_ONLY: # pragma: no cover
                    match input_type: # pragma: no cover
                        case BuiltinInputType.ROUND: # pragma: no cover
                            return "(", ")" # pragma: no cover
                case InputMode.SCRIPT: # pragma: no cover
                    return "{", "}" # pragma: no cover
        
        text_lines: list[str] = text if isinstance(text, list) else [text]
        new_opcode_segments = []
        for i, text_line in enumerate(text_lines):
            line_segments = text_line.split(" ")
            for line_segment in line_segments:
                if not line_segment:
                    continue
                if line_segment.startswith("[") and line_segment.endswith("]"):
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
                    
                    if   inputs   .has_key1(argument_name):
                        input_type = inputs.get_by_key1(argument_name).type
                        opening, closing = get_input_argument_brackets(input_type)
                    elif dropdowns.has_key1(argument_name):
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
            raise ValueError("'branchCount' must be equal to or at most 1 bigger then the line count of 'text'")
        return f"{extension_id}::{" ".join(new_opcode_segments)}" 
    
    try:
        block_type: str = block_info["blockType"]
        branch_count: int = block_info.get("branchCount", 0)
        is_terminal: bool = block_info.get("isTerminal", False)
        arguments: dict[str, dict[str, Any]] = block_info.get("arguments", {})
        opcode_type: OpcodeType
        if is_terminal and (block_type != "command"):
            raise ValueError("'isTerminal' can only be True when 'blockType' is Scratch.BlockType.COMMAND(='command')")

        
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
                raise MANIP_NotImplementedError("XML blocks are NOT supported. It is pretty much impossible to translate one into a database entry.") # TODO: reconsider
            case _:
                raise ValueError(f"Unknown value for blockType: {repr(block_type)}")
        
        opcode: str = block_info["opcode"] # might not be included so must come after eg. "label" blocks have returned alredy       
        
        inputs, dropdowns = process_arguments(arguments, menus, input_type_cls, dropdown_type_cls)
                
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
                "alignments", "hideFromPalette", "filter", "shouldRestartExistingThreads", 
                "isEdgeActivated", "func", # TODO: find all remaining attriubtes
            }:
                block_opcode = repr(block_info.get('opcode', 'Unknown'))
                raise MANIP_UnknownExtensionAttributeError(f"Unknown or not (yet) implemented block attribute (block {block_opcode}): {repr(attr)}")
    
        new_opcode = generate_new_opcode(
            text=block_info["text"],
            arguments=arguments,
            inputs=inputs,
            dropdowns=dropdowns,
            branch_count=branch_count,
        ) # first because inputs might change

        opcode_info = OpcodeInfo(
            opcode_type=opcode_type,
            inputs=inputs,
            dropdowns=dropdowns,
            can_have_monitor=can_have_monitor,
            monitor_id_behaviour=monitor_id_hehaviour,
            has_variable_id=(can_have_monitor and bool(dropdowns)), # if there are any dropdowns
        )
        
    except (KeyError, ValueError) as error:
        block_opcode = repr(block_info.get('opcode', 'Unknown'))
        if   isinstance(error, KeyError):
            raise MANIP_InvalidCustomBlockError(f"Invalid block info missing attribute {error} (block {block_opcode}): {block_info}") from error
        elif isinstance(error, ValueError):
            raise MANIP_InvalidCustomBlockError(f"Invalid block info (block {block_opcode}): {error}: {block_info}") from error
    
    return (opcode_info, new_opcode)

def generate_opcode_info_group(extension_info: dict[str, Any]) -> tuple[OpcodeInfoGroup, type[InputType], type[DropdownType]]:
    """
    Generate a group of information about the blocks of the given extension and the classes containing the custom insput and dropdown types

    Args:
        extension_info: the raw extension information
    
    Raises:
        MANIP_UnknownExtensionAttributeError: if the extension or a block has an unknown attribute
        MANIP_InvalidCustomMenuError: if the information about a menu is invalid
        MANIP_InvalidCustomBlockError: if information of a block is invalid
        MANIP_NotImplementedError: if an XML block is included in the extension info
        MANIP_ThanksError: if a block argument uses the mysterious Scratch.ArgumentType.SEPERATOR
    """
    # Relevant of the returned attributes: ["id", "blocks", "menus"]
    for attr in extension_info.keys():
        if attr not in {
            "name", "color1", "color2", "color3", "menuIconURI", "blockIconURI", "docsURI", "isDynamic", "orderBlocks",
            "id", "blocks", "menus", # TODO: find all remaining attriubtes
        }:
            raise MANIP_UnknownExtensionAttributeError(f"Unknown or not (yet) implemented extension attribute: {repr(attr)}")

    
    extension_id = extension_info["id"] # TODO: get correct name
    menus: dict[str, dict[str, Any]|list] = extension_info.get("menus", {})
    info_group = OpcodeInfoGroup(
        name=extension_id,
        opcode_info=DualKeyDict(),
    )
    input_type_cls, dropdown_type_cls = process_all_menus(menus)
    
    for i, block_info in enumerate(extension_info.get("blocks", [])):
        if isinstance(block_info, str):
            continue # ignore eg. "---"
        elif isinstance(block_info, dict):
            opcode_info, new_opcode = generate_block_opcode_info(
                block_info, 
                menus=menus, 
                input_type_cls=input_type_cls,
                dropdown_type_cls=dropdown_type_cls,
                extension_id=extension_id,
            )
        else:
            raise MANIP_InvalidCustomBlockError(f"Invalid block info: Expected type str or dict (block {i}): {block_info}")
        
        if opcode_info is not None:
            old_opcode: str = f"{extension_id}_{block_info['opcode']}" # 'opcode' is guaranteed to exist
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
    def generate_enum_code(enum_cls: type[GEnum]) -> str:
        """
        Generate the python code which can recreate the given Enum class
        
        Args:
            enum_cls: the Enum class
        """
        cls_code = f"class {enum_cls.__name__}({enum_cls.__bases__[0].__name__}):"
        if len(enum_cls) == 0:
            return cls_code + f"\n{INDENT}pass"
        for enum_item in enum_cls:
            enum_item: GEnum
            cls_code += f"\n{INDENT}{enum_item.name} = {grepr(enum_item.value, level_offset=1)}"
        return cls_code
    
    file_code = "\n\n".join((
        f"from {DATA_IMPORTS_IMPORT_PATH} import *",
        generate_enum_code(dropdown_type_cls),
        generate_enum_code(input_type_cls),
        f"ext_{info_group.name} = {grepr(info_group, safe_dkd=True)}",
    ))
    return file_code


__all__ = ["generate_opcode_info_group", "generate_file_code"]

