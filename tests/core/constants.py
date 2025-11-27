from copy  import deepcopy
from io    import BytesIO
from pydub import AudioSegment
from lxml  import etree

from pmp_manip.important_consts import (
    SHA256_SEC_MAIN_ARGUMENT_NAME, SHA256_SEC_LOCAL_ARGUMENT_NAME,
    SHA256_SEC_BROADCAST_MSG, SHA256_SEC_DROPDOWN_VALUE, SHA256_SEC_TARGET_NAME,
    SHA256_EDITOR_BUTTON_DV,
)
from pmp_manip.opcode_info.api  import DropdownValueKind, InputMode
from pmp_manip.utility          import read_all_files_of_zip, string_to_sha256, gdumps, KeyReprDict

from pmp_manip.core.asset          import FRCostume, FRSound, SRVectorCostume, SRSound
from pmp_manip.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockCallMutation,
    FRCustomBlockArgumentMutation, FRPolygonMutation, FRExpandableIfMutation,
    SRCustomBlockMutation, SRCustomBlockCallMutation, SRExpandableIfMutation,
)
from pmp_manip.core.block          import (
    FRBlock, IRBlock, IRInputValue,
    SRBlock, SRScript,
    SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, SRBlockAndBoolInputValue, 
    SRBlockOnlyInputValue, SRScriptInputValue, SRDropdownValue, SREmbeddedBlockInputValue,
)
from pmp_manip.core.comment        import FRComment, SRComment
from pmp_manip.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
    SRCustomBlockOptype,
)
from pmp_manip.core.enums          import SRSpriteRotationStyle, SRVideoState
from pmp_manip.core.meta           import FRMeta, FRPenguinModPlatformMeta
from pmp_manip.core.monitor        import (
    LIST_MONITOR_DEFAULT_WIDTH, LIST_MONITOR_DEFAULT_HEIGHT,
    FRMonitor, SRMonitor, SRListMonitor,
)
from pmp_manip.core.project        import FRProject, SRProject
from pmp_manip.core.target         import FRStage, FRSprite, SRStage, SRSprite
from pmp_manip.core.vars_lists     import _variable_sha256, _list_sha256, SRVariable, SRList
# TODO: correct formatting


