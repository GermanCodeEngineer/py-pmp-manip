from enum import Enum

class DropdownTypeInfo:
    _grepr = True
    _grepr_fields = ["direct_values", "value_segments", "old_direct_values", "fallback"]

    direct_values:     list[str | int | bool] | None = None
    value_segments:    list[str]              | None = None
    old_direct_values: list[str | int | bool] | None = None
    fallback          : list[str]              | None = None

    def __init__(self,
        direct_values:     list[str | int | bool] | None = None,
        value_segments:    list[str]              | None = None,
        old_direct_values: list[str | int | bool] | None = None,
        fallback      : list[str]              | None = None,
    ) -> None:
        self.direct_values     = direct_values     or []
        self.value_segments    = value_segments    or []
        self.old_direct_values = old_direct_values or []
        self.fallback          = fallback          or []

class DropdownType(Enum):
    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
    
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
        old_direct_values=["LOUDNESS", "TIMER"]
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

optionTypeDatabase = {
    "key": {
        "directValues"   : [
            "space", "up arrow", "down arrow", "right arrow", "left arrow", 
            "enter", "any", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", 
            "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "-", ",", ".", "`", "=", "[", "]", "\\", ";", "'", "/", "!", "@", 
            "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "{", "}", "|", 
            ":", '"', "?", "<", ">", "~", "backspace", "delete", "shift", 
            "caps lock", "scroll lock", "control", "escape", "insert", 
            "home", "end", "page up", "page down",
        ], 
        "valueSegments"  : [],
    },
    "unary math operation": {
        "directValues"   : ["abs", "floor", "ceiling", "sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "ln", "log", "e ^", "10 ^"], 
        "valueSegments"  : [],
    },
    "power|root|log": {
        "directValues"   : ["^", "root", "log"], 
        "valueSegments"  : [],
    },
    "root|log": {
        "directValues"   : ["root", "log"], 
        "valueSegments"  : [],
    },
    "text method": {
        "directValues"   : ["starts", "ends"], 
        "valueSegments"  : [],
    },
    "text case": {
        "oldDirectValues": ["upper", "lower"], 
        "directValues"   : ["uppercase", "lowercase"],
        "valueSegments"  : [],
    },
    "stop script target": {
        "directValues"   : ["all", "this script", "other scripts in sprite"], 
        "valueSegments"  : [],
    },
    "stage || other sprite": {
        "directValues"   : [], 
        "valueSegments"  : ["stage", "other sprite"],
    },
    "cloning target": {
        "directValues"   : [], 
        "valueSegments"  : ["myself if not stage", "other sprite not stage"],
        "fallback"       : ["fallback", " "],
    },
    "up|down": {
        "directValues"   : ["up", "down"], 
        "valueSegments"  : [],
    },
    "loudness|timer": {
        "directValues"   : ["loudness", "timer"], 
        "oldDirectValues": ["LOUDNESS", "TIMER"],
        "valueSegments"  : [],
    },
    "mouse || other sprite": {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "other sprite"],
    },
    "mouse|edge || other sprite": {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "edge", "other sprite"],
    },
    "mouse|edge || myself || other sprite" : {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "edge", "myself", "other sprite"],
    },
    "x|y": {
        "directValues"   : ["x", "y"], 
        "valueSegments"  : [],
    },
    "drag mode": {
        "directValues"   : ["draggable", "not draggable"], 
        "valueSegments"  : [],
    },
    "mutable sprite property": {
        "directValues"   : [], 
        "valueSegments"  : ["mutable sprite property"],
    },
    "readable sprite property": {
        "directValues"   : [], 
        "valueSegments"  : ["readable sprite property"],
    },
    "time property": {
        "directValues"   : ["year", "month", "date", "day of week", "hour", "minute", "second", "js timestamp"], 
        "oldDirectValues": ["YEAR", "MONTH", "DATE", "DAYOFWEEK"  , "HOUR", "MINUTE", "SECOND",    "TIMESTAMP"],
        "valueSegments"  : [],
    },
    "finger index": {
        "directValues"   : ["1", "2", "3", "4", "5"], 
        "valueSegments"  : [],
    },
    "random|mouse || other sprite": {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["random position", "mouse-pointer", "other sprite"],
    },
    "rotation style": {
        "directValues"   : ["left-right", "up-down", "don't rotate", "look at", "all around"], 
        "valueSegments"  : [],
    },
    "stage zone": {
        "directValues"   : ["bottom-left", "bottom", "bottom-right", "top-left", "top", "top-right", "left", "right"], 
        "valueSegments"  : [],
    },
    "text bubble color property": {
        "directValues"   : ["border"       , "fill",        "text"     ], 
        "oldDirectValues": ["BUBBLE_STROKE", "BUBBLE_FILL", "TEXT_FILL"],
        "valueSegments"  : [],
    },
    "text bubble property": {
        "directValues"   : ["MIN_WIDTH"    , "MAX_LINE_WIDTH", "STROKE_WIDTH"     , "PADDING"     , "CORNER_RADIUS", "TAIL_HEIGHT", "FONT_HEIGHT_RATIO"  , "texlim"           ], 
        "oldDirectValues": ["minimum width", "maximum width" , "border line width", "padding size", "corner radius", "tail height", "font pading percent", "text length limit"],
        "valueSegments"  : [],
    },
    "sprite effect": {
        "directValues"   : ["color", "fisheye", "whirl", "pixelate", "mosaic", "brightness", "ghost", "saturation", "red", "green", "blue", "opaque"], 
        "oldDirectValues": ["COLOR", "FISHEYE", "WHIRL", "PIXELATE", "MOSAIC", "BRIGHTNESS", "GHOST", "SATURATION", "RED", "GREEN", "BLUE", "OPAQUE"],
        "valueSegments"  : [],
    },
    "costume": {
        "directValues"   : [], 
        "valueSegments"  : ["costume"],
    },
    "backdrop": {
        "directValues"   : [], 
        "valueSegments"  : ["backdrop"],
    },
    "costume property": {
        "directValues"   : ["width", "height", "rotation center x", "rotation center y", "drawing mode"], 
        "valueSegments"  : [],
    },
    "myself || other sprite": {
        "directValues"   : [], 
        "valueSegments"  : ["myself", "other sprite"],
    },
    "front|back": {
        "directValues"   : ["front", "back"], 
        "valueSegments"  : [],
    },
    "forward|backward": {
        "directValues"   : ["forward", "backward"], 
        "valueSegments"  : [],
    },
    "infront|behind": {
        "directValues"   : ["infront", "behind"], 
        "valueSegments"  : [],
    },
    "number|name": {
        "directValues"   : ["number", "name"], 
        "valueSegments"  : [],
    },
    "sound": {
        "directValues"   : [], 
        "valueSegments"  : ["sound"],
        "fallback"       : ["fallback", " "],
    },
    "sound effect": {
        "directValues"   : ["pitch", "pan"], 
        "oldDirectValues": ["PITCH", "PAN"],
        "valueSegments"  : [],
    },
    "blockType": {
        "directValues"   : ["instruction", "lastInstruction", "textReporter", "numberReporter", "booleanReporter"], 
        "valueSegments"  : [],
    },
    "drum": {
        "directValues"   : ["(1) Snare Drum", "(2) Bass Drum", "(3) Side Stick", "(4) Crash Cymbal", "(5) Open Hi-Hat", "(6) Closed Hi-Hat", "(7) Tambourine", "(8) Hand Clap", "(9) Claves", "(10) Wood Block", "(11) Cowbell", "(12) Triangle", "(13) Bongo", "(14) Conga", "(15) Cabasa", "(16) Guiro", "(17) Vibraslap", "(18) Cuica"],
        "oldDirectValues": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"],
        "valueSegments"  : [],
    },
    "instrument": {
        "directValues"   : ["(1) Piano", "(2) Electric Piano", "(3) Organ", "(4) Guitar", "(5) Electric Guitar", "(6) Bass", "(7) Pizzicato", "(8) Cello", "(9) Trombone", "(10) Clarinet", "(11) Saxophone", "(12) Flute", "(13) Wooden Flute", "(14) Bassoon", "(15) Choir", "(16) Vibraphone", "(17) Music Box", "(18) Steel Drum", "(19) Marimba", "(20) Synth Lead", "(21) Synth Pad"],
        "oldDirectValues": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"],
        "valueSegments"  : [],
    },
    "note": {
        "directValues"   : ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130"],
        "valueSegments"  : [],
    },
    "font": {
        "directValues"   : [["suggested", "Sans Serif"], ["suggested", "Serif"], ["suggested", "Handwriting"], ["suggested", "Marker"], ["suggested", "Curly"], ["suggested", "Pixel"], ["suggested", "Playful"], ["suggested", "Bubbly"], ["suggested", "Arcade"], ["suggested", "Bits and Bytes"], ["suggested", "Technological"], ["suggested", "Scratch"], ["suggested", "Archivo"], ["suggested", "Archivo Black"], ["suggested", "random font"]],
        "oldDirectValues": ["Sans Serif", "Serif", "Handwriting", "Marker", "Curly", "Pixel", "Playful", "Bubbly", "Arcade", "Bits and Bytes", "Technological", "Scratch", "Archivo", "Archivo Black", "Random"],
        "valueSegments"  : ["font"],
    },
    "on|off": {
        "directValues"   : ["on", "off"],
        "valueSegments"  : [],
    },
    "expanded|minimized": {
        "directValues"   : ["expanded", "minimized"],
        "oldDirectValues": [True      , False      ], # Yes that is correct. I guess the dev of the pen extension must've messed up.
        "valueSegments"  : [],
    },
    "vertex count": {
        "directValues"   : [3, 4],
        "valueSegments"  : [],
    },
    "pen property": {
        "directValues"   : ["color", "saturation", "brightness", "transparency"],
        "valueSegments"  : [],
    },
    "animation technique": {
        "directValues"   : ["type", "rainbow", "zoom"],
        "valueSegments"  : [],
    },
    "left|center|right"  : {
        "directValues"   : ["left", "center", "right"],
        "valueSegments"  : [],
    },
    "video sensing property": {
        "directValues"   : ["motion", "direction"],
        "valueSegments"  : [],
    },
    "video sensing target": {
        "directValues"   : ["this sprite", "stage"],
        "oldDirectValues": ["this sprite", "Stage"],
        "valueSegments"  : [],
    },
    "video state": {
        "directValues"   : ["on", "off", "on flipped"],
        "oldDirectValues": ["on", "off", "on-flipped"],
        "valueSegments"  : [],
    },
    "text to speech voice": {
        "directValues"   : ["alto", "tenor", "squeak", "giant", "kitten", "google"],
        "oldDirectValues": ["ALTO", "TENOR", "SQUEAK", "GIANT", "KITTEN", "GOOGLE"],
        "valueSegments"  : [],
    },
    "text to speech language": {
        "directValues"   : ["Arabic (ar)", "Chinese (Mandarin) (zh-cn)", "Danish (da)", "Dutch (nl)", "English (en)", "French (fr)", "German (de)", "Hindi (hi)", "Icelandic (is)", "Italian (it)", "Japanese (ja)", "Korean (ko)", "Norwegian (nb)", "Polish (pl)", "Portuguese (Brazilian) (pt-br)", "Portuguese (pt)", "Romanian (ro)", "Russian (ru)", "Spanish (es)", "Spanish (Latin American) (es-419)", "Swedish (sv)", "Turkish (tr)", "Welsh (cy)"],
        "oldDirectValues": ["ar", "zh-cn", "da", "nl", "en", "fr", "de", "hi", "is", "it", "ja", "ko", "nb", "pl", "pt-br", "pt", "ro", "ru", "es", "es-419", "sv", "tr", "cy"],
        "valueSegments"  : [],
    },
    "translate language": {
        "directValues"   : ["Amharic (am)", "Arabic (ar)", "Azerbaijani (az)", "Basque (eu)", "Bulgarian (bg)", "Catalan (ca)", "Chinese (Mandarin) (zh-cn)", "Chinese (Traditional) (zh-tw)", "Croatian (hr)", "Czech (cs)", "Danish (da)", "Dutch (nl)", "English (en)", "Estonian (en)", "Finnish (fi)", "French (fr)", "Galician (gl)", "German (de)", "Greek (el)", "Hebrew (he)", "Hungarian (hu)", "Icelandic (is)", "Indonesian (id)", "Irish (ga)", "Italian (it)", "Japanese (ja)", "Korean (ko)", "Lativan (lv)", "Lithuanian (lt)", "Maori (mi)", "Norwegian (nb)", "Persian (fa)", "Polish (pl)", "Portuguese (pt)", "Romanian (ro)", "Russian (ru)", "Scots Gaelic (gd)", "Serbian (sr)", "Slovak (sk)", "Slovenian (sl)", "Spanish (es)", "Swedish (sv)", "Thai (th)", "Turkish (tr)", "Ukrainian (uk)", "Viatnamese (vi)",  "Welsh (cy)", "Zulu (zu)"],
        "oldDirectValues": ["am", "ar", "az", "eu", "bg", "ca", "zh-cn", "zh-tw", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "gl", "de", "el", "he", "hu", "is", "id", "ga", "it", "ja", "ko", "lv", "lt", "mi", "nb", "fa", "pl", "pt", "ro", "ru", "gd", "sr", "sk", "sl", "es", "sv", "th", "tr", "uk", "vi", "cy", "zu"],
        "valueSegments"  : [],
    },
    "makey key": {
        "directValues"   : ["space", "up arrow", "down arrow", "right arrow", "left arrow", "w", "a", "s", "d", "f", "g"],
        "oldDirectValues": ["SPACE", "UP",       "DOWN",       "RIGHT",       "LEFT",       "w", "a", "s", "d", "f", "g"],
        "valueSegments"  : [],
    },
    "makey sequence": {
        "directValues"   : ["left up right", "right up left", "left right", "right left", "up down", "down up", "up right down left", "up left down right", "up up down down left right left right"],
        "oldDirectValues": ["LEFT UP RIGHT", "RIGHT UP LEFT", "LEFT RIGHT", "RIGHT LEFT", "UP DOWN", "DOWN UP", "UP RIGHT DOWN LEFT", "UP LEFT DOWN RIGHT", "UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT"],
        "valueSegments"  : [],
    },
    "read file mode": {
        "directValues"   : ["text", "data: URL", "array buffer"],
        "oldDirectValues": ["text", "url",       "buffer"      ],
        "valueSegments"  : [],
    },
    "file selector mode": {
        "directValues"   : ["show modal", "open selector immediately"],
        "oldDirectValues": ["modal",      "selector"                 ],
        "valueSegments"  : [],
    },
}

old_option_type_name_to_enum = {
    "key": "KEY",
    "unary math operation": "UNARY_MATH_OPERATION",
    "power|root|log": "POWER_ROOT_LOG",
    "root|log": "ROOT_LOG",
    "text method": "TEXT_METHOD",
    "text case": "TEXT_CASE",
    "stop script target": "STOP_SCRIPT_TARGET",
    "stage || other sprite": "STAGE_OR_OTHER_SPRITE",
    "cloning target": "CLONING_TARGET",
    "up|down": "UP_DOWN",
    "loudness|timer": "LOUDNESS_TIMER",
    "mouse || other sprite": "MOUSE_OR_OTHER_SPRITE",
    "mouse|edge || other sprite": "MOUSE_EDGE_OR_OTHER_SPRITE",
    "mouse|edge || myself || other sprite": "MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE",
    "x|y": "X_OR_Y",
    "drag mode": "DRAG_MODE",
    "mutable sprite property": "MUTABLE_SPRITE_PROPERTY",
    "readable sprite property": "READABLE_SPRITE_PROPERTY",
    "time property": "TIME_PROPERTY",
    "finger index": "FINGER_INDEX",
    "random|mouse || other sprite": "RANDOM_MOUSE_OR_OTHER_SPRITE",
    "rotation style": "ROTATION_STYLE",
    "stage zone": "STAGE_ZONE",
    "text bubble color property": "TEXT_BUBBLE_COLOR_PROPERTY",
    "text bubble property": "TEXT_BUBBLE_PROPERTY",
    "sprite effect": "SPRITE_EFFECT",
    "costume": "COSTUME",
    "backdrop": "BACKDROP",
    "costume property": "COSTUME_PROPERTY",
    "myself || other sprite": "MYSELF_OR_OTHER_SPRITE",
    "front|back": "FRONT_BACK",
    "forward|backward": "FORWARD_BACKWARD",
    "infront|behind": "INFRONT_BEHIND",
    "number|name": "NUMBER_NAME",
    "sound": "SOUND",
    "sound effect": "SOUND_EFFECT",
    "blockType": "BLOCK_TYPE",
    "drum": "DRUM",
    "instrument": "INSTRUMENT",
    "note": "NOTE",
    "font": "FONT",
    "on|off": "ON_OFF",
    "expanded|minimized": "EXPANDED_MINIMIZED",
    "vertex count": "VERTEX_COUNT",
    "pen property": "PEN_PROPERTY",
    "animation technique": "ANIMATION_TECHNIQUE",
    "left|center|right": "LEFT_CENTER_RIGHT",
    "video sensing property": "VIDEO_SENSING_PROPERTY",
    "video sensing target": "VIDEO_SENSING_TARGET",
    "video state": "VIDEO_STATE",
    "text to speech voice": "TEXT_TO_SPEECH_VOICE",
    "text to speech language": "TEXT_TO_SPEECH_LANGUAGE",
    "translate language": "TRANSLATE_LANGUAGE",
    "makey key": "MAKEY_KEY",
    "makey sequence": "MAKEY_SEQUENCE",
    "read file mode": "READ_FILE_MODE",
    "file selector mode": "FILE_SELECTOR_MODE",
}


for member_name, old_name, t_old_name, t_member_name in zip(DropdownType.__members__.keys(), optionTypeDatabase.keys(), old_option_type_name_to_enum.keys(), old_option_type_name_to_enum.values()):
    if member_name != t_member_name:
        print((member_name, t_member_name))
    if old_name != t_old_name:
        print((old_name, t_old_name))
