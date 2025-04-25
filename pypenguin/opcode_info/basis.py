from dataclasses import dataclass
from utility import DualKeyDict

@dataclass
class OpcodeInfo:
    _grepr = True
    _grepr_fields = ["block_type", "new_opcode", "inputs", "dropdowns", "can_have_monitor"]
    
    block_type: "BlockType"
    new_opcode: str
    inputs: dict[str, "InputInfo"]
    dropdowns: dict[str, "DropdownInfo"]
    can_have_monitor: bool
    alt_opcode_prefix: str | None
    
    def get_input_info(self, input_id: str) -> "InputInfo":
        return self.inputs[input_id]
    
    def get_dropdown_info(self, dropdown_id: str) -> "DropdownInfo":
        return self.dropdowns[dropdown_id]
    
    def get_input_type(self, input_id: str) -> "InputType":
        return self.get_input_info(input_id).type
    
    def get_dropdown_type(self, dropdown_id: str) -> "DropdownType":
        return self.get_dropdown_info(dropdown_id).type

    def get_input_mode(self, input_id: str) -> "InputMode":
        return self.get_input_type(input_id).get_mode()


    def get_input_type_by_new(self, new_input_id: str) -> "InputType":
        input_id = self.get_old_input_id(new_input_id)
        return self.get_input_type(input_id)
    
    def get_dropdown_type_by_new(self, new_dropdown_id: str) -> "DropdownType":
        dropdown_id = self.get_old_dropdown_id(new_dropdown_id)
        return self.get_dropdown_type(dropdown_id)
    

    def get_new_input_id(self, input_id: str) -> str:
        return self.inputs[input_id].new

    def get_new_dropdown_id(self, dropdown_id: str) -> str:
        return self.dropdowns[dropdown_id].new
    
    def get_new_input_ids(self) -> list[str]:
        return [self.get_new_input_id(input_id) for input_id in self.inputs.keys()]
    
    def get_new_dropdown_ids(self) -> list[str]:
        return [self.get_new_dropdown_id(dropdown_id) for dropdown_id in self.dropdowns.keys()]


    def get_old_input_id(self, new_input_id: str) -> str:
        for input_id, input_info in self.inputs.items():
            if input_info.new == new_input_id:
                return input_id

    def get_old_dropdown_id(self, new_dropdown_id: str) -> str:
        for dropdown_id, dropdown_info in self.dropdowns.items():
            if dropdown_info.new == new_dropdown_id:
                return dropdown_id

OpcodeInfo()
