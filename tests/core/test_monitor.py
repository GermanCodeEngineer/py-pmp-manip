from copy   import copy
from pytest import fixture, raises

from pypenguin.important_consts import (
    NEW_OPCODE_VAR_VALUE, NEW_OPCODE_LIST_VALUE,
    SHA256_SEC_MONITOR_VARIABLE_ID,
)
from pypenguin.opcode_info.api  import DropdownValueKind
from pypenguin.opcode_info.data import info_api
from pypenguin.important_consts import SHA256_SEC_TARGET_NAME
from pypenguin.utility          import (
    string_to_sha256, 
    ThanksError, TypeValidationError, InvalidOpcodeError, UnnecessaryDropdownError, 
    MissingDropdownError, RangeValidationError, InvalidValueError,
)

from pypenguin.core.block_interface import InterToFirstIF
from pypenguin.core.context         import PartialContext
from pypenguin.core.dropdown        import SRDropdownValue
from pypenguin.core.enums           import SRVariableMonitorReadoutMode
from pypenguin.core.monitor         import (
    FRMonitor, SRMonitor, SRVariableMonitor, SRListMonitor, 
    STAGE_WIDTH, STAGE_HEIGHT,
)
from pypenguin.core.vars_lists      import variable_sha256, list_sha256

from tests.utility import execute_attr_validation_tests
from tests.core.constants import ALL_IR_BLOCKS


