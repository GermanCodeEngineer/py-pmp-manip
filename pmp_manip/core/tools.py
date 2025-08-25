from types  import MethodType
from typing import Generic, TypeAlias, TypeVar, Iterator, Iterable, Any

#from pmp_manip.important_consts import SHA256_SEC_TARGET_NAME, SHA256_SEC_BROADCAST_MSG
#from pmp_manip.opcode_info.api  import OpcodeInfoAPI, DropdownValueKind
from pmp_manip.utility          import (
    grepr_dataclass, enforce_argument_types, AbstractTreePath,
)

from pmp_manip.core.asset          import SRCostume, SRVectorCostume, SRBitmapCostume, SRSound
from pmp_manip.core.block_mutation import (
    SRMutation, SRCustomBlockArgumentMutation, SRCustomBlockMutation, SRCustomBlockCallMutation
)
from pmp_manip.core.block          import (
    SRScript, SRBlock, SRInputValue,
    SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, SRBlockAndBoolInputValue,
    SRBlockOnlyInputValue, SRScriptInputValue,
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
    SRStage, SRSprite,
    
    SRVariable, SRCloudVariable, SRList,
    SRMonitor, SRVariableMonitor, SRListMonitor,
    SRBuiltinExtension, SRCustomExtension,
    
    SRScript, SRBlock,
    SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, SRBlockAndBoolInputValue,
    SRBlockOnlyInputValue, SRScriptInputValue,
    SRDropdownValue,
    
    SRCustomBlockArgumentMutation, SRCustomBlockMutation, SRCustomBlockCallMutation,
    SRCustomBlockOpcode, SRCustomBlockArgument,
    
    SRComment,
    SRVectorCostume, SRBitmapCostume,
    SRSound,
)
SECOND_REPR_T: TypeAlias = (
    SRProject |
    SRStage | SRSprite |
    
    SRVariable | SRCloudVariable | SRList |
    SRMonitor | SRVariableMonitor | SRListMonitor |
    SRBuiltinExtension | SRCustomExtension |
    
    SRScript | SRBlock |
    SRBlockAndTextInputValue | SRBlockAndDropdownInputValue | SRBlockAndBoolInputValue |
    SRBlockOnlyInputValue | SRScriptInputValue |
    SRDropdownValue |
    
    SRCustomBlockArgumentMutation | SRCustomBlockMutation | SRCustomBlockCallMutation |
    SRCustomBlockOpcode | SRCustomBlockArgument |
    
    SRComment |
    SRVectorCostume | SRBitmapCostume |
    SRSound
)
INCLUDED_T = TypeVar("INCLUDED_T", bound=SECOND_REPR_T)

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

@grepr_dataclass(grepr_fields=["included_types"])
class TreeIteratorGenerator(Generic[INCLUDED_T]):
    """
    Implements the recursive iteration of an Abstract Object Tree in Second Representation.
    """
    included_types: tuple[type[INCLUDED_T]]
    
    @enforce_argument_types
    @classmethod
    def new_include_only(cls, included: Iterable[type[INCLUDED_T]]) -> "TreeIteratorGenerator[INCLUDED_T]":
        """
        Create a new TreeIteratorGenerator, which only yields values of the specified types.
        """
        return cls(tuple(included))

    # sadly the most specific signature we can make:
    @enforce_argument_types
    @classmethod
    def new_include_all_except(cls, excluded: Iterable[type[SECOND_REPR_T]]) -> "TreeIteratorGenerator[SECOND_REPR_T]":
        """
        Create a new TreeIteratorGenerator, which yields values of all second representation types except for the specified types.
        """
        included = [t for t in ALL_SECOND_REPR_TYPES if t not in excluded]
        return cls(tuple(included))

    @enforce_argument_types
    def iterate_tree(self, obj: SECOND_REPR_T) -> Iterable[tuple[INCLUDED_T, AbstractTreePath]]:
        """
        Run the TreeIteratorGenerator recursively on an Abstract Second Representation Tree.
        Yields pairs of node value and node path (from tree root to value).
        """
        unfiltered_pairs = self._iterate_node_unfiltered(obj, path=AbstractTreePath())
        filtered_pairs = []
        for value, path in unfiltered_pairs:
            if isinstance(value, self.included_types):
                filtered_pairs.append((value, path))
        return filtered_pairs
    
    @staticmethod
    def _iterate_node_unfiltered(
        obj: SECOND_REPR_T | list[Any] | tuple[Any] | dict[Any, Any], 
        path: AbstractTreePath,
    ) -> Iterable[tuple[SECOND_REPR_T, AbstractTreePath]]:
        """
        Run the TreeIteratorGenerator unfiltered on an Abstract Second Representation Tree.
        Yields pairs of node value and node path (from tree root to value).
        
        Args:
            obj: the object tree to iterate recursively
            path: the path from the tree root to obj
        """
        pairs = []
        if   isinstance(obj, (list, tuple)):
            for i, item in enumerate(obj):
                current_path = path.add_index_or_key(i)
                pairs.append((item, current_path))
                pairs.extend(TreeIteratorGenerator._iterate_node_unfiltered(item, current_path))
        elif isinstance(obj, dict):
            for key, value in obj.items():
                current_path = path.add_index_or_key(key)
                pairs.append((value, current_path))
                pairs.extend(TreeIteratorGenerator._iterate_node_unfiltered(value, current_path))
        elif isinstance(getattr(obj, "_iterate_node_unfiltered_", None), MethodType):
            # special case only for SRCustomBlockOpcode.segments
            # it has both str(primitive) and SRCustomBlockArgument(complex)
            pairs.extend(obj._iterate_node_unfiltered_(path))
        else:
            fields = _get_yield_fields(type(obj))
            for field in fields:
                value = getattr(obj, field)
                if value is not None:
                    current_path = path.add_attribute(field)
                    pairs.append((value, current_path))
                    pairs.extend(TreeIteratorGenerator._iterate_node_unfiltered(value, current_path))
        
        return pairs


__all__ = ["TreeIteratorGenerator"]

