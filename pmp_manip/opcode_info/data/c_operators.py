from pmp_manip.opcode_info.data_imports import *

c_operators = OpcodeInfoGroup(name="c_operators", opcode_info=DualKeyDict({
    ("operator_add", "&operators::(OPERAND1) + (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_subtract", "&operators::(OPERAND1) - (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_multiply", "&operators::(OPERAND1) * (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_divide", "&operators::(OPERAND1) / (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_power", "&operators::(OPERAND1) ^ (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_advMathExpanded", "&operators::(OPERAND1) * (OPERAND2) [OPERATION] (OPERAND3)"): OpcodeInfo(
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

    ("operator_advMath", "&operators::(OPERAND1) [OPERATION] (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("TWO", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "OPERATION"): DropdownInfo(BuiltinDropdownType.POWER_ROOT_LOG),
        }),
    ),

    ("operator_random", "&operators::pick random (OPERAND1) to (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("FROM", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("TO", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_constrainnumber", "&operators::constrain (NUM) min (MIN) max (MAX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("inp", "NUM"): InputInfo(BuiltinInputType.NUMBER),
            ("min", "MIN"): InputInfo(BuiltinInputType.NUMBER),
            ("max", "MAX"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_lerpFunc", "&operators::interpolate (OPERAND1) to (OPERAND2) by (WEIGHT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "OPERAND1"): InputInfo(BuiltinInputType.NUMBER),
            ("TWO", "OPERAND2"): InputInfo(BuiltinInputType.NUMBER),
            ("AMOUNT", "WEIGHT"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_gt", "&operators::(OPERAND1) > (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_gtorequal", "&operators::(OPERAND1) >= (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_lt", "&operators::(OPERAND1) < (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_ltorequal", "&operators::(OPERAND1) <= (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_equals", "&operators::(OPERAND1) = (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_notequal", "&operators::(OPERAND1) != (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_trueBoolean", "&operators::true"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
    ),

    ("operator_falseBoolean", "&operators::false"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
    ),

    ("operator_and", "&operators::<OPERAND1> and <OPERAND2>"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.BOOLEAN),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("operator_or", "&operators::<OPERAND1> or <OPERAND2>"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(BuiltinInputType.BOOLEAN),
            ("OPERAND2", "OPERAND2"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("operator_not", "&operators::not <OPERAND>"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND", "OPERAND"): InputInfo(BuiltinInputType.BOOLEAN),
        }),
    ),

    ("operator_newLine", "&operators::new line"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
    ),

    ("operator_tabCharacter", "&operators::tab character"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
    ),

    ("operator_join", "&operators::join (STRING1) (STRING2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("STRING1", "STRING1"): InputInfo(BuiltinInputType.TEXT),
            ("STRING2", "STRING2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_join3", "&operators::join (STRING1) (STRING2) (STRING3)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("STRING1", "STRING1"): InputInfo(BuiltinInputType.TEXT),
            ("STRING2", "STRING2"): InputInfo(BuiltinInputType.TEXT),
            ("STRING3", "STRING3"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_indexOfTextInText", "&operators::index of (SUBSTRING) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "SUBSTRING"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT2", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_lastIndexOfTextInText", "&operators::last index of (SUBSTRING) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "SUBSTRING"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT2", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_letter_of", "&operators::letter (LETTER) of (STRING)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LETTER", "LETTER"): InputInfo(BuiltinInputType.POSITIVE_INTEGER),
            ("STRING", "STRING"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_getLettersFromIndexToIndexInText", "&operators::letters from (START) to (STOP) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("INDEX1", "START"): InputInfo(BuiltinInputType.POSITIVE_INTEGER),
            ("INDEX2", "STOP"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_length", "&operators::length of (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("STRING", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_contains", "&operators::(TEXT) contains (SUBSTRING) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("STRING1", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("STRING2", "SUBSTRING"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_textStartsOrEndsWith", "&operators::(TEXT) [OPERATION] with (SUBSTRING) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("TEXT2", "SUBSTRING"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "OPERATION"): DropdownInfo(BuiltinDropdownType.TEXT_METHOD),
        }),
    ),

    ("operator_replaceAll", "&operators::in (TEXT) replace all (OLDVALUE) with (NEWVALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("term", "OLDVALUE"): InputInfo(BuiltinInputType.TEXT),
            ("res", "NEWVALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_replaceFirst", "&operators::in (TEXT) replace first (OLDVALUE) with (NEWVALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("term", "OLDVALUE"): InputInfo(BuiltinInputType.TEXT),
            ("res", "NEWVALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_regexmatch", "&operators::match (TEXT) with regex (REGEX) (MODIFIER)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("reg", "REGEX"): InputInfo(BuiltinInputType.TEXT),
            ("regrule", "MODIFIER"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_toUpperLowerCase", "&operators::(TEXT) to [CASE]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT", "TEXT"): InputInfo(BuiltinInputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "CASE"): DropdownInfo(BuiltinDropdownType.TEXT_CASE),
        }),
    ),

    ("operator_mod", "&operators::(OPERAND1) mod (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(BuiltinInputType.TEXT),
            ("NUM2", "OPERAND2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_round", "&operators::round (NUM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM", "NUM"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("operator_mathop", "&operators::[OPERATION] of (NUM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM", "NUM"): InputInfo(BuiltinInputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("OPERATOR", "OPERATION"): DropdownInfo(BuiltinDropdownType.UNARY_MATH_OPERATION),
        }),
    ),

    ("operator_stringify", "&operators::(VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("operator_boolify", "&operators::(VALUE) as a boolean"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

}))