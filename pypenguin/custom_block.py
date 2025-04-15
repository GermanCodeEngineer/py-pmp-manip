from enum import Enum
from customization_handler import CEvent, CEventType, FRtoSRApi, ch
from block_opcodes import *

class SRCustomOpcode:
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


def PRE__CB_DEF(api: FRtoSRApi, block):
    # Transfer mutation from prototype block to definition block
    # Order deletion of the prototype block and its argument blocks
    prototype_id    = block.inputs["custom_block"][1]
    prototype_block = api.get_block(prototype_id)
    block.mutation  = prototype_block.mutation
    api.schedule_block_deletion(prototype_id)
    
    for block2_id, block2 in api.get_all_blocks().items():
        if block2.parent == prototype_id:
            api.schedule_block_deletion(block2_id)
    return block
    
ch.add_opcodes_event(
    opcodes=ANY_OPCODE_CB_DEF, 
    event=CEvent(type=CEventType.PRE_FR_TO_SR, function=PRE__CB_DEF)
)

def PRE__CB_ARG(api: FRtoSRApi, block):
    # Transfer argument name from a field into the mutation
    # because only real dropdowns should be listed in "fields"
    block.mutation.set_argument_name(block.fields["VALUE"][0])
    del block.fields["VALUE"]
    return block

ch.add_opcodes_event(
    opcodes=ANY_OPCODE_CB_ARG,
    event=CEvent(type=CEventType.PRE_FR_TO_SR, function=PRE__CB_ARG)
)




