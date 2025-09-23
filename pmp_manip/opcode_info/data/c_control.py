from pmp_manip.opcode_info.data_imports import *

c_control = OpcodeInfoGroup(name="c_control", opcode_info=DualKeyDict({
    ("control_wait", "&control::wait (SECONDS) seconds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DURATION", "SECONDS"): InputInfo(BuiltinInputType.POSITIVE_NUMBER),
        }),
    ),

    ("control_waitsecondsoruntil", "&control::wait (SECONDS) seconds or until <CONDITION>"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DURATION", "SECONDS"): InputInfo(BuiltinInputType.POSITIVE_NUMBER),
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("control_repeat", "&control::repeat (TIMES) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TIMES", "TIMES"): InputInfo(BuiltinInputType.NUMBER),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_forever", "&control::forever {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_for_each", "&control::for each [VARIABLE] in (RANGE) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "RANGE"): InputInfo(BuiltinInputType.POSITIVE_INTEGER),
            ("BODY", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
        }),
    ),

    ("control_exitLoop", "&control::escape loop"): OpcodeInfo(
        opcode_type=OpcodeType.ENDING_STATEMENT,
    ),

    ("control_continueLoop", "&control::continue loop"): OpcodeInfo(
        opcode_type=OpcodeType.ENDING_STATEMENT,
    ),

    ("control_switch", "&control::switch (CONDITION) {CASES}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.ROUND),
            ("SUBSTACK", "CASES"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_switch_default", "&control::switch (CONDITION) {CASES} default {DEFAULT}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.ROUND),
            ("SUBSTACK1", "CASES"): InputInfo(BuiltinInputType.SCRIPT),
            ("SUBSTACK2", "DEFAULT"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_exitCase", "&control::exit case"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("control_case_next", "&control::run next case when (CONDITION)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("control_case", "&control::case (CONDITION) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.TEXT),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_if", "&control::if <CONDITION> then {THEN}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("SUBSTACK", "THEN"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_if_else", "&control::if <CONDITION> then {THEN} else {ELSE}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("SUBSTACK", "THEN"): InputInfo(BuiltinInputType.SCRIPT),
            ("SUBSTACK2", "ELSE"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_if_return_else_return", "&control::if <CONDITION> then (TRUEVALUE) else (FALSEVALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("boolean", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("TEXT1", "TRUEVALUE"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT2", "FALSEVALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("control_wait_until", "&control::wait until <CONDITION>"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("control_repeat_until", "&control::repeat until <CONDITION> {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_while", "&control::while <CONDITION> {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_all_at_once", "&control::all at once {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_run_as_sprite", "&control::as ([TARGET]) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("RUN_AS_OPTION", "TARGET"): InputInfo(BuiltinInputType.STAGE_OR_OTHER_SPRITE, menu=MenuInfo("control_run_as_sprite_menu", inner="RUN_AS_OPTION")),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_try_catch", "&control::try to do {TRY} if a block errors {IFERROR}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SUBSTACK", "TRY"): InputInfo(BuiltinInputType.SCRIPT),
            ("SUBSTACK2", "IFERROR"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_throw_error", "&control::throw error (ERROR)"): OpcodeInfo(
        opcode_type=OpcodeType.ENDING_STATEMENT,
        inputs=DualKeyDict({
            ("ERROR", "ERROR"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("control_error", "&control::error"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
    ),

    ("control_backToGreenFlag", "&control::run flag"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("control_stop_sprite", "&control::stop sprite ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("STOP_OPTION", "TARGET"): InputInfo(BuiltinInputType.STAGE_OR_OTHER_SPRITE, menu=MenuInfo("control_stop_sprite_menu", inner="STOP_OPTION")),
        }),
    ),

    ("control_stop", "&control::stop script [TARGET]"): OpcodeInfo(
        opcode_type=OpcodeType.DYNAMIC,
        dropdowns=DualKeyDict({
            ("STOP_OPTION", "TARGET"): DropdownInfo(BuiltinDropdownType.STOP_SCRIPT_TARGET),
        }),
    ),

    ("control_start_as_clone", "&control::when I start as a clone"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),

    ("control_create_clone_of", "&control::create clone of ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CLONE_OPTION", "TARGET"): InputInfo(BuiltinInputType.CLONING_TARGET, menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        }),
    ),

    ("control_delete_clones_of", "&control::delete clones of ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CLONE_OPTION", "TARGET"): InputInfo(BuiltinInputType.CLONING_TARGET, menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        }),
    ),

    ("control_delete_this_clone", "&control::delete this clone"): OpcodeInfo(
        opcode_type=OpcodeType.ENDING_STATEMENT,
    ),

    ("control_is_clone", "&control::is clone?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
    ),
}))