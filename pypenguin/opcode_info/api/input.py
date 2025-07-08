from pypenguin.utility import grepr_dataclass, PypenguinEnum, DynamicEnum

from pypenguin.opcode_info.api.dropdown import DropdownType, BulitinDropdownType, CustomDropdownType


@grepr_dataclass(grepr_fields=["type", "menu"])
class InputInfo:
    """
    The information about a input of a certain opcode
    """
    
    type: "InputType"
    menu: "MenuInfo | None" = None

class InputMode(PypenguinEnum):
    """
    Mostly determines the behaviour of inputs
    """

    @property
    def can_be_missing(self) -> bool:
        """
        Return wether an input of this mode is allowed to be missing. 
        (I didn't come up with some inputs just disappearing when empty; go ask the Scratch Team)

        Returns:
            wether an input of this mode is allowed to be missing
        """
        return self.value[0]  
    
    # (magic number, index)
    BLOCK_AND_TEXT               = (False, 0)
    BLOCK_AND_MENU_TEXT          = (False, 1)
    BLOCK_ONLY                   = (True , 2)
    SCRIPT                       = (True , 3)
    BLOCK_AND_BROADCAST_DROPDOWN = (False, 4)
    BLOCK_AND_DROPDOWN           = (False, 5)

class InputType:
    """
    The type of a block input, which can be used for one or many opcodes. It can be a Builtin or Custom one.
    The input type has only little influence, except those which can contain a dropdown. Then it will be used for dropdown validation.
    Its superior input mode mostly determines its behaviour
    """

    name: str
    value: tuple[InputMode, int|None, int] # (InputMode, magic number, index)

    @property
    def mode(self) -> InputMode:
        """
        Get the superior input mode

        Returns:
            the input mode
        """
        return self.value[0]

    @property
    def corresponding_dropdown_type(self) -> "DropdownType":
        """
        Get the corresponding dropdown type

        Returns:
            the corresponding dropdown type
        """
        assert self.mode in {
            InputMode.BLOCK_AND_MENU_TEXT, 
            InputMode.BLOCK_AND_BROADCAST_DROPDOWN,
            InputMode.BLOCK_AND_DROPDOWN,
        }
        if isinstance(self, BuiltinInputType):
            return BulitinDropdownType._member_map_[self.name]
        elif isinstance(self, CustomInputType):
            return CustomDropdownType._member_map_

    @property
    def magic_number(self) -> int | None:
        """
        Get the magic number used in first representation of inputs

        Returns:
            the magic number
        """
        return self.value[1]

    @classmethod
    def get_by_cb_default(cls, default: str) -> "InputType":
        """
        Get the input type by its corresponding default in custom blocks

        Returns:
            the input type
        """
        match default:
            case "":
                return BuiltinInputType.TEXT
            case "false":
                return BuiltinInputType.BOOLEAN

