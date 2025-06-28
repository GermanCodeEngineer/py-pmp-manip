from pytest import fixture, raises

from pypenguin.opcode_info.api import InputType, InputInfo, OpcodeType
from pypenguin.utility         import (
    ValidationConfig, 
    TypeValidationError, RangeValidationError, SameValueTwiceError, InvalidValueError, ConversionError,
)

from pypenguin.core.custom_block import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType, SRCustomBlockOptype,
)

from tests.utility import execute_attr_validation_tests


@fixture
def segments():
    return (
        "do sth with name",
        SRCustomBlockArgument(type=SRCustomBlockArgumentType.STRING_NUMBER, name="thing name"),
        "backwards?",
        SRCustomBlockArgument(type=SRCustomBlockArgumentType.BOOLEAN, name="do backwards?"),
        "times",
        SRCustomBlockArgument(type=SRCustomBlockArgumentType.STRING_NUMBER, name="repetitions"),
    )

@fixture
def config():
    return ValidationConfig()



def test_SRCustomBlockOpcode_from_proccode_argument_names(segments):
    custom_opcode = SRCustomBlockOpcode.from_proccode_argument_names(
        proccode="do sth with name %s backwards? %b times %s",
        argument_names=["thing name", "do backwards?", "repetitions"],
    )
    assert isinstance(custom_opcode, SRCustomBlockOpcode)
    assert custom_opcode.segments == segments


def test_SRCustomBlockOpcode_to_proccode_argument_names_defaults(segments):
    custom_opcode = SRCustomBlockOpcode(segments=segments)
    proccode, argument_names, argument_defaults = custom_opcode.to_proccode_argument_names_defaults()
    assert proccode == "do sth with name %s backwards? %b times %s"
    assert argument_names == ["thing name", "do backwards?", "repetitions"]
    assert argument_defaults == ["", "false", ""]


def test_SRCustomBlockOpcode_corresponding_input_info(segments):
    custom_opcode = SRCustomBlockOpcode(segments=segments)
    assert custom_opcode.corresponding_input_info == {
        "thing name": InputInfo(InputType.TEXT, menu=None),
        "do backwards?": InputInfo(InputType.BOOLEAN, menu=None),
        "repetitions": InputInfo(InputType.TEXT, menu=None),
    }

def test_SRCustomBlockOpcode_validate(config, segments):
    custom_opcode = SRCustomBlockOpcode(segments=segments)
    custom_opcode.validate([], config)
    # can't use execute_attr_validation_tests because frozen=True
    with raises(TypeValidationError): SRCustomBlockOpcode(segments=5).validate([], config)
    with raises(RangeValidationError): SRCustomBlockOpcode(segments=()).validate([], config)
    with raises(TypeValidationError): SRCustomBlockOpcode(segments=(-94,)).validate([], config)

def test_SRCustomBlockOpcode_validate_same_arg_name_twice(config):
    custom_opcode = SRCustomBlockOpcode(segments=(
        "...",
        SRCustomBlockArgument(type=SRCustomBlockArgumentType.STRING_NUMBER, name="the same arg name"),
        ",,,",
        SRCustomBlockArgument(type=SRCustomBlockArgumentType.BOOLEAN, name="the same arg name"),
        ";;;",
    ))
    with raises(SameValueTwiceError):
        custom_opcode.validate(path=[], config=config)



def test_SRCustomBlockArgument_validate(config):
    argument = SRCustomBlockArgument(name="some arg name", type=SRCustomBlockArgumentType.STRING_NUMBER)
    argument.validate(path=[], config=config)
    # can't use execute_attr_validation_tests because frozen=True
    with raises(TypeValidationError): SRCustomBlockArgument(name=[], type=argument.type).validate([], config)
    with raises(InvalidValueError): SRCustomBlockArgument(name="", type=argument.type).validate([], config)
    with raises(TypeValidationError): SRCustomBlockArgument(name=argument.name, type=True).validate([], config)



def test_SRCustomBlockArgumentType_corresponding_input_type():
    assert SRCustomBlockArgumentType.STRING_NUMBER.corresponding_input_type is InputType.TEXT
    assert SRCustomBlockArgumentType.STRING_NUMBER.corresponding_input_type is InputType.TEXT
    assert SRCustomBlockArgumentType.BOOLEAN.corresponding_input_type is InputType.BOOLEAN



def test_SRCustomBlockOptype_from_code():
    assert SRCustomBlockOptype.from_code(None       ) == SRCustomBlockOptype.STATEMENT
    assert SRCustomBlockOptype.from_code("statement") == SRCustomBlockOptype.STATEMENT
    assert SRCustomBlockOptype.from_code("end"      ) == SRCustomBlockOptype.ENDING_STATEMENT
    assert SRCustomBlockOptype.from_code("string"   ) == SRCustomBlockOptype.STRING_REPORTER
    assert SRCustomBlockOptype.from_code("number"   ) == SRCustomBlockOptype.NUMBER_REPORTER
    assert SRCustomBlockOptype.from_code("boolean"  ) == SRCustomBlockOptype.BOOLEAN_REPORTER
    with raises(ConversionError):
        SRCustomBlockOptype.from_code("something else")


def test_SRCustomBlockOptype_to_code():
    assert SRCustomBlockOptype.STATEMENT       .to_code() == "statement"
    assert SRCustomBlockOptype.ENDING_STATEMENT.to_code() == "end"
    assert SRCustomBlockOptype.STRING_REPORTER .to_code() == "string"
    assert SRCustomBlockOptype.NUMBER_REPORTER .to_code() == "number"
    assert SRCustomBlockOptype.BOOLEAN_REPORTER.to_code() == "boolean"


def test_SRCustomBlockOptype_is_reporter():
    assert not SRCustomBlockOptype.STATEMENT       .is_reporter()
    assert not SRCustomBlockOptype.ENDING_STATEMENT.is_reporter()
    assert     SRCustomBlockOptype.STRING_REPORTER .is_reporter()
    assert     SRCustomBlockOptype.NUMBER_REPORTER .is_reporter()
    assert     SRCustomBlockOptype.BOOLEAN_REPORTER.is_reporter()


def test_SRCustomBlockOptype_corresponding_opcode_type():
    assert SRCustomBlockOptype.STATEMENT       .corresponding_opcode_type is OpcodeType.STATEMENT       
    assert SRCustomBlockOptype.ENDING_STATEMENT.corresponding_opcode_type is OpcodeType.ENDING_STATEMENT
    assert SRCustomBlockOptype.STRING_REPORTER .corresponding_opcode_type is OpcodeType.STRING_REPORTER 
    assert SRCustomBlockOptype.NUMBER_REPORTER .corresponding_opcode_type is OpcodeType.NUMBER_REPORTER 
    assert SRCustomBlockOptype.BOOLEAN_REPORTER.corresponding_opcode_type is OpcodeType.BOOLEAN_REPORTER

