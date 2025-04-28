from json        import loads
from abc         import ABC, abstractmethod
from typing      import Any
from dataclasses import dataclass

from utility import GreprClass, ThanksError

from core.fr_to_tr_api import FRtoTRAPI
from core.custom_block import SRCustomBlockOpcode, SRCustomBlockOptype

@dataclass(repr=False)
class FRMutation(GreprClass, ABC):
    _grepr = True
    _grepr_fields = ["tag_name", "children"]
    
    tag_name: str # always "mutation"
    children: list # always []

    def __post_init__(self):
        if (self.tag_name != "mutation") or (self.children != []):
            raise ThanksError()

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMutation":
        return cls(
            tag_name = data["tagName" ],
            children = data["children"],
        )

    @abstractmethod
    def step(self, block_api: FRtoTRAPI) -> "SRMutation": pass

@dataclass(repr=False)
class FRCustomBlockArgumentMutation(FRMutation):
    _grepr_fields = FRMutation._grepr_fields + ["color"]
    
    color: tuple[str, str, str]
    
    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRCustomBlockArgumentMutation":
        return cls(
            tag_name = data["tagName" ],
            children = data["children"],
            color = tuple(loads(data["color"])),
        )
    
    def store_argument_name(self, name: str) -> None:
        self._argument_name = name
    
    def step(self, block_api: FRtoTRAPI) -> "SRCustomBlockArgumentMutation":
        if getattr(self, "_argument_name", None) is None:
            raise Exception("Argument name must be set for stepping to be possible.")
        return SRCustomBlockArgumentMutation(
            argument_name = self._argument_name,
            color1        = self.color[0],
            color2        = self.color[1],
            color3        = self.color[2],
        )

@dataclass(repr=False)
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
    def from_data(cls, data: dict[str, Any]) -> "FRCustomBlockMutation":
        if isinstance(data["warp"], bool):
            warp = data["warp"]
        elif isinstance(data["warp"], str):
            warp = loads(data["warp"])
        else: raise ValueError()
        return cls(
            tag_name          = data["tagName" ],
            children          = data["children"],
            proccode          = data["proccode"],
            argument_ids      = loads(data["argumentids"     ]),
            argument_names    = loads(data["argumentnames"   ]),
            argument_defaults = loads(data["argumentdefaults"]),
            warp              = warp,
            returns           = loads(data["returns"]),
            edited            = loads(data["edited" ]),
            optype            = loads(data["optype" ]) if "optype" in data else "statement",
            color       = tuple(loads(data["color"  ])),
        )
    
    def step(self, block_api: FRtoTRAPI) -> "SRCustomBlockMutation":
        return SRCustomBlockMutation(
            custom_opcode     = SRCustomBlockOpcode.from_proccode_names_defaults(
                proccode          = self.proccode,
                argument_names    = self.argument_names,
                argument_defaults = self.argument_defaults,
            ),
            no_screen_refresh = self.warp,
            optype            = SRCustomBlockOptype.from_string(self.optype),
            color1            = self.color[0],
            color2            = self.color[1],
            color3            = self.color[2],
        )

@dataclass(repr=False)
class FRCustomCallMutation(FRMutation):
    _grepr_fields = FRMutation._grepr_fields + ["proccode", "argument_ids", "warp", "returns", "edited", "optype", "color"]
    
    proccode: str
    argument_ids: list[str]
    warp: bool
    returns: bool | None
    edited: bool # seems to always be true
    optype: str
    color: tuple[str, str, str]
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRCustomCallMutation":
        if isinstance(data["warp"], bool):
            warp = data["warp"]
        elif isinstance(data["warp"], str):
            warp = loads(data["warp"])
        else: raise ValueError()
        return cls(
            tag_name     = data["tagName" ],
            children     = data["children"],
            proccode     = data["proccode"],
            argument_ids = loads(data["argumentids"     ]),
            warp         = warp,
            returns      = loads(data["returns"]),
            edited       = loads(data["edited" ]),
            optype       = loads(data["optype" ]) if "optype" in data else "statement",
            color  = tuple(loads(data["color"  ])),
        )
    
    def step(self, block_api: FRtoTRAPI) -> "SRCustomBlockCallMutation":
        complete_mutation = block_api.get_cb_mutation(self.proccode) # Get complete mutation
        return SRCustomBlockCallMutation(
            custom_opcode      = SRCustomBlockOpcode.from_proccode_names_defaults(
                proccode          = self.proccode,
                argument_names    = complete_mutation.argument_names,
                argument_defaults = complete_mutation.argument_defaults,
            ),
        )

@dataclass(repr=False)
class FRStopScriptMutation(FRMutation):
    _grepr_fields = FRMutation._grepr_fields + ["has_next"]
    
    has_next: bool
    
    @classmethod
    def from_data(cls, data: dict[str, bool]) -> "FRStopScriptMutation":
        return cls(
            tag_name = data["tagName" ],
            children = data["children"],
            has_next = loads(data["hasnext"]),
        )
    
    def step(self, block_api: FRtoTRAPI) -> "SRStopScriptMutation":
        return SRStopScriptMutation(
            is_ending_statement = not(self.has_next),
        )

@dataclass(repr=False)
class SRMutation(GreprClass):
    _grepr = True
    _grepr_fields = []

@dataclass(repr=False)
class SRCustomBlockArgumentMutation(SRMutation):
    _grepr_fields = FRMutation._grepr_fields + ["argument_name", "color1", "color2", "color3"]
    
    argument_name: str
    # hex format
    # what each color does, is unknown (for now)
    color1: str
    color2: str
    color3: str
    
@dataclass(repr=False)
class SRCustomBlockMutation(SRMutation):
    _grepr_fields = SRMutation._grepr_fields + ["custom_opcode", "no_screen_refresh", "optype", "color1", "color2", "color3"]
    
    custom_opcode: "SRCustomBlockOpcode"
    no_screen_refresh: bool
    optype: SRCustomBlockOptype
    
    # hex format
    # what each color does, is unknown (for now)
    color1: str
    color2: str
    color3: str

@dataclass(repr=False)    
class SRCustomBlockCallMutation(SRMutation):
    _grepr_fields = SRMutation._grepr_fields + ["custom_opcode"]
    
    custom_opcode: "SRCustomBlockOpcode"

@dataclass(repr=False)
class SRStopScriptMutation(SRMutation):
    _grepr_fields = SRMutation._grepr_fields + ["is_ending_statement"]
    
    is_ending_statement: bool

