import json

from custom_block import SRCustomOpcode

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
    color: tuple[str, str, str]
    
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
    
    def step(self):
        return SRCustomBlockMutation(
            custom_opcode     = SRCustomOpcode(
                proccode          = self.proccode,
                argument_ids      = self.argument_ids,
                argument_names    = self.argument_names,
                argument_defaults = self.argument_defaults,
            ),
            no_screen_refresh = self.warp,
            returns           = self.returns,
            optype            = self.optype,
            color1            = self.color[0],
            color2            = self.color[1],
            color3            = self.color[2],
        )


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
    _grepr_fields = FRMutation._grepr_fields + ["proccode", "argument_ids", "argument_names", "argument_defaults", "no_screen_refresh", "returns", "edited", "optype", "color1", "color2", "color3"]
    
    custom_opcode: "SRCustomOpcode"
    argument_ids: list[str]
    argument_names: list[str]
    argument_defaults: list[str]
    no_screen_refresh: bool
    returns: bool | None
    optype: str
    
    # hex format
    # what each color does, is unknown (for now)
    color1: str
    color2: str
    color3: str
    
    def __init__(self,
        custom_opcode: "SRCustomOpcode",
        no_screen_refresh: bool,
        returns: bool | None,
        optype: str,
        color1: str,
        color2: str,
        color3: str,
    ):
        self.custom_opcode     = custom_opcode
        self.no_screen_refresh = no_screen_refresh
        self.returns           = returns
        self.optype            = optype
        self.color1            = color1
        self.color2            = color2
        self.color3            = color3

