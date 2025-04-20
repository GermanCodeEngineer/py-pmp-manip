from block_info.basis import *

motion = BlockInfoSet(name="motion", opcode_prefix="motion", block_infos={
    "movesteps": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="move (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, new="STEPS"),
        },
    ),
    "movebacksteps": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="move back (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, new="STEPS"),
        },
    ),
    "moveupdownsteps": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="move [DIRECTION] (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, new="STEPS"),
        },
        dropdowns={
            "DIRECTION": DropdownInfo(DropdownType.UP_DOWN, new="DIRECTION"),
        },
    ),
    "turnright": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="turn clockwise (DEGREES) degrees",
        inputs={
            "DEGREES": InputInfo(InputType.NUMBER, new="DEGREES"),
        },
    ),
    "turnleft": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="turn counterclockwise (DEGREES) degrees",
        inputs={
            "DEGREES": InputInfo(InputType.NUMBER, new="DEGREES"),
        },
    ),
    "goto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go to ([TARGET])",
        inputs={
            "TO": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("motion_goto_menu", inner="TO")),
        },
    ),
    "gotoxy": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go to x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, new="X"),
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "changebyxy": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change by x: (DX) y: (DY)",
        inputs={
            "DX": InputInfo(InputType.NUMBER, new="DX"),
            "DY": InputInfo(InputType.NUMBER, new="DY"),
        },
    ),
    "glideto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="glide (SECONDS) secs to ([TARGET])",
        inputs={
            "SECS": InputInfo(InputType.NUMBER, new="SECONDS"),
            "TO": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("motion_glideto_menu", inner="TO")),
        },
    ),
    "glidesecstoxy": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="glide (SECONDS) secs to x: (X) y: (Y)",
        inputs={
            "SECS": InputInfo(InputType.NUMBER, new="SECONDS"),
            "X": InputInfo(InputType.NUMBER, new="X"),
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "pointindirection": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="point in direction (DIRECTION)",
        inputs={
            "DIRECTION": InputInfo(InputType.DIRECTION, new="DIRECTION"),
        },
    ),
    "pointtowards": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="point towards ([TARGET])",
        inputs={
            "TOWARDS": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("motion_glideto_menu", inner="TOWARDS")),
        },
    ),
    "pointtowardsxy": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="point towards x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, new="X"),
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "turnaround": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="turn around",
    ),
    "changexby": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change x by (DX)",
        inputs={
            "DX": InputInfo(InputType.NUMBER, new="DX"),
        },
    ),
    "setx": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set x to (X)",
        inputs={
            "X": InputInfo(InputType.NUMBER, new="X"),
        },
    ),
    "changeyby": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change y by (DY)",
        inputs={
            "DY": InputInfo(InputType.NUMBER, new="DY"),
        },
    ),
    "sety": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set y to (Y)",
        inputs={
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "ifonedgebounce": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="if on edge, bounce",
    ),
    "ifonspritebounce": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="if touching ([TARGET]), bounce",
        inputs={
            "SPRITE": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("motion_pointtowards_menu", inner="TOWARDS")),
        },
    ),
    "setrotationstyle": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set rotation style [STYLE]",
        dropdowns={
            "STYLE": DropdownInfo(DropdownType.ROTATION_STYLE, new="STYLE"),
        },
    ),
    "move_sprite_to_scene_side": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="move to stage [ZONE]",
        dropdowns={
            "ALIGNMENT": DropdownInfo(DropdownType.STAGE_ZONE, new="ZONE"),
        },
    ),
    "xposition": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="x position",
        can_have_monitor="True",
    ),
    "yposition": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="y position",
        can_have_monitor="True",
    ),
    "direction": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="direction",
        can_have_monitor="True",
    ),
})