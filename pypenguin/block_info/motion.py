from block_info.basis import *

motion = BlockInfoSet(name="motion", opcode_prefix="motion", blocks={
    "motion_movesteps": BlockInfo(
        block_type="instruction",
        new_opcode="move (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, old="STEPS"),
        },
    ),
    "motion_movebacksteps": BlockInfo(
        block_type="instruction",
        new_opcode="move back (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, old="STEPS"),
        },
    ),
    "motion_moveupdownsteps": BlockInfo(
        block_type="instruction",
        new_opcode="move [DIRECTION] (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, old="STEPS"),
        },
        dropdowns={
            "DIRECTION": DropdownInfo(DropdownType.UP_DOWN, old="DIRECTION"),
        },
    ),
    "motion_turnright": BlockInfo(
        block_type="instruction",
        new_opcode="turn clockwise (DEGREES) degrees",
        inputs={
            "DEGREES": InputInfo(InputType.NUMBER, old="DEGREES"),
        },
    ),
    "motion_turnleft": BlockInfo(
        block_type="instruction",
        new_opcode="turn counterclockwise (DEGREES) degrees",
        inputs={
            "DEGREES": InputInfo(InputType.NUMBER, old="DEGREES"),
        },
    ),
    "motion_goto": BlockInfo(
        block_type="instruction",
        new_opcode="go to ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, old="TO", menu=MenuInfo("motion_goto_menu", inner="TO")),
        },
    ),
    "motion_gotoxy": BlockInfo(
        block_type="instruction",
        new_opcode="go to x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, old="X"),
            "Y": InputInfo(InputType.NUMBER, old="Y"),
        },
    ),
    "motion_changebyxy": BlockInfo(
        block_type="instruction",
        new_opcode="change by x: (DX) y: (DY)",
        inputs={
            "DX": InputInfo(InputType.NUMBER, old="DX"),
            "DY": InputInfo(InputType.NUMBER, old="DY"),
        },
    ),
    "motion_glideto": BlockInfo(
        block_type="instruction",
        new_opcode="glide (SECONDS) secs to ([TARGET])",
        inputs={
            "SECONDS": InputInfo(InputType.NUMBER, old="SECS"),
            "TARGET": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, old="TO", menu=MenuInfo("motion_glideto_menu", inner="TO")),
        },
    ),
    "motion_glidesecstoxy": BlockInfo(
        block_type="instruction",
        new_opcode="glide (SECONDS) secs to x: (X) y: (Y)",
        inputs={
            "SECONDS": InputInfo(InputType.NUMBER, old="SECS"),
            "X": InputInfo(InputType.NUMBER, old="X"),
            "Y": InputInfo(InputType.NUMBER, old="Y"),
        },
    ),
    "motion_pointindirection": BlockInfo(
        block_type="instruction",
        new_opcode="point in direction (DIRECTION)",
        inputs={
            "DIRECTION": InputInfo(InputType.DIRECTION, old="DIRECTION"),
        },
    ),
    "motion_pointtowards": BlockInfo(
        block_type="instruction",
        new_opcode="point towards ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, old="TOWARDS", menu=MenuInfo("motion_glideto_menu", inner="TOWARDS")),
        },
    ),
    "motion_pointtowardsxy": BlockInfo(
        block_type="instruction",
        new_opcode="point towards x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, old="X"),
            "Y": InputInfo(InputType.NUMBER, old="Y"),
        },
    ),
    "motion_turnaround": BlockInfo(
        block_type="instruction",
        new_opcode="turn around",
    ),
    "motion_changexby": BlockInfo(
        block_type="instruction",
        new_opcode="change x by (DX)",
        inputs={
            "DX": InputInfo(InputType.NUMBER, old="DX"),
        },
    ),
    "motion_setx": BlockInfo(
        block_type="instruction",
        new_opcode="set x to (X)",
        inputs={
            "X": InputInfo(InputType.NUMBER, old="X"),
        },
    ),
    "motion_changeyby": BlockInfo(
        block_type="instruction",
        new_opcode="change y by (DY)",
        inputs={
            "DY": InputInfo(InputType.NUMBER, old="DY"),
        },
    ),
    "motion_sety": BlockInfo(
        block_type="instruction",
        new_opcode="set y to (Y)",
        inputs={
            "Y": InputInfo(InputType.NUMBER, old="Y"),
        },
    ),
    "motion_ifonedgebounce": BlockInfo(
        block_type="instruction",
        new_opcode="if on edge, bounce",
    ),
    "motion_ifonspritebounce": BlockInfo(
        block_type="instruction",
        new_opcode="if touching ([TARGET]), bounce",
        inputs={
            "TARGET": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, old="SPRITE", menu=MenuInfo("motion_pointtowards_menu", inner="TOWARDS")),
        },
    ),
    "motion_setrotationstyle": BlockInfo(
        block_type="instruction",
        new_opcode="set rotation style [STYLE]",
    ),
    "motion_move_sprite_to_scene_side": BlockInfo(
        block_type="instruction",
        new_opcode="move to stage [ZONE]",
    ),
    "motion_xposition": BlockInfo(
        block_type="stringReporter",
        new_opcode="x position",
        can_have_monitor="True",
    ),
    "motion_yposition": BlockInfo(
        block_type="stringReporter",
        new_opcode="y position",
        can_have_monitor="True",
    ),
    "motion_direction": BlockInfo(
        block_type="stringReporter",
        new_opcode="direction",
        can_have_monitor="True",
    ),
})