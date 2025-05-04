from pypenguin.database.beautiful.motion                   import opcodes as motion
from pypenguin.database.beautiful.looks                    import opcodes as looks
from pypenguin.database.beautiful.sounds                   import opcodes as sounds
from pypenguin.database.beautiful.events                   import opcodes as events
from pypenguin.database.beautiful.control                  import opcodes as control
from pypenguin.database.beautiful.sensing                  import opcodes as sensing
from pypenguin.database.beautiful.operators                import opcodes as operators
from pypenguin.database.beautiful.variables                import opcodes as variables
from pypenguin.database.beautiful.lists                    import opcodes as lists

from pypenguin.database.beautiful.special                  import opcodes as special
from pypenguin.database.beautiful.extension_music          import opcodes as extension_music
from pypenguin.database.beautiful.extension_pen            import opcodes as extension_pen
from pypenguin.database.beautiful.extension_text           import opcodes as extension_text
from pypenguin.database.beautiful.extension_video_sensing  import opcodes as extension_video_sensing
from pypenguin.database.beautiful.extension_text_to_speech import opcodes as extension_text_to_speech
from pypenguin.database.beautiful.extension_translate      import opcodes as extension_translate
from pypenguin.database.beautiful.extension_makey_makey    import opcodes as extension_makey_makey

from pypenguin.database.beautiful.tw_files                 import opcodes as tw_files
from pypenguin.database.beautiful.tw_temporary_variables   import opcodes as tw_temporary_variables

from pypenguin.database.beautiful.link_bitwise             import opcodes as link_bitwise

from pypenguin.database.beautiful.pm_json                  import opcodes as pm_json

#from pypenguin.utility                           import flipKeysAndValues, removeDuplicates
from pypenguin.utility import flipKeysAndValues, removeDuplicates

import functools, re

"""
Category            Status ('.'=some 'x'=all)
    Motion          [x]
    Looks           [x]
    Sound           [x]
    Events          [x]
    Control         [x]
    Sensing         [x]
    Operators       [x]
    Variables       [x]
    Lists           [x]
Extension           Status ('.'=some 'x'=all)
    Music           [x] (Scratch)
    Pen             [x] (Scratch; extended by Penguinmod)
    (Animated) Text [x] (Scratch)
    Video Sensing   [x] (Scratch)
    Text to Speech  [x] (Scratch)  
    Translate       [x] (Scratch)
    Makey Makey     [x] (Scratch)
    Files           [x] (Turbowarp)
    Bitwise         [x] (imported using Turbowarp link)
    JSON            [x] (Penguinmod)
    others aren't implemented (yet)
"""

opcodeDatabase = (
# CATEGORIES
    motion    | looks     | sounds  |
    events    | control   | sensing |
    operators | variables | lists   |
    special   |
# EXTENSIONS
    # Scratch Extensions
    extension_music         | extension_pen            | extension_text      |
    extension_video_sensing | extension_text_to_speech | extension_translate |
    extension_makey_makey   |
    # Turbowarp Extensions
    tw_files                | tw_temporary_variables   | link_bitwise        |
    # Penguinmod Extensions
    pm_json
)

def getAllDeoptimizedOpcodes():
    return [opcode for opcode in opcodeDatabase.keys()]

def getAllOptimizedOpcodes():
    opcodes = {}
    for oldOpcode, opcodeData in opcodeDatabase.items():
        if opcodeData["newOpcode"] in opcodes.values():
            index       = list(opcodes.values()).index(opcodeData["newOpcode"])
            otherOpcode = list(opcodes.keys  ())[index]
            raise Exception(f"Double opocde detected {otherOpcode} and {oldOpcode}")
        opcodes[oldOpcode] = opcodeData["newOpcode"]
    return list(opcodes.values())

def getAllMonitorOpcodes():
    opcodes = {}
    for oldOpcode, opcodeData in opcodeDatabase.items():
        if opcodeData["newOpcode"] in opcodes.values():
            index       = list(opcodes.values()).index(opcodeData["newOpcode"])
            otherOpcode = list(opcodes.keys  ())[index]
            raise Exception(f"Double opocde detected {otherOpcode} and {oldOpcode}")
        
        if opcodeData.get("canHaveMonitor") == True:
            opcodes[oldOpcode] = opcodeData["newOpcode"]
    return list(opcodes.values())

def opcodeExists(opcode):
    return opcode in opcodeDatabase

def getOptimizedOpcode(opcode):
    return opcodeDatabase[opcode]["newOpcode"]

