from copy   import copy, deepcopy
from uuid   import UUID
from pydub  import AudioSegment
from pytest import fixture, raises, MonkeyPatch

from pypenguin.important_consts import SHA256_SEC_TARGET_NAME
from pypenguin.opcode_info.api  import DropdownValueKind
from pypenguin.opcode_info.data import info_api
from pypenguin.utility          import (
    string_to_sha256,
    ValidationConfig, 
    ThanksError, ConversionError, TypeValidationError, RangeValidationError, 
    SameValueTwiceError, InvalidValueError
)

from pypenguin.core.asset           import SRVectorCostume, SRSound
from pypenguin.core.block_mutation  import SRCustomBlockMutation
from pypenguin.core.block           import FRBlock, SRScript, SRBlock
from pypenguin.core.comment         import FRComment, SRComment
from pypenguin.core.context         import PartialContext
from pypenguin.core.custom_block    import (
    SRCustomBlockOptype, 
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
)
from pypenguin.core.enums           import SRSpriteRotationStyle
from pypenguin.core.target          import FRTarget, FRStage, FRSprite, SRTarget, SRSprite
from pypenguin.core.vars_lists      import SRVariable, SRCloudVariable, SRList

from tests.core.constants import (
    SR_PROJECT, PROJECT_ASSET_FILES,
    SPRITE_DATA, FR_SPRITE, SR_SPRITE, STAGE_DATA, FR_STAGE, SR_STAGE,
    ALL_SR_SCRIPTS, ALL_FR_BLOCKS,
)
from tests.core.test_irblock import TEST_InterToFirstIF
from tests.core.test_srblock import TEST_SecondToInterIF

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
        # to fullfill the abstractmethod requirements:
        @classmethod
        def from_data(cls, data, info_api) -> "DummyFRTarget":
            pass
        def to_second(self, asset_files, info_api):
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


def test_FRTarget_to_second_common():
    (
        scripts,
        comments,
        costumes,
        sounds,
        _, _,
    )  = FR_SPRITE._to_second_common(PROJECT_ASSET_FILES, info_api)
    assert scripts == SR_SPRITE.scripts
    assert comments == SR_SPRITE.comments
    assert costumes == SR_SPRITE.costumes
    assert sounds == SR_SPRITE.sounds

def test_FRTarget_to_second_common_false_independent_block():
    frsprite = deepcopy(FR_SPRITE)
    frblock: FRBlock = frsprite.blocks["e"]
    frblock.top_level = True
    frblock.position = (77, 777)
    scripts, _, _, _, _, _ = frsprite._to_second_common(PROJECT_ASSET_FILES, info_api)
    assert scripts == SR_SPRITE.scripts # still same output expected

def test_FRTarget_to_second_common_floating_comment():
    frsprite = deepcopy(FR_SPRITE)
    frsprite.comments["qqq"] = FRComment(
        block_id=None,
        x=0,
        y=0,
        width=200,
        height=200,
        minimized=False,
        text="a floating comment",
    )
    _, floating_comments, _, _, _, _ = frsprite._to_second_common(PROJECT_ASSET_FILES, info_api)
    assert floating_comments == [SRComment(
        position=(0, 0),
        size=(200, 200),
        is_minimized=False,
        text="a floating comment",
    )]


def test_FRTarget_to_second_variables_lists():
    frsprite = copy(FR_STAGE)
    frsprite.variables = {
        "ZkrFaN(VCdWk,nAAs*L*": ("some var", 55),
        "za}CppN*OcX`Pe`H_Cxj": ("some cloud var", "https://needgod.net/", True),
    }
    frsprite.lists = {
        "S}|FmMKusDx]ogbnuxIa": ("some list", ["a", "b", "c", "$$$"]),
    }
    sprite_only_variables, sprite_only_lists = frsprite._to_second_variables_lists()
    assert sprite_only_variables == [
        SRVariable(name="some var", current_value=55),
        SRCloudVariable(name="some cloud var", current_value="https://needgod.net/"),
    ]
    assert sprite_only_lists == [
        SRList(name="some list", current_value=["a", "b", "c", "$$$"]),
    ]

