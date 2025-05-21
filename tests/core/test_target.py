from pytest import fixture, raises
from copy   import copy

from pypenguin.utility            import (
    string_to_sha256,
    ValidationConfig, 
    ThanksError, FirstToSecondConversionError, TypeValidationError, RangeValidationError, 
    SameNameTwiceError, InvalidValueError
)
from pypenguin.opcode_info import DropdownValueKind
from pypenguin.opcode_info.groups import info_api

from pypenguin.core.asset          import SRCostume, SRSound
from pypenguin.core.block          import SRScript, SRBlock
from pypenguin.core.block_mutation import SRCustomBlockMutation
from pypenguin.core.context        import PartialContext
from pypenguin.core.custom_block   import SRCustomBlockOptype, SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType
from pypenguin.core.dropdown       import SRDropdownValue
from pypenguin.core.enums          import SRSpriteRotationStyle
from pypenguin.core.target         import FRTarget, FRStage, FRSprite, SRTarget, SRSprite
from pypenguin.core.vars_lists     import SRVariable, SRCloudVariable, SRList

from tests.core.constants import SPRITE_DATA, STAGE_DATA, FR_SPRITE, FR_STAGE, SR_SPRITE, SR_STAGE

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()

@fixture
def context():
    my_variable = (DropdownValueKind.VARIABLE, "my variable")
    my_sprite_variable = (DropdownValueKind.VARIABLE, "my sprite variable")
    my_list = (DropdownValueKind.LIST, "my list")
    my_sprite_list = (DropdownValueKind.LIST, "my sprite list")
    return PartialContext(
        scope_variables=[my_variable, my_sprite_variable],
        scope_lists=[my_list, my_sprite_list],

        all_sprite_variables=[my_variable],

        sprite_only_variables=[my_sprite_variable],
        sprite_only_lists=[my_sprite_list],

        other_sprites=[(DropdownValueKind.SPRITE, "Sprite2"), (DropdownValueKind.SPRITE, "Player")],
        backdrops=[(DropdownValueKind.BACKDROP, "intro"), (DropdownValueKind.BACKDROP, "scene1")],
    )





def test_FRTarget_from_data_common():
    result = FRTarget._from_data_common(SPRITE_DATA, info_api)
    goal = {
        "is_stage": False,
        "name": "Sprite1",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "custom_vars": [],
        "blocks": FR_SPRITE.blocks,
        "comments": FR_SPRITE.comments,
        "current_costume": 0,
        "costumes": FR_SPRITE.costumes,
        "sounds": FR_SPRITE.sounds,
        "volume": 100,
        "layer_order": 1,
    }
    assert result == goal


def test_FRTarget_post_init():
    class DummyFRTarget(FRTarget):
        @classmethod # to fullfill the abstractmethod requirement
        def from_data(cls, data, info_api) -> "DummyFRTarget":
            pass

    with raises(ThanksError):
        DummyFRTarget(
            is_stage=...,
            name=...,
            variables=...,
            lists=...,
            broadcasts=...,
            custom_vars="something else",
            blocks=...,
            comments=...,
            current_costume=...,
            costumes=...,
            sounds=...,
            volume=...,
            layer_order=...,
            id=...,
        )


def test_FRTarget_step_common():
    (
        scripts,
        comments,
        costumes,
        sounds,
        _, _,
    )  = FR_SPRITE._step_common(info_api)
    assert scripts == SR_SPRITE.scripts
    assert comments == SR_SPRITE.comments
    assert costumes == SR_SPRITE.costumes
    assert sounds == SR_SPRITE.sounds


def test_FRTarget_step_variables_lists():
    frsprite = copy(FR_STAGE)
    frsprite.variables = {
        "ZkrFaN(VCdWk,nAAs*L*": ("some var", 55),
        "za}CppN*OcX`Pe`H_Cxj": ("some cloud var", "https://needgod.net/", True),
    }
    frsprite.lists = {
        "S}|FmMKusDx]ogbnuxIa": ("some list", ["a", "b", "c", "$$$"]),
    }
    sprite_only_variables, sprite_only_lists = frsprite._step_variables_lists()
    assert sprite_only_variables == [
        SRVariable(name="some var", current_value=55),
        SRCloudVariable(name="some cloud var", current_value="https://needgod.net/"),
    ]
    assert sprite_only_lists == [
        SRList(name="some list", current_value=["a", "b", "c", "$$$"]),
    ]

