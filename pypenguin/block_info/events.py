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
            "CONDITION": InputInfo(InputType.BOOLEAN, old="ANYTHING"),
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
            "VALUE": InputInfo(InputType.NUMBER, old="VALUE"),
        },
        dropdowns={
            "OPTION": DropdownInfo(DropdownType.LOUDNESS_TIMER, old="WHENGREATERTHANMENU"),
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
            "MESSAGE": InputInfo(InputType.BROADCAST, old="BROADCAST_INPUT"),
        },
    ),
    "broadcastandwait": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="broadcast ([MESSAGE]) and wait",
        inputs={
            "MESSAGE": InputInfo(InputType.BROADCAST, old="BROADCAST_INPUT"),
        },
    ),
})