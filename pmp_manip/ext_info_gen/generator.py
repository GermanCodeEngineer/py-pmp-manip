from __future__ import annotations
from copy       import copy
from typing     import Any

from pmp_manip.opcode_info.api import (
    OpcodeInfoGroup, OpcodeInfo, OpcodeType, MonitorIdBehaviour,
    InputInfo, InputMode, InputType, BuiltinInputType, MenuInfo,
    DropdownInfo, DropdownType, BuiltinDropdownType, DropdownTypeInfo,
    DropdownValueRule,
)
from pmp_manip.utility         import (
    grepr, DualKeyDict, GEnum,
    MANIP_ThanksError, MANIP_ValueError, MANIP_NotImplementedError,
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
KNOWN_EXTENSION_INFO_ATTRS = {
    "id", "blocks", "menus",
    # irrelevant for my purpose:
    "name", "color1", "color2", "color3", "menuIconURI", "blockIconURI",
    "docsURI", "isDynamic", "orderBlocks", "showStatusButton",
    "autoLoad", "blockText",
}

def find_input_and_dropdown_types(
        menus: dict[str, dict[str, Any]|list], blocks: list[dict[str, Any] | str], 
        extension_id: str
    ) -> tuple[dict[str, InputType], dict[str, DropdownType]]:
    """
    Returns two dictionaries, which contain the derived input and dropdown types based on arguments and shadows
    
    Args:
        menus: the dict mapping menu id to menu information
        blocks: the block information
        extension_id: the id of the extension
    
    Raises:
        MANIP_InvalidCustomMenuError: if the information about a menu is invalid 
    """
    input_types: dict[str, InputType] = {}
    dropdown_types: dict[str, DropdownType] = {}

    for menu_index, menu_block_id, menu_info in zip(range(len(menus)), menus.keys(), menus.values()):
        possible_values: list[str|dict[str, str]]
        rules: list[DropdownValueRule] = []
        accept_reporters: bool
        is_typeable: bool = False

        if not isinstance(menu_info, (dict, list, str)):
            raise MANIP_InvalidCustomMenuError(f"Invalid custom menu {menu_block_id!r}: must be an object, array or string(method reference)")
        if   isinstance(menu_info, dict):
            possible_values = menu_info.get("items", [])
            is_typeable = menu_info.get("isTypeable", False)
            accept_reporters = menu_info.get("acceptReporters", is_typeable)
        elif isinstance(menu_info, (list, str)):
            possible_values = menu_info
            accept_reporters = False

        
        if not isinstance(possible_values, (dict, list, str)):
            raise MANIP_InvalidCustomMenuError(f"Invalid custom menu {menu_block_id!r}: 'items' must be an array or string(method reference)")
        if   isinstance(possible_values, list): pass
        elif isinstance(possible_values, str): # str refers to a function and is therefore unpredictable
            possible_values = []
            rules.append(DropdownValueRule.EXTENSION_UNPREDICTABLE)
        
        new_possible_values = []
        old_possible_values = []
        for i, possible_value in enumerate(possible_values):
            if not isinstance(possible_value, (str, dict, list)):
                raise MANIP_InvalidCustomMenuError(f"Invalid custom menu {menu_block_id!r}: item {i}: must be a string, object, or array(2 items)")
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
            elif isinstance(possible_value, list):
                if len(possible_value) != 2:
                    raise MANIP_InvalidCustomMenuError(f"Invalid custom menu {menu_block_id!r}: item {i}: must have 2 items for an array")
                new_possible_values.append(possible_value[0])
                old_possible_values.append(possible_value[1])
        if is_typeable:
            old_possible_values = new_possible_values # "value" is not supported, see:
            # https://github.com/PenguinMod/PenguinMod-Docs/blob/654adb5afe4087b67549d7838d25862ec1a20785/docs/development/extensions/api/categories/category-info.md?plain=1#L27            

        dropdown_type_info = DropdownTypeInfo(
            direct_values     = new_possible_values,
            rules             = rules, # we assume the possible menu values are static
            old_direct_values = old_possible_values,
            fallback          = None, # there can not be a fallback when the possible values are static
        )
        dropdown_types[menu_block_id] = dropdown_type_info

        if accept_reporters:
            input_type_info = (
                InputMode.BLOCK_AND_DROPDOWN, # InputMode
                None, # magic number or old forced block opcode
                menu_block_id, # NAME of corresponding dropdown type, replaced below
                menu_index, # uniqueness index
            )
            input_types[f"M_{menu_block_id}"] = input_type_info
    
    for block_info in blocks: # TODO: add tests
        # Other types handled later
        if isinstance(block_info, dict):
            for argument_id, argument_info in block_info.get("arguments", {}).items():
                full_opcode = argument_info.get("fillInGlobal")
                if not(full_opcode) and argument_info.get("fillIn"):
                    full_opcode = f"{extension_id}_{argument_info["fillIn"]}"
                if full_opcode:
                    fill_in_id = f"S_{full_opcode}"
                    if fill_in_id not in input_types:
                        # opcode makes them necessarily different, so the uniqueness values do not matter
                        input_types[fill_in_id] = (InputMode.FORCED_EMBEDDED_BLOCK, full_opcode, None, -1)
    
    # Create the dropdown enum first
    ExtensionDropdownType = DropdownType("ExtensionDropdownType", dropdown_types)
    
    # Now replace dropdown type names with actual DropdownType enum members in input_types dict
    for key, input_type_info in list(input_types.items()):
        if input_type_info[2] is not None and isinstance(input_type_info[2], str):
            input_types[key] = (
                input_type_info[0],
                input_type_info[1],
                ExtensionDropdownType[input_type_info[2]],
                input_type_info[3],
            )
    
    # Now create the input enum
    ExtensionInputType = InputType("ExtensionInputType", input_types)
    
    return (copy(ExtensionInputType._member_map_), copy(ExtensionDropdownType._member_map_))

def generate_block_opcode_info(
        block_info: dict[str, Any], 
        menus: dict[str, dict[str, Any] | list],
        input_types: dict[str, InputType],
        dropdown_types: dict[str, DropdownType],
        extension_id: str,
    ) -> tuple[OpcodeInfo, str] | tuple[None, None]:
    """
    Generate the opcode information for one kind of block and the block opcode in 'new style'

    Args:
        block_info: the raw block information
        menus: the dict mapping menu id to menu information
        input_types: the custom input types
        dropdown_types: the custom dropdown types
        extension_id: the id of the extension
    
    Raises:
        MANIP_InvalidCustomBlockError: if the block information is invalid
        MANIP_NotImplementedError: if an XML block is given to this function
        MANIP_ThanksError: if an argument uses the mysterious Scratch.ArgumentType.SEPERATOR
    """
    def process_arguments(
            arguments: dict[str, dict[str, Any]], 
            menus: dict[str, dict|list],
            input_types: dict[str, InputType],
            dropdown_types: dict[str, DropdownType],
   ) -> tuple[DualKeyDict[str, str, InputInfo], DualKeyDict[str, str, DropdownInfo]]:
        """
        Process the argument information into input and field information. Completes input_types
        
        Args:
            arguments: the argument information
            menus: the dict mapping menu id to menu information
            input_types: the custom input types
            dropdown_types: the custom dropdown types
        
        Raises:
            ValueError: if a non-existant menu is referenced or a menu link is combined with a not matching argument type
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
                    fill_in_opcode = argument_info.get("fillIn")
                    fill_in_global_opcode = argument_info.get("fillInGlobal")
                    if fill_in_opcode or fill_in_global_opcode:
                        full_opcode = fill_in_global_opcode if fill_in_global_opcode else f"{extension_id}_{fill_in_opcode}"
                        fill_in_id = f"S_{full_opcode}"
                        if fill_in_id not in input_types:
                            # opcode makes them necessarily different, so the uniqueness values do not matter
                            temp_cls = InputType("Temp", {
                                fill_in_id: (InputMode.FORCED_EMBEDDED_BLOCK, full_opcode, None, -1)
                            })
                            input_types[fill_in_id] = temp_cls[fill_in_id]
                        input_info = InputInfo(
                            type=input_types[fill_in_id],
                            menu=None,
                        )
                    elif argument_menu is None:
                        menu = MenuInfo(opcode="note", inner="NOTE") if builitin_input_type is BuiltinInputType.NOTE else None
                        input_info = InputInfo(
                            type=builitin_input_type,
                            menu=menu,
                        )
                    else:
                        if argument_menu not in menus:
                            raise ValueError(f"Argument {repr(argument_id)}: 'menu' must refer to an existing menu")
                        menu_info = menus[argument_menu]
                        if   isinstance(menu_info, dict):
                            accept_reporters = menu_info.get("acceptReporters", menu_info.get("isTypeable", False))
                        else:
                            accept_reporters = False

                        if accept_reporters:
                            input_info = InputInfo(
                                type=input_types[f"M_{argument_menu}"],
                                menu=MenuInfo(
                                    opcode=f"{extension_id}_menu_{argument_menu}",
                                    inner=argument_menu, # menu opcode seems to also be used as field name
                                ),
                            )
                        else:
                            dropdown_info = DropdownInfo(type=dropdown_types[argument_menu])
                case "variable"|"list":
                    builtin_dropdown_type = ARGUMENT_TYPE_TO_DROPDOWN_TYPE[argument_type]
                    dropdown_info = DropdownInfo(type=builtin_dropdown_type)
                case "image":
                    continue # not really an input or dropdown, should be skipped
                case "polygon":
                    input_info = InputInfo(type=BuiltinInputType.POLYGON, menu=None)
                case "seperator":
                    raise MANIP_ThanksError() # I could not find out what thats used for
                case None: # # like in the "switch" block, no text just an optional block
                    input_info = InputInfo(type=BuiltinInputType.ROUND, menu=None)
            
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
                case InputMode.FORCED_EMBEDDED_BLOCK: # pragma: no cover
                    return "{:", ":}" # pragma: no cover
        
        text_lines: list[str] = text if isinstance(text, list) else [text]
        unified_text = "\n".join(text_lines)
        if ("{{" in unified_text) or ("}}" in unified_text):
            raise ValueError(f"'text' must not contain double curly brackets ('{{' or '}}')")
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
                    
                    if   inputs.has_key1(argument_name):
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
        prefix = overwrite_category if (overwrite_category is not None) else extension_id
        return f"&{prefix}::{" ".join(new_opcode_segments)}" 
    
    try:
        block_type: str = block_info.get("blockType", "command")
        branch_count: int = block_info.get("branchCount", None)
        branches_alt: list = block_info.get("branches", None)
        allow_embedded: bool = bool(block_info.get("canDragDuplicate", False))
        if isinstance(branch_count, int):
            pass
        elif isinstance(branches_alt, list):
            branch_count = len(branches_alt)
        else:
            branch_count = 0
        is_final_opcode: bool = block_info.get("ppm_final_opcode", False) # Custom property
        
        is_terminal: bool = bool(block_info.get("isTerminal", False) or block_info.get("terminal", False))
        arguments: dict[str, dict[str, Any]] = block_info.get("arguments", {})
        opcode_type: OpcodeType
        if is_terminal and (block_type != "command"):
            raise ValueError("'isTerminal'/'terminal' can only be True when 'blockType' is Scratch.BlockType.COMMAND(='command')")

        
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
                raise ValueError("Unknown value for 'blockType'")
        
        if "opcode" not in block_info:
            raise MANIP_InvalidCustomBlockError(f"Invalid block info missing attribute 'opcode' (block 'Unknown'): {block_info}")  
        opcode: str = block_info["opcode"] # might not be included so must come after eg. "label" blocks have returned alredy
        if is_final_opcode:
            overwrite_category = opcode.split("_", maxsplit=1)[0]
        else:
            overwrite_category = None
        
        inputs, dropdowns = process_arguments(arguments, menus, input_types, dropdown_types)
        
        disable_monitor = block_info.get("disableMonitor", None)
        checkbox_in_flyout = block_info.get("checkboxInFlyout", None)
        if isinstance(disable_monitor, bool):
            pass
        elif isinstance(checkbox_in_flyout, bool):
            disable_monitor = not checkbox_in_flyout
        else:
            disable_monitor = False
        
        can_have_monitor = opcode_type.is_reporter and (not inputs) and (not disable_monitor)
        if can_have_monitor:
            if dropdowns:
                monitor_id_hehaviour = MonitorIdBehaviour.OPCFULL_PARAMS
            else:
                monitor_id_hehaviour = MonitorIdBehaviour.OPCFULL
        else:
            monitor_id_hehaviour = None
            
        new_opcode = generate_new_opcode(
            text=block_info.get("text", opcode),
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
            allow_embedded=allow_embedded,
        )
        
    except ValueError as error:
        block_opcode = repr(block_info.get('opcode', 'Unknown'))
        raise MANIP_InvalidCustomBlockError(f"Invalid block info (block {block_opcode}): {error}: {block_info}") from error
    
    return (opcode_info, new_opcode)

def generate_opcode_info_group(extension_info: dict[str, Any]) -> tuple[OpcodeInfoGroup, dict[str, InputType], dict[str, DropdownType]]:
    """
    Generate a group of information about the blocks of the given extension and the custom input and dropdown types

    Args:
        extension_info: the raw extension information
    
    Raises:
        MANIP_UnknownExtensionAttributeError: if the extension has an unknown attribute
        MANIP_InvalidCustomMenuError: if the information about a menu is invalid
        MANIP_InvalidCustomBlockError: if information of a block is invalid
        MANIP_NotImplementedError: if an XML block is included in the extension info
        MANIP_ThanksError: if a block argument uses the mysterious Scratch.ArgumentType.SEPERATOR
    # TODO: update tests
    """
    def disambiguate_new_opcode(new_opcode: str, old_opcode: str) -> str:
        """
        Disambiguate a new opcode using it's old opcode.

        Args:
            new_opcode: the new opcode of a block.
            old_opcode: the old opcode of the same block.
        """
        return f"{new_opcode} {{{{id={old_opcode}}}}}" # e.g. "gpusb3::Run function (FUNCNAME) with args (ARGS) {{id=c_runFunc}}"
    # Relevant of the returned attributes: ["id", "blocks", "menus"]
    for attr in extension_info.keys():
        if attr not in KNOWN_EXTENSION_INFO_ATTRS:
            raise MANIP_UnknownExtensionAttributeError(f"Unknown or not (yet) implemented extension attribute: {repr(attr)}")

    
    extension_id = extension_info["id"]
    blocks: list[dict[str, Any] | str] = extension_info.get("blocks", [])
    menus: dict[str, dict[str, Any]|list] = extension_info.get("menus", {})
    input_types, dropdown_types = find_input_and_dropdown_types(menus, blocks, extension_id)
    info_group_content: DualKeyDict[str, str, OpcodeInfo] = DualKeyDict()
    conflicting_new_opcodes: set[str] = set()

    for i, block_info in enumerate(blocks):
        if isinstance(block_info, str):
            continue # ignore eg. "---"
        elif isinstance(block_info, dict):
            opcode_info, new_opcode = generate_block_opcode_info(
                block_info, 
                menus=menus, 
                input_types=input_types,
                dropdown_types=dropdown_types,
                extension_id=extension_id,
            )
        else:
            raise MANIP_InvalidCustomBlockError(f"Invalid block info: Expected type str or dict (block {i}): {block_info}")
        
        if opcode_info is not None:
            old_opcode: str = block_info["opcode"] # "opcode" is guaranteed to exis
            is_final_opcode: bool = block_info.get("ppm_final_opcode", False) # Custom property
            if not is_final_opcode:
                old_opcode: str = f"{extension_id}_{old_opcode}" # "opcode" is guaranteed to exist
            try:
                info_group_content.set(
                    key1  = old_opcode,
                    key2  = new_opcode,
                    value = opcode_info,
                )
            except MANIP_ValueError as error:
                old_exists = info_group_content.has_key1(old_opcode)
                new_exists = info_group_content.has_key2(new_opcode)
                if   old_exists: # => old opcode key conflict
                    raise MANIP_InvalidCustomBlockError(f"Invalid block info: Two blocks must not use the same 'opcode': {old_opcode}") from error
                elif new_exists and not(old_exists): # => new opcode key conflict
                    # write down that the first element with this new opcode has to be renamed too, just can not be done here
                    conflicting_new_opcodes.add(new_opcode)
                    # use old_opcode as a unique disambiguer
                    new_new_opcode = disambiguate_new_opcode(new_opcode, old_opcode)
                    info_group_content.set(
                        key1  = old_opcode,
                        key2  = new_new_opcode,
                        value = opcode_info,
                    )
                # else can not be reached; one of the keys must exist

    # Rename the first entries of conflicts too, second and above entries are handled above
    for new_opcode in conflicting_new_opcodes:
        old_opcode = info_group_content.get_key1_for_key2(new_opcode)
        new_new_opcode = disambiguate_new_opcode(new_opcode, old_opcode)
        info_group_content.change_key2_by_key1(key1=old_opcode, new_key2=new_new_opcode)

    info_group = OpcodeInfoGroup(
        name=extension_id,
        opcode_info=info_group_content,
    )
    
    for menu_opcode in menus.keys():
        old_menu_opcode = f"{extension_id}_menu_{menu_opcode}"
        new_menu_opcode = f"&{extension_id}::#menu:{menu_opcode}"
        opcode_info = OpcodeInfo(opcode_type=OpcodeType.MENU)
        info_group.add_opcode(old_menu_opcode, new_menu_opcode, opcode_info)
    return (info_group, input_types, dropdown_types)

def generate_file_code(
        info_group: OpcodeInfoGroup, 
        input_types: dict[str, InputType], 
        dropdown_types: dict[str, DropdownType],
    ) -> str:
    """
    Generate the code of a python file, which stores information about the blocks of the given extension and is required for the core module

    Args:
        info_group: the group of information about the blocks of the given extension
        input_types: the custom input types
        dropdown_types: the custom dropdown types
    """
    def generate_enum_code(cls_name: str, super_cls_name: str, enum_pairs: dict[str, GEnum]) -> str:
        """
        Generate the python code which can recreate the given Enum class from pairs and name
        
        Args:
            cls_name: the name of the Enum class
            super_cls_name: the name of the superclass of the Enum class
            enum_pairs: the pairs of an Enum class
        """
        cls_code = f"class {cls_name}({super_cls_name}):"
        if len(enum_pairs) == 0:
            return cls_code + f"\n{INDENT}pass"
        for name, enum_item in enum_pairs.items():
            enum_item: GEnum
            cls_code += f"\n{INDENT}{name} = {grepr(enum_item.value, level_offset=1, vanilla_strings=True)}"
        return cls_code
    
    file_code = "\n\n".join((
        f"from {DATA_IMPORTS_IMPORT_PATH} import *",
        generate_enum_code("ExtensionDropdownType", "DropdownType", dropdown_types),
        generate_enum_code("ExtensionInputType", "InputType", input_types),
        f"extension = {grepr(info_group, safe_dkd=True)}",
    ))
    return file_code


__all__ = ["generate_opcode_info_group", "generate_file_code"]

