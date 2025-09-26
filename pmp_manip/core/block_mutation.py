from abc         import ABC, abstractmethod
from copy        import copy, deepcopy
from dataclasses import field
from json        import loads, JSONDecodeError
from typing      import Any, ClassVar, NoReturn, Literal, TYPE_CHECKING

from pmp_manip.important_consts import SHA256_SEC_MAIN_ARGUMENT_NAME
from pmp_manip.utility          import (
    grepr_dataclass, string_to_sha256, gdumps,
    AA_TYPE, AA_HEX_COLOR, AA_LIST_OF_ONE_OF, AA_EXACT_LEN, AbstractTreePath,
    MANIP_ThanksError, MANIP_ConversionError, MANIP_DeserializationError, 
)


if TYPE_CHECKING: from pmp_manip.core.block_interface import FirstToInterIF, InterToFirstIF
from pmp_manip.core.custom_block import SRCustomBlockOpcode, SRCustomBlockOptype


def _load_bool_value(data: dict[str, Any], key: str, default: bool, allow_null: bool = False) -> bool | None:
    """
    Load a boolean from a key of a dictionary.
    
    Args:
        data: the dictionary containing a string key with a value which will be converted to a boolean.
        key: the string key in the dictionary with a value which will be converted to a boolean.
        default: the default value if the key does not exist.
        allow_null: wether null should be allowed(returned as None). Otherwise "null" is interpreted as "not set".
    
    Raises:
        MANIP_DeserializationError: if the key's value can not be interpreted as a boolean.
    """
    value = data.get(key, default)
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        if value == "undefined":
            return default
        if value == "null":
            return None if allow_null else default
        try:
            return loads(value)
        except JSONDecodeError as error:
            raise MANIP_DeserializationError(f"Invalid value for {key!r}, expected boolean-like value: {value}") from error
    else:
        raise MANIP_DeserializationError(f"Invalid value for {key!r}, expected boolean-like value: {value}")

def _load_noquote_str_value(data: dict[str, Any], key: str, default: str) -> bool:
    """
    Load a non-qouted string from a key of a dictionary.
    
    Args:
        data: the dictionary containing a string key with a value which will be converted to a non-qouted string.
        key: the string key in the dictionary with a value which will be converted to a non-qouted string.
        default: the default value if the key does not exist.
    
    Raises:
        MANIP_DeserializationError: if the key's value can not be interpreted as a non-qouted string.
    """
    value = data.get(key, default)
    if isinstance(value, str):
        if value in {"undefined", "null"}:
            return default
        if '"' not in value:
            return value
        try:
            value = loads(value)
            if '"' not in value:
                return value
            else:
                raise MANIP_DeserializationError(f"Invalid value for {key!r}, expected quoted or non-quoted string value: {value}")
        except JSONDecodeError as error:
            raise MANIP_DeserializationError(f"Invalid value for {key!r}, expected quoted or non-quoted string value: {value}") from error
    else:
        raise MANIP_DeserializationError(f"Invalid value for {key!r}, expected quoted or non-quoted string value: {value}")

def _load_color_array(data: dict[str, Any], key: str, default: tuple[str, str, str]) -> tuple[str, str, str]:
    """
    Load a triple color array from a key of a dictionary.
    
    Args:
        data: the dictionary containing a string key with a value which will be converted to a triple color array.
        key: the string key in the dictionary with a value which will be converted to a triple color array.
        default: the default value if the key does not exist.
    
    Raises:
        MANIP_DeserializationError: if the key's value can not be interpreted as a triple color array.
    """
    value = data.get(key, list(default))
    if isinstance(value, list):
        return tuple(value)
    elif isinstance(value, str):
        if value in {"undefined", "null"}:
            return default
        try:
            return tuple(loads(value))
        except JSONDecodeError as error:
            raise MANIP_DeserializationError(f"Invalid value for {key!r}, expected array-like value: {value}") from error
    else:
        raise MANIP_DeserializationError(f"Invalid value for {key!r}, expected array-like value: {value}")

