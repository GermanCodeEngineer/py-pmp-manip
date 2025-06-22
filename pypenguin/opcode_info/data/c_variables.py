from pypenguin.opcode_info.data_imports import *

c_variables = OpcodeInfoGroup(name="c_variables", opcode_info=DualKeyDict({
    ("data_setvariableto", "set [VARIABLE] to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(InputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
        }),
    ),

    ("data_changevariableby", "change [VARIABLE] by (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
        }),
    ),

    ("data_showvariable", "show variable [VARIABLE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
        }),
    ),

    ("data_hidevariable", "hide variable [VARIABLE]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
        }),
    ),

}))