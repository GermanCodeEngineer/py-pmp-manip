from typing import TYPE_CHECKING
from copy   import copy, deepcopy

from pypenguin.important_consts import (
    OPCODE_VAR_VALUE, NEW_OPCODE_VAR_VALUE, OPCODE_LIST_VALUE, NEW_OPCODE_LIST_VALUE, 
    OPCODE_STOP_SCRIPT, OPCODE_CB_PROTOTYPE, ANY_OPCODE_CB_DEF, ANY_OPCODE_CB_ARG, 
    OPCODE_CB_CALL, NEW_OPCODE_CB_CALL, OPCODE_CB_ARG_TEXT, OPCODE_CB_ARG_BOOL, 
    OPCODE_CB_DEF, NEW_OPCODE_CB_DEF, OPCODE_CB_DEF_RET, NEW_OPCODE_CB_DEF_REP,
    SHA256_SEC_LOCAL_ARGUMENT_NAME,
)
from pypenguin.utility          import string_to_sha256, DualKeyDict, InvalidValueError

from pypenguin.opcode_info.api import (
    OpcodeInfo, OpcodeType, OpcodeInfoGroup, OpcodeInfoAPI, 
    InputInfo, InputType, 
    DropdownInfo, DropdownType, 
    SpecialCase, SpecialCaseType,
    MonitorIdBehaviour,
)

from pypenguin.opcode_info.data.c_motion    import c_motion
from pypenguin.opcode_info.data.c_looks     import c_looks
from pypenguin.opcode_info.data.c_sounds    import c_sounds
from pypenguin.opcode_info.data.c_events    import c_events
from pypenguin.opcode_info.data.c_control   import c_control
from pypenguin.opcode_info.data.c_sensing   import c_sensing
from pypenguin.opcode_info.data.c_operators import c_operators
from pypenguin.opcode_info.data.c_variables import c_variables
from pypenguin.opcode_info.data.c_lists     import c_lists

if TYPE_CHECKING:
    from pypenguin.core.block_interface import FirstToInterIF, InterToFirstIF, ValidationIF
    from pypenguin.core.block           import FRBlock, IRBlock, SRBlock

from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockArgumentMutation, FRCustomBlockCallMutation, FRStopScriptMutation, 
    SRCustomBlockMutation, SRCustomBlockArgumentMutation, SRCustomBlockCallMutation, SRStopScriptMutation,
)

