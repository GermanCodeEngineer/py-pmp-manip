from pypenguin.utility import generateCustomOpcode, pp
from pypenguin.database import getOptimizedOpcode, getDeoptimizedOpcode, getOptimizedInputId, getInputMode, getInputModes, getOptimizedOptionId, getBlockType, optimizeOptionValue, getInputType, getOptionType, inputTextDefault

import copy, json

def finishScripts(data):
    newScriptDatas = []
    for scriptData in data:
        newBlockDatas = []
        for blockData in scriptData["blocks"]:
            newBlockDatas.append(finishBlock(data=blockData))
        newScriptDatas.append({
            "position": scriptData["position"],
            "blocks"  : newBlockDatas,
        })
    return newScriptDatas

def finishBlock(data):
    blockType = getBlockType(
        opcode=getDeoptimizedOpcode(
            opcode=data["opcode"]
        ),
    )
    if blockType == "menu":
        return list(data["options"].values())[0]
        """ example:
        {
            "opcode": "#TOUCHING OBJECT MENU",
            "inputs": {},
            "options": {"TOUCHINGOBJECTMENU": ["object", "_mouse_"]},
            "_info_": ...,
        }
        --> "_mouse_" """
    opcode = getDeoptimizedOpcode(opcode=data["opcode"])

    newInputDatas = {}
    for inputId, inputData in data["inputs"].items():
        newInputData = copy.deepcopy(inputData)
        if inputData.get("block") is not None:
            newInputData["block"]  = finishBlock(data=inputData["block"])
        if inputData.get("blocks") is not None:
            newInputData["blocks"] = [finishBlock(data=subBlockData) for subBlockData in inputData["blocks"]]
        if   isinstance(inputData.get("option"), dict):
            newInputData["option"] = finishBlock(data=inputData["option"])
        elif isinstance(inputData.get("option"), str):
            newInputData["option"] = inputData["option"]
        
        if opcode != "procedures_call":
            # A procedure call can't have an input like this
            inputMode = getInputMode(
                opcode=opcode,
                inputId=inputId,
            )
            # rename 'text' to 'option'
            if inputMode == "block-and-broadcast-option":
                newInputData["option"] = newInputData["text"]
                del newInputData["text"]
            # replace 'option' with 'text'
            if inputMode == "block-and-menu-text":
                newInputData["text"] = newInputData["option"]
                del newInputData["option"]

            
        
        if "option" in newInputData:
            optionType = getInputType(
                opcode=opcode,
                inputId=inputId,
            )
            newInputData["option"] = optimizeOptionValue(
                optionValue=newInputData["option"],
                optionType=optionType,
            )
        if opcode == "polygon" and inputId in ["x4", "y4"]:
            if data["options"]["VERTEX_COUNT"] == 3: 
                continue # When the polygon block has only 3 not 4 vertecies do not keep x4, y4
        newInputDatas[inputId] = newInputData
    
    newOptionDatas = {}
    for optionId, optionData in data["options"].items():
        optionType = getOptionType(
            opcode=opcode,
            optionId=optionId,
        )
        newOptionData = optimizeOptionValue(
            optionValue=optionData,
            optionType=optionType,
        )
        newOptionDatas[optionId] = newOptionData

    newData = data | {"inputs": newInputDatas, "options": newOptionDatas}
    del newData["_info_"]
    if "comment" in newData:
        del newData["comment"]["_info_"]
    return newData


def nestScripts(data):
    # Get all top level block ids
    topLevelIds = []
    for blockId, blockData in data.items():
        if isinstance(blockData, list): continue
        if blockData["_info_"]["topLevel"]:
            topLevelIds.append(blockId)
    
    # Account for that one bug(not my fault), where a block is falsely independent
    for blockId, blockData in data.items():
        for inputData in blockData["inputs"].values():
            for reference in inputData["references"]:
                subBlockData = data[reference]
                if subBlockData["_info_"]["topLevel"]:
                    subBlockData["_info_"]["topLevel"] = False
                    del subBlockData["_info_"]["position"]
                    topLevelIds.remove(reference)

    newScriptDatas = []
    for topLevelId in topLevelIds:
        scriptData = nestBlockRecursively(
            blockDatas=data,
            blockId=topLevelId,
        )
        newScriptData = {
            "position": scriptData[0]["_info_"]["position"],
            "blocks": scriptData,
        }
        newScriptDatas.append(newScriptData)
    return newScriptDatas

