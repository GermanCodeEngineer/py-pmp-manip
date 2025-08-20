from dataclasses import field
from typing      import TypeVar, Callable

from pmp_manip.utility import grepr_dataclass, remove_duplicates, GEnum, MANIP_BlameDevsError

from pmp_manip.core.context import PartialContext, CompleteContext


DROPDOWN_VALUE_T = str | int

class DropdownValueKind(GEnum):
    """
    The kind of a dropdown value clarifies what it references. Eg. VARIABLE shows that the dropdown value is referencing a variable
    """
    STANDARD       =  0
    SUGGESTION     =  1
    FALLBACK       =  2

    VARIABLE       =  3
    LIST           =  4
    BROADCAST_MSG  =  5
    
    STAGE          =  6
    SPRITE         =  7
    MYSELF         =  8
    OBJECT         =  9

    COSTUME        = 10
    BACKDROP       = 11
    SOUND          = 12

@grepr_dataclass(grepr_fields=["type"])
class DropdownInfo:
    """
    The information about a dropdown of a certain opcode
    """
    
    type: "DropdownType"

class DropdownValueRule(GEnum):
    """
    A rule which determines which values are allowed for dropdowns under given circumstances(context)
    """

    @property
    def guess_default_kind(self) -> DropdownValueKind | None:
        """
        Gets the dropdown value kind for an approximate dropdown value guess, which is used as a default(optional)

        Returns:
            the default dropdown value kind for an approximate guess
        """
        return self.value[0]
    
    @property
    def calculation_default_kind(self) -> "DropdownValueKind | None":
        """
        Gets the dropdown value kind for an exact dropdown value calculation, which is used as a default(optional)

        Returns:
            the default dropdown value kind for an exact calculation
        """
        if self.value[1]: # -> 
            return self.value[0]
        return None

    @property
    def post_validate_func(self) -> Callable[[tuple[DropdownValueKind, DROPDOWN_VALUE_T]], tuple[bool, str|None]] | None:
        """
        Gets the optional function, which checks if the dropdown value is legal, e.g. because creating a full whitelist is not reasonable

        Returns:
            the optional function, which checks if the dropdown value is legal
        """
        match self:
            case DropdownValueRule.MATRIX:
                def _matrix_post_validate_func(dropdown_value: tuple[DropdownValueKind, DROPDOWN_VALUE_T]) -> tuple[bool, str|None]:
                    value: str = dropdown_value[1]
                    msg = 'Must be a string of 25 chars. Every char must be either "0" or "1"'
                    if len(value) != 25:
                        return (False, msg)
                    for char in value: 
                        if char not in {"0", "1"}:
                            return (False, msg)
                    return (True, None)
                return _matrix_post_validate_func
        return None

    # (
    #    "default dropdown value kind", 
    #    "should keep dropdown value kind for exact calculation?", 
    #    "index for uniqueness"
    #)
    STAGE                     = (None                           , None ,  0)
    OTHER_SPRITE              = (DropdownValueKind.SPRITE       , False,  1)
    OTHER_SPRITE_EXCEPT_STAGE = (DropdownValueKind.SPRITE       , False,  2)
    MYSELF                    = (None                           , None ,  3)
    MYSELF_IF_SPRITE          = (None                           , None ,  4)

    MOUSE_POINTER             = (None                           , None ,  5)
    EDGE                      = (None                           , None ,  6)

    RANDOM_POSITION           = (None                           , None ,  7)

    MUTABLE_SPRITE_PROPERTY   = (DropdownValueKind.VARIABLE     , False,  8)
    READABLE_SPRITE_PROPERTY  = (DropdownValueKind.VARIABLE     , False,  9)

    COSTUME                   = (DropdownValueKind.COSTUME      , False, 10)
    BACKDROP                  = (DropdownValueKind.BACKDROP     , False, 11)
    SOUND                     = (DropdownValueKind.SOUND        , False, 12)

    VARIABLE                  = (DropdownValueKind.VARIABLE     , False, 13)
    LIST                      = (DropdownValueKind.LIST         , False, 14)
    BROADCAST_MSG             = (DropdownValueKind.BROADCAST_MSG, True , 15)
    
    FONT                      = (DropdownValueKind.STANDARD     , True , 16)
    MATRIX                    = (DropdownValueKind.STANDARD     , True , 17)
    
    EXTENSION_UNPREDICTABLE   = (DropdownValueKind.STANDARD     , True , 18) 
    # used for dynamic menus in custom extensions, whose values can not be predicted in python


