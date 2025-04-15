from block_info.basis import *

sensing = BlockInfoSet(name="sensing", opcode_prefix="sensing", blocks={
    "sensing_touchingobject": BlockInfo(
        block_type="booleanReporter",
        new_opcode="touching ([OBJECT]) ?",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_EDGE_OR_OTHER_SPRITE, old="TOUCHINGOBJECTMENU", menu=MenuInfo("sensing_touchingobjectmenu", inner="TOUCHINGOBJECTMENU")),
        },
    ),
    "sensing_objecttouchingobject": BlockInfo(
        block_type="booleanReporter",
        new_opcode="([OBJECT]) touching ([SPRITE]) ?",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE, old="FULLTOUCHINGOBJECTMENU", menu=MenuInfo("sensing_fulltouchingobjectmenu", inner="FULLTOUCHINGOBJECTMENU")),
            "SPRITE": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="SPRITETOUCHINGOBJECTMENU", menu=MenuInfo("sensing_touchingobjectmenusprites", inner="SPRITETOUCHINGOBJECTMENU")),
        },
    ),
    "sensing_objecttouchingclonesprite": BlockInfo(
        block_type="booleanReporter",
        new_opcode="([OBJECT]) touching clone of ([SPRITE]) ?",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE, old="FULLTOUCHINGOBJECTMENU", menu=MenuInfo("sensing_fulltouchingobjectmenu", inner="FULLTOUCHINGOBJECTMENU")),
            "SPRITE": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="SPRITETOUCHINGOBJECTMENU", menu=MenuInfo("sensing_touchingobjectmenusprites", inner="SPRITETOUCHINGOBJECTMENU")),
        },
    ),
    "sensing_touchingcolor": BlockInfo(
        block_type="booleanReporter",
        new_opcode="touching color (COLOR) ?",
        inputs={
            "COLOR": InputInfo(InputType.COLOR, old="COLOR"),
        },
    ),
    "sensing_coloristouchingcolor": BlockInfo(
        block_type="booleanReporter",
        new_opcode="color (COLOR1) is touching color (COLOR2) ?",
        inputs={
            "COLOR1": InputInfo(InputType.COLOR, old="COLOR"),
            "COLOR2": InputInfo(InputType.COLOR, old="COLOR2"),
        },
    ),
    "sensing_getxyoftouchingsprite": BlockInfo(
        block_type="stringReporter",
        new_opcode="[COORDINATE] of touching ([OBJECT]) point",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_OR_OTHER_SPRITE, old="SPRITE", menu=MenuInfo("sensing_distancetomenu", inner="DISTANCETOMENU")),
        },
        dropdowns={
            "COORDINATE": DropdownInfo(DropdownType.X_OR_Y, old="XY"),
        },
    ),
    "sensing_distanceto": BlockInfo(
        block_type="stringReporter",
        new_opcode="distance to ([OBJECT])",
        inputs={
            "OBJECT": InputInfo(InputType.MOUSE_OR_OTHER_SPRITE, old="DISTANCETOMENU", menu=MenuInfo("sensing_distancetomenu", inner="DISTANCETOMENU")),
        },
    ),
    "sensing_distanceTo": BlockInfo(
        block_type="stringReporter",
        new_opcode="distance from (X1) (Y1) to (X2) (Y2)",
        inputs={
            "X1": InputInfo(InputType.TEXT, old="x1"),
            "Y1": InputInfo(InputType.TEXT, old="y1"),
            "X2": InputInfo(InputType.TEXT, old="x2"),
            "Y2": InputInfo(InputType.TEXT, old="y2"),
        },
    ),
    "sensing_directionTo": BlockInfo(
        block_type="stringReporter",
        new_opcode="direction to (X1) (Y1) from (X2) (Y2)",
        inputs={
            "X1": InputInfo(InputType.TEXT, old="x2"),
            "Y1": InputInfo(InputType.TEXT, old="y2"),
            "X2": InputInfo(InputType.TEXT, old="x1"),
            "Y2": InputInfo(InputType.TEXT, old="y1"),
        },
    ),
    "sensing_askandwait": BlockInfo(
        block_type="instruction",
        new_opcode="ask (QUESTION) and wait",
        inputs={
            "QUESTION": InputInfo(InputType.TEXT, old="QUESTION"),
        },
    ),
    "sensing_answer": BlockInfo(
        block_type="stringReporter",
        new_opcode="answer",
        can_have_monitor="True",
    ),
    "sensing_thing_is_text": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(STRING) is text?",
        inputs={
            "STRING": InputInfo(InputType.TEXT, old="TEXT1"),
        },
    ),
    "sensing_thing_is_number": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(STRING) is number?",
        inputs={
            "STRING": InputInfo(InputType.TEXT, old="TEXT1"),
        },
    ),
    "sensing_keypressed": BlockInfo(
        block_type="booleanReporter",
        new_opcode="key ([KEY]) pressed?",
        inputs={
            "KEY": InputInfo(InputType.KEY, old="KEY_OPTION", menu=MenuInfo("sensing_keyoptions", inner="KEY_OPTION")),
        },
    ),
    "sensing_keyhit": BlockInfo(
        block_type="booleanReporter",
        new_opcode="key ([KEY]) hit?",
        inputs={
            "KEY": InputInfo(InputType.KEY, old="KEY_OPTION", menu=MenuInfo("sensing_keyoptions", inner="KEY_OPTION")),
        },
    ),
    "sensing_mousescrolling": BlockInfo(
        block_type="booleanReporter",
        new_opcode="is mouse scrolling ([DIRECTION]) ?",
        inputs={
            "DIRECTION": InputInfo(InputType.UP_DOWN, old="SCROLL_OPTION", menu=MenuInfo("sensing_scrolldirections", inner="SCROLL_OPTION")),
        },
    ),
    "sensing_mousedown": BlockInfo(
        block_type="booleanReporter",
        new_opcode="mouse down?",
        can_have_monitor="True",
    ),
    "sensing_mouseclicked": BlockInfo(
        block_type="booleanReporter",
        new_opcode="mouse clicked?",
        can_have_monitor="True",
    ),
    "sensing_mousex": BlockInfo(
        block_type="stringReporter",
        new_opcode="mouse x",
        can_have_monitor="True",
    ),
    "sensing_mousey": BlockInfo(
        block_type="stringReporter",
        new_opcode="mouse y",
        can_have_monitor="True",
    ),
    "sensing_setclipboard": BlockInfo(
        block_type="instruction",
        new_opcode="add (TEXT) to clipboard",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="ITEM"),
        },
    ),
    "sensing_getclipboard": BlockInfo(
        block_type="stringReporter",
        new_opcode="clipboard item",
        can_have_monitor="True",
    ),
    "sensing_setdragmode": BlockInfo(
        block_type="instruction",
        new_opcode="set drag mode [MODE]",
    ),
    "sensing_getdragmode": BlockInfo(
        block_type="stringReporter",
        new_opcode="draggable?",
        can_have_monitor="True",
    ),
    "sensing_loudness": BlockInfo(
        block_type="stringReporter",
        new_opcode="loudness",
        can_have_monitor="True",
    ),
    "sensing_loud": BlockInfo(
        block_type="booleanReporter",
        new_opcode="loud?",
        can_have_monitor="True",
    ),
    "sensing_resettimer": BlockInfo(
        block_type="instruction",
        new_opcode="reset timer",
    ),
    "sensing_timer": BlockInfo(
        block_type="stringReporter",
        new_opcode="timer",
        can_have_monitor="True",
    ),
    "sensing_set_of": BlockInfo(
        block_type="instruction",
        new_opcode="set [PROPERTY] of ([TARGET]) to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="VALUE"),
            "TARGET": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, old="OBJECT", menu=MenuInfo("sensing_of_object_menu", inner="OBJECT")),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.MUTABLE_SPRITE_PROPERTY, old="PROPERTY"),
        },
    ),
    "sensing_of": BlockInfo(
        block_type="stringReporter",
        new_opcode="[PROPERTY] of ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, old="OBJECT", menu=MenuInfo("sensing_of_object_menu", inner="OBJECT")),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.READABLE_SPRITE_PROPERTY, old="PROPERTY"),
        },
    ),
    "sensing_current": BlockInfo(
        block_type="stringReporter",
        new_opcode="current [PROPERTY]",
        can_have_monitor="True",
    ),
    "sensing_dayssince2000": BlockInfo(
        block_type="stringReporter",
        new_opcode="days since 2000",
        can_have_monitor="True",
    ),
    "sensing_mobile": BlockInfo(
        block_type="booleanReporter",
        new_opcode="mobile?",
    ),
    "sensing_fingerdown": BlockInfo(
        block_type="booleanReporter",
        new_opcode="finger ([INDEX]) down?",
        inputs={
            "INDEX": InputInfo(InputType.FINGER_INDEX, old="FINGER_OPTION", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "sensing_fingertapped": BlockInfo(
        block_type="booleanReporter",
        new_opcode="finger ([INDEX]) tapped?",
        inputs={
            "INDEX": InputInfo(InputType.FINGER_INDEX, old="FINGER_OPTION", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "sensing_fingerx": BlockInfo(
        block_type="stringReporter",
        new_opcode="finger ([INDEX]) x",
        inputs={
            "INDEX": InputInfo(InputType.FINGER_INDEX, old="FINGER_OPTION", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "sensing_fingery": BlockInfo(
        block_type="stringReporter",
        new_opcode="finger ([INDEX]) y",
        inputs={
            "INDEX": InputInfo(InputType.FINGER_INDEX, old="FINGER_OPTION", menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        },
    ),
    "sensing_username": BlockInfo(
        block_type="stringReporter",
        new_opcode="username",
        can_have_monitor="True",
    ),
    "sensing_loggedin": BlockInfo(
        block_type="booleanReporter",
        new_opcode="logged in?",
        can_have_monitor="True",
    ),
})