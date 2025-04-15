opcodes = {
    "videoSensing_whenMotionGreaterThan": {
        "type": "hat",
        "category": "Video Sensing",
        "newOpcode": "when video motion > (THRESHOLD)",
        "inputTypes": {"THRESHOLD": "number"},
        "inputTranslation": {"REFERENCE": "THRESHOLD"},
        "optionTypes": {},
    },
    "videoSensing_videoOn": {
        "type": "stringReporter",
        "category": "Video Sensing",
        "newOpcode": "video ([PROPERTY]) on ([TARGET])",
        "inputTypes": {"PROPERTY": "video sensing property", "TARGET": "video sensing target"},
        "optionTypes": {},
        "menus": [
            {"new": "PROPERTY", "outer": "ATTRIBUTE", "inner": "ATTRIBUTE", "menuOpcode": "videoSensing_menu_ATTRIBUTE"},
            {"new": "TARGET"  , "outer": "SUBJECT"  , "inner": "SUBJECT"  , "menuOpcode": "videoSensing_menu_SUBJECT"  },
        ],
    },
    "videoSensing_videoToggle": {
        "type": "instruction",
        "category": "Video Sensing",
        "newOpcode": "turn video ([VIDEO_STATE])",
        "inputTypes": {"VIDEO_STATE": "video state"},
        "optionTypes": {},
        "menus": [{"new": "VIDEO_STATE", "outer": "VIDEO_STATE", "inner": "VIDEO_STATE", "menuOpcode": "videoSensing_menu_VIDEO_STATE"}],
    },
    "videoSensing_setVideoTransparency": {
        "type": "instruction",
        "category": "Video Sensing",
        "newOpcode": "set video transparency to (TRANSPARENCY)",
        "inputTypes": {"TRANSPARENCY": "number"},
        "optionTypes": {},
    },
}