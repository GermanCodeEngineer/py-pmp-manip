from pmp_manip.opcode_info.data_imports import *

c_sounds = OpcodeInfoGroup(name="c_sounds", opcode_info=DualKeyDict({
    ("sound_playuntildone", "play sound ([SOUND]) until done"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_play_at_seconds_until_done", "play sound ([SOUND]) starting at (SECONDS) seconds until done"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
            ("VALUE", "SECONDS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("sound_stop", "stop sound ([SOUND])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_playallsounds", "play all sounds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("sound_stopallsounds", "stop all sounds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("sound_set_stop_fadeout_to", "set fadeout to (SECONDS) seconds on ([SOUND])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "SECONDS"): InputInfo(BuiltinInputType.NUMBER),
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_isSoundPlaying", "is ([SOUND]) playing?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_getLength", "length of ([SOUND])?"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_changeeffectby", "change [EFFECT] sound effect by (AMOUNT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "AMOUNT"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(BuiltinDropdownType.SOUND_EFFECT),
        }),
    ),

    ("sound_seteffectto", "set [EFFECT] sound effect to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(BuiltinDropdownType.SOUND_EFFECT),
        }),
    ),

    ("sound_cleareffects", "clear sound effects"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("sound_getEffectValue", "[EFFECT] sound effect"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(BuiltinDropdownType.SOUND_EFFECT),
        }),
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.SPRITE_OPCMAIN_PARAMS,
    ),

    ("sound_changevolumeby", "change volume by (AMOUNT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VOLUME", "AMOUNT"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("sound_setvolumeto", "set volume to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VOLUME", "VALUE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("sound_volume", "volume"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.SPRITE_OPCMAIN,
    ),

}))