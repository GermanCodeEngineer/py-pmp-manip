from pmp_manip.opcode_info.data_imports import *

ext_scratch_music = OpcodeInfoGroup(name="scratch_music", opcode_info=DualKeyDict({
    ("music_playDrumForBeats", "play drum ([DRUM]) for (BEATS) beats"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DRUM", "DRUM"): InputInfo(BuiltinInputType.DRUM, menu=MenuInfo("music_menu_DRUM", inner="DRUM")),
            ("BEATS", "BEATS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("music_restForBeats", "rest for (BEATS) beats"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("BEATS", "BEATS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("music_playNoteForBeats", "play note ([NOTE]) for (BEATS) beats"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("NOTE", "NOTE"): InputInfo(BuiltinInputType.NOTE, menu=MenuInfo("note", inner="NOTE")),
            ("BEATS", "BEATS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("music_setInstrument", "set instrument to ([INSTRUMENT])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("INSTRUMENT", "INSTRUMENT"): InputInfo(BuiltinInputType.INSTRUMENT, menu=MenuInfo("music_menu_INSTRUMENT", inner="INSTRUMENT")),
        }),
    ),

    ("music_setTempo", "set tempo to (TEMPO)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEMPO", "TEMPO"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("music_changeTempo", "change tempo by (TEMPO)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEMPO", "TEMPO"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("music_getTempo", "tempo"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
        monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
    ),

}))

ext_scratch_music.add_opcode("note", "#music: NOTE MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
ext_scratch_music.add_opcode("music_menu_DRUM", "#music: DRUM MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))
ext_scratch_music.add_opcode("music_menu_INSTRUMENT", "#music: INSTRUMENT MENU", OpcodeInfo(
    opcode_type=OpcodeType.MENU,
))

