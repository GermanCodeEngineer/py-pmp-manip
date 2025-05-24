from pytest import fixture, raises
from copy   import copy, deepcopy
from uuid   import uuid4

from pypenguin.utility            import (
    ValidationConfig, 
    ThanksError, TypeValidationError, RangeValidationError, 
    SameValueTwiceError, SpriteLayerStackError,
)
from pypenguin.opcode_info import info_api

from pypenguin.core.enums      import SRTTSLanguage, SRVideoState
from pypenguin.core.project    import FRProject, SRProject
from pypenguin.core.target     import FRStage, SRSprite, SRStage
from pypenguin.core.vars_lists import SRVariable, SRList

from tests.core.constants import PROJECT_DATA, FR_PROJECT, SR_PROJECT

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()


def test_FRProject_from_data():
    frproject = FRProject.from_data(PROJECT_DATA, info_api)
    assert frproject == FR_PROJECT


def test_FRProject_from_pmp_file():
    FRProject._from_pmp_file("../tests/assets/testing_blocks.pmp", info_api)
    with raises(AssertionError):
        FRProject._from_pmp_file("../tests/assets/scratch_project.sb3", info_api)


def test_FRProject_from_sb3_file():
    FRProject._from_sb3_file("../tests/assets/scratch_project.sb3", info_api)
    with raises(AssertionError):
        FRProject._from_sb3_file("../tests/assets/testing_blocks.pmp", info_api)

def test_FRProject_from_file():
    FRProject.from_file("../tests/assets/testing_blocks.pmp", info_api)
    FRProject.from_file("../tests/assets/scratch_project.sb3", info_api)
    with raises(AssertionError):
        FRProject.from_file("abc/def/ghi/jc_loves_u.any", info_api)


def test_FRProject_post_init():
    with raises(ThanksError):
        FRProject.from_data(PROJECT_DATA | {"extensionData": 7}, info_api)


def test_FRProject_step():
    assert FR_PROJECT.step(info_api) == SR_PROJECT

def test_FRProject_step_tts():
    frproject = deepcopy(FR_PROJECT)
    frstage: FRStage = frproject.targets[0]
    frstage.text_to_speech_language = "de"
    target_srproject = copy(SR_PROJECT)
    target_srproject.text_to_speech_language = SRTTSLanguage.GERMAN
    assert frproject.step(info_api) == target_srproject



def test_SRProject_create_empty():
    srproject = SRProject.create_empty()
    assert isinstance(srproject, SRProject)
    assert isinstance(srproject.stage, SRStage)
    assert srproject.sprites == []
    assert srproject.all_sprite_variables == []
    assert srproject.all_sprite_lists == []
    assert srproject.tempo == 60
    assert srproject.video_transparency == 50
    assert srproject.video_state == SRVideoState.ON
    assert srproject.text_to_speech_language == None
    assert srproject.global_monitors == []
    assert srproject.extensions == []


def test_SRProject_eq_empty():
    srproject_a = SRProject.create_empty()
    srproject_b = SRProject.create_empty()
    assert srproject_a == srproject_b

def test_SRProject_eq_copy():
    srproject_a = SRProject.create_empty()
    srproject_b = copy(srproject_a)
    assert srproject_a == srproject_b

def test_SRProject_eq_different():
    srproject_a = SRProject.create_empty()
    srproject_b = SRProject.create_empty()
    srproject_b.all_sprite_variables = [SRVariable(name="an additional var", current_value="some value")]
    assert srproject_a != srproject_b


def test_SRProject_eq_same_sprites():
    srproject_a = SRProject.create_empty()
    sprite_a1 = SRSprite.create_empty(name="sprite1")
    sprite_a2 = SRSprite.create_empty(name="sprite2")
    srproject_a.sprites = [sprite_a1, sprite_a2]

    srproject_b = SRProject.create_empty()
    sprite_b1 = SRSprite.create_empty(name="sprite1")
    sprite_b2 = SRSprite.create_empty(name="sprite2")
    srproject_b.sprites = [sprite_b1, sprite_b2]

    srproject_a.sprite_layer_stack = [sprite_a2.uuid, sprite_a1.uuid]
    srproject_b.sprite_layer_stack = [sprite_b2.uuid, sprite_b1.uuid]
    assert srproject_a == srproject_b

    srproject_b.sprite_layer_stack = [sprite_b1.uuid, sprite_b2.uuid] # reversed
    assert srproject_a != srproject_b



