from typing import TYPE_CHECKING
from copy   import copy, deepcopy

from pmp_manip.important_consts import (
    OPCODE_VAR_VALUE, NEW_OPCODE_VAR_VALUE, OPCODE_LIST_VALUE, NEW_OPCODE_LIST_VALUE, 
    OPCODE_STOP_SCRIPT, OPCODE_CHECKBOX, NEW_OPCODE_CHECKBOX, OPCODE_POLYGON, NEW_OPCODE_POLYGON,
    OPCODE_FILTER_LIST_INDEX, OPCODE_FILTER_LIST_ITEM, OPCODE_EXPANDABLE_IF, OPCODE_EXPANDABLE_MATH,
    OPCODE_CB_PROTOTYPE, ANY_OPCODE_CB_DEF, ANY_OPCODE_CB_ARG, 
    OPCODE_CB_CALL, NEW_OPCODE_CB_CALL, OPCODE_CB_ARG_TEXT, OPCODE_CB_ARG_BOOL, 
    OPCODE_CB_DEF, NEW_OPCODE_CB_DEF, OPCODE_CB_DEF_RET, NEW_OPCODE_CB_DEF_REP,
    SHA256_SEC_LOCAL_ARGUMENT_NAME,
)
from pmp_manip.utility          import (
    string_to_sha256, AbstractTreePath, 
    DualKeyDict, 
    MANIP_InvalidValueError,
)

from pmp_manip.opcode_info.api import (
    OpcodeInfo, OpcodeType, OpcodeInfoGroup, OpcodeInfoAPI, 
    InputInfo, InputType, BuiltinInputType,
    DropdownInfo, BuiltinDropdownType, 
    SpecialCase, SpecialCaseType,
    MonitorIdBehaviour,
)

from pmp_manip.opcode_info.data.c_motion    import c_motion
from pmp_manip.opcode_info.data.c_looks     import c_looks
from pmp_manip.opcode_info.data.c_sounds    import c_sounds
from pmp_manip.opcode_info.data.c_events    import c_events
from pmp_manip.opcode_info.data.c_control   import c_control
from pmp_manip.opcode_info.data.c_sensing   import c_sensing
from pmp_manip.opcode_info.data.c_operators import c_operators
from pmp_manip.opcode_info.data.c_variables import c_variables
from pmp_manip.opcode_info.data.c_lists     import c_lists

if TYPE_CHECKING:
    from pmp_manip.core.block_interface import FirstToInterIF, InterToFirstIF, ValidationIF
    from pmp_manip.core.block           import FRBlock, IRBlock, SRBlock

from pmp_manip.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockArgumentMutation, FRCustomBlockCallMutation, FRExpandableIfMutation, FRExpandableMathMutation,
    FRStopScriptMutation, FRPolygonMutation,
    SRCustomBlockMutation, SRCustomBlockArgumentMutation, SRCustomBlockCallMutation, SRExpandableIfMutation, SRExpandableMathMutation,
)

