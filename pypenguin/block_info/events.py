from block_info.basis import *

events = BlockInfoSet(name="events", opcode_prefix="event", blocks={
    "event_whenflagclicked": BlockInfo(
        block_type="hat",
        new_opcode="when green flag clicked",
    ),
    "event_whenstopclicked": BlockInfo(
        block_type="hat",
        new_opcode="when stop clicked",
    ),
    "event_always": BlockInfo(
        block_type="hat",
        new_opcode="always",
    ),
    "event_whenanything": BlockInfo(
        block_type="hat",
        new_opcode="when <CONDITION>",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="ANYTHING"),
        },
    ),
    "event_whenkeypressed": BlockInfo(
        block_type="hat",
        new_opcode="when [KEY] key pressed",
    ),
    "event_whenkeyhit": BlockInfo(
        block_type="hat",
        new_opcode="when [KEY] key hit",
    ),
    "event_whenmousescrolled": BlockInfo(
        block_type="hat",
        new_opcode="when mouse is scrolled [DIRECTION]",
    ),
    "event_whenthisspriteclicked": BlockInfo(
        block_type="hat",
        new_opcode="when this sprite clicked",
    ),
    "event_whenstageclicked": BlockInfo(
        block_type="hat",
        new_opcode="when stage clicked",
    ),
    "event_whenbackdropswitchesto": BlockInfo(
        block_type="hat",
        new_opcode="when backdrop switches to [BACKDROP]",
    ),
    "event_whengreaterthan": BlockInfo(
        block_type="hat",
        new_opcode="when [OPTION] > (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="VALUE"),
        },
        dropdowns={
            "OPTION": DropdownInfo(DropdownType.LOUDNESS_TIMER, old="WHENGREATERTHANMENU"),
        },
    ),
    "event_whenbroadcastreceived": BlockInfo(
        block_type="hat",
        new_opcode="when I receive [MESSAGE]",
    ),
    "event_broadcast": BlockInfo(
        block_type="instruction",
        new_opcode="broadcast ([MESSAGE])",
        inputs={
            "MESSAGE": InputInfo(InputType.BROADCAST, old="BROADCAST_INPUT"),
        },
    ),
    "event_broadcastandwait": BlockInfo(
        block_type="instruction",
        new_opcode="broadcast ([MESSAGE]) and wait",
        inputs={
            "MESSAGE": InputInfo(InputType.BROADCAST, old="BROADCAST_INPUT"),
        },
    ),
})