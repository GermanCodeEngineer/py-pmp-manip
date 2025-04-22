opcodes = {
    "translate_getTranslate": {
        "type": "stringReporter",
        "category": "Translate",
        "newOpcode": "translate (TEXT) to ([LANGUAGE])",
        "inputTypes": {"TEXT": "text", "LANGUAGE": "translate language"},
        "inputTranslation": {"WORDS": "TEXT"},
        "optionTypes": {},
        "menus": [{"new": "LANGUAGE", "outer": "LANGUAGE", "inner": "languages", "menuOpcode": "translate_menu_languages"}]
    },
    "translate_getViewerLanguage": {
        "type": "stringReporter",
        "category": "Translate",
        "newOpcode": "language",
        "inputTypes": {},
        "optionTypes": {},
        "canHaveMonitor": True,
    },
}