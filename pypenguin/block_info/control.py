from block_info.basis import *

control = BlockInfoSet(name="control", opcode_prefix="control", blocks={
    "control_wait": BlockInfo(
        block_type="instruction",
        new_opcode="wait (SECONDS) seconds",
        inputs={
            "SECONDS": InputInfo(InputType.POSITIVE_NUMBER, old="DURATION"),
        },
    ),
    "control_waitsecondsoruntil": BlockInfo(
        block_type="instruction",
        new_opcode="wait (SECONDS) seconds or until <CONDITION>",
        inputs={
            "SECONDS": InputInfo(InputType.POSITIVE_NUMBER, old="DURATION"),
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
        },
    ),
    "control_repeat": BlockInfo(
        block_type="instruction",
        new_opcode="repeat (TIMES) {BODY}",
        inputs={
            "TIMES": InputInfo(InputType.NUMBER, old="TIMES"),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_forever": BlockInfo(
        block_type="instruction",
        new_opcode="forever {BODY}",
        inputs={
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_for_each": BlockInfo(
        block_type="instruction",
        new_opcode="for each [VARIABLE] in (RANGE) {BODY}",
        inputs={
            "RANGE": InputInfo(InputType.POSITIVE_INTEGER, old="VALUE"),
            "BODY": InputInfo(InputType.SCRIPT, old="BODY"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
        },
    ),
    "control_exitLoop": BlockInfo(
        block_type="lastInstruction",
        new_opcode="escape loop",
    ),
    "control_continueLoop": BlockInfo(
        block_type="lastInstruction",
        new_opcode="continue loop",
    ),
    "control_switch": BlockInfo(
        block_type="instruction",
        new_opcode="switch (CONDITION) {CASES}",
        inputs={
            "CONDITION": InputInfo(InputType.ROUND, old="CONDITION"),
            "CASES": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_switch_default": BlockInfo(
        block_type="instruction",
        new_opcode="switch (CONDITION) {CASES} default {DEFAULT}",
        inputs={
            "CONDITION": InputInfo(InputType.ROUND, old="CONDITION"),
            "CASES": InputInfo(InputType.SCRIPT, old="SUBSTACK1"),
            "DEFAULT": InputInfo(InputType.SCRIPT, old="SUBSTACK2"),
        },
    ),
    "control_exitCase": BlockInfo(
        block_type="instruction",
        new_opcode="exit case",
    ),
    "control_case_next": BlockInfo(
        block_type="instruction",
        new_opcode="run next case when (CONDITION)",
        inputs={
            "CONDITION": InputInfo(InputType.TEXT, old="CONDITION"),
        },
    ),
    "control_case": BlockInfo(
        block_type="instruction",
        new_opcode="case (CONDITION) {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.TEXT, old="CONDITION"),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_if": BlockInfo(
        block_type="instruction",
        new_opcode="if <CONDITION> then {THEN}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
            "THEN": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_if_else": BlockInfo(
        block_type="instruction",
        new_opcode="if <CONDITION> then {THEN} else {ELSE}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
            "THEN": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
            "ELSE": InputInfo(InputType.SCRIPT, old="SUBSTACK2"),
        },
    ),
    "control_wait_until": BlockInfo(
        block_type="instruction",
        new_opcode="wait until <CONDITION>",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
        },
    ),
    "control_repeat_until": BlockInfo(
        block_type="instruction",
        new_opcode="repeat until <CONDITION> {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_while": BlockInfo(
        block_type="instruction",
        new_opcode="while <CONDITION> {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_if_return_else_return": BlockInfo(
        block_type="stringReporter",
        new_opcode="if <CONDITION> then (TRUEVALUE) else (FALSEVALUE)",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="boolean"),
            "TRUEVALUE": InputInfo(InputType.TEXT, old="TEXT1"),
            "FALSEVALUE": InputInfo(InputType.TEXT, old="TEXT2"),
        },
    ),
    "control_all_at_once": BlockInfo(
        block_type="instruction",
        new_opcode="all at once {BODY}",
        inputs={
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_run_as_sprite": BlockInfo(
        block_type="instruction",
        new_opcode="as ([TARGET]) {BODY}",
        inputs={
            "TARGET": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, old="RUN_AS_OPTION", menu=MenuInfo("control_run_as_sprite_menu", inner="RUN_AS_OPTION")),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "control_try_catch": BlockInfo(
        block_type="instruction",
        new_opcode="try to do {TRY} if a block errors {IFERROR}",
        inputs={
            "TRY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
            "IFERROR": InputInfo(InputType.SCRIPT, old="SUBSTACK2"),
        },
    ),
    "control_throw_error": BlockInfo(
        block_type="lastInstruction",
        new_opcode="throw error (ERROR)",
        inputs={
            "ERROR": InputInfo(InputType.TEXT, old="ERROR"),
        },
    ),
    "control_error": BlockInfo(
        block_type="stringReporter",
        new_opcode="error",
    ),
    "control_backToGreenFlag": BlockInfo(
        block_type="instruction",
        new_opcode="run flag",
    ),
    "control_stop_sprite": BlockInfo(
        block_type="instruction",
        new_opcode="stop sprite ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, old="STOP_OPTION", menu=MenuInfo("control_stop_sprite_menu", inner="STOP_OPTION")),
        },
    ),
    "control_stop": BlockInfo(
        block_type="dynamic",
        new_opcode="stop script [TARGET]",
    ),
    "control_start_as_clone": BlockInfo(
        block_type="hat",
        new_opcode="when I start as a clone",
    ),
    "control_create_clone_of": BlockInfo(
        block_type="instruction",
        new_opcode="create clone of ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.CLONING_TARGET, old="CLONE_OPTION", menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        },
    ),
    "control_delete_clones_of": BlockInfo(
        block_type="instruction",
        new_opcode="delete clones of ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.CLONING_TARGET, old="CLONE_OPTION", menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        },
    ),
    "control_delete_this_clone": BlockInfo(
        block_type="lastInstruction",
        new_opcode="delete this clone",
    ),
    "control_is_clone": BlockInfo(
        block_type="booleanReporter",
        new_opcode="is clone?",
    ),
})