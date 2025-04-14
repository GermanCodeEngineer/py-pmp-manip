from enum import Enum
from typing import Callable, Iterable
from dataclasses import dataclass

class CEventType(Enum):
    def __repr__(self):
        return f"CET.{self.name}"
    INSTEAD_FR_TO_SR = 0
    POST_FR_TO_SR    = 1


@dataclass
class CEvent:
    type: CEventType
    function: Callable
    
    def __repr__(self):
        return f"CEvent(type={repr(self.type)}, function={self.function.__name__})"

    def call(self, *args, **kwargs):
        return self.function(*args, **kwargs)

class CustomizationHandler:
    _grepr = True
    _grepr_fields = ["events"]

    events: dict[CEventType, dict[str, CEvent]]

    def __init__(self):
        self.events = {}
    
    def add_event(self, opcode: str, event: CEvent):
        if event.type not in self.events:
            self.events[event.type] = {}
        self.events[event.type][opcode] = event
    
    def add_opcodes_event(self, opcodes: Iterable[str], event: CEvent):
        for opcode in opcodes:
            self.add_event(opcode=opcode, event=event)
    
    def get_event(self, event_type: CEventType, opcode: str) -> CEvent | None:
        if event_type not in self.events:
            return None
        if opcode not in self.events[event_type]:
            return None
        return self.events[event_type][opcode]

class CEventBlockAPI:
    def __init__(self, blocks):
        self.blocks                   = blocks
        self.scheduled_block_removals = []
    def get_all_blocks(self):
        return self.blocks
    def get_block(self, block_id: str):
        return self.get_all_blocks()[block_id]
    def schedule_block_removal(self, block_id: str):
        self.scheduled_block_removals.append(block_id)

from block_opcodes import *

ch = CustomizationHandler()

from custom_block import INSTEAD__CB_DEF
ch.add_opcodes_event(
    opcodes=ANY_OPCODE_CB_DEF, 
    event=CEvent(type=CEventType.INSTEAD_FR_TO_SR, function=INSTEAD__CB_DEF)
)



