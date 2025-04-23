from typing import Any

from utility import PypenguinClass, PypenguinEnum
from utility import AA_TYPE, AA_JSON_COMPATIBLE

class SRDropdownKind(PypenguinEnum):
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
    
    def validate(self, path: list):
        AA_TYPE(self, path, "kind", SRDropdownKind)
        AA_JSON_COMPATIBLE(self, path, "value")
        # TODO: check if value is allowed
