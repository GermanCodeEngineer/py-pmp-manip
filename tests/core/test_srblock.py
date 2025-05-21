from pytest import fixture, raises
from copy   import copy, deepcopy

from pypenguin.utility            import (
    ValidationConfig, 
    TypeValidationError, RangeValidationError, InvalidOpcodeError, InvalidBlockShapeError,
    UnnecessaryInputError, MissingInputError, UnnecessaryDropdownError, MissingDropdownError,
)
from pypenguin.opcode_info.groups import info_api
from pypenguin.opcode_info        import DropdownValueKind, OpcodeType, InputType

from pypenguin.core.block     import (
    SRScript, SRBlock, SRInputValue, 
    SRBlockAndTextInputValue, SRBlockOnlyInputValue, SRBlockAndDropdownInputValue, SRScriptInputValue,
)
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
        scope_variables=[(DropdownValueKind.VARIABLE, "my variable")],
        scope_lists=[(DropdownValueKind.LIST, "my list")],

        all_sprite_variables=[(DropdownValueKind.VARIABLE, "my variable")],

        sprite_only_variables=[],
        sprite_only_lists=[],

        other_sprites=[],
        backdrops=[],
        costumes=[],
        sounds=[],

        is_stage=False,
    )



def test_SRScript_validate(config, validation_api, context):        
    srscript = ALL_SR_SCRIPTS[0]
    srscript.validate(
        path=[],
        config=config,
        info_api=info_api,
        validation_api=validation_api,
        context=context,
    )

    execute_attr_validation_tests(
        obj=srscript,
        attr_tests=[
            ("position", 5, TypeValidationError),
            ("blocks", {}, TypeValidationError),
            ("blocks", [8], TypeValidationError),
            ("blocks", [], RangeValidationError),
        ],
        validate_func=SRScript.validate,
        func_args=[[], config, info_api, validation_api, context],
    )



