import typing

class FLBlock:
    _grepr = True

class FLComplexBlock(FLBlock):
    _grepr_fields = ["opcode", "next", "parent", "inputs", "fields", "shadow", "top_level", "x", "y", "mutation"]

    opcode: str
    next: str
    parent: str
    #inputs:
    #fields:
    shadow: bool
    top_level: bool
    x: int | float | None
    y: int | float | None
    mutation: typing.Dict[str, typing.Any] | None

    @staticmethod
    def from_data(data):
        return FLComplexBlock(data)
    
    def __init__(self, data):
        self.opcode    = data["opcode"  ]
        self.next      = data["next"    ]
        self.parent    = data["parent"  ]
        self.inputs    = data["inputs"  ]
        self.fields    = data["fields"  ]
        self.shadow    = data["shadow"  ]
        self.top_level = data["topLevel"]
        self.x         = data.get("x"       , None)
        self.y         = data.get("y"       , None)
        self.mutation  = data.get("mutation", None)

class FLSimpleBlock(FLBlock):
    pass

newBlockData = {
    "opcode"  : opcode,
    "next"    : blockData["_info_"]["next"],
    "parent"  : blockData["_info_"]["parent"],
    "inputs"  : restoreInputs(
        data=blockData["inputs"],
        opcode=opcode,
        spriteName=spriteName,
        blockData=blockData,
    ),
    "fields"  : translateOptions(
        data=blockData["options"],
        opcode=opcode,
        spriteName=spriteName,
    ),
    "shadow"  : hasShadow,
    "topLevel": blockData["_info_"]["topLevel"],
}

