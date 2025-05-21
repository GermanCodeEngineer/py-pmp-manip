from pytest import raises
from copy   import deepcopy

from pypenguin.utility            import InterToSecondConversionError
from pypenguin.opcode_info import info_api
from pypenguin.important_opcodes  import *

from pypenguin.core.block import IRBlockReference

from tests.core.constants import ALL_IR_BLOCKS, ALL_SR_SCRIPTS

def test_IRBlock_step_block_and_text_block_only():
    irblock = ALL_IR_BLOCKS[IRBlockReference(id="c")]
    _, values = irblock.step(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ALL_SR_SCRIPTS[4].blocks

def test_IRBlock_step_script():
    irblock = ALL_IR_BLOCKS[IRBlockReference(id="d")]
    _, values = irblock.step(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ALL_SR_SCRIPTS[0].blocks

def test_IRBlock_step_menu():
    irblock = ALL_IR_BLOCKS[IRBlockReference(id="e")]
    _, values = irblock.step(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ["_random_"]

def test_IRBlock_step_invalid_script_count():
    irblock = deepcopy(ALL_IR_BLOCKS[IRBlockReference(id="c")])
    irblock.inputs["a text arg"].references = [
        IRBlockReference(id="b"),
        IRBlockReference(id="d"),
        IRBlockReference(id="e"),
    ]
    with raises(InterToSecondConversionError):
        irblock.step(
            all_blocks=ALL_IR_BLOCKS,
            info_api=info_api,
        )

def test_IRBlock_step_missing_input():
    irblock = deepcopy(ALL_IR_BLOCKS["o"])
    del irblock.inputs["VALUE"]
    with raises(InterToSecondConversionError):
        irblock.step(
            all_blocks=ALL_IR_BLOCKS,
            info_api=info_api,
        )
