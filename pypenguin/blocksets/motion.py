from blocksets.blockset import BlockSet, BlockData, InputData, MenuData, DropdownData

motion = BlockSet(name="motion", blocks={
    "movesteps": BlockData(
        block_type="instruction",
        new_opcode="move (STEPS) steps",
        inputs={
            "STEPS": InputData("number", old="STEPS"),
        },
    ),
    "movebacksteps": BlockData(
        block_type="instruction",
        new_opcode="move back (STEPS) steps",
        inputs={
            "STEPS": InputData("number", old="STEPS"),
        },
    ),
    "moveupdownsteps": BlockData(
        block_type="instruction",
        new_opcode="move [DIRECTION] (STEPS) steps",
        inputs={
            "STEPS": InputData("number", old="STEPS"),
        },
        dropdowns={
            "DIRECTION": DropdownData("up|down", old="DIRECTION"),
        },
    ),
    "turnright": BlockData(
        block_type="instruction",
        new_opcode="turn clockwise (DEGREES) degrees",
        inputs={
            "DEGREES": InputData("number", old="DEGREES"),
        },
    ),
    "turnleft": BlockData(
        block_type="instruction",
        new_opcode="turn counterclockwise (DEGREES) degrees",
        inputs={
            "DEGREES": InputData("number", old="DEGREES"),
        },
    ),
    "goto": BlockData(
        block_type="instruction",
        new_opcode="go to ([TARGET])",
        inputs={
            "TARGET": InputData("random|mouse || other sprite", old="TO", menu=MenuData("motion_goto_menu", inner="TO")),
        },
    ),
    "gotoxy": BlockData(
        block_type="instruction",
        new_opcode="go to x: (X) y: (Y)",
        inputs={
            "X": InputData("number", old="X"),
            "Y": InputData("number", old="Y"),
        },
    ),
    "changebyxy": BlockData(
        block_type="instruction",
        new_opcode="change by x: (DX) y: (DY)",
        inputs={
            "DX": InputData("number", old="DX"),
            "DY": InputData("number", old="DY"),
        },
    ),
    "glideto": BlockData(
        block_type="instruction",
        new_opcode="glide (SECONDS) secs to ([TARGET])",
        inputs={
            "SECONDS": InputData("number", old="SECS"),
            "TARGET": InputData("random|mouse || other sprite", old="TO", menu=MenuData("motion_glideto_menu", inner="TO")),
        },
    ),
    "glidesecstoxy": BlockData(
        block_type="instruction",
        new_opcode="glide (SECONDS) secs to x: (X) y: (Y)",
        inputs={
            "SECONDS": InputData("number", old="SECS"),
            "X": InputData("number", old="X"),
            "Y": InputData("number", old="Y"),
        },
    ),
    "pointindirection": BlockData(
        block_type="instruction",
        new_opcode="point in direction (DIRECTION)",
        inputs={
            "DIRECTION": InputData("direction", old="DIRECTION"),
        },
    ),
    "pointtowards": BlockData(
        block_type="instruction",
        new_opcode="point towards ([TARGET])",
        inputs={
            "TARGET": InputData("random|mouse || other sprite", old="TOWARDS", menu=MenuData("motion_glideto_menu", inner="TOWARDS")),
        },
    ),
    "pointtowardsxy": BlockData(
        block_type="instruction",
        new_opcode="point towards x: (X) y: (Y)",
        inputs={
            "X": InputData("number", old="X"),
            "Y": InputData("number", old="Y"),
        },
    ),
    "turnaround": BlockData(
        block_type="instruction",
        new_opcode="turn around",
    ),
    "changexby": BlockData(
        block_type="instruction",
        new_opcode="change x by (DX)",
        inputs={
            "DX": InputData("number", old="DX"),
        },
    ),
    "setx": BlockData(
        block_type="instruction",
        new_opcode="set x to (X)",
        inputs={
            "X": InputData("number", old="X"),
        },
    ),
    "changeyby": BlockData(
        block_type="instruction",
        new_opcode="change y by (DY)",
        inputs={
            "DY": InputData("number", old="DY"),
        },
    ),
    "sety": BlockData(
        block_type="instruction",
        new_opcode="set y to (Y)",
        inputs={
            "Y": InputData("number", old="Y"),
        },
    ),
    "ifonedgebounce": BlockData(
        block_type="instruction",
        new_opcode="if on edge, bounce",
    ),
    "ifonspritebounce": BlockData(
        block_type="instruction",
        new_opcode="if touching ([TARGET]), bounce",
        inputs={
            "TARGET": InputData("random|mouse || other sprite", old="SPRITE", menu=MenuData("motion_pointtowards_menu", inner="TOWARDS")),
        },
    ),
    "setrotationstyle": BlockData(
        block_type="instruction",
        new_opcode="set rotation style [STYLE]",
    ),
    "move_sprite_to_scene_side": BlockData(
        block_type="instruction",
        new_opcode="move to stage [ZONE]",
    ),
    "xposition": BlockData(
        block_type="stringReporter",
        new_opcode="x position",
        can_have_monitor="True",
    ),
    "yposition": BlockData(
        block_type="stringReporter",
        new_opcode="y position",
        can_have_monitor="True",
    ),
    "direction": BlockData(
        block_type="stringReporter",
        new_opcode="direction",
        can_have_monitor="True",
    ),
})