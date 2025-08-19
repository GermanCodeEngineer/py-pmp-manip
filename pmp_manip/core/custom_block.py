from re import split 

from pmp_manip.opcode_info.api import InputType, BuiltinInputType, InputInfo, OpcodeType
from pmp_manip.utility         import (
    grepr_dataclass, GEnum,
    AA_TYPE, AA_TUPLE_OF_TYPES, AA_MIN_LEN, AA_NOT_EQUAL,
    MANIP_SameValueTwiceError, MANIP_ConversionError,
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
            proccode: the procedure code
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
                match splitter:
                    case "%s":
                        argument_type = SRCustomBlockArgumentType.STRING_NUMBER
                    case "%b":
                        argument_type = SRCustomBlockArgumentType.BOOLEAN
                segments.append(SRCustomBlockArgument(
                    name=argument_names[i//2], 
                    type=argument_type,
                ))
            i += 2
        return cls(segments=tuple(segments))
    
    def to_proccode_argument_names_defaults(self) -> tuple[str, list[str], list[str]]:
        """
        Generates procedure code, argument names and defaults from a SRCustomBlockOpcode
        
        Returns:
            the procedure code, list of argument names and list of argument defaults
        """
        parts             = []
        argument_names    = []
        argument_defaults = []
        for segment in self.segments:
            if   isinstance(segment, str):
                parts.append(segment)
            elif isinstance(segment, SRCustomBlockArgument):
                if segment.type is SRCustomBlockArgumentType.BOOLEAN:
                    parts.append("%b")
                    argument_defaults.append("false")
                else:
                    parts.append("%s")
                    argument_defaults.append("")
                argument_names.append(segment.name)
        return (" ".join(parts), argument_names, argument_defaults)
    
    @property
    def corresponding_input_info(self) -> dict[str, InputInfo]:
        """
        Fetches the argument ids and information
        
        Returns:
            a dict mapping the argument ids to their information
        """
        return {
            segment.name: InputInfo(
                type = segment.type.corresponding_input_type,
                menu = None,
            ) 
            for segment in self.segments if isinstance(segment, SRCustomBlockArgument)
        }
    
    def validate(self, path: list) -> None:
        """
        Ensures the custom block opcode is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRCustomBlockOpcode is invalid
            MANIP_SameValueTwiceError(MANIP_ValidationError): if two arguments have the same name
        """
        AA_TUPLE_OF_TYPES(self, path, "segments", (str, SRCustomBlockArgument))
        AA_MIN_LEN(self, path, "segments", min_len=1)

        names = {}
        last_was_label = False
        for i, segment in enumerate(self.segments):
            current_path = ["segments", i]
            if isinstance(segment, SRCustomBlockArgument):
                segment.validate(current_path)
                if segment.name in names:
                    other_path = names[segment.name]
                    raise MANIP_SameValueTwiceError(other_path, current_path, 
                        f"Two arguments of a {self.__class__.__name__} must not have the same name",
                    )
                names[segment.name] = current_path
                last_was_label = False
            else:
                if last_was_label:
                    raise MANIP_TypeValidationError(path, f"A custom block opcode must not contain two labels in a row")
                last_was_label = True
                

@grepr_dataclass(grepr_fields=["name", "type"], frozen=True, unsafe_hash=True)
class SRCustomBlockArgument:
    """
    The second representation for a argument of a custom opcode
    """
    
    name: str
    type: "SRCustomBlockArgumentType"

    def validate(self, path: list) -> None:
        """
        Ensures the custom block argument is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRCustomBlockArgument is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_NOT_EQUAL(self, path, "name", value="")
        AA_TYPE(self, path, "type", SRCustomBlockArgumentType)

class SRCustomBlockArgumentType(GEnum):
    """
    The second representation for a argument type of a custom opcode argument
    """        
    
    @property
    def corresponding_input_type(self) -> InputType:
        """
        Gets the equivalent input type
        
        Returns:
            the input type
        """
        return self.value[0]

    STRING_NUMBER = (BuiltinInputType.TEXT   , 0)
    BOOLEAN       = (BuiltinInputType.BOOLEAN, 1)

class SRCustomBlockOptype(GEnum):
    """
    The second representation for the operation type of a custom block
    """
    
    @classmethod
    def from_code(cls, code: str | None) -> "SRCustomBlockOptype":
        """
        Gets the SRCustomBlockOptype based on its equivalent code
        
        Args:
            code: the equivalent code
        
        Returns:
            the SRCustomBlockOptype
        """
        if code == None:
            return cls.STATEMENT
        for value, optype_candidate in cls._value2member_map_.items():
            if value[1] == code:
                return optype_candidate
        raise MANIP_ConversionError(f"Could not find video state enum for video state code: {code}")

    def to_code(self) -> str:
        """
        Gets the optype code based on its equivalent SRCustomBlockOptype
        
        Returns:
            the optype code
        """
        return self.value[1]

    def is_reporter(self) -> bool:
        """
        Returns wether the optype is a reporter optype
        
        Returns:
            wether the optype is a reporter optype
        """
        return self.value[0]

    @property
    def corresponding_opcode_type(self) -> OpcodeType:
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

