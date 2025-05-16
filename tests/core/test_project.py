from pytest import fixture, raises
from copy   import copy, deepcopy

from pypenguin.utility            import (
    ValidationConfig, 
    ThanksError, TypeValidationError, RangeValidationError, 
)
from pypenguin.opcode_info.groups import info_api
#from pypenguin.opcode_info        import DropdownValueKind, OpcodeType, InputType

from pypenguin.core.enums   import SRTTSLanguage
from pypenguin.core.project import FRProject, SRProject
from pypenguin.core.target  import FRStage

from tests.core.constants   import PROJECT_DATA, FR_PROJECT, SR_PROJECT

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()


def test_FRProject_from_data():
    frproject = FRProject.from_data(PROJECT_DATA, info_api)
    assert frproject == FR_PROJECT


def test_FRProject_from_pmp_file():
    frproject = FRProject.from_pmp_file("../tests/assets/testing_blocks.pmp", info_api)


def test_FRProject_from_sb3_file():
    frproject = FRProject.from_sb3_file("../tests/assets/scratch_project.sb3", info_api)


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
    



def test_SRProject_validate(config):
    srproject = SR_PROJECT
    srproject.validate(config, info_api)

    execute_attr_validation_tests(
        obj=srproject,
        attr_tests=[
            ("stage", 5, TypeValidationError),
            ("sprites", (), TypeValidationError),
            ("sprites", [6.7], TypeValidationError),
            ("all_sprite_variables", {}, TypeValidationError),
            ("all_sprite_variables", ["bye"], TypeValidationError),
            ("all_sprite_lists", set(), TypeValidationError),
            ("all_sprite_lists", [{}], TypeValidationError),
            ("tempo", 5.6, TypeValidationError),
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
