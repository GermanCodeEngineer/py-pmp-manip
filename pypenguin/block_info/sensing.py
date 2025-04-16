from block_info.basis import *

sensing = BlockInfoSet(name="sensing", opcode_prefix="sensing", block_infos={
    "touchingobject": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="touching ([OBJECT]) ?",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_EDGE_OR_OTHER_SPRITE, old="TOUCHINGOBJECTMENU", menu=MenuInfo("sensing_touchingobjectmenu", inner="TOUCHINGOBJECTMENU")),
        },
    ),
    "objecttouchingobject": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="([OBJECT]) touching ([SPRITE]) ?",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE, old="FULLTOUCHINGOBJECTMENU", menu=MenuInfo("sensing_fulltouchingobjectmenu", inner="FULLTOUCHINGOBJECTMENU")),
            "SPRITE": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="SPRITETOUCHINGOBJECTMENU", menu=MenuInfo("sensing_touchingobjectmenusprites", inner="SPRITETOUCHINGOBJECTMENU")),
        },
    ),
    "objecttouchingclonesprite": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="([OBJECT]) touching clone of ([SPRITE]) ?",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE, old="FULLTOUCHINGOBJECTMENU", menu=MenuInfo("sensing_fulltouchingobjectmenu", inner="FULLTOUCHINGOBJECTMENU")),
            "SPRITE": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="SPRITETOUCHINGOBJECTMENU", menu=MenuInfo("sensing_touchingobjectmenusprites", inner="SPRITETOUCHINGOBJECTMENU")),
        },
    ),
    "touchingcolor": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="touching color (COLOR) ?",
        inputs={
            "COLOR": InputInfo(InputType.COLOR, old="COLOR"),
        },
    ),
    "coloristouchingcolor": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="color (COLOR1) is touching color (COLOR2) ?",
        inputs={
            "COLOR1": InputInfo(InputType.COLOR, old="COLOR"),
            "COLOR2": InputInfo(InputType.COLOR, old="COLOR2"),
        },
    ),
    "getxyoftouchingsprite": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[COORDINATE] of touching ([OBJECT]) point",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_OR_OTHER_SPRITE, old="SPRITE", menu=MenuInfo("sensing_distancetomenu", inner="DISTANCETOMENU")),
        },
        dropdowns={
            "COORDINATE": DropdownInfo(DropdownType.X_OR_Y, old="XY"),
        },
    ),
    "distanceto": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="distance to ([OBJECT])",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_OR_OTHER_SPRITE, old="DISTANCETOMENU", menu=MenuInfo("sensing_distancetomenu", inner="DISTANCETOMENU")),
        },
    ),
    "distanceTo": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="distance from (X1) (Y1) to (X2) (Y2)",
        inputs={
            "X1": InputInfo(InputType.TEXT, old="x1"),
            "Y1": InputInfo(InputType.TEXT, old="y1"),
            "X2": InputInfo(InputType.TEXT, old="x2"),
            "Y2": InputInfo(InputType.TEXT, old="y2"),
        },
    ),
    "directionTo": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="direction to (X1) (Y1) from (X2) (Y2)",
        inputs={
            "X1": InputInfo(InputType.TEXT, old="x2"),
            "Y1": InputInfo(InputType.TEXT, old="y2"),
            "X2": InputInfo(InputType.TEXT, old="x1"),
            "Y2": InputInfo(InputType.TEXT, old="y1"),
        },
    ),
    "askandwait": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="ask (QUESTION) and wait",
        inputs={
            "QUESTION": InputInfo(InputType.TEXT, old="QUESTION"),
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
            "STRING": InputInfo(InputType.TEXT, old="TEXT1"),
        },
    ),
    "thing_is_number": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(STRING) is number?",
        inputs={
            "STRING": InputInfo(InputType.TEXT, old="TEXT1"),
        },
    ),
    "keypressed": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="key ([KEY]) pressed?",
        inputs={
            "KEY": InputInfo(InputType.KEY, old="KEY_OPTION", menu=MenuInfo("sensing_keyoptions", inner="KEY_OPTION")),
        },
    ),
    "keyhit": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="key ([KEY]) hit?",
        inputs={
            "KEY": InputInfo(InputType.KEY, old="KEY_OPTION", menu=MenuInfo("sensing_keyoptions", inner="KEY_OPTION")),
        },
    ),
    "mousescrolling": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="is mouse scrolling ([DIRECTION]) ?",
        inputs={
            "DIRECTION": InputInfo(InputType.UP_DOWN, old="SCROLL_OPTION", menu=MenuInfo("sensing_scrolldirections", inner="SCROLL_OPTION")),
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
            "TEXT": InputInfo(InputType.TEXT, old="ITEM"),
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
            "VALUE": InputInfo(InputType.TEXT, old="VALUE"),
            "TARGET": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, old="OBJECT", menu=MenuInfo("sensing_of_object_menu", inner="OBJECT")),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.MUTABLE_SPRITE_PROPERTY, old="PROPERTY"),
        },
    ),
    "of": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[PROPERTY] of ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, old="OBJECT", menu=MenuInfo("sensing_of_object_menu", inner="OBJECT")),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.READABLE_SPRITE_PROPERTY, old="PROPERTY"),
        },
    ),
    "current": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="current [PROPERTY]",
        can_have_monitor="True",
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
            "INDEX": InputInfo(InputType.FINGER_INDEX, old="FINGER_OPTION", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "fingertapped": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="finger ([INDEX]) tapped?",
        inputs={
            "INDEX": InputInfo(InputType.FINGER_INDEX, old="FINGER_OPTION", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "fingerx": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="finger ([INDEX]) x",
        inputs={
            "INDEX": InputInfo(InputType.FINGER_INDEX, old="FINGER_OPTION", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "fingery": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="finger ([INDEX]) y",
        inputs={
            "INDEX": InputInfo(InputType.FINGER_INDEX, old="FINGER_OPTION", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
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