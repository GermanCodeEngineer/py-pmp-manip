from dataclasses import dataclass
from re          import split 

from pypenguin.utility import GreprClass, PypenguinEnum, SameNameTwiceError, ValidationConfig, FSCError
from pypenguin.utility import AA_TYPE, AA_TUPLE_OF_TYPES, AA_MIN_LEN

from pypenguin.opcode_info import InputType, OpcodeType

@dataclass(repr=False, frozen=True, unsafe_hash=True)
class SRCustomBlockOpcode(GreprClass):
    """
    The second representation for the "custom opcode" of a custom block. 
    It stores the segments, which can be either a string(=> a label) or a SRCustomBlockArgument with name and type
    """
    _grepr = True
    _grepr_fields = ["segments"]

    segments: tuple["str | SRCustomBlockArgument"]

    @classmethod
    def from_proccode_argument_names(cls, proccode: str, argument_names: list[str]) -> "SRCustomBlockOpcode":
        """
        Creates a custom block opcode given the procedure code and the argument names.
        
        Args:
            proccode: the procedure core
            argument_names: the names of the arguments
        
        Returns:
            the custom block opcode
        """
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
        """
        Fetches the argument ids and types.
        
        Returns:
            a dict mapping the argument ids to their types
        """
        return {
            segment.name: segment.type.get_corresponding_input_type() 
            for segment in self.segments if isinstance(segment, SRCustomBlockArgument)
        }
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensures the custom block opcode is valid, raise if not.
        
        Args:
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        """
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
    """
    The second representation for a argument of a custom opcode
    """
    _grepr = True
    _grepr_fields = ["name", "type"]

    name: str
    type: "SRCustomBlockArgumentType"

    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensures the custom block argument is valid, raise if not.
        
        Args:
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "type", SRCustomBlockArgumentType)

class SRCustomBlockArgumentType(PypenguinEnum):
    """
    The second representation for a argument type of a custom opcode argument
    """
    @classmethod
    def get_by_default(cls, default: str) -> "SRCustomBlockArgumentType":
        """
        Gets the argument type based on its default value.
        
        Args:
            default: the default value
        
        Returns:
            the argument type
        """
        match default:
            case "":
                return cls.STRING_NUMBER
            case "false":
                return cls.BOOLEAN
    
    def get_corresponding_input_type(self) -> InputType:
        """
        Gets the equivalent input type.
        
        Returns:
            the input type
        """
        match self:
            case SRCustomBlockArgumentType.STRING_NUMBER:
                return InputType.TEXT
            case SRCustomBlockArgumentType.BOOLEAN:
                return InputType.BOOLEAN

    STRING_NUMBER = 0
    BOOLEAN       = 1

class SRCustomBlockOptype(PypenguinEnum):
    """
    The second representation for the operation type of a custom block
    """
    @classmethod
    def from_code(cls, code: str | None) -> "SRCustomBlockOptype":
        """
        Gets the argument type based on its equivalent code.
        
        Args:
            code: the equivalent code
        
        Returns:
            the optype
        """
        if code == None:
            return cls.STATEMENT
        for value, optype_candidate in cls._value2member_map_.items():
            if value[1] == code:
                return optype_candidate
        raise FSCError(f"Couldn't find video state enum for video state code: {repr(code)}")

    def is_reporter(self) -> bool:
        """
        Returns wether the optype is a reporter optype
        
        Returns:
            wether the optype is a reporter optype
        """
        return self.value[0]

    def get_corresponding_opcode_type(self) -> OpcodeType:
        """
        Returns the corresponding opcode type
        
        Returns:
            the corresponding opcode type
        """
        return OpcodeType._member_map_[self.name]

    STATEMENT         = (False, "statement")
    ENDING_STATEMENT  = (False, "end"      )
    
    STRING_REPORTER   = (True , "string"   )
    NUMBER_REPORTER   = (True , "number"   )
    BOOLEAN_REPORTER  = (True , "boolean"  )
