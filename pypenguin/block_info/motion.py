from block_info.basis import *

motion = CategoryOpcodesInfo(name="motion", opcode_prefix="motion", block_infos={
    "movesteps": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="move (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, new="STEPS"),
        },
    ),
    "movebacksteps": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="move back (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, new="STEPS"),
        },
    ),
    "moveupdownsteps": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="move [DIRECTION] (STEPS) steps",
        inputs={
            "STEPS": InputInfo(InputType.NUMBER, new="STEPS"),
        },
        dropdowns={
            "DIRECTION": DropdownInfo(DropdownType.UP_DOWN, new="DIRECTION"),
        },
    ),
    "turnright": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="turn clockwise (DEGREES) degrees",
        inputs={
            "DEGREES": InputInfo(InputType.NUMBER, new="DEGREES"),
        },
    ),
    "turnleft": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="turn counterclockwise (DEGREES) degrees",
        inputs={
            "DEGREES": InputInfo(InputType.NUMBER, new="DEGREES"),
        },
    ),
    "goto": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go to ([TARGET])",
        inputs={
            "TO": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("motion_goto_menu", inner="TO")),
        },
    ),
    "gotoxy": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go to x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, new="X"),
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "changebyxy": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change by x: (DX) y: (DY)",
        inputs={
            "DX": InputInfo(InputType.NUMBER, new="DX"),
            "DY": InputInfo(InputType.NUMBER, new="DY"),
        },
    ),
    "glideto": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="glide (SECONDS) secs to ([TARGET])",
        inputs={
            "SECS": InputInfo(InputType.NUMBER, new="SECONDS"),
            "TO": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("motion_glideto_menu", inner="TO")),
        },
    ),
    "glidesecstoxy": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="glide (SECONDS) secs to x: (X) y: (Y)",
        inputs={
            "SECS": InputInfo(InputType.NUMBER, new="SECONDS"),
            "X": InputInfo(InputType.NUMBER, new="X"),
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "pointindirection": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="point in direction (DIRECTION)",
        inputs={
            "DIRECTION": InputInfo(InputType.DIRECTION, new="DIRECTION"),
        },
    ),
    "pointtowards": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="point towards ([TARGET])",
        inputs={
            "TOWARDS": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("motion_glideto_menu", inner="TOWARDS")),
        },
    ),
    "pointtowardsxy": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="point towards x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, new="X"),
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "turnaround": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="turn around",
    ),
    "changexby": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change x by (DX)",
        inputs={
            "DX": InputInfo(InputType.NUMBER, new="DX"),
        },
    ),
    "setx": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set x to (X)",
        inputs={
            "X": InputInfo(InputType.NUMBER, new="X"),
        },
    ),
    "changeyby": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change y by (DY)",
        inputs={
            "DY": InputInfo(InputType.NUMBER, new="DY"),
        },
    ),
    "sety": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set y to (Y)",
        inputs={
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "ifonedgebounce": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="if on edge, bounce",
    ),
    "ifonspritebounce": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="if touching ([TARGET]), bounce",
        inputs={
            "SPRITE": InputInfo(InputType.RANDOM_MOUSE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("motion_pointtowards_menu", inner="TOWARDS")),
        },
    ),
    "setrotationstyle": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set rotation style [STYLE]",
        dropdowns={
            "STYLE": DropdownInfo(DropdownType.ROTATION_STYLE, new="STYLE"),
        },
    ),
    "move_sprite_to_scene_side": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="move to stage [ZONE]",
        dropdowns={
            "ALIGNMENT": DropdownInfo(DropdownType.STAGE_ZONE, new="ZONE"),
        },
    ),
    "xposition": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="x position",
        can_have_monitor="True",
    ),
    "yposition": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="y position",
        can_have_monitor="True",
    ),
    "direction": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="direction",
        can_have_monitor="True",
    ),
})