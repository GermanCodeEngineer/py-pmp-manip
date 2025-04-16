from block_info.basis import *

operators = BlockInfoSet(name="operators", opcode_prefix="operator", block_infos={
    "add": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) + (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "subtract": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) - (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "multiply": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) * (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "divide": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) / (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "power": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) ^ (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="NUM1"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="NUM2"),
        },
    ),
    "advMathExpanded": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
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
    "advMath": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) [OPERATION] (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="ONE"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="TWO"),
        },
        dropdowns={
            "OPERATION": DropdownInfo(DropdownType.POWER_ROOT_LOG, old="OPTION"),
        },
    ),
    "random": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="pick random (OPERAND1) to (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="FROM"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="TO"),
        },
    ),
    "constrainnumber": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="constrain (NUM) min (MIN) max (MAX)",
        inputs={
            "NUM": InputInfo(InputType.NUMBER, old="inp"),
            "MIN": InputInfo(InputType.NUMBER, old="min"),
            "MAX": InputInfo(InputType.NUMBER, old="max"),
        },
    ),
    "lerpFunc": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="interpolate (OPERAND1) to (OPERAND2) by (WEIGHT)",
        inputs={
            "OPERAND1": InputInfo(InputType.NUMBER, old="ONE"),
            "OPERAND2": InputInfo(InputType.NUMBER, old="TWO"),
            "WEIGHT": InputInfo(InputType.NUMBER, old="AMOUNT"),
        },
    ),
    "gt": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) > (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "gtorequal": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) >= (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "lt": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) < (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "ltorequal": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) <= (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "equals": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) = (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "notequal": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) != (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="OPERAND2"),
        },
    ),
    "trueBoolean": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="true",
    ),
    "falseBoolean": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="false",
    ),
    "and": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="<OPERAND1> and <OPERAND2>",
        inputs={
            "OPERAND1": InputInfo(InputType.BOOLEAN, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.BOOLEAN, old="OPERAND2"),
        },
    ),
    "or": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="<OPERAND1> or <OPERAND2>",
        inputs={
            "OPERAND1": InputInfo(InputType.BOOLEAN, old="OPERAND1"),
            "OPERAND2": InputInfo(InputType.BOOLEAN, old="OPERAND2"),
        },
    ),
    "not": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="not <OPERAND>",
        inputs={
            "OPERAND": InputInfo(InputType.BOOLEAN, old="OPERAND"),
        },
    ),
    "newLine": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="new line",
    ),
    "tabCharacter": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="tab character",
    ),
    "join": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="join (STRING1) (STRING2)",
        inputs={
            "STRING1": InputInfo(InputType.TEXT, old="STRING1"),
            "STRING2": InputInfo(InputType.TEXT, old="STRING2"),
        },
    ),
    "join3": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="join (STRING1) (STRING2) (STRING3)",
        inputs={
            "STRING1": InputInfo(InputType.TEXT, old="STRING1"),
            "STRING2": InputInfo(InputType.TEXT, old="STRING2"),
            "STRING3": InputInfo(InputType.TEXT, old="STRING3"),
        },
    ),
    "indexOfTextInText": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="index of (SUBSTRING) in (TEXT)",
        inputs={
            "SUBSTRING": InputInfo(InputType.TEXT, old="TEXT1"),
            "TEXT": InputInfo(InputType.TEXT, old="TEXT2"),
        },
    ),
    "lastIndexOfTextInText": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="last index of (SUBSTRING) in (TEXT)",
        inputs={
            "SUBSTRING": InputInfo(InputType.TEXT, old="TEXT1"),
            "TEXT": InputInfo(InputType.TEXT, old="TEXT2"),
        },
    ),
    "letter_of": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="letter (LETTER) of (STRING)",
        inputs={
            "LETTER": InputInfo(InputType.POSITIVE_INTEGER, old="LETTER"),
            "STRING": InputInfo(InputType.TEXT, old="STRING"),
        },
    ),
    "getLettersFromIndexToIndexInText": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="letters from (START) to (STOP) in (TEXT)",
        inputs={
            "START": InputInfo(InputType.POSITIVE_INTEGER, old="INDEX1"),
            "STOP": InputInfo(InputType.TEXT, old="INDEX2"),
            "TEXT": InputInfo(InputType.TEXT, old="TEXT"),
        },
    ),
    "length": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="length of (TEXT)",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="STRING"),
        },
    ),
    "contains": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(TEXT) contains (SUBSTRING) ?",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="STRING1"),
            "SUBSTRING": InputInfo(InputType.TEXT, old="STRING2"),
        },
    ),
    "textStartsOrEndsWith": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(TEXT) [OPERATION] with (SUBSTRING) ?",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="TEXT1"),
            "SUBSTRING": InputInfo(InputType.TEXT, old="TEXT2"),
        },
        dropdowns={
            "OPERATION": DropdownInfo(DropdownType.TEXT_METHOD, old="OPTION"),
        },
    ),
    "replaceAll": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="in (TEXT) replace all (OLDVALUE) with (NEWVALUE)",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="text"),
            "OLDVALUE": InputInfo(InputType.TEXT, old="term"),
            "NEWVALUE": InputInfo(InputType.TEXT, old="res"),
        },
    ),
    "replaceFirst": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="in (TEXT) replace first (OLDVALUE) with (NEWVALUE)",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="text"),
            "OLDVALUE": InputInfo(InputType.TEXT, old="term"),
            "NEWVALUE": InputInfo(InputType.TEXT, old="res"),
        },
    ),
    "regexmatch": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="match (TEXT) with regex (REGEX) (MODIFIER)",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="text"),
            "REGEX": InputInfo(InputType.TEXT, old="reg"),
            "MODIFIER": InputInfo(InputType.TEXT, old="regrule"),
        },
    ),
    "toUpperLowerCase": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(TEXT) to [CASE]",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, old="TEXT"),
        },
        dropdowns={
            "CASE": DropdownInfo(DropdownType.TEXT_CASE, old="OPTION"),
        },
    ),
    "mod": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) mod (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, old="NUM1"),
            "OPERAND2": InputInfo(InputType.TEXT, old="NUM2"),
        },
    ),
    "round": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="round (NUM)",
        inputs={
            "NUM": InputInfo(InputType.NUMBER, old="NUM"),
        },
    ),
    "mathop": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[OPERATION] of (NUM)",
        inputs={
            "NUM": InputInfo(InputType.NUMBER, old="NUM"),
        },
        dropdowns={
            "OPERATION": DropdownInfo(DropdownType.UNARY_MATH_OPERATION, old="OPERATOR"),
        },
    ),
    "stringify": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="ONE"),
        },
    ),
    "boolify": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(VALUE) as a boolean",
        inputs={
            "VALUE": InputInfo(InputType.TEXT, old="ONE"),
        },
    ),
})