from pytest import fixture, raises
from copy   import copy

from pypenguin.utility import FSCError, lists_equal_ignore_order
from pypenguin.opcode_info import DropdownValueKind, InputMode

from pypenguin.core.block_api      import FTCAPI, ValidationAPI
from pypenguin.core.block          import (
    FRBlock, IRBlock, IRBlockReference, IRInputValue,
     SRBlock, SRBlockAndTextInputValue, 
    SRScript, SRBlockOnlyInputValue, SRDropdownValue
)
from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockCallMutation,
    FRCustomBlockArgumentMutation,
    SRCustomBlockMutation, SRCustomBlockCallMutation,
    SRCustomBlockArgumentMutation, SRStopScriptMutation,
)
from pypenguin.core.comment        import SRComment
from pypenguin.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
    SRCustomBlockOptype,
)

#1: frblock event_broadcast
#2: frblock motion_glideto (no pos + comment)
#5: frblock operator_random (with tuple block and normal block)
#6: frblock procedures_definition_return (with pos)
#4: frblock procedures_prototype
#3: frblock argument_reporter_boolean (missing mutation)
#7: frblock procedures_call (with pos and input block)

ALL_FR_BLOCK_DATAS = {
    "d": {
        "opcode": "event_broadcast",
        "next": "b",
        "parent": None,
        "inputs": {
            "BROADCAST_INPUT": [1, [11, "my message", "]zYMvs0rF)-eOEt26c|,"]],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 268,
        "y": 220,
    },
    "b": {
        "opcode": "motion_glideto",
        "next": None,
        "parent": "d",
        "inputs": {
            "SECS": [1, [4, "1"]],
            "TO": [1, "e"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": False,
        "comment": "j",
    },
    "e": {
        "opcode": "motion_glideto_menu",
        "next": None,
        "parent": "b",
        "inputs": {},
        "fields": {
            "TO": ["_random_", "@86dYv/6h#d_V/%rK3/M"],
        },
        "shadow": True,
        "topLevel": False,
    },
    "f": {
        "opcode": "operator_random",
        "next": None,
        "parent": None,
        "inputs": {
            "FROM": [
                3, [12, "my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable"], [4, "1"],
            ],
            "TO": [3, "g", [4, "10"]],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 304,
        "y": 424,
    },
    "m": [12, "my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable", 446, 652],
    "h": {
        "opcode": "procedures_definition_return",
        "next": None,
        "parent": None,
        "inputs": {
            "custom_block": [1, "a"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 344,
        "y": 799,
    },
    "a": {
        "opcode": "procedures_prototype",
        "next": None,
        "parent": "h",
        "inputs": {
            "?+wI]AquGQlzMnn5I8tA": [1, "i"],
            "1OrbjF=wjT?D$)m|0N=X": [1, "j"],
        },
        "fields": {},
        "shadow": True,
        "topLevel": False,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "proccode": "do sth text %s and bool %b",
            "argumentids": "[\"?+wI)AquGQlzMnn5I8tA\",\"1OrbjF=wjT?D$)m|0N=X\"]",
            "argumentnames": "[\"a text arg\",\"a bool arg\"]",
            "argumentdefaults": "[\"\",\"false\"]",
            "warp": "false",
            "returns": "true",
            "edited": "true",
            "optype": "\"number\"",
            "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
        },
    },
    "i": {
        "opcode": "argument_reporter_string_number",
        "next": None,
        "parent": "a",
        "inputs": {},
        "fields": {
            "VALUE": ["a text arg",";jX/UwBwE{CX@UdiwnJd"],
        },
        "shadow": True,
        "topLevel": False,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
        },
    },
    "j": {
        "opcode": "argument_reporter_boolean",
        "next": None,
        "parent": "a",
        "inputs": {},
        "fields": {
            "VALUE": ["a bool arg", "WM*d_x(VPqmUl[4GOC({"],
        },
        "shadow": True,
        "topLevel": False,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
        },
    },
    "g": {
        "opcode": "operator_join",
        "next": None,
        "parent": "f",
        "inputs": {
            "STRING1": [1, [10, "apple "]],
            "STRING2": [1, [10, "banana"]],
        },
        "fields": {},
        "shadow": False,
        "topLevel": False,
    },
    "c": {
        "opcode": "procedures_call",
        "next": None,
        "parent": None,
        "inputs": {
            "?+wI)AquGQlzMnn5I8tA": [3, "k", [10, ""]],
            "1OrbjF=wjT?D$)m|0N=X": [2, "l"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 499,
        "y": 933,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "proccode": "do sth text %s and bool %b",
            "argumentids": "[\"?+wI)AquGQlzMnn5I8tA\",\"1OrbjF=wjT?D$)m|0N=X\"]",
            "warp": "false",
            "returns": "true",
            "edited": "true",
            "optype": "\"number\"",
            "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
        },
    },
    "l": {
        "opcode": "operator_falseBoolean",
        "next": None,
        "parent": "c",
        "inputs": {},
        "fields": {},
        "shadow": False,
        "topLevel": False,
    },
    "k": {
        "opcode": "operator_length",
        "next": None,
        "parent": "c",
        "inputs": {
            "STRING": [1, [10, "apple"]],
        },
        "fields": {},
        "shadow": False,
        "topLevel": False,
    },
    "n": [13, "my list", "ta`eJd|abk.):i6vI0u}", 646, 561],
}

ALL_FR_BLOCKS = {
    "d": FRBlock(
        opcode="event_broadcast",
        next="b",
        parent=None,
        inputs={
            "BROADCAST_INPUT": (1, (11, "my message", "]zYMvs0rF)-eOEt26c|,")),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=268,
        y=220,
    ),
    "b": FRBlock(
        opcode="motion_glideto",
        next=None,
        parent="d",
        inputs={
            "SECS": (1, (4, "1")),
            "TO": (1, "e"),
        },
        fields={},
        shadow=False,
        top_level=False,
    ),
    "e": FRBlock(
        opcode="motion_glideto_menu",
        next=None,
        parent="b",
        inputs={},
        fields={
            "TO": ("_random_", "@86dYv/6h#d_V/%rK3/M"),
        },
        shadow=True,
        top_level=False,
    ),
    "f": FRBlock(
        opcode="operator_random",
        next=None,
        parent=None,
        inputs={
            "FROM": (
                3, (12, "my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable"), (4, "1"),
            ),
            "TO": (3, "g", (4, "10")),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=304,
        y=424,
    ),
    "m": FRBlock(
        opcode="data_variable",
        next=None,
        parent=None,
        inputs={},
        fields={
            "VARIABLE": ("my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable", ""),
        },
        shadow=False,
        top_level=True,
        x=446,
        y=652,
    ),
    "h": FRBlock(
        opcode="procedures_definition_return",
        next=None,
        parent=None,
        inputs={
            "custom_block": (1, "a"),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=344,
        y=799,
    ),
    "a": FRBlock(
        opcode="procedures_prototype",
        next=None,
        parent="h",
        inputs={
            "?+wI)AquGQlzMnn5I8tA": (1, "i"),
            "1OrbjF=wjT?D$)m|0N=X": (1, "j"),
        },
        fields={},
        shadow=True,
        top_level=False,
        mutation=FRCustomBlockMutation(
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
            color=["#FF6680", "#FF4D6A", "#FF3355"],
        ),
    ),
    "i": FRBlock(
        opcode="argument_reporter_string_number",
        next=None,
        parent="a",
        inputs={},
        fields={
            "VALUE": ("a text arg",";jX/UwBwE{CX@UdiwnJd"),
        },
        shadow=True,
        top_level=False,
        mutation=FRCustomBlockArgumentMutation(
            tag_name="mutation",
            children=[],
            color=["#FF6680", "#FF4D6A", "#FF3355"],
        ),
    ),
    "j": FRBlock(
        opcode="argument_reporter_boolean",
        next=None,
        parent="a",
        inputs={},
        fields={
            "VALUE": ("a bool arg", "WM*d_x(VPqmUl[4GOC({"),
        },
        shadow=True,
        top_level=False,
        mutation=FRCustomBlockArgumentMutation(
            tag_name="mutation",
            children=[],
            color=["#FF6680", "#FF4D6A", "#FF3355"],
        ),
    ),
    "g": FRBlock(
        opcode="operator_join",
        next=None,
        parent="f",
        inputs={
            "STRING1": (1, (10, "apple ")),
            "STRING2": (1, (10, "banana")),
        },
        fields={},
        shadow=False,
        top_level=False,
    ),
    "c": FRBlock(
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
            color=["#FF6680", "#FF4D6A", "#FF3355"],
        )
    ),
    "l": FRBlock(
        opcode="operator_falseBoolean",
        next=None,
        parent="c",
        inputs={},
        fields={},
        shadow=False,
        top_level=False,
    ),
    "k": FRBlock(
        opcode="operator_length",
        next=None,
        parent="c",
        inputs={
            "STRING": (1, (10, "apple")),
        },
        fields={},
        shadow=False,
        top_level=False,
    ),
    "n": FRBlock(
        opcode="data_variable",
        next=None,
        parent=None,
        inputs={},
        fields={
            "VARIABLE": ("my list", "ta`eJd|abk.):i6vI0u}", ""),
        },
        shadow=False,
        top_level=True,
        x=446,
        y=652,
    ),
}

ALL_IR_BLOCKS = {
    IRBlockReference(id="d"): IRBlock(
        opcode="event_broadcast",
        inputs={
            "BROADCAST_INPUT": IRInputValue(
                mode=InputMode.BLOCK_AND_BROADCAST_DROPDOWN,
                references=[],
                immediate_block=None,
                text="my message",
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=(268, 220),
        next=IRBlockReference(id="b"),
        is_top_level=True,
    ), 
    IRBlockReference(id="b"): IRBlock(
        opcode="motion_glideto",
        inputs={
            "SECS": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="1",
            ),
            "TO": IRInputValue(
                mode=InputMode.BLOCK_AND_DROPDOWN,
                references=[
                    IRBlockReference(id="e"),
                ],
                immediate_block=None,
                text=None,
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
    ), 
    IRBlockReference(id="e"): IRBlock(
        opcode="motion_glideto_menu",
        inputs={},
        dropdowns={
            "TO": "_random_",
        },
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
    ), 
    IRBlockReference(id="f"): IRBlock(
        opcode="operator_random",
        inputs={
            "FROM": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=IRBlock(
                    opcode="data_variable",
                    inputs={},
                    dropdowns={
                        "VARIABLE": "my variable",
                    },
                    comment=None,
                    mutation=None,
                    position=None,
                    next=None,
                    is_top_level=False,
                ),
                text="1",
            ),
            "TO": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[
                    IRBlockReference(id="g"),
                ],
                immediate_block=None,
                text="10",
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=(304, 424),
        next=None,
        is_top_level=True,
    ), 
    IRBlockReference(id="m"): IRBlock(
        opcode="data_variable",
        inputs={},
        dropdowns={
            "VARIABLE": "my variable",
        },
        comment=None,
        mutation=None,
        position=(446, 652),
        next=None,
        is_top_level=True,
    ), 
    IRBlockReference(id="h"): IRBlock(
        opcode="procedures_definition_return",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=SRCustomBlockMutation(
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
        ),
        position=(344, 799),
        next=None,
        is_top_level=True,
    ), 
    IRBlockReference(id="g"): IRBlock(
        opcode="operator_join",
        inputs={
            "STRING1": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="apple ",
            ),
            "STRING2": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="banana",
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
    ), 
    IRBlockReference(id="c"): IRBlock(
        opcode="procedures_call",
        inputs={
            "a text arg": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[
                    IRBlockReference(id="k"),
                ],
                immediate_block=None,
                text="",
            ),
            "a bool arg": IRInputValue(
                mode=InputMode.BLOCK_ONLY,
                references=[
                    IRBlockReference(id="l"),
                ],
                immediate_block=None,
                text=None,
            ),
        },
        dropdowns={},
        comment=None,
        mutation=SRCustomBlockCallMutation(
            custom_opcode=SRCustomBlockOpcode(
                segments=(
                    "do sth text",
                    SRCustomBlockArgument(name="a text arg", type=SRCustomBlockArgumentType.STRING_NUMBER),
                    "and bool",
                    SRCustomBlockArgument(name="a bool arg", type=SRCustomBlockArgumentType.BOOLEAN),
                ),
            ),
        ),
        position=(499, 933),
        next=None,
        is_top_level=True,
    ), 
    IRBlockReference(id="l"): IRBlock(
        opcode="operator_falseBoolean",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
    ), 
    IRBlockReference(id="k"): IRBlock(
        opcode="operator_length",
        inputs={
            "STRING": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="apple",
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
    ), 
    IRBlockReference(id="n"): IRBlock(
        opcode="data_variable",
        inputs={},
        dropdowns={
            "VARIABLE": "my list",
        },
        comment=None,
        mutation=None,
        position=(446, 652),
        next=None,
        is_top_level=True,
    ),
}

SR_BLOCK_CUSTOM_OPCODE = SRCustomBlockOpcode(
    segments=(
        "de",
        SRCustomBlockArgument(name="boolean", type=SRCustomBlockArgumentType.BOOLEAN),
        "label text",
    ),
)

ALL_SR_COMMENTS = {
    "j": SRComment(
        position=(1031, 348),
        size=(200, 200),
        is_minimized=False,
        text="hi from attached comment"
    ),
    "n": SRComment(
        position=(1019, 727),
        size=(200, 200),
        is_minimized=False,
        text="hi im a block comment",
    ),
}

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
    SRBlock(
        opcode="stop script [TARGET]",
        inputs={},
        dropdowns={
            "TARGET": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="all"),
        },
        comment=None,
        mutation=SRStopScriptMutation(is_ending_statement=True),
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
    return ValidationAPI(scripts=ALL_SR_SCRIPTS)


def test_ftcapi_get_all_blocks(ftcapi: FTCAPI):
    assert ftcapi.get_all_blocks() == ALL_FR_BLOCKS

def test_ftcapi_get_blocks(ftcapi: FTCAPI):
    assert ftcapi.get_block("d") == ALL_FR_BLOCKS["d"]

def test_ftcapi_schedule_block_deletion(ftcapi: FTCAPI):
    ftcapi_copy = copy(ftcapi)
    ftcapi_copy.schedule_block_deletion("z")
    assert ftcapi_copy.scheduled_block_deletions == ["z"]

def test_ftcapi_get_cb_mutation(ftcapi: FTCAPI):
    assert ftcapi.get_cb_mutation("do sth text %s and bool %b") == ALL_FR_BLOCKS["a"].mutation
    with raises(FSCError):
        ftcapi.get_cb_mutation("some %s proccode")

def test_ftcapi_get_comment(ftcapi: FTCAPI):
    assert ftcapi.get_comment("j") == ALL_SR_COMMENTS["j"]


def test_vapi_post_init(vapi: ValidationAPI):
    cb_mutations = {
        SR_BLOCK_CUSTOM_OPCODE: SRCustomBlockMutation(
            custom_opcode=SR_BLOCK_CUSTOM_OPCODE,
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


