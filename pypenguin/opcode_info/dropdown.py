from typing      import TYPE_CHECKING
from dataclasses import dataclass, field

from utility import PypenguinEnum, remove_duplicates

if TYPE_CHECKING:
    from core.block import SRInputValue
from core.dropdown import SRDropdownKind, SRDropdownValue
from core.context import PartialContext, FullContext

@dataclass
class DropdownInfo:
    _grepr = True
    _grepr_fields = ["type"]
    
    type: "DropdownType"

class DropdownBehaviour(PypenguinEnum):
    def get_default_kind(self) -> "SRDropdownKind | None":
        from core.dropdown import SRDropdownKind
        return {
            DropdownBehaviour.OTHER_SPRITE             : SRDropdownKind.SPRITE,
            DropdownBehaviour.OTHER_SPRITE_EXCEPT_STAGE: SRDropdownKind.SPRITE,
            DropdownBehaviour.MUTABLE_SPRITE_PROPERTY  : SRDropdownKind.VARIABLE,
            DropdownBehaviour.READABLE_SPRITE_PROPERTY : SRDropdownKind.VARIABLE,
            DropdownBehaviour.COSTUME                  : SRDropdownKind.COSTUME,
            DropdownBehaviour.BACKDROP                 : SRDropdownKind.BACKDROP,
            DropdownBehaviour.SOUND                    : SRDropdownKind.SOUND,
            DropdownBehaviour.VARIABLE                 : SRDropdownKind.VARIABLE,
            DropdownBehaviour.LIST                     : SRDropdownKind.LIST,
            DropdownBehaviour.BROADCAST                : SRDropdownKind.BROADCAST_MSG,
            DropdownBehaviour.FONT                     : SRDropdownKind.FONT,
        }.get(self, None)

    STAGE                     =  0
    OTHER_SPRITE              =  1
    OTHER_SPRITE_EXCEPT_STAGE =  2
    MYSELF                    =  3
    MYSELF_IF_SPRITE          =  4

    MOUSE_POINTER             =  5
    EDGE                      =  6

    RANDOM_POSITION           =  7

    MUTABLE_SPRITE_PROPERTY   =  8
    READABLE_SPRITE_PROPERTY  =  9

    COSTUME                   = 10
    BACKDROP                  = 11
    SOUND                     = 12

    VARIABLE                  = 13
    LIST                      = 14
    BROADCAST                 = 15
    
    FONT                      = 16

DDB = DropdownBehaviour    

@dataclass
class DropdownTypeInfo:
    _grepr = True
    _grepr_fields = ["direct_values", "behaviours", "old_direct_values", "fallback"]

    direct_values:     list[str | int | bool]  = field(default_factory=list)
    behaviours:        list[DropdownBehaviour] = field(default_factory=list)
    old_direct_values: list[str | int | bool] | None = None  
    fallback:          SRDropdownValue        | None = None
    
    def __post_init__(self):
        if self.old_direct_values is None:
            self.old_direct_values = self.direct_values        
    
