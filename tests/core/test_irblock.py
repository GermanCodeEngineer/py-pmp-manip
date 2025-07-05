from copy        import deepcopy
from dataclasses import field
from pytest      import raises

from pypenguin.opcode_info.data import info_api
from pypenguin.utility          import grepr_dataclass, ConversionError

from pypenguin.core.block_interface import InterToFirstIF
from pypenguin.core.block           import IRBlock


from tests.core.constants import ALL_FR_BLOCKS, ALL_FR_COMMENTS, ALL_IR_BLOCKS, ALL_SR_SCRIPTS


@grepr_dataclass(grepr_fields=["_block_ids"])
class TEST_InterToFirstIF(InterToFirstIF):
    _block_ids: list[str] = field(default_factory=list)

    def get_next_block_id(self, comment=False) -> str:
        block_id = self._block_ids[self._next_block_id_num - 1]
        self._next_block_id_num += 1
        return block_id



def test_IRBlock_from_menu_dropdown_value():
    expected_irblock = ALL_IR_BLOCKS["e"]
    opcode_info = info_api.get_info_by_old("motion_glideto")
    input_infos = opcode_info.get_old_input_ids_infos(block=ALL_IR_BLOCKS["b"], fti_if=None)
    irblock = IRBlock.from_menu_dropdown_value(dropdown_value="_random_", input_info=input_infos["TO"])
    assert irblock == expected_irblock


def test_IRBlock_get_references():
    assert set(ALL_IR_BLOCKS["d"].get_references()) == {"b"}
    assert set(ALL_IR_BLOCKS["b"].get_references()) == {"e", "t"}


def test_IRBlock_to_first_comment():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=["s"],
    )
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
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
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

def test_IRBlock_to_first_block_and_text_toplevel():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
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

def test_IRBlock_to_first_block_and_broadcast_dropdown_input():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
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
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
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

def test_IRBlock_to_first_2references():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
    irblock = ALL_IR_BLOCKS["t"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id="b",
        own_id="t",
    )
    assert frblock == ALL_FR_BLOCKS["t"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_variable_dropdown():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
    irblock = ALL_IR_BLOCKS["q"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id="o",
        own_id="q",
    )
    assert frblock == ALL_FR_BLOCKS["q"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_list_dropdown_tuple_block():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
    irblock = ALL_IR_BLOCKS["p"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="p",
    )
    assert frblock == ALL_FR_BLOCKS["p"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_broadcast_dropdown():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
    irblock = ALL_IR_BLOCKS["w"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="w",
    )
    assert frblock == ALL_FR_BLOCKS["w"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_standard_dropdown():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
    irblock = ALL_IR_BLOCKS["r"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="r",
    )
    assert frblock == ALL_FR_BLOCKS["r"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_empty_input():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
    irblock = ALL_IR_BLOCKS["r"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id=None,
        own_id="r",
    )
    assert frblock == ALL_FR_BLOCKS["r"]
    assert itf_if.added_blocks == {}
    assert itf_if.added_comments == {}

def test_IRBlock_to_first_empty_menu():
    itf_if = TEST_InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="Sprite1",
        _block_ids=[],
    )
    irblock = ALL_IR_BLOCKS["e"]
    frblock = irblock.to_first(
        itf_if=itf_if,
        info_api=info_api,
        parent_id="b",
        own_id="e",
    )
    assert frblock == ALL_FR_BLOCKS["e"]
    assert itf_if.added_blocks == {}
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

def test_IRBlock_to_second_substack():
    irblock = ALL_IR_BLOCKS["n"]
    _, values = irblock.to_second(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ALL_SR_SCRIPTS[6].blocks

def test_IRBlock_to_second_menu():
    irblock = ALL_IR_BLOCKS["e"]
    _, values = irblock.to_second(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ["_random_"]

def test_IRBlock_to_second_immediate_block():
    irblock = ALL_IR_BLOCKS["f"]
    _, values = irblock.to_second(
        all_blocks=ALL_IR_BLOCKS,
        info_api=info_api,
    )
    assert values == ALL_SR_SCRIPTS[1].blocks

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
