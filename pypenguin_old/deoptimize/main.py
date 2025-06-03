from pypenguin_old.utility import BlockSelector, string_to_sha256, Platform, pformat, pp, writeJSONFile, readJSONFile, ensureCorrectPath

from pypenguin_old.deoptimize.variables_lists import translateVariables, translateLists
from pypenguin_old.deoptimize.blocks_scripts import prepareScripts, flattenScripts, restoreBlocks, unprepareBlocks, makeJsonCompatible, standardizeScripts, removeTemporaryAttrs
from pypenguin_old.deoptimize.broadcasts import generateBroadcasts
from pypenguin_old.deoptimize.costumes_sounds import translateCostumes, translateSounds
from pypenguin_old.deoptimize.comments import translateComment
from pypenguin_old.deoptimize.monitors import translateMonitor
from pypenguin_old.deoptimize.scratch_adaption import adaptProject
from pypenguin_old.deoptimize.precompilation import exportBlocks, findMatchingScript
from pypenguin_old.database import deoptimizeOptionValue

import os

def translateVariablesLists(data):
    spriteNames = [sprite["name"] for sprite in data["sprites"]][1:]
    translatedVariableDatas = translateVariables(
        data=data, 
        spriteNames=spriteNames,
    )
    translatedListDatas = translateLists(
        data=data, 
        spriteNames=spriteNames,
    )
    return translatedVariableDatas, translatedListDatas

def deoptimizeProject(projectData, targetPlatform):
    precompiledFilePath = ensureCorrectPath("precompiled.json", "pypenguin_old")
    if os.path.exists(precompiledFilePath):
        precompiledScriptDatas = readJSONFile(precompiledFilePath)
    else:
        precompiledScriptDatas = []
    translatedVariableDatas, translatedListDatas = translateVariablesLists(data=projectData)    
    broadcastDatas = generateBroadcasts(data=projectData["sprites"])
    
    newSpriteDatas  = []
    exportedScriptDatas = []
    for i, spriteData in enumerate(projectData["sprites"]):
        spriteName = None if spriteData["isStage"] else spriteData["name"]
        standardizedScriptDatas    = standardizeScripts(spriteData["scripts"])
        unfinishedScriptDatas      = [] # The scripts that couldn't be precompiled
        finalBlockDatas            = {} # The blocks of the precompiled or converted scripts
        finalCommentDatas          = {} # The comments of the precompiled or converted scripts
        
        for scriptData in standardizedScriptDatas:
            precompiledBlockDatas, precompiledCommentDatas, usedScriptData = findMatchingScript(scriptData, precompiledScriptDatas, spriteName=spriteName)
            #print(100*"*")
            if precompiledBlockDatas is None:
                unfinishedScriptDatas.append(scriptData)
                #print("MANUAL", scriptData)
            else:
                finalBlockDatas           |= precompiledBlockDatas
                finalCommentDatas         |= precompiledCommentDatas
                exportedScriptDatas.append(usedScriptData)
                #print("PRECOMP", scriptData)
                    
        preparedScriptDatas = prepareScripts(unfinishedScriptDatas, context={
            "costumes" : [item["name"] for item in spriteData               ["costumes"]],
            "backdrops": [item["name"] for item in projectData["sprites"][0]["costumes"]],
        })
        flattendScriptDatas = flattenScripts(preparedScriptDatas)
        newBlockDatas, scriptCommentDatas = restoreBlocks(
            data=flattendScriptDatas,
            spriteName=spriteName,
        )
        newCommentDatas    = scriptCommentDatas
        finalCommentDatas |= scriptCommentDatas
        
        for i, commentData in enumerate(spriteData["comments"]):
            commentId = BlockSelector()
            newCommentData = translateComment(
                data=commentData,
                id=None,
            ) 
            newCommentDatas  [commentId] = newCommentData
            finalCommentDatas[commentId] = newCommentData
        
        unpreparedBlockDatas = unprepareBlocks(
            data=newBlockDatas,
        )
        finalBlockDatas |= unpreparedBlockDatas
        compatibleBlockDatas, compatibleCommentDatas = makeJsonCompatible(
            data=finalBlockDatas,
            commentDatas=finalCommentDatas,
            targetPlatform=targetPlatform,
        )
        
        exportedScriptDatas += exportBlocks(
            data=unpreparedBlockDatas, 
            commentDatas=newCommentDatas, 
            optimizedScriptDatas=unfinishedScriptDatas,
        )

        removeTemporaryAttrs(compatibleBlockDatas)
                
        newCostumeDatas = translateCostumes(
            data=spriteData["costumes"],
        )
        newSoundDatas = translateSounds(
            data=spriteData["sounds"],
        )

        if i == 0:
            token = string_to_sha256("_stage_")
        else:
            token = string_to_sha256(spriteData["name"])
        
        
        newSpriteData = {
            "isStage"       : spriteData["isStage"],
            "name"          : spriteData["name"],
            "variables"     : translatedVariableDatas[spriteName],
            "lists"         : translatedListDatas    [spriteName],
            "broadcasts"    : {},
            "customVars"    : [], # NO MEANING FOUND
            "blocks"        : compatibleBlockDatas,
            "comments"      : compatibleCommentDatas,
            "currentCostume": spriteData["currentCostume"],
            "costumes"      : newCostumeDatas,
            "sounds"        : newSoundDatas,
            "id"            : token,
            "volume"        : spriteData["volume"],
        }
        if spriteData["isStage"]:
            if projectData.get("textToSpeechLanguage", None) is None:
                newTextToSpeechLanguage = None
            else:
                newTextToSpeechLanguage = deoptimizeOptionValue(
                    optionType="text to speech language",
                    optionValue=["value", projectData["textToSpeechLanguage"]]
                ) # eg. "English (en)" -> "en"
            newSpriteData |= {
                "broadcasts"          : broadcastDatas,
                "layerOrder"          : 0,
                "tempo"               : projectData.get("tempo", 60),
                "videoTransparency"   : projectData.get("videoTransparency", 50),
                "videoState"          : projectData.get("videoState", "on"),
                "textToSpeechLanguage": newTextToSpeechLanguage,
            }
        else:
            newSpriteData |= {
                "visible"      : spriteData["visible"],
                "x"            : spriteData["position"][0],
                "y"            : spriteData["position"][1],
                "size"         : spriteData["size"],
                "direction"    : spriteData["direction"],
                "draggable"    : spriteData["draggable"],
                "rotationStyle": spriteData["rotationStyle"],
                "layerOrder"   : spriteData["layerOrder"],
            }
        newSpriteDatas.append(newSpriteData)
    
    #writeJSONFile("precompiled.json", exportedScriptDatas)    
    
    # Translate monitors
    newMonitorDatas = []
    for monitorData in projectData["monitors"]:
        newMonitorDatas.append(translateMonitor(data=monitorData))

    newProjectData = {
        "targets"      : newSpriteDatas,
        "monitors"     : newMonitorDatas,
        "extensionData": projectData.get("extensionData", {}),
        "extensions"   : projectData["extensions"],    
        "extensionURLs": projectData.get("extensionURLs", {}),
        "meta"         : {
            "semver": "3.0.0",
            "vm"    : "0.2.0",
            "agent" : "",
            "platform": {
                "name"   : "PenguinMod",
                "url"    : "https://penguinmod.com/",
                "version": "stable",
            },
        }, # Hardcoded because there is no use in changing it
        "credit": "Made using https://github.com/Fritzforcode/pypenguin_old",
    }
    if targetPlatform == Platform.SCRATCH:
        newProjectData = adaptProject(newProjectData)
    return newProjectData
    
