from typing import Any

from utility import PypenguinClass
from block_info import BlockInfoApi, DropdownType
from dropdown import SRDropdownValue, SRDropdownKind
from block_opcodes import *

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

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMonitor":
        self = cls()
        # Core Properties
        self.id          = data["id"        ] 
        self.mode        = data["mode"      ] 
        self.opcode      = data["opcode"    ] 
        self.params      = data["params"    ] 
        assert isinstance(params, dict)
        self.sprite_name = data["spriteName"] 
        self.value       = data["value"     ]
        self.x           = data["x"         ]
        self.y           = data["y"         ]
        self.visible     = data["visible"   ]
        
        # Properties for some opcodes
        self.width       = data["width"     ]
        self.height      = data["height"    ]
        self.slider_min  = data.get("sliderMin" , None)
        self.slider_max  = data.get("sliderMax" , None)
        self.is_discrete = data.get("isDiscrete", None)
        return self
    
    def step(self, info_api: BlockInfoApi) -> "SRMonitor | None":
        if (self.sprite_name not in sprite_names) and not(self.visible):
            return None # Delete monitors of non-existing sprites
        
        # TODO: get new opcode
        #opcode = selfData["opcode"]
        #if   opcode == "data_variable":
        #    newOpcode = getOptimizedOpcode(opcode="special_variable_value")
        #elif opcode == "data_listcontents":
        #    newOpcode = getOptimizedOpcode(opcode="special_list_value")
        #else:
        #    newOpcode = getOptimizedOpcode(opcode=opcode)
        
        block_info = info_api.get_info_by_opcode(self.opcode)
        
        new_dropdowns = {}
        for dropdown_id, dropdown_value in self.params.items():
            if   opcode == OPCODE_VAR_VALUE:
                new_dropdown_id = "VARIABLE"
                dropdown_type   = DropdownType.VARIABLE
            elif opcode == OPCODE_LIST_VALUE:
                new_dropdown_id = "LIST"
                dropdown_type   = DropdownType.LIST
            else:
                new_dropdown_id = block_info.get_new_dropdown_id(dropdown_id)
                dropdown_type   = block_info.get_dropdown_type  (dropdown_id)
            new_dropdowns[new_dropdown_id] = dropdown_type.translate_old_to_new_value(dropdown_value)
        
        if   self.opcode == OPCODE_VAR_VALUE:
            return SRVariableMonitor(
                opcode               = self.opcode,
                dropdowns            = new_dropdowns,
                sprite_name          = self.sprite_name,
                position             = (self.x, self.y),
                is_visible           = self.visible,
                slider_min           = self.slider_min,
                slider_max           = self.slider_max,
                allown_only_integers = self.is_discrete,
            )
        elif self.opcode == OPCODE_LIST_VALUE:
            return SRListMonitor(
                opcode      = self.opcode,
                dropdowns   = new_dropdowns,
                sprite_name = self.sprite_name,
                position    = (self.x, self.y),
                is_visible  = self.visible,
                size        = (self.width, self.height)
            )
        else:
            return SRMonitor(
                opcode      = self.opcode,
                dropdowns   = new_dropdowns,
                sprite_name = self.sprite_name,
                position    = (self.x, self.y),
                is_visible  = self.visible,
            )


class SRMonitor(PypenguinClass):
    _grepr = True
    _grepr_fields = ["opcode", "dropdowns", "sprite_name", "position", "is_visible"]
    
    opcode: str
    dropdowns: dict[str, SRDropdownValue]
    sprite_name: str | None # TODO: use sprite object instead of name
    position: tuple[int | float, int | float]
    is_visible: bool
    
    def __init__(self, 
        opcode: str,
        dropdowns: dict[str, SRDropdownValue],
        sprite_name: str | None,
        position: tuple[int | float, int | float],
        is_visible: bool,
    ):
        self.opcode      = opcode
        self.dropdowns   = dropdowns
        self.sprite_name = sprite_name
        self.position    = position
        self.is_visible  = is_visible
    
class SRVariableMonitor(SRMonitor):
    _grepr_fields = SRMonitor._grepr_fields + ["slider_min", "slider_max", "allow_only_integers"]
    
    slider_min: int | float
    slider_max: int | float
    allow_only_integers: bool
    
    def __init__(self, 
        opcode: str,
        dropdowns: dict[str, SRDropdownValue],
        sprite_name: str | None,
        position: tuple[int | float, int | float],
        is_visible: bool,
        slider_min: int | float,
        slider_max: int | float,
        allow_only_integers: bool,
    ):
        super().__init__(
            opcode      = opcode,
            dropdowns   = dropdowns,
            sprite_name = sprite_name,
            position    = position,
            is_visible  = is_visible,
        )
        self.slider_min          = slider_min
        self.slider_max          = slider_max
        self.allow_only_integers = allow_only_integers
    
class SRListMonitor(SRMonitor):
    _grepr_fields = SRMonitor._grepr_fields + ["size"]
    
    size: tuple[int | float, int | float]
    
    def __init__(self, 
        opcode: str,
        dropdowns: dict[str, SRDropdownValue],
        sprite_name: str | None,
        position: tuple[int | float, int | float],
        is_visible: bool,
        size: tuple[int | float, int | float],
    ):
        super().__init__(
            opcode      = opcode,
            dropdowns   = dropdowns,
            sprite_name = sprite_name,
            position    = position,
            is_visible  = is_visible,
        )
        self.size = size
    

