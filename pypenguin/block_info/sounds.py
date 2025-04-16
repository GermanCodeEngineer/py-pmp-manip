from block_info.basis import *

sounds = BlockInfoSet(name="sounds", opcode_prefix="sound", block_infos={
    "playuntildone": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="play sound ([SOUND]) until done",
        inputs={
            "SOUND": InputInfo(InputType.SOUND, old="SOUND_MENU", menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        },
    ),
    "play_at_seconds_until_done": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="play sound ([SOUND]) starting at (SECONDS) seconds until done",
        inputs={
            "SOUND": InputInfo(InputType.SOUND, old="SOUND_MENU", menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
            "SECONDS": InputInfo(InputType.NUMBER, old="VALUE"),
        },
    ),
    "stop": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="stop sound ([SOUND])",
        inputs={
            "SOUND": InputInfo(InputType.SOUND, old="SOUND_MENU", menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        },
    ),
    "playallsounds": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="play all sounds",
    ),
    "stopallsounds": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="stop all sounds",
    ),
    "set_stop_fadeout_to": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set fadeout to (SECONDS) seconds on ([SOUND])",
        inputs={
            "SECONDS": InputInfo(InputType.NUMBER, old="VALUE"),
            "SOUND": InputInfo(InputType.SOUND, old="SOUND_MENU", menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        },
    ),
    "isSoundPlaying": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="is ([SOUND]) playing?",
        inputs={
            "SOUND": InputInfo(InputType.SOUND, old="SOUND_MENU", menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        },
    ),
    "getLength": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="length of ([SOUND])?",
        inputs={
            "SOUND": InputInfo(InputType.SOUND, old="SOUND_MENU", menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        },
    ),
    "changeeffectby": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change [EFFECT] sound effect by (AMOUNT)",
        inputs={
            "AMOUNT": InputInfo(InputType.NUMBER, old="VALUE"),
        },
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SOUND_EFFECT, old="EFFECT"),
        },
    ),
    "seteffectto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [EFFECT] sound effect to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="VALUE"),
        },
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SOUND_EFFECT, old="EFFECT"),
        },
    ),
    "cleareffects": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="clear sound effects",
    ),
    "getEffectValue": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[EFFECT] sound effect",
        can_have_monitor="True",
    ),
    "changevolumeby": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change volume by (AMOUNT)",
        inputs={
            "AMOUNT": InputInfo(InputType.NUMBER, old="VOLUME"),
        },
    ),
    "setvolumeto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set volume to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="VOLUME"),
        },
    ),
    "volume": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="volume",
        can_have_monitor="True",
    ),
})