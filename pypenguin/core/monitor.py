from typing import Any

from utility     import PypenguinClass
from utility     import AA_TYPE, AA_DICT_OF_TYPE, AA_COORD_PAIR, AA_EQUAL, AA_BIGGER_OR_EQUAL, InvalidValueValidationError, MissingDropdownError, UnnecessaryDropdownError
from opcode_info import OpcodeInfoApi, DropdownType

from core.dropdown      import SRDropdownValue
from block_opcodes import *
from core.context       import PartialContext

class FRMonitor(PypenguinClass):
    _grepr = True
    _grepr_fields = ["id", "mode", "opcode", "params", "sprite_name", "value", "x", "y", "visible", "width", "height", "slider_min", "slider_max", "is_discrete"]

    id: str
    mode: str
    opcode: str
    params: dict[str, Any]
    sprite_name: str | None
    value: Any
    x: int | float
    y: int | float
    visible: bool
    width: int | float
    height: int | float
    slider_min: int | float | None
    slider_max: int | float | None
    is_discrete: bool | None

    def __init__(self, 
        id: str,
        mode: str,
        opcode: str,
        params: dict[str, Any],
        sprite_name: str | None,
        value: Any,
        x: int | float,
        y: int | float,
        visible: bool,

        width: int | float,
        height: int | float,
        slider_min: int | float | None,
        slider_max: int | float | None,
        is_discrete: bool | None,
    ):
        # Core Properties
        self.id          = id
        self.mode        = mode
        self.opcode      = opcode
        self.params      = params
        assert isinstance(self.params, dict)
        self.sprite_name = sprite_name
        self.value       = value
        self.x           = x
        self.y           = y
        self.visible     = visible

        # Properties for some opcodes
        self.width       = width
        self.height      = height
        self.slider_min  = slider_min
        self.slider_max  = slider_max
        self.is_discrete = is_discrete

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMonitor":
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
            width       = data["width"     ],
            height      = data["height"    ],
            slider_min  = data.get("sliderMin" , None),
            slider_max  = data.get("sliderMax" , None),
            is_discrete = data.get("isDiscrete", None),
        )
    
    def step(self, info_api: OpcodeInfoApi, sprite_names: list[str]) -> tuple[str | None, "SRMonitor | None"]:
        if ((self.sprite_name not in sprite_names) 
        and (self.sprite_name is not None) 
        and not(self.visible)):
            return None # Delete monitors of non-existing sprites
        
        block_info = info_api.get_info_by_opcode(self.opcode)
        
        new_dropdowns = {}
        for dropdown_id, dropdown_value in self.params.items():
            if   self.opcode == OPCODE_VAR_VALUE:
                new_dropdown_id = "VARIABLE"
                dropdown_type   = DropdownType.VARIABLE
            elif self.opcode == OPCODE_LIST_VALUE:
                new_dropdown_id = "LIST"
                dropdown_type   = DropdownType.LIST
            else:
                new_dropdown_id = block_info.get_new_dropdown_id(dropdown_id)
                dropdown_type   = block_info.get_dropdown_type  (dropdown_id)
            new_dropdowns[new_dropdown_id] = dropdown_type.translate_old_to_new_value(dropdown_value)
        
        if   self.opcode == OPCODE_VAR_VALUE:
            return (self.sprite_name, SRVariableMonitor(
                opcode              = block_info.new_opcode,
                dropdowns           = new_dropdowns,
                position            = (self.x, self.y),
                is_visible          = self.visible,
                slider_min          = self.slider_min,
                slider_max          = self.slider_max,
                allow_only_integers = self.is_discrete,
            ))
        elif self.opcode == OPCODE_LIST_VALUE:
            return (self.sprite_name, SRListMonitor(
                opcode      = block_info.new_opcode,
                dropdowns   = new_dropdowns,
                position    = (self.x, self.y),
                is_visible  = self.visible,
                size        = (self.width, self.height)
            ))
        else:
            return (self.sprite_name, SRMonitor(
                opcode      = block_info.new_opcode,
                dropdowns   = new_dropdowns,
                position    = (self.x, self.y),
                is_visible  = self.visible,
            ))