def test_FRTarget_step_variables_lists_invalid():
    frsprite = copy(FR_STAGE)
    frsprite.variables = {"b-bPdkv!fE]yunTdvpQi": ("some other var", None, None)}
    with raises(FirstToSecondConversionError):
        frsprite._step_variables_lists()

    frsprite = copy(FR_STAGE)
    frsprite.variables = {"LSfpvIEwXe-upUsR|ypy": ("some other list", None, None)}
    with raises(FirstToSecondConversionError):
        frsprite._step_variables_lists()



def test_FRStage_from_data():
    frstage = FRStage.from_data(STAGE_DATA, info_api)
    assert frstage == FR_STAGE

def test_FRStage_from_data_missing_id():
    stage_data = copy(STAGE_DATA)
    del stage_data["id"]
    frstage = FRStage.from_data(stage_data, info_api)
    target_stage = copy(FR_STAGE)
    target_stage.id = string_to_sha256("_stage_") # constant default value
    assert frstage == target_stage


def test_FRStage_step():
    srstage, _, _ = FR_STAGE.step(info_api)
    assert srstage == SR_STAGE



def test_FRSprite_from_data():
    frsprite = FRSprite.from_data(SPRITE_DATA, info_api)
    assert frsprite == FR_SPRITE

def test_FRSprite_from_data_missing_id():
    sprite_data = copy(SPRITE_DATA)
    del sprite_data["id"]
    frsprite = FRSprite.from_data(sprite_data, info_api)
    target_sprite = copy(FR_SPRITE)
    target_sprite.id = string_to_sha256(target_sprite.name) # constant default value
    assert frsprite == target_sprite


def test_FRSprite_step():
    srsprite, _, _ = FR_SPRITE.step(info_api)
    assert srsprite == SR_SPRITE



def test_SRTarget_create_empty():
    srtarget = SRTarget.create_empty() 
    assert isinstance(srtarget, SRTarget)
    assert srtarget.scripts == []
    assert srtarget.comments == []
    assert srtarget.costume_index == 0
    assert srtarget.sounds == []
    assert srtarget.volume == 100


def test_SRTarget_validate(config):
    srtarget = SR_STAGE
    srtarget.validate([], config, info_api)

    execute_attr_validation_tests(
        obj=srtarget,
        attr_tests=[
            ("scripts", 5, TypeValidationError),
            ("scripts", [5], TypeValidationError),
            ("comments", (), TypeValidationError),
            ("comments", [()], TypeValidationError),
            ("costumes", {}, TypeValidationError),
            ("costumes", [], RangeValidationError),
            ("costumes", [{}], TypeValidationError),
            ("costume_index", "costume1", TypeValidationError),
            ("costume_index", 3, RangeValidationError),
            ("sounds", "a str", TypeValidationError),
            ("sounds", ["a str"], TypeValidationError),
            ("volume", [], TypeValidationError),
            ("volume", -5, RangeValidationError),
            ("volume", 105, RangeValidationError),
        ],
        validate_func=SRTarget.validate,
        func_args=[[], config, info_api],
    )

def test_SRTarget_validate_same_costume_name(config):
    srtarget = SRTarget.create_empty()
    srtarget.costumes = [
        SRCostume.create_empty(name="costume1"),
        SRCostume.create_empty(name="costume1"),
    ]
    with raises(SameNameTwiceError):
        srtarget.validate([], config, info_api)

def test_SRTarget_validate_same_sound_name(config):
    srtarget = SRTarget.create_empty()
    srtarget.sounds = [
        SRSound(name="Hello there!", file_extension="wav"),
        SRSound(name="Hello there!", file_extension="wav"),
    ]
    with raises(SameNameTwiceError):
        srtarget.validate([], config, info_api)



