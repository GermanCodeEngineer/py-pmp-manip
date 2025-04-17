from enum import Enum

class BlockInfoSet:
    _grepr = True
    _grepr_fields = ["name", "opcode_prefix", "alt_opcode_prefixes", "block_infos"]
    
    name: str
    opcode_prefix: str
    alt_opcode_prefixes: list[str]
    block_infos: dict[str, "BlockInfo"]
    
    def __init__(self, 
        name: str, 
        opcode_prefix: str, 
        alt_opcode_prefixes: list[str] | None = None,
        block_infos: dict[str, "BlockInfo"] | None = None,
    ):
        self.name                = name
        self.opcode_prefix       = opcode_prefix
        self.alt_opcode_prefixes = alt_opcode_prefixes or []
        self.block_infos         = {}
        for opcode, block_info in (block_infos or {}).items():
            self.add_block(opcode, block_info)
    
    def get_all_possible_prefixes(self) -> list[str]:
        return [self.opcode_prefix] + self.alt_opcode_prefixes
    
    def uses_prefix(self, prefix: str) -> bool:
        return prefix in self.get_all_possible_prefixes()
    
    def add_block(self, opcode: str, block_info: "BlockInfo"):
        if block_info.alt_opcode_prefix is not None:
            if block_info.alt_opcode_prefix not in self.alt_opcode_prefixes:
                raise ValueError(f"Alternate opcode prefix {repr(block_info.alt_opcode_prefix)} was never added.")
        self.block_infos[opcode] = block_info
    
    def get_block_info(self, opcode: str, default_none: bool = False) -> "BlockInfo":
        if opcode in self.block_infos:
            return self.block_infos[opcode]
        if default_none:
            return None
        raise ValueError(f"Couldn't find Block {repr(opcode)}")

class BlockInfo:
    _grepr = True
    _grepr_fields = ["block_type", "new_opcode", "inputs", "dropdowns", "can_have_monitor"]
    
    block_type: "BlockType"
    new_opcode: str
    inputs: dict[str, "InputInfo"]
    dropdowns: dict[str, "DropdownInfo"]
    can_have_monitor: bool
    alt_opcode_prefix: str | None
    
    def __init__(self, 
        block_type: "BlockType", 
        new_opcode: str, 
        inputs: dict[str, "InputInfo"] = {},
        dropdowns: dict[str, "DropdownInfo"] = {},
        can_have_monitor: bool = False,
        alt_opcode_prefix: str | None = None,
    ):
        self.block_type        = block_type
        self.new_opcode        = new_opcode
        self.inputs            = inputs
        self.dropdowns         = dropdowns
        self.can_have_monitor  = can_have_monitor
        self.alt_opcode_prefix = alt_opcode_prefix
    
    def get_input_info(self, input_id: str) -> "InputInfo":
        return self.inputs[input_id]
    
    def get_input_type(self, input_id: str) -> "InputType":
        return self.get_input_info(input_id).type
    
    def get_input_mode(self, input_id: str) -> "InputMode":
        return self.get_input_type(input_id).get_mode()

    def get_new_input_id(self, input_id: str) -> str:
        return self.inputs[input_id].new

    def get_new_dropdown_id(self, dropdown_id: str) -> str:
        return self.dropdowns[dropdown_id].new

class BlockType(Enum):
    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
    
    STATEMENT         = 0
    ENDING_STATEMENT  = 1
    HAT               = 2
    
    STRING_REPORTER   = 3
    NUMBER_REPORTER   = 4
    BOOLEAN_REPORTER  = 5
    
    # Pseudo Blocktypes
    MENU              = 6
    POLYGON_MENU      = 7 # Exclusively for the "polygon" block
    NOT_RELEVANT      = 8
    DYNAMIC           = 9
    
class InputInfo:
    _grepr = True
    _grepr_fields = ["type", "new", "menu"]
    
    type: "InputType"
    new: str
    menu: "MenuInfo | None"
    
    def __init__(self, type: "InputType", new: str, menu: "MenuInfo|None" = None):
        self.type = type
        self.new  = new
        self.menu = menu

