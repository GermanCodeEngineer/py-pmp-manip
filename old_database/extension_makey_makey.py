opcodes = {
    "makeymakey_whenMakeyKeyPressed": {
        "type": "hat",
        "category": "Makey Makey",
        "newOpcode": "when ([MAKEY_KEY]) key pressed",
        "inputTypes": {"MAKEY_KEY": "makey key"},
        "optionTypes": {},
        "menus": [{"new": "MAKEY_KEY", "outer": "KEY", "inner": "KEY", "menuOpcode": "makeymakey_menu_KEY"}],
    },
    "makeymakey_whenCodePressed": {
        "type": "hat",
        "category": "Makey Makey",
        "newOpcode": "when ([MAKEY_SEQUENCE]) pressed in order",
        "inputTypes": {"MAKEY_SEQUENCE": "makey sequence"},
        "optionTypes": {},
        "menus": [{"new": "MAKEY_SEQUENCE", "outer": "SEQUENCE", "inner": "SEQUENCE", "menuOpcode": "makeymakey_menu_SEQUENCE"}],
    },
    "makeymakey_isMakeyKeyPressed": {
        "type": "booleanReporter",
        "category": "Makey Makey",
        "newOpcode": "is ([MAKEY_KEY]) pressed","inputTypes": {"MAKEY_KEY": "makey key"},
        "optionTypes": {},
        "menus": [{"new": "MAKEY_KEY", "outer": "KEY", "inner": "KEY", "menuOpcode": "makeymakey_menu_KEY"}],
    },
}