# MENUS
c_motion.add_opcode("motion_goto_menu", "&motion::#REACHABLE TARGET MENU (GO)", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_motion.add_opcode("motion_glideto_menu", "&motion::#REACHABLE TARGET MENU (GLIDE)", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_motion.add_opcode("motion_pointtowards_menu", "&motion::#OBSERVABLE TARGET MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

c_looks.add_opcode("looks_costume", "&looks::#COSTUME MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_looks.add_opcode("looks_backdrops", "&looks::#BACKDROP MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_looks.add_opcode("looks_getinput_menu", "&looks::#COSTUME PROPERTY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_looks.add_opcode("looks_changeVisibilityOfSprite_menu", "&looks::#SHOW/HIDE SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_looks.add_opcode("looks_getOtherSpriteVisible_menu", "&looks::#IS SPRITE VISIBLE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

c_sounds.add_opcode("sound_sounds_menu", "&sound::#SOUND MENU", OpcodeInfo( # this is certainly correct
    opcode_type=OpcodeType.MENU,
))

c_control.add_opcode("control_stop_sprite_menu", "&control::#STOP SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_control.add_opcode("control_create_clone_of_menu", "&control::#CLONE TARGET MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_control.add_opcode("control_run_as_sprite_menu", "&control::#RUN AS SPRITE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

c_sensing.add_opcode("sensing_touchingobjectmenu", "&sensing::#TOUCHING OBJECT MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_fulltouchingobjectmenu", "&sensing::#FULL TOUCHING OBJECT MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_touchingobjectmenusprites", "&sensing::#TOUCHING OBJECT MENU SPRITES", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_distancetomenu", "&sensing::#DISTANCE TO MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_keyoptions", "&sensing::#KEY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_scrolldirections", "&sensing::#SCROLL DIRECTION MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_of_object_menu", "&sensing::#OJBECT PROPERTY MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
c_sensing.add_opcode("sensing_fingeroptions", "&sensing::#FINGER INDEX MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

# SPECIAL BLOCKS
c_control.add_opcode(OPCODE_EXPANDABLE_IF, "&control::{{EXPANDABLE IF-THEN-ELSE CHAIN}}", OpcodeInfo(
    opcode_type=OpcodeType.STATEMENT,
    inputs=DualKeyDict(), # Overwritten by special case
    dropdowns=DualKeyDict({
        ("REMOVE", "REMOVE"): DropdownInfo(BuiltinDropdownType.EDITOR_BUTTON),
        ("ADD", "ADD"): DropdownInfo(BuiltinDropdownType.EDITOR_BUTTON)
    }),
))
c_operators.add_opcode(OPCODE_EXPANDABLE_MATH, "&operators::{{EXPANDABLE MATH CHAIN}}", OpcodeInfo(
    opcode_type=OpcodeType.STATEMENT,
    inputs=DualKeyDict(), # Overwritten by special case
    dropdowns=DualKeyDict({
        ("REMOVE", "REMOVE"): DropdownInfo(BuiltinDropdownType.EDITOR_BUTTON),
        ("ADD", "ADD"): DropdownInfo(BuiltinDropdownType.EDITOR_BUTTON)
    }),
))
c_variables.add_opcode(OPCODE_VAR_VALUE, NEW_OPCODE_VAR_VALUE, OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    dropdowns=DualKeyDict({
        ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
    }),
    can_have_monitor=True,
    monitor_id_behaviour=MonitorIdBehaviour.VARIABLE,
))
c_lists.add_opcode(OPCODE_LIST_VALUE, NEW_OPCODE_LIST_VALUE, OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    dropdowns=DualKeyDict({
        ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
    }),
    can_have_monitor=True,
    monitor_id_behaviour=MonitorIdBehaviour.LIST,
))
c_lists.add_opcode(OPCODE_FILTER_LIST_INDEX, "&lists::{{FILTER INDEX}}", OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    allow_embedded=True,
))
c_lists.add_opcode(OPCODE_FILTER_LIST_ITEM, "&lists::{{FILTER ITEM}}", OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    allow_embedded=True,
))

# CUSTOM BLOCKS CATEGORY
c_custom_blocks = OpcodeInfoGroup(
    name="Custom Opcodes",
    opcode_info=DualKeyDict({
        (OPCODE_CB_DEF, NEW_OPCODE_CB_DEF): OpcodeInfo(
            opcode_type=OpcodeType.HAT,
        ),
        (OPCODE_CB_DEF_RET, NEW_OPCODE_CB_DEF_REP): OpcodeInfo(
            opcode_type=OpcodeType.HAT,
        ),
        (OPCODE_CB_PROTOTYPE, "&customblocks::#CUSTOM BLOCK PROTOTYPE"): OpcodeInfo( # only temporary
            opcode_type=OpcodeType.NOT_RELEVANT,
        ),
        (OPCODE_CB_CALL, NEW_OPCODE_CB_CALL): OpcodeInfo(
            opcode_type=OpcodeType.DYNAMIC,
        ),
        ("procedures_return", "&customblocks::return (VALUE)"): OpcodeInfo(
            opcode_type=OpcodeType.ENDING_STATEMENT,
            inputs=DualKeyDict({
                ("return", "VALUE"): InputInfo(BuiltinInputType.TEXT),
            }),
        ),
        ("procedures_set", "&customblocks::set (PARAM) to (VALUE)"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("PARAM", "PARAM"): InputInfo(BuiltinInputType.ROUND),
                ("VALUE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
            }),
        ),
        (OPCODE_CB_ARG_TEXT, "&customblocks::custom block text arg [ARGUMENT]"): OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
        ),
        (OPCODE_CB_ARG_BOOL, "&customblocks::custom block boolean arg [ARGUMENT]"): OpcodeInfo(
            opcode_type=OpcodeType.BOOLEAN_REPORTER,
        ),
    }),
)

# SPECIAL BLOCKS WIHCH FIT INTO NO CATEGORY
g_special = OpcodeInfoGroup(
    name="Special Blocks",
    opcode_info = DualKeyDict({
        (OPCODE_CHECKBOX, NEW_OPCODE_CHECKBOX): OpcodeInfo(
            opcode_type=OpcodeType.NOT_RELEVANT,
            dropdowns=DualKeyDict({
                ("CHECKBOX", "CHECKBOX"): DropdownInfo(BuiltinDropdownType.CHECKBOX)
            }),
            has_shadow=True,
        ),
        (OPCODE_POLYGON, NEW_OPCODE_POLYGON): OpcodeInfo(
            opcode_type=OpcodeType.EMBEDDED,
            inputs=DualKeyDict(), # Overwritten by special case
            dropdowns=DualKeyDict({
                ("button", "UNTOUCHED"): DropdownInfo(BuiltinDropdownType.POLYGON_MENU_UNTOUCHED),
            }),
            has_shadow=True,
        ),
        ("note", "&special::#NOTE MENU"): OpcodeInfo(
            opcode_type=OpcodeType.MENU,
        ),
    })
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
info_api.add_group(g_special)

# Mutations
info_api.set_opcodes_mutation_class(ANY_OPCODE_CB_ARG, old_cls=FRCustomBlockArgumentMutation, new_cls=SRCustomBlockArgumentMutation)
info_api.set_opcodes_mutation_class(ANY_OPCODE_CB_DEF, old_cls=None, new_cls=SRCustomBlockMutation)
info_api.set_opcode_mutation_class(OPCODE_CB_PROTOTYPE, old_cls=FRCustomBlockMutation, new_cls=None)
info_api.set_opcode_mutation_class(OPCODE_CB_CALL, old_cls=FRCustomBlockCallMutation, new_cls=SRCustomBlockCallMutation)
info_api.set_opcode_mutation_class(OPCODE_STOP_SCRIPT, old_cls=FRStopScriptMutation, new_cls=None)
info_api.set_opcode_mutation_class(OPCODE_POLYGON, old_cls=FRPolygonMutation, new_cls=None)
info_api.set_opcode_mutation_class(OPCODE_EXPANDABLE_IF, old_cls=FRExpandableIfMutation, new_cls=SRExpandableIfMutation)
info_api.set_opcode_mutation_class(OPCODE_EXPANDABLE_MATH, old_cls=FRExpandableIfMutation, new_cls=SRExpandableIfMutation)

# Special Cases
def _149c_e47b(block: "SRBlock|IRBlock", validation_if: "ValidationIF") -> OpcodeType:
    dropdown_value = block.dropdowns["TARGET"]
    match dropdown_value.value:
        case "all" | "this script":
            return OpcodeType.ENDING_STATEMENT
        case "other scripts in sprite":
            return OpcodeType.STATEMENT
        case _:
            raise ValueError(f"Dropdown 'TARGET' is invalid. Please validate the project: {dropdown_value!r}")
info_api.add_opcode_case(OPCODE_STOP_SCRIPT, SpecialCase(
    type=SpecialCaseType.GET_OPCODE_TYPE,
    function=_149c_e47b,
))

def _bd30_2f8b(block: "SRBlock|IRBlock", validation_if: "ValidationIF") -> OpcodeType:
    # Get the complete mutation and derive OpcodeType from optype
    partial_mutation: SRCustomBlockCallMutation = block.mutation
    complete_mutation = validation_if.get_cb_mutation(partial_mutation.custom_opcode)
    return complete_mutation.optype.corresponding_opcode_type
info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.GET_OPCODE_TYPE,
    function=_bd30_2f8b,
))



