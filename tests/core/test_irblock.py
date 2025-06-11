from copy        import deepcopy
from dataclasses import field
from pytest      import raises

from pypenguin.opcode_info.data import info_api
from pypenguin.utility          import grepr_dataclass, ConversionError

from pypenguin.core.block_interface import InterToFirstIF


from tests.core.constants import ALL_FR_BLOCKS, ALL_FR_COMMENTS, ALL_IR_BLOCKS, ALL_SR_SCRIPTS


@grepr_dataclass(grepr_fields=["_block_ids"], parent_cls=InterToFirstIF)
class TEST_InterToFirstIF(InterToFirstIF):
    _block_ids: list[str] = field(default_factory=list)

    def get_next_block_id(self) -> str:
        block_id = self._block_ids[self._next_block_id_num - 1]
        self._next_block_id_num += 1
        return block_id




def test_IRBlock_to_first_comment():
    itf_if = TEST_InterToFirstIF(blocks=ALL_IR_BLOCKS, _block_ids=["s"])
    irblock = ALL_IR_BLOCKS["b"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id="d",
        own_id="b",
    )
    assert frblock == ALL_FR_BLOCKS["b"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {id: ALL_FR_COMMENTS[id] for id in {"s"}}

def test_IRBlock_to_first_immediate_block_dropdowns_not_toplevel():
    itf_if = TEST_InterToFirstIF(blocks=ALL_IR_BLOCKS, _block_ids=[])
    irblock = ALL_IR_BLOCKS["f"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="f",
    )
    assert frblock == ALL_FR_BLOCKS["f"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_block_and_text_toplevel_1item():
    itf_if = TEST_InterToFirstIF(blocks=ALL_IR_BLOCKS, _block_ids=[])
    irblock = ALL_IR_BLOCKS["c"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="c",
    )
    assert frblock == ALL_FR_BLOCKS["c"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_block_and_broadcast_dropdown():
    itf_if = TEST_InterToFirstIF(blocks=ALL_IR_BLOCKS, _block_ids=[])
    irblock = ALL_IR_BLOCKS["d"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="d",
    )
    assert frblock == ALL_FR_BLOCKS["d"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_missing_input():
    itf_if = TEST_InterToFirstIF(blocks=ALL_IR_BLOCKS, _block_ids=[])
    irblock = ALL_IR_BLOCKS["n"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="n",
    )
    assert frblock == ALL_FR_BLOCKS["n"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}



# LEFT OFF HERE


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
