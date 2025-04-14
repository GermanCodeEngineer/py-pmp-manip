def translateCostumes(data):
    newCostumeDatas = []
    for costumeData in data:
        newCostumeData = {
            "name"            : costumeData["name"],
            "extension"       : costumeData["dataFormat"],
            "bitmapResolution": None,
            "rotationCenter"  : [costumeData["rotationCenterX"], costumeData["rotationCenterY"]],
        }
        if "bitmapResolution" in costumeData:
            newCostumeData["bitmapResolution"] = costumeData["bitmapResolution"]
        else:
            newCostumeData["bitmapResolution"] = 1
        newCostumeDatas.append(newCostumeData)
    return newCostumeDatas

"""def finalizeCostume(data, width, height):
    newRotationCenter = [data["rotationCenter"][0] - width  / 2,
                         data["rotationCenter"][1] - height / 2]
    newData = {
        "name"            : data["name"],
        "extension"       : data["extension"],
        "bitmapResolution": data["bitmapResolution"],
        "rotationCenter"  : newRotationCenter,
    }
    return newData"""

def translateSounds(data):
    newSoundDatas = []
    for soundData in data:
        newSoundData = {
            "name"       : soundData["name"],
            "extension"  : soundData["dataFormat"],
            #"rate"       : soundData["rate"],        # playback speed in Hz
            #"sampleCount": soundData["sampleCount"], # = "rate" * SECONDS in secs
        }
        newSoundDatas.append(newSoundData)
    return newSoundDatas