class BuiltinInputType(InputType, PypenguinEnum):
    """
    A built-in type of a block input, which can be used for one or many opcodes.
    The input type has only little influence, except those which can contain a dropdown. Then it will be used for dropdown validation.
    Its superior input mode mostly determines its behaviour
    """

    # (InputMode, magic number, index)
    # BLOCK_AND_TEXT
    TEXT                = (InputMode.BLOCK_AND_TEXT, 10, 0)
    COLOR               = (InputMode.BLOCK_AND_TEXT,  9, 1)
    DIRECTION           = (InputMode.BLOCK_AND_TEXT,  8, 2)
    INTEGER             = (InputMode.BLOCK_AND_TEXT,  7, 3)
    POSITIVE_INTEGER    = (InputMode.BLOCK_AND_TEXT,  6, 4)
    POSITIVE_NUMBER     = (InputMode.BLOCK_AND_TEXT,  5, 5)
    NUMBER              = (InputMode.BLOCK_AND_TEXT,  4, 6)

    # BLOCK_AND_MENU_TEXT
    NOTE                = (InputMode.BLOCK_AND_MENU_TEXT, None, 0)

    # BLOCK_ONLY
    BOOLEAN             = (InputMode.BLOCK_ONLY, None, 0)
    ROUND               = (InputMode.BLOCK_ONLY, None, 1)
    EMBEDDED_MENU       = (InputMode.BLOCK_ONLY, None, 2)

    # SCRIPT
    SCRIPT              = (InputMode.SCRIPT, None, 0)

    # BLOCK_AND_BROADCAST_DROPDOWN
    BROADCAST           = (InputMode.BLOCK_AND_BROADCAST_DROPDOWN, 11, 0)

    # BLOCK_AND_DROPDOWN
    STAGE_OR_OTHER_SPRITE               = (InputMode.BLOCK_AND_DROPDOWN, None,  0)
    CLONING_TARGET                      = (InputMode.BLOCK_AND_DROPDOWN, None,  1)
    MOUSE_OR_OTHER_SPRITE               = (InputMode.BLOCK_AND_DROPDOWN, None,  2)
    MOUSE_EDGE_OR_OTHER_SPRITE          = (InputMode.BLOCK_AND_DROPDOWN, None,  3)
    MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE   = (InputMode.BLOCK_AND_DROPDOWN, None,  4)
    KEY                                 = (InputMode.BLOCK_AND_DROPDOWN, None,  5)
    UP_DOWN                             = (InputMode.BLOCK_AND_DROPDOWN, None,  6)
    FINGER_INDEX                        = (InputMode.BLOCK_AND_DROPDOWN, None,  7)
    RANDOM_MOUSE_OR_OTHER_SPRITE        = (InputMode.BLOCK_AND_DROPDOWN, None,  8)
    COSTUME                             = (InputMode.BLOCK_AND_DROPDOWN, None,  9)
    COSTUME_PROPERTY                    = (InputMode.BLOCK_AND_DROPDOWN, None, 10)
    BACKDROP                            = (InputMode.BLOCK_AND_DROPDOWN, None, 11)
    BACKDROP_PROPERTY                   = (InputMode.BLOCK_AND_DROPDOWN, None, 12)
    MYSELF_OR_OTHER_SPRITE              = (InputMode.BLOCK_AND_DROPDOWN, None, 13)
    SOUND                               = (InputMode.BLOCK_AND_DROPDOWN, None, 14)
    DRUM                                = (InputMode.BLOCK_AND_DROPDOWN, None, 15)
    INSTRUMENT                          = (InputMode.BLOCK_AND_DROPDOWN, None, 16)
    FONT                                = (InputMode.BLOCK_AND_DROPDOWN, None, 17)
    PEN_PROPERTY                        = (InputMode.BLOCK_AND_DROPDOWN, None, 18)
    VIDEO_SENSING_PROPERTY              = (InputMode.BLOCK_AND_DROPDOWN, None, 19)
    VIDEO_SENSING_TARGET                = (InputMode.BLOCK_AND_DROPDOWN, None, 20)
    VIDEO_STATE                         = (InputMode.BLOCK_AND_DROPDOWN, None, 21)
    TEXT_TO_SPEECH_VOICE                = (InputMode.BLOCK_AND_DROPDOWN, None, 22)
    TEXT_TO_SPEECH_LANGUAGE             = (InputMode.BLOCK_AND_DROPDOWN, None, 23)
    TRANSLATE_LANGUAGE                  = (InputMode.BLOCK_AND_DROPDOWN, None, 24)
    MAKEY_KEY                           = (InputMode.BLOCK_AND_DROPDOWN, None, 25)
    MAKEY_SEQUENCE                      = (InputMode.BLOCK_AND_DROPDOWN, None, 26)
    READ_FILE_MODE                      = (InputMode.BLOCK_AND_DROPDOWN, None, 27)
    FILE_SELECTOR_MODE                  = (InputMode.BLOCK_AND_DROPDOWN, None, 28)
    MATRIX                              = (InputMode.BLOCK_AND_DROPDOWN, None, 29)

@grepr_dataclass(grepr_fields=["name", "value"], init=False, unsafe_hash=True, frozen=True)
class CustomInputType(InputType, DynamicEnum):
    """
    A custom type of a block input, which can be used for one or many opcodes.
    The input type has only little influence, except those which can contain a dropdown. Then it will be used for dropdown validation.
    Its superior input mode mostly determines its behaviour
    """

@grepr_dataclass(grepr_fields=["opcode", "inner"])
class MenuInfo:
    """
    The information about a menu in an input
    """
    
    opcode: str
    inner : str

__all__ = ["InputInfo", "InputMode", "InputType", "BuiltinInputType", "CustomInputType", "MenuInfo"]
