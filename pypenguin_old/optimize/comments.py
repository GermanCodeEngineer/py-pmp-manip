def translateComment(data):
    return {
        "position"   : [data["x"], data["y"]],
        "size"       : [data["width"], data["height"]],
        "isMinimized": data["minimized"],
        "text"       : data["text"],
        "_info_"     : {
            "block": data["blockId"],
        },
    }
