from pytest import fixture, raises
from copy   import copy

from pypenguin.utility            import (
    ValidationConfig, 
    ThanksError, TypeValidationError, InvalidOpcodeError, UnnecessaryDropdownError, 
    MissingDropdownError, RangeValidationError, InvalidValueError,
)
from pypenguin.opcode_info        import DropdownValueKind
from pypenguin.opcode_info.groups import info_api
from pypenguin.important_opcodes  import NEW_OPCODE_VAR_VALUE, NEW_OPCODE_LIST_VALUE

from pypenguin.core.context  import PartialContext
from pypenguin.core.dropdown import SRDropdownValue
from pypenguin.core.enums    import SRVariableMonitorReadoutMode
from pypenguin.core.monitor  import FRMonitor, SRMonitor, SRVariableMonitor, SRListMonitor, STAGE_WIDTH, STAGE_HEIGHT

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()

@fixture
def context():
    my_variable = (DropdownValueKind.VARIABLE, "globl")
    my_sprite_variable = (DropdownValueKind.VARIABLE, "locl")
    my_list = (DropdownValueKind.LIST, "globl")
    my_sprite_list = (DropdownValueKind.LIST, "locl")
    return PartialContext(
        scope_variables=[my_variable, my_sprite_variable],
        scope_lists=[my_list, my_sprite_list],

        all_sprite_variables=[my_variable],

        sprite_only_variables=[my_sprite_variable],
        sprite_only_lists=[my_sprite_list],

        other_sprites=[(DropdownValueKind.SPRITE, "Sprite1")],
        backdrops=[(DropdownValueKind.BACKDROP, "intro"), (DropdownValueKind.BACKDROP, "scene1")],
    )

ALL_FR_MONITOR_DATAS = [
    { # [0]
        "height": 0,
        "id": "5I9nI;7P)jdiR-_X;/%l_xposition",
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
    },
    { # [1]
        "height": 0,
        "id": "5I9nI;7P)jdiR-_X;/%l_yposition",
        "isDiscrete": True,
        "mode": "default",
        "opcode": "motion_yposition",
        "params": {},
        "sliderMax": 100,
        "sliderMin": 0,
        "spriteName": "Sprite1",
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 5,
        "y": 31,
    },
    { # [2]
        "height": 0,
        "id": "$6=c?qlc|4Q*mK{XGC}z",
        "isDiscrete": False,
        "mode": "slider",
        "opcode": "data_variable",
        "params": {"VARIABLE": "globl"},
        "sliderMax": 100,
        "sliderMin": -50.3,
        "spriteName": None,
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 110,
        "y": 76,
    },
    { # [3]
        "height": 0,
        "id": "P4dp6h[X1|F3dYA4I?C`",
        "isDiscrete": True,
        "mode": "default",
        "opcode": "data_variable",
        "params": {"VARIABLE": "globl2"},
        "sliderMax": 100,
        "sliderMin": -20,
        "spriteName": None,
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 216,
        "y": 128,
    },
    { # [4]
        "height": 198,
        "id": "ru2NZobs(r+b[~|-rTCf",
        "mode": "list",
        "opcode": "data_listcontents",
        "params": {"LIST": "locl"},
        "spriteName": "Sprite1",
        "value": [],
        "visible": True,
        "width": 100,
        "x": 342,
        "y": 15,
    },
    { # [5]
       "height": 147,
       "id": "Zc!aC=9=36YS+pEb?kWj",
       "mode": "list",
       "opcode": "data_listcontents",
       "params": {"LIST": "globl"},
       "spriteName": None,
       "value": [],
       "visible": True,
       "width": 176,
       "x": 36,
       "y": 153,
    },
    { # [6]
        "height": 0,
        "id": "8kv=.#:+,mIq:M5++hvu",
        "isDiscrete": True,
        "mode": "default",
        "opcode": "data_variable",
        "params": {"VARIABLE": "locl"},
        "sliderMax": 100,
        "sliderMin": 0,
        "spriteName": "Sprite1",
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 52,
        "y": 120,
    },
    { # [7]
        "height": 0,
        "id": "sensing_mousedown",
        "isDiscrete": True,
        "mode": "default",
        "opcode": "sensing_mousedown",
        "params": {},
        "sliderMax": 100,
        "sliderMin": 0,
        "spriteName": None,
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 255,
        "y": 220,
    },
    { # [8]
        "height": 0,
        "id": "answer",
        "isDiscrete": True,
        "mode": "default",
        "opcode": "sensing_answer",
        "params": {},
        "sliderMax": 100,
        "sliderMin": 0,
        "spriteName": None,
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 205,
        "y": 5,
    },
]

