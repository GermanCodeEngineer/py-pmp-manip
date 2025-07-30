from pmp_manip.opcode_info.data_imports import *

c_control = OpcodeInfoGroup(name="c_control", opcode_info=DualKeyDict({
    ("control_wait", "wait (SECONDS) seconds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DURATION", "SECONDS"): InputInfo(BuiltinInputType.POSITIVE_NUMBER),
        }),
    ),

    ("control_waitsecondsoruntil", "wait (SECONDS) seconds or until <CONDITION>"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("DURATION", "SECONDS"): InputInfo(BuiltinInputType.POSITIVE_NUMBER),
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("control_repeat", "repeat (TIMES) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TIMES", "TIMES"): InputInfo(BuiltinInputType.NUMBER),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_forever", "forever {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_for_each", "for each [VARIABLE] in (RANGE) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "RANGE"): InputInfo(BuiltinInputType.POSITIVE_INTEGER),
            ("BODY", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
        }),
    ),

    ("control_exitLoop", "escape loop"): OpcodeInfo(
        opcode_type=OpcodeType.ENDING_STATEMENT,
    ),

    ("control_continueLoop", "continue loop"): OpcodeInfo(
        opcode_type=OpcodeType.ENDING_STATEMENT,
    ),

    ("control_switch", "switch (CONDITION) {CASES}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.ROUND),
            ("SUBSTACK", "CASES"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_switch_default", "switch (CONDITION) {CASES} default {DEFAULT}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.ROUND),
            ("SUBSTACK1", "CASES"): InputInfo(BuiltinInputType.SCRIPT),
            ("SUBSTACK2", "DEFAULT"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_exitCase", "exit case"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("control_case_next", "run next case when (CONDITION)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("control_case", "case (CONDITION) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.TEXT),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_if", "if <CONDITION> then {THEN}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("SUBSTACK", "THEN"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_if_else", "if <CONDITION> then {THEN} else {ELSE}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("SUBSTACK", "THEN"): InputInfo(BuiltinInputType.SCRIPT),
            ("SUBSTACK2", "ELSE"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_wait_until", "wait until <CONDITION>"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("control_repeat_until", "repeat until <CONDITION> {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_while", "while <CONDITION> {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CONDITION", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_if_return_else_return", "if <CONDITION> then (TRUEVALUE) else (FALSEVALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("boolean", "CONDITION"): InputInfo(BuiltinInputType.BOOLEAN),
            ("TEXT1", "TRUEVALUE"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT2", "FALSEVALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("control_all_at_once", "all at once {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_run_as_sprite", "as ([TARGET]) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("RUN_AS_OPTION", "TARGET"): InputInfo(BuiltinInputType.STAGE_OR_OTHER_SPRITE, menu=MenuInfo("control_run_as_sprite_menu", inner="RUN_AS_OPTION")),
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_try_catch", "try to do {TRY} if a block errors {IFERROR}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SUBSTACK", "TRY"): InputInfo(BuiltinInputType.SCRIPT),
            ("SUBSTACK2", "IFERROR"): InputInfo(BuiltinInputType.SCRIPT),
        }),
    ),

    ("control_throw_error", "throw error (ERROR)"): OpcodeInfo(
        opcode_type=OpcodeType.ENDING_STATEMENT,
        inputs=DualKeyDict({
            ("ERROR", "ERROR"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("control_error", "error"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
    ),

    ("control_backToGreenFlag", "run flag"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("control_stop_sprite", "stop sprite ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("STOP_OPTION", "TARGET"): InputInfo(BuiltinInputType.STAGE_OR_OTHER_SPRITE, menu=MenuInfo("control_stop_sprite_menu", inner="STOP_OPTION")),
        }),
    ),

    ("control_stop", "stop script [TARGET]"): OpcodeInfo(
        opcode_type=OpcodeType.DYNAMIC,
        dropdowns=DualKeyDict({
            ("STOP_OPTION", "TARGET"): DropdownInfo(BuiltinDropdownType.STOP_SCRIPT_TARGET),
        }),
    ),

    ("control_start_as_clone", "when I start as a clone"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
    ),

    ("control_create_clone_of", "create clone of ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CLONE_OPTION", "TARGET"): InputInfo(BuiltinInputType.CLONING_TARGET, menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        }),
    ),

    ("control_delete_clones_of", "delete clones of ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CLONE_OPTION", "TARGET"): InputInfo(BuiltinInputType.CLONING_TARGET, menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        }),
    ),

    ("control_delete_this_clone", "delete this clone"): OpcodeInfo(
        opcode_type=OpcodeType.ENDING_STATEMENT,
    ),

    ("control_is_clone", "is clone?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
    ),

}))