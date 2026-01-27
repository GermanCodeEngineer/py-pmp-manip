from copy     import copy, deepcopy
from pydub    import AudioSegment
from pytest   import fixture, raises
from uuid     import UUID

from pmp_manip.important_consts import SHA256_SEC_TARGET_NAME, SHA256_SEC_DROPDOWN_VALUE
from pmp_manip.opcode_info.api  import DropdownValueKind
from pmp_manip.opcode_info.data import info_api
from pmp_manip.utility          import (
    string_to_sha256, assert_lists_equal_ignore_order, xml_equal, AbstractTreePath,
    MANIP_ThanksError, MANIP_ConversionError, GU_TypeValidationError, GU_RangeValidationError, 
    MANIP_SameValueTwiceError, GU_InvalidValueError
)

from pmp_manip.core.asset           import SRVectorCostume, SRSound
from pmp_manip.core.block_mutation  import SRCustomBlockMutation
from pmp_manip.core.block           import FRBlock, SRScript, SRBlock
from pmp_manip.core.comment         import FRComment, SRComment
from pmp_manip.core.context         import PartialContext
from pmp_manip.core.custom_block    import (
    SRCustomBlockOptype, 
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
)
from pmp_manip.core.enums           import SRSpriteRotationStyle
from pmp_manip.core.target          import FRTarget, FRStage, FRSprite, SRTarget, SRStage, SRSprite
from pmp_manip.core.vars_lists      import SRVariable, SRCloudVariable, SRList

from tests.core.constants import (
    FR_PROJECT, SR_PROJECT, PROJECT_ASSET_FILES,
    SPRITE_DATA, FR_SPRITE, SR_SPRITE, STAGE_DATA, FR_STAGE, SR_STAGE,
    ALL_FR_BLOCKS, ALL_FR_BLOCK_DATAS, ALL_FR_MONITORS_CONVERTED, ALL_COMMENT_DATAS,
)

from tests.utils import execute_attr_validation_tests, nest_all_blocks_comments




@fixture
def info_api_extended():
    info_api_extended = copy(info_api)
    info_api_extended.opcode_info = copy(info_api.opcode_info) 
    # make sure the internals of the DualKeyDict are shallow copied as well
    from tests._gen_ext_opcode_info_.pen import extension
    info_api_extended.add_group(extension)
    return info_api_extended

@fixture
def context():
    my_variable = (DropdownValueKind.VARIABLE, "my variable")
    my_sprite_variable = (DropdownValueKind.VARIABLE, "my sprite variable")
    my_list = (DropdownValueKind.LIST, "my list")
    my_sprite_list = (DropdownValueKind.LIST, "my sprite list")
    return PartialContext(
        scope_variables=[my_variable, my_sprite_variable],
        scope_lists=[my_list, my_sprite_list],

        global_variables=[my_variable],

        local_variables={"my sprite": [my_sprite_variable]},
        local_lists={"my sprite": [my_sprite_list]},

        other_sprites=[(DropdownValueKind.SPRITE, "Sprite2"), (DropdownValueKind.SPRITE, "Player")],
        backdrops=[(DropdownValueKind.BACKDROP, "intro"), (DropdownValueKind.BACKDROP, "scene1")],
    )



def test_FRTarget_from_data_common():
    result = FRTarget._from_data_common(SPRITE_DATA)
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
        def from_data(cls, data) -> "DummyFRTarget":
            pass
        def to_data(self):
            pass
        def to_second(self, asset_files, info_api):
            pass

    with raises(MANIP_ThanksError):
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


def test_FRTarget_to_data_common():
    frsprite = copy(FR_SPRITE)
    frsprite.variables = FR_STAGE.variables
    frsprite.lists = FR_STAGE.lists
    frsprite.broadcasts = FR_STAGE.broadcasts
    expected_blocks = copy(ALL_FR_BLOCK_DATAS)
    del expected_blocks["N"]

    data = frsprite._to_data_common()
    assert data["isStage"] is False
    assert data["name"] == "Sprite1"
    assert data["variables"] == STAGE_DATA["variables"]
    assert data["lists"] == STAGE_DATA["lists"]
    assert data["broadcasts"] == STAGE_DATA["broadcasts"]
    assert data["customVars"] == []
    assert data["blocks"] == expected_blocks
    assert data["comments"] == ALL_COMMENT_DATAS
    assert data["currentCostume"] == 0
    assert data["costumes"] == SPRITE_DATA["costumes"]
    assert data["sounds"] == SPRITE_DATA["sounds"]
    assert data["volume"] == 100
    assert data["layerOrder"] == 1
    assert data["id"] == SPRITE_DATA["id"]


