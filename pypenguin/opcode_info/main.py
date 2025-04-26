from typing import Callable

from dataclasses import dataclass, field
from utility     import DualKeyDict, PypenguinClass, PypenguinEnum

from opcode_info.input        import InputInfo
from opcode_info.dropdown     import DropdownInfo
from opcode_info.special_case import SpecialCase, SpecialCaseType

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
    _grepr_fields = ["opcode_type", "inputs", "dropdowns", "can_have_monitor"]
    
    opcode_type: OpcodeType
    inputs: DualKeyDict[str, str, InputInfo] = field(default_factory=DualKeyDict)
    dropdowns: DualKeyDict[str, str, DropdownInfo] = field(default_factory=DualKeyDict)
    can_have_monitor: bool = False
    special_cases: dict[SpecialCaseType, SpecialCase] = field(default_factory=dict)

    # Special Cases
    def add_special_case(self, special_case: SpecialCase) -> None:
        self.special_cases[special_case.type] = special_case
    def get_special_case(self, case_type: SpecialCaseType) -> SpecialCase | None:
        return self.special_cases.get(case_type, None)

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
    
    # Fetching all new ids
    def get_all_new_input_ids(self) -> list[str]:
        return list(self.inputs.keys_key2())
    def get_all_new_dropdown_ids(self) -> list[str]:
        return list(self.dropdowns.keys_key2())

@dataclass
class OpcodeInfoGroup:
    _grepr = True
    _grepr_fields = ["name", "opcode_info"]

    name: str
    opcode_info: DualKeyDict[str, str, OpcodeInfo]

    def add_opcode(self, old_opcode: str, new_opcode: str, opcode_info: OpcodeInfo) -> None:
        self.opcode_info.set(
            key1  = old_opcode, 
            key2  = new_opcode, 
            value = opcode_info,
        )

class OpcodeInfoAPI(PypenguinClass):
    _grepr = True
    _grepr_fields = ["opcode_info", "old_conversion_listeners"]

    opcode_info: DualKeyDict[str, str, OpcodeInfo]

    def __init__(self):
        self.opcode_info = DualKeyDict()

    # Add Special Cases
    def add_opcode_case(self, opcode: str, special_case: SpecialCase) -> None:
        assert isinstance(opcode, str)
        opcode_info = self.get_info_by_old(opcode)
        opcode_info.add_special_case(special_case)
    
    def add_opcodes_case(self, opcodes: set[str], special_case: SpecialCase) -> None:
        assert isinstance(opcodes, set)
        for opcode in opcodes:
            self.add_opcode_case(opcode, special_case)

    # Add Categories/Extensions
    def add_group(self, group: OpcodeInfoGroup) -> None:
        for old_opcode, new_opcode, opcode_info in group.opcode_info.items_key1_key2():
            if self.opcode_info.has_key1(old_opcode) or self.opcode_info.has_key2(new_opcode):
                raise ValueError(f"Mustn't add opcode {(old_opcode, new_opcode)} twice")
            self.opcode_info.set(
                key1  = old_opcode,
                key2  = new_opcode,
                value = opcode_info,
            )
    
    # Get new opcode for old opcode
    def get_new_by_old_safe(self, old: str) -> str | None:
        # add listener for this conversion too, when needed
        if self.opcode_info.has_key1(old):
            return self.opcode_info.get_key2_for_key1(old)
        return None
    def get_new_by_old(self, old: str) -> str:
        new = self.get_new_by_old_safe(old)
        if new is not None:
            return new
        raise ValueError(f"Didn't find new opcode for old opcode {repr(old)}")
    
    # Get old opcode for new opcode
    def get_old_by_new_safe(self, new: str) -> str:
        if self.opcode_info.has_key2(new):
            return self.opcode_info.get_key1_for_key2(new)
        return None
    def get_old_by_new(self, new: str) -> str:
        old = self.get_old_by_new_safe(new)
        if old is not None:
            return old
        raise ValueError(f"Didn't find old opcode for new opcode {repr(new)}")
    
    # Fetching info by old opcode
    def get_info_by_old_safe(self, old: str) -> InputInfo | None:
        if self.opcode_info.has_key1(old):
            return self.opcode_info.get_by_key1(old)
        return None
    def get_info_by_old(self, old: str) -> InputInfo:
        info = self.get_info_by_old_safe(old)
        if info is not None:
            return info
        raise ValueError(f"Didn't find OpcodeInfo by old opcode {repr(old)}")
    
    # Fetching info by new opcode
    def get_info_by_new_safe(self, new: str) -> InputInfo | None:
        if self.opcode_info.has_key2(new):
            return self.opcode_info.get_by_key2(new)
        return None 
    def get_info_by_new(self, new: str) -> InputInfo:
        info = self.get_info_by_new_safe(new)
        if info is not None:
            return info
        raise ValueError(f"Couldn't find OpcodeInfo by new opcode {repr(new)}")