ALL_FR_MONITOR_DATAS = [
    { # [0]
        "height": 0,
        "id": f"{string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME)}_xposition",
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
    { # [1]
        "height": 0,
        "id": f"{string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME)}_yposition",
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
        "variableType": None,
        "variableId": None,
    },
    { # [2]
        "height": 0,
        "id": variable_sha256("globl", sprite_name="_stage_"),
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
        "variableType": None,
        "variableId": None,
    },
    { # [3]
        "height": 0,
        "id": variable_sha256("globl2", sprite_name="_stage_"),
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
        "variableType": None,
        "variableId": None,
    },
    { # [4]
        "height": 198,
        "id": list_sha256("locl", sprite_name="Sprite1"),
        "mode": "list",
        "opcode": "data_listcontents",
        "params": {"LIST": "locl"},
        "spriteName": "Sprite1",
        "value": [],
        "visible": True,
        "width": 100,
        "x": 342,
        "y": 15,
        "variableType": None,
        "variableId": None,
    },
    { # [5]
       "height": 147,
       "id": list_sha256("globl", sprite_name="_stage_"),
       "mode": "list",
       "opcode": "data_listcontents",
       "params": {"LIST": "globl"},
       "spriteName": None,
       "value": [],
       "visible": True,
       "width": 176,
       "x": 36,
       "y": 153,
        "variableType": None,
        "variableId": None,
    },
    { # [6]
        "height": 0,
        "id": variable_sha256("locl", sprite_name="Sprite1"),
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
        "variableType": None,
        "variableId": None,
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
        "variableType": None,
        "variableId": None,
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
        "variableType": None,
        "variableId": None,
    },
    { # [9]
        "height": 0,
        "id": f"{string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME)}_costumenumbername_number",
        "isDiscrete": True,
        "mode": "default",
        "opcode": "looks_costumenumbername",
        "params": {
            "NUMBER_NAME": "number",
        },
        "sliderMax": 100,
        "sliderMin": 0,
        "spriteName": "Sprite1",
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 184,
        "y": 136,
        "variableType": None,
        "variableId": None,
    },
    { # [10]
        "height": 0,
        "id": "backdropnumbername_number",
        "isDiscrete": True,
        "mode": "default",
        "opcode": "looks_backdropnumbername",
        "params": {
            "NUMBER_NAME": "number",
        },
        "sliderMax": 100,
        "sliderMin": 0,
        "spriteName": None,
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 2,
        "y": 116,
        "variableType": None,
        "variableId": None,
    },
    { # [11]
        "height": 0,
        "id": "current_year",
        "isDiscrete": True,
        "mode": "default",
        "opcode": "sensing_current",
        "params": {
            "CURRENTMENU": "YEAR",
        },
        "sliderMax": 100,
        "sliderMin": 0,
        "spriteName": None,
        "value": 0,
        "visible": True,
        "width": 0,
        "x": 52,
        "y": 258,
        "variableType": None,
        "variableId": None,
    },
    
    
    { # [12]
        "id": "dumbExample_last_used_base",
        "mode": "default",
        "opcode": "dumbExample_last_used_base",
        "params": {},
        "spriteName": None,
        "value": 0,
        "width": 0,
        "height": 0,
        "x": 5,
        "y": 32,
        "visible": True,
        "variableType": None,
        "variableId": None,
        "sliderMin": 0,
        "sliderMax": 100,
        "isDiscrete": True,
    },
    { # [13]
        "id": "dumbExample_last_two_inout_values_IN_OUT",
        "mode": "default",
        "opcode": "dumbExample_last_two_inout_values",
        "params": {
            "S1": "IN",
            "S2": "OUT",
        },
        "spriteName": None,
        "value": 0,
        "width": 0,
        "height": 0,
        "x": 0,
        "y": 0,
        "visible": True,
        "variableType": None,
        "variableId": string_to_sha256("dumbExample_last_two_inout_values", secondary=SHA256_SEC_MONITOR_VARIABLE_ID),
        "sliderMin": 0,
        "sliderMax": 100,
        "isDiscrete": True,
    },
]

ALL_FR_MONITORS: list[FRMonitor] = [
    FRMonitor( # [0]
        id=f"{string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME)}_xposition",
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
    FRMonitor( # [1]
        id=f"{string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME)}_yposition",
        mode="default",
        opcode="motion_yposition",
        params={},
        sprite_name="Sprite1",
        value=0,
        x=5,
        y=31,
        visible=True,
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor( # [2]
        id=variable_sha256("globl", sprite_name="_stage_"),
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
        width=0,
        height=0,
        slider_min=-50.3,
        slider_max=100,
        is_discrete=False,
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor( # [3]
        id=variable_sha256("globl2", sprite_name="_stage_"),
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
        width=0,
        height=0,
        slider_min=-20,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor( # [4]
        id=list_sha256("locl", sprite_name="Sprite1"),
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
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor( # [5]
        id=list_sha256("globl", sprite_name="_stage_"),
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
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor( # [6]
        id=variable_sha256("locl", sprite_name="Sprite1"),
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
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
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
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
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
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor( # [9]
        id=f"{string_to_sha256("Sprite1", secondary=SHA256_SEC_TARGET_NAME)}_costumenumbername_number",
        mode="default",
        opcode="looks_costumenumbername",
        params={
            "NUMBER_NAME": "number",
        },
        sprite_name=None,
        value=0,
        x=184,
        y=136,
        visible=True,
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor( # [10]
        id="backdropnumbername_number",
        mode="default",
        opcode="looks_backdropnumbername",
        params={
            "NUMBER_NAME": "number",
        },
        sprite_name=None,
        value=0,
        x=2,
        y=116,
        visible=True,
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
    ),
    FRMonitor( # [11]
        id="current_year",
        mode="default",
        opcode="sensing_current",
        params={
            "CURRENTMENU": "YEAR",
        },
        sprite_name=None,
        value=0,
        x=52,
        y=258,
        visible=True,
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=None,
    ),
    
    
    FRMonitor( # [12]
        id="dumbExample_last_used_base",
        mode="default",
        opcode="dumbExample_last_used_base",
        params={},
        sprite_name=None,
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
    FRMonitor( # [13]
        id="dumbExample_last_two_inout_values_IN_OUT",
        mode="default",
        opcode="dumbExample_last_two_inout_values",
        params={
            "S1": "IN",
            "S2": "OUT",
        },
        sprite_name=None,
        value=0,
        x=5,
        y=59,
        visible=True,
        width=0,
        height=0,
        slider_min=0,
        slider_max=100,
        is_discrete=True,
        variable_type=None,
        variable_id=string_to_sha256("dumbExample_last_two_inout_values", secondary=SHA256_SEC_MONITOR_VARIABLE_ID),
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
    SRMonitor( # [4] for [9]
        opcode="costume [PROPERTY]",
        dropdowns={
            "PROPERTY": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="number"),
        },
        position=(-56, -44),
        is_visible=True,
    ),
]

ALL_GLOBAL_SR_MONITORS: list[SRMonitor] = [
    SRVariableMonitor( # [0] for [2]
        opcode="value of [VARIABLE]",
        dropdowns={
            "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="globl"),
        },
        position=(-130, -104),
        is_visible=True,
        readout_mode=SRVariableMonitorReadoutMode.SLIDER,
        slider_min=-50.3,
        slider_max=100,
        allow_only_integers=False,
    ),
    SRVariableMonitor( # [1] for [3]
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
    SRListMonitor( # [2] for [5]
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
    SRMonitor( # [5] for [10]
        opcode="backdrop [PROPERTY]",
        dropdowns={
            "PROPERTY": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="number"),
        },
        position=(-238, -64),
        is_visible=True,
    ),
    SRMonitor( # [6] for [11]
        opcode="current [PROPERTY]",
        dropdowns={
            "PROPERTY": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="year"),
        },
        position=(-188, 78),
        is_visible=True,
    ),
    
    
    SRMonitor( # [7] for [12]
        opcode="dumbExample::last used base",
        dropdowns={},
        position=(-235, -175),
        is_visible=True,
    ),
    SRMonitor( # [8] for [13]
        opcode="dumbExample::last two [S1] and [S2] values",
        dropdowns={
            "S1": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="IN"),
            "S2": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="OUT"),
        },
        position=(-235, -121),
        is_visible=True,
    ),
]

SPRITE_NAMES = ["Sprite1"]

@fixture
def info_api_extended():
    info_api_extended = copy(info_api)
    info_api_extended.opcode_info = copy(info_api.opcode_info) 
    # make sure the internals of the DualKeyDict are shallow copied as well
    from example_extensions.gen_opcode_info.dumbExample import dumbExample
    info_api_extended.add_group(dumbExample)
    return info_api_extended

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

@fixture
def sprite_itf_if():
    return InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable", "globl"], global_lists=["my list", "globl"], 
        local_vars=["locl"], local_lists=["locl"], # variables and lists are modified
        sprite_name="Sprite1",
    )

@fixture
def stage_itf_if():
    return InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable", "globl"], global_lists=["my list", "globl"], 
        local_vars=["locl"], local_lists=["locl"], # variables and lists are modified
        sprite_name=None,
    )



def test_FRMonitor_from_to_data():
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

    assert frmonitor.to_data() == monitor_data

def test_FRMonitor_from_to_data_list():
    monitor_data = ALL_FR_MONITOR_DATAS[4]
    frmonitor = FRMonitor.from_data(monitor_data)
    assert isinstance(frmonitor, FRMonitor)
    assert frmonitor.slider_min == None
    assert frmonitor.slider_max == None
    assert frmonitor.is_discrete == None
    
    assert frmonitor.to_data() == monitor_data


def test_FRMonitor_post_init_params():
    with raises(ThanksError):
        FRMonitor.from_data(ALL_FR_MONITOR_DATAS[1] | {"params": []})

def test_FRMonitor_post_init_mode():
    with raises(ThanksError):
        FRMonitor.from_data(ALL_FR_MONITOR_DATAS[8] | {"mode": "invalid"})

def test_FRMonitor_post_init_variable_type():
    with raises(ThanksError):
        FRMonitor.from_data(ALL_FR_MONITOR_DATAS[13] | {"variableType": []})


def test_FRMonitor_to_second(info_api_extended):
    frmonitor = ALL_FR_MONITORS[7]
    srmonitor = frmonitor.to_second(
        info_api=info_api_extended,
        sprite_names=SPRITE_NAMES,
    )
    assert srmonitor == ALL_GLOBAL_SR_MONITORS[3]

def test_FRMonitor_to_second_unnecessary(info_api_extended):
    frmonitor = copy(ALL_FR_MONITORS[7])
    frmonitor.sprite_name = "A non-existing sprite"
    srmonitor = frmonitor.to_second(
        info_api=info_api_extended,
        sprite_names=SPRITE_NAMES,
    )
    assert srmonitor is None

def test_FRMonitor_to_second_dropdowns(info_api_extended):
    frmonitor = ALL_FR_MONITORS[2]
    srmonitor = frmonitor.to_second(
        info_api=info_api_extended,
        sprite_names=SPRITE_NAMES,
    )
    assert srmonitor == ALL_GLOBAL_SR_MONITORS[0]

def test_FRMonitor_to_second_list_monitor(info_api_extended):
    frmonitor = ALL_FR_MONITORS[4]
    srmonitor = frmonitor.to_second(
        info_api=info_api_extended,
        sprite_names=SPRITE_NAMES,
    )
    assert srmonitor == ALL_LOCAL_SR_MONITORS[2]



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


def test_SRMonitor_validate(info_api_extended):
    srmonitor = ALL_GLOBAL_SR_MONITORS[4]
    srmonitor.validate([], info_api_extended)
    
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
        func_args=[[], info_api_extended],
    )

def test_SRMonitor_validate_position_outside_stage(info_api_extended):
    srmonitor = copy(ALL_LOCAL_SR_MONITORS[3])
    srmonitor.position = (STAGE_HEIGHT * 2, STAGE_HEIGHT * 2)
    with raises(RangeValidationError):
        srmonitor.validate([], info_api_extended)

def test_SRMonitor_validate_unexpected_dropdown(info_api_extended):
    srmonitor = copy(ALL_LOCAL_SR_MONITORS[0])
    srmonitor.dropdowns = {"SOME_ID": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="some value")}
    with raises(UnnecessaryDropdownError):
        srmonitor.validate([], info_api_extended)

def test_SRMonitor_validate_missing_dropdown(info_api_extended):
    srmonitor = copy(ALL_LOCAL_SR_MONITORS[2])
    del srmonitor.dropdowns["LIST"]
    with raises(MissingDropdownError):
        srmonitor.validate([], info_api_extended)


def test_SRMonitor_validate_dropdown_values(info_api_extended, context):
    srmonitor = ALL_LOCAL_SR_MONITORS[3]
    srmonitor.validate_dropdown_values([], info_api_extended, context)


def test_SRMonitor_generate_id_sprite_opcmain(info_api_extended, sprite_itf_if):
    srmonitor = ALL_LOCAL_SR_MONITORS[0]
    monitor_id = srmonitor._generate_id(sprite_itf_if, info_api_extended, old_dropdown_values=[None])
    assert monitor_id == ALL_FR_MONITORS[0].id

def test_SRMonitor_generate_id_sprite_opcmain_params(info_api_extended, sprite_itf_if):
    srmonitor = ALL_LOCAL_SR_MONITORS[4]
    monitor_id = srmonitor._generate_id(sprite_itf_if, info_api_extended, old_dropdown_values=["number"])
    assert monitor_id == ALL_FR_MONITORS[9].id

def test_SRMonitor_generate_id_opcmain_params(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[5]
    monitor_id = srmonitor._generate_id(stage_itf_if, info_api_extended, old_dropdown_values=["number"])
    assert monitor_id == ALL_FR_MONITORS[10].id

def test_SRMonitor_generate_id_opcmain_lowerparam(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[6]
    monitor_id = srmonitor._generate_id(stage_itf_if, info_api_extended, old_dropdown_values=["year"])
    assert monitor_id == ALL_FR_MONITORS[11].id

def test_SRMonitor_generate_id_opcmain(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[4]
    monitor_id = srmonitor._generate_id(stage_itf_if, info_api_extended, old_dropdown_values=[None])
    assert monitor_id == ALL_FR_MONITORS[8].id

def test_SRMonitor_generate_id_opcfull_params(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[8]
    monitor_id = srmonitor._generate_id(stage_itf_if, info_api_extended, old_dropdown_values=["IN", "OUT"])
    assert monitor_id == ALL_FR_MONITORS[13].id

def test_SRMonitor_generate_id_opcfull(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[3]
    monitor_id = srmonitor._generate_id(stage_itf_if, info_api_extended, old_dropdown_values=[None])
    assert monitor_id == ALL_FR_MONITORS[7].id

def test_SRMonitor_generate_id_variable(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[0]
    monitor_id = srmonitor._generate_id(stage_itf_if, info_api_extended, old_dropdown_values=["globl"])
    assert monitor_id == ALL_FR_MONITORS[2].id

def test_SRMonitor_generate_id_list(info_api_extended, sprite_itf_if):
    srmonitor = ALL_LOCAL_SR_MONITORS[2]
    monitor_id = srmonitor._generate_id(sprite_itf_if, info_api_extended, old_dropdown_values=["locl"])
    assert monitor_id == ALL_FR_MONITORS[4].id


def test_SRMonitor_to_first_variable(info_api_extended, sprite_itf_if):
    srmonitor = ALL_LOCAL_SR_MONITORS[3]
    frmonitor = srmonitor.to_first(sprite_itf_if, info_api_extended)
    assert frmonitor == ALL_FR_MONITORS[6]

def test_SRMonitor_to_first_list(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[2]
    frmonitor = srmonitor.to_first(stage_itf_if, info_api_extended)
    assert frmonitor == ALL_FR_MONITORS[5]

def test_SRMonitor_to_first_normal(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[5]
    frmonitor = srmonitor.to_first(stage_itf_if, info_api_extended)
    assert frmonitor == ALL_FR_MONITORS[10]

def test_SRMonitor_to_first_no_variable_id(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[7]
    frmonitor = srmonitor.to_first(stage_itf_if, info_api_extended)
    assert frmonitor == ALL_FR_MONITORS[12]

def test_SRMonitor_to_first_variable_id(info_api_extended, stage_itf_if):
    srmonitor = ALL_GLOBAL_SR_MONITORS[8]
    frmonitor = srmonitor.to_first(stage_itf_if, info_api_extended)
    assert frmonitor == ALL_FR_MONITORS[13]



def test_SRVariableMonitor_validate_all_numbers(info_api_extended):
    srmonitor: SRVariableMonitor = ALL_GLOBAL_SR_MONITORS[0]
    srmonitor.validate([], info_api_extended)
    
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
        func_args=[[], info_api_extended],
    )

def test_SRVariableMonitor_validate_only_integers(info_api_extended):
    srmonitor: SRVariableMonitor = ALL_GLOBAL_SR_MONITORS[1]
    srmonitor.validate([], info_api_extended)
    
    execute_attr_validation_tests(
        obj=srmonitor,
        attr_tests=[
            ("slider_min", 4.3, TypeValidationError),
            ("slider_max", 90.45, TypeValidationError),
        ],
        validate_func=SRVariableMonitor.validate,
        func_args=[[], info_api_extended],
    )

def test_SRVariableMonitor_validate_invalid_opcode(info_api_extended):
    srmonitor: SRVariableMonitor= copy(ALL_GLOBAL_SR_MONITORS[0])
    srmonitor.opcode = "x position"
    srmonitor.dropdowns = {}
    with raises(InvalidValueError):
        srmonitor.validate([], info_api_extended)


def test_SRVariableMonitor_validate_dont_raise_when_monitor_position_outside_stage(info_api_extended):
    srmonitor: SRVariableMonitor = ALL_GLOBAL_SR_MONITORS[0]
    config = ValidationConfig(raise_when_monitor_position_outside_stage=False) # MARK
    srmonitor.validate([], info_api_extended)



def test_SRListMonitor_validate(info_api_extended):
    srmonitor = ALL_GLOBAL_SR_MONITORS[2]
    srmonitor: SRListMonitor
    srmonitor.validate([], info_api_extended)

def test_SRListMonitor_validate_too_big_size(info_api_extended):
    srmonitor = copy(ALL_GLOBAL_SR_MONITORS[2])
    srmonitor: SRListMonitor
    srmonitor.size = (2*STAGE_WIDTH, 2*STAGE_HEIGHT)
    with raises(RangeValidationError):
        srmonitor.validate([], info_api_extended)
    
    modified_config = copy(config) # MARK
    modified_config: ValidationConfig
    modified_config.raise_when_monitor_bigger_then_stage = False
    srmonitor.validate([], modified_config, info_api_extended)

def test_SRListMonitor_validate_invalid_opcode(info_api_extended):
    srmonitor = copy(ALL_GLOBAL_SR_MONITORS[2])
    srmonitor: SRListMonitor
    srmonitor.opcode = "x position"
    srmonitor.dropdowns = {}
    with raises(InvalidValueError):
        srmonitor.validate([], info_api_extended)


