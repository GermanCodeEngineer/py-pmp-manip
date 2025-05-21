from pypenguin.opcode_info import DropdownValueKind, InputMode

from pypenguin.core.asset          import FRCostume, FRSound, SRCostume, SRSound
from pypenguin.core.block          import (
    FRBlock, IRBlock, IRBlockReference, IRInputValue,
    SRBlock, SRScript, 
    SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, SRBlockOnlyInputValue, SRScriptInputValue,
    SRDropdownValue,
)
from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockCallMutation,
    FRCustomBlockArgumentMutation,
    SRCustomBlockMutation, SRCustomBlockCallMutation,
)
from pypenguin.core.comment        import FRComment, SRComment
from pypenguin.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
    SRCustomBlockOptype,
)
from pypenguin.core.enums          import SRSpriteRotationStyle, SRVideoState
from pypenguin.core.meta           import FRMeta, FRPenguinModPlatformMeta
from pypenguin.core.monitor        import FRMonitor, SRListMonitor
from pypenguin.core.project        import FRProject, SRProject
from pypenguin.core.target         import FRStage, FRSprite, SRStage, SRSprite
from pypenguin.core.vars_lists     import SRVariable, SRList

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
            "?+wI)AquGQlzMnn5I8tA": [1, "i"],
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
    "p": [13, "my list", "ta`eJd|abk.):i6vI0u}", 646, 561],
    "n": {
        "opcode": "control_if",
        "next": None,
        "parent": None,
        "inputs": {
            "SUBSTACK": [2, "o"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 528,
        "y": 1175,
    },
    "o": {
        "opcode": "data_changevariableby",
        "next": None,
        "parent": "n",
        "inputs": {
            "VALUE": [1, [4, "1"]],
        },
        "fields": {
            "VARIABLE": ["my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable", ""],
        },
        "shadow": False,
        "topLevel": False,
    },
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
        comment="j",
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
    "m": (12, "my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable", 446, 652),
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
            color=("#FF6680", "#FF4D6A", "#FF3355"),
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
            color=("#FF6680", "#FF4D6A", "#FF3355"),
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
            color=("#FF6680", "#FF4D6A", "#FF3355"),
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
            color=("#FF6680", "#FF4D6A", "#FF3355"),
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
    "p": (13, "my list", "ta`eJd|abk.):i6vI0u}", 646, 561),
    "n": FRBlock(
        opcode="control_if",
        next=None,
        parent=None,
        inputs={
            "SUBSTACK": (2, "o"),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=528,
        y=1175,
    ),
    "o": FRBlock(
        opcode="data_changevariableby",
        next=None,
        parent="n",
        inputs={
            "VALUE": (1, (4, "1")),
        },
        fields={
            "VARIABLE": ("my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable", ""),
        },
        shadow=False,
        top_level=False,
    ),
}

ALL_FR_BLOCKS_CLEAN: dict[str, FRBlock] = ALL_FR_BLOCKS | {
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
    "p": FRBlock(
        opcode="data_listcontents",
        next=None,
        parent=None,
        inputs={},
        fields={
            "LIST": ("my list", "ta`eJd|abk.):i6vI0u}", ""),
        },
        shadow=False,
        top_level=True,
        x=646,
        y=561,
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
        comment=SRComment(
            position=(1031, 348),
            size=(200, 200),
            is_minimized=False,
            text="hi from attached comment"
        ),
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
            main_color="#FF6680",
            prototype_color="#FF4D6A",
            outline_color="#FF3355",
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
    IRBlockReference(id="p"): IRBlock(
        opcode="data_listcontents",
        inputs={},
        dropdowns={
            "LIST": "my list",
        },
        comment=None,
        mutation=None,
        position=(646, 561),
        next=None,
        is_top_level=True,
    ),
    "n": IRBlock(
        opcode="control_if",
        inputs={
            "SUBSTACK": IRInputValue(
                mode=InputMode.SCRIPT,
                references=[IRBlockReference(id="o")],
                immediate_block=None,
                text=None,
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=(528, 1175),
        next=None,
        is_top_level=True,
    ),
    "o": IRBlock(
        opcode="data_changevariableby",
        inputs={
            "VALUE": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="1",
            ),
        },
        dropdowns={
            "VARIABLE": "my variable",
        },
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
    ),
}

SR_BLOCK_CUSTOM_OPCODE = SRCustomBlockOpcode(
    segments=(
        "do sth text",
        SRCustomBlockArgument(name="a text arg", type=SRCustomBlockArgumentType.STRING_NUMBER),
        "and bool",
        SRCustomBlockArgument(name="a bool arg", type=SRCustomBlockArgumentType.BOOLEAN),
    ),
)

ALL_SR_COMMENTS = {
    "j": SRComment(
        position=(1031, 348),
        size=(200, 200),
        is_minimized=False,
        text="hi from attached comment"
    ),
}

ALL_SR_SCRIPTS = [
    SRScript( # [0]
        position=(268, 220),
        blocks=[
            SRBlock(
                opcode="broadcast ([MESSAGE])",
                inputs={
                    "MESSAGE": SRBlockAndDropdownInputValue(
                        block=None, 
                        dropdown=SRDropdownValue(kind=DropdownValueKind.BROADCAST_MSG, value="my message"),
                    ),
                },
                dropdowns={},
                comment=None,
                mutation=None,
            ),
            SRBlock(
                opcode="glide (SECONDS) secs to ([TARGET])",
                inputs={
                    "SECONDS": SRBlockAndTextInputValue(block=None, text="1"),
                    "TARGET": SRBlockAndDropdownInputValue(
                        block=None, 
                        dropdown=SRDropdownValue(kind=DropdownValueKind.OBJECT, value="random position"),
                    ),
                },
                dropdowns={},
                comment=SRComment(
                    position=(1031, 348),
                    size=(200, 200),
                    is_minimized=False,
                    text="hi from attached comment"
                ),
                mutation=None,
            ),
        ],
    ), 
    SRScript( # [1]
        position=(304, 424),
        blocks=[
            SRBlock(
                opcode="pick random (OPERAND1) to (OPERAND2)",
                inputs={
                    "OPERAND1": SRBlockAndTextInputValue(
                        block=SRBlock(
                            opcode="value of [VARIABLE]",
                            inputs={},
                            dropdowns={
                                "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="my variable"),
                            },
                            comment=None,
                            mutation=None,
                        ),
                        text="1",
                    ),
                    "OPERAND2": SRBlockAndTextInputValue(
                        block=SRBlock(
                            opcode="join (STRING1) (STRING2)",
                            inputs={
                                "STRING1": SRBlockAndTextInputValue(block=None, text="apple "),
                                "STRING2": SRBlockAndTextInputValue(block=None, text="banana"),
                            },
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        text="10",
                    ),
                },
                dropdowns={},
                comment=None,
                mutation=None,
            ),
        ],
     ), 
     SRScript( # [2]
        position=(446, 652),
        blocks=[
            SRBlock(
                opcode="value of [VARIABLE]",
                inputs={},
                dropdowns={
                    "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="my variable"),
                },
                comment=None,
                mutation=None,
            ),
        ],
    ), 
    SRScript( # [3]
        position=(344, 799),
        blocks=[
            SRBlock(
                opcode="define custom block reporter",
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
                    main_color="#FF6680",
                    prototype_color="#FF4D6A",
                    outline_color="#FF3355",
                ),
            ),
        ],
    ),
    SRScript( # [4]
        position=(499, 933),
        blocks=[
            SRBlock(
                opcode="call custom block",
                inputs={
                    "a text arg": SRBlockAndTextInputValue(
                        block=SRBlock(
                            opcode="length of (TEXT)",
                            inputs={
                                "TEXT": SRBlockAndTextInputValue(block=None, text="apple"),
                            },
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        text="",
                     ),
                    "a bool arg": SRBlockOnlyInputValue(
                        block=SRBlock(
                            opcode="false",
                            inputs={},
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
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
            ),
        ],
    ), 
    SRScript( # [5]
        position=(646, 561),
        blocks=[
            SRBlock(
                opcode="value of [LIST]",
                inputs={},
                dropdowns={
                    "LIST": SRDropdownValue(kind=DropdownValueKind.LIST, value="my list"),
                },
                comment=None,
                mutation=None,
            ),
        ],
    ),
    SRScript( # [6]
        position=(528, 1175),
        blocks=[
            SRBlock(
                opcode="if <CONDITION> then {THEN}",
                inputs={
                    "CONDITION": SRBlockOnlyInputValue(block=None),
                    "THEN": SRScriptInputValue(
                        blocks=[
                            SRBlock(
                                opcode="change [VARIABLE] by (VALUE)",
                                inputs={
                                    "VALUE": SRBlockAndTextInputValue(block=None, text="1"),
                                },
                                dropdowns={
                                    "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="my variable"),
                                },
                                comment=None,
                                mutation=None,
                            ),
                        ],
                    )
                },
                dropdowns={},
                comment=None,
                mutation=None,
            ),
        ],
    ),
]

ALL_SR_BLOCKS = [
    *ALL_SR_SCRIPTS[0].blocks,
    *ALL_SR_SCRIPTS[1].blocks,
    ALL_SR_SCRIPTS[1].blocks[0].inputs["OPERAND1"].block,
    ALL_SR_SCRIPTS[1].blocks[0].inputs["OPERAND2"].block,
    *ALL_SR_SCRIPTS[2].blocks,
    *ALL_SR_SCRIPTS[3].blocks,
    *ALL_SR_SCRIPTS[4].blocks,
    ALL_SR_SCRIPTS[4].blocks[0].inputs["a text arg"].block,
    ALL_SR_SCRIPTS[4].blocks[0].inputs["a bool arg"].block,
    *ALL_SR_SCRIPTS[5].blocks,
    *ALL_SR_SCRIPTS[6].blocks,
    *ALL_SR_SCRIPTS[6].blocks[0].inputs["THEN"].blocks,
]






STAGE_DATA = {
    "isStage": True,
    "name": "Stage",
    "variables": {
        "`jEk@4|i[#Fk?(8x)AV.-my variable": [
            "my variable",
            0,
        ],
    },
    "lists": {
        "ta`eJd|abk.):i6vI0u}": [
            "my list",
            [],
        ],
    },
    "broadcasts": {
        "]zYMvs0rF)-eOEt26c|,": "my message",
    },
    "customVars": [],
    "blocks": {},
    "comments": {},
    "currentCostume": 0,
    "costumes": [
        {
            "name": "backdrop1",
            "dataFormat": "svg",
            "assetId": "cd21514d0531fdffb22204e0ec5ed84a",
            "md5ext": "cd21514d0531fdffb22204e0ec5ed84a.svg",
            "rotationCenterX": 240,
            "rotationCenterY": 180,
        },
    ],
    "sounds": [],
    "id": "p]_uD8#0^Q=ryfqeQLud",
    "volume": 100,
    "layerOrder": 0,
    "tempo": 60,
    "videoTransparency": 50,
    "videoState": "on",
    "textToSpeechLanguage": None,
}

FR_STAGE = FRStage(
    is_stage=True,
    name="Stage",
    variables={
        "`jEk@4|i[#Fk?(8x)AV.-my variable": ("my variable", 0),
    },
    lists={
        "ta`eJd|abk.):i6vI0u}": ("my list", []),
    },
    broadcasts={
        "]zYMvs0rF)-eOEt26c|,": "my message",
    },
    custom_vars=[],
    blocks={},
    comments={},
    current_costume=0,
    costumes=[
        FRCostume(
            name="backdrop1",
            asset_id="cd21514d0531fdffb22204e0ec5ed84a",
            data_format="svg",
            md5ext="cd21514d0531fdffb22204e0ec5ed84a.svg",
            rotation_center_x=240,
            rotation_center_y=180,
            bitmap_resolution=None,
        ),
    ],
    sounds=[],
    id="p]_uD8#0^Q=ryfqeQLud",
    volume=100,
    layer_order=0,
    tempo=60,
    video_transparency=50,
    video_state="on",
    text_to_speech_language=None,
)

SPRITE_DATA = {
    "isStage": False,
    "name": "Sprite1",
    "variables": {},
    "lists": {},
    "broadcasts": {},
    "customVars": [],
    "blocks": ALL_FR_BLOCK_DATAS,
    "comments": {
        "j": {
            "blockId": "b",
            "x": 1031,
            "y": 348,
            "width": 200,
            "height": 200,
            "minimized": False,
            "text": "hi from attached comment",
        },
    },
    "currentCostume": 0,
    "costumes": [
        {
            "name": "costume1",
            "bitmapResolution": 1,
            "dataFormat": "svg",
            "assetId": "c434b674f2da18ba13cdfe51dbc05ecc",
            "md5ext": "c434b674f2da18ba13cdfe51dbc05ecc.svg",
            "rotationCenterX": 26,
            "rotationCenterY": 46,
        },
    ],
    "sounds": [
        {
            "name": "Squawk",
            "assetId": "e140d7ff07de8fa35c3d1595bba835ac",
            "dataFormat": "wav",
            "rate": 48000,
            "sampleCount": 17867,
            "md5ext": "e140d7ff07de8fa35c3d1595bba835ac.wav",
        },
    ],
    "id": "5I9nI;7P)jdiR-_X;/%l",
    "volume": 100,
    "layerOrder": 1,
    "visible": True,
    "x": 0,
    "y": 0,
    "size": 100,
    "direction": 90,
    "draggable": False,
    "rotationStyle": "all around",
}

FR_SPRITE = FRSprite(
    is_stage=False,
    name="Sprite1",
    variables={},
    lists={},
    broadcasts={},
    custom_vars=[],
    blocks=ALL_FR_BLOCKS,
    comments={
        "j": FRComment(
            block_id="b",
            x=1031,
            y=348,
            width=200,
            height=200,
            minimized=False,
            text="hi from attached comment",
        ),
    },
    current_costume=0,
    costumes=[
        FRCostume(
            name="costume1",
            asset_id="c434b674f2da18ba13cdfe51dbc05ecc",
            data_format="svg",
            md5ext="c434b674f2da18ba13cdfe51dbc05ecc.svg",
            rotation_center_x=26,
            rotation_center_y=46,
            bitmap_resolution=1,
        ),
    ],
    sounds=[
        FRSound(
            name="Squawk",
            asset_id="e140d7ff07de8fa35c3d1595bba835ac",
            data_format="wav",
            md5ext="e140d7ff07de8fa35c3d1595bba835ac.wav",
            rate=48000,
            sample_count=17867,
        ),
    ],
    id="5I9nI;7P)jdiR-_X;/%l",
    volume=100,
    layer_order=1,
    visible=True,
    x=0,
    y=0,
    size=100,
    direction=90,
    draggable=False,
    rotation_style="all around",
)




FR_PROJECT = FRProject(
    targets=[
        FR_STAGE,
        FR_SPRITE,
    ],
    monitors=[
        FRMonitor(
            id="ta`eJd|abk.):i6vI0u}",
            mode="list",
            opcode="data_listcontents",
            params={
                "LIST": "my list",
            },
            sprite_name=None,
            value=[],
            x=5,
            y=5,
            visible=True,
            width=0,
            height=0,
            slider_min=None,
            slider_max=None,
            is_discrete=None,
        ),
    ],
    extension_data={},
    extensions=[],
    extension_urls={},
    meta=FRMeta(
        semver="3.0.0",
        vm="0.2.0",
        agent="",
        platform=FRPenguinModPlatformMeta(
            name="PenguinMod", 
            url="https://penguinmod.com/", 
            version="stable",
        ),
    ),
)

PROJECT_DATA = {
    "targets": [
        STAGE_DATA,
        SPRITE_DATA,
    ],
    "monitors": [
        {
            "id": "ta`eJd|abk.):i6vI0u}",
            "mode": "list",
            "opcode": "data_listcontents",
            "params": {
                "LIST": "my list",
            },
            "spriteName": None,
            "value": [],
            "width": 0,
            "height": 0,
            "x": 5,
            "y": 5,
            "visible": True,
        },
    ],
    "extensionData": {},
    "extensions": [],
    "meta": {
        "semver": "3.0.0",
        "vm": "0.2.0",
        "agent": "",
        "platform": {
            "name": "PenguinMod",
            "url": "https://penguinmod.com/",
            "version": "stable",
        },
    },
}


SR_STAGE = SRStage(
    scripts=[],
    comments=[],
    costume_index=0,
    costumes=[
        SRCostume(
            name="backdrop1",
            file_extension="svg",
            rotation_center=(240, 180),
            bitmap_resolution=1,
        ),
    ],
    sounds=[],
    volume=100,
)

SR_SPRITE = SRSprite(
    name="Sprite1",
    scripts=ALL_SR_SCRIPTS,
    comments=[],
    costume_index=0,
    costumes=[
        SRCostume(
            name="costume1",
            file_extension="svg",
            rotation_center=(26, 46),
            bitmap_resolution=1,
        ),
    ],
    sounds=[
        SRSound(name="Squawk", file_extension="wav"),
    ],
    volume=100,
    sprite_only_variables=[],
    sprite_only_lists=[],
    local_monitors=[],
    layer_order=1,
    is_visible=True,
    position=(0, 0),
    size=100,
    direction=90,
    is_draggable=False,
    rotation_style=SRSpriteRotationStyle.ALL_AROUND,
)

SR_PROJECT = SRProject(
    stage=SR_STAGE,
    sprites=[
        SR_SPRITE,
    ],
    all_sprite_variables=[
        SRVariable(name="my variable", current_value=0),
    ],
    all_sprite_lists=[
        SRList(name="my list", current_value=[]),
    ],
    tempo=60,
    video_transparency=50,
    video_state=SRVideoState.ON,
    text_to_speech_language=None,
    global_monitors=[
        SRListMonitor(
            opcode="value of [LIST]",
            dropdowns={
                "LIST": SRDropdownValue(kind=DropdownValueKind.LIST, value="my list"),
            },
            position=(-235, -175),
            is_visible=True,
            size=(100, 120),
        ),
    ],
    extensions=[],
)


