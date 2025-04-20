from block_info.basis import *

sensing = BlockInfoSet(name="sensing", opcode_prefix="sensing", block_infos={
    "touchingobject": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="touching ([OBJECT]) ?",
        inputs={
            "TOUCHINGOBJECTMENU": InputInfo(InputType.MOUSE_EDGE_OR_OTHER_SPRITE, new="OBJECT", menu=MenuInfo("sensing_touchingobjectmenu", inner="TOUCHINGOBJECTMENU")),
        },
    ),
    "objecttouchingobject": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="([OBJECT]) touching ([SPRITE]) ?",
        inputs={
            "FULLTOUCHINGOBJECTMENU": InputInfo(InputType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE, new="OBJECT", menu=MenuInfo("sensing_fulltouchingobjectmenu", inner="FULLTOUCHINGOBJECTMENU")),
            "SPRITETOUCHINGOBJECTMENU": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, new="SPRITE", menu=MenuInfo("sensing_touchingobjectmenusprites", inner="SPRITETOUCHINGOBJECTMENU")),
        },
    ),
    "objecttouchingclonesprite": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="([OBJECT]) touching clone of ([SPRITE]) ?",
        inputs={
            "FULLTOUCHINGOBJECTMENU": InputInfo(InputType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE, new="OBJECT", menu=MenuInfo("sensing_fulltouchingobjectmenu", inner="FULLTOUCHINGOBJECTMENU")),
            "SPRITETOUCHINGOBJECTMENU": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, new="SPRITE", menu=MenuInfo("sensing_touchingobjectmenusprites", inner="SPRITETOUCHINGOBJECTMENU")),
        },
    ),
    "touchingcolor": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="touching color (COLOR) ?",
        inputs={
            "COLOR": InputInfo(InputType.COLOR, new="COLOR"),
        },
    ),
    "coloristouchingcolor": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="color (COLOR1) is touching color (COLOR2) ?",
        inputs={
            "COLOR": InputInfo(InputType.COLOR, new="COLOR1"),
            "COLOR2": InputInfo(InputType.COLOR, new="COLOR2"),
        },
    ),
    "getxyoftouchingsprite": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[COORDINATE] of touching ([OBJECT]) point",
        inputs={
            "SPRITE": InputInfo(InputType.MOUSE_OR_OTHER_SPRITE, new="OBJECT", menu=MenuInfo("sensing_distancetomenu", inner="DISTANCETOMENU")),
        },
        dropdowns={
            "XY": DropdownInfo(DropdownType.X_OR_Y, new="COORDINATE"),
        },
    ),
    "distanceto": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="distance to ([OBJECT])",
        inputs={
            "DISTANCETOMENU": InputInfo(InputType.MOUSE_OR_OTHER_SPRITE, new="OBJECT", menu=MenuInfo("sensing_distancetomenu", inner="DISTANCETOMENU")),
        },
    ),
    "distanceTo": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="distance from (X1) (Y1) to (X2) (Y2)",
        inputs={
            "x1": InputInfo(InputType.TEXT, new="X1"),
            "y1": InputInfo(InputType.TEXT, new="Y1"),
            "x2": InputInfo(InputType.TEXT, new="X2"),
            "y2": InputInfo(InputType.TEXT, new="Y2"),
        },
    ),
    "directionTo": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="direction to (X1) (Y1) from (X2) (Y2)",
        inputs={
            "x2": InputInfo(InputType.TEXT, new="X1"),
            "y2": InputInfo(InputType.TEXT, new="Y1"),
            "x1": InputInfo(InputType.TEXT, new="X2"),
            "y1": InputInfo(InputType.TEXT, new="Y2"),
        },
    ),
    "askandwait": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="ask (QUESTION) and wait",
        inputs={
            "QUESTION": InputInfo(InputType.TEXT, new="QUESTION"),
        },
    ),
    "answer": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="answer",
        can_have_monitor="True",
    ),
    "thing_is_text": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(STRING) is text?",
        inputs={
            "TEXT1": InputInfo(InputType.TEXT, new="STRING"),
        },
    ),
    "thing_is_number": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(STRING) is number?",
        inputs={
            "TEXT1": InputInfo(InputType.TEXT, new="STRING"),
        },
    ),
    "keypressed": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="key ([KEY]) pressed?",
        inputs={
            "KEY_OPTION": InputInfo(InputType.KEY, new="KEY", menu=MenuInfo("sensing_keyoptions", inner="KEY_OPTION")),
        },
    ),
    "keyhit": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="key ([KEY]) hit?",
        inputs={
            "KEY_OPTION": InputInfo(InputType.KEY, new="KEY", menu=MenuInfo("sensing_keyoptions", inner="KEY_OPTION")),
        },
    ),
    "mousescrolling": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="is mouse scrolling ([DIRECTION]) ?",
        inputs={
            "SCROLL_OPTION": InputInfo(InputType.UP_DOWN, new="DIRECTION", menu=MenuInfo("sensing_scrolldirections", inner="SCROLL_OPTION")),
        },
    ),
    "mousedown": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="mouse down?",
        can_have_monitor="True",
    ),
    "mouseclicked": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="mouse clicked?",
        can_have_monitor="True",
    ),
    "mousex": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="mouse x",
        can_have_monitor="True",
    ),
    "mousey": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="mouse y",
        can_have_monitor="True",
    ),
    "setclipboard": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="add (TEXT) to clipboard",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, new="TEXT"),
        },
    ),
    "getclipboard": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="clipboard item",
        can_have_monitor="True",
    ),
    "setdragmode": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set drag mode [MODE]",
        dropdowns={
            "DRAG_MODE": DropdownInfo(DropdownType.DRAG_MODE, new="MODE"),
        },
    ),
    "getdragmode": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="draggable?",
        can_have_monitor="True",
    ),
    "loudness": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="loudness",
        can_have_monitor="True",
    ),
    "loud": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="loud?",
        can_have_monitor="True",
    ),
    "resettimer": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="reset timer",
    ),
    "timer": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="timer",
        can_have_monitor="True",
    ),
    "set_of": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [PROPERTY] of ([TARGET]) to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
            "OBJECT": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("sensing_of_object_menu", inner="OBJECT")),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.MUTABLE_SPRITE_PROPERTY, new="PROPERTY"),
        },
    ),
    "of": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[PROPERTY] of ([TARGET])",
        inputs={
            "OBJECT": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("sensing_of_object_menu", inner="OBJECT")),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.READABLE_SPRITE_PROPERTY, new="PROPERTY"),
        },
    ),
    "current": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="current [PROPERTY]",
        can_have_monitor="True",
        dropdowns={
            "CURRENTMENU": DropdownInfo(DropdownType.TIME_PROPERTY, new="PROPERTY"),
        },
    ),
    "dayssince2000": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="days since 2000",
        can_have_monitor="True",
    ),
    "mobile": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="mobile?",
    ),
    "fingerdown": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="finger ([INDEX]) down?",
        inputs={
            "FINGER_OPTION": InputInfo(InputType.FINGER_INDEX, new="INDEX", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "fingertapped": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="finger ([INDEX]) tapped?",
        inputs={
            "FINGER_OPTION": InputInfo(InputType.FINGER_INDEX, new="INDEX", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "fingerx": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="finger ([INDEX]) x",
        inputs={
            "FINGER_OPTION": InputInfo(InputType.FINGER_INDEX, new="INDEX", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "fingery": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="finger ([INDEX]) y",
        inputs={
            "FINGER_OPTION": InputInfo(InputType.FINGER_INDEX, new="INDEX", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "username": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="username",
        can_have_monitor="True",
    ),
    "loggedin": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="logged in?",
        can_have_monitor="True",
    ),
})