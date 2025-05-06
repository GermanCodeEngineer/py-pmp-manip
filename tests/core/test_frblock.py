from pytest import fixture, raises

from pypenguin.utility            import tuplify, DeserializationError, FSCError
from pypenguin.opcode_info        import InputMode
from pypenguin.opcode_info.groups import info_api
from pypenguin.important_opcodes  import *

from pypenguin.core.block          import FRBlock, TRBlock, TRBlockReference, TRInputValue
from pypenguin.core.block_api      import FTCAPI
from pypenguin.core.block_mutation import FRCustomBlockMutation, FRCustomBlockCallMutation

from tests.core.test_block_api import ALL_FR_BLOCKS, ALL_SR_COMMENTS

@fixture
def block_api():
    return FTCAPI(
        blocks=ALL_FR_BLOCKS,
        block_comments=ALL_SR_COMMENTS,
    )

# FRBlock
def test_frblock_from_data():
    data = {
        "opcode": "event_broadcast",
        "next": None,
        "parent": None,
        "inputs": {
            "BROADCAST_INPUT": [
                1, [11, "hbn", "ajUzOI^,`@L4q@F6iXUp"],
            ],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 107,
        "y": 313,
    }
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.opcode    == data["opcode"]
    assert frblock.next      == data["next"]
    assert frblock.parent    == data["parent"]
    assert frblock.inputs    == tuplify(data["inputs"])
    assert frblock.fields    == tuplify(data["fields"])
    assert frblock.shadow    == data["shadow"]
    assert frblock.top_level == data["topLevel"]

def test_frblock_from_data_comment():
    data = {
        "opcode": "motion_glideto", 
        "next": None, 
        "parent": "e", 
        "inputs": {
            "SECS": [1, [4, "1"]], 
            "TO": [1, "k"],
        }, 
        "fields": {}, 
        "shadow": False, 
        "topLevel": False, 
        "comment": "j",
    }
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.x       == None
    assert frblock.y       == None
    assert frblock.comment == data["comment"]

def test_frblock_from_data_invalid_mutation():
    data = {
        "opcode": "event_broadcast",
        "next": None,
        "parent": None,
        "inputs": {
            "BROADCAST_INPUT": [
                1, [11, "hbn", "ajUzOI^,`@L4q@F6iXUp"],
            ],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 107,
        "y": 313,
        "mutation": {...},
    }
    with raises(DeserializationError):
        FRBlock.from_data(data, info_api=info_api)

def test_frblock_from_data_missing_mutation():
    data = {
        "opcode": "argument_reporter_boolean",
        "next": None,
        "parent": "a",
        "inputs": {},
        "fields": {
            "VALUE": ["boolean", "|%?~)R0k:KB.c`h[qvn("],
        },
        "shadow": True,
        "topLevel": False,
    }
    with raises(DeserializationError):
        FRBlock.from_data(data, info_api=info_api)

def test_frblock_from_data_valid_mutation():
    data = {
        "opcode": "procedures_prototype",
        "next": None,
        "parent": "h",
        "inputs": {
            "}G[ASqXh*6Yj)lUVOc`q": [
                1,
                "p"
            ],
            "@#z0NEJ4p%{?+(BDp~@F": [
                1,
                "q"
            ]
        },
        "fields": {},
        "shadow": True,
        "topLevel": False,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "proccode": "rep %b %s",
            "argumentids": "[\"}G[ASqXh*6Yj)lUVOc`q\",\"@#z0NEJ4p%{?+(BDp~@F\"]",
            "argumentnames": "[\"booleano\",\"number in\"]",
            "argumentdefaults": "[\"false\",\"\"]",
            "warp": "true",
            "returns": "true",
            "edited": "true",
            "optype": "\"string\"",
            "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]"
        }
    }
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.mutation == FRCustomBlockMutation.from_data(data["mutation"])


def test_frblock_from_tuple_not_top_level():
    data = [OPCODE_VAR_VALUE_NUM, "a variable", ",fe+c/836;:I2j}Z3N_D"]
    parent_id = "m"
    block = FRBlock.from_tuple(data, parent_id=parent_id)
    assert isinstance(block, FRBlock)
    assert block.opcode    == OPCODE_VAR_VALUE
    assert block.next      is None
    assert block.parent    == parent_id
    assert block.inputs    == {}
    assert block.fields    == {"VARIABLE": ("a variable", ",fe+c/836;:I2j}Z3N_D", "")}
    assert block.shadow    == False
    assert block.top_level == True
    assert block.x         is None
    assert block.y         is None
    assert block.comment   is None
    assert block.mutation  is None

    with raises(DeserializationError):
        FRBlock.from_tuple(data, parent_id=None)

def test_frblock_from_tuple_list_top_level():
    data = [OPCODE_LIST_VALUE_NUM, "a list", "FAp;aT9l%(^4R:g]NHc7", 460, 628]
    block = FRBlock.from_tuple(data, parent_id=None)
    assert isinstance(block, FRBlock)
    assert block.opcode    == OPCODE_LIST_VALUE
    assert block.next      is None
    assert block.parent    is None
    assert block.inputs    == {}
    assert block.fields    == {"LIST": ("a list", "FAp;aT9l%(^4R:g]NHc7", "")}
    assert block.shadow    == False
    assert block.top_level == False
    assert block.x         == data[3]
    assert block.y         == data[4]
    assert block.comment   is None
    assert block.mutation  is None

    with raises(DeserializationError):
        FRBlock.from_tuple(data, parent_id="q")

def test_frblock_from_tuple_invalid():
    with raises(DeserializationError):
        FRBlock.from_tuple([77, ..., ...], parent_id="q")


def test_frblock_step_cb_call(block_api: FTCAPI):    
    frblock = FRBlock(
        opcode="procedures_call",
        next=None,
        parent=None,
        inputs={
            "@#z0NEJ4p%{?+(BDp~@F": [1, [10, "7"]],
            "}G[ASqXh*6Yj)lUVOc`q": [2, "u"],
        },
        fields={},
        shadow=False,
        top_level=True,
        x=716,
        y=1167,
        comment=None,
        mutation=FRCustomBlockCallMutation(
            tag_name="mutation",
            children=[],
            proccode="rep %b %s",
            argument_ids=["}G[ASqXh*6Yj)lUVOc`q", "@#z0NEJ4p%{?+(BDp~@F"],
            warp=True,
            returns=True,
            edited=True,
            optype="string",
            color=["#FF6680", "#FF4D6A", "#FF3355"],
        ),
    )
    trblock = frblock.step(
        block_api=block_api,
        info_api=info_api,
        own_id="t",
    )
    assert isinstance(trblock, TRBlock)
    assert trblock.opcode == frblock.opcode
    from pypenguin.utility import grepr
    print(grepr(trblock.inputs["number in"]))
    {
    'number in': TRInputValue(
        mode=InputMode.BLOCK_AND_TEXT,
        references=[],
        immediate_block=None,
        text=None),
    'booleano': TRInputValue(
        mode=InputMode.BLOCK_ONLY,
        references=[
            TRBlockReference(id='u')],
        immediate_block=None,
        text=None)}
    assert trblock.inputs["number in"] == TRInputValue(
            mode=InputMode.BLOCK_AND_TEXT,
            references=[],
            immediate_block=None,
            text="7",
        )
    """assert trblock.inputs == {
        "booleano": TRInputValue(
            mode=InputMode.BLOCK_ONLY,
            references=[TRBlockReference(id="u")],
            immediate_block=None,
            text=None,
        ),
        "number in": TRInputValue(
            mode=InputMode.BLOCK_AND_TEXT,
            references=[],
            immediate_block=None,
            text="7",
        ),
    }"""