class DropdownType(PypenguinEnum):    
    def get_type_info(self) -> DropdownTypeInfo:
        return self.value
    
    def get_default_kind(self) -> SRDropdownKind | None:
        default_kind = None
        for behaviour in self.get_type_info().behaviours:
            behaviour_default_kind = behaviour.get_default_kind()
            if behaviour_default_kind is not None:
                if default_kind is None:
                    default_kind = behaviour_default_kind
                else:
                    raise ValueError(f"Multiple default kinds for {self}: {default_kind} and {behaviour_default_kind}")
        return default_kind

    def calculate_possible_new_dropdown_values(self, context: PartialContext|FullContext) -> list[SRDropdownValue]:
        dropdown_type_info = self.get_type_info()
        values: list[SRDropdownValue] = []
        for value in dropdown_type_info.direct_values:
            if   isinstance(value, SRDropdownValue):
                values.append(value)
            else:
                values.append(SRDropdownValue(SRDropdownKind.STANDARD, value))
        
        for segment in dropdown_type_info.behaviours:
            match segment:
                case DDB.STAGE:
                    values.append(SRDropdownValue(SRDropdownKind.STAGE, "stage"))
                case DDB.OTHER_SPRITE:
                    values.append(SRDropdownValue(SRDropdownKind.STAGE, "stage"))
                    values.extend(context.other_sprites)
                case DDB.OTHER_SPRITE_EXCEPT_STAGE:
                    values.extend(context.other_sprites)
                case DDB.MYSELF:
                    values.append(SRDropdownValue(SRDropdownKind.MYSELF, "myself"))
                case DDB.MYSELF_IF_SPRITE:
                    if not context.is_stage:
                        values.append(SRDropdownValue(SRDropdownKind.MYSELF, "myself"))
                
                case DDB.MOUSE_POINTER:
                    values.append(SRDropdownValue(SRDropdownKind.OBJECT, "mouse-pointer"))
                case DDB.EDGE:
                    values.append(SRDropdownValue(SRDropdownKind.OBJECT, "edge"))
                
                case DDB.RANDOM_POSITION:
                    values.append(SRDropdownValue(SRDropdownKind.OBJECT, "random position"))
                
                case DDB.MUTABLE_SPRITE_PROPERTY:
                    # works only for "set [PROPERTY] of ([TARGET]) to (VALUE)"; no other block uses this though
                    # TODO: possibly add special case
                    #if inputs["TARGET"].dropdown == SRDropdownValue(SRDropdownKind.STAGE, "stage"):
                    #    values.extend([
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "backdrop"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                    #    ])
                    #else:
                    #    values.extend([
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "x position"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "y position"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "direction"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "costume"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "size"),
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                    #    ])
                    #    name_key = inputs["TARGET"].dropdown.value
                    #    values.extend(context.sprite_only_variables[name_key])
                    
                    # trying to validate here is so much additional work and makes everything a lot more complicated.
                    # instead i will choose the lazy way here
                    values.extend([
                        SRDropdownValue(SRDropdownKind.STANDARD, "backdrop"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                    ])
                    values.extend([
                        SRDropdownValue(SRDropdownKind.STANDARD, "x position"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "y position"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "direction"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "costume"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "size"),
                        SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                    ])
                    for sprite_only_variables in context.sprite_only_variables.values():
                        values.extend(sprite_only_variables)

                    raise Exception("TODO: ensure this works")
                
                case DDB.READABLE_SPRITE_PROPERTY:
                    # works only for "[PROPERTY] of ([TARGET])"; no other block uses this though
                    #if inputs["TARGET"].dropdown == SRDropdownValue(SRDropdownKind.STAGE, "stage"):
                    #    values.extend([
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "backdrop #"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "backdrop name"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                    #    ])
                    #    values.extend(context.all_sprite_variables)
                    #else:
                    #    values.extend([
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "x position"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "y position"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "direction"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "costume #"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "costume name"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "layer"), 
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "size"),
                    #        SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                    #    ])
                    #    name_key = inputs["TARGET"].dropdown.value
                    #    values.extend(context.sprite_only_variables[name_key])
                    
                    # trying to validate here is so much additional work and makes everything a lot more complicated.
                    # instead i will choose the lazy way here

                    values.extend([
                        SRDropdownValue(SRDropdownKind.STANDARD, "backdrop #"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "backdrop name"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                    ])
                    values.extend(context.all_sprite_variables)
                    values.extend([
                        SRDropdownValue(SRDropdownKind.STANDARD, "x position"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "y position"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "direction"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "costume #"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "costume name"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "layer"), 
                        SRDropdownValue(SRDropdownKind.STANDARD, "size"),
                        SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                    ])
                    for sprite_only_variables in context.sprite_only_variables.values():
                        values.extend(sprite_only_variables)

                case DDB.COSTUME:
                    values.extend(context.costumes)
                    values.extend([SRDropdownValue(SRDropdownKind.COSTUME, i) for i in range(len(context.costumes))])
                case DDB.BACKDROP:
                    values.extend(context.backdrops)
                    values.extend([SRDropdownValue(SRDropdownKind.COSTUME, i) for i in range(len(context.backdrops))])
                case DDB.SOUND:
                    values.extend(context.sounds)
                case DDB.SOUND:
                    pass
        if (values == []) and (dropdown_type_info.fallback is not None):
            values.append(dropdown_type_info.fallback.value)
        return remove_duplicates(values)

    def guess_possible_new_dropdown_values(self, include_behaviours: bool) -> list[SRDropdownValue]:
        dropdown_type_info = self.get_type_info()
        values             = []
        for value in dropdown_type_info.direct_values:
            if   isinstance(value, SRDropdownValue):
                values.append(value)
            else:
                values.append(SRDropdownValue(SRDropdownKind.STANDARD, value))
        
        if include_behaviours:
            for behaviour in dropdown_type_info.behaviours:
                match behaviour:
                    case DDB.STAGE:
                        values.append(SRDropdownValue(SRDropdownKind.STAGE, "stage"))
                    case DDB.OTHER_SPRITE:
                        values.append(SRDropdownValue(SRDropdownKind.STAGE, "stage"))
                    case DDB.OTHER_SPRITE_EXCEPT_STAGE:
                        pass # Can't be guessed, but don't include stage
                    case DDB.MYSELF:
                        values.append(SRDropdownValue(SRDropdownKind.MYSELF, "myself"))
                    case DDB.MYSELF_IF_SPRITE:
                        values.append(SRDropdownValue(SRDropdownKind.MYSELF, "myself"))
                    
                    case DDB.MOUSE_POINTER:
                        values.append(SRDropdownValue(SRDropdownKind.OBJECT, "mouse-pointer"))
                    case DDB.EDGE:
                        values.append(SRDropdownValue(SRDropdownKind.OBJECT, "edge"))
                    
                    case DDB.RANDOM_POSITION:
                        values.append(SRDropdownValue(SRDropdownKind.OBJECT, "random position"))
                    
                    case DDB.MUTABLE_SPRITE_PROPERTY:
                        values.extend([
                            SRDropdownValue(SRDropdownKind.STANDARD, "backdrop"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                        ])
                        values.extend([
                            SRDropdownValue(SRDropdownKind.STANDARD, "x position"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "y position"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "direction"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "costume"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "size"),
                            SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                        ])
                    case DDB.READABLE_SPRITE_PROPERTY:
                        values.extend([
                            SRDropdownValue(SRDropdownKind.STANDARD, "backdrop #"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "backdrop name"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                        ])
                        values.extend([
                            SRDropdownValue(SRDropdownKind.STANDARD, "x position"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "y position"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "direction"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "costume #"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "costume name"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "layer"), 
                            SRDropdownValue(SRDropdownKind.STANDARD, "size"),
                            SRDropdownValue(SRDropdownKind.STANDARD, "volume"),
                        ])
                    
                    case (DDB.COSTUME  | DDB.BACKDROP | DDB.SOUND 
                        | DDB.VARIABLE | DDB.LIST     | DDB.BROADCAST | DDB.FONT):
                        pass # Can't be guessed

                    case _: raise ValueError()
        if dropdown_type_info.fallback is not None:
            values.append(dropdown_type_info.fallback)
        return remove_duplicates(values)

    def guess_possible_old_dropdown_values(self) -> list[str]:
        dropdown_type_info = self.get_type_info()
        values = []
        for value in dropdown_type_info.old_direct_values:
            if isinstance(value, SRDropdownValue):
                values.append(value[0])
            else:
                values.append(value)
        for behaviour in dropdown_type_info.behaviours:
            match behaviour:
                case DDB.STAGE:
                    values.append("_stage_")
                case DDB.OTHER_SPRITE:
                    values.append("_stage_")
                case DDB.OTHER_SPRITE_EXCEPT_STAGE:
                    pass
                case DDB.MYSELF:
                    values.append("_myself_")
                case DDB.MYSELF_IF_SPRITE:
                    values.append("_myself_")
                
                case DDB.MOUSE_POINTER:
                    values.append("_mouse_")
                case DDB.EDGE:
                    values.append("_edge_")
                
                case DDB.RANDOM_POSITION:
                    values.append("_random_")
                
                
                case DDB.MUTABLE_SPRITE_PROPERTY:
                    values.extend(["backdrop", "volume"])
                    values.extend(["x position", "y position", "direction", "costume", "size", "volume"])
                case DDB.READABLE_SPRITE_PROPERTY:
                    values.extend(["backdrop #", "backdrop name", "volume"])
                    values.extend(["x position", "y position", "direction", "costume #", "costume name", "layer", "size", "volume"])
                
                case (DDB.COSTUME  | DDB.BACKDROP | DDB.SOUND 
                    | DDB.VARIABLE | DDB.LIST     | DDB.BROADCAST | DDB.FONT):
                        pass # Can't be guessed
                case _: raise ValueError()
        if dropdown_type_info.fallback is not None:
            values.append(dropdown_type_info.fallback.value)
        return remove_duplicates(values)

    def translate_old_to_new_value(self, old_value: str) -> SRDropdownValue:
        # TODO: add special case for this
        if self == DropdownType.EXPANDED_MINIMIZED and old_value == "FALSE": # To patch a mistake of the pen extension dev
            old_value = False
        new_values = self.guess_possible_new_dropdown_values(include_behaviours=True)
        old_values = self.guess_possible_old_dropdown_values()
        default_kind = self.get_default_kind()
        
        assert len(new_values) == len(old_values)
        
        if old_value in old_values:
            return new_values[old_values.index(old_value)]
        else:
            assert default_kind is not None
            return SRDropdownValue(default_kind, old_value)

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
    STAGE_OR_OTHER_SPRITE = DropdownTypeInfo(behaviours=[DDB.STAGE, DDB.OTHER_SPRITE])
    CLONING_TARGET = DropdownTypeInfo(
        behaviours=[DDB.MYSELF_IF_SPRITE, DDB.OTHER_SPRITE_EXCEPT_STAGE],
        fallback=SRDropdownValue(SRDropdownKind.FALLBACK, " "),
    )
    UP_DOWN = DropdownTypeInfo(direct_values=["up", "down"])
    LOUDNESS_TIMER = DropdownTypeInfo(
        direct_values=["loudness", "timer"],
        old_direct_values=["LOUDNESS", "TIMER"],
    )
    MOUSE_OR_OTHER_SPRITE = DropdownTypeInfo(behaviours=[DDB.MOUSE_POINTER, DDB.OTHER_SPRITE])
    MOUSE_EDGE_OR_OTHER_SPRITE = DropdownTypeInfo(behaviours=[DDB.MOUSE_POINTER, DDB.EDGE, DDB.OTHER_SPRITE])
    MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE = DropdownTypeInfo(behaviours=[DDB.MOUSE_POINTER, DDB.EDGE, DDB.MYSELF, DDB.OTHER_SPRITE])
    X_OR_Y = DropdownTypeInfo(direct_values=["x", "y"])
    DRAG_MODE = DropdownTypeInfo(direct_values=["draggable", "not draggable"])
    MUTABLE_SPRITE_PROPERTY = DropdownTypeInfo(behaviours=[DDB.MUTABLE_SPRITE_PROPERTY])
    READABLE_SPRITE_PROPERTY = DropdownTypeInfo(behaviours=[DDB.READABLE_SPRITE_PROPERTY])
    TIME_PROPERTY = DropdownTypeInfo(
        direct_values=["year", "month", "date", "day of week", "hour", "minute", "second", "js timestamp"],
        old_direct_values=["YEAR", "MONTH", "DATE", "DAYOFWEEK", "HOUR", "MINUTE", "SECOND", "TIMESTAMP"],
    )
    FINGER_INDEX = DropdownTypeInfo(direct_values=["1", "2", "3", "4", "5"])
    RANDOM_MOUSE_OR_OTHER_SPRITE = DropdownTypeInfo(behaviours=[DDB.RANDOM_POSITION, DDB.MOUSE_POINTER, DDB.OTHER_SPRITE])
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
    COSTUME = DropdownTypeInfo(behaviours=[DDB.COSTUME])
    BACKDROP = DropdownTypeInfo(behaviours=[DDB.BACKDROP])
    COSTUME_PROPERTY = DropdownTypeInfo(direct_values=["width", "height", "rotation center x", "rotation center y", "drawing mode"])
    MYSELF_OR_OTHER_SPRITE = DropdownTypeInfo(behaviours=[DDB.MYSELF, DDB.OTHER_SPRITE])
    FRONT_BACK = DropdownTypeInfo(direct_values=["front", "back"])
    FORWARD_BACKWARD = DropdownTypeInfo(direct_values=["forward", "backward"])
    INFRONT_BEHIND = DropdownTypeInfo(direct_values=["infront", "behind"])
    NUMBER_NAME = DropdownTypeInfo(direct_values=["number", "name"])
    SOUND = DropdownTypeInfo(
        behaviours=[DDB.SOUND], 
        fallback=SRDropdownValue(SRDropdownKind.FALLBACK, " "),
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
        direct_values=[SRDropdownValue(SRDropdownKind.SUGGESTED_FONT, name) for name in ["Sans Serif", "Serif", "Handwriting", "Marker", "Curly", "Pixel", "Playful", "Bubbly", "Arcade", "Bits and Bytes", "Technological", "Scratch", "Archivo", "Archivo Black", "Random"]],
        old_direct_values=["Sans Serif", "Serif", "Handwriting", "Marker", "Curly", "Pixel", "Playful", "Bubbly", "Arcade", "Bits and Bytes", "Technological", "Scratch", "Archivo", "Archivo Black", "Random"],
        behaviours=[DDB.FONT],
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

    
    BROADCAST = DropdownTypeInfo(behaviours=[DDB.BROADCAST])
    VARIABLE = DropdownTypeInfo(behaviours=[DDB.VARIABLE])
    LIST = DropdownTypeInfo(behaviours=[DDB.LIST])
    
    # Temporary, will be removed
    ENABLE_SCREEN_REFRESH = DropdownTypeInfo()