@functools.cache
def getDeoptimizedOpcode(opcode):
    found = False
    for oldOpcode, opcodeData in opcodeDatabase.items():
        if opcodeData["newOpcode"] == opcode:
            found = True
            break
    assert found, f"Opcode not found: {opcode}"
    return oldOpcode

def getOptimizedInputId(opcode, inputId):
    if "inputTranslation" in opcodeDatabase[opcode]:
        if inputId in opcodeDatabase[opcode]["inputTranslation"]:
            return opcodeDatabase[opcode]["inputTranslation"][inputId]
    if "menus" in opcodeDatabase[opcode]:
        for menuData in opcodeDatabase[opcode]["menus"]:
            if menuData["outer"] == inputId:
                return menuData["new"]
    return inputId

def getDeoptimizedInputId(opcode, inputId):
    if "inputTranslation" in opcodeDatabase[opcode]:
        table = flipKeysAndValues(
            opcodeDatabase[opcode]["inputTranslation"]
        )
        if inputId in table:
            return table[inputId]
    if "menus" in opcodeDatabase[opcode]:
        for menuData in opcodeDatabase[opcode]["menus"]:
            if menuData["new"] == inputId:
                return menuData["outer"]
    return inputId

def getPredefinedTokens(opcode):
    return opcodeDatabase[opcode].get("tokens", None)

def getInputType(opcode, inputId):
    try:
        return opcodeDatabase[opcode]["inputTypes"][inputId]
    except KeyError:
        raise Exception(f"Could not find input '{inputId}' for a block with opcode '{opcode}'")

def getInputTypes(opcode):
    return opcodeDatabase[opcode]["inputTypes"]

def getInputMode(opcode, inputId):
    return inputModes[getInputType(
        opcode=opcode, 
        inputId=inputId,
    )]

def getInputModes(opcode):
    return {inputId: getInputMode(
        opcode=opcode,
        inputId=inputId,
    ) for inputId in getInputTypes(opcode).keys()}

def getOptimizedOptionId(opcode, optionId):
    if "optionTranslation" not in opcodeDatabase[opcode]:
        return optionId
    if optionId not in opcodeDatabase[opcode]["optionTranslation"]:
        return optionId
    return opcodeDatabase[opcode]["optionTranslation"][optionId]

def getDeoptimizedOptionId(opcode, optionId):
    if "optionTranslation" in opcodeDatabase[opcode]:
        table = flipKeysAndValues(
            opcodeDatabase[opcode]["optionTranslation"]
        )
        if optionId in table:
            return table[optionId]
    if "menus" in opcodeDatabase[opcode]:
        for menuData in opcodeDatabase[opcode]["menus"]:
            if menuData["new"] == optionId:
                return menuData["inner"]
    return optionId

def getBlockType(opcode, defaultNone=False):
    if defaultNone:
        try:
            return opcodeDatabase[opcode]["type"]
        except KeyError:
            return None
    else:
        return opcodeDatabase[opcode]["type"]

def getBlockCategory(opcode):
    return opcodeDatabase[opcode]["category"]

def getMenu(opcode, inputId):
    if "menus" not in opcodeDatabase[opcode]:
        return None
    for menu in opcodeDatabase[opcode]["menus"]:
        if menu["new"] == inputId:
            return menu
    return None

def getInputMagicNumber(inputType):
    return {
        "broadcast"       : 11,
        "text"            : 10,
        "color"           :  9,
        "direction"       :  8,
        "integer"         :  7,
        "positive integer":  6,
        "positive number" :  5,
        "number"          :  4,
    }[inputType] # "boolean" can't occur
    return magicNumber

def getOptionType(opcode, optionId):
    return opcodeDatabase[opcode]["optionTypes"][optionId]

def getOptionTypes(opcode):
    return opcodeDatabase[opcode]["optionTypes"]

def getEmbeddedMenuOpcode(opcode):
    return opcodeDatabase[opcode].get("embeddedMenuOpcode")

def getArgumentOrder(opcode) -> list[tuple[str, str]]:
    newOpcode = getOptimizedOpcode(opcode)
    arguments = getInputModes(opcode) | {optionId: "OPTION" for optionId in getOptionTypes(opcode)}
    # Escape special characters in each argumentId
    escapedArgumentIds = [re.escape(argumentId) for argumentId in arguments.keys()]
    
    # Combine patterns to match each argumentId with surrounding brackets
    pattern = r"[\[\(\{<](?:" + "|".join(escapedArgumentIds) + r")[\]\)\}>]"
    
    # Find all matches in the string
    matches = []
    for match in re.finditer(pattern, newOpcode):
        argumentId = match.group()[1:-1]  # Extract argumentId (remove brackets)
        matches.append((argumentId, match.start()))  # Store argumentId and its index
    
    # Sort matches by their indices
    matches.sort(key=lambda arg: arg[1])
    
    return [(pair[0], arguments[pair[0]]) for pair in matches]


