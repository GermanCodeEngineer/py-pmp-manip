from copy   import deepcopy
from pytest import raises

from pypenguin.important_opcodes  import *
from pypenguin.opcode_info.data   import info_api
from pypenguin.utility            import ConversionError

from pypenguin.core.block_interface import InterToFirstIF


from tests.core.constants import ALL_FR_BLOCKS, ALL_IR_BLOCKS, ALL_SR_SCRIPTS


def test_IRBlock_to_first_block_and_text():
    itf_if = InterToFirstIF(blocks=ALL_IR_BLOCKS)
    irblock = ALL_IR_BLOCKS["c"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="c",
    )
    assert frblock == ALL_FR_BLOCKS["c"]
    assert itf_if.added_blocks == {id: ALL_FR_BLOCKS[id] for id in {}}
    assert itf_if.added_comments == {}


def test_IRBlock_to_second_block_and_text_block_only():
    irblock = ALL_IR_BLOCKS["c"]
    _, values = irblock.to_second(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ALL_SR_SCRIPTS[4].blocks

def test_IRBlock_to_second_script():
    irblock = ALL_IR_BLOCKS["d"]
    _, values = irblock.to_second(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ALL_SR_SCRIPTS[0].blocks

def test_IRBlock_to_second_menu():
    irblock = ALL_IR_BLOCKS["e"]
    _, values = irblock.to_second(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ["_random_"]

def test_IRBlock_to_second_invalid_script_count():
    irblock = deepcopy(ALL_IR_BLOCKS["c"])
    irblock.inputs["a text arg"].references = ["b", "d", "e"]
    with raises(ConversionError):
        irblock.to_second(
            all_blocks=ALL_IR_BLOCKS,
            info_api=info_api,
        )

def test_IRBlock_to_second_missing_input():
    irblock = deepcopy(ALL_IR_BLOCKS["o"])
    del irblock.inputs["VALUE"]
    with raises(ConversionError):
        irblock.to_second(
            all_blocks=ALL_IR_BLOCKS,
            info_api=info_api,
        )
