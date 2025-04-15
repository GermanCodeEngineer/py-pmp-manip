from block_info.basis import *

lists = BlockInfoSet(name="lists", opcode_prefix="data", blocks={
    "data_addtolist": BlockInfo(
        block_type="instruction",
        new_opcode="add (ITEM) to [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_deleteoflist": BlockInfo(
        block_type="instruction",
        new_opcode="delete (INDEX) of [LIST]",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_deletealloflist": BlockInfo(
        block_type="instruction",
        new_opcode="delete all of [LIST]",
    ),
    "data_shiftlist": BlockInfo(
        block_type="instruction",
        new_opcode="shift [LIST] by (INDEX)",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_insertatlist": BlockInfo(
        block_type="instruction",
        new_opcode="insert (ITEM) at (INDEX) of [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_replaceitemoflist": BlockInfo(
        block_type="instruction",
        new_opcode="replace item (INDEX) of [LIST] with (ITEM)",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_listforeachitem": BlockInfo(
        block_type="instruction",
        new_opcode="For each item [VARIABLE] in [LIST] {BODY}",
        inputs={
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_listforeachnum": BlockInfo(
        block_type="instruction",
        new_opcode="For each item # [VARIABLE] in [LIST] {BODY}",
        inputs={
            "BODY": InputInfo(InputType.SCRIPT, old="SUBSTACK"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_itemoflist": BlockInfo(
        block_type="stringReporter",
        new_opcode="item (INDEX) of [LIST]",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_itemnumoflist": BlockInfo(
        block_type="stringReporter",
        new_opcode="item # of (ITEM) in [LIST]",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_amountinlist": BlockInfo(
        block_type="stringReporter",
        new_opcode="amount of (VALUE) of [LIST]",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="VALUE"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_lengthoflist": BlockInfo(
        block_type="stringReporter",
        new_opcode="length of [LIST]",
    ),
    "data_listcontainsitem": BlockInfo(
        block_type="booleanReporter",
        new_opcode="[LIST] contains (ITEM) ?",
        inputs={
            "ITEM": InputInfo(InputType.TEXT, old="ITEM"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_itemexistslist": BlockInfo(
        block_type="booleanReporter",
        new_opcode="item (INDEX) exists in [LIST] ?",
        inputs={
            "INDEX": InputInfo(InputType.INTEGER, old="INDEX"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_listisempty": BlockInfo(
        block_type="booleanReporter",
        new_opcode="is [LIST] empty?",
    ),
    "data_reverselist": BlockInfo(
        block_type="instruction",
        new_opcode="reverse [LIST]",
    ),
    "data_arraylist": BlockInfo(
        block_type="instruction",
        new_opcode="set [LIST] to array (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="VALUE"),
        },
        dropdowns={
            "LIST": DropdownInfo(DropdownType.LIST, old="LIST"),
        },
    ),
    "data_listarray": BlockInfo(
        block_type="stringReporter",
        new_opcode="get list [LIST] as an array",
    ),
    "data_showlist": BlockInfo(
        block_type="instruction",
        new_opcode="show list [LIST]",
    ),
    "data_hidelist": BlockInfo(
        block_type="instruction",
        new_opcode="hide list [LIST]",
    ),
})