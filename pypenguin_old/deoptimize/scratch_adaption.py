import json

def adaptProject(data):
    for targetData in data["targets"]:
        del targetData["customVars"]
        del targetData["id"]
        
        for blockData in targetData["blocks"].values():
            if isinstance(blockData, list): continue # skip list blocks
            if blockData["opcode"] == "procedures_prototype":
                if blockData["mutation"]["optype"] != json.dumps("statement"):
                    print("WARNING: Scratch only supports custom blockDatas of type 'instruction'")
                del blockData["mutation"]["returns"]
                del blockData["mutation"]["edited"]
                del blockData["mutation"]["optype"]
                del blockData["mutation"]["color"]
                
    
    del data["extensionData"]
    if "extensionURLs" in data:
        del data["extensionURLs"]

    data["meta"] = {
        "semver": "3.0.0",
        "vm": "5.0.40",
        "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    return data