class InputMode(Enum):
    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
    
    BLOCK_AND_TEXT               = 0
    BLOCK_AND_MENU_TEXT          = 1
    BLOCK_ONLY                   = 2
    SCRIPT                       = 3
    BLOCK_AND_BROADCAST_DROPDOWN = 4
    BLOCK_AND_DROPDOWN           = 5

class InputType(Enum):
    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
    
    def get_mode(self) -> InputMode:
        return self.value[0]
    
    @staticmethod
    def get_by_cb_default(default: str) -> "InputType":
        match default:
            case "":
                return InputType.TEXT
            case "false":
                return InputType.BOOLEAN
            case _: raise ValueError()
    
    # BLOCK_AND_TEXT
    DIRECTION           = (InputMode.BLOCK_AND_TEXT, 0)
    INTEGER             = (InputMode.BLOCK_AND_TEXT, 1)
    POSITIVE_INTEGER    = (InputMode.BLOCK_AND_TEXT, 2)
    POSITIVE_NUMBER     = (InputMode.BLOCK_AND_TEXT, 3)
    NUMBER              = (InputMode.BLOCK_AND_TEXT, 4)
    TEXT                = (InputMode.BLOCK_AND_TEXT, 5)
    COLOR               = (InputMode.BLOCK_AND_TEXT, 6)

    # BLOCK_AND_MENU_TEXT
    NOTE                = (InputMode.BLOCK_AND_MENU_TEXT, 0)

    # BLOCK_ONLY
    BOOLEAN             = (InputMode.BLOCK_ONLY, 0)
    ROUND               = (InputMode.BLOCK_ONLY, 1)
    EMBEDDED_MENU       = (InputMode.BLOCK_ONLY, 2)

    # SCRIPT
    SCRIPT              = (InputMode.SCRIPT, 0)

    # BLOCK_AND_BROADCAST_DROPDOWN
    BROADCAST           = (InputMode.BLOCK_AND_BROADCAST_DROPDOWN, 0)

    # BLOCK_AND_DROPDOWN
    STAGE_OR_OTHER_SPRITE               = (InputMode.BLOCK_AND_DROPDOWN,  0)
    CLONING_TARGET                      = (InputMode.BLOCK_AND_DROPDOWN,  1)
    MOUSE_OR_OTHER_SPRITE               = (InputMode.BLOCK_AND_DROPDOWN,  2)
    MOUSE_EDGE_OR_OTHER_SPRITE          = (InputMode.BLOCK_AND_DROPDOWN,  3)
    MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE   = (InputMode.BLOCK_AND_DROPDOWN,  4)
    KEY                                 = (InputMode.BLOCK_AND_DROPDOWN,  5)
    UP_DOWN                             = (InputMode.BLOCK_AND_DROPDOWN,  6)
    FINGER_INDEX                        = (InputMode.BLOCK_AND_DROPDOWN,  7)
    RANDOM_MOUSE_OR_OTHER_SPRITE        = (InputMode.BLOCK_AND_DROPDOWN,  8)
    COSTUME                             = (InputMode.BLOCK_AND_DROPDOWN,  9)
    COSTUME_PROPERTY                    = (InputMode.BLOCK_AND_DROPDOWN, 10)
    BACKDROP                            = (InputMode.BLOCK_AND_DROPDOWN, 11)
    BACKDROP_PROPERTY                   = (InputMode.BLOCK_AND_DROPDOWN, 12)
    MYSELF_OR_OTHER_SPRITE              = (InputMode.BLOCK_AND_DROPDOWN, 13)
    SOUND                               = (InputMode.BLOCK_AND_DROPDOWN, 14)
    DRUM                                = (InputMode.BLOCK_AND_DROPDOWN, 15)
    INSTRUMENT                          = (InputMode.BLOCK_AND_DROPDOWN, 16)
    FONT                                = (InputMode.BLOCK_AND_DROPDOWN, 17)
    PEN_PROPERTY                        = (InputMode.BLOCK_AND_DROPDOWN, 18)
    VIDEO_SENSING_PROPERTY              = (InputMode.BLOCK_AND_DROPDOWN, 19)
    VIDEO_SENSING_TARGET                = (InputMode.BLOCK_AND_DROPDOWN, 20)
    VIDEO_STATE                         = (InputMode.BLOCK_AND_DROPDOWN, 21)
    TEXT_TO_SPEECH_VOICE                = (InputMode.BLOCK_AND_DROPDOWN, 22)
    TEXT_TO_SPEECH_LANGUAGE             = (InputMode.BLOCK_AND_DROPDOWN, 23)
    TRANSLATE_LANGUAGE                  = (InputMode.BLOCK_AND_DROPDOWN, 24)
    MAKEY_KEY                           = (InputMode.BLOCK_AND_DROPDOWN, 25)
    MAKEY_SEQUENCE                      = (InputMode.BLOCK_AND_DROPDOWN, 26)
    READ_FILE_MODE                      = (InputMode.BLOCK_AND_DROPDOWN, 27)
    FILE_SELECTOR_MODE                  = (InputMode.BLOCK_AND_DROPDOWN, 28)