def nestBlockRecursively(blockDatas, blockId):
    blockData = blockDatas[blockId]
    newInputDatas = {}
    for inputId, inputData in blockData["inputs"].items():
        subBlockDatas = []
        for reference in inputData["references"]: 
            subBlockDatas.append(nestBlockRecursively(
                blockDatas=blockDatas,
                blockId=reference,
            ))

        if inputData["listBlock"] is not None:
            subBlockDatas.insert(0, [inputData["listBlock"]])
        
        blockCount = len(subBlockDatas)
        newInputData = {"mode": inputData["mode"]}
        if 0 in range(len(subBlockDatas)):
            subScriptData = subBlockDatas[0]
            subBlockData0 = subBlockDatas[0][0]
        else:
            subScriptData = None
            subBlockData0 = None
        if 1 in range(len(subBlockDatas)):
            subBlockData1 = subBlockDatas[1][0]
        else:
            subBlockData1 = None
        match inputData["mode"]:
            case "block-and-text"|"block-and-broadcast-option":
                assert blockCount in [0, 1]
                newInputData |= {
                    "block": subBlockData0 if blockCount == 1 else None,
                    "text" : inputData["text"],
                }
            case "block-only":
                assert blockCount in [0, 1]
                newInputData |= {
                    "block": subBlockData0 if blockCount == 1 else None,
                }
            case "script":
                assert blockCount in [0, 1]
                newInputData |= {
                    "blocks": subScriptData if blockCount == 1 else [],
                }
            case "block-and-option"|"block-and-menu-text":
                assert blockCount in [1, 2]
                newInputData |= {
                    "block" : None          if blockCount == 1 else subBlockData0,
                    "option": subBlockData0 if blockCount == 1 else subBlockData1,
               }
        newInputDatas[inputId] = newInputData
    
    newBlockData = blockData | {"inputs": newInputDatas}
    newBlockDatas = [newBlockData]
    if blockData["_info_"]["next"] is not None:
        newBlockDatas += nestBlockRecursively(
            blockDatas=blockDatas,
            blockId=blockData["_info_"]["next"],
        )
    return newBlockDatas

def prepareProcedureDefinitionBlock(blockDatas, definitionId):
    definitionData = blockDatas[definitionId]
    prototypeId    = definitionData["inputs"]["custom_block"][1]
    prototypeData  = blockDatas[prototypeId]

    mutationData   = prototypeData["mutation"]
    proccode       = mutationData["proccode"]
    argumentNames  = json.loads(mutationData["argumentnames"])
    customOpcode  = generateCustomOpcode(
        proccode=proccode, 
        argumentNames=argumentNames
    )

    # Find out which block type the custom block is
    optype = json.loads(mutationData["optype"]) if "optype" in mutationData else None
    match optype:
        case None       : blockType = "instruction"
        case "statement": blockType = "instruction"
        case "end"      : blockType = "lastInstruction"
        case "string"   : blockType = "textReporter"
        case "number"   : blockType = "numberReporter"
        case "boolean"  : blockType = "booleanReporter"
    warp = mutationData["warp"] if isinstance(mutationData["warp"], bool) else json.loads(mutationData["warp"]) # Wether "no screen refresh is ticked"

    newBlockData = {
        "opcode": "define custom block",
        "inputs": {},
        "options": {
            "customOpcode"   : customOpcode,
            "noScreenRefresh": warp,
            "blockType"      : blockType,
        },
        "_info_"      : {
            "next"    : definitionData["next"],
            "topLevel": definitionData["topLevel"],
        },
    }
    if "comment" in definitionData:
        newBlockData["comment"] = definitionData["comment"]

    # Mark the prototype and the arguments display blocks to be deleted in the future
    prototypeData["doDelete"] = True

    for blockData in blockDatas.values():
        if blockData["parent"] == prototypeId:
            blockData["doDelete"] = True

    return newBlockData

