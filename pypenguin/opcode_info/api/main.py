from typing      import TYPE_CHECKING, Type, Iterable
from dataclasses import field

from pypenguin.utility import (
    DualKeyDict, grepr_dataclass, PypenguinEnum, 
    UnknownOpcodeError, SameOpcodeTwiceError,
)

from pypenguin.opcode_info.api.input        import InputInfo, InputType, InputMode
from pypenguin.opcode_info.api.dropdown     import DropdownInfo
from pypenguin.opcode_info.api.special_case import SpecialCase, SpecialCaseType

if TYPE_CHECKING:
    from pypenguin.core.block_interface import FirstToInterIF, ValidationIF, SecondToInterIF
    from pypenguin.core.block_mutation  import FRMutation, SRMutation
    from pypenguin.core.block           import FRBlock, IRBlock, SRBlock


class OpcodeType(PypenguinEnum):
    """
    Represents the shape of all blocks with a certain opcode
    """
    
    def is_reporter(self) -> bool:
        """
        Return wether a OpcodeType is a reporter shape
        
        Returns:
            wether a OpcodeType is a reporter shape
        """
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
# TODO: find solution for draw polygon block

@grepr_dataclass(grepr_fields=["opcode_type", "inputs", "dropdowns", "can_have_monitor", "old_mutation_cls", "new_mutation_cls"])
class OpcodeInfo:
    """
    The information about all the blocks with a certain opcode
    """
    
    opcode_type: OpcodeType
    inputs: DualKeyDict[str, str, InputInfo] = field(default_factory=DualKeyDict)
    dropdowns: DualKeyDict[str, str, DropdownInfo] = field(default_factory=DualKeyDict)
    can_have_monitor: bool = False
    special_cases: dict[SpecialCaseType, SpecialCase] = field(default_factory=dict)
    old_mutation_cls: Type["FRMutation"] | None = field(init=False, default_factory=type(None))
    new_mutation_cls: Type["SRMutation"] | None = field(init=False, default_factory=type(None))
    
    # Special Cases
    def add_special_case(self, special_case: SpecialCase) -> None:
        """
        Add special behaviour to a block opcode
        
        Args:
            special_case: The special behaviour to add
        
        Returns:
            None
        """
        self.special_cases[special_case.type] = special_case
    def get_special_case(self, case_type: SpecialCaseType) -> SpecialCase | None:
        """
        Get special behaviour by its SpecialCaseType
        
        Args:
            case_type: The kind of special case to look for
        
        Returns:
            the special case if exists
        """
        return self.special_cases.get(case_type, None)


    # Mutation Class
    def set_mutation_class(self, old_cls: Type["FRMutation"], new_cls: Type["SRMutation"]) -> None:
        """
        Blocks with some opcodes store additional information. For that purpose a mutation class can be added
        
        Args:
            old_cls: the mutation class to use in first representation
            new_cls: the mutation class to use in second representation
        
        Returns:
            None
        """
        self.old_mutation_cls = old_cls
        self.new_mutation_cls = new_cls


    # Info by Old Id
    def get_input_info_by_old(self, old: str) -> InputInfo:
        """
        Get information about an input by its old id
        
        Args:
            old: the old input id
        
        Returns:
            the input information
        """
        return self.inputs.get_by_key1(old)
    def get_dropdown_info_by_old(self, old: str) -> DropdownInfo:
        """
        Get information about an dropdown by its old id
        
        Args:
            old: the old dropdown id
        
        Returns:
            the dropdown information
        """
        return self.dropdowns.get_by_key1(old)
    
    
    # Info by New Id
    def get_input_info_by_new(self, new: str) -> InputInfo:
        """
        Get information about an input by its new id
        
        Args:
            new: the new input id
        
        Returns:
            the input information
        """
        return self.inputs.get_by_key2(new)
    def get_dropdown_info_by_new(self, new: str) -> DropdownInfo:
        """
        Get information about an dropdown by its new id
        
        Args:
            new: the new dropdown id
        
        Returns:
            the dropdown information
        """
        return self.dropdowns.get_by_key2(new)


    # Old Id -> New Id
    def get_new_input_id(self, old: str) -> str:
        """
        Get the new input id by its old id
        
        Args:
            old: the old input id
        
        Returns:
            the new input id
        """
        return self.inputs.get_key2_for_key1(old)
    def get_new_dropdown_id(self, old: str) -> str:
        """
        Get the new dropdown id by its old id
        
        Args:
            old: the old dropdown id
        
        Returns:
            the new dropdown id
        """
        return self.dropdowns.get_key2_for_key1(old)
    
    
    # New Id -> Old Id
    def get_old_input_id(self, new: str) -> str:
        """
        Get the old input id by its new id
        
        Args:
            new: the new input id
        
        Returns:
            the old input id
        """
        return self.inputs.get_key1_for_key2(new)
    def get_old_dropdown_id(self, new: str) -> str:
        """
        Get the old dropdown id by its new id
        
        Args:
            new: the new input id
        
        Returns:
            the old dropdown id
        """
        return self.dropdowns.get_key1_for_key2(new)
    
    
    # Fetching all ids
    def get_all_new_input_ids(self) -> list[str]:
        """
        Get all new input ids
        
        Returns:
            all new input ids
        """
        return list(self.inputs.keys_key2())
    def get_all_new_dropdown_ids(self) -> list[str]:
        """
        Get all new dropdown ids
        
        Returns:
            all new dropdown ids
        """
        return list(self.dropdowns.keys_key2())



    ##############################################################
    #               Methods based on Special Cases               #
    ##############################################################
    
    # Get the opcode type. Avoid OpcodeType.DYNAMIC
    def get_opcode_type(self, block: "IRBlock|SRBlock", validation_if: "ValidationIF") -> OpcodeType:
        instead_case = self.get_special_case(SpecialCaseType.GET_OPCODE_TYPE)
        if self.opcode_type == OpcodeType.DYNAMIC:
            assert instead_case is not None, "If opcode_type is DYNAMIC, a special case with type GET_OPCODE_TYPE must be defined"
            return instead_case.call(block, validation_if)
        else:
            assert instead_case is None, "If opcode_type is not DYNAMIC, no special case with type GET_OPCODE_TYPE should be defined"
            return self.opcode_type
    
    # Get input ids, types, modes
    def get_input_ids_types(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> DualKeyDict[str, str, InputType]:
        """
        Get all the old and new inputs ids and their input types
        
        Args:
            block: To determine the ids and types e.g. Custom Blocks need the block as context
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            DualKeyDict mapping old input id and new input id to input type
        """
        instead_case = self.get_special_case(SpecialCaseType.GET_ALL_INPUT_IDS_TYPES)
        if instead_case is None:
            return DualKeyDict({
                (old_id, new_id): input_info.type
                for old_id, new_id, input_info in self.inputs.items_key1_key2()
            })
        else:
            return instead_case.call(block=block, fti_if=fti_if)
    
    def get_new_input_ids_types(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> dict[str, InputType]:
        """
        Get all the new inputs ids and their input types
        
        Args:
            block: To determine the ids and types e.g. Custom Blocks need the block as context
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            dict mapping new input id to input type
        """
        return dict(self.get_input_ids_types(block, fti_if).items_key2())
    
    def get_old_input_ids_modes(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> dict[str, InputMode]:
        """
        Get all the old inputs ids and their input modes
        
        Args:
            block: To determine the ids and types e.g. Custom Blocks need the block as context
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            dict mapping old input id to input mode
        """
        return {
            old_id: input_type.get_mode() 
            for old_id, input_type in self.get_input_ids_types(block, fti_if).items_key1()
        }
    
    def get_old_new_input_ids(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> dict[str, str]:
        """
        Get all the old and new input ids
        
        Args:
            block: To determine the ids and types e.g. Custom Blocks need the block as context
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            dict mapping old input id to new input id
        """
        return dict(self.get_input_ids_types(block, fti_if).keys_key1_key2())
    
    def get_new_old_input_ids(self, 
        block: "FRBlock|IRBlock|SRBlock",
    ) -> dict[str, str]:
        """
        Get all the new and old input ids
        
        Args:
            block: To determine the ids and types e.g. Custom Blocks need the block as context
        
        Returns:
            dict mapping new input id to old input id
        """
        return {new: old for old, new in self.get_input_ids_types(block, None).keys_key1_key2()}
    

@grepr_dataclass(grepr_fields=["name", "opcode_info"])
class OpcodeInfoGroup:
    """
    Represents a group of block opcode information. 
    Therefore it's used to represent opcode information about categories and extensions
    """

    name: str
    opcode_info: DualKeyDict[str, str, OpcodeInfo]

    def add_opcode(self, old_opcode: str, new_opcode: str, opcode_info: OpcodeInfo) -> None:
        """
        Add an opcode to a OpcodeInfoGroup with information about it
        
        Args:
            old_opcode: the old opcode referencing opcode_info
            new_opcode: the new opcode referencing opcode_info
            opcode_info: the information about that opcode, which will be fetchable by old_opcode or new_opcode
        
        Returns:
            None
        """
        self.opcode_info.set(
            key1  = old_opcode, 
            key2  = new_opcode, 
            value = opcode_info,
        )

@grepr_dataclass(grepr_fields=["opcode_info"])
class OpcodeInfoAPI:
    """
    API which provides a way to fetch information about block opcodes
    """

    opcode_info: DualKeyDict[str, str, OpcodeInfo] = field(default_factory=DualKeyDict)

    # Add Special Cases
    def add_opcode_case(self, old_opcode: str, special_case: SpecialCase) -> None:
        """
        Add a special case to the information about an opcode
        
        Args:
            old_opcode: the old opcode referencing the target opcode information
            special_case: the special behaviour to add
        
        Returns:
            None
        """
        assert isinstance(old_opcode, str)
        opcode_info = self.get_info_by_old(old_opcode)
        opcode_info.add_special_case(special_case)
    
    def add_opcodes_case(self, old_opcodes: Iterable[str], special_case: SpecialCase) -> None:
        """
        Add a special case to the information about multiple opcodes
        
        Args:
            old_opcodes: the old opcodes referencing the target opcode information
            special_case: the special behaviour to add
        
        Returns:
            None
        """
        assert isinstance(old_opcodes, set)
        for old_opcode in old_opcodes:
            self.add_opcode_case(old_opcode, special_case)

    # Set Mutation Classes
    def set_opcode_mutation_class(self, old_opcode: str, old_cls: Type["FRMutation"], new_cls: Type["SRMutation"]) -> None:
        """
        Blocks with some opcodes store additional information. 
        For that purpose a mutation class can be added to a given opcode
        
        Args:
            old_opcodes: the old opcodes referencing the target opcode information
            old_cls: the mutation class to use in first representation
            new_cls: the mutation class to use in second representation            
        
        Returns:
            None
        """
        assert isinstance(old_opcode, str)
        opcode_info = self.get_info_by_old(old_opcode)
        opcode_info.set_mutation_class(old_cls=old_cls, new_cls=new_cls)
    
    def set_opcodes_mutation_class(self, 
        old_opcodes: Iterable[str], 
        old_cls: Type["FRMutation"], 
        new_cls: Type["SRMutation"],
    ) -> None:
        """
        Blocks with some opcodes store additional information. 
        For that purpose a mutation class can be added to the given opcodes
        
        Args:
            old_opcodes: the old opcodes referencing the target opcode information
            old_cls: the mutation class to use in first representation
            new_cls: the mutation class to use in second representation            
        
        Returns:
            None
        """
        assert isinstance(old_opcodes, set)
        for old_opcode in old_opcodes:
            self.set_opcode_mutation_class(old_opcode, old_cls=old_cls, new_cls=new_cls)

    # Add Categories/Extensions
    def add_group(self, group: OpcodeInfoGroup) -> None:
        """
        Add a category or extension to the API
        
        Args:
            group: the category or extension
        
        Returns:
            None       
        """
        for old_opcode, new_opcode, opcode_info in group.opcode_info.items_key1_key2():
            if self.opcode_info.has_key1(old_opcode) or self.opcode_info.has_key2(new_opcode):
                raise SameOpcodeTwiceError(f"Must not add opcode {(old_opcode, new_opcode)} twice")
            self.opcode_info.set(
                key1  = old_opcode,
                key2  = new_opcode,
                value = opcode_info,
            )
    
    
    # Get all opcodes
    def get_all_new(self) -> list[str]:
        """
        Get a list of all new opcodes
        
        Returns:
            a list of all new opcodes
        """
        return list(self.opcode_info.keys_key2())
    def get_all_old(self) -> list[str]:
        """
        Get a list of all old opcodes
        
        Returns:
            a list of all old opcodes
        """
        return list(self.opcode_info.keys_key1())
    
    
    # Get new opcode for old opcode
    def get_new_by_old_safe(self, old: str) -> str | None:
        """
        Safely get the new opcode for an old opcode, return None if the old opcode is unknown.
        Use this one, if you want to handle the unknown case yourself
        
        Args:
            old: the old opcode
        
        Returns:
            the new opcode or None if the old opcode is unknown
        """
        if self.opcode_info.has_key1(old):
            return self.opcode_info.get_key2_for_key1(old)
        return None
    def get_new_by_old(self, old: str) -> str:
        """
        Get the new opcode for an old opcode, raise UnknownOpcodeError if the old opcode is unknown.
        Use this one, if you do NOT want to handle the unknown case yourself
        
        Args:
            old: the old opcode
        
        Returns:
            the new opcode
        """
        new = self.get_new_by_old_safe(old)
        if new is not None:
            return new
        raise UnknownOpcodeError(f"Could not find new opcode for old opcode {repr(old)}")
    
    
    # Get old opcode for new opcode
    def get_old_by_new_safe(self, new: str) -> str:
        """
        Safely get the old opcode for an new opcode, return None if the new opcode is unknown.
        Use this one, if you want to handle the unknown case yourself
        
        Args:
            new: the new opcode
        
        Returns:
            the old opcode or None if the new opcode is unknown
        """
        if self.opcode_info.has_key2(new):
            return self.opcode_info.get_key1_for_key2(new)
        return None
    def get_old_by_new(self, new: str) -> str:
        """
        Get the old opcode for an new opcode, raise UnknownOpcodeError if the new opcode is unknown.
        Use this one, if you do NOT want to handle the unknown case yourself
        
        Args:
            new: the new opcode
        
        Returns:
            the old opcode
        """
        old = self.get_old_by_new_safe(new)
        if old is not None:
            return old
        raise UnknownOpcodeError(f"Could not find old opcode for new opcode {repr(new)}")
    
    
    # Fetching info by old opcode
    def get_info_by_old_safe(self, old: str) -> OpcodeInfo | None:
        """
        Safely get the opcode information by old opcode, return None if the old opcode is unknown.
        Use this one, if you want to handle the unknown case yourself
        
        Args:
            old: the old opcode
        
        Returns:
            the opcode information or None if the old opcode is unknown
        """
        if self.opcode_info.has_key1(old):
            return self.opcode_info.get_by_key1(old)
        return None
    def get_info_by_old(self, old: str) -> OpcodeInfo:
        """
        Get the opcode infotamtion by old opcode, raise UnknownOpcodeError if the old opcode is unknown.
        Use this one, if you do NOT want to handle the unknown case yourself
        
        Args:
            old: the old opcode
        
        Returns:
            the opcode information
        """
        info = self.get_info_by_old_safe(old)
        if info is not None:
            return info
        raise UnknownOpcodeError(f"Could not find OpcodeInfo by old opcode {repr(old)}")
    
    
    # Fetching info by new opcode
    def get_info_by_new_safe(self, new: str) -> OpcodeInfo | None:
        """
        Safely get the opcode information by new opcode, return None if the new opcode is unknown.
        Use this one, if you want to handle the unknown case yourself
        
        Args:
            new the new opcode
        
        Returns:
            the opcode information or None if the new opcode is unknown
        """
        if self.opcode_info.has_key2(new):
            return self.opcode_info.get_by_key2(new)
        return None 
    def get_info_by_new(self, new: str) -> OpcodeInfo:
        """
        Get the opcode infotamtion by new opcode, raise UnknownOpcodeError if the new opcode is unknown.
        Use this one, if you do NOT want to handle the unknown case yourself
        
        Args:
            new: the new opcode
        
        Returns:
            the opcode information
        """
        info = self.get_info_by_new_safe(new)
        if info is not None:
            return info
        raise UnknownOpcodeError(f"Could not find OpcodeInfo by new opcode {repr(new)}")


__all__ = ["OpcodeType", "OpcodeInfo", "OpcodeInfoGroup", "OpcodeInfoAPI"]

