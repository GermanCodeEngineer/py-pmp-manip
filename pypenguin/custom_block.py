from enum import Enum
from config import ConfigSetting, ConfigType, FRtoSRApi, config
from block_opcodes import *
from block_info import InputType, InputMode
from utility import PypenguinClass

class SRCustomOpcode(PypenguinClass):
    _grepr = True
    _grepr_fields = ["proccode", "arguments"]

    proccode: str
    arguments: dict[str, "SRCustomArgumentType"]

    def __init__(self, proccode: str, argument_names: list[str], argument_defaults: list[str]):
        self.proccode = proccode
        self.arguments = {
            name: SRCustomArgumentType.get_by_default(default)
            for name, default in zip(argument_names, argument_defaults)
        }
        

class SRCustomArgumentType(Enum):
    STRING_NUMBER = 0
    BOOLEAN       = 1

    def __repr__(self):
        return self.__class__.__name__ + "." + self.name
     
    @staticmethod
    def get_by_default(default):
        match default:
            case "":
                return SRCustomArgumentType.STRING_NUMBER
            case "false":
                return SRCustomArgumentType.BOOLEAN
            case _:
                raise ValueError()

class SRCustomBlockOptype(Enum):
    STATEMENT         = 0
    ENDING_STATEMENT  = 1
    
    STRING_REPORTER   = 2
    NUMBER_REPORTER   = 3
    BOOLEAN_REPORTER  = 4
    
    def __repr__(self):
        return self.__class__.__name__ + "." + self.name

    @staticmethod
    def from_string(string):
        match string:
            case None       : return SRCustomBlockOptype.STATEMENT
            case "statement": return SRCustomBlockOptype.STATEMENT
            case "end"      : return SRCustomBlockOptype.ENDING_STATEMENT
            case "string"   : return SRCustomBlockOptype.STRING_REPORTER
            case "number"   : return SRCustomBlockOptype.NUMBER_REPORTER
            case "boolean"  : return SRCustomBlockOptype.BOOLEAN_REPORTER
            case _: raise ValueError()


def PRE__CB_DEF(block_api: FRtoSRApi, block):
    # Transfer mutation from prototype block to definition block
    # Order deletion of the prototype block and its argument blocks
    # Delete "custom_block" input, which references the prototype
    prototype_id    = block.inputs["custom_block"][1]
    prototype_block = block_api.get_block(prototype_id)
    block.mutation  = prototype_block.mutation
    block_api.schedule_block_deletion(prototype_id)
    del block.inputs["custom_block"]
     
    for block2_id, block2 in block_api.get_all_blocks().items():
        if block2.parent == prototype_id:
            block_api.schedule_block_deletion(block2_id)
    return block
    
config.add_opcodes_event(
    opcodes=ANY_OPCODE_CB_DEF, 
    event=ConfigSetting(
        type=ConfigType.PRE_FR_STEP, 
        function=PRE__CB_DEF,
    ),
)

def PRE__CB_ARG(block_api: FRtoSRApi, block):
    # Transfer argument name from a field into the mutation
    # because only real dropdowns should be listed in "fields"
    block.mutation.set_argument_name(block.fields["VALUE"][0])
    del block.fields["VALUE"]
    return block

config.add_opcodes_event(
    opcodes=ANY_OPCODE_CB_ARG,
    event=ConfigSetting(
        type=ConfigType.PRE_FR_STEP, 
        function=PRE__CB_ARG,
    ),
)

def PRE__CB_CALL(block_api: FRtoSRApi, block):
    cb_mutation = block_api.get_cb_mutation(block.mutation.proccode)
    new_inputs = {}
    for input_id, input_value in block.inputs.items():
        argument_index = cb_mutation.argument_ids.index(input_id)
        argument_name  = cb_mutation.argument_names[argument_index]
        new_inputs[argument_name] = input_value
    block.inputs = new_inputs
    return block

def INSTEAD__CB_PROTOTYPE(block_api: FRtoSRApi, block) -> "SRBlock":
    # Return an empty, temporary block
    from block import SRBlock
    return SRBlock(
        opcode       = block.opcode,
        inputs       = {},
        dropdowns    = {},
        position     = None,
        comment      = None, # Can't possibly have a comment
        mutation     = None,
        next         = None,
        is_top_level = False,
    )

config.add_event(
    opcode=OPCODE_CB_PROTOTYPE,
    event=ConfigSetting(
        type=ConfigType.INSTEAD_FR_STEP,
        function=INSTEAD__CB_PROTOTYPE,
    ),
)

def INSTEAD_GET_MODES__CB_CALL(block_api: FRtoSRApi, block) -> dict[str, InputMode]:
    # Get the complete mutation
    # Then get the input's index in the triple list system
    # Then get the default and derive the corresponding input mode
    cb_mutation = block_api.get_cb_mutation(block.mutation.proccode)
    input_modes = {}
    for input_id in block.inputs.keys():
        argument_index = cb_mutation.argument_ids.index(input_id)
        argument_default = cb_mutation.argument_defaults[argument_index]
        input_modes[input_id] = InputType.get_by_cb_default(argument_default).get_mode()
    return input_modes

config.add_event(
    opcode=OPCODE_CB_CALL,
    event=ConfigSetting(
        type=ConfigType.INSTEAD_FR_STEP_INPUTS_GET_MODES, 
        function=INSTEAD_GET_MODES__CB_CALL,
    ),
)
