from typing      import Any
from dataclasses import dataclass, field

from utility        import GreprClass
from utility        import AA_TYPE, AA_TYPES, AA_COORD_PAIR, AA_LIST_OF_TYPE, AA_DICT_OF_TYPE
from utility        import UnnecessaryInputError, MissingInputError, UnnecessaryDropdownError, MissingDropdownError, InvalidValueValidationError
from opcode_info    import OpcodeInfoAPI, OpcodeInfo, InputMode, OpcodeType, SpecialCaseType
from block_opcodes  import *

from core.block_mutation import FRMutation, FRCustomBlockMutation, FRCustomArgumentMutation, FRCustomCallMutation
from core.block_mutation import SRMutation
from core.comment        import SRAttachedComment
from core.context        import FullContext
from core.dropdown       import SRDropdownValue
from core.fr_to_tr_api   import FRtoTRAPI

@dataclass
class FRBlock(GreprClass):
    _grepr = True
    _grepr_fields = ["opcode", "next", "parent", "inputs", "fields", "shadow", "top_level", "x", "y", "comment", "mutation"]

    opcode: str
    next: str | None
    parent: str
    inputs: dict[str, (
       tuple[int, str | tuple] 
     | tuple[int, str | tuple, str | tuple]
    )]
    fields: dict[str, tuple[str, str] | tuple[str, str, str]]
    shadow: bool
    top_level: bool
    x: int | float | None
    y: int | float | None
    comment: str | None # a comment id
    mutation: "FRMutation | None"

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        # TODO: add special case for this
        if   data["opcode"] == OPCODE_CB_PROTOTYPE:
            mutation = FRCustomBlockMutation.from_data(data["mutation"])
        elif data["opcode"] in ANY_OPCODE_CB_ARG:
            mutation = FRCustomArgumentMutation.from_data(data["mutation"])
        elif data["opcode"] == OPCODE_CB_CALL:
            mutation = FRCustomCallMutation.from_data(data["mutation"])
        elif "mutation" in data:
            raise ValueError(data)
        else:
            mutation = None
        return cls(
            opcode    = data["opcode"  ],
            next      = data["next"    ],
            parent    = data["parent"  ],
            inputs    = {
                input_id: tuple(
                    [tuple(item) if isinstance(item, list) else item for item in input_data]
                ) for input_id, input_data in data["inputs"].items()
            },
            fields    = {
                field_id: tuple(field_data) for field_id, field_data in data["fields"].items()
            },
            shadow    = data["shadow"  ],
            top_level = data["topLevel"],
            x         = data.get("x", None),
            y         = data.get("y", None),
            comment   = data.get("comment", None),
            mutation  = mutation,
        )
    
    @classmethod
    def from_tuple(cls, 
            obj: tuple[str, str, str] | tuple[str, str, str, int|float, int|float],
            parent_id: str | None,
        ) -> "FRBlock":
        if obj[0] == OPCODE_VAR_VALUE_NUM:
            block_data = {
                "opcode": OPCODE_VAR_VALUE,
                "next"  : None,
                "parent": parent_id,
                "inputs": {},
                "fields": {"VARIABLE": (obj[1], obj[2], '')},
                "shadow": False,
                "topLevel": parent_id is None,
            }
        elif obj[0] == OPCODE_LIST_VALUE_NUM:
            block_data = {
                "opcode": OPCODE_LIST_VALUE,
                "next"  : None,
                "parent": parent_id,
                "inputs": {},
                "fields": {"LIST": (obj[1], obj[2], '')},
                "shadow": False,
                "topLevel": parent_id is None,
            }
        else: raise ValueError(obj)
        if   (len(obj) == 3) and (parent_id is not None): 
            pass
        elif (len(obj) == 5) and (parent_id is None):
            block_data["x"] = obj[3]
            block_data["y"] = obj[4]
        else: raise ValueError()
        return cls.from_data(block_data)

    def step(self, 
        block_api: FRtoTRAPI, 
        info_api: OpcodeInfoAPI, 
        own_id: str
    ) -> "TRBlock":
        opcode_info = info_api.get_info_by_old(self.opcode)
        pre_case = opcode_info.get_special_case(SpecialCaseType.PRE_FR_STEP)
        if pre_case is not None:
            self = pre_case.call(block_api=block_api, block=self)
        
        instead_case = opcode_info.get_special_case(SpecialCaseType.INSTEAD_FR_STEP)
        if instead_case is None:
            new_inputs = self.step_inputs(
                block_api  = block_api,
                info_api   = info_api,
                opcode_info = opcode_info,
                own_id     = own_id,
            )
            new_dropdowns = {}
            for dropdown_id, dropdown_value in self.fields.items():
                new_dropdowns[dropdown_id] = dropdown_value[0]
            
            new_block = TRBlock(
                opcode       = self.opcode,
                inputs       = new_inputs,
                dropdowns    = new_dropdowns,
                position     = (self.x, self.y) if self.top_level else None,
                comment      = None if self.comment  is None else block_api.get_comment(self.comment),
                mutation     = None if self.mutation is None else self.mutation.step(
                    block_api = block_api,
                ),
                next         = None if self.next     is None else TRBlockReference(self.next),
                is_top_level = self.top_level,
            )
        else:
            new_block = instead_case.call(block_api=block_api, block=self)
        
        #TODO: add custom handler system here for e.g. draw polygon block
        return new_block

    def step_inputs(self, 
        block_api: FRtoTRAPI, 
        info_api: OpcodeInfoAPI,
        opcode_info: OpcodeInfo,
        own_id: str
    ) -> dict[str, "TRInputValue"]:
        instead_case = opcode_info.get_special_case(SpecialCaseType.INSTEAD_FR_STEP_INPUTS_GET_MODES)
        if instead_case is None:
            input_modes = {
                input_id: opcode_info.get_input_info_by_old(input_id).type.get_mode()
                for input_id in self.inputs.keys()
            }
        else:
            input_modes = instead_case.call(block_api=block_api, block=self)                
        
        new_inputs = {}
        for input_id, input_value in self.inputs.items():
            input_mode = input_modes[input_id]

            item_one_type   = type(input_value[1])
            references      = []
            immediate_block = None
            text            = None
            # Account for list blocks; 
            if   len(input_value) == 2:
                if   item_one_type == str: # e.g. "CONDITION": (2, "b")
                    # one block only, no text
                    references.append(TRBlockReference(input_value[1]))
                elif item_one_type == tuple: # e.g. "MESSAGE": (1, (10, "Bye!"))
                    # one block(currently empty) and text
                    text = input_value[1][1]
            elif len(input_value) == 3:
                item_two_type = type(input_value[2])
                if   item_one_type == str  and item_two_type == str: # e.g. "TOUCHINGOBJECTMENU": (3, "d", "e")
                    # two blocks(a menu, and a normal block) and no text
                    references.append(TRBlockReference(input_value[1]))
                    references.append(TRBlockReference(input_value[2]))
                elif item_one_type == str  and item_two_type == tuple: # e.g. 'OPERAND1': (3, 'e', (10, ''))
                    # one block and text
                    references.append(TRBlockReference(input_value[1]))
                    text = input_value[2][1]
                elif item_one_type == str  and item_two_type == type(None): # e.g. 'custom input bool': (3, 'c', None)
                    # one block
                    references.append(TRBlockReference(input_value[1]))
                elif item_one_type == tuple and item_two_type == tuple: # e.g. 'VALUE': (3, (12, 'var', '=!vkqJLb6ODy(oqe-|ZN'), (10, '0'))
                    # one list block and text
                    immediate_block = FRBlock.from_tuple(input_value[1], parent_id=own_id).step(
                        block_api=block_api,
                        info_api=info_api,
                        own_id=None, # None is fine, because tuple blocks can't possibly contain more tuple blocks 
                    )
                    text      = input_value[2][1]
                elif item_one_type == tuple and item_two_type == str: # "TOUCHINGOBJECTMENU": (3, (12, "my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable"), "b")
                    # two blocks(a menu, and a list block) and no text
                    immediate_block = FRBlock.from_tuple(input_value[1], parent_id=own_id).step(
                        block_api=block_api,
                        info_api=info_api,
                        own_id=None, # None is fine, because tuple blocks can't possibly contain more tuple blocks 
                    )
                    references.append(TRBlockReference(input_value[2]))
                else: raise ValueError()
            new_input_data_1 = {
                "mode"           : input_mode,
                "references"     : references,
                "immediate_block": immediate_block,
                "text"           : text,
            }
            
            
            references      = []
            immediate_block = None
            text            = None
            
            for item in input_value[1:]: # ignore first item(some irrelevant number)
                if isinstance(item, str):
                    references.append(TRBlockReference(item))
                elif isinstance(item, tuple) and item[0] in {4, 5, 6, 7, 8, 9, 10, 11}:
                    text = item[1]
                elif isinstance(item, tuple) and item[0] in {12, 13}:
                    immediate_block = FRBlock.from_tuple(item, parent_id=own_id).step(
                        block_api=block_api,
                        info_api=info_api,
                        own_id=None, # None is fine, because tuple blocks can't possibly contain more tuple blocks 
                    )
                else: raise ValueError()
            new_input_data_2 = {
                "mode"           : input_mode,
                "references"     : references,
                "immediate_block": immediate_block,
                "text"           : text,
            }
            
            # Im temporarily keeping both systems to ensure the new system produces the same output
            if new_input_data_1 != new_input_data_2:
                print("nid1", new_input_data_1)
                print("nid2", new_input_data_2)
                raise Exception("Conflict!")

            #print("input", input_id, input_mode, input_value)
            new_inputs[input_id] = TRInputValue(
                mode            = input_mode,
                references      = references,
                immediate_block = immediate_block,
                text            = text,
            )
        
        # Check for missing inputs and give a default value where possible otherwise raise
        for input_id, input_mode in input_modes.items():
            if input_id in new_inputs:
                continue
            if input_mode in {InputMode.BLOCK_ONLY, InputMode.SCRIPT}:
                new_inputs[input_id] = TRInputValue(
                    mode            = input_mode,
                    references      = [],
                    immediate_block = None,
                    text            = None,
                )
            # TODO: special handler case for e.g. polygon block (x4, y4)
            else: raise ValueError()
            
        # Also translate old input ids to new input ids
        return new_inputs



