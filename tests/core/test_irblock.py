from pytest import fixture, raises
from copy   import copy

from pypenguin.utility            import tuplify, DeserializationError, FSCError
from pypenguin.opcode_info        import InputMode
from pypenguin.opcode_info.groups import info_api
from pypenguin.important_opcodes  import *

from pypenguin.core.block          import (
    IRBlock, IRBlockReference, IRInputValue, SRBlock,
)
from pypenguin.core.block_api      import FTCAPI
from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockCallMutation, FRCustomBlockArgumentMutation,
    SRCustomBlockMutation, SRCustomBlockArgumentMutation,
)
from pypenguin.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
    SRCustomBlockOptype
)

from tests.utility import copymodify

from tests.core.constants import ALL_IR_BLOCKS, ALL_SR_SCRIPTS


def test_irblock_step_block_reporter():
    irblock = ALL_IR_BLOCKS[IRBlockReference(id="g")]
    _, values = irblock.step(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == [ALL_SR_SCRIPTS[1].blocks[0].inputs["OPERAND2"].block]

def test_irblock_step_script():
    irblock = ALL_IR_BLOCKS[IRBlockReference(id="d")]
    _, values = irblock.step(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ALL_SR_SCRIPTS[0].blocks

def test_irblock_step_menu():
    irblock = ALL_IR_BLOCKS[IRBlockReference(id="e")]
    _, values = irblock.step(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ["_random_"]

def test_irblock_step_invalid_script_count():
    irblock = copy(ALL_IR_BLOCKS[IRBlockReference(id="c")])
    irblock.inputs["a text arg"].references = [
        IRBlockReference("b"),
        IRBlockReference("d"),
        IRBlockReference("e"),
    ]
    with raises(FSCError):
        irblock.step(
            all_blocks=ALL_IR_BLOCKS,
            info_api=info_api,
        )

