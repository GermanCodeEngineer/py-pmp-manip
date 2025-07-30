from pmp_manip.opcode_info.data_imports import *

c_operators = OpcodeInfoGroup(name="c_operators", opcode_info=DualKeyDict({
    ("operator_add", "(OPERAND1) + (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_subtract", "(OPERAND1) - (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_multiply", "(OPERAND1) * (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_divide", "(OPERAND1) / (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_power", "(OPERAND1) ^ (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_advMathExpanded", "(OPERAND1) * (OPERAND2) [OPERATION] (OPERAND3)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("TWO", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
            ("THREE", "OPERAND3"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "OPERATION"): DropdownInfo(BuiltinDropdownType.ROOT_LOG),
        }),
    ),

    ("operator_advMath", "(OPERAND1) [OPERATION] (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("TWO", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "OPERATION"): DropdownInfo(BuiltinDropdownType.POWER_ROOT_LOG),
        }),
    ),

    ("operator_random", "pick random (OPERAND1) to (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("FROM", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("TO", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_constrainnumber", "constrain (NUM) min (MIN) max (MAX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("inp", "NUM"): InputInfo(BuiltinInputType.NUMBER),
            ("min", "MIN"): InputInfo(BuiltinInputType.NUMBER),
            ("max", "MAX"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_lerpFunc", "interpolate (OPERAND1) to (OPERAND2) by (WEIGHT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("TWO", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
            ("AMOUNT", "WEIGHT"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_gt", "(OPERAND1) > (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_gtorequal", "(OPERAND1) >= (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_lt", "(OPERAND1) < (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_ltorequal", "(OPERAND1) <= (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_equals", "(OPERAND1) = (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_notequal", "(OPERAND1) != (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_trueBoolean", "true"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
    ),

    ("operator_falseBoolean", "false"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
    ),

    ("operator_and", "<OPERAND1> and <OPERAND2>"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.BOOLEAN),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("operator_or", "<OPERAND1> or <OPERAND2>"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.BOOLEAN),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("operator_not", "not <OPERAND>"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND", "OPERAND"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("operator_newLine", "new line"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
    ),

    ("operator_tabCharacter", "tab character"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
    ),

    ("operator_join", "join (STRING1) (STRING2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("STRING1", "STRING1"): InputInfo(BuiltinInputType.TEXT),
            ("STRING2", "STRING2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_join3", "join (STRING1) (STRING2) (STRING3)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("STRING1", "STRING1"): InputInfo(BuiltinInputType.TEXT),
            ("STRING2", "STRING2"): InputInfo(BuiltinInputType.TEXT),
            ("STRING3", "STRING3"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_indexOfTextInText", "index of (SUBSTRING) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "SUBSTRING"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT2", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_lastIndexOfTextInText", "last index of (SUBSTRING) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "SUBSTRING"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT2", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_letter_of", "letter (LETTER) of (STRING)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LETTER", "LETTER"): InputInfo(BuiltinInputType.POSITIVE_INTEGER),
            ("STRING", "STRING"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_getLettersFromIndexToIndexInText", "letters from (START) to (STOP) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("INDEX1", "START"): InputInfo(BuiltinInputType.POSITIVE_INTEGER),
            ("INDEX2", "STOP"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_length", "length of (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("STRING", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_contains", "(TEXT) contains (SUBSTRING) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("STRING1", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("STRING2", "SUBSTRING"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_textStartsOrEndsWith", "(TEXT) [OPERATION] with (SUBSTRING) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT2", "SUBSTRING"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "OPERATION"): DropdownInfo(BuiltinDropdownType.TEXT_METHOD),
        }),
    ),

    ("operator_replaceAll", "in (TEXT) replace all (OLDVALUE) with (NEWVALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("term", "OLDVALUE"): InputInfo(BuiltinInputType.TEXT),
            ("res", "NEWVALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_replaceFirst", "in (TEXT) replace first (OLDVALUE) with (NEWVALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("term", "OLDVALUE"): InputInfo(BuiltinInputType.TEXT),
            ("res", "NEWVALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_regexmatch", "match (TEXT) with regex (REGEX) (MODIFIER)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("reg", "REGEX"): InputInfo(BuiltinInputType.TEXT),
            ("regrule", "MODIFIER"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_toUpperLowerCase", "(TEXT) to [CASE]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "CASE"): DropdownInfo(BuiltinDropdownType.TEXT_CASE),
        }),
    ),

    ("operator_mod", "(OPERAND1) mod (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_round", "round (NUM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM", "NUM"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_mathop", "[OPERATION] of (NUM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM", "NUM"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("OPERATOR", "OPERATION"): DropdownInfo(BuiltinDropdownType.UNARY_MATH_OPERATION),
        }),
    ),

    ("operator_stringify", "(VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_boolify", "(VALUE) as a boolean"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

}))