ALL_FR_MONITORS: list[FRMonitor] = [
    FRMonitor( # [0]
        id="5I9nI;7P)jdiR-_X;/%l_xposition",
        mode="default",
        opcode="motion_xposition",
        params={},
        sprite_name="Sprite1",
        value=0,
        x=5,
        y=5,
        visible=True,
        width=100,
        height=120,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
    ),
    FRMonitor( # [1]
        id="5I9nI;7P)jdiR-_X;/%l_yposition",
        mode="default",
        opcode="motion_yposition",
        params={},
        sprite_name="Sprite1",
        value=0,
        x=5,
        y=31,
        visible=True,
        width=100,
        height=120,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
    ),
    FRMonitor( # [2]
        id="$6=c?qlc|4Q*mK{XGC}z",
        mode="slider",
        opcode="data_variable",
        params={
            "VARIABLE": "globl",
        },
        sprite_name=None,
        value=0,
        x=110,
        y=76,
        visible=True,
        width=100,
        height=120,
        slider_min=-50.3,
        slider_max=100,
        is_discrete=False,
    ),
    FRMonitor( # [3]
        id="P4dp6h[X1|F3dYA4I?C`",
        mode="default",
        opcode="data_variable",
        params={
            "VARIABLE": "globl2",
        },
        sprite_name=None,
        value=0,
        x=216,
        y=128,
        visible=True,
        width=100,
        height=120,
        slider_min=-20,
        slider_max=100,
        is_discrete=True,
    ),
    FRMonitor( # [4]
        id="ru2NZobs(r+b[~|-rTCf",
        mode="list",
        opcode="data_listcontents",
        params={
            "LIST": "locl",
        },
        sprite_name="Sprite1",
        value=[],
        x=342,
        y=15,
        visible=True,
        width=100,
        height=198,
        slider_min=None,
        slider_max=None,
        is_discrete=None,
    ),
    FRMonitor( # [5]
        id="Zc!aC=9=36YS+pEb?kWj",
        mode="list",
        opcode="data_listcontents",
        params={
            "LIST": "globl",
        },
        sprite_name=None,
        value=[],
        x=36,
        y=153,
        visible=True,
        width=176,
        height=147,
        slider_min=None,
        slider_max=None,
        is_discrete=None,
    ),
    FRMonitor( # [6]
        id="8kv=.#:+,mIq:M5++hvu",
        mode="default",
        opcode="data_variable",
        params={
            "VARIABLE": "locl",
        },
        sprite_name="Sprite1",
        value=0,
        x=52,
        y=120,
        visible=True,
        width=100,
        height=120,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
    ),
    FRMonitor( # [7]
        id="sensing_mousedown",
        mode="default",
        opcode="sensing_mousedown",
        params={},
        sprite_name=None,
        value=0,
        x=255,
        y=220,
        visible=True,
        width=100,
        height=120,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
    ),
    FRMonitor( # [8]
        id="answer",
        mode="default",
        opcode="sensing_answer",
        params={},
        sprite_name=None,
        value=0,
        x=205,
        y=5,
        visible=True,
        width=100,
        height=120,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
    ),
]

ALL_LOCAL_SR_MONITORS: list[SRMonitor] = [
    SRMonitor( # [0] for [0]
        opcode="x position",
        dropdowns={},
        position=(-235, -175),
        is_visible=True,
    ),
    SRMonitor( # [1] for [1]
        opcode="y position",
        dropdowns={},
        position=(-235, -149),
        is_visible=True,
    ),
    SRListMonitor( # [2] for [4]
        opcode="value of [LIST]",
        dropdowns={
            "LIST": SRDropdownValue(kind=DropdownValueKind.LIST, value="locl"),
        },
        position=(102, -165),
        is_visible=True,
        size=(100, 198),
    ),
    SRVariableMonitor( # [3] for [6]
        opcode="value of [VARIABLE]",
        dropdowns={
            "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="locl"),
        },
        position=(-188, -60),
        is_visible=True,
        readout_mode=SRVariableMonitorReadoutMode.NORMAL,
        slider_min=0,
        slider_max=100,
        allow_only_integers=True,
    ),
]

