import typing
import json

from utility import gprint

# Variables
OPCODE_VAR_VALUE      = "data_variable_value"
OPCODE_LIST_VALUE     = "data_list_value"
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

class FLBlock:
    _grepr = True
    _grepr_fields = ["opcode", "next", "parent", "inputs", "fields", "shadow", "top_level", "x", "y", "mutation"]

    opcode: str
    next: str
    parent: str
    inputs: typing.Dict[str, (
       typing.Tuple[int, str | typing.Tuple] 
     | typing.Tuple[int, str | typing.Tuple, str | typing.Tuple]
    )]
    fields: typing.Dict[str, typing.Tuple[str, str] | typing.Tuple[str, str, str]]
    shadow: bool
    top_level: bool
    x: int | float | None
    y: int | float | None
    mutation: "FLMutation | None"

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
        self.x         = data.get("x"       , None)
        self.y         = data.get("y"       , None)
        if self.opcode == OPCODE_CB_PROTOTYPE:
            self.mutation = FLCustomBlockMutation.from_data(data["mutation"])
        elif self.opcode in ANY_OPCODE_CB_ARG:
            self.mutation = FLCustomArgumentMutation.from_data(data["mutation"])
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
                "fields": {"VARIABLE": obj[1]},
                "shadow": False,
                "topLevel": parent_id == None,
            }
        elif obj[0] == OPCODE_LIST_VALUE_NUM: # A magic value
            block_data = {
                "opcode": OPCODE_LIST_VALUE,
                "next"  : None,
                "parent": parent_id,
                "inputs": {},
                "fields": {"LIST": obj[1]},
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
        newBlockData = {
            "opcode"      : getOptimizedOpcode(opcode=blockData["opcode"]),
            "inputs"      : prepareInputs(
                data=blockData["inputs"],
                opcode=blockData["opcode"],
                commentDatas=commentDatas,
            ),
            "options"     : prepareOptions(
                data=blockData["fields"],
                opcode=blockData["opcode"],
            ),
            "_info_"      : {
                "next"    : blockData["next"],
                "topLevel": blockData["topLevel"],
            },
        }
        if not isListBlock and blockData["topLevel"] == True:
            newBlockData["_info_"]["position"] = [blockData["x"], blockData["y"]]
        if not isListBlock and "comment" in blockData:
            newBlockData["comment"] = commentDatas[blockData["comment"]]
        if newBlockData != None:
            newBlockDatas[blockId] = newBlockData
        #TODO: add custom handler system here

class FLMutation:
    _grepr = True
    _grepr_fields = ["tag_name", "children"]
    
    tag_name: str # always "mutation"
    children: typing.List[typing.Any] # always []
    
    @classmethod
    def from_data(cls, data):
        self = cls()
        self.tag_name = data["tagName" ]
        self.children = data["children"]
        return self

class FLCustomArgumentMutation(FLMutation):
    _grepr_fields = FLMutation._grepr_fields + ["color"]
    
    color: typing.Tuple[str, str, str]
    
    @classmethod
    def from_data(cls, data):
        self = super().from_data(data)
        self.color = tuple(json.loads(data["color"]))
        return self


class FLCustomBlockMutation(FLMutation):
    _grepr_fields = FLMutation._grepr_fields + ["proccode", "argument_ids", "argument_names", "argument_defaults", "warp", "returns", "edited", "optype", "color"]
    
    proccode: str
    argument_ids: typing.List[str]
    argument_names: typing.List[str]
    argument_defaults: typing.List[str]
    warp: bool
    returns: bool | None
    edited: bool # seems to always be true
    optype: str
    color: typing.Tuple[str, str, str]
    
    @classmethod
    def from_data(cls, data):
        self = super().from_data(data)
        self.proccode          = data["proccode"]
        self.argument_ids      = json.loads(data["argumentids"     ])
        self.argument_names    = json.loads(data["argumentnames"   ])
        self.argument_defaults = json.loads(data["argumentdefaults"])
        if isinstance(data["warp"], bool):
            self.warp = data["warp"]
        elif isinstance(data["warp"], str):
            self.warp = json.loads(data["warp"])
        else: raise ValueError()
        self.returns           = json.loads(data["returns"])
        self.edited            = json.loads(data["edited" ])
        self.optype            = json.loads(data["optype" ])
        self.color       = tuple(json.loads(data["color"  ]))
        return self

