from abc         import ABC, abstractmethod
from copy        import deepcopy
from dataclasses import field
from json        import loads
from typing      import Any, ClassVar, NoReturn, TYPE_CHECKING

from pmp_manip.important_consts import SHA256_SEC_MAIN_ARGUMENT_NAME
from pmp_manip.utility          import (
    grepr_dataclass, string_to_sha256, gdumps,
    AA_TYPE, AA_HEX_COLOR,
    MANIP_ThanksError, MANIP_ConversionError, MANIP_DeserializationError, 
)


if TYPE_CHECKING: from pmp_manip.core.block_interface import FirstToInterIF, InterToFirstIF
from pmp_manip.core.custom_block import SRCustomBlockOpcode, SRCustomBlockOptype

@grepr_dataclass(grepr_fields=["tag_name", "children"], init=False, forbid_init_only_subcls=True)
class FRMutation(ABC):
    """
    The first representation for the mutation of a block. Mutations hold special information, which only special blocks have
    """
    
    _subclasses_info_: ClassVar[dict[type["FRMutation"], tuple[set[str], set[str]]]] = {}
    # stores classes required and optional properties

    tag_name: str # always "mutation"
    children: list # always []

    def __init_subclass__(cls, *, required_properties: set[str], optional_properties: set[str]=set(), **kwargs):
        """
        Take note of a mutation subclasses required and optional properties

        Args:
            required_properties: the set of properties, a subclass instance's json data dict must contain
            optional_properties: the set of properties, a subclass instance's json data dict might contain
        """
        super().__init_subclass__(**kwargs)
        subclass_info = ({"tagName", "children"} | required_properties, optional_properties)
        FRMutation._subclasses_info_[cls] = subclass_info
    

    @classmethod
    def _find_from_data_subclasses(cls, data: dict[str, Any]) -> list[type["FRMutation"]]:
        """
        Compares the keys of the provided data with the properties of all subclasses and returns the matching ones
        
        Args:
            data: the json data
        """
        data_properties = set(data.keys())
        matches = []
        for subcls, subcls_info in FRMutation._subclasses_info_.items():
            required_properties, optional_properties = subcls_info
            if not required_properties.issubset(data_properties):
                continue
            unrecognized_properties = (data_properties - required_properties)
            if not unrecognized_properties.issubset(optional_properties):
                continue
            matches.append(subcls)
        return matches

    @classmethod
    @abstractmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMutation":
        """
        Create a FRMutation from json data. 
        Automatically chooses the right subclass and creates an instance using its from_data method
        
        Args:
            data: the json data

        Raises:
            MANIP_DeserializationError: if no or mulitple matching block mutation subclasses are found
        """
        subclass_matches = FRMutation._find_from_data_subclasses(data)
        if   len(subclass_matches) >= 2:
            subclasses_string = ", ".join([cls.__name__ for cls in subclass_matches])
            raise MANIP_DeserializationError(f"Found multiple matching block mutation subclasses"
                f"({subclasses_string}) for data: {data}")
        elif len(subclass_matches) == 1:
            return subclass_matches[0].from_data(data)
        elif len(subclass_matches) == 0:
            raise MANIP_DeserializationError(f"Could not find matching block mutation subclass for data: {data}")

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
            raise MANIP_ThanksError()

    @abstractmethod
    def to_second(self, fti_if: "FirstToInterIF") -> "SRMutation":
        """
        Convert a FRMutation into a SRMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        
        Returns:
            the SRMutation
        """

