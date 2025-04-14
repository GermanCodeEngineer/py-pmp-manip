import json

from utility import gprint
from block_mutation import FRMutation, FRCustomBlockMutation, FRCustomArgumentMutation

# Variables
OPCODE_VAR_VALUE      = "data_variableValue"
OPCODE_LIST_VALUE     = "data_listValue"
OPCODE_VAR_VALUE_NUM  = 12
OPCODE_LIST_VALUE_NUM = 13

# Custom Blocks
OPCODE_CB_DEF       = "procedures_definition"
OPCODE_CB_DEF_RET   = "procedures_definition_return"
ANY_OPCODE_CB_DEF   =  {OPCODE_CB_DEF, OPCODE_CB_DEF_RET}

OPCODE_CB_PROTOTYPE = "procedures_prototype"

OPCODE_CB_ARG_TEXT  = "argument_reporter_string_number"
OPCODE_CB_ARG_BOOL  = "argument_reporter_boolean"
ANY_OPCODE_CB_ARG   = {OPCODE_CB_ARG_TEXT, OPCODE_CB_ARG_BOOL}

class FRBlock:
    _grepr = True
    _grepr_fields = ["opcode", "next", "parent", "inputs", "fields", "shadow", "top_level", "x", "y", "comment", "mutation"]

    opcode: str
    next: str
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
                "topLevel": parent_id == None,
            }
        elif obj[0] == OPCODE_LIST_VALUE_NUM: # A magic value
            block_data = {
                "opcode": OPCODE_LIST_VALUE,
                "next"  : None,
                "parent": parent_id,
                "inputs": {},
                "fields": {"LIST": (obj[1], obj[2], '')},
                "shadow": False,
                "topLevel": parent_id == None,
            }
        else: raise ValueError()
        if   (len(obj) == 3) and (parent_id != None): 
            pass
        elif (len(obj) == 5) and (parent_id == None):
            block_data["x"] = obj[3]
            block_data["y"] = obj[4]
        else: raise ValueError()
        return cls.from_data(block_data)

    def step(self, get_comment, get_cb_mutation):
        if False:
            pass #TODO: add custom handler system here to possibly replace below
                 #      for e.g. custom block defs, prototypes, calls
        else:
            new_block = SRBlock(
                opcode    = self.opcode,
                inputs    = self.inputs, #TODO
                options   = self.fields, #TODO,
                next      = self.next,
                top_level = self.top_level,
                position  = (self.x, self.y) if self.top_level else None,
                comment   = self.comment,
                mutation  = None if self.mutation == None else self.mutation.step(),
            )
        #TODO: add custom handler system here for e.g. draw polygon block
        return new_block

class SRBlock:
    _grepr = True
    _grepr_fields = ["kws"]#["opcode", "next", "parent", "inputs", "fields", "shadow", "top_level", "x", "y", "mutation"]

    
    def __init__(self, **kwargs):
        self.kws=kwargs
        

