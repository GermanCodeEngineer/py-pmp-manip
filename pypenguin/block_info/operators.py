from block_info.basis import *

operators = BlockInfoSet(name="operators", opcode_prefix="operator", blocks={
    "operator_add": BlockInfo(
        block_type="stringReporter",
        new_opcode="(OPERAND1) + (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "operator_subtract": BlockInfo(
        block_type="stringReporter",
        new_opcode="(OPERAND1) - (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "operator_multiply": BlockInfo(
        block_type="stringReporter",
        new_opcode="(OPERAND1) * (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "operator_divide": BlockInfo(
        block_type="stringReporter",
        new_opcode="(OPERAND1) / (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "operator_power": BlockInfo(
        block_type="stringReporter",
        new_opcode="(OPERAND1) ^ (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "operator_advMathExpanded": BlockInfo(
        block_type="stringReporter",
        new_opcode="(OPERAND1) * (OPERAND2) [OPERATION] (OPERAND3)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="ONE"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="TWO"),
            "OPERAND3": InputInfo(InputType.NUMBER, old="THREE"),
        },
        dropdowns={
            "OPERATION": DropdownInfo(DropdownType.ROOT_LOG, old="OPTION"),
        },
    ),
    "operator_advMath": BlockInfo(
        block_type="stringReporter",
        new_opcode="(OPERAND1) [OPERATION] (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="ONE"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="TWO"),
        },
        dropdowns={
            "OPERATION": DropdownInfo(DropdownType.POWER_ROOT_LOG, old="OPTION"),
        },
    ),
    "operator_random": BlockInfo(
        block_type="stringReporter",
        new_opcode="pick random (OPERAND1) to (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="FROM"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="TO"),
        },
    ),
    "operator_constrainnumber": BlockInfo(
        block_type="stringReporter",
        new_opcode="constrain (NUM) min (MIN) max (MAX)",
        inputs={
            "NUM": InputInfo(InputType.NUMBER, old="inp"),
            "MIN": InputInfo(InputType.NUMBER, old="min"),
            "MAX": InputInfo(InputType.NUMBER, old="max"),
        },
    ),
    "operator_lerpFunc": BlockInfo(
        block_type="stringReporter",
        new_opcode="interpolate (OPERAND1) to (OPERAND2) by (WEIGHT)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="ONE"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="TWO"),
            "WEIGHT": InputInfo(InputType.NUMBER, old="AMOUNT"),
        },
    ),
    "operator_gt": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(OPERAND1) > (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "operator_gtorequal": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(OPERAND1) >= (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "operator_lt": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(OPERAND1) < (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "operator_ltorequal": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(OPERAND1) <= (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "operator_equals": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(OPERAND1) = (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "operator_notequal": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(OPERAND1) != (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "operator_trueBoolean": BlockInfo(
        block_type="booleanReporter",
        new_opcode="true",
    ),
    "operator_falseBoolean": BlockInfo(
        block_type="booleanReporter",
        new_opcode="false",
    ),
    "operator_and": BlockInfo(
        block_type="booleanReporter",
        new_opcode="<OPERAND1> and <OPERAND2>",
        inputs={
            "OPERAND1": InputInfo(InputType.BOOLEAN, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.BOOLEAN, old="OPERAND2"),
        },
    ),
    "operator_or": BlockInfo(
        block_type="booleanReporter",
        new_opcode="<OPERAND1> or <OPERAND2>",
        inputs={
            "OPERAND1": InputInfo(InputType.BOOLEAN, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.BOOLEAN, old="OPERAND2"),
        },
    ),
    "operator_not": BlockInfo(
        block_type="booleanReporter",
        new_opcode="not <OPERAND>",
        inputs={
            "OPERAND": InputInfo(InputType.BOOLEAN, old="OPERAND"),
        },
    ),
    "operator_newLine": BlockInfo(
        block_type="stringReporter",
        new_opcode="new line",
    ),
    "operator_tabCharacter": BlockInfo(
        block_type="stringReporter",
        new_opcode="tab character",
    ),
    "operator_join": BlockInfo(
        block_type="stringReporter",
        new_opcode="join (STRING1) (STRING2)",
        inputs={
            "STRING1": InputInfo(InputType.TEXT, old="STRING1"),
            "STRING2": InputInfo(InputType.TEXT, old="STRING2"),
        },
    ),
    "operator_join3": BlockInfo(
        block_type="stringReporter",
        new_opcode="join (STRING1) (STRING2) (STRING3)",
        inputs={
            "STRING1": InputInfo(InputType.TEXT, old="STRING1"),
            "STRING2": InputInfo(InputType.TEXT, old="STRING2"),
            "STRING3": InputInfo(InputType.TEXT, old="STRING3"),
        },
    ),
    "operator_indexOfTextInText": BlockInfo(
        block_type="stringReporter",
        new_opcode="index of (SUBSTRING) in (TEXT)",
        inputs={
            "SUBSTRING": InputInfo(InputType.TEXT, old="TEXT1"),
            "TEXT": InputInfo(InputType.TEXT, old="TEXT2"),
        },
    ),
    "operator_lastIndexOfTextInText": BlockInfo(
        block_type="stringReporter",
        new_opcode="last index of (SUBSTRING) in (TEXT)",
        inputs={
            "SUBSTRING": InputInfo(InputType.TEXT, old="TEXT1"),
            "TEXT": InputInfo(InputType.TEXT, old="TEXT2"),
        },
    ),
    "operator_letter_of": BlockInfo(
        block_type="stringReporter",
        new_opcode="letter (LETTER) of (STRING)",
        inputs={
            "LETTER": InputInfo(InputType.POSITIVE_INTEGER, old="LETTER"),
            "STRING": InputInfo(InputType.TEXT, old="STRING"),
        },
    ),
    "operator_getLettersFromIndexToIndexInText": BlockInfo(
        block_type="stringReporter",
        new_opcode="letters from (START) to (STOP) in (TEXT)",
        inputs={
            "START": InputInfo(InputType.POSITIVE_INTEGER, old="INDEX1"),
            "STOP": InputInfo(InputType.TEXT, old="INDEX2"),
            "TEXT": InputInfo(InputType.TEXT, old="TEXT"),
        },
    ),
    "operator_length": BlockInfo(
        block_type="stringReporter",
        new_opcode="length of (TEXT)",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="STRING"),
        },
    ),
    "operator_contains": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(TEXT) contains (SUBSTRING) ?",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="STRING1"),
            "SUBSTRING": InputInfo(InputType.TEXT, old="STRING2"),
        },
    ),
    "operator_textStartsOrEndsWith": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(TEXT) [OPERATION] with (SUBSTRING) ?",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="TEXT1"),
            "SUBSTRING": InputInfo(InputType.TEXT, old="TEXT2"),
        },
        dropdowns={
            "OPERATION": DropdownInfo(DropdownType.TEXT_METHOD, old="OPTION"),
        },
    ),
    "operator_replaceAll": BlockInfo(
        block_type="stringReporter",
        new_opcode="in (TEXT) replace all (OLDVALUE) with (NEWVALUE)",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="text"),
            "OLDVALUE": InputInfo(InputType.TEXT, old="term"),
            "NEWVALUE": InputInfo(InputType.TEXT, old="res"),
        },
    ),
    "operator_replaceFirst": BlockInfo(
        block_type="stringReporter",
        new_opcode="in (TEXT) replace first (OLDVALUE) with (NEWVALUE)",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="text"),
            "OLDVALUE": InputInfo(InputType.TEXT, old="term"),
            "NEWVALUE": InputInfo(InputType.TEXT, old="res"),
        },
    ),
    "operator_regexmatch": BlockInfo(
        block_type="stringReporter",
        new_opcode="match (TEXT) with regex (REGEX) (MODIFIER)",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="text"),
            "REGEX": InputInfo(InputType.TEXT, old="reg"),
            "MODIFIER": InputInfo(InputType.TEXT, old="regrule"),
        },
    ),
    "operator_toUpperLowerCase": BlockInfo(
        block_type="stringReporter",
        new_opcode="(TEXT) to [CASE]",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="TEXT"),
        },
        dropdowns={
            "CASE": DropdownInfo(DropdownType.TEXT_CASE, old="OPTION"),
        },
    ),
    "operator_mod": BlockInfo(
        block_type="stringReporter",
        new_opcode="(OPERAND1) mod (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="NUM1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="NUM2"),
        },
    ),
    "operator_round": BlockInfo(
        block_type="stringReporter",
        new_opcode="round (NUM)",
        inputs={
            "NUM": InputInfo(InputType.NUMBER, old="NUM"),
        },
    ),
    "operator_mathop": BlockInfo(
        block_type="stringReporter",
        new_opcode="[OPERATION] of (NUM)",
        inputs={
            "NUM": InputInfo(InputType.NUMBER, old="NUM"),
        },
        dropdowns={
            "OPERATION": DropdownInfo(DropdownType.UNARY_MATH_OPERATION, old="OPERATOR"),
        },
    ),
    "operator_stringify": BlockInfo(
        block_type="stringReporter",
        new_opcode="(VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="ONE"),
        },
    ),
    "operator_boolify": BlockInfo(
        block_type="booleanReporter",
        new_opcode="(VALUE) as a boolean",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="ONE"),
        },
    ),
})