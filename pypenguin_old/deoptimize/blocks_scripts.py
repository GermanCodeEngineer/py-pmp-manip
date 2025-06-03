import json, copy

from pypenguin_old.utility import numberToLiteral, BlockSelector, generateRandomToken, parseCustomOpcode, string_to_sha256, LocalStringToToken, Platform, getSelectors, editDataStructure, removeDuplicates, pp
from pypenguin_old.deoptimize.options import translateOptions
from pypenguin_old.deoptimize.comments import translateComment
from pypenguin_old.database import *

def standardizeScripts(data):
    pp(data)
    def standardizeBlock(data):
        opcode = getDeoptimizedOpcode(opcode=data["opcode"])
        if opcode == "procedures_call":
            proccode, arguments = parseCustomOpcode(customOpcode=data["options"]["customOpcode"][1])
        newInputDatas = {}
        for inputId, inputData in data.get("inputs", {}).items():
            if opcode == "procedures_call":
                argument  = arguments[inputId]
                if   argument == str:
                    inputType = "text"
                    inputMode = "block-and-text"
                elif argument == bool:
                    inputType = "boolean"
                    inputMode = "block-only"
            else:
                inputType = getInputType(
                    opcode=opcode, 
                    inputId=inputId,
                )
                inputMode = getInputMode(
                    opcode=opcode, 
                    inputId=inputId,
                )
            inputData["mode"] = inputMode
        
            if   inputMode in ["block-and-text", "block-and-menu-text"]:
                required = ["block", "text"]
            elif inputMode == "block-only":
                required = ["block"]
            elif inputMode in ["block-and-option", "block-and-broadcast-option"]:
                required = ["block", "option"]
            elif inputMode == "script":
                required = ["blocks"]
            
            for attribute in required:
                match attribute:
                    case "block":
                        if attribute in inputData:
                            inputData["block"] = standardizeBlock(inputData["block"])
                        else:
                            inputData["block"] = inputBlockDefault
                    case "text":
                        if attribute not in inputData:
                            if inputType == "note":
                                inputData["text"] = noteInputTextDefault
                            else:
                                inputData["text"] = inputTextDefault
                    case "blocks":
                        if attribute in inputData:
                            inputData["blocks"] = standardizeBlocks(inputData["blocks"])
                        else:
                            inputData["blocks"] = inputBlocksDefault
                    case "option":
                        if attribute not in inputData:
                            raise Exception()
            newInputDatas[inputId] = inputData
        
        newBlockData = {
            "opcode": data["opcode"],
            "inputs": newInputDatas,
            "options": data.get("options", {}),
            "comment": data.get("comment", None),
        }
        return newBlockData
    
    def standardizeBlocks(data):
        newBlockDatas = []
        for blockData in data:
            newBlockDatas.append(standardizeBlock(blockData))
        return newBlockDatas
        
    newScriptDatas = []
    for scriptData in data:
        newScriptDatas.append({
            "position": scriptData["position"],
            "blocks": standardizeBlocks(scriptData["blocks"]),
        })
    return newScriptDatas

def prepareScripts(data, context):
    newScriptDatas = []
    for scriptData in data:
        newBlockDatas = []
        for i, blockData in enumerate(scriptData["blocks"]):
            newBlockDatas.append(prepareBlock(
                data=blockData,
                parentOpcode=None,
                context=context,
                position=scriptData["position"] if i == 0 else None
            ))
        newScriptDatas.append({
            "position": scriptData["position"],
            "blocks"  : newBlockDatas,
        })
    return newScriptDatas

def generateMenu(data, parentOpcode, inputId):
    opcode = getDeoptimizedOpcode(opcode=parentOpcode)
    menu = getMenu(
        opcode=opcode,
        inputId=inputId,
    )
    menuOpcode = getOptimizedOpcode(opcode=menu["menuOpcode"])
    newData = {
        "opcode" : menuOpcode,
        "inputs" : {},
        "options": {
            menu["inner"]: data,
        },
    }
    return newData
    """ eg. "_mouse_" ->
    {
        "opcode": "#TOUCHING OBJECT MENU",
        "inputs": {},
        "options": {"TOUCHINGOBJECTMENU": "_mouse_"},
        "_info_": ...,
    }"""

