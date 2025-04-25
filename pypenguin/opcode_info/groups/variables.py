from utility import DualKeyDict

from opcode_info import OpcodeInfoGroup, OpcodeInfo, OpcodeType, InputInfo, InputType, DropdownInfo, DropdownType, MenuInfo

variables = OpcodeInfoGroup(name="variables", opcode_info=DualKeyDict({
    ("data_setvariableto", "set [VARIABLE] to (VALUE)"): OpcodeInfo(
        block_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(InputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
        }),
    ),
    ("data_changevariableby", "change [VARIABLE] by (VALUE)"): OpcodeInfo(
        block_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
        }),
    ),
    ("data_showvariable", "show variable [VARIABLE]"): OpcodeInfo(
        block_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
        }),
    ),
    ("data_hidevariable", "hide variable [VARIABLE]"): OpcodeInfo(
        block_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("VARIABLE", "VARIABLE"): DropdownInfo(DropdownType.VARIABLE),
        }),
    ),
}))