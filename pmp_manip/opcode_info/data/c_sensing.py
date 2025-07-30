from pmp_manip.opcode_info.data_imports import *

c_sensing = OpcodeInfoGroup(name="c_sensing", opcode_info=DualKeyDict({
    ("sensing_touchingobject", "touching ([OBJECT]) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("TOUCHINGOBJECTMENU", "OBJECT"): InputInfo(BuiltinInputType.MOUSE_EDGE_OR_OTHER_SPRITE, menu=MenuInfo("sensing_touchingobjectmenu", inner="TOUCHINGOBJECTMENU")),
        }),
    ),

    ("sensing_objecttouchingobject", "([OBJECT]) touching ([SPRITE]) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("FULLTOUCHINGOBJECTMENU", "OBJECT"): InputInfo(BuiltinInputType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE, menu=MenuInfo("sensing_fulltouchingobjectmenu", inner="FULLTOUCHINGOBJECTMENU")),
            ("SPRITETOUCHINGOBJECTMENU", "SPRITE"): InputInfo(BuiltinInputType.MYSELF_OR_OTHER_SPRITE, menu=MenuInfo("sensing_touchingobjectmenusprites", inner="SPRITETOUCHINGOBJECTMENU")),
        }),
    ),

    ("sensing_objecttouchingclonesprite", "([OBJECT]) touching clone of ([SPRITE]) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("FULLTOUCHINGOBJECTMENU", "OBJECT"): InputInfo(BuiltinInputType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE, menu=MenuInfo("sensing_fulltouchingobjectmenu", inner="FULLTOUCHINGOBJECTMENU")),
            ("SPRITETOUCHINGOBJECTMENU", "SPRITE"): InputInfo(BuiltinInputType.MYSELF_OR_OTHER_SPRITE, menu=MenuInfo("sensing_touchingobjectmenusprites", inner="SPRITETOUCHINGOBJECTMENU")),
        }),
    ),

    ("sensing_touchingcolor", "touching color (COLOR) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
        }),
    ),

    ("sensing_coloristouchingcolor", "color (COLOR1) is touching color (COLOR2) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("COLOR", "COLOR1"): InputInfo(BuiltinInputType.COLOR),
            ("COLOR2", "COLOR2"): InputInfo(BuiltinInputType.COLOR),
        }),
    ),

    ("sensing_getxyoftouchingsprite", "[COORDINATE] of touching ([OBJECT]) point"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("SPRITE", "OBJECT"): InputInfo(BuiltinInputType.MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("sensing_distancetomenu", inner="DISTANCETOMENU")),
        }),
        dropdowns=DualKeyDict({
            ("XY", "COORDINATE"): DropdownInfo(BuiltinDropdownType.X_OR_Y),
        }),
    ),

    ("sensing_distanceto", "distance to ([OBJECT])"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("DISTANCETOMENU", "OBJECT"): InputInfo(BuiltinInputType.MOUSE_OR_OTHER_SPRITE, menu=MenuInfo("sensing_distancetomenu", inner="DISTANCETOMENU")),
        }),
    ),

    ("sensing_distanceTo", "distance from (X1) (Y1) to (X2) (Y2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("x1", "X1"): InputInfo(BuiltinInputType.TEXT),
            ("y1", "Y1"): InputInfo(BuiltinInputType.TEXT),
            ("x2", "X2"): InputInfo(BuiltinInputType.TEXT),
            ("y2", "Y2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("sensing_directionTo", "direction to (X1) (Y1) from (X2) (Y2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("x2", "X1"): InputInfo(BuiltinInputType.TEXT),
            ("y2", "Y1"): InputInfo(BuiltinInputType.TEXT),
            ("x1", "X2"): InputInfo(BuiltinInputType.TEXT),
            ("y1", "Y2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("sensing_askandwait", "ask (QUESTION) and wait"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("QUESTION", "QUESTION"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("sensing_answer", "answer"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCMAIN,
    ),

    ("sensing_thing_is_text", "(STRING) is text?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "STRING"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("sensing_thing_is_number", "(STRING) is number?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "STRING"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("sensing_keypressed", "key ([KEY]) pressed?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("KEY_OPTION", "KEY"): InputInfo(BuiltinInputType.KEY, menu=MenuInfo("sensing_keyoptions", inner="KEY_OPTION")),
        }),
    ),

    ("sensing_keyhit", "key ([KEY]) hit?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("KEY_OPTION", "KEY"): InputInfo(BuiltinInputType.KEY, menu=MenuInfo("sensing_keyoptions", inner="KEY_OPTION")),
        }),
    ),

    ("sensing_mousescrolling", "is mouse scrolling ([DIRECTION]) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("SCROLL_OPTION", "DIRECTION"): InputInfo(BuiltinInputType.UP_DOWN, menu=MenuInfo("sensing_scrolldirections", inner="SCROLL_OPTION")),
        }),
    ),

    ("sensing_mousedown", "mouse down?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

    ("sensing_mouseclicked", "mouse clicked?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

    ("sensing_mousex", "mouse x"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

    ("sensing_mousey", "mouse y"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

    ("sensing_setclipboard", "add (TEXT) to clipboard"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("ITEM", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("sensing_getclipboard", "clipboard item"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

    ("sensing_setdragmode", "set drag mode [MODE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("DRAG_MODE", "MODE"): DropdownInfo(BuiltinDropdownType.DRAG_MODE),
        }),
    ),

    ("sensing_getdragmode", "draggable?"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.SPRITE_OPCMAIN,
    ),

    ("sensing_loudness", "loudness"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCMAIN,
    ),

    ("sensing_loud", "loud?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCMAIN,
    ),

    ("sensing_resettimer", "reset timer"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("sensing_timer", "timer"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCMAIN,
    ),

    ("sensing_set_of", "set [PROPERTY] of ([TARGET]) to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
            ("OBJECT", "TARGET"): InputInfo(BuiltinInputType.STAGE_OR_OTHER_SPRITE, menu=MenuInfo("sensing_of_object_menu", inner="OBJECT")),
        }),
        dropdowns=DualKeyDict({
            ("PROPERTY", "PROPERTY"): DropdownInfo(BuiltinDropdownType.MUTABLE_SPRITE_PROPERTY),
        }),
    ),

    ("sensing_of", "[PROPERTY] of ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("OBJECT", "TARGET"): InputInfo(BuiltinInputType.STAGE_OR_OTHER_SPRITE, menu=MenuInfo("sensing_of_object_menu", inner="OBJECT")),
        }),
        dropdowns=DualKeyDict({
            ("PROPERTY", "PROPERTY"): DropdownInfo(BuiltinDropdownType.READABLE_SPRITE_PROPERTY),
        }),
    ),

    ("sensing_current", "current [PROPERTY]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        dropdowns=DualKeyDict({
            ("CURRENTMENU", "PROPERTY"): DropdownInfo(BuiltinDropdownType.TIME_PROPERTY),
        }),
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCMAIN_LOWERPARAM,
    ),

    ("sensing_dayssince2000", "days since 2000"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

    ("sensing_mobile", "mobile?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
    ),

    ("sensing_fingerdown", "finger ([INDEX]) down?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("FINGER_OPTION", "INDEX"): InputInfo(BuiltinInputType.FINGER_INDEX, menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        }),
    ),

    ("sensing_fingertapped", "finger ([INDEX]) tapped?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("FINGER_OPTION", "INDEX"): InputInfo(BuiltinInputType.FINGER_INDEX, menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        }),
    ),

    ("sensing_fingerx", "finger ([INDEX]) x"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("FINGER_OPTION", "INDEX"): InputInfo(BuiltinInputType.FINGER_INDEX, menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        }),
    ),

    ("sensing_fingery", "finger ([INDEX]) y"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("FINGER_OPTION", "INDEX"): InputInfo(BuiltinInputType.FINGER_INDEX, menu=MenuInfo("sensing_fingeroptions", inner="FINGER_OPTION")),
        }),
    ),

    ("sensing_username", "username"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

    ("sensing_loggedin", "logged in?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

}))