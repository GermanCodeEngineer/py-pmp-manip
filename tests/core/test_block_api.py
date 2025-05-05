from pytest import fixture, raises
from copy   import copy

from pypenguin.utility import FSCError, lists_equal_ignore_order

from pypenguin.core.block_api      import FTCAPI, ValidationAPI
from pypenguin.core.block          import FRBlock, SRBlock
from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockArgumentMutation,
    SRCustomBlockMutation, SRCustomBlockCallMutation,
)
from pypenguin.core.comment        import SRComment
from pypenguin.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
)

from tests.utility import execute_attr_validation_tests

ALL_FR_BLOCKS = {
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

ALL_SR_COMMENTS = {
    "j": SRComment(
        position=(1031, 348),
        size=(200, 200),
        is_minimized=False,
        text="hi from attached comment"
    )
}

SR_BLOCK_CUSTOM_OPCODE = SRCustomBlockOpcode(
    segments=(
        "de",
        SRCustomBlockArgument(name="boolean", type=SRCustomBlockArgumentType.BOOLEAN),
        "label text",
    ),
)

ALL_SR_BLOCKS = [
    SRBlock(
        opcode="define custom block",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=SRCustomBlockMutation(
            custom_opcode=SR_BLOCK_CUSTOM_OPCODE,
            no_screen_refresh=False,
            optype=SRCustomBlockOptype.STATEMENT,
            color1="#FF6680",
            color2="#FF4D6A",
            color3="#FF3355",
        ),
    ),
    SRBlock(
        opcode="say (MESSAGE) for (SECONDS) seconds",
        inputs={
            "MESSAGE": SRBlockAndTextInputValue(
                block=SRBlock(
                    opcode="not <OPERAND>",
                    inputs={
                        "OPERAND": SRBlockOnlyInputValue(
                            block=SRBlock(
                                opcode="value of boolean [ARGUMENT]",
                                inputs={},
                                dropdowns={},
                                comment=None,
                                mutation=SRCustomBlockArgumentMutation(
                                    argument_name="boolean",
                                    color1="#FF6680",
                                    color2="#FF4D6A",
                                    color3="#FF3355",
                                ),
                            ),
                        ),
                    },
                    dropdowns={},
                    comment=None,
                    mutation=None,
                ),
                text="Hello!",
            ),
            "SECONDS": SRBlockAndTextInputValue(block=None, text="2"),
        },
        dropdowns={},
        comment=None,
        mutation=None,
    ),
    SRBlock(
        opcode="not <OPERAND>",
        inputs={
            "OPERAND": SRBlockOnlyInputValue(
                block=SRBlock(
                    opcode="value of boolean [ARGUMENT]",
                    inputs={},
                    dropdowns={},
                    comment=None,
                    mutation=SRCustomBlockArgumentMutation(
                        argument_name="boolean",
                        color1="#FF6680",
                        color2="#FF4D6A",
                        color3="#FF3355",
                    ),
                ),
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
    ),
    SRBlock(
        opcode="value of boolean [ARGUMENT]",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=SRCustomBlockArgumentMutation(
            argument_name="boolean",
            color1="#FF6680",
            color2="#FF4D6A",
            color3="#FF3355",
        ),
    ),
    SRBlock(
        opcode="call custom block",
        inputs={
            "boolean": SRBlockOnlyInputValue(block=None),
        },
        dropdowns={},
        comment=None,
        mutation=SRCustomBlockCallMutation(
            custom_opcode=SR_BLOCK_CUSTOM_OPCODE,
        ),
    ),
    SRScript(
        position=(822, 1315),
        blocks=[
            SRBlock(
                opcode="stop script [TARGET]",
                inputs={},
                dropdowns={
                    "TARGET": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="all"),
                },
                comment=None,
                mutation=SRStopScriptMutation(is_ending_statement=True),
            ),
        ],
    ),
]

ALL_SR_SCRIPTS = [
    SRScript(
        position=(407, 917),
        blocks=[
            SRBlock(
                opcode="define custom block",
                inputs={},
                dropdowns={},
                comment=None,
                mutation=SRCustomBlockMutation(
                    custom_opcode=SR_BLOCK_CUSTOM_OPCODE,
                    no_screen_refresh=False,
                    optype=SRCustomBlockOptype.STATEMENT,
                    color1="#FF6680",
                    color2="#FF4D6A",
                    color3="#FF3355",
                ),
            ),
            SRBlock(
                opcode="say (MESSAGE) for (SECONDS) seconds",
                inputs={
                    "MESSAGE": SRBlockAndTextInputValue(
                        block=SRBlock(
                            opcode="not <OPERAND>",
                            inputs={
                                "OPERAND": SRBlockOnlyInputValue(
                                    block=SRBlock(
                                        opcode="value of boolean [ARGUMENT]",
                                        inputs={},
                                        dropdowns={},
                                        comment=None,
                                        mutation=SRCustomBlockArgumentMutation(
                                            argument_name="boolean",
                                            color1="#FF6680",
                                            color2="#FF4D6A",
                                            color3="#FF3355",
                                        ),
                                    ),
                                ),
                            },
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        text="Hello!",
                    ),
                    "SECONDS": SRBlockAndTextInputValue(block=None, text="2"),
                },
                dropdowns={},
                comment=None,
                mutation=None,
            ),
        ]
    ),
    SRScript(
        position=(534, 945),
        blocks=[
            SRBlock(
                opcode="call custom block",
                inputs={
                    "boolean": SRBlockOnlyInputValue(block=None),
                },
                dropdowns={},
                comment=None,
                mutation=SRCustomBlockCallMutation(
                    custom_opcode=SR_BLOCK_CUSTOM_OPCODE,
                ),
            ),
        ],
    ), 
    SRScript(
        position=(822, 1315),
        blocks=[
            SRBlock(
                opcode="stop script [TARGET]",
                inputs={},
                dropdowns={
                    "TARGET": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="all"),
                },
                comment=None,
                mutation=SRStopScriptMutation(is_ending_statement=True),
            ),
        ],
    ),
]


@fixture
def ftcapi():
    return FTCAPI(
        blocks=ALL_FR_BLOCKS,
        block_comments=ALL_SR_COMMENTS,
    )

@fixture
def vapi():
    return ValidationAPI()


def test_ftcapi_get_all_blocks(ftcapi: FTCAPI):
    assert ftcapi.get_all_blocks() == ALL_FR_BLOCKS

def test_ftcapi_get_blocks(ftcapi: FTCAPI):
    assert ftcapi.get_block("al") == ALL_FR_BLOCKS["al"]

def test_ftcapi_schedule_block_deletion(ftcapi: FTCAPI):
    ftcapi_copy = copy(ftcapi)
    ftcapi_copy.schedule_block_deletion("z")
    assert ftcapi_copy.scheduled_block_deletions == ["z"]

def test_ftcapi_get_cb_mutation(ftcapi: FTCAPI):
    assert ftcapi.get_cb_mutation("rep %b %s") == ALL_FR_BLOCKS["b"].mutation
    with raises(FSCError):
        ftcapi.get_cb_mutation("some %s proccode")

def test_ftcapi_get_comment(ftcapi: FTCAPI):
    assert ftcapi.get_comment("j") == ALL_SR_COMMENTS["j"]


def test_vapi_post_init(vapi: ValidationAPI):
    cb_mutations = {
        SR_BLOCK_CUSTOM_OPCODE: SRCustomBlockMutation(
            custom_opcode=custom_opcode,
            no_screen_refresh=False,
            optype=SRCustomBlockOptype.STATEMENT,
            color1="#FF6680",
            color2="#FF4D6A",
            color3="#FF3355",
        ),
    }
    assert vapi.cb_mutations == cb_mutations


def test_vapi_get_all_blocks(vapi: ValidationAPI):
    assert lists_equal_ignore_order(vapi.get_all_blocks(), ALL_SR_BLOCKS)

def test_vapi_get_cb_mutation(vapi: ValidationAPI):
    assert vapi.get_cb_mutation(SR_BLOCK_CUSTOM_OPCODE) == vapi.cb_mutations[SR_BLOCK_CUSTOM_OPCODE]


