from database import getAllMonitorOpcodes
from validate.errors import *

allowedMenuOpcodes = getAllMonitorOpcodes()
textToSpeechLanguages = [
    None,
    "Arabic (ar)", "Chinese (Mandarin) (zh-cn)", "Danish (da)", "Dutch (nl)", "English (en)", 
    "French (fr)", "German (de)", "Hindi (hi)", "Icelandic (is)", "Italian (it)", 
    "Japanese (ja)", "Korean (ko)", "Norwegian (nb)", "Polish (pl)", "Portuguese (Brazilian) (pt-br)", 
    "Portuguese (pt)", "Romanian (ro)", "Russian (ru)", "Spanish (es)", "Spanish (Latin American) (es-419)", 
    "Swedish (sv)", "Turkish (tr)", "Welsh (cy)"
]

projectSchema = {
    "type": "object",
    "properties": {
        "sprites": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
                "required": ["name"],
            },
        },
        "globalVariables": {
            "type": "array",
        },
        "globalLists": {
            "type": "array",
        },
        "monitors": {"type": "array"},
        "extensions": {"type": "array", "items": {"type": "string"}},
        "tempo": {"type": "integer", "minimum": 20, "maximum": 500},
        "videoTransparency": {"type": "number"},
        "videoState": {"type": "string", "enum": ["on", "on flipped", "off"]},
        "textToSpeechLanguage": {
            "type": ["null", "string"],
            "enum": textToSpeechLanguages,
        },
        "extensionData": {"type": "object"},
        "extensionURLs": {"type": "object"},
    },
    "required": [
        "sprites",
        "globalVariables",
        "globalLists",
        "monitors",
        "extensions",
        #"tempo",
        #"videoTransparency",
        #"videoState",
        #"textToSpeechLanguage",
        #"extensionData",
        ###"extensionURLs",
    ],
}

spriteSchema = {
    "type": "object",
    "properties": {
        "isStage": {"type": "boolean", "const": False},
        "name": {"type": "string", "minLength": 1},
        "scripts": {"type": "array"},
        "comments": {"type": "array"},
        "currentCostume": {"type": "integer", "minimum": 0},
        "costumes": {"type": "array"},
        "sounds": {
            "type": "array",
        },
        "volume": {"type": "number", "minimum": 0, "maximum": 100},
        "localVariables": {"type": "array"},
        "localLists": {"type": "array"},
        "layerOrder": {"type": "integer", "minimum": 1},
        "visible": {"type": "boolean"},
        "position": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "size": {"type": "number", "minimum": 0},
        "direction": {"type": "number"},
        "draggable": {"type": "boolean"},
        "rotationStyle": {
            "type": "string",
            "enum": ["all around", "left-right", "don't rotate"],
        },
    },
    "required": [
        "isStage",
        "name",
        "scripts",
        "comments",
        "currentCostume",
        "costumes",
        "sounds",
        "volume",
        "layerOrder",
        "visible",
        "position",
        "size",
        "direction",
        "draggable",
        "rotationStyle",
        "localVariables",
        "localLists",
    ],
}

stageSchema = {
    "type": "object",
    "properties": {
        "isStage": {"type": "boolean", "const": True},
        "name": {"type": "string", "const": "Stage"},
        "scripts": {"type": "array"},
        "comments": {"type": "array"},
        "currentCostume": {"type": "integer", "minimum": 0},
        "costumes": {"type": "array"},
        "sounds": {"type": "array"},
        "volume": {"type": "number", "minimum": 0, "maximum": 100},
    },
    "required": [
        "isStage",
        "name",
        "scripts",
        "comments",
        "currentCostume",
        "costumes",
        "sounds",
        "volume",
    ],
}

scriptSchema = {
    "type": "object",
    "properties": {
        "position": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "blocks": {
            "type": "array",
            "items": {"type": "object"}, 
            "minItems": 1,
        },
    },
    "required": ["position", "blocks"],
} # ACNH

costumeSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "extension": {"type": "string"},
        "bitmapResolution": {"type": "integer", "minimum": 1},
        "rotationCenter": {
            "type": "array",
            "items": {"type": ["integer", "number"]},
            "minItems": 2,
            "maxItems": 2,
        },
    },
    "required": [
        "name",
        "extension",
        "bitmapResolution",
        "rotationCenter",
    ],
    "additionalProperties": False,
}

soundSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "extension": {"type": "string"},
        #"rate": {"type": "integer", "minimum": 1},
        #"sampleCount": {"type": "integer", "minimum": 1},
    },
    "required": ["name", "extension"], #"rate", "sampleCount"
}

blockSchema = {
    "type": "object",
    "properties": {
        "opcode": {"type": "string"},
        "inputs": {
            "type": "object",
            "patternProperties": {".+": {"type": "object"}},
            "additionalProperties": False,
        },
        "options": {
            "type": "object",
            "patternProperties": {".+": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
            }},
            "additionalProperties": False,
        },
        "comment": {"type": ["null", "object"]},
    },
    "required": ["opcode", "inputs", "options", "comment"],
}

commentSchema = {
    "type": "object",
    "properties": {
        "position": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "size": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "isMinimized": {"type": "boolean"},
        "text": {"type": "string"},
    },
    "required": ["position", "size", "isMinimized", "text"],
}

inputSchema = {
    "type": "object",
    "properties": {
        "mode": {
            "type": "string",
            "enum": [
                "block-only",
                "block-and-text",
                "block-and-menu-text",
                "script",
                "block-and-option",
                "block-and-broadcast-option",
            ],
        },
        "block": {"type": ["null", "object"]},
        "text": {"type": "string"},
        "option": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
        },
        "blocks": {"type": "array", "items": {"type": "object"}},
    },
    "required": ["mode"],
}

variableSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "currentValue": {"type": ["string", "number"]},
        "isCloudVariable": {"type": "boolean"},
    },
    "required": ["name", "currentValue"],
}

listSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "currentValue": {
            "type": "array",
            "items": {"type": ["string", "number"]},
        },
    },
    "required": ["name", "currentValue"],
}

monitorSchema = {
    "type": "object",
    "properties": {
        "opcode": {"type": "string", "enum": allowedMenuOpcodes},
        "options": {"type": "object"},
        "spriteName": {"type": ["string", "null"]},
        "size": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "position": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "visible": {"type": "boolean"},
        "sliderMin": {"type": "number"},
        "sliderMax": {"type": "number"},
        "onlyIntegers": {"type": "boolean"},
    },
    "required": ["opcode", "options", "spriteName", "position", "visible"],
}

from jsonschema import validate, exceptions


def validateSchema(pathToData, data, schema):
    from pypenguin_old.utility import pp

    try:
        validate(instance=data, schema=schema)
        error = None
    except exceptions.ValidationError as err:
        # Custom error message
        errorPath = list(map(str, pathToData + list(err.absolute_path)))
        error = formatError(ValidationError, errorPath, err.message)
        del err.schema
        pp(err.__dict__)
    if error != None:
        raise error

MAIN_DOCS            = "main"
SPRITE_DOCS          = "sprites"
VARIABLES_LISTS_DOCS = "variables_lists"
MONITOR_DOCS         = "monitors"
OTHER_DOCS           = "other"

SCRIPT_DOCS          = "scripts"
COMMENT_DOCS         = "comments"

OPCODE_DOCS          = "(SOON)"

