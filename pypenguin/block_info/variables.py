from block_info.basis import *

variables = BlockInfoSet(name="variables", opcode_prefix="data", blocks={
    "data_setvariableto": BlockInfo(
        block_type="instruction",
        new_opcode="set [VARIABLE] to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="VALUE"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
        },
    ),
    "data_changevariableby": BlockInfo(
        block_type="instruction",
        new_opcode="change [VARIABLE] by (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="VALUE"),
        },
        dropdowns={
            "VARIABLE": DropdownInfo(DropdownType.VARIABLE, old="VARIABLE"),
        },
    ),
    "data_showvariable": BlockInfo(
        block_type="instruction",
        new_opcode="show variable [VARIABLE]",
    ),
    "data_hidevariable": BlockInfo(
        block_type="instruction",
        new_opcode="hide variable [VARIABLE]",
    ),
})