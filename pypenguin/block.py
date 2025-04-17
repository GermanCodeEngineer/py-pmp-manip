from typing import Any

from utility               import gprint, PypenguinClass
from block_mutation        import FRMutation, FRCustomBlockMutation, FRCustomArgumentMutation, FRCustomCallMutation
from block_mutation        import SRMutation
from block_opcodes         import *
from config                import FRtoTRApi, SpecialCaseHandler, SpecialCaseType
from block_info            import BlockInfoApi, BlockInfo, InputMode
from comment               import SRAttachedComment

class FRBlock(PypenguinClass):
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

    # Temporary
    block_info: BlockInfo | None

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        self = cls()
        self.opcode    = data["opcode"  ]
        self.next      = data["next"    ]
        self.parent    = data["parent"  ]
        self.inputs    = {}
        for input_id, input_data in data["inputs"].items():
            input_data = [tuple(item) if isinstance(item, list) else item for item in input_data]
            self.inputs[input_id] = tuple(input_data)
        self.fields    = {
            field_id: tuple(field_data) for field_id, field_data in data["fields"].items()
        }
        self.shadow    = data["shadow"  ]
        self.top_level = data["topLevel"]
        self.x         = data.get("x", None)
        self.y         = data.get("y", None)
        self.comment   = data.get("comment", None)
        if self.opcode == OPCODE_CB_PROTOTYPE:
            self.mutation = FRCustomBlockMutation.from_data(data["mutation"])
        elif self.opcode in ANY_OPCODE_CB_ARG:
            self.mutation = FRCustomArgumentMutation.from_data(data["mutation"])
        elif self.opcode == OPCODE_CB_CALL:
            self.mutation = FRCustomCallMutation.from_data(data["mutation"])
        elif "mutation" in data:
            raise ValueError(data)
        else:
            self.mutation = None
        return self
    
    @classmethod
    def from_tuple(cls, obj: tuple, parent_id: str|None) -> "FRBlock":
        if obj[0] == OPCODE_VAR_VALUE_NUM: # A magic value
            block_data = {
                "opcode": OPCODE_VAR_VALUE,
                "next"  : None,
                "parent": parent_id,
                "inputs": {},
                "fields": {"VARIABLE": (obj[1], obj[2], '')},
                "shadow": False,
                "topLevel": parent_id is None,
            }
        elif obj[0] == OPCODE_LIST_VALUE_NUM: # A magic value
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


    def step_inputs(self, 
        config: SpecialCaseHandler, 
        block_api: FRtoTRApi, 
        info_api: BlockInfoApi,
        block_info: BlockInfo,
        own_id: str
    ) -> dict[str, "TRInput"]:        
        instead_event = config.get_event(
            event_type = SpecialCaseType.INSTEAD_FR_STEP_INPUTS_GET_MODES,
            opcode     = self.opcode
        )
        if instead_event is None:
            input_modes = {
                input_id: block_info.get_input_mode(input_id) 
                for input_id in self.inputs.keys()
            }
        else:
            input_modes = instead_event.call(block_api=block_api, block=self)                
        
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
                        config=config,
                        block_api=block_api,
                        info_api=info_api,
                        own_id=None, # None is fine, because tuple blocks can't possibly contain more tuple blocks 
                    )
                    text      = input_value[2][1]
                elif item_one_type == tuple and item_two_type == str: # "TOUCHINGOBJECTMENU": (3, (12, "my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable"), "b")
                    # two blocks(a menu, and a list block) and no text
                    immediate_block = FRBlock.from_tuple(input_value[1], parent_id=own_id).step(
                        config=config,
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
                        config=config,
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
            
            
            if new_input_data_1 != new_input_data_2:
                gprint("nid1", new_input_data_1)
                gprint("nid2", new_input_data_2)
                raise Exception("Conflict!")

            #print("input", input_id, input_mode, input_value)
            new_inputs[input_id] = TRInput(
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
                new_inputs[input_id] = {
                    "mode"      : input_mode,
                    "references": [],
                    "listBlock" : None,
                    "text"      : None,
                }
            # TODO: special handler case for e.g. polygon block (x4, y4)
            else: raise ValueError()
            
        # Also translate old input ids to new input ids
        new_inputs = {block_info.get_new_input_id(input_id): input_value for input_id, input_value in new_inputs.items()}
        return new_inputs

    def step(self, 
        config: SpecialCaseHandler, 
        block_api: FRtoTRApi, 
        info_api: BlockInfoApi, 
        own_id: str
    ) -> "TRBlock":
        block_info = info_api.get_info_by_opcode(self.opcode)
        pre_event = config.get_event(
            event_type = SpecialCaseType.PRE_FR_STEP,
            opcode     = self.opcode,
        )
        if pre_event is not None:
            self = pre_event.call(block_api=block_api, block=self)
        
        instead_event = config.get_event(
            event_type = SpecialCaseType.INSTEAD_FR_STEP,
            opcode     = self.opcode,
        )
        if instead_event is None:
            new_inputs = self.step_inputs(
                config     = config,
                block_api  = block_api,
                info_api   = info_api,
                block_info = block_info,
                own_id     = own_id,
            )
            new_dropdowns = {}
            for dropdown_id, dropdown_value in self.fields.items():
                new_dropdown_id = block_info.get_new_dropdown_id(dropdown_id)
                new_dropdowns[new_dropdown_id] = dropdown_value[0]
            
            new_block = TRBlock(
                opcode       = self.opcode,
                inputs       = new_inputs,
                dropdowns    = new_dropdowns,
                position     = (self.x, self.y) if self.top_level else None,
                comment      = None if self.comment  is None else block_api.get_comment(self.comment),
                mutation     = None if self.mutation is None else self.mutation.step(
                    block_api = block_api,
                ),
                next         = self.next,
                is_top_level = self.top_level,
            )
        else:
            new_block = instead_event.call(block_api=block_api, block=self)
        
        #TODO: add custom handler system here for e.g. draw polygon block
        return new_block


class TRBlock(PypenguinClass):
    """Temporary Block Representation."""
    _grepr = True
    _grepr_fields = ["opcode", "inputs", "dropdowns", "comment", "mutation", "position", "next", "is_top_level"]
    
    opcode: str
    inputs: dict[str, "TRInput"]
    dropdowns: dict[str, Any]
    comment: SRAttachedComment | None
    mutation: "SRMutation | None"
    position: tuple[int | float, int | float] | None
    next: str | None
    is_top_level: bool

    def __init__(self, 
        opcode: str,
        inputs: dict[str, "TRInput"],
        dropdowns: dict[str, Any],
        comment: SRAttachedComment | None,
        mutation: "SRMutation | None",
        position: tuple[int | float, int | float] | None,
        next: str | None,
        is_top_level: bool,
    ):
        self.opcode       = opcode
        self.inputs       = inputs
        self.dropdowns    = dropdowns
        self.comment      = comment
        self.mutation     = mutation
        self.position     = position
        self.next         = next
        self.is_top_level = is_top_level
    
    def nest_recursively(self, 
            all_blocks: dict[str, "TRBlock"],
            own_reference: str,
        ) -> tuple[tuple[int|float,int|float] | None, list["SRBlock"]]:
        new_inputs = {}
        for input_id, input_value in self.inputs.items():
            sub_blocks = []
            for sub_reference in input_value.references: 
                sub_blocks.append(all_blocks[sub_reference].nest_recursively(
                    all_blocks    = all_blocks,
                    own_reference = sub_reference,
                )[1])

            if input_value.immediate_block is not None:
                sub_blocks.insert(0, [input_value.immediate_block])
            
            block_count = len(sub_blocks)

            if block_count == 2:
                sub_script  = sub_blocks[0]
                sub_block_0 = sub_blocks[0][0]
                sub_block_1 = sub_blocks[1][0]
            elif block_count == 1:
                sub_script  = sub_blocks[0]
                sub_block_0 = sub_blocks[0][0]
                sub_block_1 = None
            elif block_count == 0:
                sub_script  = []
                sub_block_0 = None
                sub_block_1 = None
            else: raise ValueError()

            input_blocks   = []
            input_block    = None
            input_text     = None
            input_dropdown = None

            match input_value["mode"]:
                case "block-and-text"|"block-and-broadcast-option":
                    assert block_count in {0, 1}
                    input_block = sub_block_0
                    input_text  = input_value.text
                case "block-only":
                    assert block_count in {0, 1}
                    input_block = sub_block_0
                case "script":
                    assert block_count in {0, 1}
                    input_blocks = sub_script
                case "block-and-option"|"block-and-menu-text":
                    assert block_count in {1, 2}
                    if   block_count == 1:
                        input_block    = None
                        input_dropdown = sub_block_0
                    elif block_count == 2:
                        input_block    = sub_block_0
                        input_dropdown = sub_block_1
            new_inputs[input_id] = SRInput(
                mode=input_mode,
                references=input_re
            )
    
class TRInput(PypenguinClass):
    _grepr = True
    _grepr_fields = ["mode", "references", "immediate_block", "text"]
    
    mode: InputMode
    references: list["TRBlockReference"]
    immediate_block: TRBlock | None
    text: str | None
    
    def __init__(self,
        mode: InputMode,
        references: list["TRBlockReference"],
        immediate_block: TRBlock | None,
        text: str | None,
    ):
        self.mode            = mode
        self.references      = references
        self.immediate_block = immediate_block
        self.text            = text

class TRBlockReference(PypenguinClass):
    _grepr = True
    _grepr_fields = ["id"]
    
    id: str
    
    def __init__(self, id):
        self.id = id
    
    def __hash__(self):
        return hash(self.id)


class SRScript(PypenguinClass):
    _grepr = True
    _grepr_fields = ["position", "blocks"]

    position: tuple[int | float, int | float]
    blocks: list["SRBlock"]

    def __init__(self, position: tuple[int | float, int | float], blocks: list["SRBlock"]):
        self.position = position
        self.blocks   = blocks

class SRBlock(PypenguinClass):
    _grepr = True
    _grepr_fields = ["opcode", "inputs", "dropdowns", "comment", "mutation"]
    
    opcode: str
    inputs: dict[str, "SRInput"]
    dropdowns: dict[str, Any]
    comment: SRAttachedComment | None
    mutation: "SRMutation | None"

    def __init__(self, 
        opcode: str,
        inputs: dict[str, "TRInput"],
        dropdowns: dict[str, Any],
        comment: SRAttachedComment | None,
        mutation: "SRMutation | None",
    ):
        self.opcode       = opcode
        self.inputs       = inputs
        self.dropdowns    = dropdowns
        self.comment      = comment
        self.mutation     = mutation
    

class SRInput(PypenguinClass):
    _grepr = True
    _grepr_fields = ["blocks", "block", "text", "dropdown"]

    blocks: list[SRBlock] | None
    block: SRBlock | None
    text: str | None
    dropdown: Any | None
    
    
    def __init__(self,
        blocks: list[SRBlock] | None,
        block: SRBlock | None,
        text: str | None,
        dropdown: Any | None,
    ):
        self.mode            = mode
        self.references      = references
        self.immediate_block = immediate_block
        self.text            = text