inputDefault = {}
inputBlockDefault = None
inputTextDefault = ""
noteInputTextDefault = "0"
inputBlocksDefault = []
optionDefault = {}
commentDefault = None

inputModes = {
    "direction"       : "block-and-text",
    "integer"         : "block-and-text",
    "positive integer": "block-and-text",
    "positive number" : "block-and-text",
    "number"          : "block-and-text",
    "text"            : "block-and-text",
    "color"           : "block-and-text",

    "note"            : "block-and-menu-text",

    "boolean"         : "block-only",
    "round"           : "block-only",
    "embeddedMenu"    : "block-only",

    "script"          : "script",

    "broadcast"                           : "block-and-broadcast-option",
    
    "stage || other sprite"               : "block-and-option",
    "cloning target"                      : "block-and-option",
    "mouse || other sprite"               : "block-and-option",
    "mouse|edge || other sprite"          : "block-and-option",
    "mouse|edge || myself || other sprite": "block-and-option",
    "key"                                 : "block-and-option",
    "up|down"                             : "block-and-option",
    "finger index"                        : "block-and-option",
    "random|mouse || other sprite"        : "block-and-option",
    "costume"                             : "block-and-option",
    "costume property"                    : "block-and-option",
    "backdrop"                            : "block-and-option",
    "backdrop property"                   : "block-and-option",
    "myself || other sprite"              : "block-and-option",
    "sound"                               : "block-and-option",
    "drum"                                : "block-and-option",
    "instrument"                          : "block-and-option",
    "font"                                : "block-and-option",
    "pen property"                        : "block-and-option",
    "video sensing property"              : "block-and-option",
    "video sensing target"                : "block-and-option",
    "video state"                         : "block-and-option",
    "text to speech voice"                : "block-and-option",
    "text to speech language"             : "block-and-option",
    "translate language"                  : "block-and-option",
    "makey key"                           : "block-and-option",
    "makey sequence"                      : "block-and-option",
    "read file mode"                      : "block-and-option",
    "file selector mode"                  : "block-and-option",
}

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

def getOptimizedOptionValuesUsingContext(optionType, context, inputDatas):
    optionTypeData = optionTypeDatabase[optionType]
    values = []
    for value in optionTypeData["directValues"]:
        if   isinstance(value, list):
            values.append(value)
        else:
            values.append(["value", value])
    for segment in optionTypeData["valueSegments"]:
        match segment:
            case "stage":
                values += [["stage", "stage"]]
            case "myself":
                values += [["myself", "myself"]]
            case "mouse-pointer":
                values += [["object", "mouse-pointer"]]
            case "random position":
                values += [["object", "random position"]]
            case "edge":
                values += [["object", "edge"]]
            
            case "myself if not stage":
                if not context["isStage"]:
                    values += [["myself", "myself"]]
            
            case "other sprite":
                values += context["otherSprites"]
            case "other sprite not stage":
                values += context["otherSprites"]
                if ["stage", "stage"] in values:
                    values.remove(["stage", "stage"])
            case "mutable sprite property":
                # works only for "set [PROPERTY] of ([TARGET]) to (VALUE)"; no other block uses this though
                if inputDatas["TARGET"]["option"] == ["stage", "stage"]:
                    nameKey = None
                else:
                    nameKey = tuple(inputDatas["TARGET"]["option"]) # Tuples used for allowing hashing
                if nameKey == None:
                    values += [["value", "backdrop"], ["value", "volume"]]
                    values += context["globalVariables"]
                else:
                    values += [["value", "x position"], ["value", "y position"], ["value", "direction"], ["value", "costume"], ["value", "size"], ["value", "volume"]]
                    values += context["localVariables"][nameKey]
            case "readable sprite property":
                # works only for "[PROPERTY] of ([TARGET])"; no other block uses this though
                if inputDatas["TARGET"]["option"] == "_stage_":
                    nameKey = None
                else:
                    nameKey = tuple(inputDatas["TARGET"]["option"]) # Tuples used for allowing hashing
                if nameKey == None:
                    values += [["value", "backdrop #"], ["value", "backdrop name"], ["value", "volume"]]
                    values += context["globalVariables"]
                else:
                    values += [["value", "x position"], ["value", "y position"], ["value", "direction"], ["value", "costume #"], ["value", "costume name"], ["value", "layer"], ["value", "size"], ["value", "volume"]]
                    values += context["localVariables"][nameKey]
            case "costume":
                values += context["costumes"]
                values += [["costume", i] for i in range(len(context["costumes"]))]
            case "backdrop":
                values += context["backdrops"]
                values += [["costume", i] for i in range(len(context["costumes"]))]
            case "sound":
                values += context["sounds"]
            case "font":
                pass
    if values == [] and "fallback" in optionTypeData:
        values.append(optionTypeData["fallback"])
    return removeDuplicates(values)

