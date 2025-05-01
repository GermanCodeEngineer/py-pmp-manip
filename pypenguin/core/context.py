from typing      import TYPE_CHECKING, Any
from dataclasses import dataclass

from utility     import GreprClass

if TYPE_CHECKING:
    from opcode_info import DropdownValueKind


@dataclass(repr=False)
class PartialContext(GreprClass):
    """
    A temporary dataclass which stores the context for dropdown validation excluding sprite context.
    """
    _grepr = True
    _grepr_fields = ["scope_variables", "scope_lists", "all_sprite_variables", "sprite_only_variables", "sprite_only_lists", "other_sprites", "backdrops"]

    scope_variables: list[tuple["DropdownValueKind", Any]]
    scope_lists: list[tuple["DropdownValueKind", Any]]
    all_sprite_variables: list[tuple["DropdownValueKind", Any]]
    sprite_only_variables: dict[str|None, list[tuple["DropdownValueKind", Any]]]
    sprite_only_lists: dict[str|None, list[tuple["DropdownValueKind", Any]]]
    other_sprites: list[tuple["DropdownValueKind", Any]]
    backdrops: list[tuple["DropdownValueKind", Any]]

@dataclass(repr=False)
class CompleteContext(GreprClass):
    """
    A temporary dataclass which stores the context for dropdown validation including sprite context.
    """
    _grepr = True
    _grepr_fields = ["scope_variables", "scope_lists", "all_sprite_variables", "sprite_only_variables", "sprite_only_lists", "other_sprites", "backdrops", "costumes", "sounds", "is_stage"]

    scope_variables: list[tuple["DropdownValueKind", Any]]
    scope_lists: list[tuple["DropdownValueKind", Any]]
    all_sprite_variables: list[tuple["DropdownValueKind", Any]]
    sprite_only_variables: dict[str|None, list[tuple["DropdownValueKind", Any]]]
    sprite_only_lists: dict[str|None, list[tuple["DropdownValueKind", Any]]]
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
        Generates a complete context from a PartialContext and the target context.
        :param pc: the partial context (project context)  
        :param costumes: a list of valid values for a costume dropdown
        :param sounds: a list of valid values for a sound dropdown
        :param is_stage: wether the target is the stage
        """
        return CompleteContext(
            scope_variables       = pc.scope_variables,
            scope_lists           = pc.scope_lists,
            all_sprite_variables  = pc.all_sprite_variables,
            sprite_only_variables = pc.sprite_only_variables,
            sprite_only_lists     = pc.sprite_only_lists,
            other_sprites         = pc.other_sprites,
            backdrops             = pc.backdrops,

            costumes              = costumes,
            sounds                = sounds,
            is_stage              = is_stage,
        )
