from pmp_manip.opcode_info.data_imports import *

c_sounds = OpcodeInfoGroup(name="c_sounds", opcode_info=DualKeyDict({
    ("sound_playuntildone", "&sound::play sound ([SOUND]) until done"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_play_at_seconds_until_done", "&sound::play sound ([SOUND]) starting at (SECONDS) seconds until done"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
            ("VALUE", "SECONDS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),
    
    ("sound_play", "&sound::start sound ([SOUND])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
       }),
    ),
    
    ("sound_play_at_seconds", "&sound::start sound ([SOUND]) at (SECONDS) seconds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
            ("VALUE", "SECONDS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),
    
    ("sound_stop", "&sound::stop sound ([SOUND])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),
    
    ("sound_playallsounds", "&sound::play all sounds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("sound_stopallsounds", "&sound::stop all sounds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("sound_set_stop_fadeout_to", "&sound::set fadeout to (SECONDS) seconds on ([SOUND])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "SECONDS"): InputInfo(BuiltinInputType.NUMBER),
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_isSoundPlaying", "&sound::is ([SOUND]) playing?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_getLength", "&sound::length of ([SOUND])?"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("SOUND_MENU", "SOUND"): InputInfo(BuiltinInputType.SOUND, menu=MenuInfo("sound_sounds_menu", inner="SOUND_MENU")),
        }),
    ),

    ("sound_changeeffectby", "&sound::change [EFFECT] sound effect by (AMOUNT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "AMOUNT"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(BuiltinDropdownType.SOUND_EFFECT),
        }),
    ),

    ("sound_seteffectto", "&sound::set [EFFECT] sound effect to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(BuiltinDropdownType.SOUND_EFFECT),
        }),
    ),

    ("sound_cleareffects", "&sound::clear sound effects"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("sound_getEffectValue", "&sounds::[EFFECT] effect"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(BuiltinDropdownType.SOUND_EFFECT),
        }),
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.SPRITE_OPCMAIN_PARAMS,
    ),

    ("sound_changevolumeby", "&sound::change volume by (AMOUNT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VOLUME", "AMOUNT"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("sound_setvolumeto", "&sound::set volume to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VOLUME", "VALUE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("sound_volume", "&sound::volume"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.SPRITE_OPCMAIN,
    ),

}))