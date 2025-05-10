from pytest import fixture

from pypenguin.opcode_info import InputType

from pypenguin.core.custom_block import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType, SRCustomBlockOptype,
)

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



def test_srcustomblockopcode_from_proccode_argument_names(segments):
    custom_opcode = SRCustomBlockOpcode.from_proccode_argument_names(
        proccode="do sth with name %s backwards? %b times %n",
        argument_names=["thing name", "do backwards?", "repetitions"],
    )
    assert isinstance(custom_opcode, SRCustomBlockOpcode)
    assert custom_opcode.segments == segments

def test_srcustomblock_opcode_get_corresponding_input_types(segments):
    custom_opcode = SRCustomBlockOpcode(segments=segments)
    assert custom_opcode.get_corresponding_input_types() == {
        "thing name": InputType.TEXT,
        "do backwards?": InputType.BOOLEAN,
        "repetitions": InputType.TEXT,
    }

