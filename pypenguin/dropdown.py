from typing import Any
from enum import Enum

from utility import PypenguinClass

class SRDropdownKind(Enum):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"
    
    STANDARD       =  0
    VARIABLE       =  1
    LIST           =  2
    BROADCAST_MSG  =  3
    
    STAGE          =  4
    SPRITE         =  5
    MYSELF         =  6
    OBJECT         =  7

    COSTUME        =  8
    BACKDROP       =  9
    SOUND          = 10
    
    FONT           = 11
    SUGGESTED_FONT = 12

    FALLBACK       = 13

class SRDropdownValue(PypenguinClass):
    _grepr = True
    _grepr_fields = ["kind", "value"]

    kind: SRDropdownKind
    value: Any
    
    def __init__(self, kind: SRDropdownKind, value: Any):
        self.kind  = kind
        self.value = value
