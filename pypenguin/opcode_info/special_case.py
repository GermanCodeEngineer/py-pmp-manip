from dataclasses import dataclass
from typing      import Callable, Iterable

from utility import PypenguinClass, PypenguinEnum

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
class SpecialCase:
    type: SpecialCaseType
    function: Callable
    
    def __repr__(self):
        return f"SpecialCase(type={repr(self.type)}, function={self.function.__name__})"

    def call(self, *args, **kwargs):
        return self.function(*args, **kwargs)

