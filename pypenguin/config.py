from enum import Enum
from typing import Callable, Iterable
from dataclasses import dataclass

class ConfigType(Enum):
    def __repr__(self):
        return f"CET.{self.name}"
    PRE_FR_TO_SR     = 0
    INSTEAD_FR_TO_SR = 1


@dataclass
class ConfigSetting:
    type: ConfigType
    function: Callable
    
    def __repr__(self):
        return f"CEvent(type={repr(self.type)}, function={self.function.__name__})"

    def call(self, *args, **kwargs):
        return self.function(*args, **kwargs)

class Configuration:
    _grepr = True
    _grepr_fields = ["events"]

    events: dict[ConfigType, dict[str, ConfigSetting]]

    def __init__(self):
        self.events = {}
    
    def add_event(self, opcode: str, event: ConfigSetting):
        if event.type not in self.events:
            self.events[event.type] = {}
        self.events[event.type][opcode] = event
    
    def add_opcodes_event(self, opcodes: Iterable[str], event: ConfigSetting):
        for opcode in opcodes:
            self.add_event(opcode=opcode, event=event)
    
    def get_event(self, event_type: ConfigType, opcode: str) -> ConfigSetting | None:
        if event_type not in self.events:
            return None
        if opcode not in self.events[event_type]:
            return None
        return self.events[event_type][opcode]

class FRtoSRApi:    
    def __init__(self, blocks):
        self.blocks                    = blocks
        self.scheduled_block_deletions = []
    
    def get_all_blocks(self):
        return self.blocks
    def get_block(self, block_id: str):
        return self.get_all_blocks()[block_id]
    
    def schedule_block_deletion(self, block_id: str):
        self.scheduled_block_deletions.append(block_id)

    def get_cb_mutation(self, proccode: str):
        for block in self.blocks.values():
            if block.mutation is None: continue
            if block.mutation.proccode == proccode:
                return block.mutation
        raise ValueError(f"Mutation of proccode {repr(proccode)} not found.")
    
ch = Configuration()