ALL_FR_BLOCK_DATAS = {
    "d": {
        "opcode": "event_broadcast",
        "next": "b",
        "parent": None,
        "inputs": {
            "BROADCAST_INPUT": [
                1, [11, "my message", string_to_sha256("my message", secondary=SHA256_SEC_BROADCAST_MSG)]
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
        "next": "t",
        "parent": "d",
        "inputs": {
            "SECS": [1, [4, "1"]],
            "TO": [1, "e"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": False,
        "comment": "s",
    },
    "e": {
        "opcode": "motion_glideto_menu",
        "next": None,
        "parent": "b",
        "inputs": {},
        "fields": {
            "TO": ["_random_", string_to_sha256("_random_", secondary=SHA256_SEC_DROPDOWN_VALUE)],
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
                3, [12, "my variable", _variable_sha256("my variable", sprite_name="_stage_")], 
                [4, "1"],
            ],
            "TO": [3, "g", [4, "10"]],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 304,
        "y": 424,
    },
    "m": [12, "my variable", _variable_sha256("my variable", sprite_name="_stage_"), 446, 652],
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
            string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME): [1, "i"],
            string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME): [1, "j"],
        },
        "fields": {},
        "shadow": True,
        "topLevel": False,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "proccode": "do sth text %s and bool %b",
            "argumentids": gdumps([
                string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME), 
                string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME),
            ]),
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
            "VALUE": ["a text arg", string_to_sha256("a text arg", secondary=SHA256_SEC_LOCAL_ARGUMENT_NAME)],
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
            "VALUE": ["a bool arg", string_to_sha256("a bool arg", secondary=SHA256_SEC_LOCAL_ARGUMENT_NAME)],
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
            string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME): [3, "k", [10, ""]],
            string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME): [3, "l", "x"],
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
            "argumentids": gdumps([
                string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME), 
                string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME),
            ]),
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
    "x": {
        "opcode": "checkbox",
        "next": None,
        "parent": "c",
        "inputs": {},
        "fields": {
            "CHECKBOX": ["FALSE", string_to_sha256("FALSE", secondary=SHA256_SEC_DROPDOWN_VALUE)]
        },
        "shadow": True,
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
    "p": [13, "my list", _list_sha256("my list", sprite_name="_stage_"), 646, 561],
    "n": {
        "opcode": "control_if",
        "next": None,
        "parent": None,
        "inputs": {
            "CONDITION": [1, "y"],
            "SUBSTACK": [2, "o"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 528,
        "y": 1175,
    },
    "y": {
        "opcode": "checkbox",
        "next": None,
        "parent": "n",
        "inputs": {},
        "fields": {
            "CHECKBOX": ["FALSE", string_to_sha256("FALSE", secondary=SHA256_SEC_DROPDOWN_VALUE)]
        },
        "shadow": True,
        "topLevel": False,
    },
    "o": {
        "opcode": "data_changevariableby",
        "next": "q",
        "parent": "n",
        "inputs": {
            "VALUE": [1, [4, "1"]],
        },
        "fields": {
            "VARIABLE": ["my variable", _variable_sha256("my variable", sprite_name="_stage_"), ""],
        },
        "shadow": False,
        "topLevel": False,
    },
    "q": {
        "opcode": "data_showvariable",
        "next": None,
        "parent": "o",
        "inputs": {},
        "fields": {
            "VARIABLE": ["my variable", _variable_sha256("my variable", sprite_name="_stage_"), ""],
        },
        "shadow": False,
        "topLevel": False,
    },
    "r": {
        "opcode": "event_whengreaterthan",
        "next": None,
        "parent": None,
        "inputs": {
            "VALUE": [1, [4, "50"]],
        },
        "fields": {
            "WHENGREATERTHANMENU": ["LOUDNESS", string_to_sha256("LOUDNESS", secondary=SHA256_SEC_DROPDOWN_VALUE)],
        },
        "shadow": False,
        "topLevel": True,
        "x": 1784, 
        "y": -890,
    },
    "t": {
        "opcode": "motion_glideto",
        "next": None,
        "parent": "b",
        "inputs": {
            "SECS": [1, [4, "1"]],
            "TO": [3, "u", "v"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": False,
    },
    "u": {
        "opcode": "operator_falseBoolean",
        "next": None,
        "parent": "t",
        "inputs": {},
        "fields": {},
        "shadow": False,
        "topLevel": False,
    },
    "v": {
        "opcode": "motion_glideto_menu",
        "next": None,
        "parent": "t",
        "inputs": {},
        "fields": {
            "TO": ["_mouse_", string_to_sha256("_mouse_", secondary=SHA256_SEC_DROPDOWN_VALUE)],
        },
        "shadow": True,
        "topLevel": False,
    },
    "w": {
        "opcode": "event_whenbroadcastreceived",
        "next": None,
        "parent": None,
        "inputs": {},
        "fields": {
            "BROADCAST_OPTION": [
                "my message",
                string_to_sha256("my message", secondary=SHA256_SEC_BROADCAST_MSG),
                "broadcast_msg",
            ],
        },
        "shadow": False,
        "topLevel": True,
        "x": 184,
        "y": 1430,
    },
    "z": {
        "opcode": "control_if",
        "next": None,
        "parent": None,
        "inputs": {
            "CONDITION": [1, "A"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 1528,
        "y": 2175,
    },
    "A": {
        "opcode": "operator_trueBoolean",
        "next": None,
        "parent": "z",
        "inputs": {},
        "fields": {},
        "shadow": False,
        "topLevel": False,
    },
    "B": {
        "opcode": "control_switch",
        "next": None,
        "parent": None,
        "inputs": {
            "CONDITION": [2, "C"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 897,
        "y": 1365,
    },
    "C": {
        "opcode": "sensing_answer",
        "next": None,
        "parent": "B",
        "inputs": {},
        "fields": {},
        "shadow": False,
        "topLevel": False,
    },
    "D": {
        "opcode": "pen_drawComplexShape",
        "next": None,
        "parent": None,
        "inputs": {
            "COLOR": [1, [9, "#d0d228"]],
            "SHAPE": [1, "E"],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 202,
        "y": 333,
    },
    "E": {
        "opcode": "polygon",
        "next": None,
        "parent": "D",
        "inputs": {
            "x1": [2, [4, "-43.30127018922194"]],
            "y1": [2, [4, "-24.999999999999996"]],
            "x2": [2, [4, "43.30127018922194"]],
            "y2": [2, [4, "-24.999999999999996"]],
            "x3": [2, [4, "3.061616997868383e-15"]],
            "y3": [2, [4, "50"]],
        },
        "fields": {
            "button": [False, string_to_sha256(False, secondary=SHA256_SEC_DROPDOWN_VALUE)],
        },
        "shadow": True,
        "topLevel": False,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "points": "3",
            "color": "#0FBD8C",
            "midle": "[0,0]",
            "scale": "50",
            "expanded": "true",
            "needsinit": "true",
        },
    },
    "F": {
        "opcode": "control_expandableIf",
        "next": None,
        "parent": None,
        "inputs": {
            "BOOL1": [1, "G"],
            "SUBSTACK1": [1, None],
        },
        "fields": {
            "REMOVE": ["", string_to_sha256("REMOVE", secondary=SHA256_EDITOR_BUTTON_DV)],
            "ADD": ["", string_to_sha256("ADD", secondary=SHA256_EDITOR_BUTTON_DV)],
        },
        "shadow": False,
        "topLevel": True,
        "x": 335,
        "y": 753,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "branches": "1",
            "ends-in-else": "false",
        },
    },
    "G": {
        "opcode": "checkbox",
        "next": None,
        "parent": "F",
        "inputs": {},
        "fields": {
            "CHECKBOX": ["FALSE", string_to_sha256("FALSE", secondary=SHA256_SEC_DROPDOWN_VALUE)],
        },
        "shadow": True,
        "topLevel": False,
    },
}

ALL_FR_BLOCKS = {
    "d": FRBlock(
        opcode="event_broadcast",
        next="b",
        parent=None,
        inputs={
            "BROADCAST_INPUT": (
                1, (11, "my message", string_to_sha256("my message", secondary=SHA256_SEC_BROADCAST_MSG)),
            ),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=268,
        y=220,
    ),
    "b": FRBlock(
        opcode="motion_glideto",
        next="t",
        parent="d",
        inputs={
            "SECS": (1, (4, "1")),
            "TO": (1, "e"),
        },
        fields={},
        shadow=False,
        top_level=False,
        comment="s",
    ),
    "e": FRBlock(
        opcode="motion_glideto_menu",
        next=None,
        parent="b",
        inputs={},
        fields={
            "TO": ("_random_", string_to_sha256("_random_", secondary=SHA256_SEC_DROPDOWN_VALUE)),
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
                3, (12, "my variable", _variable_sha256("my variable", sprite_name="_stage_")), (4, "1"),
            ),
            "TO": (3, "g", (4, "10")),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=304,
        y=424,
    ),
    "m": (12, "my variable", _variable_sha256("my variable", sprite_name="_stage_"), 446, 652),
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
            string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME): (1, "i"),
            string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME): (1, "j"),
        },
        fields={},
        shadow=True,
        top_level=False,
        mutation=FRCustomBlockMutation(
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
        ),
    ),
    "i": FRBlock(
        opcode="argument_reporter_string_number",
        next=None,
        parent="a",
        inputs={},
        fields={
            "VALUE": ("a text arg", string_to_sha256("a text arg", secondary=SHA256_SEC_LOCAL_ARGUMENT_NAME)),
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
            "VALUE": ("a bool arg", string_to_sha256("a bool arg", secondary=SHA256_SEC_LOCAL_ARGUMENT_NAME)),
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
            string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME): (3, "k", (10, "")),
            string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME): (3, "l", "x"),
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
            argument_ids=[
                string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME), 
                string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME),
            ],
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
    "x": FRBlock(
        opcode="checkbox",
        next=None,
        parent="c",
        inputs={},
        fields={
            "CHECKBOX": ("FALSE", string_to_sha256("FALSE", secondary=SHA256_SEC_DROPDOWN_VALUE))
        },
        shadow=True,
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
    "p": (13, "my list", _list_sha256("my list", sprite_name="_stage_"), 646, 561),
    "n": FRBlock(
        opcode="control_if",
        next=None,
        parent=None,
        inputs={
            "CONDITION": (1, "y"),
            "SUBSTACK": (2, "o"),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=528,
        y=1175,
    ),
    "y": FRBlock(
        opcode="checkbox",
        next=None,
        parent="n",
        inputs={},
        fields={
            "CHECKBOX": ("FALSE", string_to_sha256("FALSE", secondary=SHA256_SEC_DROPDOWN_VALUE))
        },
        shadow=True,
        top_level=False,
    ),
    "o": FRBlock(
        opcode="data_changevariableby",
        next="q",
        parent="n",
        inputs={
            "VALUE": (1, (4, "1")),
        },
        fields={
            "VARIABLE": ("my variable", _variable_sha256("my variable", sprite_name="_stage_"), ""),
        },
        shadow=False,
        top_level=False,
    ),
    "q": FRBlock(
        opcode="data_showvariable",
        next=None,
        parent="o",
        inputs={},
        fields={
            "VARIABLE": ("my variable", _variable_sha256("my variable", sprite_name="_stage_"), ""),
        },
        shadow=False,
        top_level=False,
    ),
    "r": FRBlock(
        opcode="event_whengreaterthan",
        next=None,
        parent=None,
        inputs={
            "VALUE": (1, (4, "50")),
        },
        fields={
            "WHENGREATERTHANMENU": ("LOUDNESS", string_to_sha256("LOUDNESS", secondary=SHA256_SEC_DROPDOWN_VALUE)),
        },
        shadow=False,
        top_level=True,
        x=1784, 
        y=-890,
    ),
    "t": FRBlock(
        opcode="motion_glideto",
        next=None,
        parent="b",
        inputs={
            "SECS": (1, (4, "1")),
            "TO": (3, "u", "v"),
        },
        fields={},
        shadow=False,
        top_level=False,
    ),
    "u": FRBlock(
        opcode="operator_falseBoolean",
        next=None,
        parent="t",
        inputs={},
        fields={},
        shadow=False,
        top_level=False,
    ),
    "v": FRBlock(
        opcode="motion_glideto_menu",
        next=None,
        parent="t",
        inputs={},
        fields={
            "TO": ("_mouse_", string_to_sha256("_mouse_", secondary=SHA256_SEC_DROPDOWN_VALUE)),
        },
        shadow=True,
        top_level=False,
    ),
    "w": FRBlock(
        opcode="event_whenbroadcastreceived",
        next=None,
        parent=None,
        inputs={},
        fields={
            "BROADCAST_OPTION": (
                "my message",
                string_to_sha256("my message", secondary=SHA256_SEC_BROADCAST_MSG),
                "broadcast_msg",
            ),
        },
        shadow=False,
        top_level=True,
        x=184,
        y=1430,
        comment=None,
        mutation=None,
    ),
    "z": FRBlock(
        opcode="control_if",
        next=None,
        parent=None,
        inputs={
            "CONDITION": (1, "A"),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=1528,
        y=2175,
    ),
    "A": FRBlock(
        opcode="operator_trueBoolean",
        next=None,
        parent="z",
        inputs={},
        fields={},
        shadow=False,
        top_level=False,
    ),
    "B": FRBlock(
        opcode="control_switch",
        next=None,
        parent=None,
        inputs={
            "CONDITION": (2, "C"),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=897,
        y=1365,
        comment=None,
        mutation=None,
    ),
    "C": FRBlock(
        opcode="sensing_answer",
        next=None,
        parent="B",
        inputs={},
        fields={},
        shadow=False,
        top_level=False,
        x=None,
        y=None,
        comment=None,
        mutation=None,
    ),
    "D": FRBlock(
        opcode="pen_drawComplexShape",
        next=None,
        parent=None,
        inputs={
            "COLOR": (1, (9, "#d0d228")),
            "SHAPE": (1, "E"),
        },
        fields={},
        shadow=False,
        top_level=True,
        x=202,
        y=333,
        comment=None,
        mutation=None,
    ),
    "E": FRBlock(
        opcode="polygon",
        next=None,
        parent="D",
        inputs={
            "x1": (2, (4, "-43.30127018922194")),
            "y1": (2, (4, "-24.999999999999996")),
            "x2": (2, (4, "43.30127018922194")),
            "y2": (2, (4, "-24.999999999999996")),
            "x3": (2, (4, "3.061616997868383e-15")),
            "y3": (2, (4, "50")),
        },
        fields={
            "button": (False, string_to_sha256(False, secondary=SHA256_SEC_DROPDOWN_VALUE)),
        },
        shadow=True,
        top_level=False,
        x=None,
        y=None,
        comment=None,
        mutation=FRPolygonMutation(
            points=3,
            color="#0FBD8C",
            midle=(0, 0),
            scale=50,
            expanded=True,
            needs_init=True,
            tag_name="mutation",
            children=[],
        ),
    ),
    "F": FRBlock(
        opcode="control_expandableIf",
        next=None,
        parent=None,
        inputs={
            "BOOL1": (1, "G"),
            "SUBSTACK1": (1, None),
        },
        fields={
            "REMOVE": ("", string_to_sha256("REMOVE", secondary=SHA256_EDITOR_BUTTON_DV)),
            "ADD": ("", string_to_sha256("ADD", secondary=SHA256_EDITOR_BUTTON_DV)),
        },
        shadow=False,
        top_level=True,
        x=335,
        y=753,
        comment=None,
        mutation=FRExpandableIfMutation(
            branches=1,
            ends_in_else=False,
            tag_name="mutation",
            children=[],
        ),
    ),
    "G": FRBlock(
        opcode="checkbox",
        next=None,
        parent="F",
        inputs={},
        fields={
            "CHECKBOX": ("FALSE", string_to_sha256("FALSE", secondary=SHA256_SEC_DROPDOWN_VALUE)),
        },
        shadow=True,
        top_level=False,
        x=None,
        y=None,
        comment=None,
        mutation=None,
    ),
}

ALL_FR_BLOCKS_CLEAN: dict[str, FRBlock] = ALL_FR_BLOCKS | {
    "m": FRBlock(
        opcode="data_variable",
        next=None,
        parent=None,
        inputs={},
        fields={
            "VARIABLE": ("my variable", _variable_sha256("my variable", sprite_name="_stage_"), ""),
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
            "LIST": ("my list", _list_sha256("my list", sprite_name="_stage_"), "list"),
        },
        shadow=False,
        top_level=True,
        x=646,
        y=561,
    ),
}

ALL_COMMENT_DATAS = {
    "s": {
        "blockId": "b",
        "x": 1031,
        "y": 348,
        "width": 200,
        "height": 200,
        "minimized": False,
        "text": "hi from attached comment",
    }
}

ALL_FR_COMMENTS = {
    "s": FRComment(
        block_id  = "b",
        x         = 1031,
        y         = 348,
        width     = 200,
        height    = 200,
        minimized = False,
        text      = "hi from attached comment",
    )
}


ALL_IR_BLOCKS = {
    "d": IRBlock(
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
        next="b",
        is_top_level=True,
        in_shadow_input=False,
    ),
    "b": IRBlock(
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
                references=["e"],
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
        next="t",
        is_top_level=False,
        in_shadow_input=False,
    ),
    "e": IRBlock(
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
        in_shadow_input=False,
    ),
    "f": IRBlock(
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
                    in_shadow_input=False,
                ),
                text="1",
            ),
            "TO": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=["g"],
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
        in_shadow_input=False,
    ),
    "m": IRBlock(
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
        in_shadow_input=False,
    ),
    "h": IRBlock(
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
        in_shadow_input=False,
    ),
    "g": IRBlock(
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
        in_shadow_input=False,
    ),
    "c": IRBlock(
        opcode="procedures_call",
        inputs={
            "a text arg": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=["k"],
                immediate_block=None,
                text="",
            ),
            "a bool arg": IRInputValue(
                mode=InputMode.BLOCK_AND_BOOL,
                references=["l", "x"],
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
        in_shadow_input=False,
    ),
    "l": IRBlock(
        opcode="operator_falseBoolean",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "x": IRBlock(
        opcode="checkbox",
        inputs={},
        dropdowns={
            "CHECKBOX": "FALSE",
        },
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "k": IRBlock(
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
        in_shadow_input=False,
    ),
    "p": IRBlock(
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
        in_shadow_input=False,
    ),
    "n": IRBlock(
        opcode="control_if",
        inputs={
            "CONDITION": IRInputValue(
                mode=InputMode.BLOCK_AND_BOOL,
                references=["y"],
                immediate_block=None,
                text=None,
            ),
            "SUBSTACK": IRInputValue(
                mode=InputMode.SCRIPT,
                references=["o"],
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
        in_shadow_input=False,
    ),
    "y": IRBlock(
        opcode="checkbox",
        inputs={},
        dropdowns={
            "CHECKBOX": "FALSE",
        },
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
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
        next="q",
        is_top_level=False,
        in_shadow_input=False,
    ),
    "q": IRBlock(
        opcode="data_showvariable",
        inputs={},
        dropdowns={
            "VARIABLE": "my variable",
        },
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "r": IRBlock(
        opcode="event_whengreaterthan",
        inputs={
            "VALUE": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="50",
            ),
        },
        dropdowns={
            "WHENGREATERTHANMENU": "LOUDNESS",
        },
        comment=None,
        mutation=None,
        position=(1784, -890),
        next=None,
        is_top_level=True,
        in_shadow_input=False,
    ),
    "t": IRBlock(
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
                references=["u", "v"],
                immediate_block=None,
                text=None,
            )
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "u": IRBlock(
        opcode="operator_falseBoolean",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "v": IRBlock(
        opcode="motion_glideto_menu",
        inputs={},
        dropdowns={
            "TO": "_mouse_",
        },
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "w": IRBlock(
        opcode="event_whenbroadcastreceived",
        inputs={},
        dropdowns={
            "BROADCAST_OPTION": "my message",
        },
        comment=None,
        mutation=None,
        position=(184, 1430),
        next=None,
        is_top_level=True,
        in_shadow_input=False,
    ),
    "z": IRBlock(
        opcode="control_if",
        inputs={
            "CONDITION": IRInputValue(
                mode=InputMode.BLOCK_AND_BOOL,
                references=["A"],
                immediate_block=None,
                text=None,
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=(1528, 2175),
        next=None,
        is_top_level=True,
        in_shadow_input=False,
    ),
    "A": IRBlock(
        opcode="operator_trueBoolean",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "B": IRBlock(
        opcode="control_switch",
        inputs={
            "CONDITION": IRInputValue(
                mode=InputMode.BLOCK_ONLY,
                references=["C"],
                immediate_block=None,
                text=None,
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=(897, 1365),
        next=None,
        is_top_level=True,
        in_shadow_input=False,
    ),
    "C": IRBlock(
        opcode="sensing_answer",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "D": IRBlock(
        opcode="pen_drawComplexShape",
        inputs={
            "COLOR": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="#d0d228",
            ),
            "SHAPE": IRInputValue(
                mode=InputMode.FORCED_EMBEDDED_BLOCK,
                references=["E"],
                immediate_block=None,
                text=None,
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=(202, 333),
        next=None,
        is_top_level=True,
        in_shadow_input=False,
    ),
    "E": IRBlock(
        opcode="polygon",
        inputs={
            "x1": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="-43.30127018922194",
            ),
            "y1": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="-24.999999999999996",
            ),
            "x2": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="43.30127018922194",
            ),
            "y2": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="-24.999999999999996",
            ),
            "x3": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="3.061616997868383e-15",
            ),
            "y3": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="50",
            ),
        },
        dropdowns={
            "button": False,
        },
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
    ),
    "F": IRBlock(
        opcode="control_expandableIf",
        inputs={
            "BOOL1": IRInputValue(
                mode=InputMode.BLOCK_AND_BOOL,
                references=["G"],
                immediate_block=None,
                text=None,
            ),
            "SUBSTACK1": IRInputValue(
                mode=InputMode.SCRIPT,
                references=[],
                immediate_block=None,
                text=None,
            ),
        },
        dropdowns={},
        comment=None,
        mutation=SRExpandableIfMutation(
            branch_count=1,
            ends_in_else=False,
        ),
        position=(335, 753),
        next=None,
        is_top_level=True,
        in_shadow_input=False,
    ),
    "G": IRBlock(
        opcode="checkbox",
        inputs={},
        dropdowns={
            "CHECKBOX": "FALSE",
        },
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
        in_shadow_input=False,
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
    "s": SRComment(
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
                opcode="&events::broadcast ([MESSAGE])",
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
                opcode="&motion::glide (SECONDS) secs to ([TARGET])",
                inputs={
                    "SECONDS": SRBlockAndTextInputValue(block=None, immediate="1"),
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
            SRBlock(
                opcode="&motion::glide (SECONDS) secs to ([TARGET])",
                inputs={
                    "SECONDS": SRBlockAndTextInputValue(block=None, immediate="1"),
                    "TARGET": SRBlockAndDropdownInputValue(
                        block=SRBlock(
                            opcode="&operators::false",
                            inputs={},
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        dropdown=SRDropdownValue(kind=DropdownValueKind.OBJECT, value="mouse-pointer"),
                    ),
                },
                dropdowns={},
                comment=None,
                mutation=None,
            ),
        ],
    ),
    SRScript( # [1]
        position=(304, 424),
        blocks=[
            SRBlock(
                opcode="&operators::pick random (OPERAND1) to (OPERAND2)",
                inputs={
                    "OPERAND1": SRBlockAndTextInputValue(
                        block=SRBlock(
                            opcode="&variables::value of [VARIABLE]",
                            inputs={},
                            dropdowns={
                                "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="my variable"),
                            },
                            comment=None,
                            mutation=None,
                        ),
                        immediate="1",
                    ),
                    "OPERAND2": SRBlockAndTextInputValue(
                        block=SRBlock(
                            opcode="&operators::join (STRING1) (STRING2)",
                            inputs={
                                "STRING1": SRBlockAndTextInputValue(block=None, immediate="apple "),
                                "STRING2": SRBlockAndTextInputValue(block=None, immediate="banana"),
                            },
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        immediate="10",
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
                opcode="&variables::value of [VARIABLE]",
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
                opcode="&customblocks::define custom block reporter",
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
                opcode="&customblocks::call custom block",
                inputs={
                    "a text arg": SRBlockAndTextInputValue(
                        block=SRBlock(
                            opcode="&operators::length of (TEXT)",
                            inputs={
                                "TEXT": SRBlockAndTextInputValue(block=None, immediate="apple"),
                            },
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        immediate="",
                     ),
                    "a bool arg": SRBlockAndBoolInputValue(
                        block=SRBlock(
                            opcode="&operators::false",
                            inputs={},
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        immediate=False,
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
                opcode="&variables::value of [LIST]",
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
                opcode="&control::if <CONDITION> then {THEN}",
                inputs={
                    "CONDITION": SRBlockAndBoolInputValue(block=None, immediate=False),
                    "THEN": SRScriptInputValue(
                        blocks=[
                            SRBlock(
                                opcode="&variables::change [VARIABLE] by (VALUE)",
                                inputs={
                                    "VALUE": SRBlockAndTextInputValue(block=None, immediate="1"),
                                },
                                dropdowns={
                                    "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="my variable"),
                                },
                                comment=None,
                                mutation=None,
                            ),
                            SRBlock(
                                opcode="&variables::show variable [VARIABLE]",
                                inputs={},
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
    SRScript( # [7]
        position=(1784, -890),
        blocks=[
            SRBlock(
                opcode="&events::when [OPTION] > (VALUE)",
                inputs={
                    "VALUE": SRBlockAndTextInputValue(block=None, immediate="50"),
                },
                dropdowns={
                    "OPTION": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="loudness"),
                },
                comment=None,
                mutation=None,
            ),   
        ],
    ),
    SRScript( # [8]
        position=(184, 1430),
        blocks=[
            SRBlock(
                opcode="&events::when I receive [MESSAGE]",
                inputs={},
                dropdowns={
                    "MESSAGE": SRDropdownValue(kind=DropdownValueKind.BROADCAST_MSG, value="my message"),
                },
                comment=None,
                mutation=None,
            ),
        ],
    ),
    SRScript( # [9]
        position=(1528, 2175),
        blocks=[
            SRBlock(
                opcode="&control::if <CONDITION> then {THEN}",
                inputs={
                    "CONDITION": SRBlockAndBoolInputValue(
                        block=SRBlock(
                            opcode="&operators::true",
                            inputs={},
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        immediate=False,
                    ),
                    "THEN": SRScriptInputValue(blocks=[]),
                },
                dropdowns={},
                comment=None,
                mutation=None,
            ),
        ],
    ),
    SRScript( # [10]
        position=(897, 1365),
        blocks=[
            SRBlock(
                opcode="&control::switch (CONDITION) {CASES}",
                inputs={
                    "CONDITION": SRBlockOnlyInputValue(
                        block=SRBlock(
                            opcode="&sensing::answer",
                            inputs={},
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                    ),
                    "CASES": SRScriptInputValue(blocks=[]),
                },
                dropdowns={},
                comment=None,
                mutation=None,
            ),
        ],
    ),
    SRScript( # [11]
        position=(202, 333),
        blocks=[
            SRBlock(
                opcode="&pen::draw triangle {:SHAPE:} with fill (COLOR)",
                inputs={
                    "COLOR": SRBlockAndTextInputValue(block=None, immediate="#d0d228"),
                    "SHAPE": SREmbeddedBlockInputValue(
                        block=SRBlock(
                            opcode="&special::{{POLYGON MENU}}",
                            inputs={
                                "X1": SRBlockAndTextInputValue(block=None, immediate="-43.30127018922194"),
                                "Y1": SRBlockAndTextInputValue(block=None, immediate="-24.999999999999996"),
                                "X2": SRBlockAndTextInputValue(block=None, immediate="43.30127018922194"),
                                "Y2": SRBlockAndTextInputValue(block=None, immediate="-24.999999999999996"),
                                "X3": SRBlockAndTextInputValue(block=None, immediate="3.061616997868383e-15"),
                                "Y3": SRBlockAndTextInputValue(block=None, immediate="50"),
                            },
                            dropdowns={
                                "UNTOUCHED": SRDropdownValue(kind=DropdownValueKind.STANDARD, value=False),
                            },
                            comment=None,
                            mutation=None,
                        ),
                    ),
                },
                dropdowns={},
                comment=None,
                mutation=None,
            ),
        ],
    ),
    SRScript( # [12]
        position=(335, 753),
        blocks=[
            SRBlock(
                opcode="&control::{{EXPANDABLE IF-THEN-ELSE CHAIN}}",
                inputs={
                    "CONDITION1": SRBlockAndBoolInputValue(
                        block=None,
                        immediate=False,
                    ),
                    "THEN1": SRScriptInputValue(blocks=[]),
                },
                dropdowns={},
                comment=None,
                mutation=SRExpandableIfMutation(
                    branch_count=1,
                    ends_in_else=False,
                ),
            ),
        ],
    ),
]

ALL_SR_BLOCKS = [
    *ALL_SR_SCRIPTS[ 0].blocks,
     ALL_SR_SCRIPTS[ 0].blocks[2].inputs["TARGET"].block,
    *ALL_SR_SCRIPTS[ 1].blocks,
     ALL_SR_SCRIPTS[ 1].blocks[0].inputs["OPERAND1"].block,
     ALL_SR_SCRIPTS[ 1].blocks[0].inputs["OPERAND2"].block,
    *ALL_SR_SCRIPTS[ 2].blocks,
    *ALL_SR_SCRIPTS[ 3].blocks,
    *ALL_SR_SCRIPTS[ 4].blocks,
     ALL_SR_SCRIPTS[ 4].blocks[0].inputs["a text arg"].block,
     ALL_SR_SCRIPTS[ 4].blocks[0].inputs["a bool arg"].block,
    *ALL_SR_SCRIPTS[ 5].blocks,
    *ALL_SR_SCRIPTS[ 6].blocks,
    *ALL_SR_SCRIPTS[ 6].blocks[0].inputs["THEN"].blocks,
    *ALL_SR_SCRIPTS[ 7].blocks,
    *ALL_SR_SCRIPTS[ 8].blocks,
    *ALL_SR_SCRIPTS[ 9].blocks,
     ALL_SR_SCRIPTS[ 9].blocks[0].inputs["CONDITION"].block,
    *ALL_SR_SCRIPTS[10].blocks,
     ALL_SR_SCRIPTS[10].blocks[0].inputs["CONDITION"].block,
    *ALL_SR_SCRIPTS[11].blocks,
     ALL_SR_SCRIPTS[11].blocks[0].inputs["SHAPE"].block,
    *ALL_SR_SCRIPTS[12].blocks,
]






STAGE_DATA = {
    "isStage": True,
    "name": "Stage",
    "variables": {
        _variable_sha256("my variable", sprite_name="_stage_"): [
            "my variable",
            0,
        ],
    },
    "lists": {
        _list_sha256("my list", sprite_name="_stage_"): [
            "my list",
            [],
        ],
    },
    "broadcasts": {
        string_to_sha256("my message", secondary=SHA256_SEC_BROADCAST_MSG): "my message",
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
    "id": string_to_sha256("_stage_", secondary=SHA256_SEC_TARGET_NAME),
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
        _variable_sha256("my variable", sprite_name="_stage_"): ("my variable", 0),
    },
    lists={
        _list_sha256("my list", sprite_name="_stage_"): ("my list", []),
    },
    broadcasts={
        string_to_sha256("my message", secondary=SHA256_SEC_BROADCAST_MSG): "my message",
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
    id=string_to_sha256("_stage_", secondary=SHA256_SEC_TARGET_NAME),
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
    "comments": ALL_COMMENT_DATAS,
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
    "id": string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME),
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
    comments=ALL_FR_COMMENTS,
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
    id=string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME),
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



PROJECT_ASSET_FILES = KeyReprDict({
    file_name: content 
    for file_name, content in read_all_files_of_zip("tests/_assets_/testing_blocks.pmp").items() 
    if file_name != "project.json"
})

ALL_FR_MONITOR_DATAS = [
    {
        "id": _list_sha256("my list", sprite_name="_stage_"),
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
        "variableType": None,
        "variableId": None,
    },
    {
        "height": 0,
        "id": f'{string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME)}_xposition',
        "isDiscrete": True,
        "mode": "default",
        "opcode": "motion_xposition",
        "params": {},
        "sliderMax": 100,
        "sliderMin": 0,
        "spriteName": "Sprite1",
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 5,
        "y": 5,
        "variableType": None,
        "variableId": None,
    },
]

PROJECT_DATA = {
    "targets": [
        STAGE_DATA,
        SPRITE_DATA,
    ],
    "monitors": ALL_FR_MONITOR_DATAS,
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

ALL_FR_MONITORS = [
    FRMonitor(
        id=_list_sha256("my list", sprite_name="_stage_"),
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
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor(
        id=f'{string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME)}_xposition',
        mode="default",
        opcode="motion_xposition",
        params={},
        sprite_name="Sprite1",
        value=0,
        x=5,
        y=5,
        visible=True,
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
    ),
]
ALL_FR_MONITORS_CONVERTED = deepcopy(ALL_FR_MONITORS)
ALL_FR_MONITORS_CONVERTED[0].width = LIST_MONITOR_DEFAULT_WIDTH
ALL_FR_MONITORS_CONVERTED[0].height = LIST_MONITOR_DEFAULT_HEIGHT

FR_PROJECT = FRProject(
    targets=[
        FR_STAGE,
        FR_SPRITE,
    ],
    monitors=ALL_FR_MONITORS,
    extension_data={},
    extensions=[],
    extension_urls=KeyReprDict({}),
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
    asset_files=PROJECT_ASSET_FILES,
)



BACKDROP1_CONTENT = etree.fromstring(PROJECT_ASSET_FILES["cd21514d0531fdffb22204e0ec5ed84a.svg"])
COSTUME1_CONTENT = etree.fromstring(PROJECT_ASSET_FILES["c434b674f2da18ba13cdfe51dbc05ecc.svg"])
SQUAWK_CONTENT = AudioSegment.from_file(
    BytesIO(PROJECT_ASSET_FILES["e140d7ff07de8fa35c3d1595bba835ac.wav"]),
)

SR_STAGE = SRStage(
    scripts=[],
    comments=[],
    costumes=[
        SRVectorCostume(
            name="backdrop1",
            file_extension="svg",
            rotation_center=(240, 180),
            content=BACKDROP1_CONTENT,
        ),
    ],
    sounds=[],
    costume_index=0,
    volume=100,
)

SR_SPRITE = SRSprite(
    name="Sprite1",
    scripts=ALL_SR_SCRIPTS,
    comments=[],
    costumes=[
        SRVectorCostume(
            name="costume1",
            file_extension="svg",
            rotation_center=(26, 46),
            content=COSTUME1_CONTENT,
        ),
    ],
    sounds=[
        SRSound(
            name="Squawk", 
            file_extension="wav",
            content=SQUAWK_CONTENT,
        ),
    ],
    costume_index=0,
    volume=100,
    local_variables=[],
    local_lists=[],
    local_monitors=[
        SRMonitor( # [0] for [0]
            opcode="&motion::x position",
            dropdowns={},
            position=(-235, -175),
            is_visible=True,
        ),
    ],
    is_visible=True,
    position=(0, 0),
    size=100,
    direction=90,
    is_draggable=False,
    rotation_style=SRSpriteRotationStyle.ALL_AROUND,
)

SR_PROJECT = SRProject(
    stage=SR_STAGE,
    sprites=[SR_SPRITE],
    sprite_layer_stack=[SR_SPRITE.uuid],
    global_variables=[
        SRVariable(name="my variable", current_value=0),
    ],
    global_lists=[
        SRList(name="my list", current_value=[]),
    ],
    global_monitors=[
        SRListMonitor(
            opcode="&variables::value of [LIST]",
            dropdowns={
                "LIST": SRDropdownValue(kind=DropdownValueKind.LIST, value="my list"),
            },
            position=(-235, -175),
            is_visible=True,
            size=(100, 120),
        ),
    ],
    tempo=60,
    video_transparency=50,
    video_state=SRVideoState.ON,
    text_to_speech_language=None,
    extensions=[],
)




SB3_PROJECT_DATA_ORGINAL = {
    "targets": [
        {
            "isStage": True,
            "name": "Stage",
            "variables": {
                _variable_sha256("my variable", sprite_name="_stage_"): [
                    "my variable",
                    0,
                ],
            },
            "lists": {},
            "broadcasts": {},
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
            "sounds": [
                {
                    "name": "pop",
                    "assetId": "83a9787d4cb6f3b7632b4ddfebf74367",
                    "dataFormat": "wav",
                    "format": "",
                    "rate": 48000,
                    "sampleCount": 1123,
                    "md5ext": "83a9787d4cb6f3b7632b4ddfebf74367.wav",
                },
            ],
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
            "blocks": {
                "[hzM}SQH~fJL)OHYWkYr": {
                    "opcode": "motion_movesteps",
                    "next": None,
                    "parent": None,
                    "inputs": {
                        "STEPS": [
                            1,
                            [
                                4,
                                "10",
                            ],
                        ],
                    },
                    "fields": {},
                    "shadow": False,
                    "topLevel": True,
                    "x": 405,
                    "y": 85,
                },
                "s3F6y*$/hmQ:us~[*IQ@": {
                    "opcode": "procedures_definition",
                    "next": None,
                    "parent": None,
                    "inputs": {
                        "custom_block": [
                            1,
                            "6WEhjll%t[@Qh)]x.?#0",
                        ],
                    },
                    "fields": {},
                    "shadow": False,
                    "topLevel": True,
                    "x": 385,
                    "y": 313,
                },
                "6WEhjll%t[@Qh)]x.?#0": {
                    "opcode": "procedures_prototype",
                    "next": None,
                    "parent": "s3F6y*$/hmQ:us~[*IQ@",
                    "inputs": {},
                    "fields": {},
                    "shadow": True,
                    "topLevel": False,
                    "mutation": {
                        "tagName": "mutation",
                        "children": [],
                        "proccode": "block name",
                        "argumentids": "[]",
                        "argumentnames": "[]",
                        "argumentdefaults": "[]",
                        "warp": "true",
                    },
                },
            },
            "comments": {},
            "currentCostume": 0,
            "costumes": [
                {
                    "name": "costume1",
                    "bitmapResolution": 1,
                    "dataFormat": "svg",
                    "assetId": "bcf454acf82e4504149f7ffe07081dbc",
                    "md5ext": "bcf454acf82e4504149f7ffe07081dbc.svg",
                    "rotationCenterX": 48,
                    "rotationCenterY": 50,
                },
                {
                    "name": "costume2",
                    "bitmapResolution": 1,
                    "dataFormat": "svg",
                    "assetId": "0fb9be3e8397c983338cb71dc84d0b25",
                    "md5ext": "0fb9be3e8397c983338cb71dc84d0b25.svg",
                    "rotationCenterX": 46,
                    "rotationCenterY": 53,
                },
            ],
            "sounds": [
                {
                    "name": "Meow",
                    "assetId": "83c36d806dc92327b9e7049a565c6bff",
                    "dataFormat": "wav",
                    "format": "",
                    "rate": 48000,
                    "sampleCount": 40681,
                    "md5ext": "83c36d806dc92327b9e7049a565c6bff.wav",
                },
            ],
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
    "monitors": [],
    "extensions": [],
    "meta": {
        "semver": "3.0.0",
        "vm": "11.1.0",
        "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    },
}

SB3_PROJECT_DATA_CONVERTED = deepcopy(SB3_PROJECT_DATA_ORGINAL)
SB3_PROJECT_DATA_CONVERTED["targets"][0]["id"] = string_to_sha256(
    "_stage_", secondary=SHA256_SEC_TARGET_NAME,
)
SB3_PROJECT_DATA_CONVERTED["targets"][1]["id"] = string_to_sha256(
    SB3_PROJECT_DATA_ORGINAL["targets"][1]["name"], secondary=SHA256_SEC_TARGET_NAME,
)
