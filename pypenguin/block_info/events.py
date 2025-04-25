from block_info.basis import *

events = CategoryOpcodesInfo(name="events", opcode_prefix="event", block_infos={
    "whenflagclicked": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when green flag clicked",
    ),
    "whenstopclicked": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when stop clicked",
    ),
    "always": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="always",
    ),
    "whenanything": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when <CONDITION>",
        inputs={
            "ANYTHING": InputInfo(InputType.BOOLEAN, new="CONDITION"),
        },
    ),
    "whenkeypressed": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when [KEY] key pressed",
        dropdowns={
            "KEY_OPTION": DropdownInfo(DropdownType.KEY, new="KEY"),
        },
    ),
    "whenkeyhit": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when [KEY] key hit",
        dropdowns={
            "KEY_OPTION": DropdownInfo(DropdownType.KEY, new="KEY"),
        },
    ),
    "whenmousescrolled": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when mouse is scrolled [DIRECTION]",
        dropdowns={
            "KEY_OPTION": DropdownInfo(DropdownType.UP_DOWN, new="DIRECTION"),
        },
    ),
    "whenthisspriteclicked": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when this sprite clicked",
    ),
    "whenstageclicked": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when stage clicked",
    ),
    "whenbackdropswitchesto": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when backdrop switches to [BACKDROP]",
        dropdowns={
            "BACKDROP": DropdownInfo(DropdownType.BACKDROP, new="BACKDROP"),
        },
    ),
    "whengreaterthan": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when [OPTION] > (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, new="VALUE"),
        },
        dropdowns={
            "WHENGREATERTHANMENU": DropdownInfo(DropdownType.LOUDNESS_TIMER, new="OPTION"),
        },
    ),
    "whenbroadcastreceived": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="when I receive [MESSAGE]",
        dropdowns={
            "BROADCAST_OPTION": DropdownInfo(DropdownType.BROADCAST, new="MESSAGE"),
        },
    ),
    "broadcast": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="broadcast ([MESSAGE])",
        inputs={
            "BROADCAST_INPUT": InputInfo(InputType.BROADCAST, new="MESSAGE"),
        },
    ),
    "broadcastandwait": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="broadcast ([MESSAGE]) and wait",
        inputs={
            "BROADCAST_INPUT": InputInfo(InputType.BROADCAST, new="MESSAGE"),
        },
    ),
})