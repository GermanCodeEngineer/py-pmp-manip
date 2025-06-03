from pypenguin.utility import DualKeyDict

from pypenguin.opcode_info.api import OpcodeInfoGroup, OpcodeInfo, OpcodeType, InputInfo, InputType, DropdownInfo, DropdownType, MenuInfo


motion = OpcodeInfoGroup(name="motion", opcode_info=DualKeyDict({
    ("motion_movesteps", "move (STEPS) steps"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("STEPS", "STEPS"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_movebacksteps", "move back (STEPS) steps"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("STEPS", "STEPS"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_moveupdownsteps", "move [DIRECTION] (STEPS) steps"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("STEPS", "STEPS"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("DIRECTION", "DIRECTION"): DropdownInfo(DropdownType.UP_DOWN),
        }),
    ),
    ("motion_turnright", "turn clockwise (DEGREES) degrees"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DEGREES", "DEGREES"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_turnleft", "turn counterclockwise (DEGREES) degrees"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DEGREES", "DEGREES"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_goto", "go to ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TO", "TARGET"): InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("motion_goto_menu", inner="TO")),
        }),
    ),
    ("motion_gotoxy", "go to x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_changebyxy", "change by x: (DX) y: (DY)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DX", "DX"): InputInfo(InputType.NUMBER),
            ("DY", "DY"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_glideto", "glide (SECONDS) secs to ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SECS", "SECONDS"): InputInfo(InputType.NUMBER),
            ("TO", "TARGET"): InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("motion_glideto_menu", inner="TO")),
        }),
    ),
    ("motion_glidesecstoxy", "glide (SECONDS) secs to x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SECS", "SECONDS"): InputInfo(InputType.NUMBER),
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_pointindirection", "point in direction (DIRECTION)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DIRECTION", "DIRECTION"): InputInfo(InputType.DIRECTION),
        }),
    ),
    ("motion_pointtowards", "point towards ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TOWARDS", "TARGET"): InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("motion_glideto_menu", inner="TOWARDS")),
        }),
    ),
    ("motion_pointtowardsxy", "point towards x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_turnaround", "turn around"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),
    ("motion_changexby", "change x by (DX)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DX", "DX"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_setx", "set x to (X)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("X", "X"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_changeyby", "change y by (DY)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DY", "DY"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_sety", "set y to (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("Y", "Y"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("motion_ifonedgebounce", "if on edge, bounce"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),
    ("motion_ifonspritebounce", "if touching ([TARGET]), bounce"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SPRITE", "TARGET"): InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("motion_pointtowards_menu", inner="TOWARDS")),
        }),
    ),
    ("motion_setrotationstyle", "set rotation style [STYLE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("STYLE", "STYLE"): DropdownInfo(DropdownType.ROTATION_STYLE),
        }),
    ),
    ("motion_move_sprite_to_scene_side", "move to stage [ZONE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("ALIGNMENT", "ZONE"): DropdownInfo(DropdownType.STAGE_ZONE),
        }),
    ),
    ("motion_xposition", "x position"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
    ("motion_yposition", "y position"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
    ("motion_direction", "direction"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
}))