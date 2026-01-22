from __future__ import annotations
from typing     import Any

from pmp_manip.utility import (
    grepr_dataclass, AA_COORD_PAIR, AA_TYPE,
    AbstractTreePath, HasGreprValidate, MANIP_InvalidValueError,
)


@grepr_dataclass()
class FRComment(HasGreprValidate):
    """
    The first representation for a block. It is very close to the json data in a project
    """
    
    block_id: str | None
    x: int | float
    y: int | float
    width: int | float
    height: int | float
    minimized: bool
    text: str

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> FRComment:
        """
        Deserializes json data into a FRComment
        
        Args:
            data: the json data
        
        Returns:
            the FRComment
        """
        return cls(
            block_id  = data.get("blockId", None),
            x         = data["x"        ],
            y         = data["y"        ],
            width     = data["width"    ],
            height    = data["height"   ],
            minimized = data["minimized"],
            text      = data["text"     ],
        )
    
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRComment into json data
        
        Returns:
            the json data
        """
        return {
            "blockId"  : self.block_id,
            "x"        : self.x,
            "y"        : self.y,
            "width"    : self.width,
            "height"   : self.height,
            "minimized": self.minimized,
            "text"     : self.text,
        }
    
    def to_second(self) -> tuple[bool, SRComment]:
        """
        Converts a FRComment into a SRComment
        
        Returns:
            wether it is an attached comment(True) or a floating comment(False) and the SRComment
        """
        comment = SRComment(
            position=(self.x, self.y),
            size=(self.width, self.height),
            is_minimized=self.minimized,
            text=self.text,
        )
        return (self.block_id is not None, comment)

@grepr_dataclass()
class SRComment(HasGreprValidate):
    """
    The second representation for a comment
    """
    
    position: tuple[int | float, int | float]
    size: tuple[int | float, int | float]
    is_minimized: bool
    text: str
    
    def post_validate(self, path: AbstractTreePath) -> None:
        """
        Ensure an instance is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the instance is invalid
            MANIP_InvalidValueError(MANIP_ValidationError): if size is smaller then the minimum
        """
        if (self.size[0] < 52) or (self.size[1] < 32):
            raise MANIP_InvalidValueError(path, f"size of {self.__class__.__name__} must be at least 52 by 32")

    def to_first(self, block_id: str | None) -> FRComment:
        """
        Converts a SRComment into a FRComment
        
        Args:
            the reference id of the parent block or None if it is a floating comment

        Returns:
            the FRComment
        """
        return FRComment(
            block_id  = block_id,
            x         = self.position[0],
            y         = self.position[1],
            width     = self.size[0],
            height    = self.size[1],
            minimized = self.is_minimized,
            text      = self.text,
        )


__all__ = ["FRComment", "SRComment"]

