from pmp_manip.opcode_info.data_imports import *

link_bitwise = OpcodeInfoGroup(name="link_bitwise", opcode_info=DualKeyDict({
    ("Bitwise_isNumberBits", "is (NUM) binary?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("CENTRAL", "NUM"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_toNumberBits", "(NUM) to binary"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("CENTRAL", "NUM"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_ofNumberBits", "(NUM) to number"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("CENTRAL", "NUM"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseRightShift", "(NUM) >> (BITS)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LEFT", "NUM"): InputInfo(BuiltinInputType.NUMBER),
            ("RIGHT", "BITS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseLeftShift", "(NUM) << (BITS)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LEFT", "NUM"): InputInfo(BuiltinInputType.NUMBER),
            ("RIGHT", "BITS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseLogicalRightShift", "(NUM) >>> (BITS)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LEFT", "NUM"): InputInfo(BuiltinInputType.NUMBER),
            ("RIGHT", "BITS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseCircularRightShift", "(NUM) >> circular (BITS)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LEFT", "NUM"): InputInfo(BuiltinInputType.NUMBER),
            ("RIGHT", "BITS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseCircularLeftShift", "(NUM) << circular (BITS)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LEFT", "NUM"): InputInfo(BuiltinInputType.NUMBER),
            ("RIGHT", "BITS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseAnd", "(OPERAND1) and (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LEFT", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("RIGHT", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseOr", "(OPERAND1) or (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LEFT", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("RIGHT", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseXor", "(OPERAND1) xor (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LEFT", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("RIGHT", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("Bitwise_bitwiseNot", "not (NUM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("CENTRAL", "NUM"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

}))