def getHelpLink(path):
    def combine(file, section):
        #string = f"github.com/Fritzforcode/pypenguin_old/blob/main/docs/{file}.md"
        string = f"docs/{file}.md"
        if section != None:
            string += "#" + section
        return string
    if path == []:
        return combine(file=MAIN_DOCS, section=None)
    
    def getHelpLinkForBlocks(subPath, isNested: bool):
        file, section = None, None
        if len(subPath) == 0: # []
            if isNested:
                file    = SCRIPT_DOCS
                section = "what-inputs-look-like" 
            else:
                file = SCRIPT_DOCS
        if len(subPath) >= 1: #eg. [2]
            return getHelpLinkForBlock(subPath=subPath[1:])
        return file, section
    
    def getHelpLinkForBlock(subPath):
        file, section = None, None
        if len(subPath) == 0: # []
            return SCRIPT_DOCS, "what-a-block-looks-like"
        else:
            primary = subPath[0]
            if   primary == "opcode":
                file = OPCODE_DOCS
            elif primary == "inputs":
                pass
            elif primary == "options":
                pass
            elif primary == "comment":
                pass
            
        return file, section
    
    primary = path[0]
    
    file    = None
    section = None
    if   primary == "sprites":
        if len(path) == 1: # ["sprites"]
            return combine(file=SPRITE_DOCS, section=None)
        if len(path) == 2: # eg. ["sprites", 0]
            return combine(file=SPRITE_DOCS, section=None)
        
        secondary = path[2]
        if   secondary in ["isStage", "name", "volume", "currentCostume", "layerOrder", "visible", "position", "size", "direction", "draggable", "rotationStyle"]:
            file = SPRITE_DOCS
        
        elif secondary == "scripts"       :
            if len(path) == 3: #eg. ["sprites", 0, "scripts"]
                return combine(file=SPRITE_DOCS, section=None)
            if len(path) == 4: #eg. ["sprites", 0, "scripts", 1]
                return combine(file=SCRIPT_DOCS, section=None)
            
            tertiary = path[4]
            if   tertiary == "position":
                file = SCRIPT_DOCS
            elif tertiary == "blocks":
                # eg. ["sprites", 0, "scripts", 1, "blocks", ...] -> [...]
                file, section = getHelpLinkForBlocks(subPath=path[5:], isNested=False)
                
        elif secondary == "comments"      :
            if len(path) == 3: #eg. ["sprites", 0, "comments"]
                return combine(file=SPRITE_DOCS, section=None)
            file = COMMENT_DOCS
            
        elif secondary == "costumes"      :
            if len(path) == 3: #eg. ["sprites", 0, "costumes"]
                return combine(file=SPRITE_DOCS, section=None)
        elif secondary == "sounds"        :
            if len(path) == 3: #eg. ["sprites", 0, "sounds"]
                return combine(file=SPRITE_DOCS, section=None)
                
        elif secondary == "localVariables":
            if len(path) == 3: #eg. ["sprites", 0, "localVariables"]
                return combine(file=SPRITE_DOCS, section=None)
            file    = VARIABLES_LISTS_DOCS
            section = "what-a-variable-definition-looks-like"
        elif secondary == "localLists"    :
            if len(path) == 3: #eg. ["sprites", 0, "localVariables"]
                return combine(file=SPRITE_DOCS, section=None)
            file    = VARIABLES_LISTS_DOCS
            section = "what-a-variable-definition-looks-like"
    
    elif primary == "globalVariables":
        if len(path) == 1:
            return combine(file=MAIN_DOCS, section=None)
        file = VARIABLES_LISTS_DOCS
        section = "what-a-variable-definition-looks-like"
    elif primary == "globalLists":
        if len(path) == 1:
            return combine(file=MAIN_DOCS, section=None)
        file = VARIABLES_LISTS_DOCS
        section = "what-a-list-definition-looks-like"
    elif primary == "monitors":
        file = MONITOR_DOCS
    elif primary == "extensions":
        if len(path) == 1:
            return combine(file=MAIN_DOCS, section=None)
        file = OTHER_DOCS
        section = "extensions"
    elif primary == "tempo":
        pass # Needs completion
    elif primary == "videoTransparency":
        pass # Needs completion
    elif primary == "videoState":
        pass # Needs completion
    elif primary == "textToSpeechLanguage":
        pass # Needs completion
    elif primary == "extensionData":
        pass # Needs completion
    elif primary == "extensionURLs":
        pass # Needs completion
    
    if file != None:
        return combine(file, section)
    print(100*"NO HELP GIVEN ----- ")

def formatError(cls, path, message):
    path = [str(i) for i in path]  # Convert all indexes to string
    if path == []:
        pathString = ""
    else:
        pathString = "at [" + "/".join(path) + "] - "
    link = getHelpLink(path=path)
    return cls(f"{pathString}HELP: {link} - ERROR: {message}")