ALL_GLOBAL_SR_MONITORS: list[SRMonitor] = [
    SRVariableMonitor( # [0]
        opcode="value of [VARIABLE]",
        dropdowns={
            "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="globl"),
        },
        position=(-130, -104),
        is_visible=True,
        readout_mode=SRVariableMonitorReadoutMode.LARGE,
        slider_min=-50.3,
        slider_max=100,
        allow_only_integers=False,
    ),
    SRVariableMonitor( # [1]
        opcode="value of [VARIABLE]",
        dropdowns={
            "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="globl2"),
        },
        position=(-24, -52),
        is_visible=True,
        readout_mode=SRVariableMonitorReadoutMode.SLIDER,
        slider_min=-20,
        slider_max=100,
        allow_only_integers=True,
    ),
    SRListMonitor( # [2]
        opcode="value of [LIST]",
        dropdowns={
            "LIST": SRDropdownValue(kind=DropdownValueKind.LIST, value="globl"),
        },
        position=(-204, -27),
        is_visible=True,
        size=(176, 147)),
    SRMonitor( # [3] for [7]
        opcode="mouse down?",
        dropdowns={},
        position=(15, 40),
        is_visible=True,
    ),
    SRMonitor( # [4] for [8]
        opcode="answer",
        dropdowns={},
        position=(-35, -175),
        is_visible=True,
    ),
]

SPRITE_NAMES = ["Sprite1"]




def test_FRMonitor_from_data():
    monitor_data = ALL_FR_MONITOR_DATAS[0]
    frmonitor = FRMonitor.from_data(monitor_data)
    assert isinstance(frmonitor, FRMonitor)
    assert frmonitor.id == monitor_data["id"]
    assert frmonitor.mode == monitor_data["mode"]
    assert frmonitor.opcode == monitor_data["opcode"]
    assert frmonitor.params == monitor_data["params"]
    assert frmonitor.sprite_name == monitor_data["spriteName"]
    assert frmonitor.value == monitor_data["value"]
    assert frmonitor.x == monitor_data["x"]
    assert frmonitor.y == monitor_data["y"]
    assert frmonitor.visible == monitor_data["visible"]
    assert frmonitor.width == monitor_data["width"]
    assert frmonitor.height == monitor_data["height"]
    assert frmonitor.slider_min == monitor_data["sliderMin"]
    assert frmonitor.slider_max == monitor_data["sliderMax"]
    assert frmonitor.is_discrete == monitor_data["isDiscrete"]

def test_FRMonitor_from_data_list():
    monitor_data = ALL_FR_MONITOR_DATAS[4]
    frmonitor = FRMonitor.from_data(monitor_data)
    assert isinstance(frmonitor, FRMonitor)
    assert frmonitor.slider_min == None
    assert frmonitor.slider_max == None
    assert frmonitor.is_discrete == None


def test_FRMonitor_post_init_params():
    with raises(ThanksError):
        FRMonitor.from_data(ALL_FR_MONITOR_DATAS[1] | {"params": []})

def test_FRMonitor_post_init_mode():
    with raises(ThanksError):
        FRMonitor.from_data(ALL_FR_MONITOR_DATAS[8] | {"mode": "invalid"})


def test_FRMonitor_step():
    frmonitor = ALL_FR_MONITORS[7]
    sprite_name, srmonitor = frmonitor.step(
        info_api=info_api,
        sprite_names=SPRITE_NAMES,
    )
    assert sprite_name == frmonitor.sprite_name
    assert isinstance(srmonitor, SRMonitor)
    assert srmonitor == ALL_GLOBAL_SR_MONITORS[3]

def test_FRMonitor_step_unnecessary():
    frmonitor = copy(ALL_FR_MONITORS[7])
    frmonitor.sprite_name = "A non-existing sprite"
    result = frmonitor.step(
        info_api=info_api,
        sprite_names=SPRITE_NAMES,
    )
    assert result == (None, None)



def test_SRMonitor_post_init():
    with raises(AssertionError):
        SRMonitor(
            opcode=NEW_OPCODE_VAR_VALUE,
            dropdowns=...,
            position=...,
            is_visible=...,
        )
    with raises(AssertionError):
        SRMonitor(
            opcode=NEW_OPCODE_LIST_VALUE,
            dropdowns=...,
            position=...,
            is_visible=...,
        )


