from block_info.basis import BlockInfoSet

class BlockInfoApi:
    _grepr = True
    _grepr_fields = ["block_info_sets"]

    block_info_sets: list[BlockInfoSet]
    
    def __init__(self):
        self.block_info_sets = []

    def add_block_info_set(self, block_info_set: BlockInfoSet):
        for other_set in self.block_info_sets:
            if other_set.name == block_info_set.name:
                raise ValueError(f"A BlockInfoSet called {repr(block_info_set)} was alredy added")
        self.block_info_sets.append(block_info_set)

    def get_set_by_name(self, name: str):
        for block_info_set in self.block_info_sets:
            if block_info_set.name == name:
                return block_info_set
        raise ValueError(f"Couldn't find BlockInfoSet {repr(name)}")
    
    def get_sets_by_prefix(self, prefix: str) -> list[BlockInfoSet]:
        sets = []
        for block_info_set in self.block_info_sets:
            if block_info_set.opcode_prefix == prefix:
                sets.append(block_info_set)
        return sets
    
    def get_block_by_opcode(self, opcode: str):
        set_name = opcode[:opcode.index("_")]
        main_opcode = opcode[opcode.index("_")+1:]
        block_info_set = self.get_set_by_name(set_name)
        return block_info_set.get_block(main_opcode, default_none=True)


info_api = BlockInfoApi()
from block_info.motion import motion
info_api.add_block_info_set(motion)

from block_info.looks import looks
info_api.add_block_info_set(looks)

from block_info.sounds import sounds
info_api.add_block_info_set(sounds)

from block_info.events import events
info_api.add_block_info_set(events)

from block_info.control import control
info_api.add_block_info_set(control)

from block_info.sensing import sensing
info_api.add_block_info_set(sensing)

from block_info.operators import operators
info_api.add_block_info_set(operators)

from block_info.variables import variables
info_api.add_block_info_set(variables)

from block_info.lists import lists
info_api.add_block_info_set(lists)
