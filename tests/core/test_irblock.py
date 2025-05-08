from pytest import fixture, raises

from pypenguin.utility            import tuplify, DeserializationError, FSCError
from pypenguin.opcode_info        import InputMode
from pypenguin.opcode_info.groups import info_api
from pypenguin.important_opcodes  import *

from pypenguin.core.block          import FRBlock, IRBlock, IRBlockReference, IRInputValue
from pypenguin.core.block_api      import FTCAPI
from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockCallMutation, FRCustomBlockArgumentMutation,
    SRCustomBlockMutation, SRCustomBlockArgumentMutation,
)
from pypenguin.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
    SRCustomBlockOptype
)

from tests.core.test_block_api import ALL_IR_BLOCKS


def test_irblock_step_menu():
    irblock = IRBlock(
        opcode="sensing_touchingobjectmenu",
        inputs={},
        dropdowns={"TOUCHINGOBJECTMENU": "_mouse_"},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
    )
    _, values = irblock.step(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ["_mouse_"]

def test_irblock_step():
    pass

