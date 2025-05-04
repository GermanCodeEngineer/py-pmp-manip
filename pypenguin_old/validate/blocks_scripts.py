from pypenguin.utility import parseCustomOpcode, getListOfClosestStrings
from validate.constants import validateSchema, formatError, inputSchema, blockSchema, scriptSchema
from validate.errors import blockTypeError, unknownOpcodeError, inputIdError, missingInputAttributeError, optionIdError, optionValueCategoryError, optionValueError, undefinedVariableError, undefinedListError, undefinedCustomOpcodeError, embeddedMenuError
from validate.comments import validateComment
from database import *

allowedOpcodes = getAllOptimizedOpcodes()

def validateScript(path, data, context, isNested=False):
    returnValue = None
    # Check script format
    validateSchema(pathToData=path, data=data, schema=scriptSchema)
    
    # Check block formats
    for i, block in enumerate(data["blocks"]):
        validateBlock(
            path=path + ["blocks"] + [i],
            data=block,
            context=context,
        )
        
        oldOpcode = getDeoptimizedOpcode(opcode=block["opcode"])
        blockType = getBlockType(opcode=oldOpcode)
        if blockType == "dynamic":
            match oldOpcode:
                case "control_stop":
                    optionId = getOptimizedOptionId(opcode=oldOpcode, optionId="STOP_OPTION")
                    match block["options"][optionId][1]:
                        case "all" | "this script"    : blockType = "lastInstruction"
                        case "other scripts in sprite": blockType = "instruction"
                case "procedures_call":
                    pass # Is checked in the second iteration
        validateBlockType(
            path=path+["blocks"]+[i],
            blockType=blockType,
            isNested=isNested,
            isFirst=(i == 0),
            isLast=not(i+1 in range(len(data["blocks"]))),
            isOnly=(len(data["blocks"]) == 1),
        )

        if oldOpcode == "special_define":
            returnValue = (
                block["options"]["customOpcode"][1],
                block["options"]["blockType"][1],
            )
    return returnValue

def validateBlockType(path, blockType, isNested, isFirst, isLast, isOnly):
    if isNested:
        if blockType in ["stringReporter", "numberReporter", "booleanReporter"]:
            raise formatError(blockTypeError, path, "Reporter blocks are not allowed in the 'blocks' attribute of an input.")
        if blockType == "hat":
            raise formatError(blockTypeError, path, "Hat blocks are not allowed in the 'blocks' attribute of an input.")
    
    if   (blockType in ["stringReporter", "numberReporter", "booleanReporter"]) and not(isOnly):
        raise formatError(blockTypeError, path, "A reporter block must be the only block in it's script.")
    elif blockType == "hat" and not(isFirst):
        raise formatError(blockTypeError, path, "A hat block must to be the first block in it's script.")
    elif blockType == "lastInstruction" and not(isLast): # when there is a next block
        raise formatError(blockTypeError, path, "An ending block must be the last block in it's script.")
    elif blockType == "embeddedMenu":
        raise formatError(blockTypeError, path, "An embedded menu must be embedded in another block.")

def validateBlock(path, data, context, expectedShape=None, embeddedMenuOpcode=None):
    if "inputs" not in data:
        data["inputs"] = inputDefault
    if "options" not in data:
        data["options"] = optionDefault
    if "comment" not in data:
        data["comment"] = commentDefault
    
    # Check block format
    validateSchema(pathToData=path, data=data, schema=blockSchema)
    # Check block opcode
    if data["opcode"] not in allowedOpcodes:
        listOfClosest = getListOfClosestStrings(
            string=data["opcode"],
            possibleValues=allowedOpcodes,
        )
        raise formatError(unknownOpcodeError, path+["opcode"], f"Unknown opcode: '{data['opcode']}'. Most Similar Opcodes: {listOfClosest}")

    if data["comment"] != None:
        validateComment(path=path+["comment"], data=data["comment"])
    
    opcode = data["opcode"]
    oldOpcode = getDeoptimizedOpcode(opcode=opcode)
    validateInputs(
        path=path+["inputs"], 
        data=data["inputs"],
        opcode=opcode, 
        context=context, 
        options=data["options"],
    )
    validateOptions(
        path=path+["options"],
        data=data["options"],
        opcode=opcode,
        context=context,
        inputDatas=data["inputs"],
    )
    if oldOpcode == "procedures_call":
        validateCallInputs(
            path=path+["inputs"], 
            data=data["inputs"],
            opcode=opcode,
            optionDatas=data["options"],
            context=context,
        )
    
    validateBlockShape(
        path=path,
        oldOpcode=oldOpcode,
        expectedShape=expectedShape,
        embeddedMenuOpcode=embeddedMenuOpcode,
    )

