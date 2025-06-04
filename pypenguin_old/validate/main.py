from pypenguin_old.validate.constants import validateSchema, formatError, projectSchema
from pypenguin_old.validate.errors import doubleVariableDefinitionError, doubleListDefinitionError, equalSpriteNameError
from pypenguin_old.validate.variables_lists import validateVariable, validateList
from pypenguin_old.validate.sprites import validateSprite
from pypenguin_old.validate.monitors import validateMonitor
from pypenguin_old.database import defaultCostume
import copy

def validateProject(projectData):
    projectDataCopy = copy.deepcopy(projectData)
    # Check project format
    validateSchema(pathToData=[], data=projectDataCopy, schema=projectSchema)
    
    # Check variable formats
    errorMessage = "Variable names mustn't be the same. Please check 'globalVariables' and 'localVariables' of the same sprite."
    globalVariableNames = []
    for j, variable in enumerate(projectDataCopy["globalVariables"]):
        validateVariable(path=["globalVariables"]+[j], data=variable, isGlobal=True)
        variableName = variable["name"]
        if variableName in globalVariableNames: # if var name alredy exists globally
            raise formatError(doubleVariableDefinitionError, ["globalVariables"]+[j]+["name"], errorMessage)
    
    localVariableNames = [[] for i in range(  len( projectDataCopy["sprites"][1:] )  )]
    for i, sprite in enumerate(projectDataCopy["sprites"][1:]):
        if not isinstance(sprite.get("localVariables"), list): continue
        for j, variable in enumerate(sprite["localVariables"]):
            validateVariable(path=["sprites"]+[i]+["localVariables"]+[j], data=variable, isGlobal=False)
            variableName = variable["name"]
            if variableName in globalVariableNames or variableName in localVariableNames[i]: # if var name alredy exists globally or in the same sprite
                raise formatError(doubleVariableDefinitionError, ["sprites"]+[i]+["localVariables"]+[j]+["name"], errorMessage)
    
    
    errorMessage = "List names mustn't be the same. Please check 'globalLists' and 'localLists' of the same sprite."
    globalListNames = []
    for j, list_ in enumerate(projectDataCopy["globalLists"]):
        validateList(path=["globalLists"]+[j], data=list_)
        listName = list_["name"]
        if listName in globalListNames: # if list name alredy exists globally
            raise formatError(doubleListDefinitionError, ["globalLists"]+[j]+["name"], errorMessage)
    
    localListNames = [[] for i in range(  len( projectDataCopy["sprites"][1:] )  )]
    for i, sprite in enumerate(projectDataCopy["sprites"][1:]):
        if not isinstance(sprite.get("localLists"), list): continue
        for j, list_ in enumerate(sprite["localLists"]):
            validateList(path=["sprites"]+[i]+["localLists"]+[j], data=list_)
            listName = list_["name"]
            if listName in globalListNames or listName in localListNames[i]: # if list name alredy exists globally or in the same sprite
                raise formatError(doubleListDefinitionError, ["sprites"]+[i]+["localLists"]+[j]+["name"], errorMessage)
    

    # Check sprite formats
    spriteNames    = []
    localVariables = {}
    localLists     = {}
    otherSprites   = []
    for i, sprite in enumerate(projectDataCopy["sprites"]):
        if i == 0: spriteName = ["stage", "stage"]
        else:      spriteName = ["sprite", sprite["name"]]
        if spriteName in spriteNames: # If there is the same sprite name twice
            raise formatError(equalSpriteNameError, ["sprites"]+[i]+["name"], "Sprite names mustn't be the same.")
        spriteNames.append(spriteName)
        

        if i == 0:
            if not isinstance(sprite.get("costumes"), list):
                backdrops = None #An error will be raised later
            else:
                backdrops = [["costume", costume["name"]] for costume in sprite["costumes"]]
                if sprite["costumes"] == []:
                    backdrops.insert(0, ["costume", defaultCostume["name"]])
        else:
            otherSprites.append(spriteName)
            if not isinstance(sprite.get("localVariables"), list):
                localVariables[tuple(spriteName)] = None #An error will be raised later
            else:
                localVariables[tuple(spriteName)] = [["variable", item["name"]] for item in sprite["localVariables"]]
            if not isinstance(sprite.get("localLists"), list):
                localLists    [tuple(spriteName)] = None #An error will be raised later
            else:
                localLists    [tuple(spriteName)] = [["list"    , item["name"]] for item in sprite["localLists"    ]]
    
    contexts = {}
    for i, sprite in enumerate(projectDataCopy["sprites"]):
        scopeVariables    = [["variable", item["name"]] for item in projectDataCopy["globalVariables"]]
        scopeLists        = [["list"    , item["name"]] for item in projectDataCopy["globalLists"    ]]
        if i == 0:
            nameKey           = None
        else:
            nameKey           = sprite["name"]
            if not isinstance(sprite.get("localVariables"), list):
                scopeVariables = None
            else:
                scopeVariables += [["variable", item["name"]] for item in sprite["localVariables"]]
            if not isinstance(sprite.get("localLists"    ), list):
                scopeLists     = None
            else:
                scopeLists     += [["list"    , item["name"]] for item in sprite["localLists"    ]]

        context = {
            "scopeVariables" : scopeVariables, 
            "scopeLists"     : scopeLists, 
            "globalVariables": [["variable", item["name"]] for item in projectDataCopy["globalVariables"]],
            "localVariables" : localVariables,
            "localLists"     : localLists,
            "otherSprites": [
                target for target in otherSprites if target[1] != sprite["name"]
            ],
            "backdrops": backdrops,
        }
        validateSprite(path=["sprites"]+[i], data=sprite, context=context)
        contexts[nameKey] = context

    for i, monitorData in enumerate(projectDataCopy["monitors"]):
        validateMonitor(
            path=["monitors"]+[i], 
            data=monitorData, 
            contexts=contexts
        )
