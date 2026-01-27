from __future__ import annotations

from gceutils import (
    AbstractTreePath,
    GU_Error, GU_ValidationError, GU_PathValidationError,
    GU_TypeValidationError, GU_InvalidValueError, GU_RangeValidationError,
    GU_FailedFileWriteError, GU_FailedFileReadError, GU_FailedFileDeleteError,
    GU_FileNotFoundError,
)


class MANIP_Error(Exception): pass
class MANIP_BlameDevsError(MANIP_Error): pass
class MANIP_ImplementationDetailsExposedError(MANIP_Error): pass
class MANIP_ThanksError(MANIP_Error):
    def __init__(self):
        super().__init__("Your project is unique! It could help me with my research! Please create an issue with your project attached! https://github.com/GermanCodeEngineer/py-pmp-manip/issues/new/")

###############################################################
#                     COPIED BUILT-IN ERRORS                  #
###############################################################

class GU_FileNotFoundError(OSError): pass

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

class MANIP_MissingInputError(GU_PathValidationError, ValueError): pass
class MANIP_UnnecessaryInputError(GU_PathValidationError, ValueError): pass
class MANIP_MissingDropdownError(GU_PathValidationError, ValueError): pass
class MANIP_UnnecessaryDropdownError(GU_PathValidationError, ValueError): pass

class MANIP_InvalidDropdownValueError(GU_PathValidationError, ValueError): pass

class MANIP_InvalidOpcodeError(GU_PathValidationError, ValueError): pass
class MANIP_InvalidBlockShapeError(GU_PathValidationError, ValueError): pass
class MANIP_InvalidDirPathError(GU_PathValidationError, ValueError): pass

class MANIP_SpriteLayerStackError(GU_PathValidationError, ValueError): pass

class MANIP_SameValueTwiceError(GU_ValidationError, ValueError):
    def __init__(self, path1: AbstractTreePath, path2: AbstractTreePath, msg: str, condition: str|None = None) -> None:
        self.path1     = path1
        self.path2     = path2
        self.msg       = msg
        self.condition = condition
        
        full_message = f"At {path1} and {path2}: "
        if condition is not None:
            full_message += f"{condition}: "
        full_message += msg
        super().__init__(full_message)

###############################################################
#         ERRORS FOR THE EXT INFO GEN AND PROJECT_API         #
###############################################################

# fetch_js.py
class MANIP_InvalidExtensionCodeSourceError(MANIP_Error): pass

class MANIP_FetchError(MANIP_Error): pass
class MANIP_NetworkFetchError(MANIP_FetchError): pass
class MANIP_UnexpectedFetchError(MANIP_FetchError): pass
class MANIP_FileFetchError(MANIP_FetchError): pass

# direct_extractor.py / safe_extractor.py / api.py
class MANIP_NoNodeJSInstalledError(MANIP_Error): pass

class MANIP_SubprocessTimeoutError(MANIP_Error): pass
class MANIP_ExtensionExecutionErrorInJavascript(MANIP_Error): pass
class MANIP_UnexpectedSubprocessError(MANIP_Error): pass

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


"""__all__ = []""" # TODO: when done with error update: reintroduce maintanence