def test_FRTarget_to_second_common(info_api_extended):
    (
        scripts,
        comments,
        costumes,
        sounds,
        _, _,
    )  = FR_SPRITE._to_second_common(PROJECT_ASSET_FILES, info_api_extended)
    assert scripts == SR_SPRITE.scripts
    assert comments == SR_SPRITE.comments
    assert costumes == SR_SPRITE.costumes
    assert sounds == SR_SPRITE.sounds

def test_FRTarget_to_second_common_false_independent_block(info_api_extended):
    frsprite = deepcopy(FR_SPRITE)
    frblock: FRBlock = frsprite.blocks["e"]
    frblock.top_level = True
    frblock.x = 77
    frblock.y = 777
    scripts, _, _, _, _, _ = frsprite._to_second_common(PROJECT_ASSET_FILES, info_api_extended)
    assert scripts == SR_SPRITE.scripts # still same output expected

def test_FRTarget_to_second_common_floating_comment(info_api_extended):
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
    _, floating_comments, _, _, _, _ = frsprite._to_second_common(PROJECT_ASSET_FILES, info_api_extended)
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
    local_variables, local_lists = frsprite._to_second_variables_lists()
    assert local_variables == [
        SRVariable(name="some var", current_value=55),
        SRCloudVariable(name="some cloud var", current_value="https://needgod.net/"),
    ]
    assert local_lists == [
        SRList(name="some list", current_value=["a", "b", "c", "$$$"]),
    ]

def test_FRTarget_to_second_variables_lists_invalid():
    frsprite = copy(FR_STAGE)
    frsprite.variables = {"b-bPdkv!fE]yunTdvpQi": ("some other var", None, None)}
    with raises(MANIP_ConversionError):
        frsprite._to_second_variables_lists()

    frsprite = copy(FR_STAGE)
    frsprite.lists = {"LSfpvIEwXe-upUsR|ypy": ("some other list", None, None)}
    with raises(MANIP_ConversionError):
        frsprite._to_second_variables_lists()



def test_FRStage_from_to_data():
    frstage = FRStage.from_data(STAGE_DATA)
    assert frstage == FR_STAGE

    assert frstage.to_data() == STAGE_DATA

def test_FRStage_from_data_missing_id():
    stage_data = copy(STAGE_DATA)
    del stage_data["id"]
    frstage = FRStage.from_data(stage_data)
    target_stage = copy(FR_STAGE)
    target_stage.id = string_to_sha256("_stage_", secondary=SHA256_SEC_TARGET_NAME) # constant default value
    assert frstage == target_stage


def test_FRStage_to_second():
    srstage, _, _ = FR_STAGE.to_second(PROJECT_ASSET_FILES, info_api)
    assert srstage == SR_STAGE



def test_FRSprite_from_to_data():
    frsprite = FRSprite.from_data(SPRITE_DATA)
    assert frsprite == FR_SPRITE

    expected_blocks = copy(ALL_FR_BLOCK_DATAS)
    del expected_blocks["N"]
    assert frsprite.to_data() == (SPRITE_DATA | {"blocks": expected_blocks})

def test_FRSprite_from_data_missing_id():
    sprite_data = copy(SPRITE_DATA)
    del sprite_data["id"]
    frsprite = FRSprite.from_data(sprite_data)
    target_sprite = copy(FR_SPRITE)
    target_sprite.id = string_to_sha256(target_sprite.name, SHA256_SEC_TARGET_NAME)
    assert frsprite == target_sprite


