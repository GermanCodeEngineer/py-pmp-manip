from pypenguin_old.utility import removeDuplicates, stringToToken

from pypenguin_old.database import inputDefault, inputTextDefault, optionDefault, deoptimizeOptionValue, getDeoptimizedOpcode, getInputType, getOptionType


def findBlockBroadcastMessages(data):
    opcode = getDeoptimizedOpcode(data["opcode"])
    broadcastMessages = []
    
    if "inputs" not in data:
        data["inputs"] = inputDefault
    for inputId, inputData in data["inputs"].items():
        if opcode == "procedures_call":
            continue
        if getInputType(opcode, inputId) == "broadcast":
            if "text" not in inputData:
                if "option" in inputData:
                    inputData["text"] = inputData["option"]
                else: 
                    inputData["text"] = inputTextDefault
            if inputData["text"] not in broadcastMessages:
                broadcastMessages.append(inputData["text"])

        if "block" in inputData:
            if inputData["block"] != None:
                broadcastMessages += findBlockBroadcastMessages(data=inputData["block"])
    
    if "options" not in data:
        data["options"] = optionDefault
    for optionId, optionData in data["options"].items():
        if getOptionType(opcode=opcode, optionId=optionId) == "broadcast":
            if optionData not in broadcastMessages:
                broadcastMessages.append(optionData)
    return broadcastMessages

def generateBroadcasts(data):
    broadcastMessages = []
    for spriteData in data:
        for scriptData in spriteData["scripts"]:
            for blockData in scriptData["blocks"]:
                broadcastMessages += findBlockBroadcastMessages(data=blockData)
    broadcastMessages = removeDuplicates(broadcastMessages) # Remove duplicates
    newDatas = {}
    for broadcastMessage in broadcastMessages:
        broadcastMessage = deoptimizeOptionValue(
            optionValue=broadcastMessage,
            optionType="broadcast",
        )
        newDatas[broadcastMessage] = stringToToken(broadcastMessage)
    # Because all broadcast messages are for all sprites (None=Stage)
    return newDatas
