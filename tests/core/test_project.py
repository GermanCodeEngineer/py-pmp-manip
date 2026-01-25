from copy   import copy, deepcopy
from pytest import fixture, raises, MonkeyPatch
from uuid   import uuid4

from pmp_manip.utility            import (
    gdumps, KeyReprDict, AbstractTreePath,
    MANIPO_TypeValidationError, MANIPO_RangeValidationError, 
    MANIP_SameValueTwiceError, MANIP_SpriteLayerStackError,
)
from pmp_manip.opcode_info.data import info_api

from pmp_manip.core.enums      import SRTTSLanguage, SRVideoState, TargetPlatform
from pmp_manip.core.extension  import SRBuiltinExtension, SRCustomExtension
from pmp_manip.core.meta       import FRMeta
from pmp_manip.core.project    import FRProject, SRProject
from pmp_manip.core.target     import FRStage, SRSprite, SRStage
from pmp_manip.core.vars_lists import SRVariable, SRList

from tests.core.constants import (
    ALL_FR_BLOCK_DATAS, PROJECT_DATA, PROJECT_ASSET_FILES, 
    FR_PROJECT, SR_PROJECT, 
    SB3_PROJECT_DATA_ORGINAL, SB3_PROJECT_DATA_CONVERTED,
    ALL_FR_MONITORS_CONVERTED,
)

from tests.utility import execute_attr_validation_tests

@fixture
def info_api_extended():
    info_api_extended = copy(info_api)
    info_api_extended.opcode_info = copy(info_api.opcode_info) 
    # make sure the internals of the DualKeyDict are shallow copied as well
    from tests._gen_ext_opcode_info_.pen import extension
    info_api_extended.add_group(extension)
    return info_api_extended


def test_FRProject_from_to_data():
    frproject = FRProject.from_data(
        data=PROJECT_DATA, 
        asset_files=PROJECT_ASSET_FILES, 
    )
    assert frproject == FR_PROJECT

    expected_data = copy(PROJECT_DATA)
    expected_data["targets"] = copy(PROJECT_DATA["targets"])
    expected_data["targets"][1] = copy(PROJECT_DATA["targets"][1])
    expected_data["targets"][1]["blocks"] = copy(ALL_FR_BLOCK_DATAS)
    del expected_data["targets"][1]["blocks"]["N"]
    expected_data["extensionURLs"] = {}

    project_data, asset_files = frproject.to_data()
    assert project_data == expected_data
    assert asset_files == PROJECT_ASSET_FILES


def test_FRProject_data_sb3_to_pmp():
    frproject = FRProject._data_sb3_to_pmp(SB3_PROJECT_DATA_ORGINAL)
    assert frproject == SB3_PROJECT_DATA_CONVERTED


def test_FRProject_from_file():
    FRProject.from_file("tests/_assets_/testing_blocks.pmp")
    FRProject.from_file("tests/_assets_/scratch_project.sb3") 
    # TODO: use smaller examples and check equality


def test_FRProject_post_init():
    ... # TODO
    #with raises(MANIP_ThanksError):
    #    FRProject.from_data(
    #        data=PROJECT_DATA | {"extensionData": 7}, 
    #        asset_files=PROJECT_ASSET_FILES,
    #    )


def test_FRProject_add_all_extensions_to_info_api(monkeypatch: MonkeyPatch):
    frproject = copy(FR_PROJECT)
    frproject.extensions = ["pen", "pointerlock", "jgJSON"]
    frproject.extension_urls = KeyReprDict({"pointerlock": "https://extensions.turbowarp.org/pointerlock.js"})

    info_api_copy = deepcopy(info_api)
    results = set()
    def fake_generate_and_add_extension(extension_id: str, extension_source: str | None):
        results.add((extension_id, extension_source))
    monkeypatch.setattr(info_api_copy, "generate_and_add_extension", fake_generate_and_add_extension)

    frproject.add_all_extensions_to_info_api(info_api_copy)
    assert results == {
        ("jgJSON", None),
        ("pointerlock", "https://extensions.turbowarp.org/pointerlock.js"),
        ("pen", None),
    }


