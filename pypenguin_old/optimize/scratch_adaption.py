from pypenguin_old.utility import string_to_sha256
import json

def adaptProject(data):
    for i, spriteData in enumerate(data["targets"]):
        spriteData["customVars"] = []
        if i == 0:
            token = string_to_sha256("_stage_")
        else:
            token = string_to_sha256(spriteData["name"])
        spriteData["id"        ] = token

        for blockData in spriteData["blocks"].values():
            if isinstance(blockData, list): continue # skip list blocks
            if blockData["opcode"] == "procedures_prototype":
                blockData["mutation"]["optype"] = json.dumps("statement") # Scratch custom blocks are always "instruction" blocks
    
    data["extensionData"] = {}

    data["meta"] = {
        "semver": "3.0.0",
        "vm"    : "0.2.0",
        "agent" : "",
        "platform": {
            "name"   : "PenguinMod",
            "url"    : "https://penguinmod.com/",
            "version": "stable",
        },
    }

    return data