def prepareBlock(data, parentOpcode, context, position=None, isOption=False, inputId=None):
    isMenu = False
    if isinstance(data, str):
        if not isOption: raise Exception()
        # When the block is a menu value
        data = generateMenu(
            data=data,
            parentOpcode=parentOpcode,
            inputId=inputId,
        )
        isMenu = True
    
    
    if "inputs" not in data:
        data["inputs"] = inputDefault
    if "options" not in data:
        data["options"] = optionDefault
    opcode = getDeoptimizedOpcode(opcode=data["opcode"])
    if opcode == "procedures_call":
        proccode, arguments = parseCustomOpcode(customOpcode=data["options"]["customOpcode"][1])
    
    newInputDatas = {}
    for inputId, inputData in data["inputs"].items():
        if inputData["mode"] == "block-and-broadcast-option":
            inputData["text"] = inputData["option"]
            del inputData["option"]
        if inputData["mode"] == "block-and-menu-text":
            inputData["option"] = ["value", inputData["text"]]
            del inputData["text"]
        newInputData = copy.deepcopy(inputData)
        if inputData.get("block") is not None:
            newInputData["block"]  = prepareBlock(
                data=inputData["block"],
                parentOpcode=data["opcode"],
                context=context,
            )
        if inputData.get("blocks") is not None:
            newInputData["blocks"] = [prepareBlock(
                data=subBlockData,
                parentOpcode=data["opcode"],
                context=context,
            ) for subBlockData in inputData["blocks"]]
        if inputData.get("option") is not None:
            if opcode == "procedures_call":
                inputType = "text" if arguments[inputId]==str else ("boolean" if arguments[inputId]==bool else None)
            else:
                inputType = getInputType(
                    opcode=opcode,
                    inputId=inputId,                
                )
            newOptionData = deoptimizeOptionValue(
                optionValue=inputData["option"],
                optionType=inputType,
                context=context,
            )
            newInputData["option"] = prepareBlock(
                data=newOptionData,
                parentOpcode=data["opcode"],
                context=context,
                isOption=True,
                inputId=inputId,
            ) 
        newInputDatas[inputId] = newInputData
        
    if isMenu:
        newOptionDatas = data["options"]
    else:
        newOptionDatas = {}
        for optionId, optionData in data["options"].items():
            optionType = getOptionType(
                opcode=opcode,
                optionId=optionId,
            )
            newOptionData = deoptimizeOptionValue(
                optionValue=optionData,
                optionType=optionType,
                context=context,
            )
            newOptionDatas[optionId] = newOptionData
    
    newData = data | {
        "inputs" : newInputDatas,
        "options": newOptionDatas,
        "_info_" : {
            "position": position,
            "topLevel": position is not None,
        },
    }
    return newData

def flattenScripts(data):
    newBlockDatas = {}
    for i, scriptData in enumerate(data):
        # Generate Ids for the blocks
        newBlockDatas |= flattenBlocks(
            data=scriptData["blocks"],
            placementPath=[i]+["blocks"],
        )
    return newBlockDatas

def flattenBlocks(data, placementPath, parentId=None, firstId=None):
    range_ = range(len(data))
    blockIds = [BlockSelector() for i in range_]
    if firstId is not None:
        blockIds[0] = firstId
    newBlockDatas = {}
    for i, blockData in enumerate(data):
        blockId = blockIds[i]
        if i - 1 in range_: # When the block has a upwards neighbour
            parentId = blockIds[i - 1]
        elif i == 0:
            parentId = parentId
        if i + 1 in range_: # When the block has a downwards neighbour
            nextId = blockIds[i + 1]
        else:
            nextId = None
        
        newBlockDatas |= flattenBlock(
            data=blockData,
            blockId=blockId,
            parentId=parentId,
            nextId=nextId,
            placementPath=placementPath+[i],
        )
    return newBlockDatas