def test_FRProject_to_file(monkeypatch: MonkeyPatch):
    class DummyProject(FRProject):
        def __init__(self):
            pass

        def to_data(self):
            return (
                {"name": "My Project"},  # some dumb example data
                {"image.png": b"image-bytes"}  # asset_files
            )

    def fake_create_zip_file(path, contents):
        assert path == "project.sb3"
        assert contents == {
            "project.json": gdumps({"name": "My Project"}).encode(),
            "image.png": b"image-bytes",
        }

    from pmp_manip.core import project as project_mod
    monkeypatch.setattr(project_mod, "create_zip_file", fake_create_zip_file)

    dummy_project = DummyProject()
    FRProject.to_file(dummy_project, "project.sb3")


def test_FRProject_to_second(info_api_extended):
    assert FR_PROJECT.to_second(info_api_extended) == SR_PROJECT

def test_FRProject_to_second_empty_monitor(info_api_extended):
    frproject = deepcopy(FR_PROJECT)
    frmonitor = deepcopy(frproject.monitors[0])
    frmonitor.sprite_name = "a non existing sprite"
    frproject.monitors.append(frmonitor)
    assert frproject.to_second(info_api_extended) == SR_PROJECT # means its not included in second representation

def test_FRProject_to_second_tts(info_api_extended):
    frproject = deepcopy(FR_PROJECT)
    frstage: FRStage = frproject.targets[0]
    frstage.text_to_speech_language = "de"
    target_srproject = copy(SR_PROJECT)
    target_srproject.text_to_speech_language = SRTTSLanguage.GERMAN
    assert frproject.to_second(info_api_extended) == target_srproject

def test_FRProject_to_second_extensions(info_api_extended):
    frproject = copy(FR_PROJECT)
    frproject.extensions = ["jgJSON", "skyhigh173object"]
    frproject.extension_urls = KeyReprDict({"skyhigh173object": "https://extensions.penguinmod.com/extensions/skyhigh173/object.js"})
    srproject = frproject.to_second(info_api_extended)
    assert srproject.extensions == [
        SRBuiltinExtension(id="jgJSON"), 
        SRCustomExtension(id="skyhigh173object", url="https://extensions.penguinmod.com/extensions/skyhigh173/object.js"),
    ]




def test_SRProject_create_empty():
    srproject = SRProject.create_empty()
    assert isinstance(srproject, SRProject)
    assert isinstance(srproject.stage, SRStage)
    assert srproject.sprites == []
    assert srproject.global_variables == []
    assert srproject.global_lists == []
    assert srproject.global_monitors == []
    assert srproject.tempo == 60
    assert srproject.video_transparency == 50
    assert srproject.video_state == SRVideoState.ON
    assert srproject.text_to_speech_language == None
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
    srproject_b.global_variables = [SRVariable(name="an additional var", current_value="some value")]
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



def test_SRProject_validate(info_api_extended):
    srproject = SR_PROJECT
    srproject.validate(AbstractTreePath(), info_api_extended)

    execute_attr_validation_tests(
        obj=srproject,
        attr_tests=[
            ("stage", 5, MANIPO_TypeValidationError),
            ("sprites", (), MANIPO_TypeValidationError),
            ("sprites", [6.7], MANIPO_TypeValidationError),
            ("sprite_layer_stack", None, MANIPO_TypeValidationError),
            ("sprite_layer_stack", [None], MANIPO_TypeValidationError),
            ("sprite_layer_stack", [uuid4(), uuid4()], MANIPO_RangeValidationError), # must have exactly 1 item
            ("global_variables", {}, MANIPO_TypeValidationError),
            ("global_variables", ["bye"], MANIPO_TypeValidationError),
            ("global_lists", set(), MANIPO_TypeValidationError),
            ("global_lists", [{}], MANIPO_TypeValidationError),
            ("global_monitors", (), MANIPO_TypeValidationError),
            ("global_monitors", [[]], MANIPO_TypeValidationError),
            ("extensions", 7, MANIPO_TypeValidationError),
            ("extensions", ["jgJSON"], MANIPO_TypeValidationError),
            ("tempo", 5.6, MANIPO_TypeValidationError),
            ("tempo", 10, MANIPO_RangeValidationError), # too low
            ("video_transparency", "invalid", MANIPO_TypeValidationError),
            ("video_state", "on", MANIPO_TypeValidationError),
            ("text_to_speech_language", "fr", MANIPO_TypeValidationError),
        ],
        validate_func=SRProject.validate,
        func_args=[AbstractTreePath(), info_api],
    )

