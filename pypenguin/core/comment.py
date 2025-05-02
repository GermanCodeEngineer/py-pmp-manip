from typing      import Any
from dataclasses import dataclass

from utility import GreprClass, ValidationConfig
from utility import AA_COORD_PAIR, AA_TYPE, InvalidValueError

@dataclass(repr=False)
class FRComment(GreprClass):
    """
    The first representation for a block. It is very close to the raw data in a project
    """
    _grepr = True
    _grepr_fields = ["block_id", "x", "y", "width", "height", "minimized", "text"]
    
    block_id: str | None
    x: int | float
    y: int | float
    width: int | float
    height: int | float
    minimized: bool
    text: str

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRComment":
        """
        Deserializes raw data into a FRComment
        
        Args:
            data: the raw data
        
        Returns:
            the FRComment
        """
        return cls(
            block_id  = data["blockId"  ],
            x         = data["x"        ],
            y         = data["y"        ],
            width     = data["width"    ],
            height    = data["height"   ],
            minimized = data["minimized"],
            text      = data["text"     ],
        )
    
    def step(self) -> tuple[bool, "SRComment"]:
        """
        Converts a FRComment into a SRComment
        
        Returns:
            wether it is an attached comment(True) or a floating comment(False) and the SRComment
        """
        position = (self.x, self.y)
        size = (self.width, self.height)
        comment = SRComment(
            position=position,
            size=size,
            is_minimized=self.minimized,
            text=self.text,
        )
        return (self.block_id is not None, comment)

@dataclass(repr=False)
class SRComment(GreprClass):
    """
    The second representation for a comment
    """
    _grepr = True
    _grepr_fields = ["position", "size", "is_minimized", "text"]
    
    position: tuple[int | float, int | float]
    size: tuple[int | float, int | float]
    is_minimized: bool
    text: str
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRComment is valid, raise ValidationError if not.
        
        Args:
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        """
        AA_COORD_PAIR(self, path, "position")
        AA_COORD_PAIR(self, path, "size")
        if (self.size[0] < 52) or (self.size[1] < 32):
            raise InvalidValueError(path, f"size of {self.__class__.__name__} must be at least 52 by 32")
        AA_TYPE(self, path, "is_minimized", bool)
        AA_TYPE(self, path, "text", str)

