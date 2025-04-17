from block_info.basis import *

events = BlockInfoSet(name="events", opcode_prefix="event", block_infos={
    "whenflagclicked": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when green flag clicked",
    ),
    "whenstopclicked": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when stop clicked",
    ),
    "always": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="always",
    ),
    "whenanything": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when <CONDITION>",
        inputs={
            "ANYTHING": InputInfo(InputType.BOOLEAN, new="CONDITION"),
        },
    ),
    "whenkeypressed": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when [KEY] key pressed",
    ),
    "whenkeyhit": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when [KEY] key hit",
    ),
    "whenmousescrolled": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when mouse is scrolled [DIRECTION]",
    ),
    "whenthisspriteclicked": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when this sprite clicked",
    ),
    "whenstageclicked": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when stage clicked",
    ),
    "whenbackdropswitchesto": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when backdrop switches to [BACKDROP]",
    ),
    "whengreaterthan": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when [OPTION] > (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, new="VALUE"),
        },
        dropdowns={
            "WHENGREATERTHANMENU": DropdownInfo(DropdownType.LOUDNESS_TIMER, new="OPTION"),
        },
    ),
    "whenbroadcastreceived": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when I receive [MESSAGE]",
    ),
    "broadcast": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="broadcast ([MESSAGE])",
        inputs={
            "BROADCAST_INPUT": InputInfo(InputType.BROADCAST, new="MESSAGE"),
        },
    ),
    "broadcastandwait": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="broadcast ([MESSAGE]) and wait",
        inputs={
            "BROADCAST_INPUT": InputInfo(InputType.BROADCAST, new="MESSAGE"),
        },
    ),
})