from block_info.basis import *

lists = CategoryOpcodesInfo(name="lists", opcode_prefix="data", block_infos={
    "addtolist": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="add (ITEM) to [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, new="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "deleteoflist": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="delete (INDEX) of [LIST]",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "deletealloflist": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="delete all of [LIST]",
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "shiftlist": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="shift [LIST] by (INDEX)",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "insertatlist": OpcodeInfo(
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
    "replaceitemoflist": OpcodeInfo(
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
    "listforeachitem": OpcodeInfo(
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
    "listforeachnum": OpcodeInfo(
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
    "itemoflist": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="item (INDEX) of [LIST]",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "itemnumoflist": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="item # of (ITEM) in [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, new="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "amountinlist": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="amount of (VALUE) of [LIST]",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "lengthoflist": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="length of [LIST]",
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "listcontainsitem": OpcodeInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="[LIST] contains (ITEM) ?",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, new="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "itemexistslist": OpcodeInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="item (INDEX) exists in [LIST] ?",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, new="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "listisempty": OpcodeInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="is [LIST] empty?",
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "reverselist": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="reverse [LIST]",
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "arraylist": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [LIST] to array (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "listarray": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="get list [LIST] as an array",
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "showlist": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="show list [LIST]",
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
    "hidelist": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="hide list [LIST]",
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, new="LIST"),
        },
    ),
})