def _f9c8_6ab0(block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None") -> DualKeyDict[str, str, InputType]:
    from pmp_manip.core.block import FRBlock
    if isinstance(block, FRBlock):
        old_mutation: FRCustomBlockCallMutation = block.mutation
        assert fti_if is not None, "When a FRBlock is given, fti_if must not be None"
        mutation: SRCustomBlockCallMutation = old_mutation.to_second(fti_if)
    else:
        mutation: SRCustomBlockCallMutation = block.mutation
    
    return DualKeyDict.from_single_key_value(mutation.custom_opcode.corresponding_input_info.items())
info_api.add_opcode_case(OPCODE_CB_CALL, SpecialCase(
    type=SpecialCaseType.GET_ALL_INPUT_IDS_INFO,
    function=_f9c8_6ab0,
))

def _2dc4_f736(block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None") -> DualKeyDict[str, str, InputType]:
    # Generate X1, Y1 ... Xn, Yn depending on demand
    max_point_index = 0
    for input_id in block.inputs.keys():
        if   input_id.lower().startswith("x") or input_id.startswith("y"):
            point_index = int(input_id[1:], base=10)
        else:
            continue
        max_point_index = max(max_point_index, point_index)
    
    input_infos = DualKeyDict()
    for point_index in range(max_point_index):
        input_infos.set(
            key1  = f"x{point_index+1}",
            key2  = f"X{point_index+1}",
            value = InputInfo(BuiltinInputType.NUMBER_SPECIAL),
        )
        input_infos.set(
            key1  = f"y{point_index+1}",
            key2  = f"Y{point_index+1}",
            value = InputInfo(BuiltinInputType.NUMBER_SPECIAL),
        )
    return input_infos
info_api.add_opcode_case(OPCODE_POLYGON, SpecialCase(
    type=SpecialCaseType.GET_ALL_INPUT_IDS_INFO,
    function=_2dc4_f736,
))

def _eab0_2775(block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None") -> DualKeyDict[str, str, InputType]:
    # Generate SUBSTACK1, BOOL1 ... SUBSTACKn, BOOLn depending on demand
    mutation: FRExpandableIfMutation | SRExpandableIfMutation = block.mutation
    input_infos = DualKeyDict()
    branch_count = mutation.branch_count if isinstance(mutation, SRExpandableIfMutation) else mutation.branches
    condition_then_count = (branch_count - 1) if mutation.ends_in_else else branch_count # both mutations have ends_in_else
    for branch_index in range(condition_then_count):
        input_infos.set(
            key1  = f"SUBSTACK{branch_index+1}",
            key2  = f"THEN{branch_index+1}",
            value = InputInfo(BuiltinInputType.SCRIPT),
        )
    if mutation.ends_in_else:
        input_infos.set(
            key1  = f"SUBSTACK{branch_count}",
            key2  = f"ELSE",
            value = InputInfo(BuiltinInputType.SCRIPT),
        )
    for branch_index in range(condition_then_count):
        input_infos.set(
            key1  = f"BOOL{branch_index+1}",
            key2  = f"CONDITION{branch_index+1}",
            value = InputInfo(BuiltinInputType.BOOLEAN),
        )
    return input_infos
info_api.add_opcode_case(OPCODE_EXPANDABLE_IF, SpecialCase(
    type=SpecialCaseType.GET_ALL_INPUT_IDS_INFO,
    function=_eab0_2775,
))

def _a70a_0e97(block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None") -> DualKeyDict[str, str, InputType]:
    # Generate SUBSTACK1, BOOL1 ... SUBSTACKn, BOOLn depending on demand
    mutation: FRExpandableMathMutation | SRExpandableMathMutation = block.mutation
    input_infos = DualKeyDict()
    input_count = (len(mutation.operations) + 1) if isinstance(mutation, SRExpandableMathMutation) else mutation.input_count
    for input_index in range(input_count):
        input_infos.set(
            key1  = f"NUM{input_index+1}",
            key2  = f"OPERAND{input_index+1}",
            value = InputInfo(BuiltinInputType.NUMBER),
        )
    return input_infos
info_api.add_opcode_case(OPCODE_EXPANDABLE_MATH, SpecialCase(
    type=SpecialCaseType.GET_ALL_INPUT_IDS_INFO,
    function=_a70a_0e97,
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
    block = deepcopy(block)
    mutation: FRCustomBlockArgumentMutation = block.mutation
    mutation.store_argument_name(block.fields["VALUE"][0])
    del block.fields["VALUE"]
    return block
info_api.add_opcodes_case(ANY_OPCODE_CB_ARG, SpecialCase(
    type=SpecialCaseType.PRE_FIRST_TO_INTER, 
    function=_1a40_d676,
))

def _7fd4_5e99(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "FRBlock":
    # Remove the mutation, so that no mutation will be given to the IRBlock and SRBlock
    block = copy(block)
    block.mutation = None
    return block
info_api.add_opcode_case(OPCODE_STOP_SCRIPT, SpecialCase(
    type=SpecialCaseType.PRE_FIRST_TO_INTER, 
    function=_7fd4_5e99,
))

def _4548_6eb6(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "FRBlock":
    # => Store input values by argument names instead of argument ids
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

def _1101_80e9(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "FRBlock":
    # Remove the mutation, so that no mutation will be given to the IRBlock and SRBlock
    block = copy(block)
    block.mutation = None
    return block
info_api.add_opcode_case(OPCODE_POLYGON, SpecialCase(
    type=SpecialCaseType.PRE_FIRST_TO_INTER, 
    function=_1101_80e9,
))


def _d0e6_50e9(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "IRBlock":
    # Return an empty, temporary block
    from pmp_manip.core.block import IRBlock
    return IRBlock(
        opcode       = block.opcode,
        inputs       = ...,
        dropdowns    = ...,
        position     = ...,
        comment      = ..., # can not possibly have a comment
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
    from pmp_manip.core.block          import FRBlock

    block = deepcopy(block)
    mutation: FRCustomBlockMutation = block.mutation
    block.mutation       = None
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
            opcode    = argument_opcode,
            next      = None,
            parent    = prototype_id,
            inputs    = {},
            fields    = {
                "VALUE": (argument_name, string_to_sha256(argument_name, secondary=SHA256_SEC_LOCAL_ARGUMENT_NAME))
            },
            shadow    = True,
            top_level = False,
            mutation  = FRCustomBlockArgumentMutation(
                tag_name = "mutation", 
                children = [], 
                color    = copy(mutation.color), # use the same colors as the prototype,
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

def _5b5e_f1d7(block: "FRBlock", block_id: str, itf_if: "InterToFirstIF") -> "FRBlock":
    # Add the mutation, so that a mutation will be given to the FRBlock
    dropdown_value = block.fields["STOP_OPTION"][0]
    match dropdown_value:
        case "all" | "this script":
            has_next = False
        case "other scripts in sprite":
            has_next = True
        case _:
            raise ValueError(f"Dropdown field 'STOP_OPTION' is invalid. Please validate the project: {dropdown_value!r}")
    block = copy(block)
    block.mutation = FRStopScriptMutation(
        tag_name="mutation", children=[],
        has_next=has_next,
    )
    return block
info_api.add_opcode_case(OPCODE_STOP_SCRIPT, SpecialCase(
    type=SpecialCaseType.POST_INTER_TO_FIRST, 
    function=_5b5e_f1d7,
))

def _f77b_dd4b(block: "FRBlock", block_id: str, itf_if: "InterToFirstIF") -> "FRBlock":
    # Add the mutation, so that a mutation will be given to the FRBlock
    max_point_index = 0
    for input_id in block.inputs.keys():
        if   input_id.lower().startswith("x") or input_id.startswith("y"):
            point_index = int(input_id[1:], base=10)
        else:
            continue
        max_point_index = max(max_point_index, point_index)
    
    block = copy(block)
    block.mutation = FRPolygonMutation(
        tag_name="mutation",
        children=[],

        points=max_point_index,
        color="#0FBD8C",
        midle=(0, 0),
        scale=50,
        expanded=True,
        needs_init=True,
    )
    return block
info_api.add_opcode_case(OPCODE_POLYGON, SpecialCase(
    type=SpecialCaseType.POST_INTER_TO_FIRST, 
    function=_f77b_dd4b,
))


def _26f9_8217(path: AbstractTreePath, block: "SRBlock") -> None:
    mutation: SRCustomBlockMutation = block.mutation
    if block.opcode == NEW_OPCODE_CB_DEF:
        if mutation.optype.is_reporter():
            raise MANIP_InvalidValueError(path, f"If mutation.optype of a {block.__class__.__name__} is any ...REPORTER optype, opcode should be {NEW_OPCODE_CB_DEF_REP!r}")
    elif block.opcode == NEW_OPCODE_CB_DEF_REP:
        if not mutation.optype.is_reporter():
            raise MANIP_InvalidValueError(path, f"If mutation.optype of a {block.__class__.__name__} is NOT any ...REPORTER optype, opcode should be {NEW_OPCODE_CB_DEF!r}")
    else: raise ValueError()
info_api.add_opcodes_case(ANY_OPCODE_CB_DEF, SpecialCase(
    type=SpecialCaseType.POST_VALIDATION,
    function=_26f9_8217,
))


__all__ = ["info_api"]