def test_SRMonitor_validate(config):
    srmonitor = ALL_GLOBAL_SR_MONITORS[4]
    srmonitor.validate([], config, info_api)
    
    execute_attr_validation_tests(
        obj=srmonitor,
        attr_tests=[
            ("opcode", set(), TypeValidationError),
            ("opcode", "some undefined opcode", InvalidOpcodeError),
            ("dropdowns", [], TypeValidationError),
            ("dropdowns", {8:9}, TypeValidationError),
            ("position", 9, TypeValidationError),
            ("is_visible", None, TypeValidationError),
        ],
        validate_func=SRMonitor.validate,
        func_args=[[], config, info_api],
    )

def test_SRMonitor_validate_position_outside_stage(config):
    srmonitor = copy(ALL_LOCAL_SR_MONITORS[3])
    srmonitor.position = (STAGE_HEIGHT * 2, STAGE_HEIGHT * 2)
    with raises(RangeValidationError):
        srmonitor.validate([], config, info_api)

def test_SRMonitor_validate_unexpected_dropdown(config):
    srmonitor = copy(ALL_LOCAL_SR_MONITORS[0])
    srmonitor.dropdowns = {"SOME_ID": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="some value")}
    with raises(UnnecessaryDropdownError):
        srmonitor.validate([], config, info_api)

def test_SRMonitor_validate_missing_dropdown(config):
    srmonitor = copy(ALL_LOCAL_SR_MONITORS[2])
    del srmonitor.dropdowns["LIST"]
    with raises(MissingDropdownError):
        srmonitor.validate([], config, info_api)


def test_SRMonitor_validate_dropdown_values(context):
    srmonitor = ALL_LOCAL_SR_MONITORS[3]
    srmonitor.validate_dropdown_values([], config, info_api, context)



def test_SRVariableMonitor_validate_all_numbers(config):
    srmonitor = ALL_GLOBAL_SR_MONITORS[0]
    srmonitor: SRVariableMonitor
    srmonitor.validate([], config, info_api)
    
    execute_attr_validation_tests(
        obj=srmonitor,
        attr_tests=[
            ("allow_only_integers", 8, TypeValidationError),
            ("readout_mode", "normal", TypeValidationError),
            ("slider_min", "", TypeValidationError),
            ("slider_max", None, TypeValidationError),
            ("slider_min", 200, RangeValidationError), # bigger then slider_max
        ],
        validate_func=SRVariableMonitor.validate,
        func_args=[[], config, info_api],
    )

def test_SRVariableMonitor_validate_only_integers(config):
    srmonitor = ALL_GLOBAL_SR_MONITORS[1]
    srmonitor: SRVariableMonitor
    srmonitor.validate([], config, info_api)
    
    execute_attr_validation_tests(
        obj=srmonitor,
        attr_tests=[
            ("slider_min", 4.3, TypeValidationError),
            ("slider_max", 90.45, TypeValidationError),
        ],
        validate_func=SRVariableMonitor.validate,
        func_args=[[], config, info_api],
    )

def test_SRVariableMonitor_validate_invalid_opcode(config):
    srmonitor = copy(ALL_GLOBAL_SR_MONITORS[0])
    srmonitor: SRVariableMonitor
    srmonitor.opcode = "x position"
    srmonitor.dropdowns = {}
    with raises(InvalidValueError):
        srmonitor.validate([], config, info_api)



def test_SRListMonitor_validate(config):
    srmonitor = ALL_GLOBAL_SR_MONITORS[2]
    srmonitor: SRListMonitor
    srmonitor.validate([], config, info_api)

def test_SRListMonitor_validate_too_big_size(config):
    srmonitor = copy(ALL_GLOBAL_SR_MONITORS[2])
    srmonitor: SRListMonitor
    srmonitor.size = (2*STAGE_WIDTH, 2*STAGE_HEIGHT)
    with raises(RangeValidationError):
        srmonitor.validate([], config, info_api)
    
    modified_config = copy(config)
    modified_config: ValidationConfig
    modified_config.raise_when_monitor_bigger_then_stage = False
    srmonitor.validate([], modified_config, info_api)

def test_SRListMonitor_validate_invalid_opcode(config):
    srmonitor = copy(ALL_GLOBAL_SR_MONITORS[2])
    srmonitor: SRListMonitor
    srmonitor.opcode = "x position"
    srmonitor.dropdowns = {}
    with raises(InvalidValueError):
        srmonitor.validate([], config, info_api)


