from utility import PypenguinClass, PypenguinEnum

class SRCustomBlockOpcode(PypenguinClass):
    _grepr = True
    _grepr_fields = ["proccode", "arguments"]

    proccode: str
    arguments: dict[str, "SRCustomBlockArgumentType"]

    def __init__(self, proccode: str, argument_names: list[str], argument_defaults: list[str]):
        self.proccode = proccode
        self.arguments = {
            name: SRCustomBlockArgumentType.get_by_default(default)
            for name, default in zip(argument_names, argument_defaults)
        }

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

    @property
    def is_reporter(self):
        match self:
            case SRCustomBlockOptype.STATEMENT | SRCustomBlockOptype.ENDING_STATEMENT:
                return False
            case (SRCustomBlockOptype.STRING_REPORTER 
                | SRCustomBlockOptype.NUMBER_REPORTER
                | SRCustomBlockOptype.BOOLEAN_REPORTER):
                return True
            case _: raise ValueError()

    STATEMENT         = 0
    ENDING_STATEMENT  = 1
    
    STRING_REPORTER   = 2
    NUMBER_REPORTER   = 3
    BOOLEAN_REPORTER  = 4
