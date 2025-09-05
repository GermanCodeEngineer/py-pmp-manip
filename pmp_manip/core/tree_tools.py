from types  import MethodType
from typing import Generic, TypeVar, Iterable, Literal, Any, cast, overload

from pmp_manip.utility          import (
    grepr_dataclass, enforce_argument_types,
    AbstractTreePath, ATPathAttribute, ATPathIndexOrKey, NotSet, NotSetType,
)

from pmp_manip.core.asset          import SRCostume, SRVectorCostume, SRBitmapCostume, SRSound
from pmp_manip.core.block_mutation import (
    SRMutation, SRCustomBlockArgumentMutation, SRCustomBlockMutation, SRCustomBlockCallMutation
)
from pmp_manip.core.block          import (
    SRScript, SRBlock, SRInputValue,
    SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, SRBlockAndBoolInputValue,
    SRBlockOnlyInputValue, SRScriptInputValue, SREmbeddedBlockInputValue,
)
from pmp_manip.core.comment        import SRComment
from pmp_manip.core.custom_block   import SRCustomBlockOpcode, SRCustomBlockArgument
from pmp_manip.core.dropdown       import SRDropdownValue
from pmp_manip.core.extension      import SRExtension, SRBuiltinExtension, SRCustomExtension
from pmp_manip.core.monitor        import SRMonitor, SRVariableMonitor, SRListMonitor
from pmp_manip.core.target         import SRTarget, SRStage, SRSprite
from pmp_manip.core.project        import SRProject
from pmp_manip.core.vars_lists     import SRVariable, SRCloudVariable, SRList


ALL_SECOND_REPR_TYPES = (
    SRProject,
    SRTarget, SRStage, SRSprite,
    
    SRVariable, SRCloudVariable, SRList,
    SRMonitor, SRVariableMonitor, SRListMonitor,
    SRExtension, SRBuiltinExtension, SRCustomExtension,
    
    SRScript, SRBlock, SRInputValue,
    SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, SRBlockAndBoolInputValue,
    SRBlockOnlyInputValue, SRScriptInputValue, SREmbeddedBlockInputValue,
    SRDropdownValue,
    
    SRMutation, SRCustomBlockArgumentMutation, SRCustomBlockMutation, SRCustomBlockCallMutation,
    SRCustomBlockOpcode, SRCustomBlockArgument,
    
    SRComment,
    SRCostume, SRVectorCostume, SRBitmapCostume,
    SRSound,
)
SECOND_REPR_T = (
    SRProject |
    SRTarget | SRStage | SRSprite |
    
    SRVariable | SRCloudVariable | SRList |
    SRMonitor | SRVariableMonitor | SRListMonitor |
    SRExtension | SRBuiltinExtension | SRCustomExtension |
    
    SRScript | SRBlock | SRInputValue | SREmbeddedBlockInputValue |
    SRBlockAndTextInputValue | SRBlockAndDropdownInputValue | SRBlockAndBoolInputValue |
    SRBlockOnlyInputValue | SRScriptInputValue | SREmbeddedBlockInputValue |
    SRDropdownValue |
    
    SRMutation | SRCustomBlockArgumentMutation | SRCustomBlockMutation | SRCustomBlockCallMutation |
    SRCustomBlockOpcode | SRCustomBlockArgument |
    
    SRComment |
    SRCostume | SRVectorCostume | SRBitmapCostume |
    SRSound
)
INCLUDED_T = TypeVar("INCLUDED_T", bound=SECOND_REPR_T)
ARG_T = TypeVar("ARG_T")

