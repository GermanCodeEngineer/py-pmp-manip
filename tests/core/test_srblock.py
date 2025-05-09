from pytest import raises, fixture
from copy   import copy, deepcopy

from pypenguin.utility            import (
    ValidationConfig, 
    TypeValidationError, RangeValidationError, InvalidOpcodeError, InvalidBlockShapeError,
    UnnecessaryInputError, MissingInputError, UnnecessaryDropdownError, MissingDropdownError,
)
from pypenguin.opcode_info.groups import info_api
from pypenguin.opcode_info        import DropdownValueKind

from pypenguin.core.block     import SRScript, SRBlock, SRBlockOnlyInputValue
from pypenguin.core.block_api import ValidationAPI
from pypenguin.core.context   import CompleteContext
from pypenguin.core.dropdown  import SRDropdownValue


from tests.core.constants import ALL_SR_SCRIPTS

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()

@fixture
def validation_api():
    return ValidationAPI(
        scripts=ALL_SR_SCRIPTS,
    )

@fixture
def context():
    return CompleteContext(
        scope_variables=[SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="my variable")],
        scope_lists=[SRDropdownValue(kind=DropdownValueKind.LIST, value="my list")],

        all_sprite_variables=[SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="my variable")],

        sprite_only_variables=[],
        sprite_only_lists=[],

        other_sprites=[],
        backdrops=[],
        costumes=[],
        sounds=[],

        is_stage=False,
    )

def test_srscript_validate(config, validation_api, context):        
    script = ALL_SR_SCRIPTS[0]
    script.validate(
        path=[],
        config=config,
        info_api=info_api,
        validation_api=validation_api,
        context=context,
    )

    execute_attr_validation_tests(
        obj=script,
        attr_tests=[
            ("position", 5, TypeValidationError),
            ("blocks", {}, TypeValidationError),
            ("blocks", [8], TypeValidationError),
            ("blocks", [], RangeValidationError),
        ],
        validate_func=SRScript.validate,
        func_args=[[], config, info_api, validation_api, context],
    )


def test_srblock_validate(config, validation_api, context):
    block = ALL_SR_SCRIPTS[0].blocks[0]
    block.validate([], config, info_api, validation_api, context, expects_reporter=False)

    execute_attr_validation_tests(
        obj=block,
        attr_tests=[
            ("opcode", {}, TypeValidationError),
            ("opcode", "some_undefined_opcode", InvalidOpcodeError),
            ("inputs", {5:6}, TypeValidationError),
            ("dropdowns", [], TypeValidationError),
            ("comment", 89, TypeValidationError),
            ("mutation", "hi", TypeValidationError),
        ],
        validate_func=SRBlock.validate,
        func_args=[[], config, info_api, validation_api, context, False],
    )

def test_srblock_validate_reporter(config, validation_api, context):
    block = ALL_SR_SCRIPTS[1].blocks[0]
    block.validate([], config, info_api, validation_api, context, expects_reporter=True)

def test_srblock_validate_unexpected_mutation(config, validation_api, context):
    block = copy(ALL_SR_SCRIPTS[0].blocks[1])
    block.mutation = {...}
    with raises(TypeValidationError):
        block.validate([], config, info_api, validation_api, context, expects_reporter=False)

def test_srblock_validate_missing_mutation(config, validation_api, context):
    block = copy(ALL_SR_SCRIPTS[4].blocks[0])
    block.mutation = None
    with raises(TypeValidationError):
        block.validate([], config, info_api, validation_api, context, expects_reporter=False)

def test_srblock_validate_invalid_reporter_shape(config, validation_api, context):
    block = ALL_SR_SCRIPTS[0].blocks[0]
    with raises(InvalidBlockShapeError):
        block.validate([], config, info_api, validation_api, context, expects_reporter=True)

def test_srblock_validate_unexpected_input(config, validation_api, context):
    block = deepcopy(ALL_SR_SCRIPTS[6].blocks[0])
    block.inputs["SOME_ID"] = SRBlockOnlyInputValue(block=None)
    with raises(UnnecessaryInputError):
        block.validate([], config, info_api, validation_api, context, expects_reporter=False)

def test_srblock_validate_missing_input(config, validation_api, context):
    block = deepcopy(ALL_SR_SCRIPTS[6].blocks[0])
    del block.inputs["CONDITION"]
    with raises(MissingInputError):
        block.validate([], config, info_api, validation_api, context, expects_reporter=False) # 1


def test_srblock_validate_unexpected_dropdown(config, validation_api, context):
    block = deepcopy(ALL_SR_SCRIPTS[2].blocks[0])
    block.dropdowns["SOME_ID"] = SRDropdownValue(kind=DropdownValueKind.STANDARD, value="something")
    with raises(UnnecessaryDropdownError):
        block.validate([], config, info_api, validation_api, context, expects_reporter=True)

def test_srblock_validate_missing_dropdown(config, validation_api, context):
    block = deepcopy(ALL_SR_SCRIPTS[2].blocks[0])
    del block.dropdowns["VARIABLE"]
    with raises(MissingDropdownError):
        block.validate([], config, info_api, validation_api, context, expects_reporter=True)

