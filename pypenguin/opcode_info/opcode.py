from dataclasses import dataclass
from utility     import DualKeyDict, PypenguinClass, PypenguinEnum

from opcode_info.input      import InputInfo
from opcode_info.dropdown   import DropdownInfo

class OpcodeType(PypenguinEnum):
    STATEMENT         = 0
    ENDING_STATEMENT  = 1
    HAT               = 2
    
    STRING_REPORTER   = 3
    NUMBER_REPORTER   = 4
    BOOLEAN_REPORTER  = 5
    
    # Pseudo Blocktypes
    MENU              = 6
    POLYGON_MENU      = 7 # Exclusively for the "polygon" block
    NOT_RELEVANT      = 8
    DYNAMIC           = 9

@dataclass
class OpcodeInfo:
    _grepr = True
    _grepr_fields = ["block_type", "inputs", "dropdowns", "can_have_monitor"]
    
    block_type: OpcodeType
    inputs: DualKeyDict[str, str, InputInfo]
    dropdowns: DualKeyDict[str, str, DropdownInfo]
    can_have_monitor: bool
    alt_opcode_prefix: str | None

    # Info by Old Id
    def get_input_info_by_old(self, old: str) -> InputInfo:
        return self.inputs.get_by_key1(old)
    def get_dropdown_info_by_old(self, old: str) -> DropdownInfo:
        return self.dropdowns.get_by_key1(old)
    
    # Info by New Id
    def get_input_info_by_new(self, new: str) -> InputInfo:
        return self.inputs.get_by_key2(new)
    def get_dropdown_info_by_new(self, new: str) -> DropdownInfo:
        return self.dropdowns.get_by_key2(new)

    # Old Id -> New Id
    def get_new_input_id(self, old: str) -> str:
        return self.inputs.get_key2_for_key1(old)
    def get_new_dropdown_id(self, old: str) -> str:
        return self.dropdowns.get_key2_for_key1(old)
    
    # New Id -> Old Id
    def get_old_input_id(self, new: str) -> str:
        return self.inputs.get_key1_for_key2(new)
    def get_old_dropdown_id(self, new: str) -> str:
        return self.dropdowns.get_key1_for_key2(new)

@dataclass
class OpcodeInfoGroup:
    _grepr = True
    _grepr_fields = ["name", "opcode_info"]

    name: str
    opcode_info: DualKeyDict[str, str, OpcodeInfo]

    def add_opcode(self, old_opcode: str, new_opcode: str, opcode_info: OpcodeInfo):
        self.opcode_info.set(
            key1  = old_opcode, 
            key2  = new_opcode, 
            value = opcode_info,
        )

class OpcodeInfoAPI(PypenguinClass):
    _grepr = True
    _grepr_fields = ["opcode_info"]

    opcode_info: DualKeyDict[str, str, OpcodeInfo]

    def __init__(self):
        self.opcode_info = DualKeyDict()

    def add_group(self, group: OpcodeInfoGroup) -> None:
        for old_opcode, new_opcode, opcode_info in group.opcode_info.items_key1_key2():
            if self.opcode_info.has_key1(old_opcode) or self.opcode_info.has_key2(new_opcode):
                raise ValueError(f"Mustn't add opcode {(old_opcode, new_opcode)} twice")
            self.opcode_info.set(
                key1  = old_opcode,
                key2  = new_opcode,
                value = opcode_info,
            )
    
    def get_info_by_old_safe(self, old: str) -> InputInfo | None:
        if self.opcode_info.has_key1(old):
            return self.opcode_info.get_by_key1(old)
        return None
    
    def get_info_by_old(self, old: str) -> InputInfo:
        info = self.get_info_by_old_safe()
        if info is not None:
            return info
        raise ValueError(f"Didn't find OpcodeInfo by old opcode {repr(old)}")
    
    def get_info_by_new_safe(self, new: str) -> InputInfo | None:
        if self.opcode_info.has_key2(new):
            return self.opcode_info.get_by_key2(new)
        return None
    
    def get_info_by_new(self, new: str) -> InputInfo:
        info = self.get_info_by_new_safe()
        if info is not None:
            return info
        raise ValueError(f"Couldn't find OpcodeInfo by new opcode {repr(new)}")