@dataclass
class TRBlock(GreprClass):
    """Temporary Block Representation."""
    _grepr = True
    _grepr_fields = ["opcode", "inputs", "dropdowns", "comment", "mutation", "position", "next", "is_top_level"]
    
    opcode: str
    inputs: dict[str, "TRInputValue"]
    dropdowns: dict[str, Any]
    comment: SRAttachedComment | None
    mutation: "SRMutation | None"
    position: tuple[int | float, int | float] | None
    next: "TRBlockReference | None"
    is_top_level: bool

    def step(self, 
            all_blocks: dict[str, "TRBlock"],
            info_api: OpcodeInfoAPI,
        ) -> tuple[tuple[int|float,int|float] | None, list["SRBlock | str"]]:
        
        opcode_info = info_api.get_info_by_old(self.opcode)
        if opcode_info.opcode_type == OpcodeType.MENU:
            return (None, [list(self.dropdowns.values())[0]])
            """ example:
            {
                opcode="#TOUCHING OBJECT MENU",
                options={"TOUCHINGOBJECTMENU": ["object", "_mouse_"]},
                ...
            }
            --> "_mouse_" """
        
        new_inputs = {}
        for input_id, input_value in self.inputs.items():
            sub_blocks = []
            for sub_reference in input_value.references: 
                sub_block = all_blocks[sub_reference]
                _, more_sub_blocks = sub_block.step(
                    all_blocks    = all_blocks,
                    info_api      = info_api,
                )
                sub_blocks.append(more_sub_blocks)
            
            if input_value.immediate_block is not None:
                sub_blocks.insert(0, [input_value.immediate_block])
            
            block_count = len(sub_blocks)
            
            if block_count == 2:
                sub_script  = sub_blocks[0]
                sub_block_a = sub_blocks[0][0]
                sub_block_b = sub_blocks[1][0]
            elif block_count == 1:
                sub_script  = sub_blocks[0]
                sub_block_a = sub_blocks[0][0]
                sub_block_b = None
            elif block_count == 0:
                sub_script  = []
                sub_block_a = None
                sub_block_b = None
            else: raise ValueError()
            
            input_blocks   = []
            input_block    = None
            input_text     = None
            input_dropdown = None
            
            match input_value.mode:
                case InputMode.BLOCK_AND_TEXT:
                    assert block_count in {0, 1}
                    input_block = sub_block_a
                    input_text  = input_value.text
                case InputMode.BLOCK_AND_BROADCAST_DROPDOWN:
                    assert block_count in {0, 1}
                    input_block     = sub_block_a
                    input_dropdown  = input_value.text
                case InputMode.BLOCK_ONLY:
                    assert block_count in {0, 1}
                    input_block = sub_block_a
                case InputMode.SCRIPT:
                    assert block_count in {0, 1}
                    input_blocks = sub_script
                case InputMode.BLOCK_AND_DROPDOWN:
                    assert block_count in {1, 2}
                    if   block_count == 1:
                        input_block    = None
                        input_dropdown = sub_block_a
                    elif block_count == 2:
                        input_block    = sub_block_a
                        input_dropdown = sub_block_b
                case InputMode.BLOCK_AND_MENU_TEXT:
                    assert block_count in {1, 2}
                    if   block_count == 1:
                        input_block  = None
                        input_text   = sub_block_a
                    elif block_count == 2:
                        input_block  = sub_block_a
                        input_text   = sub_block_b
                case _: raise ValueError()

            if input_dropdown is not None:
                input_type = opcode_info.get_input_info_by_old(input_id).type
                dropdown_type = input_type.get_corresponding_dropdown_type()
                input_dropdown = dropdown_type.translate_old_to_new_value(input_dropdown)

            
            instead_case = opcode_info.get_special_case(SpecialCaseType.INSTEAD_GET_NEW_INPUT_ID)
            if instead_case is None:
                new_input_id = opcode_info.get_new_input_id(input_id)
            else:
                new_input_id = instead_case.call(block=self, input_id=input_id)
            
            # TODO: add special case for handler for polygon block(x4, y4 inputs)
            new_inputs[new_input_id] = SRInputValue(
                mode     = input_value.mode,
                blocks   = input_blocks,
                block    = input_block,
                text     = input_text,
                dropdown = input_dropdown,
            )
        
        new_dropdowns = {}
        for dropdown_id, dropdown_value in self.dropdowns.items():
            dropdown_type = opcode_info.get_dropdown_info_by_old(dropdown_id).type
            new_dropdown_id = opcode_info.get_new_dropdown_id(dropdown_id)
            new_dropdowns[new_dropdown_id] = dropdown_type.translate_old_to_new_value(
                old_value=dropdown_value
            )

        new_block = SRBlock(
            opcode    = info_api.get_new_by_old(self.opcode),
            inputs    = new_inputs,
            dropdowns = new_dropdowns,
            comment   = self.comment,
            mutation  = self.mutation,
        )
        new_blocks = [new_block]
        if self.next is not None:
            next_block = all_blocks[self.next]
            _, next_blocks = next_block.step(
                all_blocks    = all_blocks,
                info_api      = info_api,
            )
            new_blocks.extend(next_blocks)
        
        return (self.position, new_blocks) 
 
