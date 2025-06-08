from re import split 

from pypenguin.opcode_info.api import InputType, InputInfo, OpcodeType
from pypenguin.utility         import (
    grepr_dataclass, PypenguinEnum, ValidationConfig,
    AA_TYPE, AA_TUPLE_OF_TYPES, AA_MIN_LEN,
    SameValueTwiceError, ConversionError,
)

@grepr_dataclass(grepr_fields=["segments"], frozen=True, unsafe_hash=True)
class SRCustomBlockOpcode:
    """
    The second representation for the "custom opcode" of a custom block. 
    It stores the segments, which can be either a string(=> a label) or a SRCustomBlockArgument with name and type
    """

    segments: tuple["str | SRCustomBlockArgument"]

    @classmethod
    def from_proccode_argument_names(cls, proccode: str, argument_names: list[str]) -> "SRCustomBlockOpcode":
        """
        Creates a custom block opcode given the procedure code and the argument names
        
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
    
    def get_corresponding_input_info(self) -> dict[str, InputInfo]:
        """
        Fetches the argument ids and information
        
        Returns:
            a dict mapping the argument ids to their information
        """
        return {
            segment.name: InputInfo(
                type = segment.type.get_corresponding_input_type(),
                menu = None,
            ) 
            for segment in self.segments if isinstance(segment, SRCustomBlockArgument)
        }
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensures the custom block opcode is valid, raise if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRCustomBlockOpcode is invalid
            SameValueTwiceError(ValidationError): if two arguments have the same name
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
                    raise SameValueTwiceError(other_path, current_path, 
                        f"Two arguments of a {self.__class__.__name__} mustn't have the same name",
                    )
                names[segment.name] = current_path

    def _copymodify_(self, attr: str, value) -> "SRCustomBlockOpcode":
        """
        *[Internal Method]* Creates a copy with one attribute set to a new value

        Args:
            attr: the attribute to set in the copy
            value: the value to set the attribute to
        
        Returns:
            the modified copy
        """
        assert attr == "segments"
        return SRCustomBlockOpcode(segments=value)

@grepr_dataclass(grepr_fields=["name", "type"], frozen=True, unsafe_hash=True)
class SRCustomBlockArgument:
    """
    The second representation for a argument of a custom opcode
    """
    
    name: str
    type: "SRCustomBlockArgumentType"

    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensures the custom block argument is valid, raise if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRCustomBlockArgument is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "type", SRCustomBlockArgumentType)
    
    def _copymodify_(self, attr: str, value) -> "SRCustomBlockArgument":
        """
        *[Internal Method]* Creates a copy with one attribute set to a new value

        Args:
            attr: the attribute to set in the copy
            value: the value to set the attribute to
        
        Returns:
            the modified copy
        """
        assert attr in {"name", "type"}
        if   attr == "name": return SRCustomBlockArgument(name=value, type=self.type)
        elif attr == "type": return SRCustomBlockArgument(name=self.name, type=value)

class SRCustomBlockArgumentType(PypenguinEnum):
    """
    The second representation for a argument type of a custom opcode argument
    """        
    
    def get_corresponding_input_type(self) -> InputType:
        """
        Gets the equivalent input type
        
        Returns:
            the input type
        """
        return self.value[0]

    STRING_NUMBER = (InputType.TEXT   , 0)
    BOOLEAN       = (InputType.BOOLEAN, 1)

class SRCustomBlockOptype(PypenguinEnum):
    """
    The second representation for the operation type of a custom block
    """
    @classmethod
    def from_code(cls, code: str | None) -> "SRCustomBlockOptype":
        """
        Gets the argument type based on its equivalent code
        
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
        raise ConversionError(f"Couldn't find video state enum for video state code: {repr(code)}")

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

    STATEMENT        = (False, "statement")
    ENDING_STATEMENT = (False, "end"      )
    
    STRING_REPORTER  = (True , "string"   )
    NUMBER_REPORTER  = (True , "number"   )
    BOOLEAN_REPORTER = (True , "boolean"  )


__all__ = [
    "SRCustomBlockOpcode", "SRCustomBlockArgument", "SRCustomBlockArgumentType", "SRCustomBlockOptype",
]