def flattenBlock(data, blockId, parentId, nextId, placementPath):
    # Transform inputs
    newBlockDatas = {}
    newInputDatas = {}
    for inputId, inputData in data["inputs"].items():
        references = []
        listBlock = None
        if inputData.get("block") is not None:
            if inputData["block"]["opcode"] in [
                getOptimizedOpcode(opcode="special_variable_value"),
                getOptimizedOpcode(opcode="special_list_value"),
            ]:
                # If a list block, dont make it independent; instead use "listBlock"
                listBlock = inputData["block"]
                # Optional just in case
                listBlock["_info_"] |= {
                    "parent": blockId,
                    "next"  : None
                }
            else:
                subBlockId = BlockSelector()
                references.append(subBlockId)
                newBlockDatas |= flattenBlock(
                    data=inputData["block"],
                    placementPath=placementPath+["inputs"]+[inputId]+["block"],
                    blockId=subBlockId,
                    parentId=blockId,
                    nextId=None,
                )
        if inputData.get("blocks", []) != []:
            subBlockId = BlockSelector()
            references.append(subBlockId)
            newBlockDatas |= flattenBlocks(
                data=inputData["blocks"],
                placementPath=placementPath+["inputs"]+[inputId]+["blocks"],
                parentId=blockId,
                firstId=subBlockId,
            )
        if inputData.get("option") is not None:
            subBlockId = BlockSelector()
            references.append(subBlockId)
            newBlockDatas |= flattenBlock(
                data=inputData["option"],
                placementPath=placementPath+["inputs"]+[inputId]+["option"],
                blockId=subBlockId,
                parentId=blockId,
                nextId=None,
            )
        newInputData = {
            "mode"      : inputData["mode"],
            "references": references,
            "listBlock" : listBlock,
            "text"      : inputData.get("text"),
        }
        newInputDatas[inputId] = newInputData

    newBlockData = {
        "opcode" : data["opcode"],
        "inputs" : newInputDatas,
        "options": data["options"],
        "comment": data.get("comment"),
        "_info_" : data["_info_"] | {
            "parent"  : parentId,
            "next"    : nextId,
        },
        "_placementPath_": placementPath, #eg. 1 indicates an origin from the 1st script 
    }
    newBlockDatas[blockId] = newBlockData
    return newBlockDatas

def restoreProcedureDefinitionBlock(data, blockId, commentId):
    customOpcode        = data["options"]["customOpcode"]
    proccode, arguments = parseCustomOpcode(customOpcode=customOpcode)
    argumentIds         = []
    argumentNames       = []
    argumentDefaults    = []
    argumentBlockIds    = []
    for argumentName, argumentType in arguments.items():
        argumentIds     .append(generateRandomToken())
        argumentNames   .append(argumentName)
        # The argument reporter defaults
        argumentDefaults.append("" if argumentType==str else json.dumps(False))
        argumentBlockIds.append(BlockSelector())
    
    match data["options"]["blockType"]:
        case "instruction"    : returns, optype, opcode = False, "statement", "procedures_definition"
        case "lastInstruction": returns, optype, opcode = None , "end"      , "procedures_definition"
        case "textReporter"   : returns, optype, opcode = True , "string"   , "procedures_definition_return" 
        case "numberReporter" : returns, optype, opcode = True , "number"   , "procedures_definition_return"
        case "booleanReporter": returns, optype, opcode = True , "boolean"  , "procedures_definition_return"
    
    definitionId = blockId
    prototypeId  = BlockSelector()
    position     = data["_info_"]["position"]
    definitionData = {
        "opcode": opcode,
        "next": data["_info_"]["next"],
        "parent": None,
        "inputs": {"custom_block": [1, prototypeId]},
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": position[0],
        "y": position[1],
        "_placementPath_": data["_placementPath_"],
    }
    if commentId is not None:
        definitionData["comment"] = commentId
    prototypeData = {
        "opcode"  : "procedures_prototype",
        "next"    : None,
        "parent"  : definitionId,
        "inputs"  : { argumentIds[j]: [1, argumentBlockIds[j]] for j in range(len(argumentIds)) }, 
        "fields"  : {},
        "shadow"  : True,
        "topLevel": False,
        "mutation": {
            "tagName"         : "mutation",
            "children"        : [],
            "proccode"        : proccode,
            "argumentids"     : json.dumps(argumentIds),
            "argumentnames"   : json.dumps(argumentNames),
            "argumentdefaults": json.dumps(argumentDefaults),
            "warp"            : json.dumps(data["options"]["noScreenRefresh"]),
            "returns"         : json.dumps(returns),
            "edited"          : json.dumps(True),
            "optype"          : json.dumps(optype),
            "color"           : json.dumps(["#FF6680", "#eb3d5b", "#df2847"]),
        },
        "_placementPath_": data["_placementPath_"]+["CB_PROTOTYPE"],
    }
    newBlockDatas = {}
    newBlockDatas[definitionId] = definitionData
    newBlockDatas[prototypeId]  = prototypeData
    for j in range(len(argumentIds)):
        argumentName = argumentNames[j]
        newBlockDatas[argumentBlockIds[j]] = {
            "opcode": "argument_reporter_string_number" if argumentDefaults[j] == "" else "argument_reporter_boolean",
            "next": None,
            "parent": prototypeId,
            "inputs": {},
            "fields": {
                "VALUE": [argumentName, generateRandomToken()]
            },
            "shadow": True,
            "topLevel": False,
            "mutation": {
                "tagName": "mutation",
                "children": [],
                "color": "[\"#FF6680\",\"#eb3d5b\",\"#df2847\"]"
            },
            "_placementPath_": data["_placementPath_"]+["CB_PROTOTYPE_ARGS"]+[argumentName],
        }
    return newBlockDatas