@dataclass
class TRInputValue(GreprClass):
    _grepr = True
    _grepr_fields = ["mode", "references", "immediate_block", "text"]
    
    mode: InputMode
    references: list["TRBlockReference"]
    immediate_block: TRBlock | None
    text: str | None

@dataclass
class TRBlockReference(GreprClass):    
    id: str
    
    def __repr__(self):
        return f"TRBR({self.id})"
    
    def __hash__(self):
        return hash(self.id)

@dataclass
class SRScript(GreprClass):
    _grepr = True
    _grepr_fields = ["position", "blocks"]

    position: tuple[int | float, int | float]
    blocks: list["SRBlock"]

    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        context: FullContext,
    ) -> None:
        AA_COORD_PAIR(self, path, "position")
        AA_LIST_OF_TYPE(self, path, "blocks", SRBlock)
        
        for i, block in enumerate(self.blocks):
            current_path = path+["blocks", i]
            block.validate(
                path     = current_path,
                info_api = info_api,
                context  = context,
            )

@dataclass
class SRBlock(GreprClass):
    _grepr = True
    _grepr_fields = ["opcode", "inputs", "dropdowns", "comment", "mutation"]
    
    opcode: str
    inputs: dict[str, "SRInputValue"]
    dropdowns: dict[str, SRDropdownValue]
    comment: SRAttachedComment | None
    mutation: "SRMutation | None"
    
    def validate(self, 
        path: list, 
        info_api: OpcodeInfoAPI, 
        context: FullContext,
    ) -> None:
        AA_TYPE(self, path, "opcode", str)
        AA_DICT_OF_TYPE(self, path, "inputs"   , key_t=str, value_t=SRInputValue   )
        AA_DICT_OF_TYPE(self, path, "dropdowns", key_t=str, value_t=SRDropdownValue)
        AA_TYPES(self, path, "comment", (SRAttachedComment, type(None)))
        AA_TYPES(self, path, "mutation", (SRMutation, type(None)))
        
        opcode_info = info_api.get_info_by_new_safe(self.opcode)
        if opcode_info is None:
            raise InvalidValueValidationError(path, f"opcode of {self.__class__.__name__} must be a defined opcode")
        
        instead_case = opcode_info.get_special_case(SpecialCaseType.INSTEAD_GET_ALL_NEW_INPUT_IDS)
        if instead_case is None:
            new_input_ids = opcode_info.get_all_new_input_ids()
        else:
            new_input_ids = instead_case.call(block=self)
        
        for new_input_id, input_value in self.inputs.items():
            input_value.validate(
                path     = path+["inputs", (new_input_id,)],
                info_api = info_api,
                context  = context,
            )
            if new_input_id not in new_input_ids:
                raise UnnecessaryInputError(path, f"inputs of {self.__class__.__name__} with opcode {repr(self.opcode)} includes unnecessary input {repr(new_input_id)}")
        for new_input_id in new_input_ids:
            if new_input_id not in self.inputs:
                raise MissingInputError(path, f"inputs of {self.__class__.__name__} with opcode {repr(self.opcode)} is missing input {repr(new_input_id)}")
        
        new_dropdown_ids = opcode_info.get_all_new_dropdown_ids()
        for new_dropdown_id, dropdown_value in self.dropdowns.items():
            dropdown_value.validate(path+["dropdowns", (new_dropdown_id,)])
            if new_dropdown_id not in new_dropdown_ids:
                raise UnnecessaryDropdownError(path, f"dropdowns of {self.__class__.__name__} with opcode {repr(self.opcode)} includes unnecessary dropdown {repr(new_dropdown_id)}")
        for new_dropdown_id in new_dropdown_ids:
            if new_dropdown_id not in self.dropdowns:
                raise MissingDropdownError(path, f"dropdowns of {self.__class__.__name__} with opcode {repr(self.opcode)} is missing dropdown {repr(new_dropdown_id)}")

