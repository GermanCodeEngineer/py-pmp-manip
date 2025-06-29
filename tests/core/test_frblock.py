from copy   import deepcopy
from pytest import fixture, raises

from pypenguin.important_consts import (
    OPCODE_NUM_VAR_VALUE, OPCODE_VAR_VALUE, OPCODE_NUM_LIST_VALUE, OPCODE_LIST_VALUE,
    SHA256_SEC_VARIABLE, SHA256_SEC_LIST, SHA256_SEC_BROADCAST_MSG,
    SHA256_SEC_MAIN_ARGUMENT_NAME,
)
from pypenguin.opcode_info.data import info_api
from pypenguin.utility          import string_to_sha256, DeserializationError, ConversionError

from pypenguin.core.block_interface import FirstToInterIF
from pypenguin.core.block_mutation  import FRCustomBlockMutation, SRCustomBlockArgumentMutation
from pypenguin.core.block           import FRBlock, IRBlock
from pypenguin.core.vars_lists      import variable_sha256, list_sha256

from tests.core.constants import ALL_FR_BLOCK_DATAS, ALL_FR_BLOCKS, ALL_FR_BLOCKS_CLEAN, ALL_IR_BLOCKS, ALL_SR_COMMENTS


@fixture
def fti_if():
    return FirstToInterIF(
        blocks=ALL_FR_BLOCKS_CLEAN,
        block_comments=ALL_SR_COMMENTS,
    )



def test_FRBlock_from_data():
    data = ALL_FR_BLOCK_DATAS["d"]
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.opcode    == data["opcode"]
    assert frblock.next      == data["next"]
    assert frblock.parent    == data["parent"]
    assert frblock.inputs    == {
        "BROADCAST_INPUT": (1, 
            (11, "my message", string_to_sha256("my message", secondary=SHA256_SEC_BROADCAST_MSG)),
        ),
    }
    assert frblock.fields    == {}
    assert frblock.shadow    == data["shadow"]
    assert frblock.top_level == data["topLevel"]

def test_FRBlock_from_data_comment():
    data = ALL_FR_BLOCK_DATAS["b"]
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.x       is None
    assert frblock.y       is None
    assert frblock.comment == data["comment"]

def test_FRBlock_from_data_invalid_mutation():
    data = ALL_FR_BLOCK_DATAS["d"] | {"mutation": {...}}
    with raises(DeserializationError):
        FRBlock.from_data(data, info_api=info_api)

def test_FRBlock_from_data_missing_mutation():
    data = ALL_FR_BLOCK_DATAS["j"].copy()
    del data["mutation"]
    with raises(DeserializationError):
        FRBlock.from_data(data, info_api=info_api)

def test_FRBlock_from_data_valid_mutation():
    data = ALL_FR_BLOCK_DATAS["a"]
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.mutation == FRCustomBlockMutation(
        tag_name="mutation",
        children=[],
        proccode="do sth text %s and bool %b",
        argument_ids=[
            string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME), 
            string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME),
        ],
        argument_names=["a text arg", "a bool arg"],
        argument_defaults=["", "false"],
        warp=False,
        returns=True,
        edited=True,
        optype="number",
        color=("#FF6680", "#FF4D6A", "#FF3355"),
    )


def test_FRBlock_from_tuple_not_top_level():
    data = [OPCODE_NUM_VAR_VALUE, "a variable", variable_sha256("my variable", sprite_name="_stage_")]
    parent_id = "m"
    frblock = FRBlock.from_tuple(data, parent_id=parent_id)
    assert isinstance(frblock, FRBlock)
    assert frblock.opcode    == OPCODE_VAR_VALUE
    assert frblock.next      is None
    assert frblock.parent    == parent_id
    assert frblock.inputs    == {}
    assert frblock.fields    == {
        "VARIABLE": ("a variable", variable_sha256("my variable", sprite_name="_stage_"), ""),
    }
    assert frblock.shadow    is False
    assert frblock.top_level is False
    assert frblock.x         is None
    assert frblock.y         is None
    assert frblock.comment   is None
    assert frblock.mutation  is None

    with raises(ConversionError):
        FRBlock.from_tuple(data, parent_id=None)

def test_FRBlock_from_tuple_list_top_level():
    data = [OPCODE_NUM_LIST_VALUE, "a list", list_sha256("my list", sprite_name="_stage_"), 460, 628]
    frblock = FRBlock.from_tuple(data, parent_id=None)
    assert isinstance(frblock, FRBlock)
    assert frblock.opcode    == OPCODE_LIST_VALUE
    assert frblock.next      is None
    assert frblock.parent    is None
    assert frblock.inputs    == {}
    assert frblock.fields    == {"LIST": ("a list", list_sha256("my list", sprite_name="_stage_"), "list")}
    assert frblock.shadow    is False
    assert frblock.top_level is True
    assert frblock.x         == data[3]
    assert frblock.y         == data[4]
    assert frblock.comment   is None
    assert frblock.mutation  is None

    with raises(ConversionError):
        FRBlock.from_tuple(data, parent_id="qqq")

