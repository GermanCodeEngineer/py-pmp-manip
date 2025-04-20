from typing import Any

from utility import PypenguinClass

class SRVariable(PypenguinClass):
    _grepr = True
    _grepr_fields = ["current_value"]
    
    current_value: Any
    
    def __init__(self, current_value: Any):
        self.current_value = current_value


class SRSpriteOnlyVariable(SRVariable):
    pass

class SRAllSpriteVariable(SRVariable):
    pass

class SRCloudVariable(SRAllSpriteVariable):
    pass


class SRList(PypenguinClass):
    _grepr = True
    _grepr_fields = ["current_value"]
    
    current_value: list[Any]
    
    def __init__(self, current_value: list[Any]):
        self.current_value = current_value

class SRSpriteOnlyList(SRList):
    pass

class SRAllSpriteList(SRList):
    pass


