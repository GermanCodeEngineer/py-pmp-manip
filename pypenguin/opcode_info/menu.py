from dataclasses import dataclass

from pypenguin.utility import GreprClass

@dataclass
class MenuInfo(GreprClass):
    """
    The information about a menu in an input.
    """
    _grepr = True
    _grepr_fields = ["opcode", "inner"]
    
    opcode: str
    inner : str


__all__ = ["MenuInfo"]

