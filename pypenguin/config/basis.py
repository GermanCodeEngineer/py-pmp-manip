from typing import Callable, Iterable

from utility import PypenguinClass, PypenguinEnum

class SpecialCaseType(PypenguinEnum):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"
    
    # FRBlock.step:
    PRE_FR_STEP     = 10
    INSTEAD_FR_STEP = 11
    # FRBlock.step_inputs:
    INSTEAD_FR_STEP_INPUTS_GET_MODES = 20

class SpecialCase(PypenguinClass):
    type: SpecialCaseType
    function: Callable
    
    def __init__(self, type: SpecialCaseType, function: Callable):
        self.type     = type
        self.function = function

    def __repr__(self):
        return f"CEvent(type={repr(self.type)}, function={self.function.__name__})"

    def call(self, *args, **kwargs):
        return self.function(*args, **kwargs)

class SpecialCaseHandler(PypenguinClass):
    _grepr = True
    _grepr_fields = ["events"]

    events: dict[SpecialCaseType, dict[str, SpecialCase]]

    def __init__(self):
        self.events = {}
    
    def add_event(self, opcode: str, event: SpecialCase) -> None:
        if not isinstance(opcode, str): raise TypeError()
        if event.type not in self.events:
            self.events[event.type] = {}
        self.events[event.type][opcode] = event
    
    def add_opcodes_event(self, opcodes: Iterable[str], event: SpecialCase) -> None:
        if isinstance(opcodes, str): raise TypeError()
        for opcode in opcodes:
            self.add_event(opcode=opcode, event=event)
    
    def get_event(self, event_type: SpecialCaseType, opcode: str) -> SpecialCase | None:
        if event_type not in self.events:
            return None
        if opcode not in self.events[event_type]:
            return None
        return self.events[event_type][opcode]

