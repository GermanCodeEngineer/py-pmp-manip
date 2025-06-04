import json, copy
from enum import Enum
from pypenguin_old.utility import editDataStructure, BlockSelector, LocalStringToToken, getDataAtPath, pp
from pypenguin_old.database import getBlockType

class PathConstant(Enum):
    CB_PROTOTYPE_ARGS = "CB_PROTOTYPE_ARGS"

# Groups blocks into scripts and converts them into a consistent format 
def exportBlocks(data, commentDatas, optimizedScriptDatas):
    scripts = []
    for blockSelector, blockData in copy.deepcopy(data).items():
        path = blockData["_placementPath_"]
        del blockData["_placementPath_"]
        if blockData["topLevel"]:
            del blockData["x"]
            del blockData["y"]
        scriptIndex, path = path[0], path[1:]
        pathString = json.dumps(path)
        
        while len(scripts) <= scriptIndex:
            scripts.append({"deoptimizedBlocks": {}, "deoptimizedComments": {}, "table": {}})
        
        scripts[scriptIndex]["deoptimizedBlocks"][pathString   ] = blockData
        scripts[scriptIndex]["table" ][blockSelector] = pathString

        if blockData.get("comment") != None:
            commentPathString = json.dumps(path+["comment"])
            scripts[scriptIndex]["deoptimizedComments"][commentPathString   ] = commentDatas[blockData["comment"]]
            scripts[scriptIndex]["table"   ][blockData["comment"]] = commentPathString
    
    for scriptIndex, scriptData in enumerate(scripts):
        scriptData["optimized"] = optimizedScriptDatas[scriptIndex]["blocks"]
        
        # Replace remaining block selectors with paths
        table = {selector:{"_custom_": True, "_type_": BlockSelector.__name__, "path": pathString} for selector, pathString in scriptData["table"].items()}

        def conversionFunc(obj):
            nonlocal table
            if isinstance(obj, BlockSelector):
                return table[obj]
            if isinstance(obj, LocalStringToToken):
                return obj.toJSON()
        conditionFunc = lambda obj: isinstance(obj, (BlockSelector, LocalStringToToken))
        scriptData["deoptimizedBlocks"  ] = editDataStructure(scriptData["deoptimizedBlocks"  ], conditionFunc=conditionFunc, conversionFunc=conversionFunc)
        scriptData["deoptimizedComments"] = editDataStructure(scriptData["deoptimizedComments"], conditionFunc=conditionFunc, conversionFunc=conversionFunc)
        del scriptData["table"]
    return scripts


# Loads a script 
def loadScript(data, spriteName, scriptPosition):
    blockDatas   = data["deoptimizedBlocks"  ]
    commentDatas = data["deoptimizedComments"]
    table = {itemPath: BlockSelector() for itemPath in (blockDatas|commentDatas).keys()}

    def conversionFunc(obj):
        nonlocal table, spriteName
        if obj["_type_"] == BlockSelector.__name__:
            return table[obj["path"]]
        if obj["_type_"] == LocalStringToToken.__name__:
            return LocalStringToToken(main=obj["main"], spriteName=spriteName)
        
    conditionFunc = lambda obj: (
        False if not isinstance(obj, dict) else (
            (obj.get("_custom_") == True) and ("_type_" in obj)
        )
    )
    blockDatas   = editDataStructure(blockDatas  , conditionFunc=conditionFunc, conversionFunc=conversionFunc)
    for blockData in blockDatas.values():
        if blockData["topLevel"]:
            blockData["x"], blockData["y"] = scriptPosition
            break
    
    commentDatas = editDataStructure(commentDatas, conditionFunc=conditionFunc, conversionFunc=conversionFunc)
    newBlockDatas = {}
    for blockPath, blockData in blockDatas.items():
        newBlockDatas[table[blockPath]] = blockData
    newCommentDatas = {}
    for commentPath, commentData in commentDatas.items():
        newCommentDatas[table[commentPath]] = commentData
    return newBlockDatas, newCommentDatas
    
# Takes and optimized script as input and looks for a matching precompiled script
# If exactly the same script is deoptimized for the second time, the precompiled script can be adapted and used.
def findMatchingScript(scriptData, precompiledScriptDatas, spriteName):
    scriptBlockDatas = scriptData["blocks"]
    for precompiledScriptData in precompiledScriptDatas:
        #print(100*"-")
        #pp(precompiledScriptData["optimized"])
        if scriptBlockDatas == precompiledScriptData["optimized"]:
            return (*loadScript(
                precompiledScriptData, 
                spriteName=spriteName,
                scriptPosition=scriptData["position"],
            ), precompiledScriptData)
    return None, None, None