def test_FRSprite_to_second(info_api_extended):
    srsprite, _, _ = FR_SPRITE.to_second(PROJECT_ASSET_FILES, info_api_extended)
    expected = copy(SR_SPRITE)
    expected.local_monitors = [] # would be added later
    assert srsprite == expected


def test_SRTarget_validate(info_api_extended):
    srtarget = SR_STAGE
    srtarget.validate(AbstractTreePath(), info_api_extended)

    execute_attr_validation_tests(
        obj=srtarget,
        attr_tests=[
            ("scripts", 5, GU_TypeValidationError),
            ("scripts", [5], GU_TypeValidationError),
            ("comments", (), GU_TypeValidationError),
            ("comments", [()], GU_TypeValidationError),
            ("costumes", {}, GU_TypeValidationError),
            ("costumes", [], GU_RangeValidationError),
            ("costumes", [{}], GU_TypeValidationError),
            ("sounds", "a str", GU_TypeValidationError),
            ("sounds", ["a str"], GU_TypeValidationError),
            ("costume_index", "costume1", GU_TypeValidationError),
            ("costume_index", 3, GU_RangeValidationError),
            ("volume", [], GU_TypeValidationError),
            ("volume", -5, GU_RangeValidationError),
            ("volume", 105, GU_RangeValidationError),
        ],
        validate_func=SRTarget.validate,
        func_args=[AbstractTreePath(), info_api],
    )

def test_SRTarget_validate_same_comment():
    srtarget = SRStage.create_empty()
    srtarget.comments = [SRComment(
        position=(10, 10),
        size=(52, 32),
        is_minimized=False,
        text="Comment text",
    )]
    srtarget.validate(AbstractTreePath(), info_api)

def test_SRTarget_validate_same_costume_name():
    srtarget = SRStage.create_empty()
    srtarget.costumes = [
        SRVectorCostume.create_empty(name="costume1"),
        SRVectorCostume.create_empty(name="costume1"),
    ]
    with raises(MANIP_SameValueTwiceError):
        srtarget.validate(AbstractTreePath(), info_api)

def test_SRTarget_validate_same_sound_name():
    srtarget = SRStage.create_empty()
    srtarget.sounds = [
        SRSound(name="Hello there!", file_extension="wav", content=AudioSegment.silent(duration=0)),
        SRSound(name="Hello there!", file_extension="wav", content=AudioSegment.silent(duration=0)),
    ]
    with raises(MANIP_SameValueTwiceError):
        srtarget.validate(AbstractTreePath(), info_api)



def test_SRTarget_validate_scripts(context, info_api_extended):
    srtarget = SR_SPRITE
    srtarget.validate_scripts(AbstractTreePath(), info_api_extended, context)

