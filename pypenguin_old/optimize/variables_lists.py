def translateVariables(data):
    newData = []
    for variableData in data["variables"].values():
        name = variableData[0]
        currentValue = variableData[1]
        if data["isStage"]:
            if len(variableData) == 3 and variableData[2] == True:
                mode = "cloud"
            else:
                mode = "global"
        else:
            mode = "local"
        if data["customVars"] != []:
            raise Exception("Wow! I have been trying to find out what 'customVars' is used for. Can you explain how you did that? Please contact me on GitHub.")
        
        newVariableData = {
            "name"        : name,
            "currentValue": currentValue,
        }
        if mode == "global":
            newVariableData["isCloudVariable"] = False
        elif mode == "cloud":
            newVariableData["isCloudVariable"] = True
        elif mode == "local":
            pass
        newData.append(newVariableData)
    return newData
    
def translateLists(data):
    newData = []
    for listData in data["lists"].values():
        name = listData[0]
        currentValue = listData[1]
        
        newListData = {
            "name"        : name,
            "currentValue": currentValue,
        }
        newData.append(newListData)
    return newData
