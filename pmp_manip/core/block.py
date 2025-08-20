from abc         import ABC, abstractmethod
from copy        import deepcopy
from dataclasses import field
from json        import loads, dumps
from typing      import Any, TYPE_CHECKING

from pmp_manip.important_consts import (
    OPCODE_NUM_VAR_VALUE, OPCODE_VAR_VALUE, OPCODE_NUM_LIST_VALUE, OPCODE_LIST_VALUE,
    ANY_TEXT_INPUT_NUM, NEW_OPCODE_CHECKBOX,
    ANY_OPCODE_NUM_IMMEDIATE_BLOCK, ANY_OPCODE_IMMEDIATE_BLOCK, ANY_NEW_OPCODE_IMMEDIATE_BLOCK,
    SHA256_SEC_BROADCAST_MSG, SHA256_SEC_DROPDOWN_VALUE,
)
from pmp_manip.opcode_info.api  import (
    OpcodeInfoAPI, OpcodeInfo, 
    InputInfo, InputType, InputMode, BuiltinDropdownType, DropdownValueKind,
    OpcodeType, SpecialCaseType,
    DROPDOWN_VALUE_T,
)
from pmp_manip.utility          import (
    grepr_dataclass, get_closest_matches, tuplify, listify, string_to_sha256,
    AA_TYPE, AA_NONE, AA_NONE_OR_TYPE, AA_COORD_PAIR, AA_LIST_OF_TYPE, AA_DICT_OF_TYPE, AA_MIN_LEN,
    MANIP_ConversionError,
    MANIP_UnnecessaryInputError, MANIP_MissingInputError, MANIP_UnnecessaryDropdownError, MANIP_MissingDropdownError, 
    MANIP_InvalidOpcodeError, MANIP_InvalidBlockShapeError,
)

if TYPE_CHECKING: from pmp_manip.core.block_interface import (
    FirstToInterIF, InterToFirstIF, SecondToInterIF, ValidationIF,
)
from pmp_manip.core.block_mutation import FRMutation, SRMutation
from pmp_manip.core.comment        import SRComment
from pmp_manip.core.context        import CompleteContext
from pmp_manip.core.dropdown       import SRDropdownValue