def restoreBlocks(data, spriteName):
    newBlockDatas = {}
    newCommentDatas = {}
    for blockId, blockData in data.items():
        opcode = getDeoptimizedOpcode(opcode=blockData["opcode"])
        
        if blockData.get("comment") is None:
            newCommentId = None
        else:
            newCommentData = translateComment(
                data=blockData["comment"],
                id=blockId,
            )
            newCommentId = BlockSelector()
            newCommentDatas[newCommentId] = newCommentData
        

        if opcode in ["special_variable_value", "special_list_value"]:
            newBlockData = restoreListBlock(
                data=blockData,
                spriteName=spriteName,
            )
        elif opcode in ["special_define"]:
            newBlockData = None
            newBlockDatas |= restoreProcedureDefinitionBlock(
                data=blockData,
                blockId=blockId,
                commentId=newCommentId,
            )
        else:
            blockType = getBlockType(opcode=opcode)
            if blockType == "menu":
                hasShadow = True
            elif opcode in ["polygon"]:
                hasShadow = True
            else:
                hasShadow = False
            
            newBlockData = {
                "opcode"  : opcode,
                "next"    : blockData["_info_"]["next"],
                "parent"  : blockData["_info_"]["parent"],
                "inputs"  : restoreInputs(
                    data=blockData["inputs"],
                    opcode=opcode,
                    spriteName=spriteName,
                    blockData=blockData,
                ),
                "fields"  : translateOptions(
                    data=blockData["options"],
                    opcode=opcode,
                    spriteName=spriteName,
                ),
                "shadow"  : hasShadow,
                "topLevel": blockData["_info_"]["topLevel"],
                "_placementPath_": blockData["_placementPath_"],
            }
            if blockData["_info_"]["position"] is not None:
                position = blockData["_info_"]["position"]
                newBlockData |= {"x": position[0], "y": position[1]}
        
        if newBlockData is not None:
            if newCommentId is not None:
                newBlockData["comment"] = newCommentId
            newBlockDatas[blockId] = newBlockData
    return newBlockDatas, newCommentDatas

def restoreInputs(data, opcode, spriteName, blockData):
    newInputDatas = {}
    if opcode == "procedures_call":
        proccode, arguments = parseCustomOpcode(customOpcode=blockData["options"]["customOpcode"])
    for inputId, inputData in data.items():
        if opcode == "procedures_call":
            argument = arguments[inputId]
            if   argument == str:
                inputType = "text"
                inputMode = "block-and-text"
            elif argument == bool:
                inputType = "boolean"
                inputMode = "block-only"
        else:
            inputType = getInputType(
                opcode=opcode,
                inputId=inputId
            )
            inputMode = getInputMode(
                opcode=opcode,
                inputId=inputId
            )
        
        subBlocks     = inputData["references"]
        if inputData["listBlock"] is not None:
            subBlocks.insert(0, restoreListBlock(
                data=inputData["listBlock"],
                spriteName=spriteName,
            ))
        subBlockCount = len(subBlocks)
        match inputMode:
            case "block-and-text"|"block-and-broadcast-option":
                magicNumber = getInputMagicNumber(inputType=inputType)
                if inputMode == "block-and-broadcast-option":
                    text = inputData["text"][1]
                    token = string_to_sha256(text)
                    textData = [magicNumber, text, token]
                else:
                    textData = [magicNumber, inputData["text"]]
                if   subBlockCount == 0:
                    newInputData = [1, textData]
                elif subBlockCount == 1:
                    newInputData = [3, subBlocks[0], textData]
                textData = [magicNumber, inputData["text"]]
            case "block-only"|"script":
                if   subBlockCount == 0:
                    newInputData = None
                elif subBlockCount == 1:
                    newInputData = [2, subBlocks[0]]
            case "block-and-option"|"block-and-menu-text":
                if   subBlockCount == 1:
                    newInputData = [1, subBlocks[0]]
                elif subBlockCount == 2:
                    newInputData = [3, subBlocks[0],  subBlocks[1]]
        
        
        newInputId = getDeoptimizedInputId(
            opcode=opcode,
            inputId=inputId,
        )
        if newInputData is not None:
            newInputDatas[newInputId] = newInputData
    return newInputDatas

