from dataclasses import dataclass
from re          import split 

from utility import GreprClass, PypenguinEnum, SameNameTwiceError, ValidationConfig
from utility import AA_TYPE, AA_TUPLE_OF_TYPES, AA_MIN_LEN, AA_NOT_ONE_OF

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
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        AA_TUPLE_OF_TYPES(self, path, "segments", (str, SRCustomBlockArgument))
        AA_MIN_LEN(self, path, "segments", min_len=1)

        names = {}
        for i, segment in enumerate(self.segments):
            current_path = ["segments", i]
            if isinstance(segment, SRCustomBlockArgument):
                segment.validate(current_path, config)
                if segment.name in names:
                    other_path = names[segment.name]
                    raise SameNameTwiceError(other_path, current_path, f"Two arguments of a {self.__class__.__name__} mustn't have the same name")
                names[segment.name] = current_path

@dataclass(repr=False, frozen=True)
class SRCustomBlockArgument(GreprClass):
    _grepr = True
    _grepr_fields = ["type", "name"]

    type: "SRCustomBlockArgumentType"
    name: str

    def validate(self, path: list, config: ValidationConfig) -> None:
        AA_TYPE(self, path, "type", SRCustomBlockArgumentType)
        AA_TYPE(self, path, "name", str)

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
                return InputType.BOOLEAN
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

    def is_reporter(self) -> bool:
        return self.value[0]

    def get_corresponding_opcode_type(self) -> OpcodeType:
        return OpcodeType._member_map_[self.name]

    STATEMENT         = (False, 0)
    ENDING_STATEMENT  = (False, 1)
    
    STRING_REPORTER   = (True , 2)
    NUMBER_REPORTER   = (True , 3)
    BOOLEAN_REPORTER  = (True , 4)
