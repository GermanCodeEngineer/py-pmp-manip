from typing      import Any
from dataclasses import dataclass

from utility import GreprClass, ValidationConfig
from utility import AA_TYPE, AA_TYPES, AA_LIST_OF_TYPES

@dataclass(repr=False)
class SRVariable(GreprClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
    name: str
    current_value: Any

    def validate(self, path: list, config: ValidationConfig):
        AA_TYPE(self, path, "name", str)
        AA_TYPES(self, path, "current_value", (int, float, str, bool)) # Only these can be saved in Scratch Projects
        #AA_JSON_COMPATIBLE(self, path, "current_value")

class SRCloudVariable(SRVariable):
    pass

@dataclass(repr=False)
class SRList(GreprClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
    name: str
    current_value: list[Any]

    def validate(self, path: list, config: ValidationConfig):
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "current_value", list) # still must be a list
        AA_LIST_OF_TYPES(self, path, "current_value", (int, float, str, bool)) # Only these can be saved in Scratch Projects
        #AA_JSON_COMPATIBLE(self, path, "current_value")


