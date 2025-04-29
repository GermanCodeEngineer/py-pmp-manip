from dataclasses import dataclass
from re          import split 

from utility import GreprClass, PypenguinEnum

from opcode_info import InputType, OpcodeType

@dataclass(repr=False, frozen=True, unsafe_hash=True)
class SRCustomBlockOpcode(GreprClass):
    _grepr = True
    _grepr_fields = ["segments"]

    segments: tuple["str | SRCustomBlockArgument"]

    @classmethod
    def from_proccode_names_defaults(cls, proccode: str, argument_names: list[str], argument_defaults: list[str]) -> "SRCustomBlockOpcode":
        parts = split(r'(%s|%n|%b)', proccode)
        segments = []
        i = 0
        while i < len(parts):
            text_piece = parts[i].strip()
            splitter = parts[i + 1] if (i + 1) < len(parts) else None
            if text_piece != "":
                segments.append(text_piece)
            if splitter is not None: 
                segments.append(SRCustomBlockArgument(
                    type = SRCustomBlockArgumentType.BOOLEAN if splitter == "%b" else SRCustomBlockArgumentType.STRING_NUMBER,
                    name = argument_names[i//2],
                ))
            i += 2
        return cls(segments=tuple(segments))
    
    def get_corresponding_input_types(self) -> dict[str, InputType]:
        input_types = {}
        for segment in self.segments:
            if isinstance(segment, SRCustomBlockArgument):
                input_types[segment.name] = segment.type.get_corresponding_input_type()
        return input_types

@dataclass(repr=False, frozen=True)
class SRCustomBlockArgument(GreprClass):
    _grepr = True
    _grepr_fields = ["type", "name"]

    type: "SRCustomBlockArgumentType"
    name: str

class SRCustomBlockArgumentType(PypenguinEnum):
    @staticmethod
    def get_by_default(default) -> "SRCustomBlockArgumentType":
        match default:
            case "":
                return SRCustomBlockArgumentType.STRING_NUMBER
            case "false":
                return SRCustomBlockArgumentType.BOOLEAN
            case _:
                raise ValueError()
    
    def get_corresponding_input_type(self) -> InputType:
        match self:
            case SRCustomBlockArgumentType.STRING_NUMBER:
                return InputType.TEXT
            case SRCustomBlockArgumentType.BOOLEAN:
                return InputType.BOOLEAN,
            case _:
                raise ValueError()

    STRING_NUMBER = 0
    BOOLEAN       = 1

class SRCustomBlockOptype(PypenguinEnum):
    @staticmethod
    def from_string(string: str | None) -> "SRCustomBlockOptype":
        match string:
            case None       : return SRCustomBlockOptype.STATEMENT
            case "statement": return SRCustomBlockOptype.STATEMENT
            case "end"      : return SRCustomBlockOptype.ENDING_STATEMENT
            case "string"   : return SRCustomBlockOptype.STRING_REPORTER
            case "number"   : return SRCustomBlockOptype.NUMBER_REPORTER
            case "boolean"  : return SRCustomBlockOptype.BOOLEAN_REPORTER
            case _: raise ValueError()

    @property # TODO: check wether used correctly
    def is_reporter(self) -> bool:
        match self:
            case SRCustomBlockOptype.STATEMENT | SRCustomBlockOptype.ENDING_STATEMENT:
                return False
            case (SRCustomBlockOptype.STRING_REPORTER 
                | SRCustomBlockOptype.NUMBER_REPORTER
                | SRCustomBlockOptype.BOOLEAN_REPORTER):
                return True
            case _: raise ValueError()

    def get_corresponding_opcode_type(self) -> OpcodeType:
        return OpcodeType._member_map_[self.name]

    STATEMENT         = 0
    ENDING_STATEMENT  = 1
    
    STRING_REPORTER   = 2
    NUMBER_REPORTER   = 3
    BOOLEAN_REPORTER  = 4