def test_SRBlock_validate(config, validation_api, context):
    srblock = ALL_SR_SCRIPTS[0].blocks[0]
    srblock.validate([], config, info_api, validation_api, context, expects_reporter=False)

    execute_attr_validation_tests(
        obj=srblock,
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

def test_SRBlock_validate_reporter(config, validation_api, context):
    srblock = ALL_SR_SCRIPTS[1].blocks[0]
    srblock.validate([], config, info_api, validation_api, context, expects_reporter=True)

def test_SRBlock_validate_cb_def(config, validation_api, context):
    srblock = ALL_SR_SCRIPTS[4].blocks[0]
    srblock.validate([], config, info_api, validation_api, context, expects_reporter=False)    

def test_SRBlock_validate_unexpected_mutation(config, validation_api, context):
    srblock = copy(ALL_SR_SCRIPTS[0].blocks[1])
    srblock.mutation = {...}
    with raises(TypeValidationError):
        srblock.validate([], config, info_api, validation_api, context, expects_reporter=False)

def test_SRBlock_validate_missing_mutation(config, validation_api, context):
    srblock = copy(ALL_SR_SCRIPTS[4].blocks[0])
    srblock.mutation = None
    with raises(TypeValidationError):
        srblock.validate([], config, info_api, validation_api, context, expects_reporter=False)

def test_SRBlock_validate_invalid_reporter_shape(config, validation_api, context):
    srblock = ALL_SR_SCRIPTS[0].blocks[0]
    with raises(InvalidBlockShapeError):
        srblock.validate([], config, info_api, validation_api, context, expects_reporter=True)

def test_SRBlock_validate_unexpected_input(config, validation_api, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[6].blocks[0])
    srblock.inputs["SOME_ID"] = SRBlockOnlyInputValue(block=None)
    with raises(UnnecessaryInputError):
        srblock.validate([], config, info_api, validation_api, context, expects_reporter=False)

def test_SRBlock_validate_missing_input(config, validation_api, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[6].blocks[0])
    del srblock.inputs["CONDITION"]
    with raises(MissingInputError):
        srblock.validate([], config, info_api, validation_api, context, expects_reporter=False) # 1

def test_SRBlock_validate_unexpected_dropdown(config, validation_api, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[2].blocks[0])
    srblock.dropdowns["SOME_ID"] = SRDropdownValue(kind=DropdownValueKind.STANDARD, value="something")
    with raises(UnnecessaryDropdownError):
        srblock.validate([], config, info_api, validation_api, context, expects_reporter=True)

def test_SRBlock_validate_missing_dropdown(config, validation_api, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[2].blocks[0])
    del srblock.dropdowns["VARIABLE"]
    with raises(MissingDropdownError):
        srblock.validate([], config, info_api, validation_api, context, expects_reporter=True)


def test_SRBlock_validate_opcode_type():
    reporter_tests = [
        (True , 0b000), (True , 0b001), (True , 0b010), (True , 0b011),
        (True , 0b100), (True , 0b101), (True , 0b110), (False, 0b111),
    ]
    sub_tests = [ # should_raise, (is_top_level, is_first, is_last)
        (OpcodeType.STATEMENT       , [
            (False, 0b000), (False, 0b001), (False, 0b010), (False, 0b011),
            (False, 0b100), (False, 0b101), (False, 0b110), (False, 0b111),
        ]),
        (OpcodeType.ENDING_STATEMENT, [
            (True , 0b000), (False, 0b001), (True , 0b010), (False, 0b011),
            (True , 0b100), (False, 0b101), (True , 0b110), (False, 0b111),
        ]),
        (OpcodeType.HAT             , [
            (True , 0b000), (True , 0b001), (True , 0b010), (True , 0b011),
            (True , 0b100), (True , 0b101), (False, 0b110), (False, 0b111),
        ]),
        (OpcodeType.STRING_REPORTER , reporter_tests),
        (OpcodeType.NUMBER_REPORTER , reporter_tests),
        (OpcodeType.BOOLEAN_REPORTER, reporter_tests),
    ]
    for opcode_type, items in sub_tests:
        for should_raise, flags in items:
            is_top_level = bool((flags        )//0b100)
            is_first     = bool((flags % 0b100)//0b010)
            is_last      = bool((flags % 0b010)//0b001)
            if should_raise:
                with raises(InvalidBlockShapeError):
                    SRBlock.validate_opcode_type(
                        path         = [],
                        config       = config,
                        opcode_type  = opcode_type,
                        is_top_level = is_top_level,
                        is_first     = is_first,
                        is_last      = is_last,
                    )
            else:
                SRBlock.validate_opcode_type(
                    path         = [],
                    config       = config,
                    opcode_type  = opcode_type,
                    is_top_level = is_top_level,
                    is_first     = is_first,
                    is_last      = is_last,
                )



def test_SRInputValue_init():
    class DummyInputValue(SRInputValue):
        # fullfill abstract method requirement
        def validate(self, *args, **kwargs): 
            pass
    with raises(NotImplementedError):
        DummyInputValue()

def test_SRInputValue_eq():
    sub_tests = [
           (False, 
            SRBlockAndTextInputValue(block=None, text="a text field"), 
            SRBlockOnlyInputValue(block=None),
        ), (False, 
            SRBlockAndTextInputValue(block=None, text="a text field"), 
            SRBlockAndTextInputValue(block=None, text="another text"), 
        ), (False, 
            SRBlockAndTextInputValue(block=5   , text="a text field"), 
            SRBlockAndTextInputValue(block=None, text="a text field"), 
        ), (True, 
            SRBlockAndTextInputValue(block=45, text="a text field"), 
            SRBlockAndTextInputValue(block=45, text="a text field"), 
        )
    ]
    for target_result, a, b in sub_tests:
        assert (a == b) == target_result
    
    a = SRBlockAndTextInputValue(block=None, text="a text field")
    b = SRBlockOnlyInputValue(block=None)
    

def test_SRInputValue_validate_block(config, validation_api, context):
    input_value = SRBlockAndDropdownInputValue(
        block=ALL_SR_SCRIPTS[5].blocks[0],
        dropdown=SRDropdownValue(kind=DropdownValueKind.BROADCAST_MSG, value="my message"),
    )
    input_value._validate_block([], config, info_api, validation_api, context)


def test_SRBlockAndTextInputValue_validate(config, validation_api, context):
    input_type = InputType.TEXT
    input_value = SRBlockAndTextInputValue(
        block=ALL_SR_SCRIPTS[1].blocks[0],
        text="some random text",
    )
    input_value.validate([], config, info_api, validation_api, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("block", 5, TypeValidationError),
            ("text", {}, TypeValidationError),
        ],
        validate_func=SRBlockAndTextInputValue.validate,
        func_args=[[], config, info_api, validation_api, context, input_type],
    )

def test_SRBlockAndDropdownInputValue_validate(config, validation_api, context):
    input_type = InputType.MOUSE_OR_OTHER_SPRITE
    input_value = SRBlockAndDropdownInputValue(
        block=ALL_SR_SCRIPTS[5].blocks[0],
        dropdown=SRDropdownValue(kind=DropdownValueKind.OBJECT, value="mouse-pointer"),
    )
    input_value.validate([], config, info_api, validation_api, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("block", 5, TypeValidationError),
            ("dropdown", {}, TypeValidationError),
        ],
        validate_func=SRBlockAndDropdownInputValue.validate,
        func_args=[[], config, info_api, validation_api, context, input_type],
    )

def test_SRBlockOnlyInputValue_validate(config, validation_api, context):
    input_type = InputType.BOOLEAN
    input_value = SRBlockOnlyInputValue(
        block=None,
    )
    input_value.validate([], config, info_api, validation_api, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("block", 5, TypeValidationError),
        ],
        validate_func=SRBlockOnlyInputValue.validate,
        func_args=[[], config, info_api, validation_api, context, input_type],
    )

def test_SRScriptInputValue_validate(config, validation_api, context):
    input_type = InputType.SCRIPT
    input_value = SRScriptInputValue(
        blocks=ALL_SR_SCRIPTS[0].blocks,
    )
    input_value.validate([], config, info_api, validation_api, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("blocks", 9, TypeValidationError),
            ("blocks", [{}], TypeValidationError),
        ],
        validate_func=SRScriptInputValue.validate,
        func_args=[[], config, info_api, validation_api, context, input_type],
    )