@grepr_dataclass(grepr_fields=["direct_values", "rules", "old_direct_values", "fallback"])
class DropdownTypeInfo:
    """
    The information about a dropdown type, which can be used for one or many opcodes
    """

    direct_values:     list[str | int | bool]  = field(default_factory=list)
    rules:             list[DropdownValueRule] = field(default_factory=list)
    old_direct_values: list[str | int | bool] | None = None  
    fallback:          DROPDOWN_VALUE_T      | None = None
    
    def __post_init__(self) -> None:
        """
        Ensure the old_direct_values default to the direct_values

        Returns:
            None
        """
        if self.old_direct_values is None:
            self.old_direct_values = self.direct_values        
    
class DropdownType(GEnum):
    """
    The type of a block dropdown, which can be used for one or many opcodes. It can be a Builtin or Custom one.
    """

    name: str
    value: DropdownTypeInfo

    @property
    def type_info(self) -> DropdownTypeInfo:
        """
        Get the dropdown type info of a dropdown type

        Returns:
            the dropdown type
        """
        return self.value
    
    @property
    def guess_default_kind(self) -> DropdownValueKind | None:
        """
        Gets the dropdown value kind if a dropdown type for an approximate dropdown value guess, which is used as a default(optional)

        Returns:
            the default dropdown value kind for an approximate guess
        """
        default_kind = None
        for rule in self.type_info.rules:
            rule_default_kind = rule.guess_default_kind
            if rule_default_kind is not None:
                if default_kind is None:
                    default_kind = rule_default_kind
                else:
                    raise MANIP_BlameDevsError(f"Got multiple default dropdown value kinds for {self!r}: {default_kind} and {rule_default_kind}")
        return default_kind

    @property
    def calculation_default_kind(self) -> DropdownValueKind | None:
        """
        Gets the dropdown value kind if a dropdown type for an approximate dropdown value guess, which is used as a default(optional)

        Returns:
            the default dropdown value kind for an approximate guess
        """
        default_kind = None
        for rule in self.type_info.rules:
            rule_default_kind = rule.calculation_default_kind
            if rule_default_kind is not None:
                if default_kind is None:
                    default_kind = rule_default_kind
                else:
                    raise MANIP_BlameDevsError(f"Got multiple default dropdown value kinds for {self!r}: {default_kind} and {rule_default_kind}")
        return default_kind

    @property
    def post_validate_func(self) -> Callable[[tuple[DropdownValueKind, DROPDOWN_VALUE_T]], tuple[bool, str|None]] | None:
        """
        Gets the optional function, which checks if the dropdown value is legal, e.g. because creating a full whitelist is not reasonable

        Returns:
            the optional function, which checks if the dropdown value is legal
        """
        validate_func = None
        for rule in self.type_info.rules:
            rule_validate_func = rule.post_validate_func
            if rule_validate_func is not None:
                if validate_func is None:
                    validate_func = rule_validate_func
                else:
                    raise MANIP_BlameDevsError(f"Got multiple post validation functions for {self!r}: {validate_func} and {rule_validate_func}")
        return validate_func

    def calculate_possible_new_dropdown_values(self, context: PartialContext|CompleteContext) -> list[tuple[DropdownValueKind, DROPDOWN_VALUE_T]]:
        """
        Calulate all the possible values for a SRDropdownValue in certain circumstances(given context)

        Args:
            context: Context about parts of the project. Eg. costumes are important to know what values can be selected for a costume dropdown

        Returns:
            a list of possible values as tuples => (kind, value)
        """
        values: list = []
        for value in self.type_info.direct_values:
            if   isinstance(value, tuple):
                values.append(value)
            else:
                values.append((DropdownValueKind.STANDARD, value))
        
        for segment in self.type_info.rules:
            match segment:
                case DropdownValueRule.STAGE:
                    values.append((DropdownValueKind.STAGE, "stage"))
                case DropdownValueRule.OTHER_SPRITE:
                    values.append((DropdownValueKind.STAGE, "stage"))
                    values.extend(context.other_sprites)
                case DropdownValueRule.OTHER_SPRITE_EXCEPT_STAGE:
                    values.extend(context.other_sprites)
                case DropdownValueRule.MYSELF:
                    values.append((DropdownValueKind.MYSELF, "myself"))
                case DropdownValueRule.MYSELF_IF_SPRITE:
                    if not context.is_stage:
                        values.append((DropdownValueKind.MYSELF, "myself"))
                
                case DropdownValueRule.MOUSE_POINTER:
                    values.append((DropdownValueKind.OBJECT, "mouse-pointer"))
                case DropdownValueRule.EDGE:
                    values.append((DropdownValueKind.OBJECT, "edge"))
                
                case DropdownValueRule.RANDOM_POSITION:
                    values.append((DropdownValueKind.OBJECT, "random position"))
                
                case DropdownValueRule.MUTABLE_SPRITE_PROPERTY:
                    # trying to validate here is so much additional work and makes everything a lot more complicated
                    # instead i will choose the lazy way here
                    values.extend([
                        (DropdownValueKind.STANDARD, "backdrop"), 
                        (DropdownValueKind.STANDARD, "volume"),
                    ])
                    values.extend([
                        (DropdownValueKind.STANDARD, "x position"), 
                        (DropdownValueKind.STANDARD, "y position"), 
                        (DropdownValueKind.STANDARD, "direction"), 
                        (DropdownValueKind.STANDARD, "costume"), 
                        (DropdownValueKind.STANDARD, "size"),
                        (DropdownValueKind.STANDARD, "volume"),
                    ])
                    for local_variables in context.local_variables.values():
                        values.extend(local_variables)

                    raise Exception("TODO: ensure this works")
                
                case DropdownValueRule.READABLE_SPRITE_PROPERTY:
                    # trying to validate here is so much additional work and makes everything a lot more complicated
                    # instead i will choose the lazy way here

                    values.extend([
                        (DropdownValueKind.STANDARD, "backdrop #"), 
                        (DropdownValueKind.STANDARD, "backdrop name"), 
                        (DropdownValueKind.STANDARD, "volume"),
                    ])
                    values.extend(context.global_variables)
                    values.extend([
                        (DropdownValueKind.STANDARD, "x position"), 
                        (DropdownValueKind.STANDARD, "y position"), 
                        (DropdownValueKind.STANDARD, "direction"), 
                        (DropdownValueKind.STANDARD, "costume #"), 
                        (DropdownValueKind.STANDARD, "costume name"), 
                        (DropdownValueKind.STANDARD, "layer"), 
                        (DropdownValueKind.STANDARD, "size"),
                        (DropdownValueKind.STANDARD, "volume"),
                    ])
                    for local_variables in context.local_variables.values():
                        values.extend(local_variables)

                case DropdownValueRule.COSTUME:
                    values.extend(context.costumes)
                    values.extend([(DropdownValueKind.COSTUME, i+1) for i in range(len(context.costumes))])
                case DropdownValueRule.BACKDROP:
                    values.extend(context.backdrops)
                    values.extend([(DropdownValueKind.COSTUME, i+1) for i in range(len(context.backdrops))])
                case DropdownValueRule.SOUND:
                    values.extend([(DropdownValueKind.SOUND, i+1) for i in range(len(context.sounds))])
                case DropdownValueRule.VARIABLE:
                    values.extend(context.scope_variables)
                case DropdownValueRule.LIST:
                    values.extend(context.scope_lists)
                
                case DropdownValueRule.BROADCAST_MSG | DropdownValueRule.FONT:
                    pass # can not be guessed
                case DropdownValueRule.MATRIX:
                    pass # Could theoretically be guessed, but there are 3_3554_432 (2^25) possibilities

        if (values == []) and (self.type_info.fallback is not None):
            values.append(self.type_info.fallback)
        return remove_duplicates(values)

    def guess_possible_new_dropdown_values(self, include_rules: bool) -> list[tuple[DropdownValueKind, DROPDOWN_VALUE_T]]:
        """
        Guess all the possible values for a SRDropdownValue without context

        Returns:
            a list of possible values as tuples => (kind, value)
        """
        values             = []
        for value in self.type_info.direct_values:
            if   isinstance(value, tuple):
                values.append(value)
            else:
                values.append((DropdownValueKind.STANDARD, value))
        
        if include_rules:
            for rule in self.type_info.rules:
                match rule:
                    case DropdownValueRule.STAGE:
                        values.append((DropdownValueKind.STAGE, "stage"))
                    case DropdownValueRule.OTHER_SPRITE:
                        values.append((DropdownValueKind.STAGE, "stage"))
                    case DropdownValueRule.OTHER_SPRITE_EXCEPT_STAGE:
                        pass # can not be guessed, but do not include stage
                    case DropdownValueRule.MYSELF:
                        values.append((DropdownValueKind.MYSELF, "myself"))
                    case DropdownValueRule.MYSELF_IF_SPRITE:
                        values.append((DropdownValueKind.MYSELF, "myself"))
                    
                    case DropdownValueRule.MOUSE_POINTER:
                        values.append((DropdownValueKind.OBJECT, "mouse-pointer"))
                    case DropdownValueRule.EDGE:
                        values.append((DropdownValueKind.OBJECT, "edge"))
                    
                    case DropdownValueRule.RANDOM_POSITION:
                        values.append((DropdownValueKind.OBJECT, "random position"))
                    
                    case DropdownValueRule.MUTABLE_SPRITE_PROPERTY:
                        values.extend([
                            (DropdownValueKind.STANDARD, "backdrop"), 
                            (DropdownValueKind.STANDARD, "volume"),
                        ])
                        values.extend([
                            (DropdownValueKind.STANDARD, "x position"), 
                            (DropdownValueKind.STANDARD, "y position"), 
                            (DropdownValueKind.STANDARD, "direction"), 
                            (DropdownValueKind.STANDARD, "costume"), 
                            (DropdownValueKind.STANDARD, "size"),
                            (DropdownValueKind.STANDARD, "volume"),
                        ])
                    case DropdownValueRule.READABLE_SPRITE_PROPERTY:
                        values.extend([
                            (DropdownValueKind.STANDARD, "backdrop #"), 
                            (DropdownValueKind.STANDARD, "backdrop name"), 
                            (DropdownValueKind.STANDARD, "volume"),
                        ])
                        values.extend([
                            (DropdownValueKind.STANDARD, "x position"), 
                            (DropdownValueKind.STANDARD, "y position"), 
                            (DropdownValueKind.STANDARD, "direction"), 
                            (DropdownValueKind.STANDARD, "costume #"), 
                            (DropdownValueKind.STANDARD, "costume name"), 
                            (DropdownValueKind.STANDARD, "layer"), 
                            (DropdownValueKind.STANDARD, "size"),
                            (DropdownValueKind.STANDARD, "volume"),
                        ])
                    
                    case (DropdownValueRule.COSTUME  | DropdownValueRule.BACKDROP | DropdownValueRule.SOUND 
                        | DropdownValueRule.VARIABLE | DropdownValueRule.LIST     | DropdownValueRule.BROADCAST_MSG | DropdownValueRule.FONT):
                        pass # can not be guessed
                    case DropdownValueRule.MATRIX:
                        pass # Could theoretically be guessed, but there are 3.3554.432 (2**(5*5)) possibilities
        if self.type_info.fallback is not None:
            values.append((DropdownValueKind.FALLBACK, self.type_info.fallback))
        return remove_duplicates(values)

    def guess_possible_old_dropdown_values(self) -> list[DROPDOWN_VALUE_T]:
        """
        Guess all the possible values for a dropdown value in first representation without context

        Returns:
            a list of possible values
        """
        values = []
        for value in self.type_info.old_direct_values:
            if isinstance(value, tuple):
                values.append(value[0])
            else:
                values.append(value)
        for rule in self.type_info.rules:
            match rule:
                case DropdownValueRule.STAGE:
                    values.append("_stage_")
                case DropdownValueRule.OTHER_SPRITE:
                    values.append("_stage_")
                case DropdownValueRule.OTHER_SPRITE_EXCEPT_STAGE:
                    pass
                case DropdownValueRule.MYSELF:
                    values.append("_myself_")
                case DropdownValueRule.MYSELF_IF_SPRITE:
                    values.append("_myself_")
                
                case DropdownValueRule.MOUSE_POINTER:
                    values.append("_mouse_")
                case DropdownValueRule.EDGE:
                    values.append("_edge_")
                
                case DropdownValueRule.RANDOM_POSITION:
                    values.append("_random_")
                
                
                case DropdownValueRule.MUTABLE_SPRITE_PROPERTY:
                    values.extend(["backdrop", "volume"])
                    values.extend(["x position", "y position", "direction", "costume", "size", "volume"])
                case DropdownValueRule.READABLE_SPRITE_PROPERTY:
                    values.extend(["backdrop #", "backdrop name", "volume"])
                    values.extend(["x position", "y position", "direction", "costume #", "costume name", "layer", "size", "volume"])
                
                case (DropdownValueRule.COSTUME  | DropdownValueRule.BACKDROP | DropdownValueRule.SOUND 
                    | DropdownValueRule.VARIABLE | DropdownValueRule.LIST     | DropdownValueRule.BROADCAST_MSG | DropdownValueRule.FONT):
                        pass # can not be guessed
                case DropdownValueRule.MATRIX:
                    pass # Could theoretically be guessed, but there are 3_3554_432 (2^25) possibilities
        if self.type_info.fallback is not None:
            values.append((DropdownValueKind.FALLBACK, self.type_info.fallback))
        return remove_duplicates(values)

    def translate_old_to_new_value(self, old_value: DROPDOWN_VALUE_T) -> tuple[DropdownValueKind, DROPDOWN_VALUE_T]:
        """
        Translate a dropdown value from first representation into a SRDropdownValue expressed as a tuple

        Args:
            old_value: the dropdown value in first representation
        
        Returns:
            the SRDropdownValue as a tuple => (kind, value)
        """
        new_values = self.guess_possible_new_dropdown_values(include_rules=True)
        old_values = self.guess_possible_old_dropdown_values()
        
        assert len(new_values) == len(old_values)
        
        if old_value in old_values:
            return new_values[old_values.index(old_value)]
        else:
            assert self.guess_default_kind is not None
            return (self.guess_default_kind, old_value)

    def translate_new_to_old_value(self, new_value: tuple[DropdownValueKind, DROPDOWN_VALUE_T]) -> DROPDOWN_VALUE_T:
        """
        Translate a SRDropdownValue expressed as a tuple info a dropdown value from first representation

        Args:
            new_value: the SRDropdownValue as a tuple => (kind, value)
        
        Returns:
            the dropdown value in first representation
        """
        new_values = self.guess_possible_new_dropdown_values(include_rules=True)
        old_values = self.guess_possible_old_dropdown_values()
        
        assert len(new_values) == len(old_values)
        
        if new_value in new_values:
            return old_values[new_values.index(new_value)]
        else:
            assert self.guess_default_kind is not None
            return new_value[1]