@grepr_dataclass(grepr_fields=["opcode", "next", "parent", "inputs", "fields", "shadow", "top_level", "x", "y", "comment", "mutation"])
class FRBlock:
    """
    The first representation for a block. It is very close to the json data in a project
    """

    opcode: str
    next: str | None
    parent: str | None
    inputs: dict[str, (
       tuple[int, str | tuple] 
     | tuple[int, str | tuple, str | tuple]
    )]
    fields: dict[str, tuple[DROPDOWN_VALUE_T, str] | tuple[DROPDOWN_VALUE_T, str, str]]
    shadow: bool
    top_level: bool
    x: int | float | None = None
    y: int | float | None = None
    comment: str | None = None # a comment id
    mutation: "FRMutation | None" = None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRBlock":
        """
        Deserializes json data into a FRBlock
        
        Args:
            data: the json data
        
        Returns:
            the FRBlock
        """
        if "mutation" in data:
            mutation = FRMutation.from_data(data["mutation"])
        else:
            mutation = None
        return cls(
            opcode    = data["opcode"  ],
            next      = data["next"    ],
            parent    = data["parent"  ],
            inputs    = deepcopy(tuplify(data["inputs"])),
            fields    = deepcopy(tuplify(data["fields"])),
            shadow    = data["shadow"  ],
            top_level = data["topLevel"],
            x         = data.get("x", None),
            y         = data.get("y", None),
            comment   = data.get("comment", None),
            mutation  = mutation,
        )
        
    @classmethod
    def from_tuple(cls, 
        data: tuple[int, str, str] | tuple[int, str, str, int|float, int|float],
        parent_id: str | None,
    ) -> "FRBlock":
        """
        Deserializes a tuple into a FRBlock with a variable or list value opcode
        
        Args:
            data: the json data
        
        Returns:
            the FRBlock
        """
        if   len(data) == 3:
            if parent_id is None:
                raise MANIP_ConversionError(f"Invalid parent_id for FRBlock conversion of {data!r}: {parent_id}")
            x = None
            y = None
        elif len(data) == 5: 
            if parent_id is not None:
                raise MANIP_ConversionError(f"Invalid parent_id for FRBlock conversion of {data!r}: {parent_id}")
            x = data[3]
            y = data[4]
        else: raise MANIP_ConversionError(f"Invalid data for FRBlock conversion: {data!r}")
        
        if data[0] == OPCODE_NUM_VAR_VALUE:
            return cls(
                opcode    = OPCODE_VAR_VALUE,
                next      = None,
                parent    = parent_id,
                inputs    = {},
                fields    = {"VARIABLE": (data[1], data[2], "")},
                shadow    = False,
                top_level = x is not None,
                x         = x,
                y         = y,
                comment   = None,
                mutation  = None,
            )
        elif data[0] == OPCODE_NUM_LIST_VALUE:
           return FRBlock(
                opcode    = OPCODE_LIST_VALUE,
                next      = None,
                parent    = parent_id,
                inputs    = {},
                fields    = {"LIST": (data[1], data[2], "list")},
                shadow    = False,
                top_level = x is not None,
                x         = x,
                y         = y,
                comment   = None,
                mutation  = None,
            )
        else: raise MANIP_ConversionError(f"Invalid constant(first element) for FRBlock conversion: {data[0]}")

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRBlock into json data
        
        Returns:
            the json data
        """
        data = {
            "opcode"  : self.opcode,
            "next"    : self.next,
            "parent"  : self.parent,
            "inputs"  : deepcopy(listify(self.inputs)),
            "fields"  : deepcopy(listify(self.fields)),
            "shadow"  : self.shadow,
            "topLevel": self.top_level,
        }
        if self.x is not None:
            data["x"] = self.x
            data["y"] = self.y
        if self.comment is not None:
            data["comment"] = self.comment
        if self.mutation is not None:
            data["mutation"] = self.mutation.to_data()
        return data
   
    def to_tuple(self) -> tuple[int, str, str] | tuple[int, str, str, int|float, int|float]:
        """
        Serializes a FRBlock with a variable or list value opcode into a tuple
        
        Returns:
            the json data
        """
        if self.opcode not in ANY_OPCODE_IMMEDIATE_BLOCK:
            raise MANIP_ConversionError(f"To convert a FRBlock into a tuple it must have one of these opcodes: {ANY_OPCODE_IMMEDIATE_BLOCK}")
        
        if   self.opcode == OPCODE_VAR_VALUE:
            magic_number = OPCODE_NUM_VAR_VALUE
            name         = self.fields["VARIABLE"][0]
            sha256       = self.fields["VARIABLE"][1]
        elif self.opcode == OPCODE_LIST_VALUE:
            magic_number = OPCODE_NUM_LIST_VALUE
            name         = self.fields["LIST"][0]
            sha256       = self.fields["LIST"][1]
        
        if self.top_level:
            return (magic_number, name, sha256, self.x, self.y)
        else:
            return (magic_number, name, sha256)

    def to_inter(self, 
        fti_if: "FirstToInterIF", 
        info_api: OpcodeInfoAPI, 
        own_id: str
    ) -> "IRBlock":
        """
        Converts a FRBlock into a IRBlock
        
        Args:
            fti_if: interface which allows the management of other blocks
            info_api: the opcode info api used to fetch information about opcodes
            own_id: the reference id of this FRBlock
        
        Returns:
            the IRBlock
        """
        opcode_info = info_api.get_info_by_old(self.opcode)
        pre_handler = opcode_info.get_special_case(SpecialCaseType.PRE_FIRST_TO_INTER)
        if pre_handler is not None:
            self = pre_handler.call(block=self, block_id=own_id, fti_if=fti_if)
        
        instead_handler = opcode_info.get_special_case(SpecialCaseType.INSTEAD_FIRST_TO_INTER)
        if instead_handler is None:
            new_inputs = self._to_inter_inputs(
                fti_if      = fti_if,
                info_api    = info_api,
                opcode_info = opcode_info,
                own_id      = own_id,
            )
            new_dropdowns = {}
            for dropdown_id, dropdown_value in self.fields.items():
                new_dropdowns[dropdown_id] = dropdown_value[0]
            
            new_block = IRBlock(
                opcode       = self.opcode,
                inputs       = new_inputs,
                dropdowns    = new_dropdowns,
                position     = (self.x, self.y) if self.top_level else None,
                comment      = None if self.comment  is None else fti_if.get_comment(self.comment),
                # the result of get_comment is a comment which is not used by any block => fine
                mutation     = None if self.mutation is None else self.mutation.to_second(fti_if),
                next         = self.next,
                is_top_level = self.top_level,
            )
        else:
            new_block = instead_handler.call(block=self, block_id=own_id, fti_if=fti_if)
        return new_block

    def _to_inter_inputs(self, 
        fti_if: "FirstToInterIF", 
        info_api: OpcodeInfoAPI,
        opcode_info: OpcodeInfo,
        own_id: str
    ) -> dict[str, "IRInputValue"]:
        """
        *[Helper Method]* Converts the inputs of a FRBlock into the IR Fromat
        
        Args:
            fti_if: interface which allows the management of other blocks
            info_api: the opcode info api used to fetch information about opcodes
            opcode_info: the Information about the block's opcode
        
        Returns:
            the inputs in IR Format
        """
        input_infos = opcode_info.get_old_input_ids_infos(block=self, fti_if=fti_if)
        
        new_inputs = {}
        for input_id, input_value in self.inputs.items():
            input_mode = input_infos[input_id].type.mode

            references      = []
            immediate_block = None
            text            = None
            for item in input_value[1:]: # ignore first item(some irrelevant number)
                if isinstance(item, str):
                    references.append(item)
                elif isinstance(item, tuple) and item[0] in ANY_TEXT_INPUT_NUM:
                    text = item[1]
                elif isinstance(item, tuple) and item[0] in ANY_OPCODE_NUM_IMMEDIATE_BLOCK:
                    immediate_fr_block = FRBlock.from_tuple(item, parent_id=own_id)
                    immediate_block = immediate_fr_block.to_inter(
                        fti_if = fti_if,
                        info_api  = info_api,
                        own_id    = None, # None is fine, because tuple blocks can not possibly contain more tuple blocks 
                    )
                else: raise MANIP_ConversionError(f"Invalid input value {input_value!r} for input {input_id!r}")

            new_inputs[input_id] = IRInputValue(
                mode            = input_mode,
                references      = references,
                immediate_block = immediate_block,
                text            = text,
            )        
        return new_inputs



@grepr_dataclass(grepr_fields=["opcode", "inputs", "dropdowns", "comment", "mutation", "position", "next", "is_top_level"])
class IRBlock:
    """
    The intermediate representation for a block. It has similarities with SRBlock but uses an id system
    """
    
    opcode: str
    inputs: dict[str, "IRInputValue"]
    dropdowns: dict[str, DROPDOWN_VALUE_T]
    comment: SRComment | None
    mutation: "SRMutation | None"
    position: tuple[int | float, int | float] | None
    next: "str | None"
    is_top_level: bool

    @classmethod
    def from_menu_dropdown_value(cls, dropdown_value: DROPDOWN_VALUE_T, input_info: InputInfo) -> "IRBlock":
        """
        Creates a IRBlock which only contains a menu SRDropdownValue

        Args:
            dropdown_value: the SRDropdownValue to contain in the block
            input_info: information about the input, that the created menu block will be used for

        Returns:
            the IRBlock
        """
        return cls(
            opcode       = input_info.menu.opcode,
            inputs       = {},
            dropdowns    = {
                input_info.menu.inner: dropdown_value,
            },
            comment      = None,
            mutation     = None,
            position     = None,
            next         = None,
            is_top_level = False,
        )

    def get_references(self) -> list[str]:
        """
        Get a list of block ids, this block references

        Returns:
            a list of block ids, this block references
        """
        references = []
        if self.next is not None:
            references.append(self.next)
        for input_value in self.inputs.values():
            references.extend(input_value.references)
        return references

    def to_first(self, 
        itf_if: "InterToFirstIF", 
        info_api: OpcodeInfoAPI,
        parent_id: str|None,
        own_id: str|None,
    ) -> FRBlock | tuple[int, str, str] | tuple[int, str, str, int|float, int|float]:
        """
        Converts a IRBlock into a FRBlock
        
        Args:
            itf_if: interface which allows the management of other blocks and more
            info_api: the opcode info api used to fetch information about opcodes
            parent_id: the reference id of the parent block or None
            own_id: the reference id of this FRBlock or None for immediate blocks
        
        Returns:
            the FRBlock
        """
        opcode_info = info_api.get_info_by_old(self.opcode)

        if self.comment is None:
            comment_id = None
        else:
            frcomment = self.comment.to_first(block_id=own_id)
            comment_id = itf_if.add_comment(frcomment)
        input_infos = opcode_info.get_old_input_ids_infos(block=self, fti_if=None) 
        # fti_if is not needed for a IRBlock

        old_inputs = {}
        for input_id, input_value in self.inputs.items():
            input_type = input_infos[input_id].type
            elements = input_value.references.copy()
            if input_value.immediate_block is not None:
                frblock = input_value.immediate_block.to_first(
                    itf_if      = itf_if,
                    info_api    = info_api,
                    parent_id   = own_id,
                    own_id      = None, # an immediate block can not have any references => no own id needed?
                )
                elements.insert(0, frblock)
            match input_type.mode:
                case InputMode.BLOCK_AND_TEXT:
                    magic_text_number = input_type.magic_number
                    elements.append((magic_text_number, input_value.text))
                case InputMode.BLOCK_AND_BROADCAST_DROPDOWN:
                    magic_text_number = input_type.magic_number
                    elements.append((magic_text_number, input_value.text, 
                        string_to_sha256(input_value.text, secondary=SHA256_SEC_BROADCAST_MSG)
                    ))
            
            if input_type.mode.can_be_missing:
                magic_number = 2
            else:
                match len(elements):
                    case 1: magic_number = 1
                    case 2: magic_number = 3
            old_inputs[input_id] = (magic_number, *elements)

        old_fields = {}
        for dropdown_id, dropdown_value in self.dropdowns.items():
            if opcode_info.opcode_type is OpcodeType.MENU:
                dropdown_type = None # use the default _ option
            else:
                dropdown_type = opcode_info.get_dropdown_info_by_old(dropdown_id).type
            match dropdown_type:
                case BuiltinDropdownType.VARIABLE:
                    suffix    = ""
                    sha256    = itf_if.get_variable_sha256(variable_name=dropdown_value)
                case BuiltinDropdownType.LIST:
                    suffix    = "list"
                    sha256    = itf_if.get_list_sha256(list_name=dropdown_value)
                case BuiltinDropdownType.BROADCAST:
                    suffix    = "broadcast_msg"
                    sha256    = string_to_sha256(dropdown_value, secondary=SHA256_SEC_BROADCAST_MSG)
                case _:
                    suffix    = None
                    sha256    = string_to_sha256(dropdown_value, secondary=SHA256_SEC_DROPDOWN_VALUE)
            if suffix is None:
                old_fields[dropdown_id] = (dropdown_value, sha256)
            else:
                old_fields[dropdown_id] = (dropdown_value, sha256, suffix)                
        
        old_block = FRBlock(
            opcode    = self.opcode,
            next      = self.next,
            parent    = parent_id,
            inputs    = old_inputs,
            fields    = old_fields,
            shadow    = opcode_info.has_shadow,
            top_level = self.is_top_level,
            x         = self.position[0] if self.is_top_level else None,
            y         = self.position[1] if self.is_top_level else None,
            comment   = comment_id,
            mutation  = None if self.mutation is None else self.mutation.to_first(itf_if=itf_if),
        )

        post_handler = opcode_info.get_special_case(SpecialCaseType.POST_INTER_TO_FIRST)
        if post_handler is not None:
            old_block = post_handler.call(block=old_block, block_id=own_id, itf_if=itf_if)
        if self.opcode in ANY_OPCODE_IMMEDIATE_BLOCK:
            return old_block.to_tuple()
        else:
            return old_block
    
    def to_second(self, 
        all_blocks: dict[str, "IRBlock"],
        info_api: OpcodeInfoAPI,
    ) -> tuple[tuple[int|float,int|float] | None, list["SRBlock | str"]]:
        """
        Converts a IRBlock into a SRBlock
        
        Args:
            all_blocks: a dictionary of all blocks
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the SRBlock
        """
        opcode_info = info_api.get_info_by_old(self.opcode)
        if opcode_info.opcode_type == OpcodeType.MENU: # The attribute is fine because DYNAMIC should never generate MENU
            return (None, [list(self.dropdowns.values())[0]])
            """ example:
            IRBlock(
                opcode="#TOUCHING OBJECT MENU",
                dropdowns={"TOUCHINGOBJECTMENU": "_mouse_"},
                ...
            )
            --> "_mouse_" """
        
        old_new_input_ids = opcode_info.get_old_new_input_ids(block=self, fti_if=None)
        input_infos = opcode_info.get_new_input_ids_infos(block=self, fti_if=None) 
        # maps old input ids to new input ids and gets input information # fti_if is not necessary for a IRBlock 
        
        new_inputs = {}
        for input_id, input_value in self.inputs.items():
            sub_scripts: list[list[SRBlock|str]] = []
            if input_value.immediate_block is not None:
                _, sub_blocks = input_value.immediate_block.to_second(
                    all_blocks = all_blocks,
                    info_api   = info_api,
                )
                sub_scripts.append(sub_blocks)
            
            for sub_reference in input_value.references: 
                sub_block = all_blocks[sub_reference]
                _, sub_blocks = sub_block.to_second(
                    all_blocks    = all_blocks,
                    info_api      = info_api,
                )
                sub_scripts.append(sub_blocks)
            
            script_count = len(sub_scripts)
            if script_count == 2:
                sub_script  = sub_scripts[0] # blocks of first script
                sub_block_a = sub_scripts[0][0] # first block of first script
                sub_block_b = sub_scripts[1][0] # first block of second script
            elif script_count == 1:
                sub_script  = sub_scripts[0] # blocks of first script
                sub_block_a = sub_scripts[0][0] # first block of first script
                sub_block_b = None
            elif script_count == 0:
                sub_script  = []
                sub_block_a = None
                sub_block_b = None
            else: raise MANIP_ConversionError(f"Invalid script count: {script_count}")
            
            input_blocks    = []
            input_block     = None
            input_immediate = None
            input_dropdown  = None
            
            match input_value.mode:
                case InputMode.BLOCK_AND_TEXT:
                    assert script_count in {0, 1}
                    input_block     = sub_block_a
                    input_immediate = input_value.text
                case InputMode.BLOCK_AND_BROADCAST_DROPDOWN:
                    assert script_count in {0, 1}
                    input_block     = sub_block_a
                    input_dropdown  = input_value.text
                case InputMode.BLOCK_AND_BOOL:
                    assert script_count in {0, 1, 2} # this:
                    # should be compatible with older projects too, which do not have CHECKBOX block yet
                    checkbox_block = None
                    if   script_count == 0:
                        pass
                    elif script_count == 1:
                        if sub_block_a.opcode == NEW_OPCODE_CHECKBOX:
                            checkbox_block = sub_block_a
                        else:
                            input_block    = sub_block_a
                    elif script_count == 2:
                        assert sub_block_a.opcode != NEW_OPCODE_CHECKBOX
                        assert sub_block_b.opcode == NEW_OPCODE_CHECKBOX
                        input_block    = sub_block_a
                        checkbox_block = sub_block_b
                    if checkbox_block is None:
                        input_immediate = False 
                        # use False instead of None -> a checkbox block will be added when converted to FR again
                    else:
                        checkbox_value = checkbox_block.dropdowns["CHECKBOX"].value
                        input_immediate = loads(checkbox_value.lower()) # "FALSE" -> False, "TRUE" -> True
                case InputMode.BLOCK_ONLY:
                    assert script_count in {0, 1}
                    input_block = sub_block_a
                case InputMode.SCRIPT:
                    assert script_count in {0, 1}
                    input_blocks = sub_script
                case InputMode.BLOCK_AND_DROPDOWN | InputMode.BLOCK_AND_MENU_TEXT:
                    assert script_count in {1, 2}
                    if   script_count == 1:
                        input_block    = None
                        input_dropdown = sub_block_a
                    elif script_count == 2:
                        input_block    = sub_block_a
                        input_dropdown = sub_block_b

            new_input_id = old_new_input_ids[input_id]
            if input_dropdown is not None:
                input_type = input_infos[new_input_id].type
                dropdown_type = input_type.corresponding_dropdown_type
                input_dropdown = SRDropdownValue.from_tuple(
                    dropdown_type.translate_old_to_new_value(input_dropdown)
                )

            new_inputs[new_input_id] = SRInputValue.from_mode(
                mode      = input_value.mode,
                blocks    = input_blocks,
                block     = input_block,
                immediate = input_immediate,
                dropdown  = input_dropdown,
            )
        
        # Check for missing inputs and give a default value where possible otherwise raise
        for new_input_id in input_infos.keys():
            if new_input_id not in new_inputs:
                input_mode = input_infos[new_input_id].type.mode
                if input_mode.can_be_missing:
                    new_inputs[new_input_id] = SRInputValue.from_mode(mode=input_mode, immediate=False)
                    # immediate must be False, SRBlockAndBoolInputValue might otherwise get None
                else:
                    raise MANIP_ConversionError(f"For a block with opcode {self.opcode!r}, input {new_input_id!r} is missing")
        
        new_dropdowns = {}
        for dropdown_id, dropdown_value in self.dropdowns.items():
            dropdown_type = opcode_info.get_dropdown_info_by_old(dropdown_id).type
            new_dropdown_id = opcode_info.get_new_dropdown_id(dropdown_id)
            new_dropdowns[new_dropdown_id] = SRDropdownValue.from_tuple(dropdown_type.translate_old_to_new_value(dropdown_value))

        new_block = SRBlock(
            opcode    = info_api.get_new_by_old(self.opcode),
            inputs    = new_inputs,
            dropdowns = new_dropdowns,
            comment   = deepcopy(self.comment),
            mutation  = deepcopy(self.mutation),
        )
        new_blocks = [new_block]
        if self.next is not None:
            next_block = all_blocks[self.next]
            _, next_blocks = next_block.to_second(
                all_blocks    = all_blocks,
                info_api      = info_api,
            )
            new_blocks.extend(next_blocks)
        
        return (self.position, new_blocks) 
 
@grepr_dataclass(grepr_fields=["mode", "references", "immediate_block", "text"])
class IRInputValue:
    """
    The intermediate representation for the value of a block's input
    """
    
    mode: InputMode
    references: list["str"]
    immediate_block: IRBlock | None
    text: str | None



@grepr_dataclass(grepr_fields=["position", "blocks"])
class SRScript:
    """
    The second representation for a script. 
    It uses a nested block structure and is much more user friendly then the first representation
    """

    position: tuple[int | float, int | float]
    blocks: list["SRBlock"]

    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF",
        context: CompleteContext,
    ) -> None:
        """
        Ensure a SRScript is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate the values of dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRScript is invalid
        """
        AA_COORD_PAIR(self, path, "position")
        AA_LIST_OF_TYPE(self, path, "blocks", SRBlock)
        AA_MIN_LEN(self, path, "blocks", min_len=1)
        
        for i, block in enumerate(self.blocks):
            current_path = path+["blocks", i]
            block.validate(
                path             = current_path,
                info_api         = info_api,
                validation_if    = validation_if,
                context          = context,
                expects_reporter = False,
            )
            opcode_info = info_api.get_info_by_new(block.opcode)
            opcode_type = opcode_info.get_opcode_type(block=block, validation_if=validation_if)
            SRBlock.validate_opcode_type(
                opcode_type  = opcode_type,
                path         = current_path,
                is_top_level = True,
                is_first     = (i == 0),
                is_last      = ((i+1) == len(self.blocks)),
            )
    
    def to_inter(self, 
        sti_if: "SecondToInterIF",
        info_api: OpcodeInfoAPI, 
    ) -> str:
        """
        Converts a SRScript into intermediate representation. 
        Adds the blocks in intermediate representation to the interface.
        Returns the reference id of the top level block
        
        Args:
            sti_if: interface used to manage blocks
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the reference id of the top level block
        """
        block_ids = [sti_if.get_next_block_id() for i in range(len(self.blocks))]
        for i, block in enumerate(self.blocks):
            next_id = block_ids[i+1] if i+1 < len(self.blocks) else None
            irblock = block.to_inter(
                sti_if       = sti_if,
                info_api     = info_api,
                next         = next_id,
                position     = self.position if i==0 else None,
                is_top_level = i == 0,
            )
            sti_if.schedule_block_addition(block_ids[i], irblock)
        return block_ids[0]

@grepr_dataclass(grepr_fields=["opcode", "inputs", "dropdowns", "comment", "mutation"])
class SRBlock:
    """
    The second representation for a block. 
    It uses a nested block structure and is much more user friendly then the first representation
    """
    
    opcode: str
    inputs: dict[str, "SRInputValue"] = field(default_factory=dict)
    dropdowns: dict[str, SRDropdownValue] = field(default_factory=dict)
    comment: SRComment | None = None
    mutation: SRMutation | None = None
    
    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF", 
        context: CompleteContext,
        expects_reporter: bool,
    ) -> None:
        """
        Ensure a SRBlock is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate dropdowns
            expects_reporter: Wether this block should be a reporter
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRBlock is invalid
            MANIP_InvalidOpcodeError(MANIP_ValidationError): if the opcode is not a defined opcode
            MANIP_UnnecessaryInputError(MANIP_ValidationError): if a key of inputs is not expected for the specific opcode
            MANIP_MissingInputError(MANIP_ValidationError): if an expected key of inputs for the specific opcode is missing
            MANIP_UnnecessaryDropdownError(MANIP_ValidationError): if a key of dropdowns is not expected for the specific opcode
            MANIP_MissingDropdownError(MANIP_ValidationError): if an expected key of dropdowns for the specific opcode is missing
            MANIP_InvalidBlockShapeError(MANIP_ValidationError): if a reporter block was expected but a non-reporter block was found
        """
        AA_TYPE(self, path, "opcode", str)
        AA_DICT_OF_TYPE(self, path, "inputs"   , key_t=str, value_t=SRInputValue   )
        AA_DICT_OF_TYPE(self, path, "dropdowns", key_t=str, value_t=SRDropdownValue)
        AA_NONE_OR_TYPE(self, path, "comment", SRComment)
        AA_NONE_OR_TYPE(self, path, "mutation", SRMutation)
        
        cls_name = self.__class__.__name__
        opcode_info = info_api.get_info_by_new_safe(self.opcode)
        if opcode_info is None:
            closest_matches = get_closest_matches(self.opcode, info_api.all_new, n=10)
            msg = (
                f"opcode of {cls_name} must be a defined opcode not {self.opcode!r}. "
                f"The closest matches are: \n  - "+"\n  - ".join([repr(m) for m in closest_matches])
            )
            raise MANIP_InvalidOpcodeError(path, msg)
        
        if self.comment is not None:
            self.comment.validate(path+["comment"])
        
        if opcode_info.new_mutation_cls is None:
            AA_NONE(self, path, "mutation", condition="For this opcode")
        else:
            AA_TYPE(self, path, "mutation", opcode_info.new_mutation_cls, condition="For this opcode")
            self.mutation.validate(path+["mutation"])

        input_infos = opcode_info.get_new_input_ids_infos(block=self, fti_if=None) 
        # maps input ids to their types # fti_if is not necessary for a IRBlock
        
        for new_input_id, input in self.inputs.items():
            if new_input_id not in input_infos.keys():
                raise MANIP_UnnecessaryInputError(path, 
                    f"inputs of {cls_name!r} with opcode {self.opcode!r} includes unnecessary input {new_input_id!r}",
                )
            input.validate(
                path          = path+["inputs", (new_input_id,)],
                info_api      = info_api,
                validation_if = validation_if,
                context       = context,
                input_type    = input_infos[new_input_id].type,
            )
        for new_input_id in input_infos.keys():
            if new_input_id not in self.inputs:
                raise MANIP_MissingInputError(path, 
                    f"inputs of {cls_name!r} with opcode {self.opcode!r} is missing input {new_input_id!r}",
                )
        
        new_dropdown_ids = opcode_info.get_all_new_dropdown_ids()
        for new_dropdown_id, dropdown in self.dropdowns.items():
            if new_dropdown_id not in new_dropdown_ids:
                raise MANIP_UnnecessaryDropdownError(path, 
                    f"dropdowns of {cls_name!r} with opcode {self.opcode!r} includes unnecessary dropdown {new_dropdown_id!r}",
                )
            current_path = path+["dropdowns", (new_dropdown_id,)]
            dropdown.validate(current_path)
            dropdown.validate_value(
                path          = current_path,
                dropdown_type = opcode_info.get_dropdown_info_by_new(new_dropdown_id).type,
                context       = context,
            )
        for new_dropdown_id in new_dropdown_ids:
            if new_dropdown_id not in self.dropdowns:
                raise MANIP_MissingDropdownError(path, 
                    f"dropdowns of {cls_name!r} with opcode {self.opcode!r} is missing dropdown {new_dropdown_id!r}",
                )
        
        opcode_type = opcode_info.get_opcode_type(block=self, validation_if=validation_if)
        if expects_reporter and not(opcode_type.is_reporter):
            raise MANIP_InvalidBlockShapeError(path, "Expected a reporter block here")

        post_case = opcode_info.get_special_case(SpecialCaseType.POST_VALIDATION)
        if post_case is not None:
            post_case.call(path=path, block=self)

    @staticmethod
    def validate_opcode_type(
        path: list,
        opcode_type: OpcodeType,
        is_top_level: bool,
        is_first: bool,
        is_last: bool,
    ) -> None:
        """
        Ensure a block shape is allowed at a specific location.  
        
        Args:
            path: the path from the project to itself. Used for better error messages
            opcode_type: the opcode type of this block
            is_top_level: Wether this block is in a script(True) or in a substack(False)
            is_fist: Wether this block is the first in it's script/substack
            is_last: Wether this block is the last in it's script/substack
        
        Returns:
            None
        
        Raises:
            MANIP_InvalidBlockShapeError(MANIP_ValidationError): if the opcode_type of the block's opcode is invalid in a specific situation
        """
        if   opcode_type == OpcodeType.STATEMENT: pass
        elif opcode_type == OpcodeType.ENDING_STATEMENT:
            if not is_last: # when there is a next block
                raise MANIP_InvalidBlockShapeError(path, "A block of type ENDING_STATEMENT must be the last block in it's script or substack")
        elif opcode_type == OpcodeType.HAT:
            if not is_top_level:
                raise MANIP_InvalidBlockShapeError(path, "A block of type HAT is not allowed within a substack")
            elif not is_first:
                raise MANIP_InvalidBlockShapeError(path, "A block of type HAT must to be the first block in it's script or substack")
        elif opcode_type.is_reporter:
            if not is_top_level:
                raise MANIP_InvalidBlockShapeError(path, "A block of any ...REPORTER type is not allowed within a substack")
            elif not(is_first and is_last):
                raise MANIP_InvalidBlockShapeError(path, "If contained in a substack, a block of any ...REPORTER type must be the only block in that substack")
    
    def find_broadcast_messages(self) -> list[str]:
        """
        Finds the used broadcast messages in this block
               
        Returns:
            the used broadcast messages
        """
        broadcast_messages = []
        for input_value in self.inputs.values():
            if isinstance(input_value, SRBlockAndDropdownInputValue) :
                if input_value.dropdown is not None:
                    if input_value.dropdown.kind is DropdownValueKind.BROADCAST_MSG:
                        broadcast_messages.append(input_value.dropdown.value)
            
            if   isinstance(input_value, 
                (SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, 
                 SRBlockAndBoolInputValue, SRBlockOnlyInputValue)
            ):
                sub_blocks = [] if input_value.block is None else [input_value.block]
            elif isinstance(input_value, SRScriptInputValue):
                sub_blocks = input_value.blocks
            
            for sub_block in sub_blocks:
                broadcast_messages.extend(sub_block.find_broadcast_messages())
        for dropdown_value in self.dropdowns.values():
            if dropdown_value is not None:
                if dropdown_value.kind is DropdownValueKind.BROADCAST_MSG:
                    broadcast_messages.append(dropdown_value.value)
        return broadcast_messages

    def to_inter(self, 
        sti_if: "SecondToInterIF",
        info_api: OpcodeInfoAPI, 
        next: str | None, 
        position: tuple[int | float, int | float] | None,
        is_top_level: bool, 
    ) -> IRBlock:
        """
        Converts a SRBlock into a IRBlock
        
        Args:
            sti_if: interface used to manage blocks
            info_api: the opcode info api used to fetch information about opcodes
            next: the id of the next block in the same script or substack
            position: the position of the block if is_top_level is True
            is_top_level: wether the block is the first block in a script
        
        Returns:
            the IRBlock
        """
        opcode_info = info_api.get_info_by_new(self.opcode)
        
        # Map new input Ids to old input Ids
        new_old_input_ids = opcode_info.get_new_old_input_ids  (block=self, fti_if=None) 
        input_infos       = opcode_info.get_new_input_ids_infos(block=self, fti_if=None)
        # fti_if is not needed for a SRBlock
        old_inputs = {}
        for input_id, input_value in self.inputs.items():
            input_info   = input_infos[input_id]
            input_mode   = input_info.type.mode
            old_input_id = new_old_input_ids[input_id]
            
            input_sub_scripts: list[list[SRBlock | IRBlock]] = []
            input_immediate = None
            input_dropdown  = None

            if isinstance(getattr(input_value, "block", None), SRBlock):
                input_sub_scripts.append([input_value.block])
            match input_mode:
                case InputMode.BLOCK_AND_TEXT:
                    input_immediate = input_value.immediate
                case InputMode.BLOCK_AND_BROADCAST_DROPDOWN:
                    input_immediate = input_value.dropdown.value
                case InputMode.BLOCK_AND_BOOL:
                    checkbox_value = dumps(input_value.immediate).upper()
                    checkbox_block = SRBlock(
                        opcode=NEW_OPCODE_CHECKBOX,
                        inputs={},
                        dropdowns={
                            "CHECKBOX": SRDropdownValue(kind=DropdownValueKind.STANDARD, value=checkbox_value),
                        },
                    )
                    input_sub_scripts.append([checkbox_block]) # important: must come after "block"
                case InputMode.BLOCK_ONLY:
                    pass
                case InputMode.SCRIPT:
                    if input_value.blocks:
                        input_sub_scripts.append(input_value.blocks)
                case InputMode.BLOCK_AND_DROPDOWN | InputMode.BLOCK_AND_MENU_TEXT:
                    input_dropdown = input_value.dropdown

            if input_dropdown is not None:
                dropdown_type = input_info.type.corresponding_dropdown_type
                input_dropdown = dropdown_type.translate_new_to_old_value(input_dropdown.to_tuple())
                input_sub_scripts.append([IRBlock.from_menu_dropdown_value(input_dropdown, input_info)])

            references      = []
            immediate_block = None

            for sub_blocks in input_sub_scripts:
                first_block = sub_blocks[0]
                if   isinstance(first_block, IRBlock) and (len(sub_blocks) == 1):
                    block_id = sti_if.get_next_block_id()
                    sti_if.schedule_block_addition(block_id, first_block)
                    references.append(block_id)
                elif isinstance(first_block, SRBlock) and (len(sub_blocks) == 1) and (first_block.opcode in ANY_NEW_OPCODE_IMMEDIATE_BLOCK):
                    immediate_block  = first_block.to_inter(
                        sti_if       = sti_if,
                        info_api     = info_api,
                        next         = None,
                        position     = None,
                        is_top_level = False,
                    )
                elif isinstance(first_block, SRBlock):
                    sub_blocks: list[SRBlock]
                    block_ids = [sti_if.get_next_block_id() for i in range(len(sub_blocks))]
                    for i, sub_block in enumerate(sub_blocks):
                        next_id = block_ids[i+1] if i+1 < len(sub_blocks) else None
                        irblock = sub_block.to_inter(
                            sti_if       = sti_if,
                            info_api     = info_api,
                            next         = next_id,
                            position     = None,
                            is_top_level = False,
                        )
                        sti_if.schedule_block_addition(block_ids[i], irblock)
                    references.append(block_ids[0])
                else: raise MANIP_ConversionError(f"Invalid input sub script: {sub_blocks}")

            old_input_value = IRInputValue(
                mode            = input_mode,
                references      = references,
                immediate_block = immediate_block,
                text            = input_immediate,
            )
            if (
                not(input_mode.can_be_missing) or old_input_value.references
                or (old_input_value.immediate_block is not None) or (old_input_value.text is not None)
            ):
                old_inputs[old_input_id] = old_input_value

        # Map new dropdown IDs to old dropdown IDs and values
        old_dropdowns = {}
        for dropdown_id, dropdown_value in self.dropdowns.items():
            dropdown_info = opcode_info.get_dropdown_info_by_new(dropdown_id)
            old_dropdown_id = opcode_info.get_old_dropdown_id(dropdown_id)
            old_dropdowns[old_dropdown_id] = dropdown_info.type.translate_new_to_old_value(dropdown_value.to_tuple())

        return IRBlock(
            opcode       = info_api.get_old_by_new(self.opcode),
            inputs       = old_inputs,
            dropdowns    = old_dropdowns,
            comment      = deepcopy(self.comment),
            mutation     = deepcopy(self.mutation),
            position     = position,
            next         = next,
            is_top_level = is_top_level,
        )

@grepr_dataclass(grepr_fields=[], eq=False, order=False, init=False, forbid_init_only_subcls=True) # eq must be True for order to work, is overwritten
class SRInputValue(ABC):
    """
    The second representation for a block input. 
    It can contain a substack of blocks, a block, an immediate text or boolean field and a dropdown
    **Please use the subclasses instead**
    **Be careful when accessing fields**, because only the subclasses guarantee there existance
    """
    
    # these are not guaranteed to exist and are only listed for good typing
    blocks: list[SRBlock]     | None = field(init=False, repr=False, hash=False, compare=False) 
    block: SRBlock            | None = field(init=False, repr=False, hash=False, compare=False)
    immediate: str | bool     | None = field(init=False, repr=False, hash=False, compare=False)
    dropdown: SRDropdownValue | None = field(init=False, repr=False, hash=False, compare=False)

    @classmethod
    def from_mode(cls,
        mode: InputMode,
        blocks: list[SRBlock]     | None = None,
        block: SRBlock            | None = None,
        immediate: str | bool     | None = None,
        dropdown: SRDropdownValue | None = None,
    ) -> "SRInputValue":
        """
        Creates a SRInputValue, given its mode and data
        
        Args:
            mode: the input mode
            blocks: the substack blocks
            block: the block of the input
            immediate: the text or boolean field of the input
            dropdown: the dropdown of the input
        
        Returns:
            the input value
        """
        match mode:
            case InputMode.BLOCK_AND_TEXT:
                return SRBlockAndTextInputValue(block=block, immediate=immediate)
            case InputMode.BLOCK_AND_DROPDOWN | InputMode.BLOCK_AND_BROADCAST_DROPDOWN | InputMode.BLOCK_AND_MENU_TEXT:
                return SRBlockAndDropdownInputValue(block=block, dropdown=dropdown)
            case InputMode.BLOCK_AND_BOOL:
                return SRBlockAndBoolInputValue(block=block, immediate=immediate)
            case InputMode.BLOCK_ONLY:
                return SRBlockOnlyInputValue(block=block)
            case InputMode.SCRIPT:
                return SRScriptInputValue(blocks=[] if blocks is None else blocks)            

    @abstractmethod
    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF", 
        context: CompleteContext, 
        input_type: InputType, 
    ) -> None:
        """
        Ensures this input is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate dropdowns
            input_type: the type of this input. Used to valdiate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRInputValue is invalid
        """

    def _validate_block(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF", 
        context: CompleteContext, 
    ) -> None:
        """
        *[Helper Method]* Ensures the block of this input is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the block of the SRInputValue is invalid
        """
        block: SRBlock = self.block
        AA_NONE_OR_TYPE(self, path, "block", SRBlock)
        if block is not None:
            block.validate(
                path             = path+["block"],
                info_api         = info_api,
                validation_if    = validation_if,
                context          = context,
                expects_reporter = True,
            )

@grepr_dataclass(grepr_fields=["block", "immediate"])
class SRBlockAndTextInputValue(SRInputValue):
    """
    The second representation for a block input, which has an immediate text field and might contain a block
    """

    block: SRBlock | None
    immediate: str

    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF", 
        context: CompleteContext, 
        input_type: InputType, 
    ) -> None:
        """
        Ensures this input is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate dropdowns
            input_type: the type of this input. Used to valdiate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRBlockAndTextInputValue is invalid
        """
        self._validate_block(
            path          = path,
            info_api      = info_api,
            validation_if = validation_if,
            context       = context,
        )
        AA_TYPE(self, path, "immediate", str)

@grepr_dataclass(grepr_fields=["block", "dropdown"])
class SRBlockAndDropdownInputValue(SRInputValue):
    """
    The second representation for a block input, which has a dropdown and might contain a block
    """
    
    block: SRBlock | None
    dropdown: SRDropdownValue

    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF", 
        context: CompleteContext, 
        input_type: InputType, 
    ) -> None:
        """
        Ensures this input is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate dropdowns
            input_type: the type of this input. Used to valdiate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRBlockAndDropdownInputValue is invalid
        """
        self._validate_block(
            path          = path,
            info_api      = info_api,
            validation_if = validation_if,
            context       = context,
        )
        AA_TYPE(self, path, "dropdown", SRDropdownValue)
        
        current_path = path+["dropdown"]
        self.dropdown.validate(current_path)
        self.dropdown.validate_value(
            path          = current_path,
            dropdown_type = input_type.corresponding_dropdown_type,
            context       = context,
        )

@grepr_dataclass(grepr_fields=["block", "immediate"])
class SRBlockAndBoolInputValue(SRInputValue):
    """
    The second representation for a block input, which has an immediate boolean field and might contain a block
    """

    block: SRBlock | None
    immediate: bool # Can not be None, default is False (see IRBlock.to_second, case InputMode.BLOCK_AND_BOOL)

    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF", 
        context: CompleteContext, 
        input_type: InputType, 
    ) -> None:
        """
        Ensures this input is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate dropdowns
            input_type: the type of this input. Used to valdiate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRBlockAndBoolInputValue is invalid
        """
        self._validate_block(
            path          = path,
            info_api      = info_api,
            validation_if = validation_if,
            context       = context,
        )
        AA_TYPE(self, path, "immediate", bool)

@grepr_dataclass(grepr_fields=["block"])
class SRBlockOnlyInputValue(SRInputValue):
    """
    The second representation for a block input, which might contain a block
    """
    
    block: SRBlock | None

    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF", 
        context: CompleteContext, 
        input_type: InputType, 
    ) -> None:
        """
        Ensures this input is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate dropdowns
            input_type: the type of this input. Used to valdiate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRBlockOnlyInputValue is invalid
        """
        self._validate_block(
            path          = path,
            info_api      = info_api,
            validation_if = validation_if,
            context       = context,
        )

@grepr_dataclass(grepr_fields=["blocks"])
class SRScriptInputValue(SRInputValue):
    """
    The second representation for a block input, which contains a substack of blocks
    """
    
    blocks: list[SRBlock]

    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        validation_if: "ValidationIF", 
        context: CompleteContext, 
        input_type: InputType, 
    ) -> None:
        """
        Ensures this input is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            validation_if: interface which allows the management of other blocks 
            context: Context about parts of the project. Used to validate dropdowns
            input_type: the type of this input. Used to valdiate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRScriptInputValue is invalid
        """
        AA_LIST_OF_TYPE(self, path, "blocks", SRBlock)
        for i, block in enumerate(self.blocks):
            current_path = path+["blocks", i]
            block.validate(
                path             = current_path,
                info_api         = info_api,
                validation_if    = validation_if,
                context          = context,
                expects_reporter = False,
            )
            opcode_info = info_api.get_info_by_new(block.opcode)
            opcode_type = opcode_info.get_opcode_type(block=block, validation_if=validation_if)
            SRBlock.validate_opcode_type(
                path         = current_path,
                opcode_type  = opcode_type,
                is_top_level = False,
                is_first     = (i == 0),
                is_last      = ((i+1) == len(self.blocks)),
            )


__all__ = [
    "FRBlock", "IRBlock", "IRInputValue", 
    "SRScript", "SRBlock", "SRInputValue", 
    "SRBlockAndTextInputValue", "SRBlockAndDropdownInputValue", "SRBlockAndBoolInputValue",
    "SRBlockOnlyInputValue", "SRScriptInputValue",
]

