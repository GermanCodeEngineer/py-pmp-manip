from pmp_manip.opcode_info.data_imports import *

ext_scratch_makey_makey = OpcodeInfoGroup(name="scratch_makey_makey", opcode_info=DualKeyDict({
    ("makeymakey_whenMakeyKeyPressed", "when ([MAKEY_KEY]) key pressed"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        inputs=DualKeyDict({
            ("KEY", "MAKEY_KEY"): InputInfo(BuiltinInputType.MAKEY_KEY, menu=MenuInfo("makeymakey_menu_KEY", inner="KEY")),
        }),
    ),

    ("makeymakey_whenCodePressed", "when ([MAKEY_SEQUENCE]) pressed in order"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        inputs=DualKeyDict({
            ("SEQUENCE", "MAKEY_SEQUENCE"): InputInfo(BuiltinInputType.MAKEY_SEQUENCE, menu=MenuInfo("makeymakey_menu_SEQUENCE", inner="SEQUENCE")),
        }),
    ),

    ("makeymakey_isMakeyKeyPressed", "is ([MAKEY_KEY]) pressed"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("KEY", "MAKEY_KEY"): InputInfo(BuiltinInputType.MAKEY_KEY, menu=MenuInfo("makeymakey_menu_KEY", inner="KEY")),
        }),
    ),

}))