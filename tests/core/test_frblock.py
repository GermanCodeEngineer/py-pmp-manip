from pytest import fixture, raises

from pypenguin.utility            import DeserializationError
from pypenguin.opcode_info        import InputMode
from pypenguin.opcode_info.groups import info_api
from pypenguin.important_opcodes  import *

from pypenguin.core.block          import FRBlock, IRBlock, IRBlockReference, IRInputValue
from pypenguin.core.block_api      import FICAPI
from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockCallMutation,
    SRCustomBlockMutation, SRCustomBlockCallMutation, SRCustomBlockArgumentMutation,
)
from pypenguin.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
    SRCustomBlockOptype
)

from tests.core.constants import ALL_FR_BLOCKS, ALL_FR_BLOCK_DATAS, ALL_SR_COMMENTS

@fixture
def ficapi():
    return FICAPI(
        blocks=ALL_FR_BLOCKS,
        block_comments=ALL_SR_COMMENTS,
    )

# FRBlock
def test_FRBlock_from_data():
    data = ALL_FR_BLOCK_DATAS["d"]
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.opcode    == data["opcode"]
    assert frblock.next      == data["next"]
    assert frblock.parent    == data["parent"]
    assert frblock.inputs    == {
        "BROADCAST_INPUT": (1, (11, "my message", "]zYMvs0rF)-eOEt26c|,")),
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
        argument_ids=["?+wI)AquGQlzMnn5I8tA", "1OrbjF=wjT?D$)m|0N=X"],
        argument_names=["a text arg", "a bool arg"],
        argument_defaults=["", "false"],
        warp=False,
        returns=True,
        edited=True,
        optype="number",
        color=("#FF6680", "#FF4D6A", "#FF3355"),
    )


def test_FRBlock_from_tuple_not_top_level():
    data = [OPCODE_VAR_VALUE_NUM, "a variable", ",fe+c/836;:I2j}Z3N_D"]
    parent_id = "m"
    frblock = FRBlock.from_tuple(data, parent_id=parent_id)
    assert isinstance(frblock, FRBlock)
    assert frblock.opcode    == OPCODE_VAR_VALUE
    assert frblock.next      is None
    assert frblock.parent    == parent_id
    assert frblock.inputs    == {}
    assert frblock.fields    == {"VARIABLE": ("a variable", ",fe+c/836;:I2j}Z3N_D", "")}
    assert frblock.shadow    is False
    assert frblock.top_level is False
    assert frblock.x         is None
    assert frblock.y         is None
    assert frblock.comment   is None
    assert frblock.mutation  is None

    with raises(DeserializationError):
        FRBlock.from_tuple(data, parent_id=None)

def test_FRBlock_from_tuple_list_top_level():
    data = [OPCODE_LIST_VALUE_NUM, "a list", "FAp;aT9l%(^4R:g]NHc7", 460, 628]
    frblock = FRBlock.from_tuple(data, parent_id=None)
    assert isinstance(frblock, FRBlock)
    assert frblock.opcode    == OPCODE_LIST_VALUE
    assert frblock.next      is None
    assert frblock.parent    is None
    assert frblock.inputs    == {}
    assert frblock.fields    == {"LIST": ("a list", "FAp;aT9l%(^4R:g]NHc7", "")}
    assert frblock.shadow    is False
    assert frblock.top_level is True
    assert frblock.x         == data[3]
    assert frblock.y         == data[4]
    assert frblock.comment   is None
    assert frblock.mutation  is None

    with raises(DeserializationError):
        FRBlock.from_tuple(data, parent_id="qqq")

def test_FRBlock_from_tuple_invalid():
    with raises(DeserializationError):
        FRBlock.from_tuple([77, ..., ...], parent_id="qqq")


def test_FRBlock_step(ficapi: FICAPI):
    # TODO: next
    frblock = ALL_FR_BLOCKS["f"]
    trblock = frblock.step(
        block_api=ficapi,
        info_api=info_api,
        own_id="f",
    )
    assert isinstance(trblock, IRBlock)
    assert trblock.opcode       == frblock.opcode
    assert trblock.inputs       == {
        "FROM": IRInputValue(
            mode=InputMode.BLOCK_AND_TEXT,
            references=[],
            immediate_block=IRBlock(
                opcode="data_variable",
                inputs={},
                dropdowns={
                    "VARIABLE": "my variable",
                },
                position=None,
                comment=None,
                mutation=None,
                next=None,
                is_top_level=False,
            ),
            text="1",
        ),
        "TO": IRInputValue(
            mode=InputMode.BLOCK_AND_TEXT,
            references=[IRBlockReference(id="g")],
            immediate_block=None,
            text="10",
        ),
    }
    assert trblock.dropdowns    == {}
    assert trblock.position     == (304, 424)
    assert trblock.comment      is None
    assert trblock.mutation     is None
    assert trblock.next         is None
    assert trblock.is_top_level is True

