from pmp_manip.opcode_info.data_imports import *

ext_scratch_text = OpcodeInfoGroup(name="scratch_text", opcode_info=DualKeyDict({
    ("text_setText", "show text (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEXT", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("text_animateText", "[ANIMATION_TECHNIQUE] text (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEXT", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("ANIMATE", "ANIMATION_TECHNIQUE"): DropdownInfo(BuiltinDropdownType.ANIMATION_TECHNIQUE),
        }),
    ),

    ("text_clearText", "show sprite"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("text_setFont", "set font to ([FONT])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("FONT", "FONT"): InputInfo(BuiltinInputType.FONT, menu=MenuInfo("text_menu_FONT", inner="FONT")),
        }),
    ),

    ("text_setColor", "set text color to (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
        }),
    ),

    ("text_setWidth", "set width to (WIDTH) aligned [ALIGN]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("WIDTH", "WIDTH"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("ALIGN", "ALIGN"): DropdownInfo(BuiltinDropdownType.LEFT_CENTER_RIGHT),
        }),
    ),

    ("text_rainbow", "rainbow for (SECONDS) seconds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SECS", "SECONDS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("text_addLine", "add line (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEXT", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("text_setOutlineWidth", "set outline width to (WIDTH)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("WIDTH", "WIDTH"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("text_setOutlineColor", "set outline color to (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
        }),
    ),

    ("text_getVisible", "is text visible?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        can_have_monitor=True,
    ),

    ("text_getWidth", "get width of the text"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
    ),

    ("text_getHeight", "get height of the text"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
    ),

    ("text_getDisplayedText", "displayed text"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
    ),

    ("text_getRender", "get data uri of last rendered text"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor=True,
    ),

}))