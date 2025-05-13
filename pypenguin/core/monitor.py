from typing      import Any
from dataclasses import dataclass
from math        import inf

from pypenguin.utility           import (
    GreprClass, ValidationConfig,
    AA_TYPE, AA_TYPES, AA_DICT_OF_TYPE, AA_COORD_PAIR, AA_BOXED_COORD_PAIR, AA_EQUAL, AA_BIGGER_OR_EQUAL, 
    InvalidOpcodeError, MissingDropdownError, UnnecessaryDropdownError, ThanksError,
)
from pypenguin.opcode_info       import OpcodeInfoAPI, DropdownType
from pypenguin.important_opcodes import *

from pypenguin.core.dropdown import SRDropdownValue
from pypenguin.core.context  import PartialContext

STAGE_WIDTH : int = 480
STAGE_HEIGHT: int = 360
LIST_MONITOR_DEFAULT_WIDTH  = 100
LIST_MONITOR_DEFAULT_HEIGHT = 120

@dataclass(repr=False)
class FRMonitor(GreprClass):
    """
    The first representation for a monitor
    """
    _grepr = True
    _grepr_fields = ["id", "mode", "opcode", "params", "sprite_name", "value", "x", "y", "visible", "width", "height", "slider_min", "slider_max", "is_discrete"]

    # Core Properties
    id: str
    mode: str
    opcode: str
    params: dict[str, Any]
    sprite_name: str | None
    value: Any
    x: int | float
    y: int | float
    visible: bool
    
    # Properties which matter for some opcodes
    width: int | float
    height: int | float
    slider_min: int | float | None
    slider_max: int | float | None
    is_discrete: bool | None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMonitor":
        """
        Deserializes raw data into a FRMonitor.
        
        Args:
            data: the raw data
        
        Returns:
            the FRMonitor
        """
        return cls(
            # Core Properties
            id          = data["id"        ], 
            mode        = data["mode"      ], 
            opcode      = data["opcode"    ], 
            params      = data["params"    ], 
            sprite_name = data["spriteName"], 
            value       = data["value"     ],
            x           = data["x"         ],
            y           = data["y"         ],
            visible     = data["visible"   ],
            
            # Properties for some opcodes
            width       = data["width" ],
            height      = data["height"],
            slider_min  = data.get("sliderMin" , None),
            slider_max  = data.get("sliderMax" , None),
            is_discrete = data.get("isDiscrete", None),
        )
    
    def __post_init__(self) -> None:
        """
        Ensure my assumptions about monitors were correct.
        
        Returns:
            None
        """
        if not isinstance(self.params, dict):
            raise ThanksError()

    def step(self, info_api: OpcodeInfoAPI, sprite_names: list[str]) -> tuple[str | None, "SRMonitor | None"]:
        """
        Converts a FRMonitor into a SRMonitor
        
        Args:
            info_api: the opcode info api used to fetch information about opcodes
            sprite_names: a list of sprite names in the project, used to delete monitors of deleted sprites
        
        Returns:
            the SRMonitor
        """
        if (self.sprite_name is not None) and (self.sprite_name not in sprite_names):
            return (None, None) # Delete monitors of non-existing sprites: possibly not needed anymore
        
        opcode_info = info_api.get_info_by_old(self.opcode)
        
        new_dropdowns = {}
        for dropdown_id, dropdown_value in self.params.items():
            new_dropdown_id = opcode_info.get_new_dropdown_id(dropdown_id)
            dropdown_type   = opcode_info.get_dropdown_info_by_old(dropdown_id).type
            new_dropdowns[new_dropdown_id] = SRDropdownValue.from_tuple(dropdown_type.translate_old_to_new_value(dropdown_value))
        
        new_opcode = info_api.get_new_by_old(self.opcode)
        position   = (self.x - (STAGE_WIDTH//2), self.y - (STAGE_HEIGHT//2)) # this lets the center of stage be the origin        
        if   self.opcode == OPCODE_VAR_VALUE:
            return (self.sprite_name, SRVariableMonitor(
                opcode              = new_opcode,
                dropdowns           = new_dropdowns,
                position            = position,
                is_visible          = self.visible,
                slider_min          = self.slider_min,
                slider_max          = self.slider_max,
                allow_only_integers = self.is_discrete,
            ))
        elif self.opcode == OPCODE_LIST_VALUE:
            return (self.sprite_name, SRListMonitor(
                opcode      = new_opcode,
                dropdowns   = new_dropdowns,
                position    = position,
                is_visible  = self.visible,
                size        = (
                    LIST_MONITOR_DEFAULT_WIDTH  if self.width  == 0 else self.width,
                    LIST_MONITOR_DEFAULT_HEIGHT if self.height == 0 else self.height,
                )
            ))
        else:
            return (self.sprite_name, SRMonitor(
                opcode      = new_opcode,
                dropdowns   = new_dropdowns,
                position    = position,
                is_visible  = self.visible,
            ))

@dataclass(repr=False)
class SRMonitor(GreprClass):
    """
    The second representation for a monitor. It is much more user friendly.
    """
    _grepr = True
    _grepr_fields = ["opcode", "dropdowns", "sprite", "position", "is_visible"]
    
    opcode: str
    dropdowns: dict[str, SRDropdownValue]
    position: tuple[int | float, int | float] # Center of the Stage is the origin
    is_visible: bool
    
    def __post_init__(self) -> None:
        """
        Ensure that it is impossible to create a variable/list monitor without using the correct subclass.

        Returns:
            None
        """
        if   self.opcode == NEW_OPCODE_VAR_VALUE:
            assert isinstance(self, SRVariableMonitor), f"Must be a SRVariableMonitor instance if opcode is {repr(NEW_OPCODE_VAR_VALUE)}"
        elif self.opcode == NEW_OPCODE_LIST_VALUE:
            assert isinstance(self, SRListMonitor), f"Must be a SRListMonitor instance if opcode is {repr(NEW_OPCODE_LIST_VALUE)}"
    
    def validate(self, path: list, config: ValidationConfig, info_api: OpcodeInfoAPI) -> None:
        """
        Ensure a SRMonitor is valid, raise ValidationError if not.
        To validate the exact dropdown values you should additionally call the validate_dropdown_values method.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        """
        AA_TYPE(self, path, "opcode", str)
        AA_DICT_OF_TYPE(self, path, "dropdowns", key_t=str, value_t=SRDropdownValue)
        if config.raise_when_monitor_position_outside_stage:
            AA_BOXED_COORD_PAIR(self, path, "position", 
                min_x=-(STAGE_WIDTH //2), max_x=(STAGE_WIDTH //2), 
                min_y=-(STAGE_HEIGHT//2), max_y=(STAGE_HEIGHT//2),
            )
        else:
            AA_COORD_PAIR(self, path, "position")
        AA_TYPE(self, path, "is_visible", bool)
        
        opcode_info = info_api.get_info_by_new_safe(self.opcode)
        if (opcode_info is None) or (not opcode_info.can_have_monitor):
            raise InvalidOpcodeError(path, f"opcode of {self.__class__.__name__} must be a defined opcode. That block must be able to have monitors")
        
        new_dropdown_ids = opcode_info.get_all_new_dropdown_ids()
        for new_dropdown_id, dropdown_value in self.dropdowns.items():
            dropdown_value.validate(path+["dropdowns", (new_dropdown_id,)], config)
            if new_dropdown_id not in new_dropdown_ids:
                raise UnnecessaryDropdownError(path, f"dropdowns of {self.__class__.__name__} with opcode {repr(self.opcode)} includes unnecessary dropdown {repr(new_dropdown_id)}")
        for new_dropdown_id in new_dropdown_ids:
            if new_dropdown_id not in self.dropdowns:
                raise MissingDropdownError(path, f"dropdowns of {self.__class__.__name__} with opcode {repr(self.opcode)} is missing dropdown {repr(new_dropdown_id)}")
    
    def validate_dropdown_values(self, path: list, config: ValidationConfig, info_api: OpcodeInfoAPI, context: PartialContext) -> None:
        """
        Ensure the dropdown values of a SRMonitor are valid, raise ValidationError if not.
        For validation of the monitor itself, call the validate method.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
            info_api: the opcode info api used to fetch information about opcodes
            context: Context about parts of the project. Used to validate dropdowns
        
        Returns:
            None
        """
        opcode_info = info_api.get_info_by_new(self.opcode)
        for new_dropdown_id, dropdown in self.dropdowns.items():
            dropdown_type = opcode_info.get_dropdown_info_by_new(new_dropdown_id).type
            dropdown.validate_value(
                path          = path+["dropdowns", (new_dropdown_id,)],
                config        = config,
                dropdown_type = dropdown_type, 
                context       = context,
            )

@dataclass(repr=False)
class SRVariableMonitor(SRMonitor):
    """
    The second representation exclusively for variable monitors
    """
    _grepr_fields = SRMonitor._grepr_fields + ["slider_min", "slider_max", "allow_only_integers"]
    
    slider_min: int | float
    slider_max: int | float
    allow_only_integers: bool
    
    def validate(self, path: list, config: ValidationConfig, info_api: OpcodeInfoAPI):
        """
        Ensure a SRVariableMonitor is valid, raise ValidationError if not.
        To validate the exact dropdown values you should additionally call the validate_dropdown_values method.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        """
        super().validate(path, config, info_api)
        AA_EQUAL(self, path, "opcode", NEW_OPCODE_VAR_VALUE)
        
        AA_TYPE(self, path, "allow_only_integers", bool)
        if self.allow_only_integers:
            condition = "When allow_only_integers is True"
            AA_TYPE(self, path, "slider_min", int, condition=condition)
            AA_TYPE(self, path, "slider_max", int, condition=condition)
        else:
            condition = "When allow_only_integers is False"
            AA_TYPES(self, path, "slider_min", (int, float), condition=condition)
            AA_TYPES(self, path, "slider_max", (int, float), condition=condition)

        AA_BIGGER_OR_EQUAL(self, path, "slider_max", "slider_min")

@dataclass(repr=False)
class SRListMonitor(SRMonitor):
    """
    The second representation exclusively for list monitors
    """
    _grepr_fields = SRMonitor._grepr_fields + ["size"]

    size: tuple[int | float, int | float]
    
    def validate(self, path: list, config: ValidationConfig, info_api: OpcodeInfoAPI):
        """
        Ensure a SRListMonitor is valid, raise ValidationError if not.
        To validate the exact dropdown values you should additionally call the validate_dropdown_values method.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        """
        super().validate(path, config, info_api)
        AA_EQUAL(self, path, "opcode", NEW_OPCODE_LIST_VALUE)
        
        if config.raise_when_monitor_bigger_then_stage:
            AA_BOXED_COORD_PAIR(self, path, "size", min_x=100, max_x=STAGE_WIDTH, min_y=60, max_y=STAGE_HEIGHT)
        else:
            AA_BOXED_COORD_PAIR(self, path, "size", min_x=100, max_x=inf,         min_y=60, max_y=inf         )

