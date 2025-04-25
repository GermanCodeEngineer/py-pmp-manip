from utility import PypenguinEnum

class TextToSpeechLanguage(PypenguinEnum):    
    @staticmethod
    def from_string(string: str):
        match string:
            case "ar"    : return TextToSpeechLanguage.ARABIC
            case "zh-cn" : return TextToSpeechLanguage.CHINESE_MANDARIN
            case "da"    : return TextToSpeechLanguage.DANISH
            case "nl"    : return TextToSpeechLanguage.DUTCH
            case "en"    : return TextToSpeechLanguage.ENGLISH
            case "fr"    : return TextToSpeechLanguage.FRENCH
            case "de"    : return TextToSpeechLanguage.GERMAN
            case "hi"    : return TextToSpeechLanguage.HINDI
            case "is"    : return TextToSpeechLanguage.ICELANDIC
            case "it"    : return TextToSpeechLanguage.ITALIAN
            case "ja"    : return TextToSpeechLanguage.JAPANESE
            case "ko"    : return TextToSpeechLanguage.KOREAN
            case "nb"    : return TextToSpeechLanguage.NORWEGIAN
            case "pl"    : return TextToSpeechLanguage.POLISH
            case "pt-br" : return TextToSpeechLanguage.PORTUGUESE_BRAZILIAN
            case "pt"    : return TextToSpeechLanguage.PORTUGUESE
            case "ro"    : return TextToSpeechLanguage.ROMANIAN
            case "ru"    : return TextToSpeechLanguage.RUSSIAN
            case "es"    : return TextToSpeechLanguage.SPANISH
            case "es-419": return TextToSpeechLanguage.SPANISH_LATIN_AMERICAN
            case "sv"    : return TextToSpeechLanguage.SWEDISH
            case "tr"    : return TextToSpeechLanguage.TURKISH
            case "cy"    : return TextToSpeechLanguage.WELSH
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
    
