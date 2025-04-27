from typing      import Any
from dataclasses import dataclass

from utility import GreprClass
from utility import AA_TYPE, AA_JSON_COMPATIBLE

@dataclass(repr=False)
class SRVariable(GreprClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
    name: str
    current_value: Any

    def validate(self, path: list):
        AA_TYPE(self, path, "name", str)
        AA_JSON_COMPATIBLE(self, path, "current_value") # TODO: check wether these are all possible to use in Scratch

class SRSpriteOnlyVariable(SRVariable):
    pass

class SRAllSpriteVariable(SRVariable):
    pass

class SRCloudVariable(SRAllSpriteVariable):
    pass

@dataclass(repr=False)
class SRList(GreprClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
    name: str
    current_value: list[Any]

    def validate(self, path: list):
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "current_value", list) # still must be a list
        AA_JSON_COMPATIBLE(self, path, "current_value") # TODO: check wether these are all possible to use in Scratch       


class SRSpriteOnlyList(SRList):
    pass

class SRAllSpriteList(SRList):
    pass


