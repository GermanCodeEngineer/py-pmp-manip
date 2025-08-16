from typing import TYPE_CHECKING, Any

if TYPE_CHECKING: from pmp_manip.opcode_info.api import DropdownValueKind
from pmp_manip.utility import grepr_dataclass


@grepr_dataclass(grepr_fields=["scope_variables", "scope_lists", "global_variables", "local_variables", "local_lists", "other_sprites", "backdrops"])
class PartialContext:
    """
    A temporary dataclass which stores the context for dropdown validation excluding sprite context
    """

    scope_variables: list[tuple["DropdownValueKind", Any]]
    scope_lists: list[tuple["DropdownValueKind", Any]]
    global_variables: list[tuple["DropdownValueKind", Any]]
    local_variables: dict[str|None, list[tuple["DropdownValueKind", Any]]]
    local_lists: dict[str|None, list[tuple["DropdownValueKind", Any]]]
    other_sprites: list[tuple["DropdownValueKind", Any]]
    backdrops: list[tuple["DropdownValueKind", Any]]

@grepr_dataclass(grepr_fields=["scope_variables", "scope_lists", "global_variables", "local_variables", "local_lists", "other_sprites", "backdrops", "costumes", "sounds", "is_stage"])
class CompleteContext:
    """
    A temporary dataclass which stores the context for dropdown validation including sprite context
    """

    scope_variables: list[tuple["DropdownValueKind", Any]]
    scope_lists: list[tuple["DropdownValueKind", Any]]
    global_variables: list[tuple["DropdownValueKind", Any]]
    local_variables: dict[str|None, list[tuple["DropdownValueKind", Any]]]
    local_lists: dict[str|None, list[tuple["DropdownValueKind", Any]]]
    other_sprites: list[tuple["DropdownValueKind", Any]]
    backdrops: list[tuple["DropdownValueKind", Any]]

    costumes: list[tuple["DropdownValueKind", Any]]
    sounds: list[tuple["DropdownValueKind", Any]]
    is_stage: bool

    @classmethod
    def from_partial(cls, 
        pc: PartialContext, 
        costumes: list[tuple["DropdownValueKind", Any]], 
        sounds: list[tuple["DropdownValueKind", Any]], 
        is_stage: bool
    ) -> "CompleteContext":
        """
        Generates a complete context from a PartialContext and the target context

        Args:
            pc: the partial context (project context)  
            costumes: a list of valid values for a costume dropdown
            sounds: a list of valid values for a sound dropdown
            is_stage: wether the target is the stage
        """
        return CompleteContext(
            scope_variables       = pc.scope_variables,
            scope_lists           = pc.scope_lists,
            global_variables  = pc.global_variables,
            local_variables = pc.local_variables,
            local_lists     = pc.local_lists,
            other_sprites         = pc.other_sprites,
            backdrops             = pc.backdrops,

            costumes              = costumes,
            sounds                = sounds,
            is_stage              = is_stage,
        )


__all__ = ["PartialContext", "CompleteContext"]

