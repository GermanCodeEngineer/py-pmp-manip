from block_info.basis import *

operators = BlockInfoSet(name="operators", opcode_prefix="operator", block_infos={
    "add": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) + (OPERAND2)",
        inputs={
            "NUM1": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "NUM2": InputInfo(InputType.NUMBER, new="OPERAND2"),
        },
    ),
    "subtract": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) - (OPERAND2)",
        inputs={
            "NUM1": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "NUM2": InputInfo(InputType.NUMBER, new="OPERAND2"),
        },
    ),
    "multiply": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) * (OPERAND2)",
        inputs={
            "NUM1": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "NUM2": InputInfo(InputType.NUMBER, new="OPERAND2"),
        },
    ),
    "divide": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) / (OPERAND2)",
        inputs={
            "NUM1": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "NUM2": InputInfo(InputType.NUMBER, new="OPERAND2"),
        },
    ),
    "power": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) ^ (OPERAND2)",
        inputs={
            "NUM1": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "NUM2": InputInfo(InputType.NUMBER, new="OPERAND2"),
        },
    ),
    "advMathExpanded": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) * (OPERAND2) [OPERATION] (OPERAND3)",
        inputs={
            "ONE": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "TWO": InputInfo(InputType.NUMBER, new="OPERAND2"),
            "THREE": InputInfo(InputType.NUMBER, new="OPERAND3"),
        },
        dropdowns={
            "OPTION": DropdownInfo(DropdownType.ROOT_LOG, new="OPERATION"),
        },
    ),
    "advMath": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) [OPERATION] (OPERAND2)",
        inputs={
            "ONE": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "TWO": InputInfo(InputType.NUMBER, new="OPERAND2"),
        },
        dropdowns={
            "OPTION": DropdownInfo(DropdownType.POWER_ROOT_LOG, new="OPERATION"),
        },
    ),
    "random": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="pick random (OPERAND1) to (OPERAND2)",
        inputs={
            "FROM": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "TO": InputInfo(InputType.NUMBER, new="OPERAND2"),
        },
    ),
    "constrainnumber": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="constrain (NUM) min (MIN) max (MAX)",
        inputs={
            "inp": InputInfo(InputType.NUMBER, new="NUM"),
            "min": InputInfo(InputType.NUMBER, new="MIN"),
            "max": InputInfo(InputType.NUMBER, new="MAX"),
        },
    ),
    "lerpFunc": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="interpolate (OPERAND1) to (OPERAND2) by (WEIGHT)",
        inputs={
            "ONE": InputInfo(InputType.NUMBER, new="OPERAND1"),
            "TWO": InputInfo(InputType.NUMBER, new="OPERAND2"),
            "AMOUNT": InputInfo(InputType.NUMBER, new="WEIGHT"),
        },
    ),
    "gt": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) > (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, new="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, new="OPERAND2"),
        },
    ),
    "gtorequal": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) >= (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, new="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, new="OPERAND2"),
        },
    ),
    "lt": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) < (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, new="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, new="OPERAND2"),
        },
    ),
    "ltorequal": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) <= (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, new="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, new="OPERAND2"),
        },
    ),
    "equals": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) = (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, new="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, new="OPERAND2"),
        },
    ),
    "notequal": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(OPERAND1) != (OPERAND2)",
        inputs={
            "OPERAND1": InputInfo(InputType.TEXT, new="OPERAND1"),
            "OPERAND2": InputInfo(InputType.TEXT, new="OPERAND2"),
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
            "OPERAND1": InputInfo(InputType.BOOLEAN, new="OPERAND1"),
            "OPERAND2": InputInfo(InputType.BOOLEAN, new="OPERAND2"),
        },
    ),
    "or": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="<OPERAND1> or <OPERAND2>",
        inputs={
            "OPERAND1": InputInfo(InputType.BOOLEAN, new="OPERAND1"),
            "OPERAND2": InputInfo(InputType.BOOLEAN, new="OPERAND2"),
        },
    ),
    "not": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="not <OPERAND>",
        inputs={
            "OPERAND": InputInfo(InputType.BOOLEAN, new="OPERAND"),
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
            "STRING1": InputInfo(InputType.TEXT, new="STRING1"),
            "STRING2": InputInfo(InputType.TEXT, new="STRING2"),
        },
    ),
    "join3": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="join (STRING1) (STRING2) (STRING3)",
        inputs={
            "STRING1": InputInfo(InputType.TEXT, new="STRING1"),
            "STRING2": InputInfo(InputType.TEXT, new="STRING2"),
            "STRING3": InputInfo(InputType.TEXT, new="STRING3"),
        },
    ),
    "indexOfTextInText": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="index of (SUBSTRING) in (TEXT)",
        inputs={
            "TEXT1": InputInfo(InputType.TEXT, new="SUBSTRING"),
            "TEXT2": InputInfo(InputType.TEXT, new="TEXT"),
        },
    ),
    "lastIndexOfTextInText": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="last index of (SUBSTRING) in (TEXT)",
        inputs={
            "TEXT1": InputInfo(InputType.TEXT, new="SUBSTRING"),
            "TEXT2": InputInfo(InputType.TEXT, new="TEXT"),
        },
    ),
    "letter_of": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="letter (LETTER) of (STRING)",
        inputs={
            "LETTER": InputInfo(InputType.POSITIVE_INTEGER, new="LETTER"),
            "STRING": InputInfo(InputType.TEXT, new="STRING"),
        },
    ),
    "getLettersFromIndexToIndexInText": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="letters from (START) to (STOP) in (TEXT)",
        inputs={
            "INDEX1": InputInfo(InputType.POSITIVE_INTEGER, new="START"),
            "INDEX2": InputInfo(InputType.TEXT, new="STOP"),
            "TEXT": InputInfo(InputType.TEXT, new="TEXT"),
        },
    ),
    "length": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="length of (TEXT)",
        inputs={
            "STRING": InputInfo(InputType.TEXT, new="TEXT"),
        },
    ),
    "contains": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(TEXT) contains (SUBSTRING) ?",
        inputs={
            "STRING1": InputInfo(InputType.TEXT, new="TEXT"),
            "STRING2": InputInfo(InputType.TEXT, new="SUBSTRING"),
        },
    ),
    "textStartsOrEndsWith": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(TEXT) [OPERATION] with (SUBSTRING) ?",
        inputs={
            "TEXT1": InputInfo(InputType.TEXT, new="TEXT"),
            "TEXT2": InputInfo(InputType.TEXT, new="SUBSTRING"),
        },
        dropdowns={
            "OPTION": DropdownInfo(DropdownType.TEXT_METHOD, new="OPERATION"),
        },
    ),
    "replaceAll": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="in (TEXT) replace all (OLDVALUE) with (NEWVALUE)",
        inputs={
            "text": InputInfo(InputType.TEXT, new="TEXT"),
            "term": InputInfo(InputType.TEXT, new="OLDVALUE"),
            "res": InputInfo(InputType.TEXT, new="NEWVALUE"),
        },
    ),
    "replaceFirst": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="in (TEXT) replace first (OLDVALUE) with (NEWVALUE)",
        inputs={
            "text": InputInfo(InputType.TEXT, new="TEXT"),
            "term": InputInfo(InputType.TEXT, new="OLDVALUE"),
            "res": InputInfo(InputType.TEXT, new="NEWVALUE"),
        },
    ),
    "regexmatch": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="match (TEXT) with regex (REGEX) (MODIFIER)",
        inputs={
            "text": InputInfo(InputType.TEXT, new="TEXT"),
            "reg": InputInfo(InputType.TEXT, new="REGEX"),
            "regrule": InputInfo(InputType.TEXT, new="MODIFIER"),
        },
    ),
    "toUpperLowerCase": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(TEXT) to [CASE]",
        inputs={
            "TEXT": InputInfo(InputType.TEXT, new="TEXT"),
        },
        dropdowns={
            "OPTION": DropdownInfo(DropdownType.TEXT_CASE, new="CASE"),
        },
    ),
    "mod": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(OPERAND1) mod (OPERAND2)",
        inputs={
            "NUM1": InputInfo(InputType.TEXT, new="OPERAND1"),
            "NUM2": InputInfo(InputType.TEXT, new="OPERAND2"),
        },
    ),
    "round": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="round (NUM)",
        inputs={
            "NUM": InputInfo(InputType.NUMBER, new="NUM"),
        },
    ),
    "mathop": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[OPERATION] of (NUM)",
        inputs={
            "NUM": InputInfo(InputType.NUMBER, new="NUM"),
        },
        dropdowns={
            "OPERATOR": DropdownInfo(DropdownType.UNARY_MATH_OPERATION, new="OPERATION"),
        },
    ),
    "stringify": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="(VALUE)",
        inputs={
            "ONE": InputInfo(InputType.TEXT, new="VALUE"),
        },
    ),
    "boolify": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="(VALUE) as a boolean",
        inputs={
            "ONE": InputInfo(InputType.TEXT, new="VALUE"),
        },
    ),
})