def test_FRBlock_from_tuple_invalid():
    with raises(ConversionError):
        FRBlock.from_tuple([1, 2], parent_id="qqq")

    with raises(ConversionError):
        FRBlock.from_tuple([77, ..., ...], parent_id="qqq")


def test_FRBlock_to_tuple_invalid_opcode():
    frblock = ALL_FR_BLOCKS_CLEAN["g"]
    with raises(ConversionError):
        frblock.to_tuple()

def test_FRBlock_to_tuple_variable_top_level():
    frblock = ALL_FR_BLOCKS_CLEAN["m"]
    assert frblock.to_tuple() == ALL_FR_BLOCKS["m"]

def test_FRBlock_to_tuple_list():
    frblock = ALL_FR_BLOCKS_CLEAN["p"]
    assert frblock.to_tuple() == ALL_FR_BLOCKS["p"]

def test_FRBlock_to_tuple_variable_not_top_level():
    sha256 = variable_sha256("my variable", sprite_name="_stage_")
    frblock = FRBlock(
        opcode    = OPCODE_VAR_VALUE,
        next      = None,
        parent    = "f",
        inputs    = {},
        fields    = {"VARIABLE": ("my variable", sha256, "")},
        shadow    = False,
        top_level = False,
        x         = None,
        y         = None,
        comment   = None,
        mutation  = None,
    )
    assert frblock.to_tuple() == (OPCODE_NUM_VAR_VALUE, "my variable", sha256)



def test_FRBlock_to_inter(fti_if: FirstToInterIF):
    frblock: FRBlock = ALL_FR_BLOCKS["f"]
    irblock = frblock.to_inter(
        fti_if=fti_if,
        info_api=info_api,
        own_id="f",
    )
    assert irblock == ALL_IR_BLOCKS["f"]

def test_FRBlock_to_inter_cb_def_pre_and_instead_handler(fti_if: FirstToInterIF):
    frblock: FRBlock = ALL_FR_BLOCKS["h"]
    irblock = frblock.to_inter(
        fti_if=fti_if,
        info_api=info_api,
        own_id="h",
    )
    assert irblock == ALL_IR_BLOCKS["h"]

def test_FRBlock_to_inter_cb_prototype(fti_if: FirstToInterIF):
    frblock: FRBlock = ALL_FR_BLOCKS["a"]
    irblock = frblock.to_inter(
        fti_if=fti_if,
        info_api=info_api,
        own_id="a",
    )
    assert isinstance(irblock, IRBlock) # An empty block which will be deleted in the next step
    assert irblock.opcode       == frblock.opcode
    assert irblock.inputs       == ...
    assert irblock.dropdowns    == ...
    assert irblock.position     == ...
    assert irblock.comment      == ...
    assert irblock.mutation     == ...
    assert irblock.next         == ...
    assert irblock.is_top_level == ...

def test_FRBlock_to_inter_cb_arg(fti_if: FirstToInterIF):
    frblock: FRBlock = ALL_FR_BLOCKS["i"]
    irblock = frblock.to_inter(
        fti_if=fti_if,
        info_api=info_api,
        own_id="i",
    )
    assert isinstance(irblock, IRBlock)
    assert irblock.opcode       == frblock.opcode
    assert irblock.inputs       == {}
    assert irblock.dropdowns    == {}
    assert irblock.position     is None
    assert irblock.comment      is None
    assert irblock.mutation     == SRCustomBlockArgumentMutation(
        argument_name="a text arg",
        main_color="#FF6680",
        prototype_color="#FF4D6A",
        outline_color="#FF3355",
    )
    assert irblock.next         is None
    assert irblock.is_top_level is False

def test_FRBlock_to_inter_cb_call(fti_if: FirstToInterIF):
    frblock: FRBlock = ALL_FR_BLOCKS["c"]
    irblock = frblock.to_inter(
        fti_if=fti_if,
        info_api=info_api,
        own_id="c",
    )
    assert irblock == ALL_IR_BLOCKS["c"]

def test_FRBlock_to_inter_invalid_input_element(fti_if: FirstToInterIF):
    frblock: FRBlock = deepcopy(ALL_FR_BLOCKS["g"])
    frblock.inputs["STRING1"] = (1, (10, "apple "), (40, "abc"))
    with raises(ConversionError):
        frblock.to_inter(
            fti_if=fti_if,
            info_api=info_api,
            own_id="g",
        )

