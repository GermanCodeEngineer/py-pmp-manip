from copy   import deepcopy
from typing import Any

from pmp_manip.config           import get_config
from pmp_manip.opcode_info.api  import OpcodeInfoAPI, MonitorIdBehaviour, DROPDOWN_VALUE_T
from pmp_manip.utility          import (
    grepr_dataclass, string_to_sha256,
    AA_TYPE, AA_TYPES, AA_DICT_OF_TYPE, AA_COORD_PAIR, AA_BOXED_COORD_PAIR, AA_EQUAL, AA_BIGGER_OR_EQUAL, 
    MANIP_InvalidOpcodeError, MANIP_MissingDropdownError, MANIP_UnnecessaryDropdownError, MANIP_ThanksError,
)
from pmp_manip.important_consts import (
    OPCODE_VAR_VALUE, OPCODE_LIST_VALUE, NEW_OPCODE_VAR_VALUE, NEW_OPCODE_LIST_VALUE, 
    SHA256_SEC_TARGET_NAME, SHA256_SEC_MONITOR_VARIABLE_ID,
)

from pmp_manip.core.block_interface import InterToFirstIF
from pmp_manip.core.context         import PartialContext, CompleteContext
from pmp_manip.core.dropdown        import SRDropdownValue
from pmp_manip.core.enums           import SRVariableMonitorReadoutMode


STAGE_WIDTH : int = 480
STAGE_HEIGHT: int = 360
LIST_MONITOR_DEFAULT_WIDTH : int|float = 100
LIST_MONITOR_DEFAULT_HEIGHT: int|float = 120
LIST_MONITOR_MIN_WIDTH : int|float = 100
LIST_MONITOR_MIN_HEIGHT: int|float = 60


