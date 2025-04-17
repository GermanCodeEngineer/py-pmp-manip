from typing import Callable

from utility               import gprint
from block_mutation        import FRMutation, FRCustomBlockMutation, FRCustomArgumentMutation, FRCustomCallMutation
from block_mutation        import SRMutation
from block_opcodes         import *
from config                import FRtoSRApi, Configuration, ConfigType
from block_info            import BlockInfoApi, BlockInfo

class FRBlock:
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
    def from_data(cls, data):
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
    def from_tuple(cls, obj: tuple, parent_id: str|None):
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
        else: raise ValueError()
        if   (len(obj) == 3) and (parent_id is not None): 
            pass
        elif (len(obj) == 5) and (parent_id is None):
            block_data["x"] = obj[3]
            block_data["y"] = obj[4]
        else: raise ValueError()
        return cls.from_data(block_data)

    

    def step_inputs(self, config: Configuration, block_api: FRtoSRApi, block_info: BlockInfo):
        #TODO: Replace the old with the new input ids
        
        instead_event = config.get_event(
            event_type = ConfigType.INSTEAD_FR_STEP_INPUTS_GET_MODES,
            opcode     = self.opcode
        )
        if instead_event is None:
            input_modes = {
                input_id: block_info.get_input_mode(input_id) 
                for input_id in self.inputs.keys()
            }
        else:
            input_modes = instead_event.call(block_api=block_api, block=self)                
        
        for input_id, input_value in self.inputs.items():
            input_mode = input_modes[input_id]

            item_one_type = type(input_value)
            references    = []
            list_block    = None
            text          = None
            # Account for list blocks; 
            if   len(input_value) == 2:
                if   item_one_type == str: # e.g. "CONDITION": [2, "b"]
                    # one block only, no text
                    references.append(input_value[1])
                elif item_one_type == list: # e.g. "MESSAGE": [1, [10, "Bye!"]]
                    # one block(currently empty) and text
                    text = input_value[1][1]
            elif len(input_value) == 3:
                #print("step 1")
                itemTwoType = type(input_value[2])
                if   item_one_type == str  and itemTwoType == str: # e.g. "TOUCHINGOBJECTMENU": [3, "d", "e"]
                    # two blocks(a menu, and a normal block) and no text
                    references.append(input_value[1])
                    references.append(input_value[2])
                elif item_one_type == str  and itemTwoType == list: # e.g. 'OPERAND1': [3, 'e', [10, '']]
                    # one block and text
                    references.append(input_value[1])
                    text = input_value[2][1]
                elif item_one_type == str  and itemTwoType == type(None): # e.g. 'custom input bool': [3, 'c', None]
                    # one block
                    references.append(input_value[1])
                elif item_one_type == list and itemTwoType == list: # e.g. 'VALUE': [3, [12, 'var', '=!vkqJLb6ODy(oqe-|ZN'], [10, '0']]
                    # one list block and text
                    listBlock = prepareListBlock(
                        data=input_value[1], 
                        blockId=None,
                        commentDatas=commentDatas,
                    ) #translate list blocks into standard blocks
                    text      = input_value[2][1]
                elif item_one_type == list and itemTwoType == str: # "TOUCHINGOBJECTMENU": [3, [12, "my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable"], "b"]
                    # two blocks(a menu, and a list block) and no text
                    listBlock = prepareListBlock(
                        data=input_value[1], 
                        blockId=None,
                        commentDatas=commentDatas,
                    )
                    references.append(input_value[2])
            newInputData = {
                "mode"      : input_mode,
                "references": references,
                "listBlock" : listBlock,
                "text"      : text,
    }

            print("input", input_id, input_mode, input_value)

    def step(self, config: Configuration, block_api: FRtoSRApi, info_api: BlockInfoApi) -> "SRBlock":
        block_info = info_api.get_info_by_opcode(self.opcode)
        pre_event = config.get_event(
            event_type = ConfigType.PRE_FR_STEP,
            opcode     = self.opcode,
        )
        if pre_event is not None:
            self = pre_event.call(block_api=block_api, block=self)
        
        instead_event = config.get_event(
            event_type = ConfigType.INSTEAD_FR_STEP,
            opcode     = self.opcode,
        )
        if instead_event is None:
            new_block = SRBlock(
                opcode       = self.opcode,
                inputs       = self.step_inputs(
                    config     = config,
                    block_api  = block_api,
                    block_info = block_info,
                ),
                dropdowns    = self.fields, #TODO
                position     = (self.x, self.y) if self.top_level else None,
                comment      = self.comment,
                mutation     = None if self.mutation is None else self.mutation.step(
                    block_api = block_api,
                ),
                next         = self.next,
                is_top_level = self.top_level,
            )
        else:
            new_block = instead_event.call(block_api=block_api, block=self)
            pass #TODO: add custom handler system here to possibly replace below
                 #      for e.g. custom block defs, prototypes, calls
        
        #TODO: add custom handler system here for e.g. draw polygon block
        return new_block

class SRBlock:
    _grepr = True
    _grepr_fields = ["opcode", "inputs", "dropdowns", "comment", "mutation", "position", "next", "is_top_level"]
    
    opcode: str
    #inputs: dict[str, ?]
    #dropdowns: dict[str, ?]
    comment: str | None # a comment id
    position: tuple[int | float, int | float] | None
    mutation: "SRMutation | None"
    next: str | None
    is_top_level: bool

    def __init__(self, 
        opcode: str,
        inputs,#: dict[str, ?],
        dropdowns,#: dict[str, ?],
        comment: str | None, # a comment id
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
        

