from __future__ import annotations
from typing     import Iterable, Any

from pmp_manip.utility import grepr_dataclass, enforce_argument_types, TreeVisitor as BaseTreeVisitor

from pmp_manip.core.asset          import SRCostume, SRVectorCostume, SRBitmapCostume, SRSound
from pmp_manip.core.block_mutation import (
    SRMutation, SRCustomBlockArgumentMutation, SRCustomBlockMutation, SRCustomBlockCallMutation,
    SRExpandableIfMutation, SRExpandableOperatorMutation, SRExpandableJoinMutation,
    SRExpandableOperatorMenu,
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
    SRExpandableIfMutation, SRExpandableOperatorMutation, SRExpandableJoinMutation,
    SRCustomBlockOpcode, SRCustomBlockArgument, SRExpandableOperatorMenu,
    
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
    SRExpandableIfMutation | SRExpandableOperatorMutation | SRExpandableJoinMutation |
    SRCustomBlockOpcode | SRCustomBlockArgument | SRExpandableOperatorMenu |
    
    SRComment |
    SRCostume | SRVectorCostume | SRBitmapCostume |
    SRSound
)

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
    SRExpandableIfMutation: [],
    SRExpandableOperatorMutation: [],
    SRExpandableJoinMutation: [],
    SRCustomBlockOpcode: ["segments"], # see above
    SRCustomBlockArgument: [], # see above
    
    SRComment: [],
    SRCostume: [],
    SRVectorCostume: [],
    SRBitmapCostume: [],
    SRSound: [],
}


class SRTreeVisitor(BaseTreeVisitor):
    """
    Implements the recursive iteration of an Abstract Object Tree in Second Representation.
    """

    # sadly the most specific signature we can make:
    @enforce_argument_types
    @classmethod
    def create_new_include_all_except(cls, excluded: Iterable[type[SECOND_REPR_T]]) -> SRTreeVisitor[SECOND_REPR_T]:
        """
        Create a new tree visitor, which includes values of all second representation types except for the specified types.
        """
        return super().create_new_include_all_except(excluded, universe=ALL_SECOND_REPR_TYPES)

    @classmethod
    def _get_yield_fields(own_cls, target_cls: type[Any]) -> list[str]:
        """
        Get the relevant fields of a second representation type.
        """
        fields = []
        for base in target_cls.__bases__:
            if base in YIELD_FIELDS:
                fields.extend(own_cls._get_yield_fields(base))
        fields.extend(YIELD_FIELDS[target_cls])
        return fields
    

__all__ = ["SRTreeVisitor"]

