from pmp_manip.opcode_info.data_imports import *

c_lists = OpcodeInfoGroup(name="c_lists", opcode_info=DualKeyDict({
    ("data_addtolist", "&lists::add (ITEM) to [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("ITEM", "ITEM"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_deleteoflist", "&lists::delete (INDEX) of [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("INDEX", "INDEX"): InputInfo(BuiltinInputType.INTEGER),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_deletealloflist", "&lists::delete all of [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_shiftlist", "&lists::shift [LIST] by (INDEX)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("INDEX", "INDEX"): InputInfo(BuiltinInputType.INTEGER),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_insertatlist", "&lists::insert (ITEM) at (INDEX) of [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("ITEM", "ITEM"): InputInfo(BuiltinInputType.TEXT),
            ("INDEX", "INDEX"): InputInfo(BuiltinInputType.INTEGER),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_replaceitemoflist", "&lists::replace item (INDEX) of [LIST] with (ITEM)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("INDEX", "INDEX"): InputInfo(BuiltinInputType.INTEGER),
            ("ITEM", "ITEM"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_listforeachitem", "&lists::For each item [VARIABLE] in [LIST] {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_listforeachnum", "&lists::For each item # [VARIABLE] in [LIST] {BODY}}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SUBSTACK", "BODY"): InputInfo(BuiltinInputType.SCRIPT),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_itemoflist", "&lists::item (INDEX) of [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("INDEX", "INDEX"): InputInfo(BuiltinInputType.INTEGER),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_itemnumoflist", "&lists::item # of (ITEM) in [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ITEM", "ITEM"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_amountinlist", "&lists::amount of (VALUE) of [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_lengthoflist", "&lists::length of [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_listcontainsitem", "&lists::[LIST] contains (ITEM) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("ITEM", "ITEM"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_itemexistslist", "&lists::item (INDEX) exists in [LIST] ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("INDEX", "INDEX"): InputInfo(BuiltinInputType.INTEGER),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_listisempty", "&lists::is [LIST] empty?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_reverselist", "&lists::reverse [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_filterlist", "&lists::filter [LIST] by (INDEX) (ITEM) <KEEP>"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("INDEX", "INDEX"): InputInfo(BuiltinInputType.FILTER_LIST_INDEX),
            ("ITEM" , "ITEM"): InputInfo(BuiltinInputType.FILTER_LIST_ITEM),
            ("BOOL" , "KEEP"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_arraylist", "&lists::set [LIST] to array (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_listarray", "&lists::get list [LIST] as an array"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_showlist", "&lists::show list [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

    ("data_hidelist", "&lists::hide list [LIST]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("LIST", "LIST"): DropdownInfo(BuiltinDropdownType.LIST),
        }),
    ),

}))