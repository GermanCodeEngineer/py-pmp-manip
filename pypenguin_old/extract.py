from pypenguin_old.optimize import optimizeProjectJSON

import urllib.parse
import os, shutil, zipfile

from pypenguin_old.utility import readJSONFile, writeJSONFile, ensureCorrectPath, getUniqueFilename, ensureEmptyDir, getImageSize, Platform

def extractProject(
    projectFilePath         : str,
    optimizedProjectDir     : str,
    sourcePlatform          : Platform,
    deoptimizedDebugFilePath: str | None = None,
    optimizedDebugFilePath  : str | None = None,
    developing              : bool = False,
):
    if developing:
        projectFilePath = ensureCorrectPath(
            projectFilePath, "PyPenguin",
            isDir=False,
            ensureExists=True,
            allowNone=False,
        )
        
        optimizedProjectDir = ensureCorrectPath(
            optimizedProjectDir, "PyPenguin",
            isDir=True,
            ensureIsValid=True,
            allowNone=False,
        )
        
        deoptimizedDebugFilePath = ensureCorrectPath(
            deoptimizedDebugFilePath, "PyPenguin",
            isDir=False,
            ensureIsValid=True,
            allowNone=True,
        )
        
        optimizedDebugFilePath = ensureCorrectPath(
            optimizedDebugFilePath, "PyPenguin",
            isDir=False,
            ensureIsValid=True,
            allowNone=True,
        )
    
    temporaryDir = os.path.abspath(os.path.join(
        optimizedProjectDir,
        os.pardir,
        "temporary"
    )) # eg. .../folder/myProject -> .../folder/temporary
    # make sure the folder doesn't exist yet, so it won't be overwritten
    temporaryDir = getUniqueFilename(temporaryDir)
    
    try:
        # Extract the PenguinMod project
        with zipfile.ZipFile(projectFilePath, 'r') as zip_ref:
            zip_ref.extractall(temporaryDir)
        
        # Read the deoptimized project.json
        deoptimizedData = readJSONFile(
            os.path.join(temporaryDir, "project.json")
        )
        
        if deoptimizedDebugFilePath != None:
            writeJSONFile(
                deoptimizedDebugFilePath, 
                data=readJSONFile(os.path.join(temporaryDir, "project.json")),
            )
    
        # Optimize project.json
        optimizedData = optimizeProjectJSON(
            projectData=deoptimizedData,
            sourcePlatform=sourcePlatform,
        )
        
        # Make sure the project dir exists and is empty
        ensureEmptyDir(optimizedProjectDir)
        
        # Reorganize Assets
        for i, sprite in enumerate(optimizedData["sprites"]):
            deoptimizedSprite  = deoptimizedData["targets"][i]
            # Encode the sprite name
            if sprite["isStage"]:
                encodedSpriteName = "stage"
            else:
                encodedSpriteName = "sprite_" + urllib.parse.quote(sprite["name"])
        
            # Make sure the sprite dir has the costumes dir
            os.makedirs(
                os.path.join(
                    optimizedProjectDir,
                    encodedSpriteName,
                    "costumes",
                ), 
                exist_ok=True
            )
            
            # Make sure the sprite dir has the sounds dir
            os.makedirs(
                os.path.join(
                    optimizedProjectDir,
                    encodedSpriteName,
                    "sounds",
                ), 
                exist_ok=True
            )
            
            assets = sprite["costumes"] + sprite["sounds"]
            
            newCostumes = []
            newSounds   = []
            
            for j, asset in enumerate(assets):
                isCostume        = j in range(len(sprite["costumes"]))
                identifier       = "costumes" if isCostume else "sounds"
                offset           = 0 if isCostume else len(sprite["costumes"])
                deoptimizedAsset = deoptimizedSprite[identifier][j-offset]
                oldAssetName     = deoptimizedAsset["assetId"] + "." + asset["extension"]
                encodedAssetName = urllib.parse.quote(asset["name"] + "." + asset["extension"])
                srcPath = os.path.join(temporaryDir, oldAssetName)
                destPath = os.path.join(
                    optimizedProjectDir, 
                    encodedSpriteName, 
                    identifier, 
                    encodedAssetName,
                )
                print(srcPath, destPath)
                shutil.copy(
                    src=srcPath,
                    dst=destPath
                )
                if isCostume:
                #    width, height = getImageSize(file=srcPath)
                #    newCostumes.append(finalizeCostume(
                #        data=costume,
                #        width=width,
                #        height=height,
                #    ))
                    newCostumes.append(asset) # currently not changed
                else:
                    newSounds  .append(asset) # currently not changed
                
                
            sprite["costumes"] = newCostumes
            sprite["sounds"  ] = newSounds
            """
            # Copy and rename costumes
            newCostumes = []
            for j, costume in enumerate(sprite["costumes"]):
                deoptimizedCostume = deoptimizedSprite["costumes"][j]
                oldCostumeName     = deoptimizedCostume["assetId"] + "." + costume["extension"]
                encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["extension"])
                srcPath = os.path.join(temporaryDir, oldCostumeName)
                destPath = os.path.join(
                    optimizedProjectDir, 
                    encodedSpriteName, 
                    "costumes", 
                    encodedCostumeName
                )
                #width, height = getImageSize(file=srcPath)
                shutil.copy(
                    src=srcPath,
                    dst=destPath
                )
                #newCostumes.append(finalizeCostume(
                #    data=costume,
                #    width=width,
                #    height=height,
                #))
                newCostumes.append(costume)
            sprite["costumes"] = newCostumes           
            
            # Copy and rename sounds            
            for j, sound in enumerate(sprite["sounds"]):
                deoptimizedSound = deoptimizedSprite["sounds"][j]
                oldSoundName     =      deoptimizedSound["assetId"] + "." + sound["extension"]
                encodedSoundName = urllib.parse.quote(sound["name"] + "." + sound["extension"])
                srcPath = os.path.join(temporaryDir, oldSoundName)
                destPath = os.path.join(
                    optimizedProjectDir, 
                    encodedSpriteName, 
                    "sounds", 
                    encodedSoundName
                )
                shutil.copy(
                    src=srcPath,
                    dst=destPath
                )
            """
        
        if optimizedDebugFilePath != None:
            writeJSONFile(optimizedDebugFilePath, data=optimizedData)
    
            
        # Add the optimized project.json
        writeJSONFile(
            filePath=os.path.join(optimizedProjectDir, "project.json"), 
            data=optimizedData,
        )
    finally:
        # Remove the temporary directory, even when an error happens
        if os.path.exists(temporaryDir):
            shutil.rmtree(temporaryDir)
    return optimizedData
