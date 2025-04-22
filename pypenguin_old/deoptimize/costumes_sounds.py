from pypenguin.database import defaultCostumeDeoptimized

def translateCostumes(data):
    newCostumeDatas = []
    for costumeData in data:
        newCostumeData = {
            "name"            : costumeData["name"],
            "assetId"         : None, # is replaced later
            "dataFormat"      : costumeData["extension"],
            "md5ext"          : None, # is replaced later
            "rotationCenterX" : costumeData["rotationCenter"][0], # is finalized later
            "rotationCenterY" : costumeData["rotationCenter"][1], # is finalized later
        }
        if "bitmapResolution" in costumeData:
            newCostumeData["bitmapResolution"] = costumeData["bitmapResolution"]
        newCostumeDatas.append(newCostumeData)
    if newCostumeDatas == []: # When there are no costumes
        defaultCostumeModified = defaultCostumeDeoptimized.copy() | {"isDefault": True}
        newCostumeDatas.append(defaultCostumeModified)
    return newCostumeDatas

#def finalizeCostume(data, md5, md5ext, width, height):
def finalizeCostume(data, md5, md5ext):
    # Integrate md5 hash, keep all other attributes
    newData = {
        "name"            : data["name"],
        "assetId"         : md5,
        "dataFormat"      : data["dataFormat"],
        "md5ext"          : md5ext,
        "rotationCenterX" : data["rotationCenterX"], # + width  / 2,
        "rotationCenterY" : data["rotationCenterY"], # + height / 2,
    }
    if "bitmapResolution" in data:
        newData["bitmapResolution"] = data["bitmapResolution"]
    return newData

def translateSounds(data):
    newSoundDatas = []
    for soundData in data:
        newSoundData = {
            "name"       : soundData["name"],
            "assetId"    : None, # is replaced later
            "dataFormat" : soundData["extension"],
            "rate"       : None, # is replaced later # playback speed in Hz
            "sampleCount": None, # is replaced later # = "rate" * SECONDS in secs
            "md5ext"     : None, # is replaced later # md5 hash with extension
        }
        #newSoundData = {
        #    "name"       : soundData["name"],
        #    "assetId"    : None, # is replaced later
        #    "dataFormat" : soundData["extension"],
        #    "rate"       : soundData["rate"],        # playback speed in Hz
        #    "sampleCount": soundData["sampleCount"], # = "rate" * SECONDS in secs
        #    "md5ext"     : None, # is replaced later
        #}
        newSoundDatas.append(newSoundData)
    return newSoundDatas

def finalizeSound(data, md5, md5ext, sampleRate, sampleCount):
    newData = {
        "name"       : data["name"],
        "assetId"    : md5,
        "dataFormat" : data["dataFormat"],
        "rate"       : sampleRate,
        "sampleCount": sampleCount,
        "md5ext"     : md5ext,
    }
    return newData