def validateBlockShape(path, oldOpcode, expectedShape, embeddedMenuOpcode=None):
    blockType = getBlockType(opcode=oldOpcode)
    if   expectedShape == "stringReporter":
        possibleValues = ["stringReporter", "booleanReporter", "dynamic"]
        message = "Must be either a string or boolean reporter block."
    elif expectedShape == "booleanReporter":
        possibleValues = ["booleanReporter", "dynamic"]
        message = "Must be a boolean reporter block."
    else:
        if expectedShape == "embeddedMenu":
            if oldOpcode != embeddedMenuOpcode:
                emo = getOptimizedOpcode(embeddedMenuOpcode)
                raise formatError(embeddedMenuError, path+["opcode"], f"Must be '{emo}'.")
        return
    if blockType not in possibleValues:
        raise formatError(blockTypeError, path, message)

def validateInputs(path, data, opcode, context, options):
    oldOpcode       = getDeoptimizedOpcode(opcode=opcode)
    allowedInputIds = list(getInputTypes(opcode=oldOpcode).keys()) # List of inputs which are defined for the specific opcode
    if oldOpcode == "procedures_call": # Inputs in the call custom block block are custom
        return
    for inputId, inputValue in data.items():
        if inputId not in allowedInputIds:
            raise formatError(inputIdError, path, f"Input '{inputId}' is not defined for a block with opcode '{opcode}'.")
    for inputId in allowedInputIds:
        inputType = getInputType(
            opcode=oldOpcode,
            inputId=inputId,
        )
        inputMode = getInputMode(
            opcode=oldOpcode,
            inputId=inputId,
        )
        if (inputMode not in ["block-only", "script"]) or (inputType == "embeddedMenu"):
            canPassAnyway = False
            if (oldOpcode == "polygon" and inputId in ["x4", "y4"]):
                if options["VERTEX_COUNT"] != 4:
                    canPassAnyway  = True # x4 and y4 are only required when VERTEX_COUNT is 4 
            if (inputId not in data) and not(canPassAnyway):
                raise formatError(inputIdError, path, f"A block with opcode '{opcode}' must have the input '{inputId}'.")

    inputTypes = getInputTypes(opcode=oldOpcode)

    # Check input formats
    for inputId in data:
        inputType = inputTypes[inputId]

        if inputId in data:
            inputMode = inputModes[inputType]
            inputValue = data[inputId]
            validateInputValue(
                path=path+[inputId],
                inputValue=inputValue,
                inputType=inputType,
                inputMode=inputMode,
                opcode=opcode,
                inputDatas=data,
                context=context,
            )

def validateInputValue(path, inputValue, inputType, inputMode, opcode, inputDatas, context):
    oldOpcode = getDeoptimizedOpcode(opcode)
    inputValue["mode"] = inputMode
    # Check input value format
    validateSchema(pathToData=path, data=inputValue, schema=inputSchema)
    if   inputMode in ["block-and-text", "block-and-menu-text"]:
        required = ["block", "text"]
    elif inputMode == "block-only":
        required = ["block"]
    elif inputMode == "script":
        required = ["blocks"]
    elif inputMode in ["block-and-option", "block-and-broadcast-option"]:
        required = ["option"]
    
    for attribute in required:
        if attribute not in inputValue:
            match attribute:
                case "block":
                    if inputType == "embeddedMenu":
                        raise formatError(missingInputAttributeError, path, "Must have the attribute 'block' in this case.")
                    inputValue["block"] = inputBlockDefault
                case "text":
                    if inputType == "note":
                        inputValue["text"] = noteInputTextDefault
                    else:
                        inputValue["text"] = inputTextDefault
                case "blocks":
                    inputValue["blocks"] = inputBlocksDefault
                case "option":
                    raise formatError(missingInputAttributeError, path, "Must have the attribute 'option'.")
    if inputValue.get("block") == None:
        if inputType == "embeddedMenu":
            raise formatError(embeddedMenuError, path+["block"], "Mustn't be None in this case.")
    else: # When the input has a block and it isn't None, check the block format
        emo = getEmbeddedMenuOpcode(oldOpcode)
        validateBlock(
            path=path+["block"], 
            data=inputValue["block"], 
            context=context,
            expectedShape="booleanReporter" if inputType == "boolean" else ("embeddedMenu" if inputType == "embeddedMenu" else "stringReporter"),
            embeddedMenuOpcode=emo,
        )
    
    if inputValue.get("blocks", []) != []:
        preparedData = {"position": [0,0], "blocks": inputValue["blocks"]}
        validateScript(
            path=path, 
            data=preparedData, 
            context=context,
            isNested=True
        )
    
    if inputValue.get("option") != None:
        validateOptionValue(
            path=path+["option"],
            data=inputValue["option"],
            opcode=opcode,
            optionType=inputType, # Might need to be changed
            context=context,
            inputDatas=inputDatas,
        )

