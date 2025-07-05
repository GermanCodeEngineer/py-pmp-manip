from copy   import copy, deepcopy
from pytest import fixture, raises
from uuid   import uuid4

from pypenguin.utility            import (
    ValidationConfig, 
    ThanksError, TypeValidationError, RangeValidationError, 
    SameValueTwiceError, SpriteLayerStackError,
)
from pypenguin.opcode_info.data import info_api

from pypenguin.core.enums      import SRTTSLanguage, SRVideoState, TargetPlatform
from pypenguin.core.extension  import SRBuiltinExtension, SRCustomExtension
from pypenguin.core.meta       import FRMeta
from pypenguin.core.project    import FRProject, SRProject
from pypenguin.core.target     import FRStage, SRSprite, SRStage
from pypenguin.core.vars_lists import SRVariable, SRList

from tests.core.constants import (
    PROJECT_DATA, PROJECT_ASSET_FILES, 
    FR_PROJECT, SR_PROJECT, 
    SB3_PROJECT_DATA_ORGINAL, SB3_PROJECT_DATA_CONVERTED,
    ALL_FR_MONITORS_CONVERTED,
)

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()


def test_FRProject_from_data():
    frproject = FRProject.from_data(
        data=PROJECT_DATA, 
        asset_files=PROJECT_ASSET_FILES, 
        info_api=info_api,
    )
    assert frproject == FR_PROJECT


def test_FRProject_data_sb3_to_pmp():
    frproject = FRProject._data_sb3_to_pmp(SB3_PROJECT_DATA_ORGINAL)
    assert frproject == SB3_PROJECT_DATA_CONVERTED


def test_FRProject_from_file():
    FRProject.from_file("../tests/assets/testing_blocks.pmp", info_api)
    FRProject.from_file("../tests/assets/scratch_project.sb3", info_api) 
    # TODO: use smaller examples and check equality
    with raises(AssertionError):
        FRProject.from_file("abc/def/ghi/christ_loves_u.bible", info_api)


def test_FRProject_post_init():
    with raises(ThanksError):
        FRProject.from_data(
            data=PROJECT_DATA | {"extensionData": 7}, 
            asset_files=PROJECT_ASSET_FILES,
            info_api=info_api,
        )


def test_FRProject_to_second():
    assert FR_PROJECT.to_second(info_api) == SR_PROJECT

def test_FRProject_to_second_empty_monitor():
    frproject = deepcopy(FR_PROJECT)
    frmonitor = deepcopy(frproject.monitors[0])
    frmonitor.sprite_name = "a non existing sprite"
    frproject.monitors.append(frmonitor)
    assert frproject.to_second(info_api) == SR_PROJECT # means its not included in second representation

def test_FRProject_to_second_tts():
    frproject = deepcopy(FR_PROJECT)
    frstage: FRStage = frproject.targets[0]
    frstage.text_to_speech_language = "de"
    target_srproject = copy(SR_PROJECT)
    target_srproject.text_to_speech_language = SRTTSLanguage.GERMAN
    assert frproject.to_second(info_api) == target_srproject

def test_FRProject_to_second_extensions():
    frproject = copy(FR_PROJECT)
    frproject.extensions = ["jgJSON", "skyhigh173object"]
    frproject.extension_urls = {"skyhigh173object": "https://extensions.penguinmod.com/extensions/skyhigh173/object.js"}
    srproject = frproject.to_second(info_api)
    assert srproject.extensions == [
        SRBuiltinExtension(id="jgJSON"), 
        SRCustomExtension(id="skyhigh173object", url="https://extensions.penguinmod.com/extensions/skyhigh173/object.js"),
    ]




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


def test_SRProject_eq_other_class():
    srproject_a = SRProject.create_empty()
    assert srproject_a != 5

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

    srproject_a.sprite_layer_stack = [sprite_a2.uuid, sprite_a1.uuid]
    srproject_b.sprite_layer_stack = [sprite_b1.uuid]
    assert srproject_a != srproject_b

    srproject_a.sprite_layer_stack = [sprite_a2.uuid, sprite_a1.uuid]
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

def test_SRProject_validate_extensions(config):
    srproject = SRProject.create_empty()
    srproject.extensions.append(SRBuiltinExtension("jgJSON"))
    srproject.validate(config, info_api)


def test_SRProject_validate_same_sprite_name(config):
    srproject = SRProject.create_empty()
    sprite1 = SRSprite.create_empty(name="sprite1")
    sprite2 = SRSprite.create_empty(name="sprite1")
    srproject.sprites = [sprite1, sprite2]
    srproject.sprite_layer_stack = [sprite2.uuid, sprite1.uuid]
    with raises(SameValueTwiceError):
        srproject.validate(config, info_api)

