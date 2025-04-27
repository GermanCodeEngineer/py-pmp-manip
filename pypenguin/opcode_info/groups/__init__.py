from typing import TYPE_CHECKING

from utility       import DualKeyDict
from block_opcodes import *

from opcode_info.main             import OpcodeInfo, OpcodeType, OpcodeInfoGroup, OpcodeInfoAPI
from opcode_info.input            import InputInfo, InputType, InputMode
from opcode_info.dropdown         import DropdownInfo, DropdownType
from opcode_info.special_case     import SpecialCase, SpecialCaseType

from opcode_info.groups.motion    import motion
from opcode_info.groups.looks     import looks
from opcode_info.groups.sounds    import sounds
from opcode_info.groups.events    import events
from opcode_info.groups.control   import control
from opcode_info.groups.sensing   import sensing
from opcode_info.groups.operators import operators
from opcode_info.groups.variables import variables
from opcode_info.groups.lists     import lists

if TYPE_CHECKING:
    from core.block          import FRBlock, TRBlock
    from core.fr_to_tr_api   import FRtoTRAPI

motion.add_opcode("motion_goto_menu", "#REACHABLE TARGET MENU (GO)", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
motion.add_opcode("motion_glideto_menu", "#REACHABLE TARGET MENU (GLIDE)", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
motion.add_opcode("motion_pointtowards_menu", "#OBSERVABLE TARGET MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

looks.add_opcode("looks_costume", "#COSTUME MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
looks.add_opcode("looks_backdrops", "#BACKDROP MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
looks.add_opcode("looks_getinput_menu", "#COSTUME PROPERTY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
looks.add_opcode("looks_changeVisibilityOfSprite_menu", "#SHOW/HIDE SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
looks.add_opcode("looks_getOtherSpriteVisible_menu", "#IS SPRITE VISIBLE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

sounds.add_opcode("sound_sounds_menu", "#SOUND MENU", OpcodeInfo( # this is certainly correct.
    opcode_type=OpcodeType.MENU,
))

control.add_opcode("control_stop_sprite_menu", "#STOP SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
control.add_opcode("control_create_clone_of_menu", "#CLONE TARGET MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
control.add_opcode("control_run_as_sprite_menu", "#RUN AS SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

sensing.add_opcode("sensing_touchingobjectmenu", "#TOUCHING OBJECT MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
sensing.add_opcode("sensing_fulltouchingobjectmenu", "#FULL TOUCHING OBJECT MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
sensing.add_opcode("sensing_touchingobjectmenusprites", "#TOUCHING OBJECT MENU SPRITES", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
sensing.add_opcode("sensing_distancetomenu", "#DISTANCE TO MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
sensing.add_opcode("sensing_keyoptions", "#KEY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
sensing.add_opcode("sensing_scrolldirections", "#SCROLL DIRECTION MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
sensing.add_opcode("sensing_of_object_menu", "#OJBECT PROPERTY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
sensing.add_opcode("sensing_fingeroptions", "#FINGER INDEX MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

variables.add_opcode(OPCODE_VAR_VALUE, NEW_OPCODE_VAR_VALUE, OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    dropdowns=DualKeyDict({
        ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
    }),
    can_have_monitor="True",
))
lists.add_opcode(OPCODE_LIST_VALUE, NEW_OPCODE_LIST_VALUE, OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    dropdowns=DualKeyDict({
        ("LIST", "LIST"): DropdownInfo(DropdownType.LIST),
    }),
    can_have_monitor="True",
))

custom_blocks = OpcodeInfoGroup(
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
        (OPCODE_CB_CALL, "call custom opcode"): OpcodeInfo(
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
info_api.add_group(motion       )
info_api.add_group(looks        )
info_api.add_group(sounds       )
info_api.add_group(events       )
info_api.add_group(control      )
info_api.add_group(sensing      )
info_api.add_group(operators    )
info_api.add_group(variables    )
info_api.add_group(lists        )
info_api.add_group(custom_blocks)


def PRE__CB_DEF(block: "FRBlock", block_api: "FRtoTRAPI") -> "FRBlock":
    # Transfer mutation from prototype block to definition block
    # Order deletion of the prototype block and its argument blocks
    # Delete "custom_block" input, which references the prototype
    prototype_id    = block.inputs["custom_block"][1]
    prototype_block = block_api.get_block(prototype_id)
    block.mutation  = prototype_block.mutation
    block_api.schedule_block_deletion(prototype_id)
    del block.inputs["custom_block"]
     
    for block_candidate_id, block_candidate in block_api.get_all_blocks().items():
        if block_candidate.parent == prototype_id:
            block_api.schedule_block_deletion(block_candidate_id)
    return block

info_api.add_opcodes_case(ANY_OPCODE_CB_DEF, SpecialCase(
    type=SpecialCaseType.PRE_FR_STEP, 
    function=PRE__CB_DEF,
))

def PRE__CB_ARG(block: "FRBlock", block_api: "FRtoTRAPI") -> "FRBlock":
    # Transfer argument name from a field into the mutation
    # because only real dropdowns should be listed in "fields"
    block.mutation.store_argument_name(block.fields["VALUE"][0])
    del block.fields["VALUE"]
    return block

info_api.add_opcodes_case(ANY_OPCODE_CB_ARG, SpecialCase(
    type=SpecialCaseType.PRE_FR_STEP, 
    function=PRE__CB_ARG,
))

def PRE__CB_CALL(block: "FRBlock", block_api: "FRtoTRAPI") -> "FRBlock":
    cb_mutation = block_api.get_cb_mutation(block.mutation.proccode)
    new_inputs = {}
    for input_id, input_value in block.inputs.items():
        argument_index = cb_mutation.argument_ids.index(input_id)
        argument_name  = cb_mutation.argument_names[argument_index]
        new_inputs[argument_name] = input_value
    block.inputs = new_inputs
    return block

info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.PRE_FR_STEP, 
    function=PRE__CB_CALL,
))

def INSTEAD__CB_PROTOTYPE(block: "FRBlock", block_api: "FRtoTRAPI") -> "TRBlock":
    # Return an empty, temporary block
    from core.block import TRBlock
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

info_api.add_opcode_case(OPCODE_CB_PROTOTYPE, SpecialCase(
    type=SpecialCaseType.INSTEAD_FR_STEP,
    function=INSTEAD__CB_PROTOTYPE,
))

def INSTEAD_GET_MODES__CB_CALL(block: "FRBlock", block_api: "FRtoTRAPI") -> dict[str, InputMode]:
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

info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.INSTEAD_FR_STEP_INPUTS_GET_MODES, 
    function=INSTEAD_GET_MODES__CB_CALL,
))

info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.INSTEAD_GET_NEW_INPUT_ID, 
    function=(lambda block, input_id: input_id),
))

info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.INSTEAD_GET_ALL_NEW_INPUT_IDS_TYPES,
    function=(lambda block: block.mutation.custom_opcode.get_corresponding_input_types()),
))

