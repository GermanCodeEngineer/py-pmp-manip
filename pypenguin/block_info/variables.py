from block_info.basis import *

variables = BlockInfoSet(name="variables", opcode_prefix="data", block_infos={
    "setvariableto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [VARIABLE] to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
        },
    ),
    "changevariableby": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change [VARIABLE] by (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, new="VALUE"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, new="VARIABLE"),
        },
    ),
    "showvariable": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="show variable [VARIABLE]",
    ),
    "hidevariable": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="hide variable [VARIABLE]",
    ),
})