from typing      import TYPE_CHECKING, Type
from dataclasses import dataclass, field
from utility     import DualKeyDict, GreprClass, PypenguinEnum

from opcode_info.input        import InputInfo, InputType, InputMode
from opcode_info.dropdown     import DropdownInfo
from opcode_info.special_case import SpecialCase, SpecialCaseType

if TYPE_CHECKING:
    from core.block import FRBlock, TRBlock, SRBlock
    from core.block_api import FRtoTRAPI, ValidationAPI
    from core.block_mutation import FRMutation, SRMutation

class OpcodeType(PypenguinEnum):
    def is_reporter(self) -> bool:
        return self.value[0]

    STATEMENT         = (False, 0)
    ENDING_STATEMENT  = (False, 1)
    HAT               = (False, 2)
    
    STRING_REPORTER   = (True , 3)
    NUMBER_REPORTER   = (True , 4)
    BOOLEAN_REPORTER  = (True , 5)
    
    # Pseudo Blocktypes
    MENU              = (False, 6)
    POLYGON_MENU      = (False, 7) # Exclusively for the "polygon" block
    NOT_RELEVANT      = (False, 8)
    DYNAMIC           = (False, 9)

@dataclass
class OpcodeInfo:
    _grepr = True
    _grepr_fields = ["opcode_type", "inputs", "dropdowns", "can_have_monitor", "old_mutation_cls", "new_mutation_cls"]
    
    opcode_type: OpcodeType
    inputs: DualKeyDict[str, str, InputInfo] = field(default_factory=DualKeyDict)
    dropdowns: DualKeyDict[str, str, DropdownInfo] = field(default_factory=DualKeyDict)
    can_have_monitor: bool = False
    special_cases: dict[SpecialCaseType, SpecialCase] = field(default_factory=dict)
    old_mutation_cls: Type["FRMutation"] | None = field(init=False, default_factory=type(None))
    new_mutation_cls: Type["SRMutation"] | None = field(init=False, default_factory=type(None))
    
    # Special Cases
    def add_special_case(self, special_case: SpecialCase) -> None:
        self.special_cases[special_case.type] = special_case
    def get_special_case(self, case_type: SpecialCaseType) -> SpecialCase | None:
        return self.special_cases.get(case_type, None)

    # Mutation Class
    def set_mutation_classes(self, old_cls: Type["FRMutation"], new_cls: Type["SRMutation"]) -> None:
        self.old_mutation_cls = old_cls
        self.new_mutation_cls = new_cls

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
    
    # Fetching all ids
    def get_all_new_input_ids(self) -> list[str]:
        return list(self.inputs.keys_key2())
    def get_all_new_dropdown_ids(self) -> list[str]:
        return list(self.dropdowns.keys_key2())

    ##############################################################
    #               Methods based on Special Cases               #
    ##############################################################
    
    # Get the opcode type. Avoid OpcodeType.DYNAMIC
    def get_opcode_type(self, block: "TRBlock|SRBlock", validation_api: "ValidationAPI") -> OpcodeType:
        instead_case = self.get_special_case(SpecialCaseType.GET_OPCODE_TYPE)
        if self.opcode_type == OpcodeType.DYNAMIC:
            assert instead_case is not None, "If opcode_type is DYNAMIC, a special case with type GET_OPCODE_TYPE must be defined"
            return instead_case.call(block, validation_api)
        else:
            assert instead_case is None, "If opcode_type is not DYNAMIC, no special case with type GET_OPCODE_TYPE should be defined"
            return self.opcode_type
    
    # Get input ids, types, modes
    def get_input_ids_types(self, 
        block: "FRBlock|TRBlock|SRBlock", block_api: "FRtoTRAPI|None",
    ) -> DualKeyDict[str, str, InputType]:
        """
        :param block: To determine the ids and types e.g. Custom Blocks need the block as context
        :param block_api: only necessary if block is a FRBlock
        :return: DualKeyDict mapping old input id and new input id to input type
        """
        instead_case = self.get_special_case(SpecialCaseType.GET_ALL_INPUT_IDS_TYPES)
        if instead_case is None:
            return DualKeyDict({
                (old_id, new_id): input_info.type
                for old_id, new_id, input_info in self.inputs.items_key1_key2()
            })
        else:
            return instead_case.call(block=block, block_api=block_api)
    
    def get_new_input_ids_types(self, 
        block: "FRBlock|TRBlock|SRBlock", block_api: "FRtoTRAPI|None",
    ) -> dict[str, InputType]:
        """
        :param block: To determine the ids and types e.g. Custom Blocks need the block as context
        :param block_api: only necessary if block is a FRBlock
        :return: dict mapping new input id to input type
        """
        return dict(self.get_input_ids_types(block, block_api).items_key2())
    
    def get_old_input_ids_modes(self, 
        block: "FRBlock|TRBlock|SRBlock", block_api: "FRtoTRAPI|None",
    ) -> dict[str, InputMode]:
        """
        :param block: To determine the ids and types e.g. Custom Blocks need the block as context
        :param block_api: only necessary if block is a FRBlock
        :return: dict mapping old input id to input mode
        """
        return {
            old_id: input_type.get_mode() 
            for old_id, input_type in self.get_input_ids_types(block, block_api).items_key1()
        }
    
    # Get new input id
    def get_old_new_input_ids(self, 
        block: "FRBlock|TRBlock|SRBlock", block_api: "FRtoTRAPI|None",
    ) -> dict[str, str]:
        """
        :param block: To determine the ids e.g. Custom Blocks need the block as context
        :param block_api: only necessary if block is a FRBlock
        :return: dict mapping old input id to new input id
        """
        return dict(self.get_input_ids_types(block, block_api).keys_key1_key2())

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

