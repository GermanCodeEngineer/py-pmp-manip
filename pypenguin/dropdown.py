from typing import Any
from enum import Enum

from utility import PypenguinClass

class SRDropdownKind(Enum):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"
    
    STANDARD       =  0
    VARIABLE       =  1
    LIST           =  2
    
    STAGE          =  3
    SPRITE         =  4
    MYSELF         =  5
    OBJECT         =  6

    COSTUME        =  7
    BACKDROP       =  8
    SOUND          =  9

    FONT           = 10
    SUGGESTED_FONT = 11

    FALLBACK       = 12

class SRDropdownValue(PypenguinClass):
    _grepr = True
    _grepr_fields = ["kind", "value"]

    kind: SRDropdownKind
    value: Any
    
    def __init__(self, kind: SRDropdownKind, value: Any):
        self.kind  = kind
        self.value = value
