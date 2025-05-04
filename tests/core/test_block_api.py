from pytest import fixture, raises
from copy   import copy

from pypenguin.utility import FSCError

from pypenguin.core.block_api      import FTCAPI, ValidationAPI
from pypenguin.core.block          import FRBlock
from pypenguin.core.block_mutation import FRCustomBlockMutation, FRCustomBlockArgumentMutation
from pypenguin.core.comment        import SRComment

from tests.utility import execute_attr_validation_tests

ALL_BLOCKS = {
    "al": FRBlock(
        opcode="event_whenflagclicked",
        next="z",
        parent=None,
        inputs={},
        fields={},
        shadow=False,
        top_level=True,
        x=-616,
        y=-568,
        comment=None,
        mutation=None
    ), 
    "z": FRBlock(
        opcode="control_forever",
        next=None,
        parent="al",
        inputs={
            "SUBSTACK": (2, "am")},
        fields={},
        shadow=False,
        top_level=False,
        x=None,
        y=None,
        comment=None,
        mutation=None,
    ), 
    "am": FRBlock(
        opcode="control_if",
        next=None,
        parent="z",
        inputs={},
        fields={},
        shadow=False,
        top_level=False,
        x=None,
        y=None,
        comment=None,
        mutation="j",
    ),
    "h": FRBlock(
        opcode="procedures_definition_return",
        next=None,
        parent=None,
        inputs={
            "custom_block": (1, "b")},
        fields={},
        shadow=False,
        top_level=True,
        x=775,
        y=859,
        comment=None,
        mutation=None,
    ),
    "b": FRBlock(
        opcode="procedures_prototype",
        next=None,
        parent="h",
        inputs={
            "}G[ASqXh*6Yj)lUVOc`q": (1, "p"),
            "@#z0NEJ4p%{?+(BDp~@F": (1, "q")},
        fields={},
        shadow=True,
        top_level=False,
        x=None,
        y=None,
        comment=None,
        mutation=FRCustomBlockMutation(
            tag_name="mutation",
            children=[],
            proccode="rep %b %s",
            argument_ids=["}G[ASqXh*6Yj)lUVOc`q", "@#z0NEJ4p%{?+(BDp~@F"],
            argument_names=["booleano", "number in"],
            argument_defaults=["false", ""],
            warp=True,
            returns=True,
            edited=True,
            optype="string",
            color=("#FF6680", "#FF4D6A", "#FF3355")
        ),
    ),
    "p": FRBlock(
        opcode="argument_reporter_boolean",
        next=None,
        parent="b",
        inputs={},
        fields={
            "VALUE": ("booleano", "jb#5h4WJxZ*5[DJ]./?+")},
        shadow=True,
        top_level=False,
        x=None,
        y=None,
        comment=None,
        mutation=FRCustomBlockArgumentMutation(
            tag_name="mutation",
            children=[],
            color=("#FF6680", "#FF4D6A", "#FF3355")
        ),
    ),
    "q": FRBlock(
        opcode="argument_reporter_string_number",
        next=None,
        parent="b",
        inputs={},
        fields={
            "VALUE": ("number in", "8/qVRnf-YhH[,*vDNE[:")},
        shadow=True,
        top_level=False,
        x=None,
        y=None,
        comment=None,
        mutation=FRCustomBlockArgumentMutation(
            tag_name="mutation",
            children=[],
            color=("#FF6680", "#FF4D6A", "#FF3355"),
        ),
    ),
}

ALL_COMMENTS = {
    "j": SRComment(
        position=(1031, 348),
        size=(200, 200),
        is_minimized=False,
        text="hi from attached comment"
    )
}

@fixture
def ftcapi():
    return FTCAPI(
        blocks=ALL_BLOCKS,
        block_comments=ALL_COMMENTS,
    )

def test_ftcapi_get_all_blocks(ftcapi: FTCAPI):
    assert ftcapi.get_all_blocks() == ALL_BLOCKS

def test_ftcapi_get_blocks(ftcapi: FTCAPI):
    assert ftcapi.get_block("al") == ALL_BLOCKS["al"]

def test_ftcapi_schedule_block_deletion(ftcapi: FTCAPI):
    ftcapi_copy = copy(ftcapi)
    ftcapi_copy.schedule_block_deletion("z")
    assert ftcapi_copy.scheduled_block_deletions == ["z"]

def test_ftcapi_get_cb_mutation(ftcapi: FTCAPI):
    assert ftcapi.get_cb_mutation("rep %b %s") == ALL_BLOCKS["b"].mutation
    with raises(FSCError):
        ftcapi.get_cb_mutation("some %s proccode")

def test_ftcapi_get_comment(ftcapi: FTCAPI):
    assert ftcapi.get_comment("j") == ALL_COMMENTS["j"]

