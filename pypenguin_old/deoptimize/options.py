from pypenguin_old.utility import generateRandomToken, stringToToken, LocalStringToToken

from pypenguin_old.database import getOptionType, getBlockType, getDeoptimizedOptionId


def translateOptions(data, opcode, spriteName):
    blockType = getBlockType(opcode=opcode)
    if blockType == "menu":
        key = list(data.keys())[0]
        value = list(data.values())[0]
        return {key: [value, generateRandomToken()]}
    
    newData = {}
    for optionId, optionData in data.items():
        mode = getOptionType(
            opcode=opcode,
            optionId=optionId,
        )
        if mode in ["variable", "list", "broadcast"]:
            if mode == "variable":
                token = LocalStringToToken(optionData, spriteName=spriteName)
                magicString = ""
            elif mode == "list":
                token = LocalStringToToken(optionData, spriteName=spriteName)
                magicString = "list"
            elif mode == "broadcast":
                token = stringToToken(optionData)
                magicString = "broadcast_msg"
            
            newOptionData = [optionData, token, magicString]
        elif mode in ["boolean", "round", "blockType", "opcode", "customBlockId"]:
            newOptionData = optionData
        else:
            newOptionData = [optionData, generateRandomToken()]
        
        newOptionId = getDeoptimizedOptionId(
            opcode=opcode,
            optionId=optionId,
        )
        newData[newOptionId] = newOptionData
    return newData