def validateCallInputs(path, data, opcode, optionDatas, context):
    proccode, inputTypes = parseCustomOpcode(optionDatas["customOpcode"][1])
    inputTypes = {k: ("text" if v==str else "boolean") for k,v in inputTypes.items()}
    for inputId, inputType in inputTypes.items():
        if inputType == "text" and inputId not in data:
            raise formatError(inputIdError, path, f"A custom block with custom opcode '{optionDatas['customOpcode'][1]}' must have the input '{inputId}'.")

    # Check input formats
    for inputId in data:
        if inputId not in inputTypes:
            raise formatError(inputIdError, path, f"Input '{inputId}' is not defined for a custom block with custom opcode '{optionDatas['customOpcode'][1]}'.")
    
    for inputId, inputValue in data.items():
        validateInputValue(
            path=path+[inputId],
            inputValue=inputValue,
            inputType=inputTypes[inputId],
            inputMode=inputModes[inputTypes[inputId]],
            opcode=opcode,
            inputDatas=data,
            context=context,
        )

def validateOptions(path, data, opcode, context, inputDatas):
    oldOpcode        = getDeoptimizedOpcode(opcode=opcode)
    allowedOptionIds = list(getOptionTypes(opcode=oldOpcode).keys()) # List of inputs which are defined for the specific opcode
    for optionId, optionValue in data.items():
        if optionId not in allowedOptionIds:
            raise formatError(optionIdError, path, f"Option '{optionId}' is not defined for a block with opcode '{opcode}'.")
    for optionId in allowedOptionIds:
        if optionId not in data:
            raise formatError(optionIdError, path, f"A block with opcode '{opcode}' must have the option '{optionId}'.")

        
        optionType = getOptionType(
            opcode=oldOpcode,
            optionId=optionId,
        )
        optionValue = data[optionId]
        validateOptionValue(
            path=path+[optionId],
            data=optionValue,
            opcode=opcode,
            optionType=optionType,
            context=context,
            inputDatas=inputDatas,
        )

def validateOptionValue(path, data, opcode, optionType, context, inputDatas):
    def makeString(possibleValues):
        if possibleValues == []:
            string = "No possible values."
        else:
            string = ""
            for value in possibleValues:
                string += "\n- "
                string += repr(value)
        return string
    def validateCategory(path, data, suggestion, message=None):
        if data != suggestion:
            raise formatError(optionValueCategoryError, path, f"Must be '{suggestion}'." if message==None else message)
    match optionType:
        case "broadcast"|"reporter name"|"opcode":
            if not isinstance(data[1], str):
                raise formatError(optionValueError, path, f"Must be a string.")
            validateCategory(path+[0], data[0], "value")
        case "variable":
            possibleValues = context["scopeVariables"]
            possibleValuesString = makeString(possibleValues)
            if data not in possibleValues:
                raise formatError(undefinedVariableError, path, f"Must be a defined variable. Must be one of these: {possibleValuesString}")
        case "list":
            possibleValues = context["scopeLists"]
            possibleValuesString = makeString(possibleValues)
            if data not in possibleValues:
                raise formatError(undefinedListError, path, f"Must be a defined list. Must be one of these: {possibleValuesString}")
        case "boolean":
            validateCategory(path+[0], data[0], "value")
            if not isinstance(data[1], bool):
                raise formatError(optionValueError, path, f"Must be a boolean.")
        case _:
            possibleValues = getOptimizedOptionValuesUsingContext(
                optionType=optionType,
                context=context,
                inputDatas=inputDatas,
            )
            _, defaultPrefix = getOptimizedOptionValuesUsingNoContext(
                optionType=optionType,
            )
            possibleValuesString = makeString(possibleValues)
            if data not in possibleValues:
                if defaultPrefix == None:
                    raise formatError(optionValueError, path, f"Must be one of these: {possibleValuesString}")
                else:
                    validateCategory(path, data[0], defaultPrefix, message=f"If item 0 is not {repr(defaultPrefix)} must be one of these: {possibleValuesString}")

