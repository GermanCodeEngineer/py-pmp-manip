from block_info.basis import *

variables = CategoryOpcodesInfo(name="variables", opcode_prefix="data", block_infos={
    "setvariableto": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [VARIABLE] to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
        },
    ),
    "changevariableby": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change [VARIABLE] by (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, new="VALUE"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
        },
    ),
    "showvariable": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="show variable [VARIABLE]",
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
        },
    ),
    "hidevariable": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="hide variable [VARIABLE]",
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
        },
    ),
})