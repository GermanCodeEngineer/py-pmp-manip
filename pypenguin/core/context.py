from typing      import TYPE_CHECKING
from dataclasses import dataclass

from utility import GreprClass

if TYPE_CHECKING:
    from core.dropdown import SRDropdownValue

@dataclass(repr=False)
class PartialContext(GreprClass):
    _grepr = True
    _grepr_fields = ["scope_variables", "scope_lists", "all_sprite_variables", "sprite_only_variables", "sprite_only_lists", "other_sprites", "backdrops"]

    scope_variables: list["SRDropdownValue"]
    scope_lists: list["SRDropdownValue"]
    all_sprite_variables: list["SRDropdownValue"]
    sprite_only_variables: dict[str|None, list["SRDropdownValue"]]
    list["SRDropdownValue"]
    sprite_only_lists: dict[str|None, list["SRDropdownValue"]]
    other_sprites: list["SRDropdownValue"]
    backdrops: list["SRDropdownValue"]

@dataclass(repr=False)
class FullContext(GreprClass):
    _grepr = True
    _grepr_fields = ["scope_variables", "scope_lists", "all_sprite_variables", "sprite_only_variables", "sprite_only_lists", "other_sprites", "backdrops", "costumes", "sounds", "is_stage"]

    scope_variables: list["SRDropdownValue"]
    scope_lists: list["SRDropdownValue"]
    all_sprite_variables: list["SRDropdownValue"]
    sprite_only_variables: dict[str|None, list["SRDropdownValue"]]
    sprite_only_lists: dict[str|None, list["SRDropdownValue"]]
    other_sprites: list["SRDropdownValue"]
    backdrops: list["SRDropdownValue"]

    costumes: list["SRDropdownValue"]
    sounds: list["SRDropdownValue"]
    is_stage: bool

    @classmethod
    def from_partial(cls, pc: PartialContext, costumes: list["SRDropdownValue"], sounds: list["SRDropdownValue"], is_stage: bool) -> "FullContext":
        return FullContext(
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
