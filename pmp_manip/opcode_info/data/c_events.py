from pmp_manip.opcode_info.data_imports import *

c_events = OpcodeInfoGroup(name="c_events", opcode_info=DualKeyDict({
    ("event_whenflagclicked", "&events::when green flag clicked"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),

    ("event_whenstopclicked", "&events::when stop clicked"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),

    ("event_always", "&events::always"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),

    ("event_whenanything", "&events::when <CONDITION>"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        inputs=DualKeyDict({
            ("ANYTHING", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("event_whenkeypressed", "&events::when [KEY] key pressed"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("KEY_OPTION", "KEY"): DropdownInfo(BuiltinDropdownType.KEY),
        }),
    ),

    ("event_whenkeyhit", "&events::when [KEY] key hit"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("KEY_OPTION", "KEY"): DropdownInfo(BuiltinDropdownType.KEY),
        }),
    ),

    ("event_whenmousescrolled", "&events::when mouse is scrolled [DIRECTION]"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("KEY_OPTION", "DIRECTION"): DropdownInfo(BuiltinDropdownType.UP_DOWN),
        }),
    ),

    ("event_whenthisspriteclicked", "&events::when this sprite clicked"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),

    ("event_whenstageclicked", "&events::when stage clicked"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),

    ("event_whenbackdropswitchesto", "&events::when backdrop switches to [BACKDROP]"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("BACKDROP", "BACKDROP"): DropdownInfo(BuiltinDropdownType.BACKDROP),
        }),
    ),

    ("event_whengreaterthan", "&events::when [OPTION] > (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("WHENGREATERTHANMENU", "OPTION"): DropdownInfo(BuiltinDropdownType.LOUDNESS_TIMER),
        }),
    ),

    ("event_whenbroadcastreceived", "&events::when I receive [MESSAGE]"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("BROADCAST_OPTION", "MESSAGE"): DropdownInfo(BuiltinDropdownType.BROADCAST),
        }),
    ),

    ("event_broadcast", "&events::broadcast ([MESSAGE])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("BROADCAST_INPUT", "MESSAGE"): InputInfo(BuiltinInputType.BROADCAST),
        }),
    ),

    ("event_broadcastandwait", "&events::broadcast ([MESSAGE]) and wait"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("BROADCAST_INPUT", "MESSAGE"): InputInfo(BuiltinInputType.BROADCAST),
        }),
    ),

}))