from dataclasses import dataclass
from typing      import Callable

from utility import PypenguinEnum, GreprClass

class SpecialCaseType(PypenguinEnum):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"
    
    # FRBlock.step:
    PRE_FR_STEP     = 0
    INSTEAD_FR_STEP = 1
    # FRBlock.step_inputs:
    INSTEAD_FR_STEP_INPUTS_GET_MODES = 2
    
    # TRBlock.step:
    INSTEAD_GET_NEW_INPUT_ID = 3
    
    # SRBlock.validate:
    INSTEAD_GET_ALL_NEW_INPUT_IDS = 4

@dataclass
class SpecialCase(GreprClass):
    _grepr = True
    _grepr_fields = ["type", "function"]

    type: SpecialCaseType
    function: Callable
    
    def call(self, *args, **kwargs):
        return self.function(*args, **kwargs)