def getOptimizedOptionValuesUsingNoContext(optionType, addSegements:bool=True):
    optionTypeData = optionTypeDatabase[optionType]
    values         = []
    defaultPrefix  = None
    for value in optionTypeData["directValues"]:
        if   isinstance(value, list):
            values.append(value)
        else:
            values.append(["value", value])
    if addSegements:
        for segment in optionTypeData["valueSegments"]:
            match segment:
                case "stage":
                    values += [["stage", "stage"]]
                case "myself":
                    values += [["myself", "myself"]]
                case "mouse-pointer":
                    values += [["object", "mouse-pointer"]]
                case "random position":
                    values += [["object", "random position"]]
                case "edge":
                    values += [["object", "edge"]]
                
                case "myself if not stage":
                    values += [["myself", "myself"]]
                
                case "other sprite":
                    values += [["stage", "stage"]]
                    defaultPrefix = "sprite"
                case "other sprite not stage":
                    defaultPrefix = "sprite"
                case "mutable sprite property":
                    values += [["value", "backdrop"], ["value", "volume"]]
                    values += [["value", "x position"], ["value", "y position"], ["value", "direction"], ["value", "costume"], ["value", "size"]]
                    defaultPrefix = "variable"
                case "readable sprite property":
                    values += [["value", "backdrop #"], ["value", "backdrop name"], ["value", "volume"]]
                    values += [["value", "x position"], ["value", "y position"], ["value", "direction"], ["value", "costume #"], ["value", "costume name"], ["value", "layer"], ["value", "size"]]
                    defaultPrefix = "variable"
                case "costume":
                    # Can't be guessed
                    defaultPrefix = "costume"
                case "backdrop":
                    # Can't be guessed
                    defaultPrefix = "backdrop"
                case "sound":
                    # Can't be guessed
                    defaultPrefix = "sound"
                case "font":
                    defaultPrefix = "font"
    if "fallback" in optionTypeData:
        values.append(optionTypeData["fallback"])
    return removeDuplicates(values), defaultPrefix

def getDeoptimizedOptionValues(optionType):
    optionTypeData = optionTypeDatabase[optionType]
    values = []
    directValues = optionTypeData["oldDirectValues"] if "oldDirectValues" in optionTypeData else optionTypeData["directValues"]
    for value in directValues:
        if   isinstance(value, list):
            values.append(value[0])
        else:
            values.append(value)
    for segment in optionTypeData["valueSegments"]:
        match segment:
            case "stage":
                values += ["_stage_"]
            case "myself":
                values += ["_myself_"]
            case "mouse-pointer":
                values += ["_mouse_"]
            case "random position":
                values += ["_random_"]
            case "edge":
                values += ["_edge_"]
            
            case "myself if not stage":
                values += ["_myself_"]
            
            case "other sprite":
                values += ["_stage_"]
            case "other sprite not stage":
                pass
            case "mutable sprite property":
                values += ["backdrop", "volume"]
                values += ["x position", "y position", "direction", "costume", "size"] #"volume"
            case "readable sprite property":
                values += ["backdrop #", "backdrop name", "volume"]
                values += ["x position", "y position", "direction", "costume #", "costume name", "layer", "size"] #"volume"
            case "costume":
                pass # Can't be guessed
            case "backdrop":
                pass # Can't be guessed
            case "sound":
                pass # Can't be guessed
            case "font":
                pass
    if "fallback" in optionTypeData:
        values.append(optionTypeData["fallback"][1])
    return removeDuplicates(values)

