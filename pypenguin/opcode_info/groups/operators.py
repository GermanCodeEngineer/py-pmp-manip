from pypenguin.utility import DualKeyDict

from pypenguin.opcode_info import OpcodeInfoGroup, OpcodeInfo, OpcodeType, InputInfo, InputType, DropdownInfo, DropdownType, MenuInfo

operators = OpcodeInfoGroup(name="operators", opcode_info=DualKeyDict({
    ("operator_add", "(OPERAND1) + (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_subtract", "(OPERAND1) - (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_multiply", "(OPERAND1) * (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_divide", "(OPERAND1) / (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_power", "(OPERAND1) ^ (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("NUM2", "OPERAND2"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_advMathExpanded", "(OPERAND1) * (OPERAND2) [OPERATION] (OPERAND3)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("TWO", "OPERAND2"): InputInfo(InputType.NUMBER),
            ("THREE", "OPERAND3"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "OPERATION"): DropdownInfo(DropdownType.ROOT_LOG),
        }),
    ),
    ("operator_advMath", "(OPERAND1) [OPERATION] (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("TWO", "OPERAND2"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "OPERATION"): DropdownInfo(DropdownType.POWER_ROOT_LOG),
        }),
    ),
    ("operator_random", "pick random (OPERAND1) to (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("FROM", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("TO", "OPERAND2"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_constrainnumber", "constrain (NUM) min (MIN) max (MAX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("inp", "NUM"): InputInfo(InputType.NUMBER),
            ("min", "MIN"): InputInfo(InputType.NUMBER),
            ("max", "MAX"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_lerpFunc", "interpolate (OPERAND1) to (OPERAND2) by (WEIGHT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "OPERAND1"): InputInfo(InputType.NUMBER),
            ("TWO", "OPERAND2"): InputInfo(InputType.NUMBER),
            ("AMOUNT", "WEIGHT"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_gt", "(OPERAND1) > (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(InputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_gtorequal", "(OPERAND1) >= (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(InputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_lt", "(OPERAND1) < (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(InputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_ltorequal", "(OPERAND1) <= (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(InputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_equals", "(OPERAND1) = (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(InputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_notequal", "(OPERAND1) != (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(InputType.TEXT),
            ("OPERAND2", "OPERAND2"): InputInfo(InputType.TEXT),
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
            ("OPERAND1", "OPERAND1"): InputInfo(InputType.BOOLEAN),
            ("OPERAND2", "OPERAND2"): InputInfo(InputType.BOOLEAN),
        }),
    ),
    ("operator_or", "<OPERAND1> or <OPERAND2>"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND1", "OPERAND1"): InputInfo(InputType.BOOLEAN),
            ("OPERAND2", "OPERAND2"): InputInfo(InputType.BOOLEAN),
        }),
    ),
    ("operator_not", "not <OPERAND>"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("OPERAND", "OPERAND"): InputInfo(InputType.BOOLEAN),
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
            ("STRING1", "STRING1"): InputInfo(InputType.TEXT),
            ("STRING2", "STRING2"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_join3", "join (STRING1) (STRING2) (STRING3)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("STRING1", "STRING1"): InputInfo(InputType.TEXT),
            ("STRING2", "STRING2"): InputInfo(InputType.TEXT),
            ("STRING3", "STRING3"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_indexOfTextInText", "index of (SUBSTRING) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "SUBSTRING"): InputInfo(InputType.TEXT),
            ("TEXT2", "TEXT"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_lastIndexOfTextInText", "last index of (SUBSTRING) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "SUBSTRING"): InputInfo(InputType.TEXT),
            ("TEXT2", "TEXT"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_letter_of", "letter (LETTER) of (STRING)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("LETTER", "LETTER"): InputInfo(InputType.POSITIVE_INTEGER),
            ("STRING", "STRING"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_getLettersFromIndexToIndexInText", "letters from (START) to (STOP) in (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("INDEX1", "START"): InputInfo(InputType.POSITIVE_INTEGER),
            ("INDEX2", "STOP"): InputInfo(InputType.TEXT),
            ("TEXT", "TEXT"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_length", "length of (TEXT)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("STRING", "TEXT"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_contains", "(TEXT) contains (SUBSTRING) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("STRING1", "TEXT"): InputInfo(InputType.TEXT),
            ("STRING2", "SUBSTRING"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_textStartsOrEndsWith", "(TEXT) [OPERATION] with (SUBSTRING) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("TEXT1", "TEXT"): InputInfo(InputType.TEXT),
            ("TEXT2", "SUBSTRING"): InputInfo(InputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "OPERATION"): DropdownInfo(DropdownType.TEXT_METHOD),
        }),
    ),
    ("operator_replaceAll", "in (TEXT) replace all (OLDVALUE) with (NEWVALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(InputType.TEXT),
            ("term", "OLDVALUE"): InputInfo(InputType.TEXT),
            ("res", "NEWVALUE"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_replaceFirst", "in (TEXT) replace first (OLDVALUE) with (NEWVALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(InputType.TEXT),
            ("term", "OLDVALUE"): InputInfo(InputType.TEXT),
            ("res", "NEWVALUE"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_regexmatch", "match (TEXT) with regex (REGEX) (MODIFIER)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(InputType.TEXT),
            ("reg", "REGEX"): InputInfo(InputType.TEXT),
            ("regrule", "MODIFIER"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_toUpperLowerCase", "(TEXT) to [CASE]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("TEXT", "TEXT"): InputInfo(InputType.TEXT),
        }),
        dropdowns=DualKeyDict({
            ("OPTION", "CASE"): DropdownInfo(DropdownType.TEXT_CASE),
        }),
    ),
    ("operator_mod", "(OPERAND1) mod (OPERAND2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM1", "OPERAND1"): InputInfo(InputType.TEXT),
            ("NUM2", "OPERAND2"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_round", "round (NUM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM", "NUM"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("operator_mathop", "[OPERATION] of (NUM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("NUM", "NUM"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("OPERATOR", "OPERATION"): DropdownInfo(DropdownType.UNARY_MATH_OPERATION),
        }),
    ),
    ("operator_stringify", "(VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "VALUE"): InputInfo(InputType.TEXT),
        }),
    ),
    ("operator_boolify", "(VALUE) as a boolean"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("ONE", "VALUE"): InputInfo(InputType.TEXT),
        }),
    ),
}))