from pypenguin_old.utility import Platform

from pypenguin_old.optimize.costumes_sounds  import translateCostumes, translateSounds
from pypenguin_old.optimize.variables_lists  import translateVariables, translateLists
from pypenguin_old.optimize.blocks_scripts   import getCustomBlockMutations, prepareBlocks, nestScripts, finishScripts
from pypenguin_old.optimize.comments         import translateComment
from pypenguin_old.optimize.monitors         import translateMonitors
from pypenguin_old.optimize.scratch_adaption import adaptProject
from pypenguin_old.database                  import optimizeOptionValue

def optimizeProjectJSON(projectData, sourcePlatform):
    if sourcePlatform == Platform.SCRATCH:
        projectData = adaptProject(projectData)
    newSpriteDatas = []
    spriteNames    = [] # needed for monitor translation
    for i, spriteData in enumerate(projectData["targets"]):
        if i == 0: spriteNames.append(None              )
        else     : spriteNames.append(spriteData["name"])
        mutationDatas = getCustomBlockMutations(data=spriteData["blocks"])
        commentDatas = spriteData["comments"]
        floatingCommentDatas = [] # The comments that aren't connected to any blocks
        attachedCommentDatas = {}
        for commentId, commentData in commentDatas.items():
            if commentData["blockId"] == None: # No Block connection
                floatingCommentDatas.append(translateComment(data=commentData))
            else:
                attachedCommentDatas[commentId] = translateComment(data=commentData)
        
        preparedBlockDatas = prepareBlocks(
            data=spriteData["blocks"], 
            commentDatas=attachedCommentDatas,
            mutationDatas=mutationDatas,
        )
        nestedScriptDatas  = nestScripts  (data=preparedBlockDatas)
        newScriptDatas     = finishScripts(data=nestedScriptDatas)

        translatedCostumeDatas  = translateCostumes (data=spriteData["costumes"])
        translatedSoundDatas    = translateSounds   (data=spriteData["sounds"])
        translatedVariableDatas = translateVariables(data=spriteData)
        translatedListDatas     = translateLists    (data=spriteData)
        newSpriteData = {
            "isStage"       : i == 0,
            "name"          : spriteData["name"],
            "scripts"       : newScriptDatas,
            "comments"      : floatingCommentDatas,
            "currentCostume": spriteData["currentCostume"],
            "costumes"      : translatedCostumeDatas,
            "sounds"        : translatedSoundDatas,
            "volume"        : spriteData["volume"],
        }
        if spriteData["isStage"]:
            globalVariableDatas = translatedVariableDatas
            globalListDatas = translatedListDatas
        else:
            newSpriteData |= {
                "localVariables": translatedVariableDatas,
                "localLists"    : translatedListDatas,
                "layerOrder"    : spriteData["layerOrder"],
                "visible"       : spriteData["visible"],
                "position"      : [spriteData["x"], spriteData["y"]],
                "size"          : spriteData["size"],
                "direction"     : spriteData["direction"],
                "draggable"     : spriteData["draggable"],
                "rotationStyle" : spriteData["rotationStyle"],
            }
        newSpriteDatas.append(newSpriteData)
    stageData = projectData["targets"][0]
    newMonitorDatas = translateMonitors(
        data=projectData["monitors"],
        spriteNames=spriteNames,
    )
    if stageData["textToSpeechLanguage"] == None:
        newTextToSpeechLanguage = None
    else:
        newTextToSpeechLanguage = optimizeOptionValue(
            optionType="text to speech language",
            optionValue=stageData["textToSpeechLanguage"],
        )[1] # eg. "en" -> "English (en)"
    newData = {
        "sprites"             : newSpriteDatas,
        "globalVariables"     : globalVariableDatas,
        "globalLists"         : globalListDatas,
        "tempo"               : stageData["tempo"], # I moved these from the stage to the project because they influence the whole project
        "videoTransparency"   : stageData["videoTransparency"],
        "videoState"          : stageData["videoState"],
        "textToSpeechLanguage": newTextToSpeechLanguage,

        "monitors"            : newMonitorDatas,
        "extensionData"       : projectData["extensionData"],
        "extensions"          : projectData["extensions"],
        "credit"              : "Made using https://github.com/Fritzforcode/PyPenguin"
    }
    if projectData.get("extensionURLs", {}) != {}:
        newData["extensionURLs"] = projectData["extensionURLs"]
    return newData
    