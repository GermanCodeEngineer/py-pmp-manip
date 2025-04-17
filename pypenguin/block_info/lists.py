from block_info.basis import *

lists = BlockInfoSet(name="lists", opcode_prefix="data", block_infos={
    "addtolist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="add (ITEM) to [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, new="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "deleteoflist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="delete (INDEX) of [LIST]",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
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
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "insertatlist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="insert (ITEM) at (INDEX) of [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, new="ITEM"),
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "replaceitemoflist": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="replace item (INDEX) of [LIST] with (ITEM)",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
            "ITEM": InputInfo(InputType.TEXT, new="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "listforeachitem": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="For each item [VARIABLE] in [LIST] {BODY}",
        inputs={
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "listforeachnum": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="For each item # [VARIABLE] in [LIST] {BODY}",
        inputs={
            "SUBSTACK": InputInfo(InputType.SCRIPT, new="BODY"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "itemoflist": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="item (INDEX) of [LIST]",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "itemnumoflist": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="item # of (ITEM) in [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, new="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "amountinlist": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="amount of (VALUE) of [LIST]",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
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
            "ITEM": InputInfo(InputType.TEXT, new="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "itemexistslist": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="item (INDEX) exists in [LIST] ?",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
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
            "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
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