YIELD_FIELDS: dict[type[SECOND_REPR_T], list[str]] = {
    SRProject: ["stage", "sprites", "global_variables", "global_lists", "global_monitors", "extensions"],
    SRTarget: ["scripts", "comments", "costumes", "sounds"],
    SRStage: [],
    SRSprite: ["local_variables", "local_lists", "local_monitors"],
    
    SRVariable: [],
    SRCloudVariable: [],
    SRList: [],
    SRMonitor: ["dropdowns"],
    SRVariableMonitor: [],
    SRListMonitor: [],
    SRExtension: [],
    SRBuiltinExtension: [],
    SRCustomExtension: [],
    
    SRScript: ["blocks"],
    SRBlock: ["inputs", "dropdowns", "comment", "mutation"],
    SRInputValue: [],
    SRBlockAndTextInputValue: ["block"],
    SRBlockAndDropdownInputValue: ["block", "dropdown"],
    SRBlockAndBoolInputValue: ["block"],
    SRBlockOnlyInputValue: ["block"],
    SRScriptInputValue: ["blocks"],
    SRDropdownValue: [], # kinda primitive, borderline, just included to complete second repr fully
    SREmbeddedBlockInputValue: ["block"],
    
    SRMutation: [],
    SRCustomBlockArgumentMutation: [],
    SRCustomBlockMutation: ["custom_opcode"],
    SRCustomBlockCallMutation: ["custom_opcode"],
    SRCustomBlockOpcode: ["segments"], # see above
    SRCustomBlockArgument: [], # see above
    
    SRComment: [],
    SRCostume: [],
    SRVectorCostume: [],
    SRBitmapCostume: [],
    SRSound: [],
}


def _get_yield_fields(cls: type[SECOND_REPR_T]):
    """
    Get the relevant fields of a second representation type.
    """
    fields = []
    for base in cls.__bases__:
        if base in YIELD_FIELDS:
            fields.extend(_get_yield_fields(base))
    fields.extend(YIELD_FIELDS[cls])
    return fields

def _visit_node_unfiltered(
    obj: SECOND_REPR_T | list[Any] | tuple[Any] | dict[Any, Any], 
    path: AbstractTreePath,
) -> Iterable[tuple[AbstractTreePath, SECOND_REPR_T]]:
    """
    Run the TreeVisitor unfiltered on an Abstract Second Representation Tree.
    Returns pairs of node path (from tree root to value) and node value.
    
    Args:
        obj: the object tree to iterate recursively
        path: the path from the tree root to obj
    """
    pairs = []
    if   isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            current_path = path.add_index_or_key(i)
            pairs.append((current_path, item))
            pairs.extend(_visit_node_unfiltered(item, current_path))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            current_path = path.add_index_or_key(key)
            pairs.append((current_path, value))
            pairs.extend(_visit_node_unfiltered(value, current_path))
    elif isinstance(getattr(obj, "_visit_node_unfiltered_", None), MethodType):
        # special case only for SRCustomBlockOpcode.segments
        # it has both str(primitive) and SRCustomBlockArgument(complex)
        pairs.extend(obj._visit_node_unfiltered_(path))
    else:
        fields = _get_yield_fields(type(obj))
        for field in fields:
            value = getattr(obj, field)
            if value is not None:
                current_path = path.add_attribute(field)
                pairs.append((current_path, value))
                pairs.extend(_visit_node_unfiltered(value, current_path))
    return pairs

