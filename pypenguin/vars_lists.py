from typing import Any

from utility import PypenguinClass

class SRVariable(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
    name: str
    current_value: Any
    
    def __init__(self, name: str, current_value: Any):
        self.name          = name
        self.current_value = current_value


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
    current_value: Any
    
    def __init__(self, name: str, current_value: Any):
        self.name          = name
        self.current_value = current_value

class SRSpriteOnlyList(SRList):
    pass

class SRAllSpriteList(SRList):
    pass