@grepr_dataclass(grepr_fields=["color",  "warp", "edited", "has_next"])
class FRCustomBlockArgumentMutation(FRMutation, required_properties={"color"}, optional_properties={"warp", "edited", "hasnext"}):
    """
    The first representation for the mutation of a custom block's argument reporter
    """
    
    color: tuple[str, str, str]
    warp: bool = False # should not exist and if present seems to be False
    edited: bool = False # should not exist and if present seems to be False
    has_next: bool = False # should not exist and if present seems to be False

    _argument_name: str | None = field(init=False)
    
    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRCustomBlockArgumentMutation":
        """
        Create a FRCustomBlockArgumentMutation from json data
        
        Args:
            data: the json data
        
        Returns:
            the FRCustomBlockArgumentMutation
        
        Raises:
            MANIP_DeserializationError: if 'warp', 'edited' or 'hasnext' is neither False nor unset
        """
        warp     = data.get("warp"   , False)
        edited   = data.get("edited" , False)
        has_next = data.get("hasnext", False)
        
        if   warp == False: pass
        elif warp == gdumps(False): warp = False
        else: raise MANIP_DeserializationError(f"Invalid value for 'warp', expected it to either not be set or to be False: {warp!r}")
        if   edited == False: pass
        elif edited == gdumps(False): edited = False
        else: raise MANIP_DeserializationError(f"Invalid value for 'edited', expected it to either not be set or to be False: {edited!r}")
        if   has_next == False: pass
        elif has_next == gdumps(False): has_next = False
        else: raise MANIP_DeserializationError(f"Invalid value for 'hasnext', expected it to either not be set or to be False: {has_next!r}")
        
        return cls(
            tag_name = data["tagName" ],
            children = deepcopy(data["children"]),
            color    = tuple(loads(data["color"])),
            
            warp     = warp,
            edited   = edited,
            has_next = has_next,
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
        I know doing it this way is not very great; there should be no huge consequences though
        
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
            raise MANIP_ConversionError("Argument name must be set before SR conversion")
        return SRCustomBlockArgumentMutation(
            argument_name   = self._argument_name,
            main_color      = self.color[0],
            prototype_color = self.color[1],
            outline_color   = self.color[2],
        )

@grepr_dataclass(grepr_fields=["proccode", "argument_ids", "argument_names", "argument_defaults", "warp", "returns", "edited", "optype", "color"])
class FRCustomBlockMutation(FRMutation, 
        required_properties={"proccode", "argumentids", "argumentnames", "argumentdefaults", "warp"},
        optional_properties={"returns", "edited", "optype", "color"},
    ):
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
        else: raise MANIP_DeserializationError(f"Invalid value for 'warp': {data['warp']}")
        return cls(
            tag_name          = data["tagName" ],
            children          = deepcopy(data["children"]),
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
class FRCustomBlockCallMutation(FRMutation, 
        required_properties={"proccode", "argumentids", "warp"},
        optional_properties={"returns", "edited", "optype", "color"},
    ):
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
        else: raise MANIP_DeserializationError(f"Invalid value for 'warp': {data['warp']}")
        return cls(
            tag_name     = data["tagName" ],
            children     = deepcopy(data["children"]),
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
class FRStopScriptMutation(FRMutation, required_properties={"hasnext"}):
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
            children = deepcopy(data["children"]),
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
   
    def to_second(self, fti_if: "FirstToInterIF") -> NoReturn:
        """
        A second representation of a stop script mutation does not exist. 
        It would just store alredy known information in a second place.
        """
        raise NotImplementedError("A second representation of a stop script mutation does not exist. It is not needed for a IRBlock or SRBlock")


@grepr_dataclass(grepr_fields=[], init=False, forbid_init_only_subcls=True)
class SRMutation(ABC):
    """
    The second representation for the mutation of a block. Mutations hold special information, which only special blocks have. This representation is much more user friendly then the first representation
    """

    @abstractmethod
    def validate(self, path: list) -> None:
        """
        Ensure the SRMutation is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRMutation is invalid
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
        Ensure the SRCustomBlockArgumentMutation is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRCustomBlockArgumentMutation is invalid
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
        Ensure the SRCustomBlockMutation is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRCustomBlockMutation is invalid
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
        result = self.custom_opcode.to_proccode_argument_names_defaults()
        proccode, argument_names, argument_defaults = result
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
        Ensure the SRCustomBlockCallMutation is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRCustomBlockCallMutation is invalid
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


__all__ = [
    "FRMutation", 
    "FRCustomBlockArgumentMutation", "FRCustomBlockMutation", "FRCustomBlockCallMutation", "FRStopScriptMutation",
    "SRMutation", 
    "SRCustomBlockArgumentMutation", "SRCustomBlockMutation", "SRCustomBlockCallMutation",
]

