from block_info.basis import *

lists = BlockInfoSet(name="lists", opcode_prefix="data", block_infos={
    "addtolist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="add (ITEM) to [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "deleteoflist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="delete (INDEX) of [LIST]",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "deletealloflist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="delete all of [LIST]",
    ),
    "shiftlist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="shift [LIST] by (INDEX)",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "insertatlist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="insert (ITEM) at (INDEX) of [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "replaceitemoflist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="replace item (INDEX) of [LIST] with (ITEM)",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "listforeachitem": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="For each item [VARIABLE] in [LIST] {BODY}",
        inputs={
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "listforeachnum": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="For each item # [VARIABLE] in [LIST] {BODY}",
        inputs={
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "itemoflist": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="item (INDEX) of [LIST]",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "itemnumoflist": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="item # of (ITEM) in [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "amountinlist": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="amount of (VALUE) of [LIST]",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="VALUE"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "lengthoflist": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="length of [LIST]",
    ),
    "listcontainsitem": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="[LIST] contains (ITEM) ?",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "itemexistslist": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="item (INDEX) exists in [LIST] ?",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "listisempty": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="is [LIST] empty?",
    ),
    "reverselist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="reverse [LIST]",
    ),
    "arraylist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [LIST] to array (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="VALUE"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "listarray": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="get list [LIST] as an array",
    ),
    "showlist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="show list [LIST]",
    ),
    "hidelist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="hide list [LIST]",
    ),
})