c_motion.add_opcode("motion_goto_menu", "#REACHABLE TARGET MENU (GO)", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_motion.add_opcode("motion_glideto_menu", "#REACHABLE TARGET MENU (GLIDE)", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_motion.add_opcode("motion_pointtowards_menu", "#OBSERVABLE TARGET MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

c_looks.add_opcode("looks_costume", "#COSTUME MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_looks.add_opcode("looks_backdrops", "#BACKDROP MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_looks.add_opcode("looks_getinput_menu", "#COSTUME PROPERTY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_looks.add_opcode("looks_changeVisibilityOfSprite_menu", "#SHOW/HIDE SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_looks.add_opcode("looks_getOtherSpriteVisible_menu", "#IS SPRITE VISIBLE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

c_sounds.add_opcode("sound_sounds_menu", "#SOUND MENU", OpcodeInfo( # this is certainly correct
    opcode_type=OpcodeType.MENU,
))

c_control.add_opcode("control_stop_sprite_menu", "#STOP SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_control.add_opcode("control_create_clone_of_menu", "#CLONE TARGET MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_control.add_opcode("control_run_as_sprite_menu", "#RUN AS SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

c_sensing.add_opcode("sensing_touchingobjectmenu", "#TOUCHING OBJECT MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_fulltouchingobjectmenu", "#FULL TOUCHING OBJECT MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_touchingobjectmenusprites", "#TOUCHING OBJECT MENU SPRITES", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_distancetomenu", "#DISTANCE TO MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_keyoptions", "#KEY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_scrolldirections", "#SCROLL DIRECTION MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_of_object_menu", "#OJBECT PROPERTY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_fingeroptions", "#FINGER INDEX MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

c_variables.add_opcode(OPCODE_VAR_VALUE, NEW_OPCODE_VAR_VALUE, OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    dropdowns=DualKeyDict({
        ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
    }),
    can_have_monitor=True,
    monitor_id_behaviour=MonitorIdBehaviour.VARIABLE,
))
c_lists.add_opcode(OPCODE_LIST_VALUE, NEW_OPCODE_LIST_VALUE, OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    dropdowns=DualKeyDict({
        ("LIST", "LIST"): DropdownInfo(DropdownType.LIST),
    }),
    can_have_monitor=True,
    monitor_id_behaviour=MonitorIdBehaviour.LIST,
))

c_custom_blocks = OpcodeInfoGroup(
    name="Custom Opcodes",
    opcode_info=DualKeyDict({
        (OPCODE_CB_DEF, NEW_OPCODE_CB_DEF): OpcodeInfo(
            opcode_type=OpcodeType.HAT,
        ),
        (OPCODE_CB_DEF_RET, NEW_OPCODE_CB_DEF_REP): OpcodeInfo(
            opcode_type=OpcodeType.HAT,
        ),
        (OPCODE_CB_PROTOTYPE, "#CUSTOM BLOCK PROTOTYPE"): OpcodeInfo( # only temporary
            opcode_type=OpcodeType.NOT_RELEVANT,
        ),
        (OPCODE_CB_CALL, NEW_OPCODE_CB_CALL): OpcodeInfo(
            opcode_type=OpcodeType.DYNAMIC,
        ),
        ("procedures_return", "return (VALUE)"): OpcodeInfo(
            opcode_type=OpcodeType.ENDING_STATEMENT,
            inputs=DualKeyDict({
                ("return", "VALUE"): InputInfo(InputType.TEXT),
            }),
        ),
        ("procedures_set", "set (PARAM) to (VALUE)"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("PARAM", "PARAM"): InputInfo(InputType.ROUND),
                ("VALUE", "VALUE"): InputInfo(InputType.TEXT),
            }),
        ),
        (OPCODE_CB_ARG_TEXT, "value of text [ARGUMENT]"): OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
        ),
        (OPCODE_CB_ARG_BOOL, "value of boolean [ARGUMENT]"): OpcodeInfo(
            opcode_type=OpcodeType.BOOLEAN_REPORTER,
        ),
    }),
)

info_api = OpcodeInfoAPI()
info_api.add_group(c_motion       )
info_api.add_group(c_looks        )
info_api.add_group(c_sounds       )
info_api.add_group(c_events       )
info_api.add_group(c_control      )
info_api.add_group(c_sensing      )
info_api.add_group(c_operators    )
info_api.add_group(c_variables    )
info_api.add_group(c_lists        )
info_api.add_group(c_custom_blocks)

# Mutations
info_api.set_opcode_mutation_class(OPCODE_STOP_SCRIPT, old_cls=FRStopScriptMutation, new_cls=SRStopScriptMutation)
info_api.set_opcode_mutation_class(OPCODE_CB_PROTOTYPE, old_cls=FRCustomBlockMutation, new_cls=None)
info_api.set_opcodes_mutation_class(ANY_OPCODE_CB_DEF, old_cls=None, new_cls=SRCustomBlockMutation)
info_api.set_opcodes_mutation_class(ANY_OPCODE_CB_ARG, old_cls=FRCustomBlockArgumentMutation, new_cls=SRCustomBlockArgumentMutation)
info_api.set_opcode_mutation_class(OPCODE_CB_CALL, old_cls=FRCustomBlockCallMutation, new_cls=SRCustomBlockCallMutation)

# Special Cases
def _149c_e47b(block: "SRBlock|IRBlock", validation_if: "ValidationIF") -> OpcodeType:
    from pypenguin.core.block_mutation import SRStopScriptMutation
    mutation: SRStopScriptMutation = block.mutation
    return OpcodeType.ENDING_STATEMENT if mutation.is_ending_statement else OpcodeType.STATEMENT
info_api.add_opcode_case(OPCODE_STOP_SCRIPT, SpecialCase(
    type=SpecialCaseType.GET_OPCODE_TYPE,
    function=_149c_e47b,
))

def _bd30_2f8b(block: "SRBlock|IRBlock", validation_if: "ValidationIF") -> OpcodeType:
    # Get the complete mutation and derive OpcodeType from optype
    from pypenguin.core.block_mutation import SRCustomBlockCallMutation
    partial_mutation: SRCustomBlockCallMutation = block.mutation
    complete_mutation = validation_if.get_cb_mutation(partial_mutation.custom_opcode)
    return complete_mutation.optype.corresponding_opcode_type
info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.GET_OPCODE_TYPE,
    function=_bd30_2f8b,
))



