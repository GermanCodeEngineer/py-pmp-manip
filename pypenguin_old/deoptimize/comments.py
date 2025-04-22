def translateComment(data, id):
    return {
        "blockId"  : id,
        "x"        : data["position"][0],
        "y"        : data["position"][1],
        "width"    : data["size"][0],
        "height"   : data["size"][1],
        "minimized": data["isMinimized"],
        "text"     : data["text"],
    }