@dataclass
class OpcodeInfoAPI(GreprClass):
    _grepr = True
    _grepr_fields = ["opcode_info"]

    opcode_info: DualKeyDict[str, str, OpcodeInfo] = field(default_factory=DualKeyDict)

    # Add Special Cases
    def add_opcode_case(self, old_opcode: str, special_case: SpecialCase) -> None:
        assert isinstance(old_opcode, str)
        opcode_info = self.get_info_by_old(old_opcode)
        opcode_info.add_special_case(special_case)
    
    def add_opcodes_case(self, old_opcodes: set[str], special_case: SpecialCase) -> None:
        assert isinstance(old_opcodes, set)
        for old_opcode in old_opcodes:
            self.add_opcode_case(old_opcode, special_case)

    # Set Mutation Classes
    def set_opcode_mutation_classes(self, old_opcode: str, old_cls: Type["FRMutation"], new_cls: Type["SRMutation"]) -> None:
        assert isinstance(old_opcode, str)
        opcode_info = self.get_info_by_old(old_opcode)
        opcode_info.set_mutation_classes(old_cls=old_cls, new_cls=new_cls)
    
    def set_opcodes_mutation_classes(self, old_opcodes: set[str], old_cls: Type["FRMutation"], new_cls: Type["SRMutation"]) -> None:
        assert isinstance(old_opcodes, set)
        for old_opcode in old_opcodes:
            self.set_opcode_mutation_classes(old_opcode, old_cls=old_cls, new_cls=new_cls)

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
    
    # Get all opcodes
    def get_all_new(self) -> list[str]:
        return list(self.opcode_info.keys_key2())
    #def get_all_old(self) -> list[str]:
    #    return list(self.opcode_info.keys_key1())
    
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
    def get_info_by_old_safe(self, old: str) -> OpcodeInfo | None:
        if self.opcode_info.has_key1(old):
            return self.opcode_info.get_by_key1(old)
        return None
    def get_info_by_old(self, old: str) -> OpcodeInfo:
        info = self.get_info_by_old_safe(old)
        if info is not None:
            return info
        raise ValueError(f"Didn't find OpcodeInfo by old opcode {repr(old)}")
    
    # Fetching info by new opcode
    def get_info_by_new_safe(self, new: str) -> OpcodeInfo | None:
        if self.opcode_info.has_key2(new):
            return self.opcode_info.get_by_key2(new)
        return None 
    def get_info_by_new(self, new: str) -> OpcodeInfo:
        info = self.get_info_by_new_safe(new)
        if info is not None:
            return info
        raise ValueError(f"Couldn't find OpcodeInfo by new opcode {repr(new)}")
