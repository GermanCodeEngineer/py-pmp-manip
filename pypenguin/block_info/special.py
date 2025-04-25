from block_info.basis import *

special = CategoryOpcodesInfo(name="special", opcode_prefix="special", block_infos={
    "motion_goto_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#REACHABLE TARGET MENU (GO)",
    ),
    "motion_glideto_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#REACHABLE TARGET MENU (GLIDE)",
    ),
    "motion_pointtowards_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#OBSERVABLE TARGET MENU",
    ),
    "looks_costume": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#COSTUME MENU",
    ),
    "looks_backdrops": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#BACKDROP MENU",
    ),
    "looks_getinput_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#COSTUME PROPERTY MENU",
    ),
    "looks_changeVisibilityOfSprite_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#SHOW/HIDE SPRITE MENU",
    ),
    "looks_getOtherSpriteVisible_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#IS SPRITE VISIBLE MENU",
    ),
    "sound_sounds_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#SOUND MENU",
    ),
    "control_stop_sprite_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#STOP SPRITE MENU",
    ),
    "control_create_clone_of_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#CLONE TARGET MENU",
    ),
    "control_run_as_sprite_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#RUN AS SPRITE MENU",
    ),
    "sensing_touchingobjectmenu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#TOUCHING OBJECT MENU",
    ),
    "sensing_fulltouchingobjectmenu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#FULL TOUCHING OBJECT MENU",
    ),
    "sensing_touchingobjectmenusprites": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#TOUCHING OBJECT MENU SPRITES",
    ),
    "sensing_distancetomenu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#DISTANCE TO MENU",
    ),
    "sensing_keyoptions": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#KEY MENU",
    ),
    "sensing_scrolldirections": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#SCROLL DIRECTION MENU",
    ),
    "sensing_of_object_menu": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#OJBECT PROPERTY MENU",
    ),
    "sensing_fingeroptions": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#FINGER INDEX MENU",
    ),
    "music_menu_DRUM": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#DRUM MENU",
    ),
    "music_menu_INSTRUMENT": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#INSTRUMENT MENU",
    ),
    "pen_menu_FONT": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#PEN FONT MENU",
    ),
    "pen_menu_colorParam": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#PEN PROPERTY MENU",
    ),
    "text_menu_FONT": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#TEXT FONT MENU",
    ),
    "videoSensing_menu_ATTRIBUTE": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#VIDEO SENSING PROPERTY",
    ),
    "videoSensing_menu_SUBJECT": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#VIDEO SENSING TARGET",
    ),
    "videoSensing_menu_VIDEO_STATE": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#VIDEO STATE",
    ),
    "text2speech_menu_voices": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#TEXT TO SPEECH VOICE MENU",
    ),
    "text2speech_menu_languages": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#TEXT TO SPEECH LANGUAGE MENU",
    ),
    "translate_menu_languages": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#TRANSLATE LANGUAGE MENU",
    ),
    "makeymakey_menu_KEY": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#MAKEY KEY MENU",
    ),
    "makeymakey_menu_SEQUENCE": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#MAKEY KEY SEQUENCE MENU",
    ),
    "twFiles_menu_encoding": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#FILE ENCODING MENU",
    ),
    "twFiles_menu_automaticallyOpen": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#FILE SELECTOR MODE MENU",
    ),
    "note": OpcodeInfo(
        block_type=BlockType.MENU,
        new_opcode="#NOTE MENU",
    ),
    "polygon": OpcodeInfo(
        block_type=BlockType.POLYGON_MENU,
        new_opcode="POLYGON MENU",
        inputs={
            "x1": InputInfo(InputType.NUMBER, new="x1"),
            "y1": InputInfo(InputType.NUMBER, new="y1"),
            "x2": InputInfo(InputType.NUMBER, new="x2"),
            "y2": InputInfo(InputType.NUMBER, new="y2"),
            "x3": InputInfo(InputType.NUMBER, new="x3"),
            "y3": InputInfo(InputType.NUMBER, new="y3"),
            "x4": InputInfo(InputType.NUMBER, new="x4"),
            "y4": InputInfo(InputType.NUMBER, new="y4"),
        },
        dropdowns={
            "button": DropdownInfo(DropdownType.EXPANDED_MINIMIZED, new="EXPANDED_MINIMIZED"),
            "VERTEX_COUNT": DropdownInfo(DropdownType.VERTEX_COUNT, new="VERTEX_COUNT"),
        },
    ),
    "variable_value": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="value of [VARIABLE]",
        can_have_monitor="True",
    ),
    "list_value": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="value of [LIST]",
        can_have_monitor="True",
    ),
    "define": OpcodeInfo(
        block_type=BlockType.HAT,
        new_opcode="define custom block",
    ),
    "procedures_call": OpcodeInfo(
        block_type=BlockType.DYNAMIC,
        new_opcode="call custom block",
    ),
    "procedures_return": OpcodeInfo(
        block_type=BlockType.ENDING_STATEMENT,
        new_opcode="return (VALUE)",
        inputs={
            "return": InputInfo(InputType.TEXT, new="VALUE"),
        },
    ),
    "procedures_set": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set (PARAM) to (VALUE)",
        inputs={
            "PARAM": InputInfo(InputType.ROUND, new="PARAM"),
            "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
        },
    ),
    "argument_reporter_string_number": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="value of text [ARGUMENT]",
    ),
    "argument_reporter_boolean": OpcodeInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="value of boolean [ARGUMENT]",
    ),
})