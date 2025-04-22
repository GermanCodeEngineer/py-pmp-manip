opcodes = {
    "text2speech_speakAndWait": {
        "type": "instruction",
        "category": "Text to Speech",
        "newOpcode": "speak (TEXT)",
        "inputTypes": {"TEXT": "text"},
        "inputTranslation": {"WORDS": "TEXT"},
        "optionTypes": {},
    },
    "text2speech_setVoice": {
        "type": "instruction",
        "category": "Text to Speech",
        "newOpcode": "set voice to ([VOICE])",
        "inputTypes": {"VOICE": "text to speech voice"},
        "optionTypes": {},
        "menus": [{"new": "VOICE", "outer": "VOICE", "inner": "voices", "menuOpcode": "text2speech_menu_voices"}],
    },
    "text2speech_setLanguage": {
        "type": "instruction",
        "category": "Text to Speech",
        "newOpcode": "set language to ([LANGUAGE])",
        "inputTypes": {"LANGUAGE": "text to speech language"},
        "optionTypes": {},
        "menus": [{"new": "LANGUAGE", "outer": "LANGUAGE", "inner": "languages", "menuOpcode": "text2speech_menu_languages"}],
    },
    "text2speech_setSpeed": {
        "type": "instruction",
        "category": "Text to Speech",
        "newOpcode": "set reading speed to (SPEED) %",
        "inputTypes": {"SPEED": "number"},
        "optionTypes": {},
    },
}