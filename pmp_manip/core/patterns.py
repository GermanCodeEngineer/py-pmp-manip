from __future__ import annotations
from dataclasses import field
from typing import TypeVar, Callable, TypeAlias, Generic, Any, ClassVar

from pmp_manip.opcode_info.api import DropdownValueKind, DROPDOWN_VALUE_T
from pmp_manip.utility          import (
    grepr_dataclass, enforce_argument_types,
)

from pmp_manip.core.block_mutation import (
    SRMutation, SRCustomBlockArgumentMutation, SRCustomBlockMutation, SRCustomBlockCallMutation,
)
from pmp_manip.core.block          import (SRScript, SRBlock, SRInputValue)
from pmp_manip.core.comment        import SRComment
from pmp_manip.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType, SRCustomBlockOptype,
)
from pmp_manip.core.dropdown       import SRDropdownValue
#from pmp_manip.core.extension      import SRExtension, SRBuiltinExtension, SRCustomExtension
#from pmp_manip.core.monitor        import SRMonitor, SRVariableMonitor, SRListMonitor
#from pmp_manip.core.target         import SRTarget, SRStage, SRSprite
#from pmp_manip.core.project        import SRProject
#from pmp_manip.core.vars_lists     import SRVariable, SRCloudVariable, SRList


CONST_T = TypeVar("CONST_T")

@grepr_dataclass(grepr_fields=["value"])
class Const(Generic[CONST_T]): # TODO: find better name
    value: CONST_T

# parametric alias
ConstOrFunc     : TypeAlias = Const[CONST_T] | Callable[[CONST_T], bool]
CBOpcodeSegmentT: TypeAlias = str | SRCustomBlockArgument
MutationPatternT: TypeAlias = "CBArgumentMutationPattern | CBMutationPattern | CBCallMutationPattern"

ScriptHandler         : TypeAlias = ConstOrFunc[SRScript]                     | "ScriptPattern"

BlockHandler          : TypeAlias = ConstOrFunc[SRBlock]                      | "BlockPattern"
OptBlockHandler       : TypeAlias = ConstOrFunc[SRBlock | None]               | "BlockPattern"
BlockListHandler      : TypeAlias = ConstOrFunc[list[SRBlock]]                | list[BlockHandler]

MutationHandler       : TypeAlias = ConstOrFunc[SRMutation]                   | MutationPatternT

InputHandler          : TypeAlias = ConstOrFunc[SRInputValue]                 | "InputPattern"
InputDictHandler      : TypeAlias = ConstOrFunc[dict[str, SRInputValue]]      | dict[str, InputHandler]

DropdownHandler       : TypeAlias = ConstOrFunc[SRDropdownValue]              | "DropdownPattern"
OptDropdownHandler    : TypeAlias = ConstOrFunc[SRDropdownValue | None]       | "DropdownPattern"
DropdownDictHandler   : TypeAlias = ConstOrFunc[dict[str, SRDropdownValue]]   | dict[str, DropdownHandler]

CBOpcodeHandler       : TypeAlias = ConstOrFunc[SRCustomBlockOpcode]          | "CBOpcodePattern"
CBArgumentHandler     : TypeAlias = ConstOrFunc[CBOpcodeSegmentT]             | "CBArgumentPattern"
CBArgumentTupleHandler: TypeAlias = ConstOrFunc[tuple[CBOpcodeSegmentT]]      | tuple[CBArgumentHandler]

@grepr_dataclass(
    grepr_fields=["access_point_id"], init=False, forbid_init_only_subcls=True,
    suggested_subcls_names=[
        "ScriptPattern", "BlockPattern", "InputPattern", "DropdownPattern",
        "CBArgumentMutationPattern", "CBMutationPattern", "CBCallMutationPattern",
        "CBOpcodePattern", "CBArgumentPattern",
    ],
)
class Pattern:
    """
    Basis for a Pattern selecting Second Representation Scripts, Blocks etc.
    """
    _match_type_: ClassVar[type]
    _match_fields_: ClassVar[list[str]]

    access_point_id: str | None = None
    
    def match(self, value: Any, result: MatchResult) -> bool:
        """
        Check if a Pattern matches with a Second Representation Tree.
        """
        if not isinstance(value, type(self)._match_type_):
            return False
        for field in type(self)._match_fields_:
            field_handler = getattr(self, field)
            try:
                field_value = getattr(value, field, None)
            except (AttributeError, Exception): # just to be safe even though default=None
                return False
            if   field_handler is None:
                field_matches = True
            elif isinstance(field_handler, (list, tuple)):
                field_matches = _match_list_tuple_handler(field_handler, field_value, result)
            elif isinstance(field_handler, dict):
                field_matches = _match_dict_handler(field_handler, field_value, result)
            else: # Const, Func or Pattern
                field_matches = _match_handler(field_handler, field_value, result)
            if not field_matches:
                return False
        if self.access_point_id is not None:
            result.add_access_point(self.access_point_id, value)
        return True


