from validate.constants import validateSchema, monitorSchema, formatError
from validate.blocks_scripts import validateOptions
from database import getDeoptimizedOpcode
from validate.errors import monitorSpriteNameError, missingMonitorAttributeError, monitorSliderRangeError

def validateMonitor(path, data, contexts):
    validateSchema(pathToData=path, data=data, schema=monitorSchema)

    opcode      = getDeoptimizedOpcode(opcode=data["opcode"])
    spriteNames = list(contexts.keys())
    if data["spriteName"] not in spriteNames:
        raise formatError(monitorSpriteNameError, path+["spriteName"], f"Must be the name of an existing sprite. Must be one of these: {spriteNames}.")
    
    context = contexts[data["spriteName"]]
    if data["spriteName"] != None: # Disallow local variables/lists for a local variable/list monitor
        context["scopeVariables"] = context["localVariables"]["sprite", (data["spriteName"])]
        context["scopeLists"    ] = context["localLists"    ]["sprite", (data["spriteName"])]

    validateOptions(
        path=path+["options"],
        data=data["options"],
        opcode=data["opcode"],
        context=context,
        inputDatas=None,
    )

    if   opcode == "special_variable_value":
        required = ["sliderMin", "sliderMax", "onlyIntegers"]
    elif opcode == "special_list_value":
        required = ["size"]
    else:
        required = []
    
    for attribute in required:
        if attribute not in data:
            raise formatError(missingMonitorAttributeError, path, f"Must have the '{attribute}' attribute.")

    if   opcode == "special_variable_value":
        if not (data["sliderMin"] <= data["sliderMax"]):
            raise formatError(monitorSliderRangeError, path, "'sliderMin' must be below 'sliderMax'.")
        if data["onlyIntegers"]:
            if not isinstance(data["sliderMin"], int):
                raise formatError(monitorSliderRangeError, path+["sliderMin"], "Must be an integer because 'onlyIntegers' is true.")
            if not isinstance(data["sliderMax"], int):
                raise formatError(monitorSliderRangeError, path+["sliderMax"], "Must be an integer because 'onlyIntegers' is true.")