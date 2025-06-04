import re

# -----------------------
# Custom Opcode Functions
# -----------------------
def escapeChars(inputString: str, charsToEscape: list) -> str:
    escapedString = re.sub(r'\\', r'\\\\', inputString)
    for char in charsToEscape:
        escapedString = re.sub(re.escape(char), r'\\' + char, escapedString)
    return escapedString

def parseCustomOpcode(customOpcode: str):
    part = ""
    mode = None
    arguments = {}
    isEscaped = False
    justCompletedArgument = False
    proccode = ""

    for i, char in enumerate(customOpcode):
        if char == "\\":
            justCompletedArgument = False
            part += "\\" if isEscaped else ""
            isEscaped = not isEscaped
        elif char == "(":
            if isEscaped:
                part += char
                isEscaped = False
            else:
                mode = str
                if not part.endswith(" "):
                    part += " "
                proccode += part + "%s "
                part = ""
        elif char == "<":
            if isEscaped:
                part += char
                isEscaped = False
            else:
                mode = bool
                if not part.endswith(" "):
                    part += " "
                proccode += part + "%b "
                part = ""
        elif char == ")":
            if isEscaped:
                part += char
            else:
                if mode != str:
                    raise Exception()
                arguments[part] = str
                part = ""
                justCompletedArgument = True
        elif char == ">":
            if isEscaped:
                part += char
            else:
                if mode != bool:
                    raise Exception()
                arguments[part] = bool
                part = ""
                justCompletedArgument = True
        else:
            if not (char == " " and justCompletedArgument):
                justCompletedArgument = False
                part += char

    proccode += part
    proccode = proccode.removesuffix(" ")
    return proccode, arguments

def generateCustomOpcode(proccode: str, argumentNames: list[str]):
    customOpcode = ""
    i = 0
    j = 0
    chars_to_escape = ["(", ")", "<", ">"]
    
    while i < len(proccode):
        char = proccode[i]
        char2 = proccode[i + 1] if i + 1 < len(proccode) else None
        char3 = proccode[i + 2] if i + 2 < len(proccode) else None
        
        if char == " " and char2 == "%" and char3 in {"s", "n"}:
            argumentName = escapeChars(argumentNames[j], chars_to_escape)
            customOpcode += " (" + argumentName + ")"
            j += 1
            i += 3  # Skip over '%s'/'%n'
        elif char == " " and char2 == "%" and char3 == "b":
            argumentName = escapeChars(argumentNames[j], chars_to_escape)
            customOpcode += " <" + argumentName + ">"
            j += 1
            i += 3  # Skip over '%b'
        else:
            customOpcode += escapeChars(char, chars_to_escape)
            i += 1
    return customOpcode.removesuffix(" ")

