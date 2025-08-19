from pmp_manip.opcode_info.data_imports import *

ext_scratch_text_to_speech = OpcodeInfoGroup(name="scratch_text_to_speech", opcode_info=DualKeyDict({
    ("text2speech_speakAndWait", "speak (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("WORDS", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("text2speech_setVoice", "set voice to ([VOICE])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VOICE", "VOICE"): InputInfo(BuiltinInputType.TEXT_TO_SPEECH_VOICE, menu=MenuInfo("text2speech_menu_voices", inner="voices")),
        }),
    ),

    ("text2speech_setLanguage", "set language to ([LANGUAGE])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("LANGUAGE", "LANGUAGE"): InputInfo(BuiltinInputType.TEXT_TO_SPEECH_LANGUAGE, menu=MenuInfo("text2speech_menu_languages", inner="languages")),
        }),
    ),

    ("text2speech_setSpeed", "set reading speed to (SPEED) %"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SPEED", "SPEED"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

}))