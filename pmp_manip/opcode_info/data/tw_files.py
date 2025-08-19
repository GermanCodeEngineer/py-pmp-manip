from pmp_manip.opcode_info.data_imports import *

ext_tw_files = OpcodeInfoGroup(name="tw_files", opcode_info=DualKeyDict({
    ("twFiles_showPickerAs", "open a file as ([MODE])"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("as", "MODE"): InputInfo(BuiltinInputType.READ_FILE_MODE, menu=MenuInfo("twFiles_menu_encoding", inner="encoding")),
        }),
    ),

    ("twFiles_showPickerExtensionsAs", "open a (EXTENSION) file as ([MODE])"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("extension", "EXTENSION"): InputInfo(BuiltinInputType.TEXT),
            ("as", "MODE"): InputInfo(BuiltinInputType.READ_FILE_MODE, menu=MenuInfo("twFiles_menu_encoding", inner="encoding")),
        }),
    ),

    ("twFiles_download", "download ([MODE]) (TEXT) as (FILE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("encoding", "MODE"): InputInfo(BuiltinInputType.READ_FILE_MODE, menu=MenuInfo("twFiles_menu_encoding", inner="encoding")),
            ("text", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("file", "FILE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("twFiles_setOpenMode", "set open file selector mode to ([MODE])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("mode", "MODE"): InputInfo(BuiltinInputType.FILE_SELECTOR_MODE, menu=MenuInfo("twFiles_menu_automaticallyOpen", inner="automaticallyOpen")),
        }),
    ),

    ("twFiles_getFileName", "last opened file name"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

}))