def test_FRTarget_to_second_variables_lists_invalid():
    frsprite = copy(FR_STAGE)
    frsprite.variables = {"b-bPdkv!fE]yunTdvpQi": ("some other var", None, None)}
    with raises(ConversionError):
        frsprite._to_second_variables_lists()

    frsprite = copy(FR_STAGE)
    frsprite.lists = {"LSfpvIEwXe-upUsR|ypy": ("some other list", None, None)}
    with raises(ConversionError):
        frsprite._to_second_variables_lists()



def test_FRStage_from_data():
    frstage = FRStage.from_data(STAGE_DATA, info_api)
    assert frstage == FR_STAGE

def test_FRStage_from_data_missing_id():
    stage_data = copy(STAGE_DATA)
    del stage_data["id"]
    frstage = FRStage.from_data(stage_data, info_api)
    target_stage = copy(FR_STAGE)
    target_stage.id = string_to_sha256("_stage_", secondary=SHA256_SEC_TARGET_NAME) # constant default value
    assert frstage == target_stage


def test_FRStage_to_second():
    srstage, _, _ = FR_STAGE.to_second(PROJECT_ASSET_FILES, info_api)
    assert srstage == SR_STAGE



def test_FRSprite_from_data():
    frsprite = FRSprite.from_data(SPRITE_DATA, info_api)
    assert frsprite == FR_SPRITE

def test_FRSprite_from_data_missing_id():
    sprite_data = copy(SPRITE_DATA)
    del sprite_data["id"]
    frsprite = FRSprite.from_data(sprite_data, info_api)
    target_sprite = copy(FR_SPRITE)
    target_sprite.id = string_to_sha256(target_sprite.name, SHA256_SEC_TARGET_NAME)
    assert frsprite == target_sprite


def test_FRSprite_to_second():
    srsprite, _, _ = FR_SPRITE.to_second(PROJECT_ASSET_FILES, info_api)
    expected = copy(SR_SPRITE)
    expected.local_monitors = [] # would be added later
    assert srsprite == expected



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

def test_SRTarget_validate_same_comment(config):
    srtarget = SRTarget.create_empty()
    srtarget.comments = [SRComment(
        position=(10, 10),
        size=(52, 32),
        is_minimized=False,
        text="Comment text",
    )]
    srtarget.validate([], config, info_api)

def test_SRTarget_validate_same_costume_name(config):
    srtarget = SRTarget.create_empty()
    srtarget.costumes = [
        SRVectorCostume.create_empty(name="costume1"),
        SRVectorCostume.create_empty(name="costume1"),
    ]
    with raises(SameValueTwiceError):
        srtarget.validate([], config, info_api)

def test_SRTarget_validate_same_sound_name(config):
    srtarget = SRTarget.create_empty()
    srtarget.sounds = [
        SRSound(name="Hello there!", file_extension="wav", content=AudioSegment.silent(duration=0)),
        SRSound(name="Hello there!", file_extension="wav", content=AudioSegment.silent(duration=0)),
    ]
    with raises(SameValueTwiceError):
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
    with raises(SameValueTwiceError):
        srtarget.validate_scripts([], config, info_api, context)


def test_SRTarget_get_complete_context(context):
    srtarget = copy(SR_SPRITE)
    srtarget.sounds = [SRSound(name="Hello World!", file_extension="mp3", content=AudioSegment.silent(duration=0))]
    complete_context = srtarget._get_complete_context(context)
    assert complete_context.costumes == [(DropdownValueKind.COSTUME, "costume1")]
    assert complete_context.sounds == [(DropdownValueKind.SOUND, "Hello World!")]
    assert complete_context.is_stage == False


