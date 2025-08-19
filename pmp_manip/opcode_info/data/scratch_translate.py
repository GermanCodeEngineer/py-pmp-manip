from pmp_manip.opcode_info.data_imports import *

ext_scratch_translate = OpcodeInfoGroup(name="scratch_translate", opcode_info=DualKeyDict({
    ("translate_getTranslate", "translate (TEXT) to ([LANGUAGE])"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("WORDS", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("LANGUAGE", "LANGUAGE"): InputInfo(BuiltinInputType.TRANSLATE_LANGUAGE, menu=MenuInfo("translate_menu_languages", inner="languages")),
        }),
    ),

    ("translate_getViewerLanguage", "language"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
    ),

}))