def prepareProcedureCallBlock(blockDatas, blockId, commentDatas, mutationDatas):
    data             = blockDatas[blockId]
    proccode         = data["mutation"]["proccode"]
    mutationData     = mutationDatas[proccode]
    argumentNames    = json.loads(mutationData["argumentnames"])
    argumentTokens   = json.loads(mutationData["argumentids"])
    argumentDefaults = json.loads(mutationData["argumentdefaults"])

    newInputDatas = {}
    for i, argumentToken in enumerate(argumentTokens):
        inputId         = argumentNames[i]
        argumentDefault = argumentDefaults[i]
        if argumentDefault == "":
            inputMode = "block-and-text" # is of text type
        elif argumentDefault == "false":
            inputMode = "block-only"     # is of boolean type
        if argumentToken in data["inputs"]:
            newInputData = prepareInputValue(
                data=data["inputs"][argumentToken],
                inputMode=inputMode,
                commentDatas=commentDatas,
            )
        else:
            # Only "block-only" inputs can disappear randomly --> None is fine for "text"
            newInputData = {
                "mode"      : inputMode,
                "references": [],
                "listBlock" : None,
                "text"      : None,
            }
        newInputDatas[inputId] = newInputData

    customOpcode  = generateCustomOpcode(
        proccode=proccode, 
        argumentNames=argumentNames
    )

    newBlockData = {
        "opcode": getOptimizedOpcode(opcode="procedures_call"),
        "inputs": newInputDatas,
        "options": {
            "customOpcode": customOpcode,
        },
        "_info_"      : {
            "next"    : data["next"],
            "topLevel": data["topLevel"],
        },
    }
    return newBlockData

def prepareBlocks(data, commentDatas, mutationDatas):
    newBlockDatas = {}
    for blockId, blockData in data.items():
        isListBlock = isinstance(blockData, list)
        if isListBlock: # For list blocks e.g. value of a variable
            newBlockData = prepareListBlock(
                data=blockData, 
                blockId=blockId,
                commentDatas=commentDatas,
            )
        elif blockData["opcode"] in ["procedures_definition", "procedures_definition_return"]:
            newBlockData = prepareProcedureDefinitionBlock(
                blockDatas=data,
                definitionId=blockId,
            )
        elif blockData["opcode"] == "procedures_prototype":
            newBlockData = None # The valuable information of the prototype is alredy being transfered into the optimized definition block
        elif blockData["opcode"] == "procedures_call":
            newBlockData = prepareProcedureCallBlock(
                blockDatas=data,
                blockId=blockId,
                commentDatas=commentDatas,
                mutationDatas=mutationDatas,
            )
        else: # For normal blocks
            newBlockData = {
                "opcode"      : getOptimizedOpcode(opcode=blockData["opcode"]),
                "inputs"      : prepareInputs(
                    data=blockData["inputs"],
                    opcode=blockData["opcode"],
                    commentDatas=commentDatas,
                ),
                "options"     : prepareOptions(
                    data=blockData["fields"],
                    opcode=blockData["opcode"],
                ),
                "_info_"      : {
                    "next"    : blockData["next"],
                    "topLevel": blockData["topLevel"],
                },
            }
            if blockData["opcode"] == "polygon":
                vertext_count = json.loads(blockData["mutation"]["points"])
                newBlockData["options"]["VERTEX_COUNT"] = vertext_count
        if not isListBlock and blockData["topLevel"] == True:
            newBlockData["_info_"]["position"] = [blockData["x"], blockData["y"]]
        if not isListBlock and "comment" in blockData:
            newBlockData["comment"] = commentDatas[blockData["comment"]]
        if newBlockData is not None:
            newBlockDatas[blockId] = newBlockData
    blockDatas = newBlockDatas
    newBlockDatas = {}
    for blockId, blockData in blockDatas.items():
        if blockData.get("doDelete") == True:
            continue
        newBlockDatas[blockId] = blockData
    return newBlockDatas