def test_SRTarget_validate_scripts_same_custom_opcode(context):
    srtarget = SRStage.create_empty()
    cb_def_script = SRScript(
        position=(0, 0),
        blocks=[
            SRBlock(
                opcode="&customblocks::define custom block",
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
    with raises(MANIP_SameValueTwiceError):
        srtarget.validate_scripts(AbstractTreePath(), info_api, context)


def test_SRTarget_get_complete_context(context):
    srtarget = copy(SR_SPRITE)
    srtarget.sounds = [SRSound(name="Hello World!", file_extension="mp3", content=AudioSegment.silent(duration=0))]
    complete_context = srtarget._get_complete_context(context)
    assert complete_context.costumes == [(DropdownValueKind.COSTUME, "costume1")]
    assert complete_context.sounds == [(DropdownValueKind.SOUND, "Hello World!")]
    assert complete_context.is_stage == False

def test_SRTarget_to_first_common_sprite(info_api_extended):
    srtarget = copy(SR_SPRITE)
    srtarget.comments = [ # add some comments
        SRComment(
            position=(10391, 97154),
            size=(300, 300),
            is_minimized=False,
            text="hi :)",
        )
    ]
    
    (
        old_blocks, old_comments,
        old_costumes, old_sounds,
        old_variables, old_lists,
        old_monitors,
        asset_files,
    ) = srtarget._to_first_common(
        info_api_extended,
        global_vars=SR_PROJECT.global_variables,
        global_lists=SR_PROJECT.global_lists,
        global_monitors=SR_PROJECT.global_monitors,
    )
    expected_comments = FR_SPRITE.comments | {
        "qqq": FRComment(
            block_id=None,
            x=10391,
            y=97154,
            width=300,
            height=300,
            minimized=False,
            text="hi :)",
        ),
    }
    nested_generated_blocks, nested_generated_comments = nest_all_blocks_comments(old_blocks, old_comments)
    nested_expected_blocks , nested_expected_comments  = nest_all_blocks_comments(ALL_FR_BLOCKS, expected_comments)
    # Compensate for one "checkbox" block which does not exist to simulate older projects
    for block in nested_expected_blocks:
        if not isinstance(block, FRBlock): continue
        if block.opcode != "control_if": continue
        condition_blocks = block.inputs["CONDITION"]
        if len(condition_blocks) != 2: continue
        first_block = condition_blocks[1]
        if first_block.opcode != "operator_trueBoolean": continue
        block.inputs["CONDITION"] = (
            3,
            condition_blocks[1],
            FRBlock(
                opcode="checkbox",
                next=None,
                parent=Ellipsis,
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
            )
        )
        break
    for block in nested_expected_blocks:
        if not isinstance(block, FRBlock): continue
        if block.opcode != "control_expandableIf": continue
        if block.inputs.get("SUBSTACK1", None) != (1, None): continue
        del block.inputs["SUBSTACK1"]
        break
    assert_lists_equal_ignore_order(nested_generated_blocks, nested_expected_blocks)
    assert_lists_equal_ignore_order(nested_generated_comments, nested_expected_comments)

    # standardize costume and sound hashes:
    assert old_costumes == [costume.to_second(PROJECT_ASSET_FILES).to_first()[0] for costume in FR_SPRITE.costumes]
    assert old_sounds   == [sound  .to_second(PROJECT_ASSET_FILES).to_first()[0] for sound   in FR_SPRITE.sounds  ]
    assert old_variables == FR_SPRITE.variables
    assert old_lists     == FR_SPRITE.lists
    assert_lists_equal_ignore_order(old_monitors, FR_PROJECT.monitors[1:2])
    
    # asset_files cant easily be tested:
    assert len(asset_files) == 2 
    generated_image = old_costumes[0].to_second(asset_files).content
    expected_image  = SR_SPRITE.costumes[0].content
    assert xml_equal(generated_image, expected_image)
    generated_sound = old_sounds[0].to_second(asset_files).content
    expected_sound  = SR_SPRITE.sounds[0].content
    assert generated_sound == expected_sound

def test_SRTarget_to_first_common_stage():
    srtarget = SR_STAGE
    
    (
        old_blocks, old_comments,
        old_costumes, old_sounds,
        old_variables, old_lists,
        old_monitors,
        asset_files,
    ) = srtarget._to_first_common(
        info_api,
        global_vars=SR_PROJECT.global_variables,
        global_lists=SR_PROJECT.global_lists,
        global_monitors=SR_PROJECT.global_monitors,
    )
    # only variables, lists and monitors might differ from a sprite
    assert old_blocks == {}
    assert old_comments == {}
    assert old_variables == FR_STAGE.variables
    assert old_lists     == FR_STAGE.lists
    assert_lists_equal_ignore_order(old_monitors, ALL_FR_MONITORS_CONVERTED[0:1])







def test_SRStage_create_empty():
    srtarget = SRStage.create_empty() 
    assert isinstance(srtarget, SRStage)
    assert srtarget.scripts == []
    assert srtarget.comments == []
    assert srtarget.sounds == []
    assert srtarget.costume_index == 0
    assert srtarget.volume == 100

def test_SRStage_to_first():
    srstage = SR_STAGE
    expected_frstage = copy(FR_STAGE)
    expected_frstage.costumes = [costume.to_second(PROJECT_ASSET_FILES).to_first()[0] for costume in expected_frstage.costumes]
    expected_frstage.sounds   = [sound  .to_second(PROJECT_ASSET_FILES).to_first()[0] for sound   in expected_frstage.sounds  ]
    frstage, old_global_monitors, asset_files = srstage.to_first(
        info_api,
        global_vars=SR_PROJECT.global_variables,
        global_lists=SR_PROJECT.global_lists,
        global_monitors=SR_PROJECT.global_monitors,
        broadcast_messages=["my message"],
        tempo=expected_frstage.tempo,
        video_transparency=expected_frstage.video_transparency,
        video_state=expected_frstage.video_state,
        text_to_speech_language=expected_frstage.text_to_speech_language
    )
    assert frstage == expected_frstage



def test_SRSprite_create_empty():
    srsprite = SRSprite.create_empty(name="Player") 
    assert isinstance(srsprite, SRSprite)
    assert srsprite.scripts == []
    assert srsprite.comments == []
    assert srsprite.sounds == []
    assert srsprite.costume_index == 0
    assert srsprite.volume == 100
    assert srsprite.name == "Player"
    assert srsprite.local_variables == []
    assert srsprite.local_lists == []
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
        srsprite.uuid = "something does not matter"


def test_SRSprite_validate(info_api_extended):
    srsprite = SR_SPRITE
    srsprite.validate(AbstractTreePath(), info_api_extended)

    execute_attr_validation_tests(
        obj=srsprite,
        attr_tests=[
            ("name", False, GU_TypeValidationError),
            ("name", "_stage_", GU_InvalidValueError),
            ("local_variables", (), GU_TypeValidationError),
            ("local_variables", [()], GU_TypeValidationError),
            ("local_lists", {}, GU_TypeValidationError),
            ("local_lists", [{}], GU_TypeValidationError),
            ("local_monitors", None, GU_TypeValidationError),
            ("local_monitors", [None], GU_TypeValidationError),
            ("is_visible", "a str", GU_TypeValidationError),
            ("position", 45, GU_TypeValidationError),
            ("position", ("", ""), GU_TypeValidationError),
            ("size", "100", GU_TypeValidationError),
            ("size", -4, GU_RangeValidationError),
            ("direction", [], GU_TypeValidationError),
            ("direction", 190, GU_RangeValidationError),
            ("is_draggable", [], GU_TypeValidationError),
            ("rotation_style", "don't rotate", GU_TypeValidationError),
        ],
        validate_func=SRSprite.validate,
        func_args=[AbstractTreePath(), info_api_extended],
    )

def test_SRSprite_validate_vars_lists():
    srsprite = SRSprite.create_empty(name="my sprite")
    srsprite.local_variables = [
        SRVariable(name="my var", current_value="Günther Jauch")
    ]
    srsprite.local_lists = [
        SRList(name="my var", current_value=["Günther Jauch", "Dieter Bohlen"])
    ]
    srsprite.validate(AbstractTreePath(), info_api)

def test_SRSprite_validate_uuid():
    srsprite = SRSprite.create_empty(name="my sprite")
    srsprite.__dict__["uuid"] = "abc-def-ghi"
    with raises(GU_TypeValidationError):
        srsprite.validate(AbstractTreePath(), info_api)


def test_SRSprite_validate_monitors(context):
    srsprite = SR_SPRITE
    srsprite.validate_monitor_dropdown_values(AbstractTreePath(), info_api, context)



def test_SRSprite_to_first(info_api_extended):
    srsprite = SR_SPRITE
    expected_frsprite = copy(FR_SPRITE)
    expected_frsprite.costumes = [costume.to_second(PROJECT_ASSET_FILES).to_first()[0] for costume in expected_frsprite.costumes]
    expected_frsprite.sounds   = [sound  .to_second(PROJECT_ASSET_FILES).to_first()[0] for sound   in expected_frsprite.sounds  ]
    frsprite, old_local_monitors, asset_files = srsprite.to_first(
        info_api_extended,
        global_vars=SR_PROJECT.global_variables,
        global_lists=SR_PROJECT.global_lists,
        layer_order=SR_PROJECT.sprite_layer_stack.index(SR_SPRITE.uuid)+1,
    )
    # blocks and comments are tested in _to_first_common, so just ignore:
    frsprite.blocks = {}
    frsprite.comments = {}
    expected_frsprite.blocks = {}
    expected_frsprite.comments = {}
    assert frsprite == expected_frsprite