@grepr_dataclass(grepr_fields=["included_types"])
class TreeVisitor(Generic[INCLUDED_T]):
    """
    Implements the recursive iteration of an Abstract Object Tree in Second Representation.
    """
    included_types: tuple[type[INCLUDED_T], ...]
    
    @enforce_argument_types
    @classmethod
    def new_include_only(cls, included: Iterable[type[INCLUDED_T]]) -> "TreeVisitor[INCLUDED_T]":
        """
        Create a new TreeVisitor, which only includes values of the specified types.
        """
        return cls(tuple(included))

    # sadly the most specific signature we can make:
    @enforce_argument_types
    @classmethod
    def new_include_all_except(cls, excluded: Iterable[type[SECOND_REPR_T]]) -> "TreeVisitor[SECOND_REPR_T]":
        """
        Create a new TreeVisitor, which includes values of all second representation types except for the specified types.
        """
        included = [t for t in ALL_SECOND_REPR_TYPES if t not in excluded]
        return cls(tuple(included))

    # INCLUDED_T will be inferred as Any by type checkers, no solution possible currently
    @enforce_argument_types
    def visit_tree(self, obj: SECOND_REPR_T) -> dict[AbstractTreePath, INCLUDED_T]:
        """
        Run the TreeVisitor recursively on an Abstract Second Representation Tree.
        Returns a map from node path (from tree root to value) to node value.
        """
        unfiltered_pairs = _visit_node_unfiltered(obj, path=AbstractTreePath())
        filtered_map: dict[AbstractTreePath, INCLUDED_T] = {}
        for path, value in unfiltered_pairs:
            if isinstance(value, self.included_types):
                filtered_map[path] = cast(INCLUDED_T, value)
        return filtered_map

@overload
def get_path_in_tree(tree: SECOND_REPR_T, path: AbstractTreePath, default: NotSetType = NotSet) -> SECOND_REPR_T: ...
@overload
def get_path_in_tree(tree: SECOND_REPR_T, path: AbstractTreePath, default: ARG_T) -> SECOND_REPR_T | ARG_T: ...
@enforce_argument_types
def get_path_in_tree(tree: SECOND_REPR_T, path: AbstractTreePath, default: NotSetType | ARG_T = NotSet) -> SECOND_REPR_T | ARG_T:
    """
    Dynamically get a node in an Abstract Second Representation Tree by its path.

    Raises:
        ValueError: if the path could not be accessed.
    """
    current_object = tree
    for i, item in enumerate(path):
        if   isinstance(item, ATPathAttribute):
            try:
                current_object = getattr(current_object, item.value)
            except (AttributeError, TypeError, Exception) as error:
                if default is NotSet:
                    raise ValueError(f"Failed to get attribute {item.value!r} of object at path {path[:i]}: {error}") from error
                else:
                    return default
        elif isinstance(item, ATPathIndexOrKey):
            try:
                current_object = current_object[item.value]
            except (IndexError, KeyError, TypeError, Exception) as error:
                if default is NotSet:
                    raise ValueError(f"Failed to get index or key {item.value!r} of object at path {path[:i]}: {error}") from error
                else:
                    return default
    return current_object

@enforce_argument_types
def path_exists_in_tree(tree: SECOND_REPR_T, path: AbstractTreePath) -> bool:
    """
    Checks if a path is exists/is accessiable in an Abstract Second Representation Tree.
    """
    try:
        get_path_in_tree(tree, path)
        return True
    except ValueError:
        return False

@enforce_argument_types
def set_path_in_tree(tree: SECOND_REPR_T, path: AbstractTreePath, value: SECOND_REPR_T) -> None:
    """
    Dynamically set a node in an Abstract Second Representation Tree by its path to a value.

    Raises:
        TypeError: if the path is invalid.
        AttributeError: if the last attribute could not be set for some reason.
        IndexError: if the last index is out of range.
    """
    # Get the object of which an attribute, index or key is supposed to be set.
    obj = get_path_in_tree(tree, path[:-1])
    path_item = path[-1]
    if   isinstance(path_item, ATPathAttribute):
        try:
            setattr(obj, path_item.value, value)
        except (AttributeError, TypeError) as error:
            raise type(error)(f"Failed to set attribute {path_item.value!r} of object at path {path}: {error}") from error
    elif isinstance(path_item, ATPathIndexOrKey):
        try:
            obj[path_item.value] = value
        except (IndexError, TypeError) as error:
            raise type(error)(f"Failed to set index or key {path_item.value!r} of object at path {path}: {error}") from error


__all__ = ["TreeVisitor", "get_path_in_tree", "path_exists_in_tree", "set_path_in_tree"]

