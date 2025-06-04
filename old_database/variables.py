opcodes = {
    "data_setvariableto": {
        "type": "instruction",
        "category": "Variables",
        "newOpcode": "set [VARIABLE] to (VALUE)",
        "inputTypes": {"VALUE": "text"},
        "optionTypes": {"VARIABLE": "variable"},
    },
    "data_changevariableby": {
        "type": "instruction",
        "category": "Variables",
        "newOpcode": "change [VARIABLE] by (VALUE)",
        "inputTypes": {"VALUE": "number"},
        "optionTypes": {"VARIABLE": "variable"},
    },
    "data_showvariable": {
        "type": "instruction",
        "category": "Variables",
        "newOpcode": "show variable [VARIABLE]",
        "inputTypes": {},
        "optionTypes": {"VARIABLE": "variable"},
    },
    "data_hidevariable": {
        "type": "instruction",
        "category": "Variables",
        "newOpcode": "hide variable [VARIABLE]",
        "inputTypes": {},
        "optionTypes": {"VARIABLE": "variable"},
    },
}