@dataclass
class SRInputValue(GreprClass):
    _grepr = True
    _grepr_fields = ["mode"]

    mode: InputMode
    blocks: list[SRBlock] = field(default_factory=list)
    block: SRBlock            | None = None
    text: str                 | None = None
    dropdown: SRDropdownValue | None = None
    
    def __post_init__(self):
        match self.mode:
            case InputMode.BLOCK_AND_TEXT | InputMode.BLOCK_AND_MENU_TEXT:
                self.block    = block
                self.text     = text
                self._grepr_fields = SRInputValue._grepr_fields + ["block", "text"]
            case InputMode.BLOCK_AND_DROPDOWN | InputMode.BLOCK_AND_BROADCAST_DROPDOWN:
                self.block    = block
                self.dropdown = dropdown
                self._grepr_fields = SRInputValue._grepr_fields + ["block", "dropdown"]
            case InputMode.BLOCK_ONLY:
                self.block    = block
                self._grepr_fields = SRInputValue._grepr_fields + ["block"]
            case InputMode.SCRIPT:
                self.blocks   = blocks or []
                self._grepr_fields = SRInputValue._grepr_fields + ["blocks"]
    
    def validate(self, path: list, info_api: OpcodeInfoAPI, context: FullContext) -> None:
        AA_TYPE(self, path, "mode", InputMode)
        AA_LIST_OF_TYPE(self, path, "blocks", SRBlock)
        AA_TYPES(self, path, "block", (SRBlock, type(None)))
        AA_TYPES(self, path, "text", (str, type(None)))
        AA_TYPES(self, path, "dropdown", (SRDropdownValue, type(None)))
        
        # TODO: complete this
