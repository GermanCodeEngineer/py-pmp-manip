from utility                      import DualKeyDict
from block_opcodes                import *

from opcode_info.opcode           import OpcodeInfo, OpcodeType, OpcodeInfoGroup
from opcode_info.input            import InputInfo, InputType
from opcode_info.dropdown         import DropdownInfo, DropdownType

from opcode_info.groups.motion    import motion
from opcode_info.groups.looks     import looks
from opcode_info.groups.sounds    import sounds
from opcode_info.groups.events    import events
from opcode_info.groups.control   import control
from opcode_info.groups.sensing   import sensing
from opcode_info.groups.operators import operators
from opcode_info.groups.variables import variables
from opcode_info.groups.lists     import lists

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

variables.add_opcode(OPCODE_VAR_VALUE, OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    new_opcode=NEW_OPCODE_VAR_VALUE,
    dropdowns={
        "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
    },
    can_have_monitor="True",
))
lists.add_opcode(OPCODE_LIST_VALUE, OpcodeInfo(
    opcode_type=OpcodeType.STRING_REPORTER,
    new_opcode=NEW_OPCODE_LIST_VALUE,
    dropdowns={
        "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
    },
    can_have_monitor="True",
))

def CB_OLD_OPCODE_HANDLER(new_opcode: str, mutation: "SRMutation | None") -> str | None:
    from core.block_mutation import SRCustomOpcodeMutation
    if new_opcode == NEW_OPCODE_CB_DEF:
        assert isinstance(mutation, SRCustomOpcodeMutation)
        if mutation.optype.is_reporter:
            return OPCODE_CB_DEF_RET
        else:
            return OPCODE_CB_DEF
    return None

custom_opcodes = OpcodeInfoGroup(
    name="Custom Opcodes",
    opcode_infos=DualKeyDict({
        (OPCODE_CB_DEF, NEW_OPCODE_CB_DEF): OpcodeInfo(
            opcode_type=OpcodeType.HAT,
        ),
        (OPCODE_CB_DEF_RET, NEW_OPCODE_CB_DEF): OpcodeInfo(
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
            inputs={
                ("PARAM", "PARAM"): InputInfo(InputType.ROUND),
                ("VALUE", "VALUE"): InputInfo(InputType.TEXT),
            },
        ),
        (OPCODE_CB_ARG_TEXT, "value of text [ARGUMENT]"): OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            alt_opcode_prefix="argument",
        ),
        (OPCODE_CB_ARG_BOOL, "value of boolean [ARGUMENT]"): OpcodeInfo(
            opcode_type=OpcodeType.BOOLEAN_REPORTER,
            alt_opcode_prefix="argument",
        ),
    }),
    get_old_opcode_handler=CB_OLD_OPCODE_HANDLER,
)





info_api = OpcodeInfoApi()
info_api.add_opcode_info_set(motion       )
info_api.add_opcode_info_set(looks        )
info_api.add_opcode_info_set(sounds       )
info_api.add_opcode_info_set(events       )
info_api.add_opcode_info_set(control      )
info_api.add_opcode_info_set(sensing      )
info_api.add_opcode_info_set(operators    )
info_api.add_opcode_info_set(variables    )
info_api.add_opcode_info_set(lists        )
info_api.add_opcode_info_set(custom_opcodes)
