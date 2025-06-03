from abc         import ABC, abstractmethod
from json        import loads
from typing      import Any, TYPE_CHECKING
from dataclasses import field

from pypenguin.utility import (
    grepr_dataclass, ValidationConfig,
    AA_TYPE, AA_HEX_COLOR,
    ThanksError, ConversionError, DeserializationError, 
)


if TYPE_CHECKING: from pypenguin.core.block_api import FIConversionAPI
from pypenguin.core.custom_block import SRCustomBlockOpcode, SRCustomBlockOptype

@grepr_dataclass(grepr_fields=["tag_name", "children"])
class FRMutation(ABC):
    """
    The first representation for the mutation of a block. Mutations hold special information, which only special blocks have
    """
    
    tag_name: str # always "mutation"
    children: list # always []

    @classmethod
    @abstractmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMutation":
        """
        Create a mutation from raw data
        
        Args:
            data: the raw data
        
        Returns:
            the mutation
        """

    def __post_init__(self) -> None:
        """
        Ensure my assumptions about mutations were correct
        
        Returns:
            None
        """
        if (self.tag_name != "mutation") or (self.children != []):
            raise ThanksError()

    @abstractmethod
    def step(self, ficapi: "FIConversionAPI") -> "SRMutation":
        """
        Convert a mutation from first into second representation
        
        Args:
            ficapi: API used to fetch information about other blocks
        
        Returns:
            the second representation of the mutation
        """

@grepr_dataclass(grepr_fields=["color"], parent_cls=FRMutation)
class FRCustomBlockArgumentMutation(FRMutation):
    """
    The first representation for the mutation of a custom block's argument reporter
    """
    
    color: tuple[str, str, str]
    _argument_name: str | None = field(init=False)
    
    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRCustomBlockArgumentMutation":
        """
        Create a custom block argument mutation from raw data
        
        Args:
            data: the raw data
        
        Returns:
            the mutation
        """
        return cls(
            tag_name = data["tagName" ],
            children = data["children"],
            color = tuple(loads(data["color"])),
        )
    
    def __post_init__(self) -> None:
        """
        Create the empty '_argument_name' attribute
        
        Returns:
            None
        """
        super().__post_init__()
        self._argument_name = None
    
    def store_argument_name(self, name: str) -> None:
        """
        Temporarily store the argument name so it can be used later when the step method is called.
        I know doing it this way isn't very great; there should be no huge consequences though
        
        Args:
            name: the argument name
        
        Returns:
            None
        """
        self._argument_name = name
    
    def step(self, ficapi: "FIConversionAPI") -> "SRCustomBlockArgumentMutation":
        """
        Convert a custom block argument mutation from first into second representation
        
        Args:
            ficapi: API used to fetch information about other blocks
        
        Returns:
            the second representation of the mutation
        """
        if getattr(self, "_argument_name", None) is None:
            raise ConversionError("Argument name must be set before SR conversion")
        return SRCustomBlockArgumentMutation(
            argument_name = self._argument_name,
            main_color        = self.color[0],
            prototype_color        = self.color[1],
            outline_color        = self.color[2],
        )

@grepr_dataclass(grepr_fields=["proccode", "argument_ids", "argument_names", "argument_defaults", "warp", "returns", "edited", "optype", "color"], parent_cls=FRMutation)
class FRCustomBlockMutation(FRMutation):
    """
    The first representation for the mutation of a custom block definition
    """
    
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
        """
        Create a custom block definition mutation from raw data
        
        Args:
            data: the raw data
        
        Returns:
            the mutation
        """
        if isinstance(data["warp"], bool):
            warp = data["warp"]
        elif isinstance(data["warp"], str):
            warp = loads(data["warp"])
        else: raise DeserializationError(f"Invalid value for warp: {data['warp']}")
        return cls(
            tag_name          = data["tagName" ],
            children          = data["children"],
            proccode          = data["proccode"],
            argument_ids      = loads(data["argumentids"     ]),
            argument_names    = loads(data["argumentnames"   ]),
            argument_defaults = loads(data["argumentdefaults"]),
            warp              = warp,
            returns           = loads(data["returns"]) if "returns" in data else False,
            edited            = loads(data["edited" ]) if "edited" in data else True,
            optype            = loads(data["optype" ]) if "optype" in data else "statement",
            color             = tuple(loads(data["color"])) if "color" in data else ("#FF6680", "#FF4D6A", "#FF3355"),
        )
    
    def step(self, ficapi: "FIConversionAPI") -> "SRCustomBlockMutation":
        """
        Convert a custom block definition mutation from first into second representation
        
        Args:
            ficapi: API used to fetch information about other blocks
        
        Returns:
            the second representation of the mutation
        """
        return SRCustomBlockMutation(
            custom_opcode     = SRCustomBlockOpcode.from_proccode_argument_names(
                proccode          = self.proccode,
                argument_names    = self.argument_names,
            ),
            no_screen_refresh = self.warp,
            optype            = SRCustomBlockOptype.from_code(self.optype),
            main_color            = self.color[0],
            prototype_color            = self.color[1],
            outline_color            = self.color[2],
        )