def validateScriptCustomBlocks(path, data, CBTypes, isNested=False):
    for i, block in enumerate(data):
        validateBlockCustomBlocks(
            path=path+[i], 
            data=block, 
            CBTypes=CBTypes,
        )
        
        oldOpcode = getDeoptimizedOpcode(opcode=block["opcode"])
        if oldOpcode != "procedures_call":
            continue
        
        customOpcode = validateCustomOpcode(
            path=path+[i],
            block=block,
            CBTypes=CBTypes,
        )
        
        blockType = CBTypes[customOpcode]
        validateBlockType(
            path=path+[i],
            blockType=blockType,
            isNested=isNested,
            isFirst=(i == 0),
            isLast=not(i+1 in range(len(data))),
            isOnly=(len(data) == 1),
        )

def validateCustomOpcode(path, block, CBTypes):
    customOpcode = block["options"]["customOpcode"][1]
    if customOpcode not in CBTypes:
        if CBTypes == {}:
            customOpcodesString = "No defined custom blocks."
        else:
            customOpcodesString = ""
            for co in CBTypes.keys():
                customOpcodesString += f"\n- {['value', co]}"
        raise formatError(undefinedCustomOpcodeError, path+["options"]+["customOpcode"], f"Custom block '{customOpcode}' is not defined. Defined custom opcodes: {customOpcodesString}")
    return customOpcode

def validateBlockCustomBlocks(path, data, CBTypes, expectedShape=None):
    oldOpcode = getDeoptimizedOpcode(opcode=data["opcode"])
    if "inputs" in data:
        if oldOpcode == "procedures_call":
            proccode, inputTypes = parseCustomOpcode(data["options"]["customOpcode"][1])
            inputTypes = {k: ("text" if v==str else "boolean") for k,v in inputTypes.items()}
        else:
            inputTypes = getInputTypes(opcode=oldOpcode)
        
        for inputId, inputValue in data["inputs"].items():
            inputType = inputTypes[inputId]
            
            inputBlock = inputValue.get("block")
            if inputBlock != None:
                validateBlockCustomBlocks(
                    path=path+["inputs"]+[inputId]+["block"],
                    data=inputBlock,
                    CBTypes=CBTypes,
                    expectedShape="booleanReporter" if inputType == "boolean" else ("embeddedMenu" if inputType == "embeddedMenu" else "stringReporter"),
                )
            
            inputBlocks = inputValue.get("blocks")
            if inputBlocks != None:
                validateScriptCustomBlocks(
                    path=path+["inputs"]+[inputId]+["blocks"],
                    data=inputBlocks,
                    CBTypes=CBTypes,
                    isNested=True,
                )
    if   expectedShape == "stringReporter":
        possibleValues = ["stringReporter", "booleanReporter"]
        message = "Must be either a string or boolean reporter block."
    elif expectedShape == "booleanReporter":
        possibleValues = ["booleanReporter"]
        message = "Must be a boolean reporter block."
    else:
        return
    blockType = getBlockType(opcode=oldOpcode)
    if blockType == "dynamic" and oldOpcode == "procedures_call":
        customOpcode = validateCustomOpcode(
            path=path,
            block=data,
            CBTypes=CBTypes,
        )
        blockType = CBTypes[customOpcode]
        if blockType in ["textReporter", "numberReporter"]:
            blockType = "stringReporter"
    if blockType not in possibleValues:
        raise formatError(blockTypeError, path, message)
