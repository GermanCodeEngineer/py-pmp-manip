from block_info.basis import *

control = BlockInfoSet(name="control", opcode_prefix="control", block_infos={
    "wait": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="wait (SECONDS) seconds",
        inputs={
            "SECONDS": InputInfo(InputType.POSITIVE_NUMBER, old="DURATION"),
        },
    ),
    "waitsecondsoruntil": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="wait (SECONDS) seconds or until <CONDITION>",
        inputs={
            "SECONDS": InputInfo(InputType.POSITIVE_NUMBER, old="DURATION"),
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
        },
    ),
    "repeat": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="repeat (TIMES) {BODY}",
        inputs={
            "TIMES": InputInfo(InputType.NUMBER, old="TIMES"),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "forever": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="forever {BODY}",
        inputs={
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "for_each": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="for each [VARIABLE] in (RANGE) {BODY}",
        inputs={
            "RANGE": InputInfo(InputType.POSITIVE_INTEGER, old="VALUE"),
            "BODY": InputInfo(InputType.SCRIPT, old="BODY"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
        },
    ),
    "exitLoop": BlockInfo(
        block_type=BlockType.ENDING_STATEMENT,
        new_opcode="escape loop",
    ),
    "continueLoop": BlockInfo(
        block_type=BlockType.ENDING_STATEMENT,
        new_opcode="continue loop",
    ),
    "switch": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="switch (CONDITION) {CASES}",
        inputs={
            "CONDITION": InputInfo(InputType.ROUND, old="CONDITION"),
            "CASES": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "switch_default": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="switch (CONDITION) {CASES} default {DEFAULT}",
        inputs={
            "CONDITION": InputInfo(InputType.ROUND, old="CONDITION"),
            "CASES": InputInfo(InputType.SCRIPT, old="SUBSTACK1"),
            "DEFAULT": InputInfo(InputType.SCRIPT, old="SUBSTACK2"),
        },
    ),
    "exitCase": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="exit case",
    ),
    "case_next": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="run next case when (CONDITION)",
        inputs={
            "CONDITION": InputInfo(InputType.TEXT, old="CONDITION"),
        },
    ),
    "case": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="case (CONDITION) {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.TEXT, old="CONDITION"),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "if": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="if <CONDITION> then {THEN}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
            "THEN": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "if_else": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="if <CONDITION> then {THEN} else {ELSE}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
            "THEN": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
            "ELSE": InputInfo(InputType.SCRIPT, old="SUBSTACK2"),
        },
    ),
    "wait_until": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="wait until <CONDITION>",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
        },
    ),
    "repeat_until": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="repeat until <CONDITION> {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "while": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="while <CONDITION> {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="CONDITION"),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "if_return_else_return": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="if <CONDITION> then (TRUEVALUE) else (FALSEVALUE)",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, old="boolean"),
            "TRUEVALUE": InputInfo(InputType.TEXT, old="TEXT1"),
            "FALSEVALUE": InputInfo(InputType.TEXT, old="TEXT2"),
        },
    ),
    "all_at_once": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="all at once {BODY}",
        inputs={
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "run_as_sprite": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="as ([TARGET]) {BODY}",
        inputs={
            "TARGET": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, old="RUN_AS_OPTION", menu=MenuInfo("control_run_as_sprite_menu", inner="RUN_AS_OPTION")),
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
    ),
    "try_catch": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="try to do {TRY} if a block errors {IFERROR}",
        inputs={
            "TRY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
            "IFERROR": InputInfo(InputType.SCRIPT, old="SUBSTACK2"),
        },
    ),
    "throw_error": BlockInfo(
        block_type=BlockType.ENDING_STATEMENT,
        new_opcode="throw error (ERROR)",
        inputs={
            "ERROR": InputInfo(InputType.TEXT, old="ERROR"),
        },
    ),
    "error": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="error",
    ),
    "backToGreenFlag": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="run flag",
    ),
    "stop_sprite": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="stop sprite ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, old="STOP_OPTION", menu=MenuInfo("control_stop_sprite_menu", inner="STOP_OPTION")),
        },
    ),
    "stop": BlockInfo(
        block_type=BlockType.DYNAMIC,
        new_opcode="stop script [TARGET]",
    ),
    "start_as_clone": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when I start as a clone",
    ),
    "create_clone_of": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="create clone of ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.CLONING_TARGET, old="CLONE_OPTION", menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        },
    ),
    "delete_clones_of": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="delete clones of ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.CLONING_TARGET, old="CLONE_OPTION", menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        },
    ),
    "delete_this_clone": BlockInfo(
        block_type=BlockType.ENDING_STATEMENT,
        new_opcode="delete this clone",
    ),
    "is_clone": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="is clone?",
    ),
})