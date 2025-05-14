from pytest import fixture, raises
from copy   import copy, deepcopy

from pypenguin.utility            import (
    ValidationConfig, 
    TypeValidationError, RangeValidationError, InvalidOpcodeError, InvalidBlockShapeError,
    UnnecessaryInputError, MissingInputError, UnnecessaryDropdownError, MissingDropdownError,
)
from pypenguin.opcode_info.groups import info_api
from pypenguin.opcode_info        import DropdownValueKind, OpcodeType, InputType

from pypenguin.core.asset          import FRCostume, FRSound
from pypenguin.core.block          import FRBlock
from pypenguin.core.block_api      import ValidationAPI
from pypenguin.core.block_mutation import FRCustomBlockMutation, FRCustomBlockArgumentMutation, FRCustomBlockCallMutation
from pypenguin.core.comment        import FRComment
from pypenguin.core.context        import CompleteContext
from pypenguin.core.dropdown       import SRDropdownValue
from pypenguin.core.meta           import FRMeta, FRPenguinModPlatformMeta
from pypenguin.core.monitor        import FRMonitor
from pypenguin.core.project        import FRProject
from pypenguin.core.target         import FRStage, FRSprite


from tests.core.constants import ALL_SR_SCRIPTS

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()

@fixture
def validation_api():
    return ValidationAPI(
        scripts=ALL_SR_SCRIPTS,
    )

@fixture
def context():
    return CompleteContext(
        scope_variables=[(DropdownValueKind.VARIABLE, "my variable")],
        scope_lists=[(DropdownValueKind.LIST, "my list")],

        all_sprite_variables=[(DropdownValueKind.VARIABLE, "my variable")],

        sprite_only_variables=[],
        sprite_only_lists=[],

        other_sprites=[],
        backdrops=[],
        costumes=[],
        sounds=[],

        is_stage=False,
    )

