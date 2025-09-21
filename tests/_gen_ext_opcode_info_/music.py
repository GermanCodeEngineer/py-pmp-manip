from pmp_manip.opcode_info.data_imports import *

class ExtensionDropdownType(DropdownType):
    DRUM = DropdownTypeInfo(
        direct_values=["(1) Snare Drum", "(2) Bass Drum", "(3) Side Stick", "(4) Crash Cymbal", "(5) Open Hi-Hat", "(6) Closed Hi-Hat", "(7) Tambourine", "(8) Hand Clap", "(9) Claves", "(10) Wood Block", "(11) Cowbell", "(12) Triangle", "(13) Bongo", "(14) Conga", "(15) Cabasa", "(16) Guiro", "(17) Vibraslap", "(18) Cuica"],
        rules=[],
        old_direct_values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"],
        fallback=None,
    )
    INSTRUMENT = DropdownTypeInfo(
        direct_values=["(1) Piano", "(2) Electric Piano", "(3) Organ", "(4) Guitar", "(5) Electric Guitar", "(6) Bass", "(7) Pizzicato", "(8) Cello", "(9) Trombone", "(10) Clarinet", "(11) Saxophone", "(12) Flute", "(13) Wooden Flute", "(14) Bassoon", "(15) Choir", "(16) Vibraphone", "(17) Music Box", "(18) Steel Drum", "(19) Marimba", "(20) Synth Lead", "(21) Synth Pad"],
        rules=[],
        old_direct_values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"],
        fallback=None,
    )

class ExtensionInputType(InputType):
    DRUM = (InputMode.BLOCK_AND_DROPDOWN, None, ExtensionDropdownType.DRUM, 0)
    INSTRUMENT = (InputMode.BLOCK_AND_DROPDOWN, None, ExtensionDropdownType.INSTRUMENT, 1)

extension = OpcodeInfoGroup(
    name="music",
    opcode_info=DualKeyDict({
        ("music_midiPlayDrumForBeats", "music::play drum ([DRUM]) for (BEATS) beats {{id=music_midiPlayDrumForBeats}}"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("DRUM", "DRUM"): InputInfo(
                    type=ExtensionInputType.DRUM,
                    menu=MenuInfo(opcode="music_menu_DRUM", inner="DRUM"),
                ),
                ("BEATS", "BEATS"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_restForBeats", "music::rest for (BEATS) beats"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("BEATS", "BEATS"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_playNoteForBeats", "music::play note ([NOTE]) for (BEATS) beats"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("NOTE", "NOTE"): InputInfo(
                    type=BuiltinInputType.NOTE,
                    menu=MenuInfo(opcode="note", inner="NOTE"),
                ),
                ("BEATS", "BEATS"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_setInstrument", "music::set instrument to ([INSTRUMENT])"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("INSTRUMENT", "INSTRUMENT"): InputInfo(
                    type=ExtensionInputType.INSTRUMENT,
                    menu=MenuInfo(opcode="music_menu_INSTRUMENT", inner="INSTRUMENT"),
                ),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_midiSetInstrument", "music::set instrument to (INSTRUMENT)"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("INSTRUMENT", "INSTRUMENT"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_setTempo", "music::set tempo to (TEMPO)"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("TEMPO", "TEMPO"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_changeTempo", "music::change tempo by (TEMPO)"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("TEMPO", "TEMPO"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_getTempo", "music::tempo"): OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=True,
            monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_playDrumForBeats", "music::play drum ([DRUM]) for (BEATS) beats {{id=music_playDrumForBeats}}"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("DRUM", "DRUM"): InputInfo(
                    type=ExtensionInputType.DRUM,
                    menu=MenuInfo(opcode="music_menu_DRUM", inner="DRUM"),
                ),
                ("BEATS", "BEATS"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_menu_DRUM", "music_menu_DRUM"): OpcodeInfo(
            opcode_type=OpcodeType.MENU,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=True,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("music_menu_INSTRUMENT", "music_menu_INSTRUMENT"): OpcodeInfo(
            opcode_type=OpcodeType.MENU,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=True,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
    }),
)