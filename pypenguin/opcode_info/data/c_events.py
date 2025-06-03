from pypenguin.utility import DualKeyDict

from pypenguin.opcode_info.api import OpcodeInfoGroup, OpcodeInfo, OpcodeType, InputInfo, InputType, DropdownInfo, DropdownType, MenuInfo


events = OpcodeInfoGroup(name="events", opcode_info=DualKeyDict({
    ("event_whenflagclicked", "when green flag clicked"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),
    ("event_whenstopclicked", "when stop clicked"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),
    ("event_always", "always"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),
    ("event_whenanything", "when <CONDITION>"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        inputs=DualKeyDict({
            ("ANYTHING", "CONDITION"): InputInfo(InputType.BOOLEAN),
        }),
    ),
    ("event_whenkeypressed", "when [KEY] key pressed"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("KEY_OPTION", "KEY"): DropdownInfo(DropdownType.KEY),
        }),
    ),
    ("event_whenkeyhit", "when [KEY] key hit"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("KEY_OPTION", "KEY"): DropdownInfo(DropdownType.KEY),
        }),
    ),
    ("event_whenmousescrolled", "when mouse is scrolled [DIRECTION]"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("KEY_OPTION", "DIRECTION"): DropdownInfo(DropdownType.UP_DOWN),
        }),
    ),
    ("event_whenthisspriteclicked", "when this sprite clicked"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),
    ("event_whenstageclicked", "when stage clicked"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),
    ("event_whenbackdropswitchesto", "when backdrop switches to [BACKDROP]"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("BACKDROP", "BACKDROP"): DropdownInfo(DropdownType.BACKDROP),
        }),
    ),
    ("event_whengreaterthan", "when [OPTION] > (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("WHENGREATERTHANMENU", "OPTION"): DropdownInfo(DropdownType.LOUDNESS_TIMER),
        }),
    ),
    ("event_whenbroadcastreceived", "when I receive [MESSAGE]"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        dropdowns=DualKeyDict({
            ("BROADCAST_OPTION", "MESSAGE"): DropdownInfo(DropdownType.BROADCAST),
        }),
    ),
    ("event_broadcast", "broadcast ([MESSAGE])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("BROADCAST_INPUT", "MESSAGE"): InputInfo(InputType.BROADCAST),
        }),
    ),
    ("event_broadcastandwait", "broadcast ([MESSAGE]) and wait"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("BROADCAST_INPUT", "MESSAGE"): InputInfo(InputType.BROADCAST),
        }),
    ),
}))