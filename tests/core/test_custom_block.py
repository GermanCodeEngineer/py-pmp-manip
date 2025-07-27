from pytest import fixture, raises

from pypenguin.opcode_info.api import BuiltinInputType, InputInfo, OpcodeType
from pypenguin.utility         import (
    PP_TypeValidationError, PP_RangeValidationError, PP_SameValueTwiceError, PP_InvalidValueError, PP_ConversionError,
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
        "thing name": InputInfo(BuiltinInputType.TEXT, menu=None),
        "do backwards?": InputInfo(BuiltinInputType.BOOLEAN, menu=None),
        "repetitions": InputInfo(BuiltinInputType.TEXT, menu=None),
    }

def test_SRCustomBlockOpcode_validate(segments):
    custom_opcode = SRCustomBlockOpcode(segments=segments)
    custom_opcode.validate([])
    # can't use execute_attr_validation_tests because frozen=True
    with raises(PP_TypeValidationError): SRCustomBlockOpcode(segments=5).validate([])
    with raises(PP_RangeValidationError): SRCustomBlockOpcode(segments=()).validate([])
    with raises(PP_TypeValidationError): SRCustomBlockOpcode(segments=(-94,)).validate([])

def test_SRCustomBlockOpcode_validate_same_arg_name_twice():
    custom_opcode = SRCustomBlockOpcode(segments=(
        "...",
        SRCustomBlockArgument(type=SRCustomBlockArgumentType.STRING_NUMBER, name="the same arg name"),
        ",,,",
        SRCustomBlockArgument(type=SRCustomBlockArgumentType.BOOLEAN, name="the same arg name"),
        ";;;",
    ))
    with raises(PP_SameValueTwiceError):
        custom_opcode.validate(path=[])



def test_SRCustomBlockArgument_validate():
    argument = SRCustomBlockArgument(name="some arg name", type=SRCustomBlockArgumentType.STRING_NUMBER)
    argument.validate(path=[])
    # can't use execute_attr_validation_tests because frozen=True
    with raises(PP_TypeValidationError): SRCustomBlockArgument(name=[], type=argument.type).validate([])
    with raises(PP_InvalidValueError): SRCustomBlockArgument(name="", type=argument.type).validate([])
    with raises(PP_TypeValidationError): SRCustomBlockArgument(name=argument.name, type=True).validate([])



def test_SRCustomBlockArgumentType_corresponding_input_type():
    assert SRCustomBlockArgumentType.STRING_NUMBER.corresponding_input_type is BuiltinInputType.TEXT
    assert SRCustomBlockArgumentType.STRING_NUMBER.corresponding_input_type is BuiltinInputType.TEXT
    assert SRCustomBlockArgumentType.BOOLEAN.corresponding_input_type is BuiltinInputType.BOOLEAN



def test_SRCustomBlockOptype_from_code():
    assert SRCustomBlockOptype.from_code(None       ) == SRCustomBlockOptype.STATEMENT
    assert SRCustomBlockOptype.from_code("statement") == SRCustomBlockOptype.STATEMENT
    assert SRCustomBlockOptype.from_code("end"      ) == SRCustomBlockOptype.ENDING_STATEMENT
    assert SRCustomBlockOptype.from_code("string"   ) == SRCustomBlockOptype.STRING_REPORTER
    assert SRCustomBlockOptype.from_code("number"   ) == SRCustomBlockOptype.NUMBER_REPORTER
    assert SRCustomBlockOptype.from_code("boolean"  ) == SRCustomBlockOptype.BOOLEAN_REPORTER
    with raises(PP_ConversionError):
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