class BuiltinDropdownType(DropdownType):
    """
    A built-in type of a block dropdown, which can be used for one or many opcodes.
    """

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
    STAGE_OR_OTHER_SPRITE = DropdownTypeInfo(rules=[DropdownValueRule.STAGE, DropdownValueRule.OTHER_SPRITE])
    CLONING_TARGET = DropdownTypeInfo(
        rules=[DropdownValueRule.MYSELF_IF_SPRITE, DropdownValueRule.OTHER_SPRITE_EXCEPT_STAGE],
        fallback=" ",
    )
    UP_DOWN = DropdownTypeInfo(direct_values=["up", "down"])
    LOUDNESS_TIMER = DropdownTypeInfo(
        direct_values=["loudness", "timer"],
        old_direct_values=["LOUDNESS", "TIMER"],
    )
    MOUSE_OR_OTHER_SPRITE = DropdownTypeInfo(rules=[DropdownValueRule.MOUSE_POINTER, DropdownValueRule.OTHER_SPRITE_EXCEPT_STAGE])
    MOUSE_EDGE_OR_OTHER_SPRITE = DropdownTypeInfo(rules=[DropdownValueRule.MOUSE_POINTER, DropdownValueRule.EDGE, DropdownValueRule.OTHER_SPRITE])
    MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE = DropdownTypeInfo(rules=[DropdownValueRule.MOUSE_POINTER, DropdownValueRule.EDGE, DropdownValueRule.MYSELF, DropdownValueRule.OTHER_SPRITE])
    X_OR_Y = DropdownTypeInfo(direct_values=["x", "y"])
    DRAG_MODE = DropdownTypeInfo(direct_values=["draggable", "not draggable"])
    MUTABLE_SPRITE_PROPERTY = DropdownTypeInfo(rules=[DropdownValueRule.MUTABLE_SPRITE_PROPERTY])
    READABLE_SPRITE_PROPERTY = DropdownTypeInfo(rules=[DropdownValueRule.READABLE_SPRITE_PROPERTY])
    TIME_PROPERTY = DropdownTypeInfo(
        direct_values=["year", "month", "date", "day of week", "hour", "minute", "second", "js timestamp"],
        old_direct_values=["YEAR", "MONTH", "DATE", "DAYOFWEEK", "HOUR", "MINUTE", "SECOND", "TIMESTAMP"],
    )
    FINGER_INDEX = DropdownTypeInfo(direct_values=["1", "2", "3", "4", "5"])
    RANDOM_MOUSE_OR_OTHER_SPRITE = DropdownTypeInfo(rules=[DropdownValueRule.RANDOM_POSITION, DropdownValueRule.MOUSE_POINTER, DropdownValueRule.OTHER_SPRITE_EXCEPT_STAGE])
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
    COSTUME = DropdownTypeInfo(rules=[DropdownValueRule.COSTUME])
    BACKDROP = DropdownTypeInfo(rules=[DropdownValueRule.BACKDROP])
    COSTUME_PROPERTY = DropdownTypeInfo(direct_values=["width", "height", "rotation center x", "rotation center y", "drawing mode"])
    MYSELF_OR_OTHER_SPRITE = DropdownTypeInfo(rules=[DropdownValueRule.MYSELF, DropdownValueRule.OTHER_SPRITE])
    FRONT_BACK = DropdownTypeInfo(direct_values=["front", "back"])
    FORWARD_BACKWARD = DropdownTypeInfo(direct_values=["forward", "backward"])
    INFRONT_BEHIND = DropdownTypeInfo(direct_values=["infront", "behind"])
    NUMBER_NAME = DropdownTypeInfo(direct_values=["number", "name"])
    SOUND = DropdownTypeInfo(
        rules=[DropdownValueRule.SOUND], 
        fallback=" ",
    )
    SOUND_EFFECT = DropdownTypeInfo(
        direct_values=["pitch", "pan"],
        old_direct_values=["PITCH", "PAN"],
    )
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
        direct_values=[(DropdownValueKind.SUGGESTION, name) for name in ["Sans Serif", "Serif", "Handwriting", "Marker", "Curly", "Pixel", "Playful", "Bubbly", "Arcade", "Bits and Bytes", "Technological", "Scratch", "Archivo", "Archivo Black", "Random"]],
        old_direct_values=["Sans Serif", "Serif", "Handwriting", "Marker", "Curly", "Pixel", "Playful", "Bubbly", "Arcade", "Bits and Bytes", "Technological", "Scratch", "Archivo", "Archivo Black", "Random"],
        rules=[DropdownValueRule.FONT],
    )
    ON_OFF = DropdownTypeInfo(direct_values=["on", "off"])
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
    MATRIX = DropdownTypeInfo(rules=[DropdownValueRule.MATRIX])

    VARIABLE = DropdownTypeInfo(rules=[DropdownValueRule.VARIABLE])
    LIST = DropdownTypeInfo(rules=[DropdownValueRule.LIST])
    BROADCAST = DropdownTypeInfo(rules=[DropdownValueRule.BROADCAST_MSG])
    
    # TEMPORARY ONES (do not exist in actual SR only during transformation)
    CHECKBOX = DropdownTypeInfo(direct_values=["FALSE", "TRUE"])


__all__ = [
    "DROPDOWN_VALUE_T",
    "DropdownValueKind", "DropdownInfo", "DropdownValueRule", 
    "DropdownTypeInfo", "DropdownType", "BuiltinDropdownType",
]