def optimizeOptionValue(optionValue, optionType):
    if optionType in ["broadcast", "reporter name", "opcode", "boolean"]:
        return ["value", optionValue]
    if optionType in ["variable", "list"]:
        return [optionType, optionValue]
    if optionType == "expanded|minimized" and optionValue == "FALSE": # To patch a mistake of the pen extension dev
        optionValue = False
    optimizedValues, defaultPrefix = getOptimizedOptionValuesUsingNoContext(optionType=optionType)
    deoptimizedValues              = getDeoptimizedOptionValues            (optionType=optionType)
    if len(optimizedValues) != len(deoptimizedValues):
        raise Exception()
    
    if optionValue in deoptimizedValues:
        result = optimizedValues[deoptimizedValues.index(optionValue)]
    else:
        if defaultPrefix == None:
            raise Exception()
        result = [defaultPrefix, optionValue]
    return result


def deoptimizeOptionValue(optionValue, optionType, context=None):
    if optionType in ["broadcast", "reporter name", "opcode", "variable", "list", "boolean"]:
        return optionValue[1]
    optimizedValues, defaultPrefix = getOptimizedOptionValuesUsingNoContext(optionType=optionType)
    deoptimizedValues              = getDeoptimizedOptionValues            (optionType=optionType)
    if len(optimizedValues) != len(deoptimizedValues):
        raise Exception()
    
    if optionType in ["costume", "backdrop"] and isinstance(optionValue[1], int):
        names = context["costumes"] if optionType=="costumes" else context["backdrops"]
        if names == []: names = [defaultCostume["name"]]
        return names[optionValue[1]]
    elif optionValue in optimizedValues:
        return deoptimizedValues[optimizedValues.index(optionValue)]
    else:
        return optionValue[1]

def autocompleteOptionValue(optionValue, optionType):
    if optionType in ["broadcast", "reporter name", "opcode", "boolean"]:
        return ["value", optionValue]
    if optionType in ["variable", "list"]:
        return [optionType, optionValue]
    directValues, _ = getOptimizedOptionValuesUsingNoContext(
        optionType=optionType,
        addSegements=False,
    )
    secondaryDirectValues = [value[1] for value in directValues]
    allValues, defaultPrefix =  getOptimizedOptionValuesUsingNoContext(
        optionType=optionType,
        addSegements=True,
    )
    secondaryAllValues = [value[1] for value in allValues]
    if   optionValue in secondaryDirectValues:
        result = directValues[secondaryDirectValues.index(optionValue)]
    elif optionValue in secondaryAllValues:
        result = allValues[secondaryAllValues.index(optionValue)]
    else:
        if defaultPrefix == None: raise Exception()
        result = [defaultPrefix, optionValue]
    return result

def getOptionValueDefault(optionType):
    possibleValues, _ = getOptimizedOptionValuesUsingNoContext(optionType=optionType)
    if possibleValues==[] and optionType in ["costume", "backdrop"]:
        return [optionType, 0] # the first costume is the default
    assert len(possibleValues) > 0, "No default option value found."
    return possibleValues[0]
        

defaultCostume = {
    "name": "empty costume",
    "extension": "svg",
    "bitmapResolution": 1,
    "rotationCenter": [0, 0]
}

defaultCostumeDeoptimized = {
    "name": "empty costume",
    "bitmapResolution": 1,
    "assetId": "cd21514d0531fdffb22204e0ec5ed84a",
    "dataFormat": "svg",
    "md5ext": "cd21514d0531fdffb22204e0ec5ed84a.svg",
    "rotationCenterX": 0,
    "rotationCenterY": 0
}

defaultCostumeFilePath = "assets/defaultCostume.svg"

defaultStage = {
    "name": "Stage",
    "isStage": True,
    "scripts": [],
    "comments": [],
    "currentCostume": 0,
    "costumes": [],
    "sounds": [],
    "volume": 100,
}

defaultSprite = {
    "name": "Sprite1", 
    "isStage": False, 
    "scripts": [], 
    "comments": [], 
    "currentCostume": 0, 
    "costumes": [], 
    "sounds": [], 
    "volume": 100, 
    "layerOrder": 1, 
    "visible": True, 
    "position": [0,0], 
    "size": 100, 
    "direction": 90, 
    "draggable": True, 
    "rotationStyle": "all around", 
    "localVariables": [], 
    "localLists": [],
}

defaultProject = {
    "sprites": [
        defaultStage,
        defaultSprite,
    ],
    "globalVariables": [{"name": "my variable", "currentValue": "", "isCloudVariable": False}],
    "globalLists": [],
    "monitors": [],
    "extensions": [],
}
