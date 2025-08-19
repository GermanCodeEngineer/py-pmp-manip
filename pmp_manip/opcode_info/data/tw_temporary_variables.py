from pmp_manip.opcode_info.data_imports import *

ext_tw_temporary_variables = OpcodeInfoGroup(name="tw_temporary_variables", opcode_info=DualKeyDict({
    ("lmsTempVars2_setThreadVariable", "set thread var (VARIABLE) to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
            ("STRING", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_changeThreadVariable", "change thread var (VARIABLE) by (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
            ("NUM", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_getThreadVariable", "thread var (VARIABLE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_threadVariableExists", "thread var (VARIABLE) exists?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_forEachThreadVariable", "for (VARIABLE) in (COUNT) {BODY}"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
            ("NUM", "COUNT"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("lmsTempVars2_listThreadVariables", "active thread variables"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
    ),

    ("lmsTempVars2_setRuntimeVariable", "set runtime var (VARIABLE) to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
            ("STRING", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_changeRuntimeVariable", "change runtime var (VARIABLE) by (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
            ("NUM", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_getRuntimeVariable", "runtime var (VARIABLE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_runtimeVariableExists", "runtime var (VARIABLE) exists?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_deleteRuntimeVariable", "delete runtime var (VARIABLE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VAR", "VARIABLE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("lmsTempVars2_deleteAllRuntimeVariables", "delete all runtime variables"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("lmsTempVars2_listRuntimeVariables", "active runtime variables"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
    ),

}))