@grepr_dataclass(grepr_fields=["position", "blocks"])
class ScriptPattern(Pattern):
    """
    Pattern for selecting SRScript instances with certain data.
    """
    _match_type_: ClassVar = SRScript
    _match_fields_: ClassVar = ["position", "blocks"]
    
    position: ConstOrFunc[tuple[int|float, int|float]] | None = None
    blocks  : BlockListHandler = field(default_factory=list)

@grepr_dataclass(grepr_fields=["opcode", "inputs", "dropdowns", "comment", "mutation"])
class BlockPattern(Pattern):
    """
    Pattern for selecting SRBlock instances with certain data.
    """
    _match_type_: ClassVar = SRBlock
    _match_fields_: ClassVar = ["opcode", "inputs", "dropdowns", "comment", "mutation"]
    
    opcode   : ConstOrFunc[str] | None = None
    inputs   : InputDictHandler    = field(default_factory=dict)
    dropdowns: DropdownDictHandler = field(default_factory=dict)
    comment  : ConstOrFunc[SRComment | None] | None = None # possibly CommentPattern
    mutation : MutationHandler  | None = None

@grepr_dataclass(grepr_fields=["blocks", "block", "immediate", "dropdown"])
class InputPattern(Pattern):
    """
    Pattern for selecting SRInputValue or subclass instances with certain data.
    """
    _match_type_: ClassVar = SRInputValue
    _match_fields_: ClassVar = ["blocks", "block", "immediate", "dropdown"]
    
    blocks   : BlockListHandler = field(default_factory=list)
    block    : OptBlockHandler | None = None
    immediate: ConstOrFunc[str | bool | None] = None
    dropdown : OptDropdownHandler | None = None

@grepr_dataclass(grepr_fields=["kind", "value"])
class DropdownPattern(Pattern):
    """
    Pattern for selecting SRDropdownValue instances with certain data.
    """
    _match_type_: ClassVar = SRDropdownValue
    _match_fields_: ClassVar = ["kind", "value"]
    
    kind : ConstOrFunc[DropdownValueKind] | None = None
    value: ConstOrFunc[DROPDOWN_VALUE_T ] | None = None

@grepr_dataclass(grepr_fields=["argument_name", "main_color", "prototype_color", "outline_color"])
class CBArgumentMutationPattern(Pattern):
    """
    Pattern for selecting SRCustomBlockArgumentMutation instances with certain data.
    """
    _match_type_: ClassVar = SRCustomBlockArgumentMutation
    _match_fields_: ClassVar = ["argument_name", "main_color", "prototype_color", "outline_color"]

    argument_name  : ConstOrFunc[str] | None = None
    main_color     : ConstOrFunc[str] | None = None
    prototype_color: ConstOrFunc[str] | None = None
    outline_color  : ConstOrFunc[str] | None = None

@grepr_dataclass(grepr_fields=["custom_opcode", "no_screen_refresh", "optype", "main_color", "prototype_color", "outline_color"])
class CBMutationPattern(Pattern):
    """
    Pattern for selecting SRCustomBlockMutation instances with certain data.
    """
    _match_type_: ClassVar = SRCustomBlockMutation
    _match_fields_: ClassVar = ["custom_opcode", "no_screen_refresh", "optype", "main_color", "prototype_color", "outline_color"]

    custom_opcode    : CBOpcodeHandler   | None = None
    no_screen_refresh: ConstOrFunc[bool] | None = None
    optype           : ConstOrFunc[SRCustomBlockOpcode] | None = None
    main_color       : ConstOrFunc[str]  | None = None
    prototype_color  : ConstOrFunc[str]  | None = None
    outline_color    : ConstOrFunc[str]  | None = None

@grepr_dataclass(grepr_fields=["custom_opcode"])
class CBCallMutationPattern(Pattern):
    """
    Pattern for selecting SRCustomBlockCallMutation instances with certain data.
    """
    _match_type_: ClassVar = SRCustomBlockCallMutation
    _match_fields_: ClassVar = ["custom_opcode"]

    custom_opcode: CBOpcodeHandler | None = None

