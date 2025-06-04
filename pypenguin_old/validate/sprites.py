from pypenguin_old.database import defaultCostume
from pypenguin_old.validate.errors import spriteNameError, layerOrderError, equalCostumeName, equalSoundName, currentCostumeError, doubleCustomBlockDefinitionError
from pypenguin_old.validate.constants import validateSchema, formatError, stageSchema, spriteSchema
from pypenguin_old.validate.costumes_sounds import validateCostume, validateSound
from pypenguin_old.validate.blocks_scripts import validateScript, validateScriptCustomBlocks
from pypenguin_old.validate.comments import validateComment

def validateSprite(path, data, context):
    i = path[-1]
    if i == 0: # If it should be the stage
        # Check stage format
        validateSchema(pathToData=path, data=data, schema=stageSchema)
        if data["name"] != "Stage": 
            raise formatError(spriteNameError, path+["name"], "The 'name' attribute of the stage (the first sprite) must always be 'Stage'.")
    else: # If it should be a sprite
        # Check sprite format
        validateSchema(pathToData=path, data=data, schema=spriteSchema)
        
        if data["name"] in ["_myself_", "_stage_", "_mouse_", "_edge_"]:
            raise formatError(spriteNameError, path+["name"], f"'{data['name']}' isn't a valid sprite name. Please pick another name.")
        if data["layerOrder"] < 1:
            raise formatError(layerOrderError, path+["layerOrder"], "'layerOrder' of a sprite must be at least 1.")
        
    # Check costume formats
    if len(data["costumes"]) < 1:
        data["costumes"].append(defaultCostume)
    costumeNames = []
    for j, costume in enumerate(data["costumes"]):
        validateCostume(path=path+["costumes"]+[j], data=costume, isStage=i==0)
        costumeName = ["costume", costume["name"]]
        if costumeName in costumeNames: # If a costume with the same name alredy exists
            raise formatError(equalCostumeName, path+["costumes"]+[j]+["name"], "Costume names mustn't be the same.")
        costumeNames.append(costumeName)
    
    # Check sound formats
    soundNames = []
    for j, sound in enumerate(data["sounds"]):
        validateSound(path=path+["sounds"]+[j], data=sound)
        soundName = ["sound", sound["name"]]
        if soundName in soundNames: # If a sound with the same name alredy exists
            raise formatError(equalSoundName, path+["sounds"]+[j]+["name"], "Sound names mustn't be the same.")
        soundNames.append(soundName)
    
    
    # Make sure that currentCostume refers to an existing costume
    if data["currentCostume"] >= len(data["costumes"]):
        raise formatError(currentCostumeError, path+["currentCostume"], f"Is out of range. There are only {len(data['costumes'])} costumes in this sprite, so 'currentCostume' could be at most {len(data['costumes']) - 1}.")
    
    # Check script formats
    spriteContext = context | {
        "costumes": costumeNames,
        "sounds"  : soundNames,
        "isStage" : i == 0,
    }
    
    CBTypes = {} 
    for j, script in enumerate(data["scripts"]):
        CBInfo = validateScript(
            path=path+["scripts"]+[j], 
            data=script, 
            context=spriteContext, 
        )
        if CBInfo == None:
            continue
        if CBInfo[0] in CBTypes:
            raise formatError(doubleCustomBlockDefinitionError, path+["scripts"]+[j]+[0], f"Custom block '{CBInfo[0]}' is defined twice.")
        CBTypes[CBInfo[0]] = CBInfo[1]
    
    for j, script in enumerate(data["scripts"]):
        validateScriptCustomBlocks(
            path=path+["scripts"]+[j]+["blocks"], 
            data=script["blocks"], 
            CBTypes=CBTypes
        )
        
    # Check comment formats
    for j, comment in enumerate(data["comments"]):
        validateComment(
            path=path+["comments"]+[j], 
            data=comment,
        )

    