from pypenguin.opcode_info.data_imports import *

scratch_music = OpcodeInfoGroup(name="scratch_music", opcode_info=DualKeyDict({
    ("music_playDrumForBeats", "play drum ([DRUM]) for (BEATS) beats"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DRUM", "DRUM"): InputInfo(InputType.DRUM, menu=MenuInfo("music_menu_DRUM", inner="DRUM")),
            ("BEATS", "BEATS"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("music_restForBeats", "rest for (BEATS) beats"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("BEATS", "BEATS"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("music_playNoteForBeats", "play note ([NOTE]) for (BEATS) beats"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("NOTE", "NOTE"): InputInfo(InputType.NOTE, menu=MenuInfo("note", inner="NOTE")),
            ("BEATS", "BEATS"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("music_setInstrument", "set instrument to ([INSTRUMENT])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("INSTRUMENT", "INSTRUMENT"): InputInfo(InputType.INSTRUMENT, menu=MenuInfo("music_menu_INSTRUMENT", inner="INSTRUMENT")),
        }),
    ),

    ("music_setTempo", "set tempo to (TEMPO)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEMPO", "TEMPO"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("music_changeTempo", "change tempo by (TEMPO)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEMPO", "TEMPO"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("music_getTempo", "tempo"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),

}))