def test_SRProject_validate(config):
    srproject = SR_PROJECT
    srproject.validate(config, info_api)

    execute_attr_validation_tests(
        obj=srproject,
        attr_tests=[
            ("stage", 5, TypeValidationError),
            ("sprites", (), TypeValidationError),
            ("sprites", [6.7], TypeValidationError),
            ("sprite_layer_stack", None, TypeValidationError),
            ("sprite_layer_stack", [None], TypeValidationError),
            ("sprite_layer_stack", [uuid4(), uuid4()], RangeValidationError), # must have exactly 1 item
            ("all_sprite_variables", {}, TypeValidationError),
            ("all_sprite_variables", ["bye"], TypeValidationError),
            ("all_sprite_lists", set(), TypeValidationError),
            ("all_sprite_lists", [{}], TypeValidationError),
            ("tempo", 5.6, TypeValidationError),
            ("tempo", 10, RangeValidationError), # too low
            ("video_transparency", "invalid", TypeValidationError),
            ("video_state", "on", TypeValidationError),
            ("text_to_speech_language", "fr", TypeValidationError),
            ("global_monitors", (), TypeValidationError),
            ("global_monitors", [[]], TypeValidationError),
            ("extensions", 7, TypeValidationError),
            ("extensions", ["jgJSON"], TypeValidationError),
        ],
        validate_func=SRProject.validate,
        func_args=[config, info_api],
    )

def test_SRProject_validate_same_sprite_name(config):
    srproject = SRProject.create_empty()
    sprite1 = SRSprite.create_empty(name="sprite1")
    sprite2 = SRSprite.create_empty(name="sprite1")
    srproject.sprites = [sprite1, sprite2]
    srproject.sprite_layer_stack = [sprite2.uuid, sprite1.uuid]
    with raises(SameValueTwiceError):
        srproject.validate(config, info_api)

def test_SRProject_validate_sprites_layer_order(config):
    srproject = SRProject.create_empty()
    sprite1 = SRSprite.create_empty(name="sprite1")
    sprite2 = SRSprite.create_empty(name="sprite2")
    srproject.sprites = [sprite1, sprite2]
    srproject.sprite_layer_stack = [sprite2.uuid, sprite1.uuid]
    srproject._validate_sprites([], config, info_api)

    srproject.sprite_layer_stack = [sprite1.uuid, uuid4()]
    with raises(SpriteLayerStackError):
        srproject._validate_sprites([], config, info_api)
    


def test_SRProject_validate_var_names_same_global(config):
    srproject = SRProject.create_empty()
    srproject.all_sprite_variables = [
        SRVariable(name="same var", current_value=5),
        SRVariable(name="same var", current_value=";)"),
    ]
    with raises(SameValueTwiceError):
        srproject._validate_var_names([], config)

def test_SRProject_validate_var_names_same_inter(config):
    srproject = SRProject.create_empty()
    srproject.all_sprite_variables = [SRVariable(name="same var", current_value="(;")]
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.sprite_only_variables = [SRVariable(name="same var", current_value=")=")]
    srproject.sprites = [sprite]
    with raises(SameValueTwiceError):
        srproject._validate_var_names([], config)

def test_SRProject_validate_var_list_same_global(config):
    srproject = SRProject.create_empty()
    srproject.all_sprite_lists = [
        SRList(name="same list", current_value=[5]),
        SRList(name="same list", current_value=[";)"]),
    ]
    with raises(SameValueTwiceError):
        srproject._validate_list_names([], config)

def test_SRProject_validate_var_list_same_inter(config):
    srproject = SRProject.create_empty()
    srproject.all_sprite_lists = [SRList(name="same var", current_value=["(;", ");"])]
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.sprite_only_lists = [SRList(name="same var", current_value=[")=", "(="])]
    srproject.sprites = [sprite]
    with raises(SameValueTwiceError):
        srproject._validate_list_names([], config)