def test_SRProject_validate_extensions():
    srproject = SRProject.create_empty()
    srproject.extensions.append(SRBuiltinExtension("jgJSON"))
    srproject.validate(AbstractTreePath(), info_api)


def test_SRProject_validate_same_sprite_name():
    srproject = SRProject.create_empty()
    sprite1 = SRSprite.create_empty(name="sprite1")
    sprite2 = SRSprite.create_empty(name="sprite1")
    srproject.sprites = [sprite1, sprite2]
    srproject.sprite_layer_stack = [sprite2.uuid, sprite1.uuid]
    with raises(MANIP_SameValueTwiceError):
        srproject.validate(AbstractTreePath(), info_api)

def test_SRProject_validate_same_extension_id():
    srproject = SRProject.create_empty()
    srproject.extensions = [
        SRBuiltinExtension(id="thatExtension"),
        SRBuiltinExtension(id="thatExtension"),
    ]
    with raises(MANIP_SameValueTwiceError):
        srproject.validate(AbstractTreePath(), info_api)

def test_SRProject_validate_sprites_same_sprite_uuid():
    srproject = SRProject.create_empty()
    sprite1 = SRSprite.create_empty(name="sprite1")
    sprite2 = SRSprite.create_empty(name="sprite2")
    uuid = sprite1.uuid
    sprite2.__dict__["uuid"] = uuid
    srproject.sprites = [sprite1, sprite2]
    srproject.sprite_layer_stack = [uuid, uuid]
    with raises(MANIP_SameValueTwiceError):
        srproject._validate_sprites(AbstractTreePath(), info_api)

def test_SRProject_validate_sprites_invalid_layer_stack():
    srproject = SRProject.create_empty()
    sprite1 = SRSprite.create_empty(name="sprite1")
    sprite2 = SRSprite.create_empty(name="sprite2")
    srproject.sprites = [sprite1, sprite2]
    srproject.sprite_layer_stack = [sprite2.uuid, sprite1.uuid]
    srproject._validate_sprites(AbstractTreePath(), info_api)

    srproject.sprite_layer_stack = [sprite1.uuid, uuid4()]
    with raises(MANIP_SpriteLayerStackError):
        srproject._validate_sprites(AbstractTreePath(), info_api)

    srproject.sprite_layer_stack = [sprite1.uuid, sprite1.uuid]
    with raises(MANIP_SameValueTwiceError):
        srproject._validate_sprites(AbstractTreePath(), info_api)
    

def test_SRProject_validate_var_names():
    srproject = SRProject.create_empty()
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.local_variables = [
        SRVariable(name="var1", current_value=")="),
        SRVariable(name="var2", current_value="(="),
    ]
    srproject.sprites = [sprite]
    srproject.sprite_layer_stack = [sprite.uuid]
    srproject._validate_var_names(AbstractTreePath())

def test_SRProject_validate_var_names_same_global():
    srproject = SRProject.create_empty()
    srproject.global_variables = [
        SRVariable(name="same var", current_value=5),
        SRVariable(name="same var", current_value=";)"),
    ]
    with raises(MANIP_SameValueTwiceError):
        srproject._validate_var_names(AbstractTreePath())

def test_SRProject_validate_var_names_same_inter():
    srproject = SRProject.create_empty()
    srproject.global_variables = [SRVariable(name="same var", current_value="(;")]
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.local_variables = [SRVariable(name="same var", current_value=")=")]
    srproject.sprites = [sprite]
    with raises(MANIP_SameValueTwiceError):
        srproject._validate_var_names(AbstractTreePath())


