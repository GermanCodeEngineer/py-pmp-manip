from utility import PypenguinEnum
from dataclasses import dataclass

from opcode_info.menu     import MenuInfo
from opcode_info.dropdown import DropdownType

@dataclass
class InputInfo:
    """
    The information about a input of a certain opcode.
    """
    _grepr = True
    _grepr_fields = ["type", "menu"]
    
    type: "InputType"
    menu: MenuInfo | None = None

class InputMode(PypenguinEnum):
    """
    Mostly determines the behaviour of inputs.
    """

    def can_be_missing(self) -> bool:
        """
        Return wether an input of this mode is allowed to be missing. 
        (I didn't come up with some inputs just disappearing when empty; go ask the Scratch Team)

        Returns:
            wether an input of this mode is allowed to be missing
        """
        return self in {InputMode.BLOCK_ONLY, InputMode.SCRIPT}        
    
    BLOCK_AND_TEXT               = 0
    BLOCK_AND_MENU_TEXT          = 1
    BLOCK_ONLY                   = 2
    SCRIPT                       = 3
    BLOCK_AND_BROADCAST_DROPDOWN = 4
    BLOCK_AND_DROPDOWN           = 5

class InputType(PypenguinEnum):
    """
    A input type, which can be used for one or many opcodes.
    The input type has only little influence, except those which can contain a dropdown. Then it will be used for dropdown validation.
    Its superior input mode mostly determines its behaviour.
    """

    def get_mode(self) -> InputMode:
        """
        Get the superior input mode.

        Returns:
            the input mode
        """
        return self.value[0]
    
    def get_corresponding_dropdown_type(self) -> "DropdownType":
        """
        Get the corresponding dropdown type.

        Returns:
            the corresponding dropdown type
        """
        assert self.get_mode() in {
            InputMode.BLOCK_AND_MENU_TEXT, 
            InputMode.BLOCK_AND_BROADCAST_DROPDOWN,
            InputMode.BLOCK_AND_DROPDOWN,
        }
        return DropdownType._member_map_[self.name]

    @classmethod
    def get_by_cb_default(cls, default: str) -> "InputType":
        """
        Get the input type by its corresponding default in custom blocks.

        Returns:
            the input type
        """
        match default:
            case "":
                return cls.TEXT
            case "false":
                return cls.BOOLEAN
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

