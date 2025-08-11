from pmp_manip.utility import GEnum, MANIP_ConversionError


class SRCodeEnum(GEnum):
    """
    The base class for an enum which is based on a string code
    """

    @classmethod
    def from_code(cls, code: str) -> "SRCodeEnum":
        """
        Gets the equivalent enum by its string code
        
        Args:
            code: the string code
        
        Returns:
            the equivalent enum
        """
        if code in cls._value2member_map_:
            return cls._value2member_map_[code]
        raise MANIP_ConversionError(f"Could not find an enum for code: {code}")

    def to_code(self) -> str:
        """
        Gets the equivalent string code for the enum
        
        Returns:
            the equivalent string code
        """
        return self.value

class SRTTSLanguage(SRCodeEnum):
    """
    The second representation for a text to speech language
    """
    ARABIC                 = "ar"
    CHINESE_MANDARIN       = "zh-cn"
    DANISH                 = "da"
    DUTCH                  = "nl"
    ENGLISH                = "en"
    FRENCH                 = "fr"
    GERMAN                 = "de"
    HINDI                  = "hi"
    ICELANDIC              = "is"
    ITALIAN                = "it"
    JAPANESE               = "ja"
    KOREAN                 = "ko"
    NORWEGIAN              = "nb"
    POLISH                 = "pl"
    PORTUGUESE_BRAZILIAN   = "pt-br"
    PORTUGUESE             = "pt"
    ROMANIAN               = "ro"
    RUSSIAN                = "ru"
    SPANISH                = "es"
    SPANISH_LATIN_AMERICAN = "es-419"
    SWEDISH                = "sv"
    TURKISH                = "tr"
    WELSH                  = "cy"
    
class SRVideoState(SRCodeEnum):
    """
    The second representation for the video state of a project
    """

    ON         = "on"
    ON_FLIPPED = "on flipped"
    OFF        = "off"

class SRSpriteRotationStyle(SRCodeEnum):
    """
    The second representation for the rotation style of a sprite (e.g. "all around")
    """

    ALL_AROUND  = "all around"
    LEFT_RIGHT  = "left-right"
    DONT_ROTATE = "don't rotate"

class SRVariableMonitorReadoutMode(SRCodeEnum):
    """
    The second representation for the readout mode of a sprite (e.g. "normal readout" or "slider")
    """

    NORMAL = "default"
    LARGE  = "large"
    SLIDER = "slider"


class TargetPlatform(GEnum):
    """
    Represents a target platform for the conversion of a SRProject to a FRProject
    """
    SCRATCH    = 0
    PENGUINMOD = 1


__all__ = ["SRTTSLanguage", "SRVideoState", "SRSpriteRotationStyle", "SRVariableMonitorReadoutMode", "TargetPlatform"]