PROJECT_DATA = {
    "targets": [
        {
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
        },
        {
            "isStage": False,
            "name": "Sprite1",
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "customVars": [],
            "blocks": {
                "d": {
                    "opcode": "event_broadcast",
                    "next": "b",
                    "parent": None,
                    "inputs": {
                        "BROADCAST_INPUT": [
                            1,
                            [
                                11,
                                "my message",
                                "]zYMvs0rF)-eOEt26c|,",
                            ],
                        ],
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
                        "SECS": [
                            1,
                            [
                                4,
                                "1",
                            ],
                        ],
                        "TO": [
                            1,
                            "f",
                        ],
                    },
                    "fields": {},
                    "shadow": False,
                    "topLevel": False,
                    "comment": "e",
                },
                "f": {
                    "opcode": "motion_glideto_menu",
                    "next": None,
                    "parent": "b",
                    "inputs": {},
                    "fields": {
                        "TO": [
                            "_random_",
                            "@86dYv/6h#d_V/%rK3/M",
                        ],
                    },
                    "shadow": True,
                    "topLevel": False,
                },
                "g": {
                    "opcode": "operator_random",
                    "next": None,
                    "parent": None,
                    "inputs": {
                        "FROM": [
                            3,
                            [
                                12,
                                "my variable",
                                "`jEk@4|i[#Fk?(8x)AV.-my variable",
                            ],
                            [
                                4,
                                "1",
                            ],
                        ],
                        "TO": [
                            3,
                            "h",
                            [
                                4,
                                "10",
                            ],
                        ],
                    },
                    "fields": {},
                    "shadow": False,
                    "topLevel": True,
                    "x": 304,
                    "y": 424,
                },
                "i": {
                    "opcode": "procedures_definition_return",
                    "next": None,
                    "parent": None,
                    "inputs": {
                        "custom_block": [
                            1,
                            "a",
                        ],
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
                    "parent": "i",
                    "inputs": {
                        "?+wI)AquGQlzMnn5I8tA": [
                            1,
                            "j",
                        ],
                        "1OrbjF=wjT?D$)m|0N=X": [
                            1,
                            "k",
                        ],
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
                "j": {
                    "opcode": "argument_reporter_string_number",
                    "next": None,
                    "parent": "a",
                    "inputs": {},
                    "fields": {
                        "VALUE": [
                            "a text arg",
                            ";jX/UwBwE{CX@UdiwnJd",
                        ],
                    },
                    "shadow": True,
                    "topLevel": False,
                    "mutation": {
                        "tagName": "mutation",
                        "children": [],
                        "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
                    },
                },
                "k": {
                    "opcode": "argument_reporter_boolean",
                    "next": None,
                    "parent": "a",
                    "inputs": {},
                    "fields": {
                        "VALUE": [
                            "a bool arg",
                            "WM*d_x(VPqmUl[4GOC({",
                        ],
                    },
                    "shadow": True,
                    "topLevel": False,
                    "mutation": {
                        "tagName": "mutation",
                        "children": [],
                        "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
                    },
                },
                "h": {
                    "opcode": "operator_join",
                    "next": None,
                    "parent": "g",
                    "inputs": {
                        "STRING1": [
                            1,
                            [
                                10,
                                "apple ",
                            ],
                        ],
                        "STRING2": [
                            1,
                            [
                                10,
                                "banana",
                            ],
                        ],
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
                        "?+wI)AquGQlzMnn5I8tA": [
                            3,
                            "l",
                            [
                                10,
                                "",
                            ],
                        ],
                        "1OrbjF=wjT?D$)m|0N=X": [
                            2,
                            "m",
                        ],
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
                "m": {
                    "opcode": "operator_falseBoolean",
                    "next": None,
                    "parent": "c",
                    "inputs": {},
                    "fields": {},
                    "shadow": False,
                    "topLevel": False,
                },
                "l": {
                    "opcode": "operator_length",
                    "next": None,
                    "parent": "c",
                    "inputs": {
                        "STRING": [
                            1,
                            [
                                10,
                                "apple",
                            ],
                        ],
                    },
                    "fields": {},
                    "shadow": False,
                    "topLevel": False,
                },
                "p": [
                    12,
                    "my variable",
                    "`jEk@4|i[#Fk?(8x)AV.-my variable",
                    446,
                    652,
                ],
                "q": [
                    13,
                    "my list",
                    "ta`eJd|abk.):i6vI0u}",
                    646,
                    561,
                ],
                "r": {
                    "opcode": "argument_reporter_string_number",
                    "next": None,
                    "parent": "a",
                    "inputs": {},
                    "fields": {
                        "VALUE": [
                            "a text arg",
                            "^yv5=2v`Ry/g^Z`)Ys.1",
                        ],
                    },
                    "shadow": True,
                    "topLevel": False,
                    "mutation": {
                        "tagName": "mutation",
                        "children": [],
                        "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
                    },
                },
                "s": {
                    "opcode": "argument_reporter_boolean",
                    "next": None,
                    "parent": "a",
                    "inputs": {},
                    "fields": {
                        "VALUE": [
                            "a bool arg",
                            "2z2~7Noo4%=i2{EWKf(_",
                        ],
                    },
                    "shadow": True,
                    "topLevel": False,
                    "mutation": {
                        "tagName": "mutation",
                        "children": [],
                        "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
                    },
                },
                "t": {
                    "opcode": "argument_reporter_string_number",
                    "next": None,
                    "parent": "a",
                    "inputs": {},
                    "fields": {
                        "VALUE": [
                            "a text arg",
                            "^#w/pW=4-9Dq9)klf:9x",
                        ],
                    },
                    "shadow": True,
                    "topLevel": False,
                    "mutation": {
                        "tagName": "mutation",
                        "children": [],
                        "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
                    },
                },
                "u": {
                    "opcode": "argument_reporter_boolean",
                    "next": None,
                    "parent": "a",
                    "inputs": {},
                    "fields": {
                        "VALUE": [
                            "a bool arg",
                            "5gbANC]?3[@Ynp:~POWJ",
                        ],
                    },
                    "shadow": True,
                    "topLevel": False,
                    "mutation": {
                        "tagName": "mutation",
                        "children": [],
                        "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]",
                    },
                },
                "n": {
                    "opcode": "control_if",
                    "next": None,
                    "parent": None,
                    "inputs": {
                        "SUBSTACK": [
                            2,
                            "o",
                        ],
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
                        "VALUE": [
                            1,
                            [
                                4,
                                "1",
                            ],
                        ],
                    },
                    "fields": {
                        "VARIABLE": [
                            "my variable",
                            "`jEk@4|i[#Fk?(8x)AV.-my variable",
                            "",
                        ],
                    },
                    "shadow": False,
                    "topLevel": False,
                },
            },
            "comments": {
                "e": {
                    "blockId": "b",
                    "x": 620.6666690685131,
                    "y": 276.1481481481487,
                    "width": 200,
                    "height": 200,
                    "minimized": False,
                    "text": "im a comment",
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
        },
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

FR_PROJECT = FRProject(
    targets=[
        FRStage(
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
        ),
        FRSprite(
            is_stage=False,
            name="Sprite1",
            variables={},
            lists={},
            broadcasts={},
            custom_vars=[],
            blocks={
                "d": FRBlock(
                    opcode="event_broadcast",
                    next="b",
                    parent=None,
                    inputs={
                        "BROADCAST_INPUT": (1, (
                                11,
                                "my message",
                                "]zYMvs0rF)-eOEt26c|,",
                            )),
                    },
                    fields={},
                    shadow=False,
                    top_level=True,
                    x=268,
                    y=220,
                    comment=None,
                    mutation=None,
                ),
                "b": FRBlock(
                    opcode="motion_glideto",
                    next=None,
                    parent="d",
                    inputs={
                        "SECS": (1, (4, "1")),
                        "TO": (1, "f"),
                    },
                    fields={},
                    shadow=False,
                    top_level=False,
                    x=None,
                    y=None,
                    comment="e",
                    mutation=None,
                ),
                "f": FRBlock(
                    opcode="motion_glideto_menu",
                    next=None,
                    parent="b",
                    inputs={},
                    fields={
                        "TO": ("_random_", "@86dYv/6h#d_V/%rK3/M"),
                    },
                    shadow=True,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=None,
                ),
                "g": FRBlock(
                    opcode="operator_random",
                    next=None,
                    parent=None,
                    inputs={
                        "FROM": (
                            3,
                            (
                                12,
                                "my variable",
                                "`jEk@4|i[#Fk?(8x)AV.-my variable",
                            ),
                            (4, "1"),
                        ),
                        "TO": (
                            3,
                            "h",
                            (4, "10"),
                        ),
                    },
                    fields={},
                    shadow=False,
                    top_level=True,
                    x=304,
                    y=424,
                    comment=None,
                    mutation=None,
                ),
                "i": FRBlock(
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
                    comment=None,
                    mutation=None,
                ),
                "a": FRBlock(
                    opcode="procedures_prototype",
                    next=None,
                    parent="i",
                    inputs={
                        "?+wI)AquGQlzMnn5I8tA": (1, "j"),
                        "1OrbjF=wjT?D$)m|0N=X": (1, "k"),
                    },
                    fields={},
                    shadow=True,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=FRCustomBlockMutation(
                        tag_name="mutation",
                        children=[],
                        proccode="do sth text %s and bool %b",
                        argument_ids=[
                            "?+wI)AquGQlzMnn5I8tA",
                            "1OrbjF=wjT?D$)m|0N=X",
                        ],
                        argument_names=[
                            "a text arg",
                            "a bool arg",
                        ],
                        argument_defaults=[
                            "",
                            "false",
                        ],
                        warp=False,
                        returns=True,
                        edited=True,
                        optype="number",
                        color=(
                            "#FF6680",
                            "#FF4D6A",
                            "#FF3355",
                        ),
                    ),
                ),
                "j": FRBlock(
                    opcode="argument_reporter_string_number",
                    next=None,
                    parent="a",
                    inputs={},
                    fields={
                        "VALUE": ("a text arg", ";jX/UwBwE{CX@UdiwnJd"),
                    },
                    shadow=True,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=FRCustomBlockArgumentMutation(
                        tag_name="mutation",
                        children=[],
                        color=(
                            "#FF6680",
                            "#FF4D6A",
                            "#FF3355",
                        ),
                    ),
                ),
                "k": FRBlock(
                    opcode="argument_reporter_boolean",
                    next=None,
                    parent="a",
                    inputs={},
                    fields={
                        "VALUE": ("a bool arg", "WM*d_x(VPqmUl[4GOC({"),
                    },
                    shadow=True,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=FRCustomBlockArgumentMutation(
                        tag_name="mutation",
                        children=[],
                        color=(
                            "#FF6680",
                            "#FF4D6A",
                            "#FF3355",
                        ),
                    ),
                ),
                "h": FRBlock(
                    opcode="operator_join",
                    next=None,
                    parent="g",
                    inputs={
                        "STRING1": (1, (10, "apple ")),
                        "STRING2": (1, (10, "banana")),
                    },
                    fields={},
                    shadow=False,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=None,
                ),
                "c": FRBlock(
                    opcode="procedures_call",
                    next=None,
                    parent=None,
                    inputs={
                        "?+wI)AquGQlzMnn5I8tA": (
                            3,
                            "l",
                            (10, ""),
                        ),
                        "1OrbjF=wjT?D$)m|0N=X": (2, "m"),
                    },
                    fields={},
                    shadow=False,
                    top_level=True,
                    x=499,
                    y=933,
                    comment=None,
                    mutation=FRCustomBlockCallMutation(
                        tag_name="mutation",
                        children=[],
                        proccode="do sth text %s and bool %b",
                        argument_ids=[
                            "?+wI)AquGQlzMnn5I8tA",
                            "1OrbjF=wjT?D$)m|0N=X",
                        ],
                        warp=False,
                        returns=True,
                        edited=True,
                        optype="number",
                        color=(
                            "#FF6680",
                            "#FF4D6A",
                            "#FF3355",
                        ),
                    ),
                ),
                "m": FRBlock(
                    opcode="operator_falseBoolean",
                    next=None,
                    parent="c",
                    inputs={},
                    fields={},
                    shadow=False,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=None,
                ),
                "l": FRBlock(
                    opcode="operator_length",
                    next=None,
                    parent="c",
                    inputs={
                        "STRING": (1, (10, "apple")),
                    },
                    fields={},
                    shadow=False,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=None,
                ),
                "p": (
                    12,
                    "my variable",
                    "`jEk@4|i[#Fk?(8x)AV.-my variable",
                    446,
                    652,
                ),
                "q": (
                    13,
                    "my list",
                    "ta`eJd|abk.):i6vI0u}",
                    646,
                    561,
                ),
                "r": FRBlock(
                    opcode="argument_reporter_string_number",
                    next=None,
                    parent="a",
                    inputs={},
                    fields={
                        "VALUE": ("a text arg", "^yv5=2v`Ry/g^Z`)Ys.1"),
                    },
                    shadow=True,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=FRCustomBlockArgumentMutation(
                        tag_name="mutation",
                        children=[],
                        color=(
                            "#FF6680",
                            "#FF4D6A",
                            "#FF3355",
                        ),
                    ),
                ),
                "s": FRBlock(
                    opcode="argument_reporter_boolean",
                    next=None,
                    parent="a",
                    inputs={},
                    fields={
                        "VALUE": ("a bool arg", "2z2~7Noo4%=i2{EWKf(_"),
                    },
                    shadow=True,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=FRCustomBlockArgumentMutation(
                        tag_name="mutation",
                        children=[],
                        color=(
                            "#FF6680",
                            "#FF4D6A",
                            "#FF3355",
                        ),
                    ),
                ),
                "t": FRBlock(
                    opcode="argument_reporter_string_number",
                    next=None,
                    parent="a",
                    inputs={},
                    fields={
                        "VALUE": ("a text arg", "^#w/pW=4-9Dq9)klf:9x"),
                    },
                    shadow=True,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=FRCustomBlockArgumentMutation(
                        tag_name="mutation",
                        children=[],
                        color=(
                            "#FF6680",
                            "#FF4D6A",
                            "#FF3355",
                        ),
                    ),
                ),
                "u": FRBlock(
                    opcode="argument_reporter_boolean",
                    next=None,
                    parent="a",
                    inputs={},
                    fields={
                        "VALUE": ("a bool arg", "5gbANC]?3[@Ynp:~POWJ"),
                    },
                    shadow=True,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=FRCustomBlockArgumentMutation(
                        tag_name="mutation",
                        children=[],
                        color=(
                            "#FF6680",
                            "#FF4D6A",
                            "#FF3355",
                        ),
                    ),
                ),
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
                    comment=None,
                    mutation=None,
                ),
                "o": FRBlock(
                    opcode="data_changevariableby",
                    next=None,
                    parent="n",
                    inputs={
                        "VALUE": (1, (4, "1")),
                    },
                    fields={
                        "VARIABLE": (
                            "my variable",
                            "`jEk@4|i[#Fk?(8x)AV.-my variable",
                            "",
                        ),
                    },
                    shadow=False,
                    top_level=False,
                    x=None,
                    y=None,
                    comment=None,
                    mutation=None,
                ),
            },
            comments={
                "e": FRComment(
                    block_id="b",
                    x=620.6666690685131,
                    y=276.1481481481487,
                    width=200,
                    height=200,
                    minimized=False,
                    text="im a comment",
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
        ),
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
        platform=FRPenguinModPlatformMeta(name="PenguinMod", url="https://penguinmod.com/", version="stable"),
    ),
)


def test_FRProject_from_data():
    pass


