class MANIP_Error(Exception):
    pass


class MANIP_BlameDevsError(MANIP_Error): pass
class MANIP_PathError(MANIP_Error): pass

class MANIP_ThanksError(MANIP_Error):
    def __init__(self):
        super().__init__("Your project is unique! It could help me with my research! Please create an issue with your project attached! https://github.com/GermanCodeEngineer/py-pmp-manip/issues/new/")


###############################################################
#                ERRORS FOR THE OPCODE INFO API               #
###############################################################

class MANIP_OpcodeInfoError(MANIP_Error): pass
class MANIP_UnknownOpcodeError(MANIP_OpcodeInfoError): pass
class MANIP_SameOpcodeTwiceError(MANIP_OpcodeInfoError): pass

class MANIP_ExtensionModuleNotFoundError(MANIP_Error): pass
class MANIP_UnexpectedExtensionModuleImportError(MANIP_Error): pass
class MANIP_UnknownBuiltinExtensionError(MANIP_Error): pass

###############################################################
#                  ERRORS FOR DESERIALIZATION                 #
###############################################################

class MANIP_DeserializationError(MANIP_Error):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Issue during deserialization: {msg}")

###############################################################
#         ERRORS FOR CONVERSION BETWEEN REPRESENTATIONS       #
###############################################################

class MANIP_ConversionError(MANIP_Error): pass

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

class MANIP_ValidationError(MANIP_Error): pass

class MANIP_PathValidationError(MANIP_ValidationError):
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
    
class MANIP_TypeValidationError(MANIP_PathValidationError): pass
class MANIP_InvalidValueError(MANIP_PathValidationError): pass
class MANIP_RangeValidationError(MANIP_PathValidationError): pass

class MANIP_MissingInputError(MANIP_PathValidationError): pass
class MANIP_UnnecessaryInputError(MANIP_PathValidationError): pass
class MANIP_MissingDropdownError(MANIP_PathValidationError): pass
class MANIP_UnnecessaryDropdownError(MANIP_PathValidationError): pass

class MANIP_InvalidDropdownValueError(MANIP_PathValidationError): pass

class MANIP_InvalidOpcodeError(MANIP_PathValidationError): pass
class MANIP_InvalidBlockShapeError(MANIP_PathValidationError): pass
class MANIP_InvalidDirPathError(MANIP_PathValidationError): pass

class MANIP_SpriteLayerStackError(MANIP_PathValidationError): pass

class MANIP_SameValueTwiceError(MANIP_ValidationError):
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

# fetch_js.py
class MANIP_InvalidExtensionCodeSourceError(MANIP_Error): pass

class MANIP_FetchError(MANIP_Error): pass
class MANIP_NetworkFetchError(MANIP_FetchError): pass
class MANIP_UnexpectedFetchError(MANIP_FetchError): pass
class MANIP_FileFetchError(MANIP_FetchError): pass

# direct_extractor.py / safe_extractor.py
class MANIP_NoNodeJSInstalledError(MANIP_Error): pass

class MANIP_ExtensionExecutionError(MANIP_Error): pass
class MANIP_ExtensionExecutionTimeoutError(MANIP_ExtensionExecutionError): pass
class MANIP_ExtensionExecutionErrorInJavascript(MANIP_ExtensionExecutionError): pass
class MANIP_UnexpectedExtensionExecutionError(MANIP_ExtensionExecutionError): pass

class MANIP_ExtensionJSONDecodeError(MANIP_Error): pass


class MANIP_BadOrInvalidExtensionCodeError(MANIP_Error): pass
class MANIP_InvalidExtensionCodeSyntaxError(MANIP_BadOrInvalidExtensionCodeError): pass
class MANIP_BadExtensionCodeFormatError(MANIP_BadOrInvalidExtensionCodeError): pass
class MANIP_InvalidTranslationMessageError(MANIP_BadOrInvalidExtensionCodeError): pass

class MANIP_JsNodeTreeToJsonConversionError(MANIP_Error): pass

# generator.py
class MANIP_InvalidExtensionInformationError(MANIP_Error): pass
class MANIP_InvalidCustomMenuError(MANIP_InvalidExtensionInformationError): pass
class MANIP_InvalidCustomBlockError(MANIP_InvalidExtensionInformationError): pass
class MANIP_UnknownExtensionAttributeError(MANIP_InvalidExtensionInformationError): pass

# manager.py
class MANIP_ExtensionFetchError(MANIP_Error): """Groups any error in fetch_js"""
class MANIP_DirectExtensionInfoExtractionError(MANIP_Error): """Groups any error in extract_extension_info_directly"""
class MANIP_SafeExtensionInfoExtractionError(MANIP_Error): """Groups any error in extract_extension_info_safely"""
class MANIP_ExtensionInfoConvertionError(MANIP_Error): """Groups any error in generate_opcode_info_group"""




###############################################################
#                      ERRORS FOR THE CONFIG                  #
###############################################################

class MANIP_ConfigurationError(MANIP_Error): pass


###############################################################
#                       ERRORS FOR UTILITY                    #
###############################################################

class MANIP_FailedFileWriteError(MANIP_Error): pass
class MANIP_FailedFileReadError(MANIP_Error): pass
class MANIP_FailedFileDeleteError(MANIP_Error): pass

###############################################################
#                     COPIED BUILT-IN ERRORS                  #
###############################################################

class MANIP_NotImplementedError(MANIP_Error): pass
class MANIP_TypeError(MANIP_Error): pass
class MANIP_KeyError(MANIP_Error): pass
class MANIP_IndexError(MANIP_Error): pass
class MANIP_ValueError(MANIP_Error): pass
class MANIP_AttributeError(MANIP_Error): pass
class MANIP_OSError(MANIP_Error): pass
class MANIP_FileNotFoundError(MANIP_OSError): pass

###############################################################
#                         SPECIAL ERRORS                      #
###############################################################

class MANIP_UnsupportedOSError(MANIP_Error): pass
class MANIP_SetupRequiredError(MANIP_Error): pass # TODO: comment unused errors
class MANIP_TempNotImplementedError(MANIP_Error):
    """Occurs on features that are not YET implemented"""


"""__all__ = [
    "MANIP_Error", "MANIP_BlameDevsError", "MANIP_ThanksError", 
    
    
    "MANIP_OpcodeInfoError", "MANIP_UnknownOpcodeError", "MANIP_SameOpcodeTwiceError", 
    
    
    "MANIP_DeserializationError", "MANIP_ConversionError",
    
    
    "MANIP_ValidationError", "MANIP_PathValidationError", "MANIP_TypeValidationError", "MANIP_InvalidValueError",
    "MANIP_RangeValidationError", "MANIP_MissingInputError", "MANIP_UnnecessaryInputError", 
    "MANIP_MissingDropdownError", "MANIP_UnnecessaryDropdownError", "MANIP_InvalidDropdownValueError", 
    "MANIP_InvalidOpcodeError", "MANIP_InvalidBlockShapeError", "MANIP_SpriteLayerStackError", 
    "MANIP_SameValueTwiceError",
    
    
    "MANIP_InvalidExtensionSourceError", 
    "MANIP_FetchError", "MANIP_NetworkFetchError", "MANIP_UnexpectedFetchError", "MANIP_FileFetchError",
    "MANIP_JsParsingError", 
    "MANIP_InvalidExtensionCodeError", "MANIP_EsprimaToJsonConversionError", 
    
    "MANIP_UnknownExtensionAttributeError",
    
    
    "MANIP_ConfigurationError", 
]""" # TODO: when done with error update: reintroduce maintanence

