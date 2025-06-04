import os, shutil
import urllib.parse

from pypenguin_old.deoptimize import deoptimizeProject
from pypenguin_old.deoptimize.costumes_sounds import finalizeCostume, finalizeSound

from pypenguin_old.utility import readJSONFile, writeJSONFile, ensureCorrectPath, getUniqueFilename, generateMd5, getImageSize, getAudioInfo, Platform

from pypenguin_old.database import defaultCostumeFilePath

def compressProject(
    optimizedProjectDir     : str,
    projectFilePath         : str,
    targetPlatform          : Platform,
    deoptimizedDebugFilePath: str | None = None,
    developing              : bool = False,
):
    if developing:
        optimizedProjectDir = ensureCorrectPath(
            optimizedProjectDir, "PyPenguin",
            isDir=True,
            ensureExists=True,
            allowNone=False,
        )
        
        projectFilePath = ensureCorrectPath(
            projectFilePath, "PyPenguin",
            isDir=False,
            ensureIsValid=True,
            allowNone=False,
        )
        
        deoptimizedDebugFilePath = ensureCorrectPath(
            deoptimizedDebugFilePath, "PyPenguin",
            isDir=False,
            ensureIsValid=True,
            allowNone=True,
        )
        
    defCostumeFilePath = ensureCorrectPath(
        defaultCostumeFilePath, "PyPenguin",
    )
    
    temporaryDir = os.path.abspath(os.path.join(
        optimizedProjectDir,
        os.pardir,
        "temporary"
    )) # eg. .../folder/myProject -> .../folder/temporary
    # make sure the folder doesn't exist yet, so it won't be overwritten
    temporaryDir = getUniqueFilename(temporaryDir)
    
    # Read the optimized project.json
    optimizedData = readJSONFile(
        os.path.join(optimizedProjectDir, "project.json")
    )
    # Deoptimize the project data
    deoptimizedData = deoptimizeProject(
        projectData=optimizedData,
        targetPlatform=targetPlatform
    )
    try:
        # Make sure the temporary Dir exists and is empty
        os.makedirs(temporaryDir, exist_ok=True)
        
        # Reorganize Assets
        for i, sprite in enumerate(optimizedData["sprites"]):
            deoptimizedSprite = deoptimizedData["targets"][i]
    
            # Encode the sprite name
            if sprite["isStage"]:
                encodedSpriteName = "stage"
            else:
                encodedSpriteName = "sprite_" + urllib.parse.quote(sprite["name"])
            
            assets = deoptimizedSprite["costumes"] + deoptimizedSprite["sounds"]
            
            newCostumes = []
            newSounds   = []
            for j, asset in enumerate(assets):
                isCostume  = j in range(len(deoptimizedSprite["costumes"]))
                identifier = "costumes" if isCostume else "sounds" 
                encodedAssetName = urllib.parse.quote(asset["name"] + "." + asset["dataFormat"])
                if isCostume and asset.get("isDefault", False):
                    srcPath = defCostumeFilePath
                else:
                    srcPath = os.path.join(
                        optimizedProjectDir, 
                        encodedSpriteName, 
                        identifier, 
                        encodedAssetName,
                    )
                md5    = generateMd5(file=srcPath)
                md5ext = md5 + "." + asset["dataFormat"]
                shutil.copy(
                    src=srcPath,
                    dst=os.path.join(temporaryDir, md5ext),
                )
                
                if isCostume:
                    #width, height = getImageSize(file=srcPath)
                    newCostumes.append(finalizeCostume(
                        data=asset, 
                        md5=md5,
                        md5ext=md5ext,
                        #width=width,
                        #height=height,
                    ))
                else:
                    sampleRate, sampleCount = getAudioInfo(filePath=srcPath)
                    newSounds.append(finalizeSound(
                        data=asset, 
                        md5=md5,
                        md5ext=md5ext,
                        sampleRate=sampleRate,
                        sampleCount=sampleCount,
                    ))
            deoptimizedSprite["costumes"] = newCostumes
            deoptimizedSprite["sounds"  ] = newSounds
            
            """
            # Copy and rename costumes
            newCostumes = []
            for costume in deoptimizedSprite["costumes"]:
                encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
                if costume.get("isDefault") == True:
                    srcPath = defCostumeFilePath
                else:
                    srcPath = os.path.join(
                        optimizedProjectDir, 
                        encodedSpriteName, 
                        "costumes", 
                        encodedCostumeName
                    )
                md5    = generateMd5(file=srcPath)
                md5ext = md5 + "." + costume["dataFormat"]
                width, height = getImageSize(file=srcPath)
                shutil.copy(
                    src=srcPath,
                    dst=os.path.join(temporaryDir, md5ext),
                )
                newCostumes.append(finalizeCostume(
                    data=costume, 
                    md5=md5,
                    md5ext=md5ext,
                    #width=width,
                    #height=height,
                ))
            
            deoptimizedSprite["costumes"] = newCostumes
    
    
            
            # Copy and rename sounds
            newSounds = []
            for sound in deoptimizedSprite["sounds"]:
                encodedSoundName = urllib.parse.quote(sound["name"] + "." + sound["dataFormat"])
                srcPath = os.path.join(
                    optimizedProjectDir, 
                    encodedSpriteName, 
                    "sounds", 
                    encodedSoundName
                )
                md5    = generateMd5(file=srcPath)
                md5ext = md5 + "." + sound["dataFormat"]
                shutil.copy(
                    src=srcPath,
                    dst=os.path.join(temporaryDir, md5ext),
                )
                newSounds.append(finalizeSound(
                    data=sound, 
                    md5=md5,
                    md5ext=md5ext,
                ))
            
            deoptimizedSprite["sounds"] = newSounds
            """
        
        if deoptimizedDebugFilePath != None:
            writeJSONFile(deoptimizedDebugFilePath, data=deoptimizedData)
        
        # Write the deoptimized project.json
        writeJSONFile(
            filePath=os.path.join(temporaryDir, "project.json"),
            data=deoptimizedData,
        )
        # Make sure projectFilePath does not exist
        if os.path.exists(projectFilePath):
            os.remove(projectFilePath)
    
        # Compress the temporary Dir into a zip file
        shutil.make_archive(
            os.path.splitext(projectFilePath)[0],
            "zip",
            temporaryDir,
        )
        print("created", projectFilePath)
    
        # Change its file extension to .pmp
        os.rename(
            os.path.splitext(projectFilePath)[0] + ".zip",
            projectFilePath,
        )
    finally:
        # Delete the temporary directory, even when an error occurs
        if os.path.exists(temporaryDir):
            shutil.rmtree(temporaryDir)
    