def restoreListBlock(data, spriteName):
    if   data["opcode"] == getOptimizedOpcode(opcode="special_variable_value"):
        magicNumber = 12
        value = data["options"]["VARIABLE"]
    elif data["opcode"] == getOptimizedOpcode(opcode="special_list_value"    ):
        magicNumber = 13
        value = data["options"]["LIST"]
    
    token = LocalStringToToken(value, spriteName=spriteName)
    newData = [magicNumber, value, token]
    if data["_info_"]["topLevel"]:
        newData += data["_info_"]["position"]
    # No _placementPath_ needed. In cases, where list blocks are not contained within other blocks, they shouldn't impact performance too much.
    return newData

def unprepareBlocks(data):
    mutationDatas = {}
    for blockData in data.values():
        if isinstance(blockData, dict):
            #print("- opcode", blockData["opcode"], repr(blockData.get("mutation", {}).get("proccode")))
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
                #mutationDatas[mutationData["proccode"].replace(" %n"," %s")] = mutationData # %n => %s for compatability
    newBlockDatas = {}
    for blockId, blockData in data.items():
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_call":
                customOpcode = blockData["fields"]["customOpcode"]
                del blockData["fields"]["customOpcode"]
                proccode, arguments = parseCustomOpcode(customOpcode=customOpcode)
                mutationData         = mutationDatas[proccode]
                #mutationData         = mutationDatas[proccode.replace(" %n"," %s")] # %n => %s for compatability
                modifiedMutationData = mutationData.copy()
                del modifiedMutationData["argumentnames"]
                del modifiedMutationData["argumentdefaults"]
                blockData["mutation"] = modifiedMutationData
        
                argumentIds   = json.loads(mutationData["argumentids"])
                argumentNames = json.loads(mutationData["argumentnames"])
                blockData["inputs"] = {
                    argumentIds[argumentNames.index(inputId)]: 
                    inputValue for inputId,inputValue in blockData["inputs"].items() 
                }

            elif blockData["opcode"] == "control_stop":
                match blockData["fields"]["STOP_OPTION"][0]:
                    case "all" | "this script"    : hasNext = False
                    case "other scripts in sprite": hasNext = True
                blockData["mutation"] = {
                    "tagName": "mutation",
                    "children": [],
                    "hasnext": json.dumps(hasNext)
                }
            
            elif blockData["opcode"] == "polygon":
                blockData["mutation"] = { # seems to alwys be constant
                    "tagName": "mutation",
                    "children": [],
                    "points": json.dumps(blockData["fields"]["VERTEX_COUNT"][0]), # TODO: research
                    "color": "#0FBD8C",
                    "midle": "[0,0]",
                    "scale": "50",
                    "expanded": "false"
                }
                del blockData["fields"]["VERTEX_COUNT"]
            newBlockDatas[blockId] = blockData
    return newBlockDatas

# Replaces block selectors with literals eg. "t"
def makeJsonCompatible(data, commentDatas, targetPlatform):  
    selectors = removeDuplicates(getSelectors(data) + getSelectors(commentDatas))
    # Translation table from selector object to literal
    if   targetPlatform == Platform.PENGUINMOD:
        table = {selector: numberToLiteral(i+1)  for i, selector in enumerate(selectors)}
    elif targetPlatform == Platform.SCRATCH:
        table = {selector: generateRandomToken() for    selector in           selectors }
    def conversionFunc(obj):
        nonlocal table
        if isinstance(obj, BlockSelector):
            return table[obj]
        if isinstance(obj, LocalStringToToken):
            return obj.toToken()
    conditionFunc = lambda obj: isinstance(obj, (BlockSelector, LocalStringToToken))
    data         = editDataStructure(data        , conditionFunc=conditionFunc, conversionFunc=conversionFunc)
    commentDatas = editDataStructure(commentDatas, conditionFunc=conditionFunc, conversionFunc=conversionFunc)
    return data, commentDatas

def removeTemporaryAttrs(data):
    for block in data.values():
        if "_placementPath_" in block:
            del block["_placementPath_"]
