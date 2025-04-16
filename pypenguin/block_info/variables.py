from block_info.basis import *

variables = BlockInfoSet(name="variables", opcode_prefix="data", block_infos={
    "setvariableto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [VARIABLE] to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="VALUE"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
        },
    ),
    "changevariableby": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change [VARIABLE] by (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="VALUE"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
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