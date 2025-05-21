from dataclasses import dataclass

from pypenguin.utility import grepr_dataclass

@grepr_dataclass(grepr_fields=["opcode", "inner"])
class MenuInfo:
    """
    The information about a menu in an input
    """
    
    opcode: str
    inner : str


__all__ = ["MenuInfo"]

