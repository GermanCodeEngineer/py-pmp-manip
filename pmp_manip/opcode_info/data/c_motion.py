from pmp_manip.opcode_info.data_imports import *

c_motion = OpcodeInfoGroup(name="c_motion", opcode_info=DualKeyDict({
    ("motion_movesteps", "&motion::move (STEPS) steps"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("STEPS", "STEPS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_movebacksteps", "&motion::move back (STEPS) steps"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("STEPS", "STEPS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_moveupdownsteps", "&motion::move [DIRECTION] (STEPS) steps"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("STEPS", "STEPS"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("DIRECTION", "DIRECTION"): DropdownInfo(BuiltinDropdownType.UP_DOWN),
        }),
    ),

    ("motion_turnright", "&motion::turn clockwise (DEGREES) degrees"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DEGREES", "DEGREES"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_turnleft", "&motion::turn counterclockwise (DEGREES) degrees"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DEGREES", "DEGREES"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_goto", "&motion::go to ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TO", "TARGET"): InputInfo(BuiltinInputType.RANDOM_MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("motion_goto_menu", inner="TO")),
        }),
    ),

    ("motion_gotoxy", "&motion::go to x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_changebyxy", "&motion::change by x: (DX) y: (DY)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DX", "DX"): InputInfo(BuiltinInputType.NUMBER),
            ("DY", "DY"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_glideto", "&motion::glide (SECONDS) secs to ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SECS", "SECONDS"): InputInfo(BuiltinInputType.NUMBER),
            ("TO", "TARGET"): InputInfo(BuiltinInputType.RANDOM_MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("motion_glideto_menu", inner="TO")),
        }),
    ),

    ("motion_glidesecstoxy", "&motion::glide (SECONDS) secs to x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SECS", "SECONDS"): InputInfo(BuiltinInputType.NUMBER),
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_pointindirection", "&motion::point in direction (DIRECTION)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DIRECTION", "DIRECTION"): InputInfo(BuiltinInputType.DIRECTION),
        }),
    ),

    ("motion_pointtowards", "&motion::point towards ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TOWARDS", "TARGET"): InputInfo(BuiltinInputType.RANDOM_MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("motion_glideto_menu", inner="TOWARDS")),
        }),
    ),

    ("motion_pointtowardsxy", "&motion::point towards x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_turnaround", "&motion::turn around"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("motion_changexby", "&motion::change x by (DX)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DX", "DX"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_setx", "&motion::set x to (X)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_changeyby", "&motion::change y by (DY)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DY", "DY"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_sety", "&motion::set y to (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("motion_ifonedgebounce", "&motion::if on edge, bounce"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("motion_ifonspritebounce", "&motion::if touching ([TARGET]), bounce"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SPRITE", "TARGET"): InputInfo(BuiltinInputType.RANDOM_MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("motion_pointtowards_menu", inner="TOWARDS")),
        }),
    ),

    ("motion_setrotationstyle", "&motion::set rotation style [STYLE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("STYLE", "STYLE"): DropdownInfo(BuiltinDropdownType.ROTATION_STYLE),
        }),
    ),

    ("motion_move_sprite_to_scene_side", "&motion::move to stage [ZONE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("ALIGNMENT", "ZONE"): DropdownInfo(BuiltinDropdownType.STAGE_ZONE),
        }),
    ),

    ("motion_xposition", "&motion::x position"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.SPRITE_OPCMAIN,
    ),

    ("motion_yposition", "&motion::y position"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.SPRITE_OPCMAIN,
    ),

    ("motion_direction", "&motion::direction"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.SPRITE_OPCMAIN,
    ),

}))