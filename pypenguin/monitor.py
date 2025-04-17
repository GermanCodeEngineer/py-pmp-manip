from typing import Any

from utility import PypenguinClass

class FRMonitor(PypenguinClass):
    _grepr = True
    _grepr_fields = ["id", "mode", "opcode", "params", "sprite_name", "value", "width", "height", "x", "y", "visible", "slider_min", "slider_max", "is_discrete"]

    id: str
    mode: str
    opcode: str
    params: dict[str, Any]
    sprite_name: str | None
    value: Any
    width: int | float
    height: int | float
    x: int | float
    y: int | float
    visible: bool
    slider_min: int | float | None
    slider_max: int | float | None
    is_discrete: bool | None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMonitor":
        self = cls()
        self.id          = data["id"        ] 
        self.mode        = data["mode"      ] 
        self.opcode      = data["opcode"    ] 
        self.params      = data["params"    ] 
        self.sprite_name = data["spriteName"] 
        self.value       = data["value"     ]
        self.width       = data["width"     ]
        self.height      = data["height"    ]
        self.x           = data["x"         ]
        self.y           = data["y"         ]
        self.visible     = data["visible"   ]
        self.slider_min  = data.get("sliderMin" )
        self.slider_max  = data.get("sliderMax" )
        self.is_discrete = data.get("isDiscrete")
        return self