@grepr_dataclass(grepr_fields=["segments"])
class CBOpcodePattern(Pattern):
    """
    Pattern for selecting SRCustomBlockOpcode instances with certain data.
    """
    _match_type_: ClassVar = SRCustomBlockOpcode
    _match_fields_: ClassVar = ["segments"]

    segments: CBArgumentTupleHandler | None = None

@grepr_dataclass(grepr_fields=["name", "type"])
class CBArgumentPattern(Pattern):
    """
    Pattern for selecting SRCustomBlockArgument instances with certain data.
    """
    _match_type_: ClassVar = SRCustomBlockArgument
    _match_fields_: ClassVar = ["name", "type"]

    name: ConstOrFunc[str] | None = None
    type: ConstOrFunc[SRCustomBlockArgumentType] | None = None


@grepr_dataclass(grepr_fields=["access_points"])
class MatchResult:
    """
    Represents the result of a Sucessful Match from a Pattern with a Second Representation Tree.
    Allows the access of auto-filled access points by their id.
    """
    access_points: dict[str, Any] = field(init=False, default_factory=dict)

    def get_access_point(self, access_point_id: str) -> Any:
        """
        Get the value at a configured access point.

        Raises:
            ValueError: if an unkown id is provided.
        """
        try:
            return self.access_points[access_point_id]
        except KeyError:
            pass
        raise ValueError(f"Unknown access point: {access_point_id}")

    def add_access_point(self, access_point_id: str, value: Any) -> None:
        """
        Set a new access point.

        Raises:
            ValueError: if an alredy set id is provided.
        """
        if access_point_id in self.access_points:
            raise ValueError(f"Access point is alredy defined: {access_point_id}")
        self.access_points[access_point_id] = value
    
    

def _match_list_tuple_handler(
    handler: list[ConstOrFunc[Any] | Pattern] | tuple[ConstOrFunc[Any] | Pattern],
    value: list[Any],
    result: MatchResult,
) -> bool:
    """
    Check if a list or tuple of Constant, Pattern or Callable matches with a Second Representation Tree.
    """
    for i, item_handler in enumerate(handler):
        try:
            item_value = value[i]
        except (TypeError, IndexError, Exception):
            return False
        item_matches = _match_handler(item_handler, item_value, result)
        if not item_matches:
            return False
    return True

def _match_dict_handler(
    handler: dict[Any, ConstOrFunc[Any] | Pattern],
    value: dict[Any, Any],
    result: MatchResult,
) -> bool:
    """
    Check if a dict of Any and Constant, Pattern or Callable matches with a Second Representation Tree.
    """
    for key, item_handler in handler.items():
        try:
            item_value = value[key]
        except (TypeError, KeyError, Exception):
            return False
        item_matches = _match_handler(item_handler, item_value, result)
        if not item_matches:
            return False
    return True

def _match_handler(
    handler: ConstOrFunc[Any] | Pattern, 
    value: Any, 
    result: MatchResult,
) -> bool:
    """
    Check if a Constant, Pattern or Callable matches with a Second Representation Tree.
    On Success a MatchResult is returned. On Fail None is returned.
    
    Raises:
        TypeError: if the or any nested handler func returns a non-bool value.
    """
    if   isinstance(handler, Const):
        matches = handler.value == value
    elif isinstance(handler, Pattern):
        matches = handler.match(value, result)
    elif callable(handler):
        matches = handler(value)
        if not isinstance(matches, bool):
            raise TypeError(f"Custom handler func must return bool, not {type(matches)}")
    return matches

# TODO: possibly use SECOND_REPR_T instead of Any
@enforce_argument_types
def match_handler(handler: ConstOrFunc[Any] | Pattern, value: Any) -> MatchResult | None:
    """
    Check if a Constant, Pattern or Callable matches with a Second Representation Tree.
    On Success a MatchResult is returned. On Fail None is returned.
    
    Raises:
        TypeError: if the or any nested handler func returns a non-bool value.
    """
    result = MatchResult()
    matches = _match_handler(handler, value, result)
    return result if matches else None


__all__ = [
    "Const", "Pattern", 
    "ScriptPattern", "BlockPattern", "InputPattern", "DropdownPattern",
    "CBArgumentMutationPattern", "CBMutationPattern", "CBCallMutationPattern",
    "CBOpcodePattern", "CBArgumentPattern",
    "match_handler"
]

