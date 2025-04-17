from enum import Enum
from utility import PypenguinClass

class SRCustomOpcode(PypenguinClass):
    _grepr = True
    _grepr_fields = ["proccode", "arguments"]

    proccode: str
    arguments: dict[str, "SRCustomArgumentType"]

    def __init__(self, proccode: str, argument_names: list[str], argument_defaults: list[str]):
        self.proccode = proccode
        self.arguments = {
            name: SRCustomArgumentType.get_by_default(default)
            for name, default in zip(argument_names, argument_defaults)
        }
        

class SRCustomArgumentType(Enum):
    STRING_NUMBER = 0
    BOOLEAN       = 1

    def __repr__(self) -> str:
        return self.__class__.__name__ + "." + self.name
     
    @staticmethod
    def get_by_default(default) -> "SRCustomArgumentType":
        match default:
            case "":
                return SRCustomArgumentType.STRING_NUMBER
            case "false":
                return SRCustomArgumentType.BOOLEAN
            case _:
                raise ValueError()

class SRCustomBlockOptype(Enum):
    STATEMENT         = 0
    ENDING_STATEMENT  = 1
    
    STRING_REPORTER   = 2
    NUMBER_REPORTER   = 3
    BOOLEAN_REPORTER  = 4
    
    def __repr__(self) -> str:
        return self.__class__.__name__ + "." + self.name

    @staticmethod
    def from_string(string) -> "SRCustomBlockOptype":
        match string:
            case None       : return SRCustomBlockOptype.STATEMENT
            case "statement": return SRCustomBlockOptype.STATEMENT
            case "end"      : return SRCustomBlockOptype.ENDING_STATEMENT
            case "string"   : return SRCustomBlockOptype.STRING_REPORTER
            case "number"   : return SRCustomBlockOptype.NUMBER_REPORTER
            case "boolean"  : return SRCustomBlockOptype.BOOLEAN_REPORTER
            case _: raise ValueError()