def test_SRTarget_validate_scripts(config, context):
    srtarget = SR_SPRITE
    srtarget.validate_scripts([], config, info_api, context)

def test_SRTarget_validate_scripts_same_custom_opcode(config, context):
    srtarget = SRTarget.create_empty()
    cb_def_script = SRScript(
        position=(0, 0),
        blocks=[
            SRBlock(
                opcode="define custom block",
                inputs={},
                dropdowns={},
                comment=None,
                mutation=SRCustomBlockMutation(
                    custom_opcode=SRCustomBlockOpcode(segments=(
                        "hi", SRCustomBlockArgument("name", SRCustomBlockArgumentType.STRING_NUMBER),
                    )),
                    no_screen_refresh=True,
                    optype=SRCustomBlockOptype.ENDING_STATEMENT,
                    main_color="#FF6680",
                    prototype_color="#FF4D6A",
                    outline_color="#FF3355",
                ),
            ),
        ],
    )
    srtarget.scripts = [
        cb_def_script,
        copy(cb_def_script),
    ]
    with raises(SameNameTwiceError):
        srtarget.validate_scripts([], config, info_api, context)


def test_SRTarget_get_complete_context(context):
    srtarget = copy(SR_SPRITE)
    srtarget.sounds = [SRSound(name="Hello World!", file_extension="mp3")]
    complete_context = srtarget.get_complete_context(context)
    assert complete_context.costumes == [SRDropdownValue(DropdownValueKind.COSTUME, "costume1")]
    assert complete_context.sounds == [SRDropdownValue(DropdownValueKind.SOUND, "Hello World!")]
    assert complete_context.is_stage == False



def test_SRSprite_create_empty():
    srsprite = SRSprite.create_empty(name="Player", layer_order=2) 
    assert isinstance(srsprite, SRTarget)
    assert srsprite.scripts == []
    assert srsprite.comments == []
    assert srsprite.costume_index == 0
    assert srsprite.sounds == []
    assert srsprite.volume == 100
    assert srsprite.name == "Player"
    assert srsprite.sprite_only_variables == []
    assert srsprite.sprite_only_lists == []
    assert srsprite.local_monitors == []
    assert srsprite.layer_order == 2
    assert srsprite.is_visible is True
    assert srsprite.position == (0, 0)
    assert srsprite.size == 100
    assert srsprite.direction == 90
    assert srsprite.is_draggable is False
    assert srsprite.rotation_style == SRSpriteRotationStyle.ALL_AROUND


def test_SRSprite_validate(config):
    srsprite = SR_SPRITE
    srsprite.validate([], config, info_api)

    execute_attr_validation_tests(
        obj=srsprite,
        attr_tests=[
            ("name", False, TypeValidationError),
            ("name", "_stage_", InvalidValueError),
            ("sprite_only_variables", (), TypeValidationError),
            ("sprite_only_variables", [()], TypeValidationError),
            ("sprite_only_lists", {}, TypeValidationError),
            ("sprite_only_lists", [{}], TypeValidationError),
            ("local_monitors", None, TypeValidationError),
            ("local_monitors", [None], TypeValidationError),
            ("layer_order", "costume1", TypeValidationError),
            ("layer_order", 0, RangeValidationError),
            ("is_visible", "a str", TypeValidationError),
            ("position", 45, TypeValidationError),
            ("position", ("", ""), TypeValidationError),
            ("size", "100", TypeValidationError),
            ("size", -4, RangeValidationError),
            ("direction", [], TypeValidationError),
            ("direction", 190, RangeValidationError),
            ("is_draggable", [], TypeValidationError),
            ("rotation_style", "don't rotate", TypeValidationError),
        ],
        validate_func=SRSprite.validate,
        func_args=[[], config, info_api],
    )


def test_SRSprite_validate_monitors(config, context):
    srsprite = SR_SPRITE
    srsprite.validate_monitor_dropdown_values([], config, info_api, context)

