from utility import PypenguinEnum

class SRTTSLanguage(PypenguinEnum):    
    @staticmethod
    def from_string(string: str):
        match string:
            case "ar"    : return SRTTSLanguage.ARABIC
            case "zh-cn" : return SRTTSLanguage.CHINESE_MANDARIN
            case "da"    : return SRTTSLanguage.DANISH
            case "nl"    : return SRTTSLanguage.DUTCH
            case "en"    : return SRTTSLanguage.ENGLISH
            case "fr"    : return SRTTSLanguage.FRENCH
            case "de"    : return SRTTSLanguage.GERMAN
            case "hi"    : return SRTTSLanguage.HINDI
            case "is"    : return SRTTSLanguage.ICELANDIC
            case "it"    : return SRTTSLanguage.ITALIAN
            case "ja"    : return SRTTSLanguage.JAPANESE
            case "ko"    : return SRTTSLanguage.KOREAN
            case "nb"    : return SRTTSLanguage.NORWEGIAN
            case "pl"    : return SRTTSLanguage.POLISH
            case "pt-br" : return SRTTSLanguage.PORTUGUESE_BRAZILIAN
            case "pt"    : return SRTTSLanguage.PORTUGUESE
            case "ro"    : return SRTTSLanguage.ROMANIAN
            case "ru"    : return SRTTSLanguage.RUSSIAN
            case "es"    : return SRTTSLanguage.SPANISH
            case "es-419": return SRTTSLanguage.SPANISH_LATIN_AMERICAN
            case "sv"    : return SRTTSLanguage.SWEDISH
            case "tr"    : return SRTTSLanguage.TURKISH
            case "cy"    : return SRTTSLanguage.WELSH
            case _: raise ValueError()

    ARABIC                 =  0
    CHINESE_MANDARIN       =  1
    DANISH                 =  2
    DUTCH                  =  3
    ENGLISH                =  4
    FRENCH                 =  5
    GERMAN                 =  6
    HINDI                  =  7
    ICELANDIC              =  8
    ITALIAN                =  9
    JAPANESE               = 10
    KOREAN                 = 11
    NORWEGIAN              = 12
    POLISH                 = 13
    PORTUGUESE_BRAZILIAN   = 14
    PORTUGUESE             = 15
    ROMANIAN               = 16
    RUSSIAN                = 17
    SPANISH                = 18
    SPANISH_LATIN_AMERICAN = 19
    SWEDISH                = 20
    TURKISH                = 21
    WELSH                  = 22
    
class SRVideoState(PypenguinEnum):
    @staticmethod
    def from_string(value: str) -> "SRVideoState":
        if   value == "on"        : return SRVideoState.ON
        elif value == "on flipped": return SRVideoState.ON_FLIPPED
        elif value == "off"       : return SRVideoState.OFF
        else: raise ValueError(f"Invalid video state: {value}")

    ON         = 0
    ON_FLIPPED = 1
    OFF        = 2

class SRSpriteRotationStyle(PypenguinEnum):
    @staticmethod
    def from_string(string: str):
        match string:
            case "all around"  : return SRSpriteRotationStyle.ALL_AROUND
            case "left-right"  : return SRSpriteRotationStyle.LEFT_RIGHT
            case "don't rotate": return SRSpriteRotationStyle.DONT_ROTATE
            case _: raise ValueError()

    ALL_AROUND  = 0
    LEFT_RIGHT  = 1
    DONT_ROTATE = 2