@grepr_dataclass(grepr_fields=["proccode", "argument_ids", "warp", "returns", "edited", "optype", "color"], parent_cls=FRMutation)
class FRCustomBlockCallMutation(FRMutation):
    """
    The first representation for the mutation of a custom block call
    """
    
    proccode: str
    argument_ids: list[str]
    warp: bool
    returns: bool | None
    edited: bool # seems to always be true
    optype: str
    color: tuple[str, str, str]
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRCustomBlockCallMutation":
        """
        Create a custom block call mutation from raw data
        
        Args:
            data: the raw data
        
        Returns:
            the mutation
        """
        if isinstance(data["warp"], bool):
            warp = data["warp"]
        elif isinstance(data["warp"], str):
            warp = loads(data["warp"])
        else: raise DeserializationError(f"Invalid value for warp: {data['warp']}")
        return cls(
            tag_name     = data["tagName" ],
            children     = data["children"],
            proccode     = data["proccode"],
            argument_ids = loads(data["argumentids"]),
            warp         = warp,
            returns      = loads(data["returns"]),
            edited       = loads(data["edited" ]),
            optype       = loads(data["optype" ]) if "optype" in data else "statement",
            color  = tuple(loads(data["color"  ])),
        )
    
    def step(self, ficapi: "FIConversionAPI") -> "SRCustomBlockCallMutation":
        """
        Convert a custom block call mutation from first into second representation
        
        Args:
            ficapi: API used to fetch information about other blocks
        
        Returns:
            the second representation of the mutation
        """
        complete_mutation = ficapi.get_cb_mutation(self.proccode) # Get complete mutation
        return SRCustomBlockCallMutation(
            custom_opcode      = SRCustomBlockOpcode.from_proccode_argument_names(
                proccode          = self.proccode,
                argument_names    = complete_mutation.argument_names,
            ),
        )

@grepr_dataclass(grepr_fields=["has_next"], parent_cls=FRMutation)
class FRStopScriptMutation(FRMutation):
    """
    The first representation for the mutation of a stop script mutation
    """
    
    has_next: bool
    
    @classmethod
    def from_data(cls, data: dict[str, bool]) -> "FRStopScriptMutation":
        """
        Create a mutation for the "stop [this script v]" block from raw data
        
        Args:
            data: the raw data
        
        Returns:
            the mutation
        """
        return cls(
            tag_name = data["tagName" ],
            children = data["children"],
            has_next = loads(data["hasnext"]),
        )
    
    def step(self, ficapi: "FIConversionAPI") -> "SRStopScriptMutation":
        """
        Convert a stop script mutation from first into second representation
        
        Args:
            ficapi: API used to fetch information about other blocks
        
        Returns:
            the second representation of the mutation
        """
        return SRStopScriptMutation(
            is_ending_statement = not(self.has_next),
        )


@grepr_dataclass(grepr_fields=[])
class SRMutation(ABC):
    """
    The second representation for the mutation of a block. Mutations hold special information, which only special blocks have. This representation is much more user friendly then the first representation
    """

    @abstractmethod
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure the mutation is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRMutation is invalid
        """

@grepr_dataclass(grepr_fields=["argument_name", "main_color", "prototype_color", "outline_color"], parent_cls=SRMutation)
class SRCustomBlockArgumentMutation(SRMutation):
    """
    The second representation for the mutation of a custom block argument reporter
    """
    
    argument_name: str
    # hex format
    # what each color does, is unknown (for now)
    main_color: str
    prototype_color: str
    outline_color: str

    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure the custom block argument mutation is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRCustomBlockArgumentMutation is invalid
        """
        AA_TYPE(self, path, "argument_name", str)
        AA_HEX_COLOR(self, path, "main_color")
        AA_HEX_COLOR(self, path, "prototype_color")
        AA_HEX_COLOR(self, path, "outline_color")
    
@grepr_dataclass(grepr_fields=["custom_opcode", "no_screen_refresh", "optype", "main_color", "prototype_color", "outline_color"], parent_cls=SRMutation)
class SRCustomBlockMutation(SRMutation):
    """
    The second representation for the mutation of a custom block definition
    """
    
    custom_opcode: "SRCustomBlockOpcode"
    no_screen_refresh: bool
    optype: SRCustomBlockOptype
    
    # hex format
    # what each color does, is unknown (for now)
    main_color: str
    prototype_color: str
    outline_color: str
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure the custom block definition mutation is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRCustomBlockMutation is invalid
        """
        AA_TYPE(self, path, "custom_opcode", SRCustomBlockOpcode)
        AA_TYPE(self, path, "no_screen_refresh", bool)
        AA_TYPE(self, path, "optype", SRCustomBlockOptype)
        AA_HEX_COLOR(self, path, "main_color")
        AA_HEX_COLOR(self, path, "prototype_color")
        AA_HEX_COLOR(self, path, "outline_color")

        self.custom_opcode.validate(path+["custom_opcode"], config)

@grepr_dataclass(grepr_fields=["custom_opcode"], parent_cls=SRMutation)    
class SRCustomBlockCallMutation(SRMutation):
    """
    The second representation for the mutation of a custom block call
    """
    
    custom_opcode: "SRCustomBlockOpcode"
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure the custom block call mutation is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRCustomBlockCallMutation is invalid
        """
        AA_TYPE(self, path, "custom_opcode", SRCustomBlockOpcode)

        self.custom_opcode.validate(path+["custom_opcode"], config)

@grepr_dataclass(grepr_fields=["is_ending_statement"], parent_cls=SRMutation)
class SRStopScriptMutation(SRMutation):
    """
    The second representation for the mutation of a "stop [this script v] block
    """
    
    is_ending_statement: bool

    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure the stop script mutation is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRStopScriptMutation is invalid
        """
        AA_TYPE(self, path, "is_ending_statement", bool)


__all__ = [
    "FRMutation", "FRCustomBlockArgumentMutation", 
    "FRCustomBlockMutation", "FRCustomBlockCallMutation", "FRStopScriptMutation",
    "SRMutation", "SRCustomBlockArgumentMutation", 
    "SRCustomBlockMutation", "SRCustomBlockCallMutation", "SRStopScriptMutation",
]

