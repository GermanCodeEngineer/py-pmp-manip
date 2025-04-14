from typing import any
import json

class FRMutation:
    _grepr = True
    _grepr_fields = ["tag_name", "children"]
    
    tag_name: str # always "mutation"
    children: list # always []
    
    @classmethod
    def from_data(cls, data):
        self = cls()
        self.tag_name = data["tagName" ]
        self.children = data["children"]
        return self

class FRCustomArgumentMutation(FRMutation):
    _grepr_fields = FRMutation._grepr_fields + ["color"]
    
    color: tuple[str, str, str]
    
    @classmethod
    def from_data(cls, data):
        self = super().from_data(data)
        self.color = tuple(json.loads(data["color"]))
        return self
    
    def step(self):
        return SRCustomArgumentMutation(
          color1 = self.color[0],
          color2 = self.color[1],
          color3 = self.color[2],
        )


class FRCustomBlockMutation(FRMutation):
    _grepr_fields = FRMutation._grepr_fields + ["proccode", "argument_ids", "argument_names", "argument_defaults", "warp", "returns", "edited", "optype", "color"]
    
    proccode: str
    argument_ids: list[str]
    argument_names: list[str]
    argument_defaults: list[str]
    warp: bool
    returns: bool | None
    edited: bool # seems to always be true
    optype: str
    
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


class SRMutation:
    _grepr = True
    _grepr_fields = []

class SRCustomArgumentMutation(SRMutation):
    _grepr_fields = FRMutation._grepr_fields + ["color1", "color2", "color3"]
    
    # hex format
    # what each color does, is unknown (for now)
    color1: str
    color2: str
    color3: str
    
    def __init__(self, color1: str, color2: str, color3: str):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3

# TODO: implement this correctly, dont just copy everything from FR
class SRCustomBlockMutation(SRMutation):
    _grepr_fields = FRMutation._grepr_fields + ["proccode", "argument_ids", "argument_names", "argument_defaults", "warp", "returns", "edited", "optype", "color1", "color2", "color3"]
    
    proccode: str
    argument_ids: list[str]
    argument_names: list[str]
    argument_defaults: list[str]
    warp: bool
    returns: bool | None
    edited: bool # seems to always be true
    optype: str
    
    # hex format
    # what each color does, is unknown (for now)
    color1: str
    color2: str
    color3: str
    
    def __init__(self,
        proccode: str,
        argument_ids: list[str],
        argument_names: list[str],
        argument_defaults: list[str],
        warp: bool,
        returns: bool | None,
        edited: bool,
        optype: str,
        color1: str,
        color2: str,
        color3: str,
    ):
        self.proccode          = proccode
        self.argument_ids      = argument_ids
        self.argument_names    = argument_names
        self.argument_defaults = argument_defaults
        self.warp              = warp
        self.returns           = returns
        self.edited            = edited
        self.optype            = optype
        self.color1            = color1
        self.color2            = color2
        self.color3            = color3