def test_SRStage_to_first(monkeypatch: MonkeyPatch):
    block_ids = ["s", "b", "t", "e", "u", "v"]
    class LOCKED_SecondToInterIF(TEST_SecondToInterIF):
        def __post_init__(self):
            nonlocal block_ids
            self._block_ids = block_ids
    class LOCKED_InterToFirstIF(TEST_InterToFirstIF):
        def __post_init__(self):
            super().__post_init__()
            nonlocal block_ids
            self._block_ids = block_ids
    import pypenguin.core.target as target_mod
    monkeypatch.setattr(target_mod, "SecondToInterIF", LOCKED_SecondToInterIF)
    monkeypatch.setattr(target_mod, "InterToFirstIF" , LOCKED_InterToFirstIF )
    
    srstage = copy(SR_STAGE)
    srstage.comments = [
        SRComment(
            position=(10391, 97154),
            size=(300, 300),
            is_minimized=False,
            text="hi :)",
        )
    ]
    srstage.scripts = [ALL_SR_SCRIPTS[0]]
    target_frstage = copy(FR_STAGE)
    target_frstage.costumes = [costume.to_second(PROJECT_ASSET_FILES).to_first()[0] for costume in target_frstage.costumes]
    target_frstage.sounds   = [sound  .to_second(PROJECT_ASSET_FILES).to_first()[0] for sound   in target_frstage.sounds  ]
    target_frstage.comments = {
        "a": FRComment(
            block_id=None,
            x=10391,
            y=97154,
            width=300,
            height=300,
            minimized=False,
            text="hi :)",
        ),
    }
    target_frstage.blocks = {k: ALL_FR_BLOCKS[k] for k in {"d", "b", "e", "t", "u", "v"}}
    
    frstage, global_monitors, asset_files = srstage.to_first(
        info_api,
        global_vars=SR_PROJECT.all_sprite_variables,
        global_lists=SR_PROJECT.all_sprite_lists,
        global_monitors=SR_PROJECT.global_monitors,
        broadcast_messages=["my message"],
        tempo=SR_PROJECT.tempo,
        video_transparency=SR_PROJECT.video_transparency,
        video_state=FR_STAGE.video_state,
        text_to_speech_language=FR_STAGE.text_to_speech_language,
    )
    assert frstage.costumes == target_frstage.costumes
    assert frstage.sounds == target_frstage.sounds
    assert frstage.broadcasts == target_frstage.broadcasts
    a = frstage.blocks
    b = target_frstage.blocks
    print(SRBlock.__repr__(a))
    print(SRBlock.__repr__(b))
    #assert len(a) == len(b)
    assert a == b
    #for a_key, a_v in a.items():
    #    if a_key in b and b[a_key] == a_v:
    #        continue
    #    candidates = []
    #    for b_key, b_v in b.items():
    #        if getattr(a_v, "opcode", None) == getattr(b_v, "opcode", None):
    #            candidates.append((b_key, b_v))
    #    if not candidates: raise Exception("NONE FOUND", a_key, a_v.opcode)
    #    print(100*"=")
    #    print("FOR", repr(a_key), f"{len(candidates)} options", a_v)
    #    for c in candidates:
    #        print(c)
    #    #raise Exception()

            
    assert a == b
    #assert frstage.blocks == target_frstage.blocks
    assert frstage.comments == target_frstage.comments
    assert frstage == target_frstage
    raise Exception("SUCCES")
    assert global_monitors == [] # TODO
    assert asset_files == 0 # TODO



def test_SRSprite_create_empty():
    srsprite = SRSprite.create_empty(name="Player") 
    assert isinstance(srsprite, SRSprite)
    assert srsprite.scripts == []
    assert srsprite.comments == []
    assert srsprite.costume_index == 0
    assert srsprite.sounds == []
    assert srsprite.volume == 100
    assert srsprite.name == "Player"
    assert srsprite.sprite_only_variables == []
    assert srsprite.sprite_only_lists == []
    assert srsprite.local_monitors == []
    assert srsprite.is_visible is True
    assert srsprite.position == (0, 0)
    assert srsprite.size == 100
    assert srsprite.direction == 90
    assert srsprite.is_draggable is False
    assert srsprite.rotation_style == SRSpriteRotationStyle.ALL_AROUND
    assert isinstance(srsprite.uuid, UUID)


def test_SRSprite_setattr():
    srsprite = SR_SPRITE
    with raises(AttributeError):
        srsprite.uuid = "something doesn't matter"


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

def test_SRSprite_validate_vars_lists(config):
    srsprite = SRSprite.create_empty(name="my sprite")
    srsprite.sprite_only_variables = [
        SRVariable(name="my var", current_value="Günther Jauch")
    ]
    srsprite.sprite_only_lists = [
        SRList(name="my var", current_value=["Günther Jauch", "Dieter Bohlen"])
    ]
    srsprite.validate([], config, info_api)

def test_SRSprite_validate_uuid(config):
    srsprite = SRSprite.create_empty(name="my sprite")
    srsprite.__dict__["uuid"] = "abc-def-ghi"
    with raises(TypeValidationError):
        srsprite.validate([], config, info_api)


def test_SRSprite_validate_monitors(config, context):
    srsprite = SR_SPRITE
    srsprite.validate_monitor_dropdown_values([], config, info_api, context)