def test_SRProject_validate_sprites_same_sprite_uuid(config):
    srproject = SRProject.create_empty()
    sprite1 = SRSprite.create_empty(name="sprite1")
    sprite2 = SRSprite.create_empty(name="sprite2")
    uuid = sprite1.uuid
    sprite2.__dict__["uuid"] = uuid
    srproject.sprites = [sprite1, sprite2]
    srproject.sprite_layer_stack = [uuid, uuid]
    with raises(SameValueTwiceError):
        srproject._validate_sprites([], config, info_api)

def test_SRProject_validate_sprites_invalid_layer_stack(config):
    srproject = SRProject.create_empty()
    sprite1 = SRSprite.create_empty(name="sprite1")
    sprite2 = SRSprite.create_empty(name="sprite2")
    srproject.sprites = [sprite1, sprite2]
    srproject.sprite_layer_stack = [sprite2.uuid, sprite1.uuid]
    srproject._validate_sprites([], config, info_api)

    srproject.sprite_layer_stack = [sprite1.uuid, uuid4()]
    with raises(SpriteLayerStackError):
        srproject._validate_sprites([], config, info_api)

    srproject.sprite_layer_stack = [sprite1.uuid, sprite1.uuid]
    with raises(SameValueTwiceError):
        srproject._validate_sprites([], config, info_api)
    

def test_SRProject_validate_var_names(config):
    srproject = SRProject.create_empty()
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.sprite_only_variables = [
        SRVariable(name="var1", current_value=")="),
        SRVariable(name="var2", current_value="(="),
    ]
    srproject.sprites = [sprite]
    srproject.sprite_layer_stack = [sprite.uuid]
    srproject._validate_var_names([], config)

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


def test_SRProject_validate_list_names(config):
    srproject = SRProject.create_empty()
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.sprite_only_lists = [
        SRList(name="list1", current_value=[")="]),
        SRList(name="list2", current_value=["(="]),
    ]
    srproject.sprites = [sprite]
    srproject.sprite_layer_stack = [sprite.uuid]
    srproject._validate_list_names([], config)

def test_SRProject_validate_list_names_same_global(config):
    srproject = SRProject.create_empty()
    srproject.all_sprite_lists = [
        SRList(name="same list", current_value=[5]),
        SRList(name="same list", current_value=[";)"]),
    ]
    with raises(SameValueTwiceError):
        srproject._validate_list_names([], config)

def test_SRProject_validate_list_names_same_inter(config):
    srproject = SRProject.create_empty()
    srproject.all_sprite_lists = [SRList(name="same var", current_value=["(;", ");"])]
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.sprite_only_lists = [SRList(name="same var", current_value=[")=", "(="])]
    srproject.sprites = [sprite]
    with raises(SameValueTwiceError):
        srproject._validate_list_names([], config)


def test_SRProject_find_broadcast_messages():
    assert set(SR_PROJECT._find_broadcast_messages()) == {"my message"}


def test_SRProject_to_first_main():
    srproject = deepcopy(SR_PROJECT)
    srproject.sprites[0].scripts = [] # pretend there are no blocks, because they can't be easily compared and are tested elsewhere
    expected_frproject = deepcopy(FR_PROJECT) 
    for target in expected_frproject.targets:
        target.costumes = [costume.to_second(PROJECT_ASSET_FILES).to_first()[0] for costume in target.costumes]
        target.sounds   = [sound  .to_second(PROJECT_ASSET_FILES).to_first()[0] for sound   in target.sounds  ]
    expected_frproject.targets[1].blocks     = {} # see above
    expected_frproject.targets[1].comments   = {} # see above
    expected_frproject.targets[0].broadcasts = {} # see above
    expected_frproject.monitors              = ALL_FR_MONITORS_CONVERTED
    frproject = srproject.to_first(info_api, target_platform=TargetPlatform.PENGUINMOD)
    assert len(frproject.asset_files) == len(expected_frproject.asset_files)
    frproject.asset_files = expected_frproject.asset_files = {}
    assert frproject == expected_frproject

def test_SRProject_to_first_extensions():
    srproject = copy(SR_PROJECT)
    srproject.extensions = [
        SRBuiltinExtension(id="jgJSON"), 
        SRCustomExtension(id="truefantombase", url="https://extensions.turbowarp.org/true-fantom/base.js"),
    ]
    frproject = srproject.to_first(info_api, target_platform=TargetPlatform.PENGUINMOD)
    assert frproject.extensions == ["jgJSON", "truefantombase"]
    assert frproject.extension_urls == {"truefantombase": "https://extensions.turbowarp.org/true-fantom/base.js"}

def test_SRProject_to_first_scratch_platform():
    srproject = SR_PROJECT
    frproject = srproject.to_first(info_api, target_platform=TargetPlatform.SCRATCH)
    assert frproject.meta == FRMeta.new_scratch_meta()