class DropdownInfo:
    _grepr = True
    _grepr_fields = ["type", "new"]
    
    type: "DropdownType"
    new: str
    
    def __init__(self, type: "DropdownType", new: str):
        self.type = type
        self.new  = new


class DropdownTypeInfo:
    _grepr = True
    _grepr_fields = ["direct_values", "value_segments", "old_direct_values", "fallback"]

    direct_values:     list[str | int | bool] | None = None
    value_segments:    list[str]              | None = None
    old_direct_values: list[str | int | bool] | None = None
    fallback:          list[str]              | None = None

    def __init__(self,
        direct_values:     list[str | int | bool] | None = None,
        value_segments:    list[str]              | None = None,
        old_direct_values: list[str | int | bool] | None = None,
        fallback:          list[str]              | None = None,
    ) -> None:
        self.direct_values     = direct_values     or []
        self.value_segments    = value_segments    or []
        self.old_direct_values = old_direct_values or []
        self.fallback          = fallback          or []

class DropdownType(Enum):    
    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
    
    def get_type_info(self) -> DropdownTypeInfo:
        return self.value
    
    KEY = DropdownTypeInfo(
        direct_values=[
            "space", "up arrow", "down arrow", "right arrow", "left arrow", 
            "enter", "any", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", 
            "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "-", ",", ".", "`", "=", "[", "]", "\\", ";", "'", "/", "!", "@", 
            "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "{", "}", "|", 
            ":", '"', "?", "<", ">", "~", "backspace", "delete", "shift", 
            "caps lock", "scroll lock", "control", "escape", "insert", 
            "home", "end", "page up", "page down",
        ]
    )
    UNARY_MATH_OPERATION = DropdownTypeInfo(
        direct_values=["abs", "floor", "ceiling", "sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "ln", "log", "e ^", "10 ^"]
    )
    POWER_ROOT_LOG = DropdownTypeInfo(direct_values=["^", "root", "log"])
    ROOT_LOG = DropdownTypeInfo(direct_values=["root", "log"])
    TEXT_METHOD = DropdownTypeInfo(direct_values=["starts", "ends"])
    TEXT_CASE = DropdownTypeInfo(
        direct_values=["uppercase", "lowercase"],
        old_direct_values=["upper", "lower"]
    )
    STOP_SCRIPT_TARGET = DropdownTypeInfo(
        direct_values=["all", "this script", "other scripts in sprite"]
    )
    STAGE_OR_OTHER_SPRITE = DropdownTypeInfo(value_segments=["stage", "other sprite"])
    CLONING_TARGET = DropdownTypeInfo(
        value_segments=["myself if not stage", "other sprite not stage"],
        fallback=["fallback", " "]
    )
    UP_DOWN = DropdownTypeInfo(direct_values=["up", "down"])
    LOUDNESS_TIMER = DropdownTypeInfo(
        direct_values=["loudness", "timer"],
        old_direct_values=["LOUDNESS", "TIMER"],
    )
    MOUSE_OR_OTHER_SPRITE = DropdownTypeInfo(value_segments=["mouse-pointer", "other sprite"])
    MOUSE_EDGE_OR_OTHER_SPRITE = DropdownTypeInfo(value_segments=["mouse-pointer", "edge", "other sprite"])
    MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE = DropdownTypeInfo(value_segments=["mouse-pointer", "edge", "myself", "other sprite"])
    X_OR_Y = DropdownTypeInfo(direct_values=["x", "y"])
    DRAG_MODE = DropdownTypeInfo(direct_values=["draggable", "not draggable"])
    MUTABLE_SPRITE_PROPERTY = DropdownTypeInfo(value_segments=["mutable sprite property"])
    READABLE_SPRITE_PROPERTY = DropdownTypeInfo(value_segments=["readable sprite property"])
    TIME_PROPERTY = DropdownTypeInfo(
        direct_values=["year", "month", "date", "day of week", "hour", "minute", "second", "js timestamp"],
        old_direct_values=["YEAR", "MONTH", "DATE", "DAYOFWEEK", "HOUR", "MINUTE", "SECOND", "TIMESTAMP"],
    )
    FINGER_INDEX = DropdownTypeInfo(direct_values=["1", "2", "3", "4", "5"])
    RANDOM_MOUSE_OR_OTHER_SPRITE = DropdownTypeInfo(value_segments=["random_position", "mouse-pointer", "other sprite"])
    ROTATION_STYLE = DropdownTypeInfo(direct_values=["left-right", "up-down", "don't rotate", "look at", "all around"])
    STAGE_ZONE = DropdownTypeInfo(direct_values=["bottom-left", "bottom", "bottom-right", "top-left", "top", "top-right", "left", "right"])
    TEXT_BUBBLE_COLOR_PROPERTY = DropdownTypeInfo(
        direct_values=["border", "fill", "text"],
        old_direct_values=["BUBBLE_STROKE", "BUBBLE_FILL", "TEXT_FILL"],
    )
    TEXT_BUBBLE_PROPERTY = DropdownTypeInfo(
        direct_values = ["MIN_WIDTH", "MAX_LINE_WIDTH", "STROKE_WIDTH", "PADDING", "CORNER_RADIUS", "TAIL_HEIGHT", "FONT_HEIGHT_RATIO", "texlim"],
        old_direct_values=["minimum width", "maximum width" , "border line width", "padding size", "corner radius", "tail height", "font pading percent", "text length limit"],
    )
    SPRITE_EFFECT = DropdownTypeInfo(
        direct_values=["color", "fisheye", "whirl", "pixelate", "mosaic", "brightness", "ghost", "saturation", "red", "green", "blue", "opaque"],
        old_direct_values=["COLOR", "FISHEYE", "WHIRL", "PIXELATE", "MOSAIC", "BRIGHTNESS", "GHOST", "SATURATION", "RED", "GREEN", "BLUE", "OPAQUE"],
    )
    COSTUME = DropdownTypeInfo(value_segments=["costume"])
    BACKDROP = DropdownTypeInfo(value_segments=["backdrop"])
    COSTUME_PROPERTY = DropdownTypeInfo(direct_values=["width", "height", "rotation center x", "rotation center y", "drawing mode"])
    MYSELF_OR_OTHER_SPRITE = DropdownTypeInfo(value_segments=["myself", "other sprite"])
    FRONT_BACK = DropdownTypeInfo(direct_values=["front", "back"])
    FORWARD_BACKWARD = DropdownTypeInfo(direct_values=["forward", "backward"])
    INFRONT_BEHIND = DropdownTypeInfo(direct_values=["infront", "behind"])
    NUMBER_NAME = DropdownTypeInfo(direct_values=["number", "name"])
    SOUND = DropdownTypeInfo(
        value_segments=["sound"], 
        fallback=["fallback", " "]
    )
    SOUND_EFFECT = DropdownTypeInfo(
        direct_values=["pitch", "pan"],
        old_direct_values=["PITCH", "PAN"],
    )
    BLOCK_TYPE = DropdownTypeInfo(direct_values=["instruction", "lastInstruction", "textReporter", "numberReporter", "booleanReporter"],)
    DRUM = DropdownTypeInfo(
        direct_values=["(1) Snare Drum", "(2) Bass Drum", "(3) Side Stick", "(4) Crash Cymbal", "(5) Open Hi-Hat", "(6) Closed Hi-Hat", "(7) Tambourine", "(8) Hand Clap", "(9) Claves", "(10) Wood Block", "(11) Cowbell", "(12) Triangle", "(13) Bongo", "(14) Conga", "(15) Cabasa", "(16) Guiro", "(17) Vibraslap", "(18) Cuica"],
        old_direct_values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"],
    )
    INSTRUMENT = DropdownTypeInfo(
        direct_values=["(1) Piano", "(2) Electric Piano", "(3) Organ", "(4) Guitar", "(5) Electric Guitar", "(6) Bass", "(7) Pizzicato", "(8) Cello", "(9) Trombone", "(10) Clarinet", "(11) Saxophone", "(12) Flute", "(13) Wooden Flute", "(14) Bassoon", "(15) Choir", "(16) Vibraphone", "(17) Music Box", "(18) Steel Drum", "(19) Marimba", "(20) Synth Lead", "(21) Synth Pad"],
        old_direct_values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"],
    )
    NOTE = DropdownTypeInfo(direct_values=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130"])
    FONT = DropdownTypeInfo(
        direct_values=[["suggested", "Sans Serif"], ["suggested", "Serif"], ["suggested", "Handwriting"], ["suggested", "Marker"], ["suggested", "Curly"], ["suggested", "Pixel"], ["suggested", "Playful"], ["suggested", "Bubbly"], ["suggested", "Arcade"], ["suggested", "Bits and Bytes"], ["suggested", "Technological"], ["suggested", "Scratch"], ["suggested", "Archivo"], ["suggested", "Archivo Black"], ["suggested", "random font"]],
        old_direct_values=["Sans Serif", "Serif", "Handwriting", "Marker", "Curly", "Pixel", "Playful", "Bubbly", "Arcade", "Bits and Bytes", "Technological", "Scratch", "Archivo", "Archivo Black", "Random"],
    )
    ON_OFF = DropdownTypeInfo(direct_values=["on", "off"])
    EXPANDED_MINIMIZED = DropdownTypeInfo(
        direct_values=["expanded", "minimized"],
        old_direct_values=[True, False],
    )
    VERTEX_COUNT = DropdownTypeInfo(direct_values=[3, 4])
    PEN_PROPERTY = DropdownTypeInfo(direct_values=["color", "saturation", "brightness", "transparency"])
    ANIMATION_TECHNIQUE = DropdownTypeInfo(direct_values=["type", "rainbow", "zoom"])
    LEFT_CENTER_RIGHT = DropdownTypeInfo(direct_values=["left", "center", "right"])
    VIDEO_SENSING_PROPERTY = DropdownTypeInfo(direct_values=["motion", "direction"])
    VIDEO_SENSING_TARGET = DropdownTypeInfo(
        direct_values=["sprite", "stage"],
        old_direct_values=["this sprite", "Stage"],
    )
    VIDEO_STATE = DropdownTypeInfo(
        direct_values=["on", "off", "on flipped"],
        old_direct_values=["on", "off", "on-flipped"],
    )
    TEXT_TO_SPEECH_VOICE = DropdownTypeInfo(
        direct_values=["alto", "tenor", "squeak", "giant", "kitten", "google"],
        old_direct_values=["ALTO", "TENOR", "SQUEAK", "GIANT", "KITTEN", "GOOGLE"],
    )
    TEXT_TO_SPEECH_LANGUAGE = DropdownTypeInfo(
        direct_values=["Arabic (ar)", "Chinese (Mandarin) (zh-cn)", "Danish (da)", "Dutch (nl)", "English (en)", "French (fr)", "German (de)", "Hindi (hi)", "Icelandic (is)", "Italian (it)", "Japanese (ja)", "Korean (ko)", "Norwegian (nb)", "Polish (pl)", "Portuguese (Brazilian) (pt-br)", "Portuguese (pt)", "Romanian (ro)", "Russian (ru)", "Spanish (es)", "Spanish (Latin American) (es-419)", "Swedish (sv)", "Turkish (tr)", "Welsh (cy)"],
        old_direct_values=["ar", "zh-cn", "da", "nl", "en", "fr", "de", "hi", "is", "it", "ja", "ko", "nb", "pl", "pt-br", "pt", "ro", "ru", "es", "es-419", "sv", "tr", "cy"],
    )
    TRANSLATE_LANGUAGE = DropdownTypeInfo(
        direct_values=["Amharic (am)", "Arabic (ar)", "Azerbaijani (az)", "Basque (eu)", "Bulgarian (bg)", "Catalan (ca)", "Chinese (Mandarin) (zh-cn)", "Chinese (Traditional) (zh-tw)", "Croatian (hr)", "Czech (cs)", "Danish (da)", "Dutch (nl)", "English (en)", "Estonian (en)", "Finnish (fi)", "French (fr)", "Galician (gl)", "German (de)", "Greek (el)", "Hebrew (he)", "Hungarian (hu)", "Icelandic (is)", "Indonesian (id)", "Irish (ga)", "Italian (it)", "Japanese (ja)", "Korean (ko)", "Lativan (lv)", "Lithuanian (lt)", "Maori (mi)", "Norwegian (nb)", "Persian (fa)", "Polish (pl)", "Portuguese (pt)", "Romanian (ro)", "Russian (ru)", "Scots Gaelic (gd)", "Serbian (sr)", "Slovak (sk)", "Slovenian (sl)", "Spanish (es)", "Swedish (sv)", "Thai (th)", "Turkish (tr)", "Ukrainian (uk)", "Viatnamese (vi)",  "Welsh (cy)", "Zulu (zu)"],
        old_direct_values=["am", "ar", "az", "eu", "bg", "ca", "zh-cn", "zh-tw", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "gl", "de", "el", "he", "hu", "is", "id", "ga", "it", "ja", "ko", "lv", "lt", "mi", "nb", "fa", "pl", "pt", "ro", "ru", "gd", "sr", "sk", "sl", "es", "sv", "th", "tr", "uk", "vi", "cy", "zu"],
    )
    MAKEY_KEY = DropdownTypeInfo(
        direct_values=["space", "up arrow", "down arrow", "right arrow", "left arrow", "w", "a", "s", "d", "f", "g"],
        old_direct_values= ["SPACE", "UP", "DOWN", "RIGHT", "LEFT", "w", "a", "s", "d", "f", "g"],
    )
    MAKEY_SEQUENCE = DropdownTypeInfo(
        direct_values=["left up right", "right up left", "left right", "right left", "up down", "down up", "up right down left", "up left down right", "up up down down left right left right"],
        old_direct_values=["LEFT UP RIGHT", "RIGHT UP LEFT", "LEFT RIGHT", "RIGHT LEFT", "UP DOWN", "DOWN UP", "UP RIGHT DOWN LEFT", "UP LEFT DOWN RIGHT", "UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT"],
    )
    READ_FILE_MODE = DropdownTypeInfo(
        direct_values=["text", "data: URL", "array buffer"],
        old_direct_values=["text", "url", "buffer"],
    )
    FILE_SELECTOR_MODE = DropdownTypeInfo(
        direct_values=["show modal", "open selector immediately"],
        old_direct_values=["modal", "selector"],
    )

    
    BROADCAST = DropdownTypeInfo()
    VARIABLE = DropdownTypeInfo()
    LIST = DropdownTypeInfo()
    
    # Temporary, will be removed
    ENABLE_DISABLE_SCREEN_REFRESH = DropdownTypeInfo()
    CUSTOM_OPCODE = DropdownTypeInfo()
    REPORTER_NAME = DropdownTypeInfo()

class MenuInfo:
    _grepr = True
    _grepr_fields = ["opcode", "inner"]
    
    opcode: str
    inner : str
    
    def __init__(self, opcode: str, inner: str):
        self.opcode = opcode
        self.inner  = inner
