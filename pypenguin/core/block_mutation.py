from abc         import ABC, abstractmethod
from copy        import deepcopy
from json        import loads
from typing      import Any, TYPE_CHECKING
from dataclasses import field

from pypenguin.important_consts import SHA256_SEC_MAIN_ARGUMENT_NAME
from pypenguin.utility          import (
    grepr_dataclass, string_to_sha256, gdumps,
    AA_TYPE, AA_HEX_COLOR,
    PP_ThanksError, PP_ConversionError, PP_DeserializationError, 
)


if TYPE_CHECKING: from pypenguin.core.block_interface import FirstToInterIF, InterToFirstIF
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
        Create a FRMutation from json data
        
        Args:
            data: the json data
        
        Returns:
            the FRMutation
        """

    @abstractmethod
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRMutation into json data
        
        Returns:
            the json data
        """

    def __post_init__(self) -> None:
        """
        Ensure my assumptions about mutations were correct
        
        Returns:
            None
        """
        if (self.tag_name != "mutation") or (self.children != []):
            raise PP_ThanksError()

    @abstractmethod
    def to_second(self, fti_if: "FirstToInterIF") -> "SRMutation":
        """
        Convert a FRMutation into a SRMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the SRMutation
        """

@grepr_dataclass(grepr_fields=["color"])
class FRCustomBlockArgumentMutation(FRMutation):
    """
    The first representation for the mutation of a custom block's argument reporter
    """
    
    color: tuple[str, str, str]
    _argument_name: str | None = field(init=False)
    
    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRCustomBlockArgumentMutation":
        """
        Create a FRCustomBlockArgumentMutation from json data
        
        Args:
            data: the json data
        
        Returns:
            the FRCustomBlockArgumentMutation
        """
        return cls(
            tag_name = data["tagName" ],
            children = data["children"],
            color    = tuple(loads(data["color"])),
        )

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRCustomBlockArgumentMutation into json data
        
        Returns:
            the json data
        """
        return {
            "tagName" : self.tag_name,
            "children": deepcopy(self.children),
            "color"   : gdumps(self.color), # automatically converts to list
        }
    
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
    
    def to_second(self, fti_if: "FirstToInterIF") -> "SRCustomBlockArgumentMutation":
        """
        Convert a FRCustomBlockArgumentMutation into a SRCustomBlockArgumentMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the SRCustomBlockArgumentMutation
        """
        if getattr(self, "_argument_name", None) is None:
            raise PP_ConversionError("Argument name must be set before SR conversion")
        return SRCustomBlockArgumentMutation(
            argument_name   = self._argument_name,
            main_color      = self.color[0],
            prototype_color = self.color[1],
            outline_color   = self.color[2],
        )

@grepr_dataclass(grepr_fields=["proccode", "argument_ids", "argument_names", "argument_defaults", "warp", "returns", "edited", "optype", "color"])
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
        Create a FRCustomBlockMutation from json data
        
        Args:
            data: the json data
        
        Returns:
            the FRCustomBlockMutation
        """
        if isinstance(data["warp"], bool):
            warp = data["warp"]
        elif isinstance(data["warp"], str):
            warp = loads(data["warp"])
        else: raise PP_DeserializationError(f"Invalid value for warp: {data['warp']}")
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
    
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRCustomBlockMutation into json data
        
        Returns:
            the json data
        """
        return {
            "tagName"         : self.tag_name,
            "children"        : deepcopy(self.children),
            "proccode"        : self.proccode,
            "argumentids"     : gdumps(self.argument_ids),
            "argumentnames"   : gdumps(self.argument_names),
            "argumentdefaults": gdumps(self.argument_defaults),
            "warp"            : gdumps(self.warp), # seems to be a str usually
            "returns"         : gdumps(self.returns),
            "edited"          : gdumps(self.edited),
            "optype"          : gdumps(self.optype),
            "color"           : gdumps(self.color), # automatically converts to list
        }
        
    def to_second(self, fti_if: "FirstToInterIF") -> "SRCustomBlockMutation":
        """
        Convert a FRCustomBlockMutation into a SRCustomBlockMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the SRCustomBlockMutation
        """
        return SRCustomBlockMutation(
            custom_opcode     = SRCustomBlockOpcode.from_proccode_argument_names(
                proccode          = self.proccode,
                argument_names    = self.argument_names,
            ),
            no_screen_refresh = self.warp,
            optype            = SRCustomBlockOptype.from_code(self.optype),
            main_color        = self.color[0],
            prototype_color   = self.color[1],
            outline_color     = self.color[2],
        )

@grepr_dataclass(grepr_fields=["proccode", "argument_ids", "warp", "returns", "edited", "optype", "color"])
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
        Create a FRCustomBlockCallMutation from json data
        
        Args:
            data: the json data
        
        Returns:
            the FRCustomBlockCallMutation
        """
        if isinstance(data["warp"], bool):
            warp = data["warp"]
        elif isinstance(data["warp"], str):
            warp = loads(data["warp"])
        else: raise PP_DeserializationError(f"Invalid value for warp: {data['warp']}")
        return cls(
            tag_name     = data["tagName" ],
            children     = data["children"],
            proccode     = data["proccode"],
            argument_ids = loads(data["argumentids"]),
            warp         = warp,
            returns      = loads(data["returns"]),
            edited       = loads(data["edited" ]),
            optype       = loads(data["optype" ]) if "optype" in data else "statement",
            color        = tuple(loads(data["color"])),
        )
    
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRCustomBlockCallMutation into json data
        
        Returns:
            the json data
        """
        return {
            "tagName"    : self.tag_name,
            "children"   : deepcopy(self.children),
            "proccode"   : self.proccode,
            "argumentids": gdumps(self.argument_ids),
            "warp"       : gdumps(self.warp), # seems to be a str usually
            "returns"    : gdumps(self.returns),
            "edited"     : gdumps(self.edited),
            "optype"     : gdumps(self.optype),
            "color"      : gdumps(self.color), # automatically converts to list
        }
        
    def to_second(self, fti_if: "FirstToInterIF") -> "SRCustomBlockCallMutation":
        """
        Convert a FRCustomBlockCallMutation into a SRCustomBlockCallMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the SRCustomBlockCallMutation
        """
        complete_mutation = fti_if.get_cb_mutation(self.proccode) # Get complete mutation
        return SRCustomBlockCallMutation(
            custom_opcode      = SRCustomBlockOpcode.from_proccode_argument_names(
                proccode       = self.proccode,
                argument_names = complete_mutation.argument_names,
            ),
        )

@grepr_dataclass(grepr_fields=["has_next"])
class FRStopScriptMutation(FRMutation):
    """
    The first representation for the mutation of a stop script mutation
    """
    
    has_next: bool
    
    @classmethod
    def from_data(cls, data: dict[str, bool]) -> "FRStopScriptMutation":
        """
        Create a FRStopScriptMutation(for the "stop [this script v]" block) from json data
        
        Args:
            data: the json data
        
        Returns:
            the FRStopScriptMutation
        """
        return cls(
            tag_name = data["tagName" ],
            children = data["children"],
            has_next = loads(data["hasnext"]),
        )

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRStopScriptMutation into json data
        
        Returns:
            the json data
        """
        return {
            "tagName" : self.tag_name,
            "children": deepcopy(self.children),
            "hasnext" : gdumps(self.has_next),
        }
   
    def to_second(self, fti_if: "FirstToInterIF") -> "SRStopScriptMutation":
        """
        Convert a FRStopScriptMutation into a SRStopScriptMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the SRStopScriptMutation
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
    def validate(self, path: list) -> None:
        """
        Ensure the SRMutation is valid, raise PP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            PP_ValidationError: if the SRMutation is invalid
        """

    @abstractmethod
    def to_first(self, itf_if: "InterToFirstIF") -> "FRMutation":
        """
        Convert a SRMutation into a FRMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the FRMutation
        """

@grepr_dataclass(grepr_fields=["argument_name", "main_color", "prototype_color", "outline_color"])
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

    def validate(self, path: list) -> None:
        """
        Ensure the SRCustomBlockArgumentMutation is valid, raise PP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            PP_ValidationError: if the SRCustomBlockArgumentMutation is invalid
        """
        AA_TYPE(self, path, "argument_name", str)
        AA_HEX_COLOR(self, path, "main_color")
        AA_HEX_COLOR(self, path, "prototype_color")
        AA_HEX_COLOR(self, path, "outline_color")
    
    def to_first(self, itf_if: "InterToFirstIF") -> FRCustomBlockArgumentMutation:
        """
        Convert a SRCustomBlockArgumentMutation into a FRCustomBlockArgumentMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the FRCustomBlockArgumentMutation
        """
        return FRCustomBlockArgumentMutation(
            tag_name = "mutation",
            children = [],
            color    = (self.main_color, self.prototype_color, self.outline_color),
        )
    
@grepr_dataclass(grepr_fields=["custom_opcode", "no_screen_refresh", "optype", "main_color", "prototype_color", "outline_color"])
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
    
    def validate(self, path: list) -> None:
        """
        Ensure the SRCustomBlockMutation is valid, raise PP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            PP_ValidationError: if the SRCustomBlockMutation is invalid
        """
        AA_TYPE(self, path, "custom_opcode", SRCustomBlockOpcode)
        AA_TYPE(self, path, "no_screen_refresh", bool)
        AA_TYPE(self, path, "optype", SRCustomBlockOptype)
        AA_HEX_COLOR(self, path, "main_color")
        AA_HEX_COLOR(self, path, "prototype_color")
        AA_HEX_COLOR(self, path, "outline_color")

        self.custom_opcode.validate(path+["custom_opcode"])

    
    def to_first(self, itf_if: "InterToFirstIF") -> FRCustomBlockMutation:
        """
        Convert a SRCustomBlockMutation into a FRCustomBlockMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the FRCustomBlockMutation
        """
        (proccode, argument_names, argument_defaults
        ) = self.custom_opcode.to_proccode_argument_names_defaults()
        argument_ids = [
            string_to_sha256(argument_name, secondary=SHA256_SEC_MAIN_ARGUMENT_NAME) 
            for argument_name in argument_names
        ]
        if self.optype is SRCustomBlockOptype.ENDING_STATEMENT:
            returns = None
        else:
            returns = self.optype.is_reporter()
        return FRCustomBlockMutation(
            tag_name          = "mutation",
            children          = [],
            proccode          = proccode,
            argument_ids      = argument_ids,
            argument_names    = argument_names,
            argument_defaults = argument_defaults,
            warp              = self.no_screen_refresh,
            returns           = returns,
            edited            = True, # seems to always be true
            optype            = self.optype.to_code(),
            color             = (self.main_color, self.prototype_color, self.outline_color),
        )

@grepr_dataclass(grepr_fields=["custom_opcode"])    
class SRCustomBlockCallMutation(SRMutation):
    """
    The second representation for the mutation of a custom block call
    """
    
    custom_opcode: "SRCustomBlockOpcode"
    
    def validate(self, path: list) -> None:
        """
        Ensure the SRCustomBlockCallMutation is valid, raise PP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            PP_ValidationError: if the SRCustomBlockCallMutation is invalid
        """
        AA_TYPE(self, path, "custom_opcode", SRCustomBlockOpcode)

        self.custom_opcode.validate(path+["custom_opcode"])
    
    def to_first(self, itf_if: "InterToFirstIF") -> FRCustomBlockCallMutation:
        """
        Convert a SRCustomBlockCallMutation into a FRCustomBlockCallMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the FRCustomBlockCallMutation
        """
        complete_mutation = itf_if.get_sr_cb_mutation(self.custom_opcode)
        proccode, argument_names, _ = self.custom_opcode.to_proccode_argument_names_defaults()
        argument_ids = [
            string_to_sha256(argument_name, secondary=SHA256_SEC_MAIN_ARGUMENT_NAME) 
            for argument_name in argument_names
        ]
        if complete_mutation.optype is SRCustomBlockOptype.ENDING_STATEMENT:
            returns = None
        else:
            returns = complete_mutation.optype.is_reporter()
        return FRCustomBlockCallMutation(
            tag_name     = "mutation",
            children     = [],
            proccode     = proccode,
            argument_ids = argument_ids,
            warp         = complete_mutation.no_screen_refresh,
            returns      = returns,
            edited       = True, # seems to always be true
            optype       = complete_mutation.optype.to_code(),
            color        = (
                complete_mutation.main_color, 
                complete_mutation.prototype_color, 
                complete_mutation.outline_color,
            ),
        )

@grepr_dataclass(grepr_fields=["is_ending_statement"])
class SRStopScriptMutation(SRMutation):
    """
    The second representation for the mutation of a "stop [this script v] block
    """
    
    is_ending_statement: bool

    def validate(self, path: list) -> None:
        """
        Ensure the SRStopScriptMutation is valid, raise PP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            PP_ValidationError: if the SRStopScriptMutation is invalid
        """
        AA_TYPE(self, path, "is_ending_statement", bool)

    def to_first(self, itf_if: "InterToFirstIF") -> FRStopScriptMutation:
        """
        Convert a SRStopScriptMutation into a FRStopScriptMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the FRStopScriptMutation
        """
        return FRStopScriptMutation(
            tag_name = "mutation",
            children = [],
            has_next = not(self.is_ending_statement),
        )


__all__ = [
    "FRMutation", "FRCustomBlockArgumentMutation", 
    "FRCustomBlockMutation", "FRCustomBlockCallMutation", "FRStopScriptMutation",
    "SRMutation", "SRCustomBlockArgumentMutation", 
    "SRCustomBlockMutation", "SRCustomBlockCallMutation", "SRStopScriptMutation",
]