def test_FRBlock_step_cb_def(ficapi: FICAPI):
    frblock = ALL_FR_BLOCKS["h"]
    trblock = frblock.step(
        block_api=ficapi,
        info_api=info_api,
        own_id="h",
    )
    assert isinstance(trblock, IRBlock)
    assert trblock.opcode       == frblock.opcode
    assert trblock.inputs       == {}
    assert trblock.dropdowns    == {}
    assert trblock.position     == (344, 799)
    assert trblock.comment      is None
    assert trblock.mutation     == SRCustomBlockMutation(
        custom_opcode=SRCustomBlockOpcode(
            segments=(
                "do sth text",
                SRCustomBlockArgument(name="a text arg", type=SRCustomBlockArgumentType.STRING_NUMBER),
                "and bool",
                SRCustomBlockArgument(name="a bool arg", type=SRCustomBlockArgumentType.BOOLEAN),
            ),
        ),
        no_screen_refresh=False,
        optype=SRCustomBlockOptype.NUMBER_REPORTER,
        color1="#FF6680",
        color2="#FF4D6A", 
        color3="#FF3355",
    )
    assert trblock.next         is None
    assert trblock.is_top_level is True

def test_FRBlock_step_cb_prototype(ficapi: FICAPI):
    frblock = ALL_FR_BLOCKS["a"]
    trblock = frblock.step(
        block_api=ficapi,
        info_api=info_api,
        own_id="a",
    )
    assert isinstance(trblock, IRBlock) # An empty block which will be deleted in the next step
    assert trblock.opcode       == frblock.opcode
    assert trblock.inputs       == ...
    assert trblock.dropdowns    == ...
    assert trblock.position     == ...
    assert trblock.comment      == ...
    assert trblock.mutation     == ...
    assert trblock.next         == ...
    assert trblock.is_top_level == ...

def test_FRBlock_step_cb_arg(ficapi: FICAPI):
    frblock = ALL_FR_BLOCKS["i"]
    trblock = frblock.step(
        block_api=ficapi,
        info_api=info_api,
        own_id="i",
    )
    assert isinstance(trblock, IRBlock)
    assert trblock.opcode       == frblock.opcode
    assert trblock.inputs       == {}
    assert trblock.dropdowns    == {}
    assert trblock.position     is None
    assert trblock.comment      is None
    assert trblock.mutation     == SRCustomBlockArgumentMutation(
        argument_name="a text arg",
        color1="#FF6680",
        color2="#FF4D6A",
        color3="#FF3355",
    )
    assert trblock.next         is None
    assert trblock.is_top_level is False

def test_FRBlock_step_cb_call(ficapi: FICAPI):    
    frblock = ALL_FR_BLOCKS["c"]
    frblock = FRBlock(
        opcode="procedures_call",
        next=None,
        parent=None,
        inputs={
            "?+wI)AquGQlzMnn5I8tA": (3, "k", (10, "")),
            "1OrbjF=wjT?D$)m|0N=X": (2, "l"),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=499,
        y=933,
        mutation=FRCustomBlockCallMutation(
            tag_name="mutation",
            children=[],
            proccode="do sth text %s and bool %b",
            argument_ids=["?+wI)AquGQlzMnn5I8tA", "1OrbjF=wjT?D$)m|0N=X"],
            warp=False,
            returns=True,
            edited=True,
            optype="number",
            color=("#FF6680", "#FF4D6A", "#FF3355"),
        )
    )
    trblock = frblock.step(
        block_api=ficapi,
        info_api=info_api,
        own_id="t",
    )
    assert isinstance(trblock, IRBlock)
    assert trblock.opcode       == frblock.opcode
    assert trblock.inputs       == {
        "a text arg": IRInputValue(
            mode=InputMode.BLOCK_AND_TEXT,
            references=[IRBlockReference(id="k")],
            immediate_block=None,
            text="",
        ),
        "a bool arg": IRInputValue(
            mode=InputMode.BLOCK_ONLY,
            references=[IRBlockReference(id="l")],
            immediate_block=None,
            text=None,
        ),
    }
    assert trblock.dropdowns    == {}
    assert trblock.position     == (499, 933)
    assert trblock.comment      is None
    assert trblock.mutation     == SRCustomBlockCallMutation(
        custom_opcode=SRCustomBlockOpcode(
            segments=(
                "do sth text",
                SRCustomBlockArgument(name="a text arg", type=SRCustomBlockArgumentType.STRING_NUMBER),
                "and bool",
                SRCustomBlockArgument(name="a bool arg", type=SRCustomBlockArgumentType.BOOLEAN),
            ),
        ),
    )
    assert trblock.next         is None
    assert trblock.is_top_level is True