def prepareInputValue(data, inputMode, commentDatas):
    itemOneType = type(data[1])
    references    = []
    listBlock     = None
    text          = None
    # Account for list blocks; 
    if   len(data) == 2:
        if   itemOneType == str: # e.g. "CONDITION": [2, "b"]
            # one block only, no text
            references.append(data[1])
        elif itemOneType == list: # e.g. "MESSAGE": [1, [10, "Bye!"]]
            # one block(currently empty) and text
            text = data[1][1]
    elif len(data) == 3:
        #print("step 1")
        itemTwoType = type(data[2])
        if   itemOneType == str  and itemTwoType == str: # e.g. "TOUCHINGOBJECTMENU": [3, "d", "e"]
            # two blocks(a menu, and a normal block) and no text
            references.append(data[1])
            references.append(data[2])
        elif itemOneType == str  and itemTwoType == list: # e.g. 'OPERAND1': [3, 'e', [10, '']]
            # one block and text
            references.append(data[1])
            text = data[2][1]
        elif itemOneType == str  and itemTwoType == type(None): # e.g. 'custom input bool': [3, 'c', None]
            # one block
            references.append(data[1])
        elif itemOneType == list and itemTwoType == list: # e.g. 'VALUE': [3, [12, 'var', '=!vkqJLb6ODy(oqe-|ZN'], [10, '0']]
            # one list block and text
            listBlock = prepareListBlock(
                data=data[1], 
                blockId=None,
                commentDatas=commentDatas,
            ) #translate list blocks into standard blocks
            text      = data[2][1]
        elif itemOneType == list and itemTwoType == str: # "TOUCHINGOBJECTMENU": [3, [12, "my variable", "`jEk@4|i[#Fk?(8x)AV.-my variable"], "b"]
            # two blocks(a menu, and a list block) and no text
            listBlock = prepareListBlock(
                data=data[1], 
                blockId=None,
                commentDatas=commentDatas,
            )
            references.append(data[2])
    newInputData = {
        "mode"      : inputMode,
        "references": references,
        "listBlock" : listBlock,
        "text"      : text,
    }
    return newInputData

def prepareInputs(data, opcode, commentDatas):
    # Replace the old with the new input ids
    newData = {}
    for inputId, inputData in data.items():
        newInputId = getOptimizedInputId(
            opcode=opcode, 
            inputId=inputId,
        )
        newData[newInputId] = inputData
    data = newData
    
    # Optimize the input values
    newData = {}
    for inputId, inputData in data.items():
        inputMode = getInputMode(
            opcode=opcode,
            inputId=inputId,
        )
        newData[inputId] = prepareInputValue(
            data=inputData,
            inputMode=inputMode,
            commentDatas=commentDatas,
        )
    
    for inputId, inputMode in getInputModes(opcode).items():
        if inputId not in newData:
            if inputMode in ["block-only", "script"]:
                newData[inputId] = {
                    "mode"      : inputMode,
                    "references": [],
                    "listBlock" : None,
                    "text"      : None,
                }
            elif opcode == "polygon" and inputId in ["x4", "y4"]:
                newData[inputId] = {
                    "mode"      : inputMode,
                    "references": [],
                    "listBlock" : None,
                    "text"      : inputTextDefault,
                }
            else:
                raise Exception(inputMode)
    return newData

def prepareOptions(data, opcode):
    newData = {}
    for optionId, optionData in data.items():
        newOptionId = getOptimizedOptionId(
            optionId=optionId,
            opcode=opcode,
        )
        newData[newOptionId] = optionData[0]
    return newData

def prepareListBlock(data, blockId, commentDatas):
    # A variable or list block
    if data[0] == 12: # A magic value
        newData = {
            "opcode": getOptimizedOpcode(opcode="special_variable_value"),
            "inputs": {},
            "options": {"VARIABLE": data[1]},
            "_info_"      : {
                "position": None,
                "next"    : None,
                "topLevel": False,
            },
        }
    elif data[0] == 13: # A magic value
        newData = {
            "opcode": getOptimizedOpcode(opcode="special_list_value"),
            "inputs": {},
            "options": {"LIST": data[1]},
            "_info_"      : {
                "position": None,
                "next"    : None,
                "topLevel": False,
            },
        }
    if len(data) > 3:
        newData["_info_"]["position"] = data[3:5]
        newData["_info_"]["topLevel"] = True
    
    # Get the comment attached to the block
    blockCommentData = None
    for commentData in commentDatas.values():
        if commentData["_info_"]["block"] == blockId:
            blockCommentData = commentData
            break
    if blockCommentData is not None:
        newData["comment"] = blockCommentData
        
    return newData

def getCustomBlockMutations(data):
    mutationDatas = {}
    for blockData in data.values():
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
    return mutationDatas
