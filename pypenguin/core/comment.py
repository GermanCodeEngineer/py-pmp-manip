from typing import Any

from utility import PypenguinClass
from utility import AA_COORD_PAIR, AA_TYPE, InvalidValueValidationError

class FRComment(PypenguinClass):
    _grepr = True
    _grepr_fields = ["block_id", "x", "y", "width", "height", "minimized", "text"]
    
    block_id: str | None
    x: int | float
    y: int | float
    width: int | float
    height: int | float
    minimized: bool
    text: str
    
    def __init__(self, 
        block_id: str | None,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        minimized: bool,
        text: str,
    ):
        self.block_id  = block_id
        self.x         = x
        self.y         = y
        self.width     = width
        self.height    = height
        self.minimized = minimized
        self.text      = text

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRComment":
        return cls(
            block_id  = data["blockId"  ],
            x         = data["x"        ],
            y         = data["y"        ],
            width     = data["width"    ],
            height    = data["height"   ],
            minimized = data["minimized"],
            text      = data["text"     ],
        )
    
    def step(self) -> "SRComment":
        position = (self.x, self.y)
        size = (self.width, self.height)
        if self.block_id is None: 
            return SRFloatingComment(
                position=position,
                size=size,
                is_minimized=self.minimized,
                text=self.text,
            )
        else:
            return SRAttachedComment(
                position=position,
                size=size,
                is_minimized=self.minimized,
                text=self.text,
            )

class SRComment(PypenguinClass):
    _grepr = True
    _grepr_fields = ["position", "size", "is_minimized", "text"]
    
    position: tuple[int | float, int | float]
    size: tuple[int | float, int | float]
    is_minimized: bool
    text: str
    
    def __init__(self, 
        position: tuple[int | float, int | float], 
        size: tuple[int | float, int | float], 
        is_minimized: bool, 
        text: str,
    ):
        self.position     = position
        self.size         = size
        self.is_minimized = is_minimized
        self.text         = text
    
    def validate(self, path: list) -> None:
        AA_COORD_PAIR(self, path, "position")
        AA_COORD_PAIR(self, path, "size")
        if (self.size[0] < 52) or (self.size[1] < 32):
            raise InvalidValueValidationError(path, f"size of {self.__class__.__name__} must be at least 52 by 32")
        AA_TYPE(self, path, "is_minimized", bool)
        AA_TYPE(self, path, "text", str)

class SRFloatingComment(SRComment):
    pass

class SRAttachedComment(SRComment):
    pass