def test_SRProject_validate_list_names():
    srproject = SRProject.create_empty()
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.local_lists = [
        SRList(name="list1", current_value=[")="]),
        SRList(name="list2", current_value=["(="]),
    ]
    srproject.sprites = [sprite]
    srproject.sprite_layer_stack = [sprite.uuid]
    srproject._validate_list_names(AbstractTreePath())

def test_SRProject_validate_list_names_same_global():
    srproject = SRProject.create_empty()
    srproject.global_lists = [
        SRList(name="same list", current_value=[5]),
        SRList(name="same list", current_value=[";)"]),
    ]
    with raises(MANIP_SameValueTwiceError):
        srproject._validate_list_names(AbstractTreePath())

def test_SRProject_validate_list_names_same_inter():
    srproject = SRProject.create_empty()
    srproject.global_lists = [SRList(name="same var", current_value=["(;", ");"])]
    sprite = SRSprite.create_empty(name="Sprite1")
    sprite.local_lists = [SRList(name="same var", current_value=[")=", "(="])]
    srproject.sprites = [sprite]
    with raises(MANIP_SameValueTwiceError):
        srproject._validate_list_names(AbstractTreePath())


def test_SRProject_add_all_extensions_to_info_api(monkeypatch: MonkeyPatch):
    srproject = copy(SR_PROJECT)
    srproject.extensions = [
        SRBuiltinExtension(id="pen"),
        SRCustomExtension(id="pointerlock", url="https://extensions.turbowarp.org/pointerlock.js"),
        SRBuiltinExtension(id="jgJSON"),
    ]

    info_api_copy = deepcopy(info_api)
    results = set()
    def fake_generate_and_add_extension(extension_id: str, extension_source: str | None):
        results.add((extension_id, extension_source))
    monkeypatch.setattr(info_api_copy, "generate_and_add_extension", fake_generate_and_add_extension)

    srproject.add_all_extensions_to_info_api(info_api_copy)
    assert results == {
        ("jgJSON", None),
        ("pointerlock", "https://extensions.turbowarp.org/pointerlock.js"),
        ("pen", None),
    }


def test_SRProject_find_broadcast_messages():
    assert set(SR_PROJECT._find_broadcast_messages()) == {"my message"}


def test_SRProject_to_first_main(info_api_extended):
    srproject = deepcopy(SR_PROJECT)
    srproject.sprites[0].scripts = [] # pretend there are no blocks, because they can not be easily compared and are tested elsewhere
    expected_frproject = deepcopy(FR_PROJECT) 
    for target in expected_frproject.targets:
        target.costumes = [costume.to_second(PROJECT_ASSET_FILES).to_first()[0] for costume in target.costumes]
        target.sounds   = [sound  .to_second(PROJECT_ASSET_FILES).to_first()[0] for sound   in target.sounds  ]
    expected_frproject.targets[1].blocks     = {} # see above
    expected_frproject.targets[1].comments   = {} # see above
    expected_frproject.targets[0].broadcasts = {} # see above
    expected_frproject.monitors              = ALL_FR_MONITORS_CONVERTED
    frproject = srproject.to_first(info_api_extended, target_platform=TargetPlatform.PENGUINMOD)
    assert len(frproject.asset_files) == len(expected_frproject.asset_files)
    frproject.asset_files = expected_frproject.asset_files = KeyReprDict()
    assert frproject == expected_frproject

def test_SRProject_to_first_extensions(info_api_extended):
    srproject = copy(SR_PROJECT)
    srproject.extensions = [
        SRBuiltinExtension(id="jgJSON"), 
        SRCustomExtension(id="truefantombase", url="https://extensions.turbowarp.org/true-fantom/base.js"),
    ]
    frproject = srproject.to_first(info_api_extended, target_platform=TargetPlatform.PENGUINMOD)
    assert frproject.extensions == ["jgJSON", "truefantombase"]
    assert frproject.extension_urls == KeyReprDict({"truefantombase": "https://extensions.turbowarp.org/true-fantom/base.js"})

def test_SRProject_to_first_scratch_platform(info_api_extended):
    srproject = SR_PROJECT
    frproject = srproject.to_first(info_api_extended, target_platform=TargetPlatform.SCRATCH)
    assert frproject.meta == FRMeta.new_scratch_meta()
