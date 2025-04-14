from pypenguin.database import getOptimizedOpcode, getOptimizedOptionId, optimizeOptionValue, getOptionType

def translateMonitors(data, spriteNames):
    newMonitorDatas = []
    for monitorData in data:
        opcode = monitorData["opcode"]
        if   opcode == "data_variable":
            newOpcode = getOptimizedOpcode(opcode="special_variable_value")
        elif opcode == "data_listcontents":
            newOpcode = getOptimizedOpcode(opcode="special_list_value")
        else:
            newOpcode = getOptimizedOpcode(opcode=opcode)
        
        newOptionDatas = {}
        paramDatas = {} if monitorData["params"]==None else monitorData["params"]
        for optionId, optionData in paramDatas.items():
            if   opcode == "data_variable":
                newOptionId = "VARIABLE"
                optionType  = "variable"
            elif opcode == "data_listcontents":
                newOptionId = "LIST"
                optionType  = "list"
            else:
                newOptionId = getOptimizedOptionId(
                    opcode=opcode,
                    optionId=optionId,
                )
                optionType = getOptionType(
                    opcode=opcode, 
                    optionId=optionId
                )
            newOptionData = optimizeOptionValue(
                optionValue=optionData,
                optionType=optionType,
            )
            newOptionDatas[newOptionId] = newOptionData

        newMonitorData = {
            "opcode"    : newOpcode,
            "options"   : newOptionDatas,
            "spriteName": monitorData["spriteName"],
            "position"  : [monitorData["x"], monitorData["y"]],
            "visible"   : monitorData["visible"],
        }
        if opcode == "data_variable":
            newMonitorData["sliderMin"] = monitorData["sliderMin"]
            newMonitorData["sliderMax"] = monitorData["sliderMax"]
            newMonitorData["onlyIntegers"] = monitorData["isDiscrete"]
        elif opcode == "data_listcontents":
            newMonitorData["size"] = [monitorData["width"], monitorData["height"]]
        if (newMonitorData["spriteName"] not in spriteNames) and not(newMonitorData["visible"]):
            continue
        newMonitorDatas.append(newMonitorData)

    return newMonitorDatas
