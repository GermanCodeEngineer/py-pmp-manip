from typing import TYPE_CHECKING

from config.basis import SpecialCaseHandler, SpecialCase, SpecialCaseType
from utility import PypenguinClass
from block_info import InputType, InputMode
from block_opcodes import *

if TYPE_CHECKING:
    from block import FRBlock, TRBlock
    from comment import SRAttachedComment
    from block_mutation import FRCustomBlockMutation

class FRtoTRApi(PypenguinClass):
    _grepr = True
    _grepr_fields = ["blocks", "scheduled_block_deletions"]

    blocks: dict[str, "FRBlock"]
    block_comments: dict[str, "SRAttachedComment"]
    scheduled_block_deletions: list[str]    

    def __init__(self, blocks: dict[str, "FRBlock"], block_comments: dict[str, "SRAttachedComment"]):
        self.blocks                    = blocks
        self.block_comments            = block_comments
        self.scheduled_block_deletions = []
    
    def get_all_blocks(self) -> dict[str, "FRBlock"]:
        return self.blocks
    
    def get_block(self, block_id: str) -> "FRBlock":
        return self.get_all_blocks()[block_id]
    
    def schedule_block_deletion(self, block_id: str) -> None:
        self.scheduled_block_deletions.append(block_id)

    def get_cb_mutation(self, proccode: str) -> "FRCustomBlockMutation":
        from block_mutation import FRCustomBlockMutation
        for block in self.blocks.values():
            if not isinstance(block.mutation, FRCustomBlockMutation): continue
            if block.mutation.proccode == proccode:
                return block.mutation
        raise ValueError(f"Mutation of proccode {repr(proccode)} not found.")

    def get_comment(self, comment_id: str) -> "SRAttachedComment":
        return self.block_comments[comment_id]


config = SpecialCaseHandler()
def PRE__CB_DEF(block: "FRBlock", block_api: FRtoTRApi) -> "FRBlock":
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
    event=SpecialCase(
        type=SpecialCaseType.PRE_FR_STEP, 
        function=PRE__CB_DEF,
    ),
)

def PRE__CB_ARG(block: "FRBlock", block_api: FRtoTRApi) -> "FRBlock":
    # Transfer argument name from a field into the mutation
    # because only real dropdowns should be listed in "fields"
    block.mutation.store_argument_name(block.fields["VALUE"][0])
    del block.fields["VALUE"]
    return block

config.add_opcodes_event(
    opcodes=ANY_OPCODE_CB_ARG,
    event=SpecialCase(
        type=SpecialCaseType.PRE_FR_STEP, 
        function=PRE__CB_ARG,
    ),
)

def PRE__CB_CALL(block: "FRBlock", block_api: FRtoTRApi) -> "FRBlock":
    cb_mutation = block_api.get_cb_mutation(block.mutation.proccode)
    new_inputs = {}
    for input_id, input_value in block.inputs.items():
        argument_index = cb_mutation.argument_ids.index(input_id)
        argument_name  = cb_mutation.argument_names[argument_index]
        new_inputs[argument_name] = input_value
    block.inputs = new_inputs
    return block

config.add_event(
    opcode=OPCODE_CB_CALL,
    event=SpecialCase(
        type=SpecialCaseType.PRE_FR_STEP, 
        function=PRE__CB_CALL,
    ),
)

def INSTEAD__CB_PROTOTYPE(block: "FRBlock", block_api: FRtoTRApi) -> "TRBlock":
    # Return an empty, temporary block
    from block import TRBlock
    return TRBlock(
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
    event=SpecialCase(
        type=SpecialCaseType.INSTEAD_FR_STEP,
        function=INSTEAD__CB_PROTOTYPE,
    ),
)

def INSTEAD_GET_MODES__CB_CALL(block: "FRBlock", block_api: FRtoTRApi) -> dict[str, InputMode]:
    # Get the complete mutation
    # Then get the input's index in the triple list system
    # Then get the default and derive the corresponding input mode
    cb_mutation = block_api.get_cb_mutation(block.mutation.proccode)
    input_modes = {}
    #for input_id in block.inputs.keys():
    #    argument_index = cb_mutation.argument_ids.index(input_id)
    #    argument_default = cb_mutation.argument_defaults[argument_index]
    #    input_modes[input_id] = InputType.get_by_cb_default(argument_default).get_mode()
    for argument_index, argument_name in enumerate(cb_mutation.argument_names):
        argument_default = cb_mutation.argument_defaults[argument_index]
        input_modes[argument_name] = InputType.get_by_cb_default(argument_default).get_mode()
    return input_modes

config.add_event(
    opcode=OPCODE_CB_CALL,
    event=SpecialCase(
        type=SpecialCaseType.INSTEAD_FR_STEP_INPUTS_GET_MODES, 
        function=INSTEAD_GET_MODES__CB_CALL,
    ),
)


