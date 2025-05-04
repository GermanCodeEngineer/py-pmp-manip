from pypenguin.utility import PypenguinEnum, FSCError

class SRTTSLanguage(PypenguinEnum):    
    """
    The second representation for a text to speech language
    """

    @classmethod
    def from_code(cls, code: str) -> "SRTTSLanguage":
        """
        Gets the equivalent language enum by its scratch language code.
        
        Args:
            code: the language code
        
        Returns:
            the language enum
        """
        if code in cls._value2member_map_:
            return cls._value2member_map_[code]
        raise FSCError(f"Couldn't find language enum for language code: {repr(code)}")
        
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
    
class SRVideoState(PypenguinEnum):
    """
    The second representation for the video state of a project
    """

    @classmethod
    def from_code(cls, code: str) -> "SRVideoState":
        """
        Gets the equivalent video state enum by its video state code.
        
        Args:
            code: the video state code
        
        Returns:
            the video state enum
        """
        if code in cls._value2member_map_:
            return cls._value2member_map_[code]
        raise FSCError(f"Couldn't find video state enum for video state code: {repr(code)}")
    
    ON         = "on"
    ON_FLIPPED = "on flipped"
    OFF        = "off"

class SRSpriteRotationStyle(PypenguinEnum):
    """
    The second representation for the rotation style of a sprite
    """

    @classmethod
    def from_code(cls, code: str) -> "SRSpriteRotationStyle":
        """
        Gets the equivalent rotation style enum by its rotation style code.
        
        Args:
            code: the rotation style code
        
        Returns:
            the rotation style enum
        """
        if code in cls._value2member_map_:
            return cls._value2member_map_[code]
        raise FSCError(f"Couldn't find rotation style enum for rotation style code: {repr(code)}")

    ALL_AROUND  = "all around"
    LEFT_RIGHT  = "left-right"
    DONT_ROTATE = "don't rotate"

