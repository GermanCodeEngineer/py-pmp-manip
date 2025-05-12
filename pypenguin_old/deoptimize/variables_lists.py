from pypenguin.utility import string_to_sha256


def translateVariables(data, spriteNames):
    newData = {k:{} for k in spriteNames+[None]}
    for spriteData in data["sprites"]:
        if spriteData["isStage"]:
            spriteName = None
            localVariableDatas = data["globalVariables"]
        else:
            spriteName = spriteData["name"]
            localVariableDatas = spriteData["localVariables"]
        for variableData in localVariableDatas:
            newVariableData = translateVariable(data=variableData, spriteName=spriteName)
            token = string_to_sha256(variableData["name"], secondary=spriteName)
            newData[spriteName][token] = newVariableData
    return newData

def translateVariable(data, spriteName):
    name = data["name"]
    newData = [name, data["currentValue"]]

    if spriteName is None: # stage
        if data["isCloudVariable"]: # cloud var
            newData.append(True)
    return newData

def translateLists(data, spriteNames):
    newData = {k:{} for k in spriteNames+[None]}
    for spriteData in data["sprites"]:
        if spriteData["isStage"]:
            spriteName = None
            localListDatas = data["globalLists"]
        else:
            spriteName = spriteData["name"]
            localListDatas = spriteData["localLists"]
        for listData in localListDatas:
            newListData = translateList(data=listData)
            token = string_to_sha256(listData["name"], secondary=spriteName)
            newData[spriteName][token] = newListData
    return newData

def translateList(data):
    name = data["name"]
    newData = [name, data["currentValue"]]
    
    return newData