def _f9c8_6ab0(block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None") -> DualKeyDict[str, str, InputType]:
    from pypenguin.core.block_mutation import FRCustomBlockCallMutation, SRCustomBlockCallMutation
    from pypenguin.core.block import FRBlock
    if isinstance(block, FRBlock):
        old_mutation: FRCustomBlockCallMutation = block.mutation
        assert fti_if is not None, "When a FRBlock is given, fti_if mustn't be None"
        mutation: SRCustomBlockCallMutation = old_mutation.to_second(fti_if=fti_if)
    else:
        mutation: SRCustomBlockCallMutation = block.mutation
    
    return DualKeyDict.from_same_keys(mutation.custom_opcode.corresponding_input_info)
info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.GET_ALL_INPUT_IDS_INFO,
    function=_f9c8_6ab0,
))


def _2841_608f(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "FRBlock":
    # Transfer mutation from prototype block to definition block
    # Order deletion of the prototype block and its argument blocks
    # Delete "custom_block" input, which references the prototype block
    block = deepcopy(block)
    prototype_id    = block.inputs["custom_block"][1]
    prototype_block = fti_if.get_block(prototype_id)
    block.mutation  = prototype_block.mutation
    fti_if.schedule_block_deletion(prototype_id)
    del block.inputs["custom_block"]
    
    target_ids = fti_if.get_block_ids_by_parent_id(prototype_id)
    [fti_if.schedule_block_deletion(target_id) for target_id in target_ids]
    return block
info_api.add_opcodes_case(ANY_OPCODE_CB_DEF, SpecialCase(
    type=SpecialCaseType.PRE_FIRST_TO_INTER, 
    function=_2841_608f,
))

def _1a40_d676(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "FRBlock":
    # Transfer argument name from a field into the mutation
    # because only real dropdowns should be listed in "fields"
    from pypenguin.core.block_mutation import FRCustomBlockArgumentMutation
    block = deepcopy(block)
    mutation: FRCustomBlockArgumentMutation = block.mutation
    mutation.store_argument_name(block.fields["VALUE"][0])
    del block.fields["VALUE"]
    return block
info_api.add_opcodes_case(ANY_OPCODE_CB_ARG, SpecialCase(
    type=SpecialCaseType.PRE_FIRST_TO_INTER, 
    function=_1a40_d676,
))

def _4548_6eb6(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "FRBlock":
    # => Store input values by argument names instead of argument ids
    from pypenguin.core.block_mutation import FRCustomBlockCallMutation
    block = copy(block)
    partial_mutation: FRCustomBlockCallMutation = block.mutation
    complete_mutation = fti_if.get_cb_mutation(partial_mutation.proccode)
    new_inputs = {}
    for argument_id, input_value in block.inputs.items():
        argument_index = complete_mutation.argument_ids.index(argument_id)
        argument_name  = complete_mutation.argument_names[argument_index]
        new_inputs[argument_name] = input_value
    block.inputs = new_inputs
    return block
info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.PRE_FIRST_TO_INTER, 
    function=_4548_6eb6,
))

def _d0e6_50e9(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "IRBlock":
    # Return an empty, temporary block
    from pypenguin.core.block import IRBlock
    return IRBlock(
        opcode       = block.opcode,
        inputs       = ...,
        dropdowns    = ...,
        position     = ...,
        comment      = ..., # Can't possibly have a comment
        mutation     = ...,
        next         = ...,
        is_top_level = ...,
    )
info_api.add_opcode_case(OPCODE_CB_PROTOTYPE, SpecialCase(
    type=SpecialCaseType.INSTEAD_FIRST_TO_INTER,
    function=_d0e6_50e9,
))


def _f5d7_e3e2(block: "FRBlock", block_id: str, itf_if: "InterToFirstIF") -> "FRBlock":
    # Transfer mutation from definition block to prototype block
    # Create the prototype block and its argument blocks
    # Create the "custom_block" input, which references the prototype block
    from pypenguin.core.block_mutation import FRCustomBlockMutation, FRCustomBlockArgumentMutation
    from pypenguin.core.block          import FRBlock

    mutation: FRCustomBlockMutation = block.mutation
    prototype_id         = itf_if.get_next_block_id()
    argument_block_ids   = [itf_if.get_next_block_id() for i in range(len(mutation.argument_names))]


    block.inputs["custom_block"] = (1, prototype_id)
    prototype_inputs = {
        argument_id: (1, argument_block_id) 
        for argument_id, argument_block_id in zip(mutation.argument_ids, argument_block_ids)
    }
    prototype_block = FRBlock(
        opcode    = "procedures_prototype",
        next      = None,
        parent    = block_id,
        inputs    = prototype_inputs, 
        fields    = {},
        shadow    = True,
        top_level = False,
        mutation  = mutation,
    )
    itf_if.schedule_block_addition(prototype_id, prototype_block)
    for argument_name, argument_default, argument_block_id in zip(
        mutation.argument_names, mutation.argument_defaults, argument_block_ids
    ):
        argument_opcode = OPCODE_CB_ARG_TEXT if argument_default == "" else OPCODE_CB_ARG_BOOL
        argument_block = FRBlock(
            opcode   = argument_opcode,
            next     = None,
            parent   = prototype_id,
            inputs   = {},
            fields   = {
                "VALUE": (argument_name, string_to_sha256(argument_name, secondary=SHA256_SEC_LOCAL_ARGUMENT_NAME))
            },
            shadow   = True,
            topLevel = False,
            mutation = FRCustomBlockArgumentMutation(
                tag_name="mutation", 
                children=[], 
                color=mutation.color, # use the same colors as the prototype,
            ),
        )
        itf_if.schedule_block_addition(argument_block_id, argument_block)
    return block
info_api.add_opcodes_case(ANY_OPCODE_CB_DEF, SpecialCase(
    type=SpecialCaseType.POST_INTER_TO_FIRST,
    function=_f5d7_e3e2,
))

def _61f9_4fd5(block: "FRBlock", block_id: str, itf_if: "InterToFirstIF") -> "FRBlock":
    # => Store input values by argument ids instead of argument names
    from pypenguin.core.block_mutation import FRCustomBlockCallMutation
    block = copy(block)
    partial_mutation: FRCustomBlockCallMutation = block.mutation
    complete_mutation = itf_if.get_fr_cb_mutation(partial_mutation.proccode)
    new_inputs = {}
    for argument_name, input_value in block.inputs.items():
        argument_index = complete_mutation.argument_names.index(argument_name)
        argument_id    = complete_mutation.argument_ids[argument_index]
        new_inputs[argument_id] = input_value
    block.inputs = new_inputs
    return block
info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.POST_INTER_TO_FIRST, 
    function=_61f9_4fd5,
))



def _26f9_8217(path:list, block: "SRBlock") -> None:
    from pypenguin.core.block_mutation import SRCustomBlockMutation
    mutation: SRCustomBlockMutation = block.mutation
    if block.opcode == NEW_OPCODE_CB_DEF:
        if mutation.optype.is_reporter():
            raise InvalidValueError(path, f"If mutation.optype of a {block.__class__.__name__} is ...REPORTER, opcode should be {repr(NEW_OPCODE_CB_DEF_REP)}")
    elif block.opcode == NEW_OPCODE_CB_DEF_REP:
        if not mutation.optype.is_reporter():
            raise InvalidValueError(path, f"If mutation.optype of a {block.__class__.__name__} is NOT ...REPORTER, opcode should be {repr(NEW_OPCODE_CB_DEF)}")
    else: raise ValueError()
info_api.add_opcodes_case(ANY_OPCODE_CB_DEF, SpecialCase(
    type=SpecialCaseType.POST_VALIDATION,
    function=_26f9_8217,
))


__all__ = ["info_api"]

