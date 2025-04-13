import typing
import json

from utility import gprint

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
    mutation: typing.Dict[str, typing.Any] | None

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
        if self.opcode == "procedures_prototype":
            self.mutation = FLCustomBlockMutation.from_data(data["mutation"])
        elif self.opcode in {"argument_reporter_string_number", "argument_reporter_boolean"}:
            self.mutation = FLCustomArgumentMutation.from_data(data["mutation"])
        elif "mutation" in data:
            raise ValueError(data)
        else:
            self.mutation = None
        return self

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