@grepr_dataclass(grepr_fields=["id", "mode", "opcode", "params", "sprite_name", "value", "x", "y", "visible", "width", "height", "slider_min", "slider_max", "is_discrete", "variable_type", "variable_id"])
class FRMonitor:
    """
    The first representation for a monitor
    """

    # Core Properties
    id: str
    mode: str
    opcode: str
    params: dict[str, DROPDOWN_VALUE_T]
    sprite_name: str | None
    value: DROPDOWN_VALUE_T
    x: int | float
    y: int | float
    visible: bool

    # Properties which matter for some opcodes
    width: int | float
    height: int | float
    slider_min: int | float | None
    slider_max: int | float | None
    is_discrete: bool | None

    # Properties which matter for blocks from custom extensions
    variable_type: None
    variable_id: str | None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMonitor":
        """
        Deserializes json_data into a FRMonitor
        
        Args:
            data: the json_data
        
        Returns:
            the FRMonitor
        """
        return cls(
            # Core Properties
            id          = data["id"        ], 
            mode        = data["mode"      ], 
            opcode      = data["opcode"    ], 
            params      = deepcopy(data["params"]), 
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

            # Properties which matter for blocks from custom extensions
            variable_type = data.get("variableType", None),
            variable_id   = data.get("variableId"  , None),
        )
    
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRMonitor into json data
        
        Returns:
            the json data
        """
        data = {
            "id"          : self.id,
            "mode"        : self.mode,
            "opcode"      : self.opcode,
            "params"      : deepcopy(self.params),
            "spriteName"  : self.sprite_name,
            "value"       : self.value,
            "x"           : self.x,
            "y"           : self.y,
            "visible"     : self.visible,

            "width"       : self.width,
            "height"      : self.height,

            "variableType": self.variable_type,
            "variableId"  : self.variable_id,
        }
        if self.is_discrete is not None:
            data["sliderMin" ] = self.slider_min
            data["sliderMax" ] = self.slider_max
            data["isDiscrete"] = self.is_discrete
        return data
    
    def __post_init__(self) -> None:
        """
        Ensure my assumptions about monitors were correct
        
        Returns:
            None
        """
        if not isinstance(self.params, dict):
            raise MANIP_ThanksError()
        if self.opcode == OPCODE_VAR_VALUE:
            valid = self.mode in {"default", "large", "slider"}
        elif self.opcode == OPCODE_LIST_VALUE:
            valid = self.mode == "list"
        else:
            valid = self.mode == "default"
        if not valid:
            raise MANIP_ThanksError()
        # TODO: implement variable_type
        #if self.variable_type not in {None, ""}:
        #    raise MANIP_ThanksError()

    def to_second(self, info_api: OpcodeInfoAPI, sprite_names: list[str]) -> "SRMonitor | None":
        """
        Converts a FRMonitor into a SRMonitor
        
        Args:
            info_api: the opcode info api used to fetch information about opcodes
            sprite_names: a list of sprite names in the project, used to delete monitors of deleted sprites
        
        Returns:
            the SRMonitor
        """
        if (self.sprite_name is not None) and (self.sprite_name not in sprite_names):
            return None # Delete monitors of non-existing sprites: possibly not needed anymore
        
        opcode_info = info_api.get_info_by_old(self.opcode)
        
        new_dropdowns = {}
        for dropdown_id, dropdown_value in self.params.items():
            new_dropdown_id = opcode_info.get_new_dropdown_id(dropdown_id)
            dropdown_type   = opcode_info.get_dropdown_info_by_old(dropdown_id).type
            new_dropdown_value = dropdown_type.translate_old_to_new_value(dropdown_value)
            new_dropdowns[new_dropdown_id] = SRDropdownValue.from_tuple(new_dropdown_value)
        
        new_opcode = info_api.get_new_by_old(self.opcode)
        position   = (self.x - (STAGE_WIDTH//2), self.y - (STAGE_HEIGHT//2)) # this lets the center of stage be the origin        
        if   self.opcode == OPCODE_VAR_VALUE:
            return SRVariableMonitor(
                opcode              = new_opcode,
                dropdowns           = new_dropdowns,
                position            = position,
                is_visible          = self.visible,
                readout_mode        = SRVariableMonitorReadoutMode.from_code(self.mode),
                slider_min          = self.slider_min,
                slider_max          = self.slider_max,
                allow_only_integers = self.is_discrete,
            )
        elif self.opcode == OPCODE_LIST_VALUE:
            return SRListMonitor(
                opcode      = new_opcode,
                dropdowns   = new_dropdowns,
                position    = position,
                is_visible  = self.visible,
                size        = (
                    LIST_MONITOR_DEFAULT_WIDTH  if self.width  == 0 else self.width,
                    LIST_MONITOR_DEFAULT_HEIGHT if self.height == 0 else self.height,
                )
            )
        else:
            return SRMonitor(
                opcode      = new_opcode,
                dropdowns   = new_dropdowns,
                position    = position,
                is_visible  = self.visible,
            )

@grepr_dataclass(grepr_fields=["opcode", "dropdowns", "position", "is_visible"])
class SRMonitor:
    """
    The second representation for a monitor. It is much more user friendly
    """
    
    opcode: str
    dropdowns: dict[str, SRDropdownValue]
    position: tuple[int | float, int | float] # Center of the Stage is the origin
    is_visible: bool
    
    def __post_init__(self) -> None:
        """
        Ensure that it is impossible to create a variable/list monitor without using the correct subclass

        Returns:
            None
        """
        if   self.opcode == NEW_OPCODE_VAR_VALUE:
            assert isinstance(self, SRVariableMonitor), f"Must be a SRVariableMonitor instance if opcode is {NEW_OPCODE_VAR_VALUE!r}"
        elif self.opcode == NEW_OPCODE_LIST_VALUE:
            assert isinstance(self, SRListMonitor), f"Must be a SRListMonitor instance if opcode is {NEW_OPCODE_LIST_VALUE!r}"
        else:
            assert not isinstance(self, (SRVariableMonitor, SRListMonitor)), (
                f"must not be a SRVariableMonitor or SRListMonitor if opcode "
                f"is neither {NEW_OPCODE_VAR_VALUE!r} nor {NEW_OPCODE_LIST_VALUE!r}")
            
    
    def validate(self, path: list, info_api: OpcodeInfoAPI) -> None:
        """
        Ensure a SRMonitor is valid, raise MANIP_ValidationError if not
        To validate the exact dropdown values you should additionally call the validate_dropdown_values method
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRMonitor is invalid
            MANIP_InvalidOpcodeError(MANIP_ValidationError): if the opcode is not a defined opcode
            MANIP_UnnecessaryDropdownError(MANIP_ValidationError): if a key of dropdowns is not expected for the specific opcode
            MANIP_MissingDropdownError(MANIP_ValidationError): if an expected key of dropdowns for the specific opcode is missing
        """
        AA_TYPE(self, path, "opcode", str)
        AA_DICT_OF_TYPE(self, path, "dropdowns", key_t=str, value_t=SRDropdownValue)
        if get_config().validation.raise_if_monitor_position_outside_stage:
            AA_BOXED_COORD_PAIR(self, path, "position", 
                min_x=-(STAGE_WIDTH //2), max_x=(STAGE_WIDTH //2), 
                min_y=-(STAGE_HEIGHT//2), max_y=(STAGE_HEIGHT//2),
            )
        else:
            AA_COORD_PAIR(self, path, "position")
        AA_TYPE(self, path, "is_visible", bool)
        
        cls_name = self.__class__.__name__
        opcode_info = info_api.get_info_by_new_safe(self.opcode)
        if (opcode_info is None) or (not opcode_info.can_have_monitor):
            raise MANIP_InvalidOpcodeError(path, 
                f"opcode of {cls_name} must be a defined opcode. That block must be able to have monitors",
            )
        
        new_dropdown_ids = opcode_info.get_all_new_dropdown_ids()
        for new_dropdown_id, dropdown_value in self.dropdowns.items():
            dropdown_value.validate(path+["dropdowns", (new_dropdown_id,)])
            if new_dropdown_id not in new_dropdown_ids:
                raise MANIP_UnnecessaryDropdownError(path, 
                    f"dropdowns of {cls_name} with opcode {self.opcode!r} includes unnecessary dropdown {new_dropdown_id!r}",
                )
        for new_dropdown_id in new_dropdown_ids:
            if new_dropdown_id not in self.dropdowns:
                raise MANIP_MissingDropdownError(path, 
                    f"dropdowns of {cls_name} with opcode {self.opcode!r} is missing dropdown {new_dropdown_id!r}",
                )
    
    def validate_dropdown_values(self, 
        path: list, 
        info_api: OpcodeInfoAPI, 
        context: PartialContext | CompleteContext,
     ) -> None:
        """
        Ensure the dropdown values of a SRMonitor are valid, raise MANIP_ValidationError if not
        For validation of the monitor itself, call the validate method
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            context: Context about parts of the project. Used to validate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if some of the dropdown values of the SRMonitor are invalid
        """
        opcode_info = info_api.get_info_by_new(self.opcode)
        for new_dropdown_id, dropdown in self.dropdowns.items():
            dropdown_type = opcode_info.get_dropdown_info_by_new(new_dropdown_id).type
            dropdown.validate_value(
                path          = path+["dropdowns", (new_dropdown_id,)],
                dropdown_type = dropdown_type, 
                context       = context,
            )
    
    def _generate_id(self, itf_if: InterToFirstIF, info_api: OpcodeInfoAPI, old_dropdown_values: list[DROPDOWN_VALUE_T]) -> str:
        """
        Generates the id needed for a FRMonitor

        Args:
            itf_if: interface which allows the management of other blocks and more
            info_api: the opcode info api used to fetch information about opcodes
            old_dropdown_values: the dropdown values of the monitor in first representation
        
        Returns:
            the monitor id
        """
        opcode_info = info_api.get_info_by_new(self.opcode)
        monitor_id_behaviour: MonitorIdBehaviour = opcode_info.monitor_id_behaviour
        sprite_sha256 = None if itf_if.sprite_name is None else string_to_sha256(itf_if.sprite_name, secondary=SHA256_SEC_TARGET_NAME)
        opcode_full = info_api.get_old_by_new(self.opcode)
        opcode_main = opcode_full[opcode_full.index("_")+1:] # e.g. "motion_xposition" -> "xposition"
        match monitor_id_behaviour:
            case MonitorIdBehaviour.SPRITE_OPCMAIN:
                return f"{sprite_sha256}_{opcode_main}"
            case MonitorIdBehaviour.SPRITE_OPCMAIN_PARAMS:
                return f"{sprite_sha256}_{opcode_main}_{'_'.join(old_dropdown_values)}"
            case MonitorIdBehaviour.OPCMAIN_PARAMS:
                return f"{opcode_main}_{'_'.join(old_dropdown_values)}"
            case MonitorIdBehaviour.OPCMAIN_LOWERPARAM:
                assert len(old_dropdown_values) == 1
                return f"{opcode_main}_{old_dropdown_values[0].lower()}"
            case MonitorIdBehaviour.OPCMAIN:
                return opcode_main
            case MonitorIdBehaviour.OPCFULL_PARAMS:
                return f"{opcode_full}_{'_'.join(old_dropdown_values)}"
            case MonitorIdBehaviour.OPCFULL:
                return opcode_full
            case MonitorIdBehaviour.VARIABLE:
                assert len(old_dropdown_values) == 1
                return itf_if.get_variable_sha256(old_dropdown_values[0])
            case MonitorIdBehaviour.LIST:
                assert len(old_dropdown_values) == 1
                return itf_if.get_list_sha256    (old_dropdown_values[0])

    def to_first(self, itf_if: InterToFirstIF, info_api: OpcodeInfoAPI) -> FRMonitor:
        """
        Converts a SRMonitor into a FRMonitor
        
        Args:
            itf_if: interface which allows the management of other blocks and more
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the FRMonitor
        """        
        opcode_info = info_api.get_info_by_new(self.opcode)
        if   isinstance(self, SRVariableMonitor): # opcode = NEW_OPCODE_VAR_VALUE
            mode          = self.readout_mode.to_code()
            value         = 0
            width, height = 0, 0
            slider_min    = self.slider_min
            slider_max    = self.slider_max
            is_discrete   = self.allow_only_integers
        elif isinstance(self, SRListMonitor): # opcode = NEW_OPCODE_LIST_VALUE
            mode          = "list"
            value         = []
            width, height = self.size
            slider_min    = None
            slider_max    = None
            is_discrete   = None
        else:
            mode          = "default"
            value         = 0
            width, height = 0, 0
            slider_min    = 0
            slider_max    = 100
            is_discrete   = True
        
        old_dropdowns = {}
        for dropdown_id, dropdown_value in self.dropdowns.items():
            old_dropdown_id    = opcode_info.get_old_dropdown_id(dropdown_id)
            dropdown_type      = opcode_info.get_dropdown_info_by_new(dropdown_id).type
            old_dropdown_value = dropdown_type.translate_new_to_old_value(dropdown_value.to_tuple())
            old_dropdowns[old_dropdown_id] = old_dropdown_value
        
        old_dropdown_values = list(old_dropdowns.values())
        old_opcode = info_api.get_old_by_new(self.opcode)
        if opcode_info.has_variable_id:
            variable_id = string_to_sha256(old_opcode, secondary=SHA256_SEC_MONITOR_VARIABLE_ID)
        else:
            variable_id = None
        
        return FRMonitor(
            id            = self._generate_id(itf_if, info_api, old_dropdown_values),
            mode          = mode,
            opcode        = old_opcode,
            params        = old_dropdowns,
            sprite_name   = itf_if.sprite_name,
            value         = value,
            x             = self.position[0] + (STAGE_WIDTH //2),
            y             = self.position[1] + (STAGE_HEIGHT//2),
            visible       = self.is_visible,

            width         = width,
            height        = height,
            slider_min    = slider_min,
            slider_max    = slider_max,
            is_discrete   = is_discrete,

            variable_type = None,
            variable_id   = variable_id,
        )
        

@grepr_dataclass(grepr_fields=["readout_mode", "slider_min", "slider_max", "allow_only_integers"])
class SRVariableMonitor(SRMonitor):
    """
    The second representation exclusively for variable monitors
    """
    
    readout_mode: SRVariableMonitorReadoutMode
    slider_min: int | float
    slider_max: int | float
    allow_only_integers: bool
    
    def validate(self, path: list, info_api: OpcodeInfoAPI):
        """
        Ensure a SRVariableMonitor is valid, raise MANIP_ValidationError if not
        To validate the exact dropdown values you should additionally call the validate_dropdown_values method
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRVariableMonitor is invalid
        """
        super().validate(path, info_api)
        AA_EQUAL(self, path, "opcode", NEW_OPCODE_VAR_VALUE)
        
        AA_TYPE(self, path, "readout_mode", SRVariableMonitorReadoutMode)
        AA_TYPE(self, path, "allow_only_integers", bool)
        if self.allow_only_integers:
            allowed_types = (int,)
            condition = "When allow_only_integers is True"
        else:
            allowed_types = (int, float)
            condition = "When allow_only_integers is False"
        AA_TYPES(self, path, "slider_min", allowed_types, condition=condition)
        AA_TYPES(self, path, "slider_max", allowed_types, condition=condition)

        AA_BIGGER_OR_EQUAL(self, path, "slider_max", "slider_min")

@grepr_dataclass(grepr_fields=["size"])
class SRListMonitor(SRMonitor):
    """
    The second representation exclusively for list monitors
    """

    size: tuple[int | float, int | float]
    
    def validate(self, path: list, info_api: OpcodeInfoAPI):
        """
        Ensure a SRListMonitor is valid, raise MANIP_ValidationError if not
        To validate the exact dropdown values you should additionally call the validate_dropdown_values method
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRListMonitor is invalid
        """
        super().validate(path, info_api)
        AA_EQUAL(self, path, "opcode", NEW_OPCODE_LIST_VALUE)
        
        if get_config().validation.raise_if_monitor_bigger_then_stage:
            max_x, max_y = STAGE_WIDTH, STAGE_HEIGHT
        else:
            max_x, max_y = None, None
        AA_BOXED_COORD_PAIR(self, path, "size", 
            min_x=LIST_MONITOR_MIN_WIDTH , max_x=max_x, 
            min_y=LIST_MONITOR_MIN_HEIGHT, max_y=max_y,
        )


__all__ = [
    "STAGE_WIDTH", "STAGE_HEIGHT", 
    "FRMonitor", "SRMonitor", "SRVariableMonitor", "SRListMonitor",
]