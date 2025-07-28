class PP_Error(Exception):
    pass


class PP_BlameDevsError(PP_Error): pass
class PP_PathError(PP_Error): pass

class PP_ThanksError(PP_Error):
    def __init__(self):
        super().__init__("Your project is unique! It could help me with my research! Please create an issue with your project attached! https://github.com/Fritzforcode/pypenguin/issues/new/")


###############################################################
#                ERRORS FOR THE OPCODE INFO API               #
###############################################################

class PP_OpcodeInfoError(PP_Error): pass
class PP_UnknownOpcodeError(PP_OpcodeInfoError): pass
class PP_SameOpcodeTwiceError(PP_OpcodeInfoError): pass

###############################################################
#                  ERRORS FOR DESERIALIZATION                 #
###############################################################

class PP_DeserializationError(PP_Error):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Issue during deserialization: {msg}")

###############################################################
#         ERRORS FOR CONVERSION BETWEEN REPRESENTATIONS       #
###############################################################

class PP_ConversionError(PP_Error): pass

###############################################################
#                    ERRORS FOR VALIDATION                    #
###############################################################

def _generate_path_string(path: list) -> str:
    path_string = ""
    for item in path:
        if   isinstance(item, str):
            path_string += "." + item
        elif isinstance(item, int):
            path_string += "[" + str(item) + "]"
        elif isinstance(item, tuple) and (len(item) == 1) and isinstance(item[0], str):
            path_string += "[" + repr(item[0]) + "]"
        else: raise ValueError()
    return path_string

class PP_ValidationError(PP_Error): pass

class PP_PathValidationError(PP_ValidationError):
    def __init__(self, path: list, msg: str, condition: str|None = None) -> None:
        self.path      = path
        self.msg       = msg
        self.condition = condition
        
        path_string = _generate_path_string(path)
        full_message = ""
        if path_string != "":
            full_message += f"At {path_string}: "
        if condition is not None:
            full_message += f"{condition}: "
        full_message += msg
        super().__init__(full_message)
    
class PP_TypeValidationError(PP_PathValidationError): pass
class PP_InvalidValueError(PP_PathValidationError): pass
class PP_RangeValidationError(PP_PathValidationError): pass

class PP_MissingInputError(PP_PathValidationError): pass
class PP_UnnecessaryInputError(PP_PathValidationError): pass
class PP_MissingDropdownError(PP_PathValidationError): pass
class PP_UnnecessaryDropdownError(PP_PathValidationError): pass

class PP_InvalidDropdownValueError(PP_PathValidationError): pass

class PP_InvalidOpcodeError(PP_PathValidationError): pass
class PP_InvalidBlockShapeError(PP_PathValidationError): pass

class PP_SpriteLayerStackError(PP_PathValidationError): pass

class PP_SameValueTwiceError(PP_ValidationError):
    def __init__(self, path1: list, path2: list, msg: str, condition: str|None = None) -> None:
        self.path1     = path1
        self.path2     = path2
        self.msg       = msg
        self.condition = condition
        
        path1_string = _generate_path_string(path1)
        path2_string = _generate_path_string(path2)
        full_message = f"At {path1_string} and {path2_string}: "
        if condition is not None:
            full_message += f"{condition}: "
        full_message += msg
        super().__init__(full_message)



###############################################################
#                 ERRORS FOR THE EXT INFO GEN                 #
###############################################################

# extractor.py
class PP_InvalidExtensionCodeSourceError(PP_Error): pass

class PP_FetchError(PP_Error): pass
class PP_NetworkFetchError(PP_FetchError): pass
class PP_UnexpectedFetchError(PP_FetchError): pass
class PP_FileFetchError(PP_FetchError): pass

class PP_FileNotFoundError(PP_Error): pass

class PP_JsNodeTreeToJsonConversionError(PP_Error): pass

class PP_BadOrInvalidExtensionCodeError(PP_Error): pass
class PP_InvalidExtensionCodeSyntaxError(PP_BadOrInvalidExtensionCodeError):
    def __init__(self, message: str, line: int | None = None, column: int | None = None):
        super().__init__(f"{message} at line {line}, column {column}")
        self.line = line
        self.column = column
class PP_BadExtensionCodeFormatError(PP_BadOrInvalidExtensionCodeError): pass
class PP_InvalidTranslationMessageError(PP_BadOrInvalidExtensionCodeError): pass

# generator.py

class PP_InvalidExtensionInformationError(PP_Error): pass
class PP_InvalidCustomMenuError(PP_InvalidExtensionInformationError): pass
class PP_InvalidCustomBlockError(PP_InvalidExtensionInformationError): pass
class PP_UnknownExtensionAttributeError(PP_InvalidExtensionInformationError): pass





###############################################################
#                      ERRORS FOR THE CONFIG                  #
###############################################################

class PP_ConfigurationError(PP_Error): pass


###############################################################
#                       ERRORS FOR UTILITY                    #
###############################################################

class PP_FailedFileWriteError(PP_Error): pass
class PP_FailedFileReadError(PP_Error): pass

###############################################################
#                     COPIED BUILT-IN ERRORS                  #
###############################################################

class PP_NotImplementedError(PP_Error): pass
class PP_TypeError(PP_Error): pass
class PP_ValueError(PP_Error): pass

###############################################################
#                         SPECIAL ERRORS                      #
###############################################################

class PP_UnsupportedOSError(PP_Error): pass
class PP_SetupRequiredError(PP_Error): pass
class PP_TempNotImplementedError(PP_Error):
    """Occurs on features that are not YET implemented"""


"""__all__ = [
    "PP_Error", "PP_BlameDevsError", "PP_ThanksError", 
    
    
    "PP_OpcodeInfoError", "PP_UnknownOpcodeError", "PP_SameOpcodeTwiceError", 
    
    
    "PP_DeserializationError", "PP_ConversionError",
    
    
    "PP_ValidationError", "PP_PathValidationError", "PP_TypeValidationError", "PP_InvalidValueError",
    "PP_RangeValidationError", "PP_MissingInputError", "PP_UnnecessaryInputError", 
    "PP_MissingDropdownError", "PP_UnnecessaryDropdownError", "PP_InvalidDropdownValueError", 
    "PP_InvalidOpcodeError", "PP_InvalidBlockShapeError", "PP_SpriteLayerStackError", 
    "PP_SameValueTwiceError",
    
    
    "PP_InvalidExtensionSourceError", 
    "PP_FetchError", "PP_NetworkFetchError", "PP_UnexpectedFetchError", "PP_FileFetchError",
    "PP_JsParsingError", 
    "PP_InvalidExtensionCodeError", "PP_EsprimaToJsonConversionError", 
    
    "PP_UnknownExtensionAttributeError",
    
    
    "PP_ConfigurationError", 
]""" # TODO: when done with error update: reintroduce maintanence

