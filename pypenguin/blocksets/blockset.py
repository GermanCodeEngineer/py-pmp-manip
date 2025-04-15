class BlockSet:
    _grepr = True
    _grepr_fields = ["name", "blocks"]
    
    name: str
    blocks: dict[str, "BlockData"]
    
    def __init__(self, name: str, blocks: dict[str, "BlockData"]):
        self.name   = name
        self.blocks = blocks

class BlockData:
    _grepr = True
    _grepr_fields = ["block_type", "new_opcode", "inputs", "dropdowns", "can_have_monitor"]
    
    block_type: str
    new_opcode: str
    inputs: dict[str, "InputData"]
    dropdowns: dict[str, "DropdownData"]
    can_have_monitor: bool
    
    
    def __init__(self, 
        block_type: str, 
        new_opcode: str, 
        inputs: dict[str, "InputData"] = {},
        dropdowns: dict[str, "DropdownData"] = {},
        can_have_monitor: bool = False
    ):
        self.block_type       = block_type
        self.new_opcode       = new_opcode
        self.inputs           = inputs
        self.dropdowns        = dropdowns
        self.can_have_monitor = can_have_monitor

from enum import Enum

class InputType(Enum):
    # block-and-text
    DIRECTION           = "direction"
    INTEGER             = "integer"
    POSITIVE_INTEGER    = "positive integer"
    POSITIVE_NUMBER     = "positive number"
    NUMBER              = "number"
    TEXT                = "text"
    COLOR               = "color"

    # block-and-menu-text
    NOTE                = "note"

    # block-only
    BOOLEAN             = "boolean"
    ROUND               = "round"
    EMBEDDED_MENU       = "embeddedMenu"

    # script
    SCRIPT              = "script"

    # block-and-broadcast-option
    BROADCAST           = "broadcast"

    # block-and-option
    STAGE_OR_OTHER_SPRITE               = "stage || other sprite"
    CLONING_TARGET                      = "cloning target"
    MOUSE_OR_OTHER_SPRITE               = "mouse || other sprite"
    MOUSE_EDGE_OR_OTHER_SPRITE          = "mouse|edge || other sprite"
    MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE   = "mouse|edge || myself || other sprite"
    KEY                                 = "key"
    UP_DOWN                             = "up|down"
    FINGER_INDEX                        = "finger index"
    RANDOM_MOUSE_OR_OTHER_SPRITE        = "random|mouse || other sprite"
    COSTUME                             = "costume"
    COSTUME_PROPERTY                    = "costume property"
    BACKDROP                            = "backdrop"
    BACKDROP_PROPERTY                   = "backdrop property"
    MYSELF_OR_OTHER_SPRITE              = "myself || other sprite"
    SOUND                               = "sound"
    DRUM                                = "drum"
    INSTRUMENT                          = "instrument"
    FONT                                = "font"
    PEN_PROPERTY                        = "pen property"
    VIDEO_SENSING_PROPERTY              = "video sensing property"
    VIDEO_SENSING_TARGET                = "video sensing target"
    VIDEO_STATE                         = "video state"
    TEXT_TO_SPEECH_VOICE                = "text to speech voice"
    TEXT_TO_SPEECH_LANGUAGE             = "text to speech language"
    TRANSLATE_LANGUAGE                  = "translate language"
    MAKEY_KEY                           = "makey key"
    MAKEY_SEQUENCE                      = "makey sequence"
    READ_FILE_MODE                      = "read file mode"
    FILE_SELECTOR_MODE                  = "file selector mode"

class InputData:
    _grepr = True
    _grepr_fields = ["type", "old", "menu"]
    
    type: str
    old: str
    menu: "MenuData | None"
    
    def __init__(self, type: str, old: str, menu: "MenuData|None" = None):
        self.type = type
        self.old  = old
        self.menu = menu

class DropdownData:
    _grepr = True
    _grepr_fields = ["type", "old"]
    
    type: str
    old: str
    
    def __init__(self, type: str, old: str):
        self.type = type
        self.old  = old

class MenuData:
    _grepr = True
    _grepr_fields = ["opcode", "inner"]
    
    opcode: str
    inner : str
    
    def __init__(self, opcode: str, inner: str):
        self.opcode = opcode
        self.inner  = inner
