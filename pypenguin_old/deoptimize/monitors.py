from pypenguin.utility import string_to_sha256
from pypenguin.database import getDeoptimizedOpcode, getDeoptimizedOptionId

def translateMonitor(data):
    opcode = getDeoptimizedOpcode(opcode=data["opcode"])
    if   opcode == "special_variable_value":
        opcode = "data_variable"
    elif opcode == "special_list_value":
        opcode = "data_listcontents"
    newOptionDatas = {}
    for optionId, optionData in data["options"].items():
        if   opcode == "data_variable":
            newOptionId = "VARIABLE"
        elif opcode == "data_listcontents":
            newOptionId = "LIST"
        else:
            newOptionId = getDeoptimizedOptionId(
                opcode=opcode,
                optionId=optionId,
            )
        newOptionDatas[newOptionId] = optionData

    opcodeMainPart     = "_".join(opcode.split("_")[1:]) # e.g. "motion_xposition" -> "xposition"

    if data["spriteName"] is None:
        spriteToken = string_to_sha256("_stage_")
    else:
        spriteToken = string_to_sha256(data["spriteName"])

    match opcode:
        case "motion_xposition"|"motion_yposition"|"motion_direction"|"looks_sayWidth"|"looks_sayHeight"|"looks_stretchGetX"|"looks_stretchGetY"|"looks_getSpriteVisible"|"getSpriteVisible"|"looks_layersGetLayer"|"looks_size"|"looks_tintColor"|"sound_volume"|"sensing_getdragmode":
            behaviour = 1
        case "looks_getEffectValue"|"looks_costumenumbername"|"sound_getEffectValue":
            behaviour = 2
            parameter = list(data["options"].values())[0]
        case "looks_backdropnumbername":
            behaviour = 3
            parameter = list(data["options"].values())[0]
        case "sensing_current":
            behaviour = 4
            parameter = list(data["options"].values())[0]
        case "sensing_answer"|"sensing_loudness"|"sensing_loud"|"sensing_timer":
            behaviour = 5
        case "sensing_mousedown"|"sensing_mouseclicked"|"sensing_mousex"|"sensing_mousey"|"sensing_getclipboard"|"sensing_dayssince2000"|"sensing_username"|"sensing_loggedin":
            behaviour = 6
        case "data_variable":
            behaviour = "variable"
            parameter = list(data["options"].values())[0]
        case "data_listcontents":
            behaviour = "list"
            parameter = list(data["options"].values())[0]
        case _: raise Exception(opcode)
    
    match behaviour:
        case 1:
            id = f"{spriteToken}_{opcodeMainPart}"
        case 2:
            id = f"{spriteToken}_{opcodeMainPart}_{parameter}"
        case 3:
            id =               f"{opcodeMainPart}_{parameter}"
        case 4:
            id =               f"{opcodeMainPart}_{parameter.lower()}"
        case 5:
            id =               f"{opcodeMainPart}"
        case 6:
            id =               f"{opcode}"
        case "variable":
            id = string_to_sha256(parameter, secondary=data["spriteName"])
        case "list":
            id = string_to_sha256(parameter, secondary=data["spriteName"])

    if opcode == "data_listcontents": width, height = data["size"]
    else                            : width, height = [0, 0]
    
    newData = {
        "id"        : id,
        "mode"      : "list" if opcode=="data_listcontents" else "default",
        "opcode"    : opcode,
        "params"    : newOptionDatas,
        "spriteName": data["spriteName"],
        "value"     : []     if opcode=="data_listcontents" else 0,
        "width"     : width,
        "height"    : height,
        "x"         : data["position"][0],
        "y"         : data["position"][1],
        "visible"   : data["visible"],
    }
    if   opcode == "data_variable":
        newData |= {
            "sliderMin" : data["sliderMin"],
            "sliderMax" : data["sliderMax"],
            "isDiscrete": data["onlyIntegers"],
        }
    elif opcode == "data_listcontents":
        pass
    else:
        newData |= {
            "sliderMin" : 0,
            "sliderMax" : 100,
            "isDiscrete": True,
        }
    return newData
