#from pytest import fixture, raises
#from copy   import copy

from pypenguin.utility import FSCError, lists_equal_ignore_order
from pypenguin.opcode_info import DropdownValueKind
from pypenguin.opcode_info.groups import info_api

from pypenguin.core.block_api      import FTCAPI, ValidationAPI
from pypenguin.core.block          import (
    FRBlock, SRBlock, SRBlockAndTextInputValue, 
    SRScript, SRBlockOnlyInputValue, SRDropdownValue
)
from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockCallMutation,
    FRCustomBlockArgumentMutation,
    SRCustomBlockMutation, SRCustomBlockCallMutation,
    SRCustomBlockArgumentMutation, SRStopScriptMutation,
)
from pypenguin.core.comment        import SRComment
from pypenguin.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
    SRCustomBlockOptype,
)
from pypenguin.core.project import SRProject
from pypenguin.core.target import FRSprite

from tests.core.test_block_api import ALL_FR_BLOCKS

sprite = FRSprite(
    is_stage=False,
    name="my sprite",
    variables={},
    lists={},
    broadcasts={},
    custom_vars=[],
    comments={},
    current_costume=0,
    costumes=[],
    sounds=[],
    id="okfrngerge",
    volume=0,
    layer_order=1,
    visible=True,
    direction=0,
    draggable=False,
    rotation_style="all around",
    blocks=ALL_FR_BLOCKS,
    x=100,
    y=100,
    size=100,
)
new_sprite, _, _ = sprite.step(info_api=info_api)
print(new_sprite.scripts)