@grepr_dataclass(
    grepr_fields=["tag_name", "children"], init=False, forbid_init_only_subcls=True,
    suggested_subcls_names=["FRCustomBlockArgumentMutation", "FRCustomBlockMutation", "FRCustomBlockCallMutation", "FRStopScriptMutation", "FRPolygonMutation"]
)
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
class FRCustomBlockArgumentMutation(FRMutation,
    required_properties={"color"},
    optional_properties={"warp", "edited", "hasnext"},
    ):
    """
    The first representation for the mutation of a custom block's argument reporter
    """
    
    color: tuple[str, str, str]
    warp: Literal[False] = False # should not exist and if present seems to be False
    edited: Literal[False] = False # should not exist and if present seems to be False
    has_next: Literal[False] = False # should not exist and if present seems to be False

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
            children = deepcopy(data["children"]),
            color    = _load_color_array(data, key="color", default=("#FF6680", "#FF4D6A", "#FF3355")),
            
            warp     = _load_bool_value(data, "warp", default=False),
            edited   = _load_bool_value(data, "edited", default=False),
            has_next = _load_bool_value(data, "hasnext", default=False),
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

@grepr_dataclass(grepr_fields=["proccode", "argument_ids", "argument_names", "argument_defaults", "warp", "returns", "edited", "optype", "color", "has_next"])
class FRCustomBlockMutation(FRMutation, 
        required_properties={"proccode", "argumentids", "argumentnames", "argumentdefaults", "warp"},
        optional_properties={"returns", "edited", "optype", "color", "hasnext"},
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
    has_next: Literal[False] = False # should not exist and if present seems to be False

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRCustomBlockMutation":
        """
        Create a FRCustomBlockMutation from json data
        
        Args:
            data: the json data
        
        Returns:
            the FRCustomBlockMutation
        """
        return cls(
            tag_name          = data["tagName" ],
            children          = deepcopy(data["children"]),
            proccode          = data["proccode"],
            argument_ids      = loads(data["argumentids"     ]),
            argument_names    = loads(data["argumentnames"   ]),
            argument_defaults = loads(data["argumentdefaults"]),
            warp              = _load_bool_value(data, key="warp", default=False),
            returns           = _load_bool_value(data, key="returns", default=False, allow_null=True),
            edited            = _load_bool_value(data, key="edited", default=True),
            optype            = _load_noquote_str_value(data, key="optype", default="statement"),
            color             = _load_color_array(data, key="color", default=("#FF6680", "#FF4D6A", "#FF3355")),
            has_next          = _load_bool_value(data, key="hasnext", default=False),
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
        optional_properties={"returns", "edited", "optype", "color", "hasnext"},
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
    has_next: Literal[False] = False # should not exist and if present seems to be False
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRCustomBlockCallMutation":
        """
        Create a FRCustomBlockCallMutation from json data
        
        Args:
            data: the json data
        
        Returns:
            the FRCustomBlockCallMutation
        """
        return cls(
            tag_name          = data["tagName" ],
            children          = deepcopy(data["children"]),
            proccode          = data["proccode"],
            argument_ids      = loads(data["argumentids"]),
            warp              = _load_bool_value(data, key="warp", default=False),
            returns           = _load_bool_value(data, key="returns", default=False, allow_null=True),
            edited            = _load_bool_value(data, key="edited", default=True),
            optype            = _load_noquote_str_value(data, key="optype", default="statement"),
            color             = _load_color_array(data, key="color", default=("#FF6680", "#FF4D6A", "#FF3355")),
            has_next          = _load_bool_value(data, key="hasnext", default=False),
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

@grepr_dataclass(grepr_fields=["branches", "ends_in_else"])
class FRExpandableIfMutation(FRMutation,
        required_properties={"branches", "ends-in-else"},
        optional_properties=set(),
    ):
    """
    The first representation for the mutation of an expandable if block
    """

    branches: int
    ends_in_else: bool
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRExpandableIfMutation":
        """
        Create a FRExpandableIfMutation(for the inner "block" of the old "draw triangle" block) from json data
        
        Args:
            data: the json data
        """
        return cls(
            tag_name     = data["tagName" ],
            children     = deepcopy(data["children"]),
            branches     = loads(data["branches"]),
            ends_in_else = _load_bool_value(data, key="ends-in-else", default=False),
        )

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRExpandableIfMutation into json data
        """
        return {
            "tagName"     : self.tag_name,
            "children"    : deepcopy(self.children),
            "branches"    : gdumps(self.branches),
            "ends-in-else": gdumps(self.ends_in_else),
        }
   
    def to_second(self, fti_if: "FirstToInterIF") -> "SRExpandableIfMutation":
        """
        Convert a FRExpandableIfMutation into a SRExpandableIfMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        """
        return SRExpandableIfMutation(
            branch_count=self.branches,
            ends_in_else=self.ends_in_else,
        )

@grepr_dataclass(grepr_fields=["input_count", "menu_values"])
class FRExpandableMathMutation(FRMutation,
        required_properties={"inputcount", "menuvalues"},
        optional_properties=set(),
    ):
    """
    The first representation for the mutation of an expandable math block
    """

    input_count: int
    menu_values: list[Literal["+", "-", "*", "/", "^"]]
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRExpandableMathMutation":
        """
        Create a FRExpandableMathMutation from json data
        
        Args:
            data: the json data
        """
        return cls(
            tag_name    = data["tagName" ],
            children    = deepcopy(data["children"]),
            input_count = loads(data["inputcount"]),
            menu_values = list(data["menuvalues"]),
        )

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRExpandableMathMutation into json data
        """
        return {
            "tagName"   : self.tag_name,
            "children"  : deepcopy(self.children),
            "inputcount": gdumps(self.input_count),
            "menuvalues": "".join(self.menu_values),
        }
   
    def to_second(self, fti_if: "FirstToInterIF") -> "SRExpandableMathMutation":
        """
        Convert a FRExpandableMathMutation into a SRExpandableMathMutation
        
        Args:
            fti_if: interface which allows the management of other blocks
        """
        return SRExpandableMathMutation(operations=copy(self.menu_values))

@grepr_dataclass(grepr_fields=["has_next"])
class FRStopScriptMutation(FRMutation,
    required_properties={"hasnext"},
    optional_properties={"warp", "edited"},
    ):
    """
    The first representation for the mutation of a stop script mutation
    """
    
    has_next: bool
    warp: Literal[False] = False # should not exist and if present seems to be False
    edited: Literal[False] = False # should not exist and if present seems to be False
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRStopScriptMutation":
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
            has_next = _load_bool_value(data, key="hasnext", default=False)
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
        raise NotImplementedError("A second representation of a stop script mutation does not exist. It is not needed for an IRBlock or SRBlock")

@grepr_dataclass(grepr_fields=["points", "color", "midle", "scale", "expanded", "needs_init"])
class FRPolygonMutation(FRMutation, 
        required_properties={"points", "color", "midle", "scale", "expanded", "needsinit"},
        optional_properties=set(),
    ):
    """
    The first representation for the mutation of a stop script mutation
    """

    points: int # usually 3 or 4
    color: Literal["#0FBD8C"] | str
    midle: tuple[Literal[0], Literal[0]]
    scale: Literal[50]
    expanded: Literal[True]
    needs_init: Literal[True]
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRPolygonMutation":
        """
        Create a FRPolygonMutation(for the inner "block" of the old "draw triangle" block) from json data
        
        Args:
            data: the json data
        """
        return cls(
            tag_name   = data["tagName" ],
            children   = deepcopy(data["children"]),
            points     = loads(data["points"]),
            color      = data["color"],
            midle      = tuple(loads(data["midle"])),
            scale      = loads(data["scale"]),
            expanded   = _load_bool_value(data, key="expanded", default=True),
            needs_init = _load_bool_value(data, key="needsinit", default=True),
        )

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRPolygonMutation into json data
        """
        return {
            "tagName"  : self.tag_name,
            "children" : deepcopy(self.children),
            "points"   : gdumps(self.points),
            "color"    : self.color,
            "midle"    : gdumps(self.midle),
            "scale"    : gdumps(self.scale),
            "expanded" : gdumps(self.expanded),
            "needsinit": gdumps(self.needs_init),
        }
   
    def to_second(self, fti_if: "FirstToInterIF") -> NoReturn:
        """
        A second representation of a polygon mutation does not exist. 
        It would just store alredy known information in a second place.
        """
        raise NotImplementedError("A second representation of a polygon mutation does not exist. It is not needed for an IRBlock or SRBlock")


@grepr_dataclass(
    grepr_fields=[], init=False, forbid_init_only_subcls=True, 
    suggested_subcls_names=["SRCustomBlockArgumentMutation", "SRCustomBlockMutation", "SRCustomBlockCallMutation"],
)
class SRMutation(ABC):
    """
    The second representation for the mutation of a block. Mutations hold special information, which only special blocks have. This representation is much more user friendly then the first representation
    """

    @abstractmethod
    def validate(self, path: AbstractTreePath) -> None:
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
            itf_if: interface which allows the management of other blocks
        
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

    def validate(self, path: AbstractTreePath) -> None:
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
            itf_if: interface which allows the management of other blocks
        
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
    
    def validate(self, path: AbstractTreePath) -> None:
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

        self.custom_opcode.validate(path.add_attribute("custom_opcode"))

    
    def to_first(self, itf_if: "InterToFirstIF") -> FRCustomBlockMutation:
        """
        Convert a SRCustomBlockMutation into a FRCustomBlockMutation
        
        Args:
            itf_if: interface which allows the management of other blocks
        
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
    
    def validate(self, path: AbstractTreePath) -> None:
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

        self.custom_opcode.validate(path.add_attribute("custom_opcode"))
    
    def to_first(self, itf_if: "InterToFirstIF") -> FRCustomBlockCallMutation:
        """
        Convert a SRCustomBlockCallMutation into a FRCustomBlockCallMutation
        
        Args:
            itf_if: interface which allows the management of other blocks
        
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

@grepr_dataclass(grepr_fields=["branch_count", "ends_in_else"])
class SRExpandableIfMutation(SRMutation):
    """
    The second representation for the mutation of an expandable if block
    """

    branch_count: int
    ends_in_else: bool
    
    def validate(self, path: AbstractTreePath) -> None:
        """
        Ensure the SRExpandableIfMutation is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the SRExpandableIfMutation is invalid
        """
        AA_TYPE(self, path, "branch_count", int)
        AA_TYPE(self, path, "ends_in_else", bool)
    
    def to_first(self, itf_if: "InterToFirstIF") -> "FRExpandableIfMutation":
        """
        Convert a SRExpandableIfMutation into a FRExpandableIfMutation

        Args:
            itf_if: interface which allows the management of other blocks
        """
        return FRExpandableIfMutation(
            tag_name="mutation",
            children=[],
            branches=self.branch_count,
            ends_in_else=self.ends_in_else,
        )

@grepr_dataclass(grepr_fields=["operations"])
class SRExpandableMathMutation(SRMutation):
    """
    The second representation for the mutation of an expandable math block
    """

    operations: list[Literal["+", "-", "*", "/", "^"]]
    
    def validate(self, path: AbstractTreePath) -> None:
        """
        Ensure the SRExpandableMathMutation is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the SRExpandableMathMutation is invalid
        """
        AA_LIST_OF_ONE_OF(self, path, "operations", ["+", "-", "*", "/", "^"])
    
    def to_first(self, itf_if: "InterToFirstIF") -> "FRExpandableMathMutation":
        """
        As this mutation represents both first and second representation self will be returned

        Args:
            itf_if: interface which allows the management of other blocks
        """
        return FRExpandableMathMutation(
            tag_name="mutation",
            children=[],
            input_count=len(self.operations)+1,
            menu_values=copy(self.operations),
        )


__all__ = [
    "FRMutation", 
    "FRCustomBlockArgumentMutation", "FRCustomBlockMutation", "FRCustomBlockCallMutation", "FRExpandableIfMutation", "FRExpandableMathMutation",
    "FRStopScriptMutation", "FRPolygonMutation",
    "SRMutation", 
    "SRCustomBlockArgumentMutation", "SRCustomBlockMutation", "SRCustomBlockCallMutation", "SRExpandableIfMutation", "SRExpandableMathMutation",
]

