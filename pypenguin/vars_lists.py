from typing import Any

from utility import PypenguinClass
from utility import AA_TYPE, AA_JSON_COMPATIBLE

class SRVariable(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
    name: str
    current_value: Any
    
    def __init__(self, name: str, current_value: Any):
        self.name          = name
        self.current_value = current_value

    def validate(self, path: list|None = None):
        path = [] if path is None else path
        AA_TYPE(self, path, "name", str)
        AA_JSON_COMPATIBLE(self, path, "current_value")
        # TODO: check wether these are all possible to use in Scratch       

class SRSpriteOnlyVariable(SRVariable):
    pass

class SRAllSpriteVariable(SRVariable):
    pass

class SRCloudVariable(SRAllSpriteVariable):
    pass


class SRList(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
    name: str
    current_value: list[Any]
    
    def __init__(self, name: str, current_value: Any):
        self.name          = name
        self.current_value = current_value

    def validate(self, path: list|None = None):
        path = [] if path is None else path
        AA_TYPE(self, path, "name", str)
        AA_JSON_COMPATIBLE(self, path, "current_value")
        # TODO: check wether these are all possible to use in Scratch       
        AA_TYPE(self, path, "current_value", list) # still must be a list

class SRSpriteOnlyList(SRList):
    pass

class SRAllSpriteList(SRList):
    pass