class SRMonitor(PypenguinClass):
    _grepr = True
    _grepr_fields = ["opcode", "dropdowns", "sprite", "position", "is_visible"]
    
    opcode: str
    dropdowns: dict[str, SRDropdownValue]
    position: tuple[int | float, int | float]
    is_visible: bool
    
    def __init__(self, 
        opcode: str,
        dropdowns: dict[str, SRDropdownValue],
        position: tuple[int | float, int | float],
        is_visible: bool,
    ):
        self.opcode     = opcode
        if   opcode == NEW_OPCODE_VAR_VALUE:
            assert isinstance(self, SRVariableMonitor), f"Must be a SRVariableMonitor instance if opcode is {repr(NEW_OPCODE_VAR_VALUE)}"
        elif opcode == NEW_OPCODE_LIST_VALUE:
            assert isinstance(self, SRListMonitor), f"Must be a SRListMonitor instance if opcode is {repr(NEW_OPCODE_LIST_VALUE)}"
        self.dropdowns  = dropdowns
        self.position   = position
        self.is_visible = is_visible
    
    def validate(self, path: list, info_api: OpcodeInfoApi):
        AA_TYPE(self, path, "opcode", str)
        AA_DICT_OF_TYPE(self, path, "dropdowns", key_t=str, value_t=SRDropdownValue)
        AA_COORD_PAIR(self, path, "position") # TODO: possibly ensure position is on stage
        AA_TYPE(self, path, "is_visible", bool)
        
        block_info = info_api.get_info_by_new_opcode(
            self.opcode, 
            mutation=None, 
            default_none=True,
         )
        if (block_info is None) or (not block_info.can_have_monitor):
            raise InvalidValueValidationError(path, f"opcode of {self.__class__.__name__} must be a defined opcode. That block must be able to have monitors")
        
        new_dropdown_ids = block_info.get_new_dropdown_ids()
        for new_dropdown_id, dropdown_value in self.dropdowns.items():
            dropdown_value.validate(path+["dropdowns", (new_dropdown_id,)])
            if new_dropdown_id not in new_dropdown_ids:
                raise UnnecessaryDropdownError(path, f"dropdowns of {self.__class__.__name__} with opcode {repr(self.opcode)} includes unnecessary dropdown {new_dropdown_id}")
        for new_dropdown_id in new_dropdown_ids:
            if new_dropdown_id not in self.dropdowns:
                raise MissingDropdownError(path, f"dropdowns of {self.__class__.__name__} with opcode {repr(self.opcode)} is missing dropdown {new_dropdown_id}")
    
    def validate_dropdowns_values(self, path: list, info_api: OpcodeInfoApi, context: PartialContext):
        block_info = info_api.get_info_by_new_opcode(
            self.opcode, 
            mutation=None,
            default_none=False,
        )
        for new_dropdown_id, dropdown_value in self.dropdowns.items():
            dropdown_type = block_info.get_dropdown_type_by_new(new_dropdown_id)
            dropdown_value.validate_value(
                path          = path + ["dropdowns", (new_dropdown_id,)],
                dropdown_type = dropdown_type, 
                context       = context,
                inputs        = {},
            )


class SRVariableMonitor(SRMonitor):
    _grepr_fields = SRMonitor._grepr_fields + ["slider_min", "slider_max", "allow_only_integers"]
    
    slider_min: int | float
    slider_max: int | float
    allow_only_integers: bool
    
    def __init__(self, 
        opcode: str,
        dropdowns: dict[str, SRDropdownValue],
        position: tuple[int | float, int | float],
        is_visible: bool,
        slider_min: int | float,
        slider_max: int | float,
        allow_only_integers: bool,
    ):
        super().__init__(
            opcode     = opcode,
            dropdowns  = dropdowns,
            position   = position,
            is_visible = is_visible,
        )
        self.slider_min          = slider_min
        self.slider_max          = slider_max
        self.allow_only_integers = allow_only_integers
    
    def validate(self, path: list, info_api: OpcodeInfoApi):
        super().validate(path, info_api)
        AA_EQUAL(self, path, "opcode", NEW_OPCODE_VAR_VALUE)
        
        AA_TYPE(self, path, "allow_only_integers", bool)
        if self.allow_only_integers:
            condition = "When allow_only_integers is True"
            AA_TYPE(self, path, "slider_min", int, condition=condition)
            AA_TYPE(self, path, "slider_max", int, condition=condition)
        else:
            condition = "When allow_only_integers is False"
            AA_TYPE(self, path, "slider_min", float, condition=condition)
            AA_TYPE(self, path, "slider_max", float, condition=condition)

        AA_BIGGER_OR_EQUAL(self, path, "slider_max", "slider_min")

class SRListMonitor(SRMonitor):
    _grepr_fields = SRMonitor._grepr_fields + ["size"]

    size: tuple[int | float, int | float]
    
    def __init__(self, 
        opcode: str,
        dropdowns: dict[str, SRDropdownValue],
        position: tuple[int | float, int | float],
        is_visible: bool,
        size: tuple[int | float, int | float],
    ):
        super().__init__(
            opcode     = opcode,
            dropdowns  = dropdowns,
            position   = position,
            is_visible = is_visible,
        )
        self.size = size
    
    def validate(self, path: list, info_api: OpcodeInfoApi):
        super().validate(path, info_api)
        AA_EQUAL(self, path, "opcode", NEW_OPCODE_LIST_VALUE)
        
        AA_COORD_PAIR(self, path, "size") # TODO: possibly check maximum width and height

