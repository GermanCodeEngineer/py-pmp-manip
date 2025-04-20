from block_info.basis import *

control = BlockInfoSet(name="control", opcode_prefix="control", block_infos={
    "wait": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="wait (SECONDS) seconds",
        inputs={
            "DURATION": InputInfo(InputType.POSITIVE_NUMBER, new="SECONDS"),
        },
    ),
    "waitsecondsoruntil": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="wait (SECONDS) seconds or until <CONDITION>",
        inputs={
            "DURATION": InputInfo(InputType.POSITIVE_NUMBER, new="SECONDS"),
            "CONDITION": InputInfo(InputType.BOOLEAN, new="CONDITION"),
        },
    ),
    "repeat": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="repeat (TIMES) {BODY}",
        inputs={
            "TIMES": InputInfo(InputType.NUMBER, new="TIMES"),
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
    ),
    "forever": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="forever {BODY}",
        inputs={
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
    ),
    "for_each": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="for each [VARIABLE] in (RANGE) {BODY}",
        inputs={
            "VALUE": InputInfo(InputType.POSITIVE_INTEGER, new="RANGE"),
            "BODY": InputInfo(InputType.SCRIPT, new="BODY"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
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
            "CONDITION": InputInfo(InputType.ROUND, new="CONDITION"),
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="CASES"),
        },
    ),
    "switch_default": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="switch (CONDITION) {CASES} default {DEFAULT}",
        inputs={
            "CONDITION": InputInfo(InputType.ROUND, new="CONDITION"),
            "SUBSTACK1": InputInfo(InputType.SCRIPT, new="CASES"),
            "SUBSTACK2": InputInfo(InputType.SCRIPT, new="DEFAULT"),
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
            "CONDITION": InputInfo(InputType.TEXT, new="CONDITION"),
        },
    ),
    "case": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="case (CONDITION) {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.TEXT, new="CONDITION"),
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
    ),
    "if": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="if <CONDITION> then {THEN}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, new="CONDITION"),
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="THEN"),
        },
    ),
    "if_else": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="if <CONDITION> then {THEN} else {ELSE}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, new="CONDITION"),
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="THEN"),
            "SUBSTACK2": InputInfo(InputType.SCRIPT, new="ELSE"),
        },
    ),
    "wait_until": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="wait until <CONDITION>",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, new="CONDITION"),
        },
    ),
    "repeat_until": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="repeat until <CONDITION> {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, new="CONDITION"),
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
    ),
    "while": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="while <CONDITION> {BODY}",
        inputs={
            "CONDITION": InputInfo(InputType.BOOLEAN, new="CONDITION"),
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
    ),
    "if_return_else_return": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="if <CONDITION> then (TRUEVALUE) else (FALSEVALUE)",
        inputs={
            "boolean": InputInfo(InputType.BOOLEAN, new="CONDITION"),
            "TEXT1": InputInfo(InputType.TEXT, new="TRUEVALUE"),
            "TEXT2": InputInfo(InputType.TEXT, new="FALSEVALUE"),
        },
    ),
    "all_at_once": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="all at once {BODY}",
        inputs={
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
    ),
    "run_as_sprite": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="as ([TARGET]) {BODY}",
        inputs={
            "RUN_AS_OPTION": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("control_run_as_sprite_menu", inner="RUN_AS_OPTION")),
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
    ),
    "try_catch": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="try to do {TRY} if a block errors {IFERROR}",
        inputs={
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="TRY"),
            "SUBSTACK2": InputInfo(InputType.SCRIPT, new="IFERROR"),
        },
    ),
    "throw_error": BlockInfo(
        block_type=BlockType.ENDING_STATEMENT,
        new_opcode="throw error (ERROR)",
        inputs={
            "ERROR": InputInfo(InputType.TEXT, new="ERROR"),
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
            "STOP_OPTION": InputInfo(InputType.STAGE_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("control_stop_sprite_menu", inner="STOP_OPTION")),
        },
    ),
    "stop": BlockInfo(
        block_type=BlockType.DYNAMIC,
        new_opcode="stop script [TARGET]",
        dropdowns={
            "STOP_OPTION": DropdownInfo(DropdownType.STOP_SCRIPT_TARGET, new="TARGET"),
        },
    ),
    "start_as_clone": BlockInfo(
        block_type=BlockType.HAT,
        new_opcode="when I start as a clone",
    ),
    "create_clone_of": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="create clone of ([TARGET])",
        inputs={
            "CLONE_OPTION": InputInfo(InputType.CLONING_TARGET, new="TARGET", menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
        },
    ),
    "delete_clones_of": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="delete clones of ([TARGET])",
        inputs={
            "CLONE_OPTION": InputInfo(InputType.CLONING_TARGET, new="TARGET", menu=MenuInfo("control_create_clone_of_menu", inner="CLONE_OPTION")),
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