from pmp_manip.opcode_info.data_imports import *

c_variables = OpcodeInfoGroup(name="c_variables", opcode_info=DualKeyDict({
    ("data_setvariableto", "&variables::set [VARIABLE] to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
        }),
    ),

    ("data_changevariableby", "&variables::change [VARIABLE] by (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
        }),
    ),

    ("data_showvariable", "&variables::show variable [VARIABLE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
        }),
    ),

    ("data_hidevariable", "&variables::hide variable [VARIABLE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(BuiltinDropdownType.VARIABLE),
        }),
    ),

}))