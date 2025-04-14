from typing import Callable

from utility               import gprint
from block_mutation        import FRMutation, FRCustomBlockMutation, FRCustomArgumentMutation
from block_mutation        import SRMutation
from block_opcodes         import *
from customization_handler import CustomizationHandler, CEventType

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

    def step(self, ch: CustomizationHandler, manager, get_comment: Callable, get_cb_mutation: Callable):
        instead_event = ch.get_event(
            event_type=CEventType.INSTEAD_FR_TO_SR,
            opcode=self.opcode,
        )
        if instead_event is None:
            new_block = SRBlock(
                opcode       = self.opcode,
                inputs       = self.inputs, #TODO
                dropdowns    = self.fields, #TODO,
                position     = (self.x, self.y) if self.top_level else None,
                comment      = self.comment,
                mutation     = None if self.mutation is None else self.mutation.step(),
                next         = self.next,
                is_top_level = self.top_level,
            )
        else:
            new_block = instead_event.call(manager=manager, block=self)
            pass #TODO: add custom handler system here to possibly replace below
                 #      for e.g. custom block defs, prototypes, calls
        #TODO: add custom handler system here for e.g. draw polygon block
        return new_block

class SRBlock:
    _grepr = True
    _grepr_fields = ["opcode", "inputs", "dropdowns", "position", "comment", "mutation", "next", "top_level"]
    
    opcode: str
    #inputs: dict[str, ?]
    #dropdowns: dict[str, ?]
    position: tuple[int | float, int | float] | None
    comment: str | None # a comment id
    mutation: "SRMutation | None"
    next: str | None
    is_top_level: bool

    def __init__(self, 
        opcode: str,
        inputs,#: dict[str, ?],
        dropdowns,#: dict[str, ?],
        position: tuple[int | float, int | float] | None,
        comment: str | None, # a comment id
        mutation: "SRMutation | None",
        next: str | None,
        is_top_level: bool,
    ):
        self.opcode       = opcode
        self.inputs       = inputs
        self.dropdowns    = dropdowns
        self.position     = position
        self.comment      = comment
        self.mutation     = mutation
        self.next         = next
        self.is_top_level = is_top_level
        

