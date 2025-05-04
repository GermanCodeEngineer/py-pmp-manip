original_to_enum_name = {
    "direction"                           : "DIRECTION",
    "integer"                             : "INTEGER",
    "positive integer"                    : "POSITIVE_INTEGER",
    "positive number"                     : "POSITIVE_NUMBER",
    "number"                              : "NUMBER",
    "text"                                : "TEXT",
    "color"                               : "COLOR",

    "note"                                : "NOTE",

    "boolean"                             : "BOOLEAN",
    "round"                               : "ROUND",
    "embeddedMenu"                        : "EMBEDDED_MENU",

    "script"                              : "SCRIPT",

    "broadcast"                           : "BROADCAST",

    "stage || other sprite"               : "STAGE_OR_OTHER_SPRITE",
    "cloning target"                      : "CLONING_TARGET",
    "mouse || other sprite"               : "MOUSE_OR_OTHER_SPRITE",
    "mouse|edge || other sprite"          : "MOUSE_EDGE_OR_OTHER_SPRITE",
    "mouse|edge || myself || other sprite": "MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE",
    "key"                                 : "KEY",
    "up|down"                             : "UP_DOWN",
    "finger index"                        : "FINGER_INDEX",
    "random|mouse || other sprite"        : "RANDOM_MOUSE_OR_OTHER_SPRITE",
    "costume"                             : "COSTUME",
    "costume property"                    : "COSTUME_PROPERTY",
    "backdrop"                            : "BACKDROP",
    "backdrop property"                   : "BACKDROP_PROPERTY",
    "myself || other sprite"              : "MYSELF_OR_OTHER_SPRITE",
    "sound"                               : "SOUND",
    "drum"                                : "DRUM",
    "instrument"                          : "INSTRUMENT",
    "font"                                : "FONT",
    "pen property"                        : "PEN_PROPERTY",
    "video sensing property"              : "VIDEO_SENSING_PROPERTY",
    "video sensing target"                : "VIDEO_SENSING_TARGET",
    "video state"                         : "VIDEO_STATE",
    "text to speech voice"                : "TEXT_TO_SPEECH_VOICE",
    "text to speech language"             : "TEXT_TO_SPEECH_LANGUAGE",
    "translate language"                  : "TRANSLATE_LANGUAGE",
    "makey key"                           : "MAKEY_KEY",
    "makey sequence"                      : "MAKEY_SEQUENCE",
    "read file mode"                      : "READ_FILE_MODE",
    "file selector mode"                  : "FILE_SELECTOR_MODE",
}

old_option_type_name_to_enum = {
    "key": "KEY",
    "unary math operation": "UNARY_MATH_OPERATION",
    "power|root|log": "POWER_ROOT_LOG",
    "root|log": "ROOT_LOG",
    "text method": "TEXT_METHOD",
    "text case": "TEXT_CASE",
    "stop script target": "STOP_SCRIPT_TARGET",
    "stage || other sprite": "STAGE_OR_OTHER_SPRITE",
    "cloning target": "CLONING_TARGET",
    "up|down": "UP_DOWN",
    "loudness|timer": "LOUDNESS_TIMER",
    "mouse || other sprite": "MOUSE_OR_OTHER_SPRITE",
    "mouse|edge || other sprite": "MOUSE_EDGE_OR_OTHER_SPRITE",
    "mouse|edge || myself || other sprite": "MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE",
    "x|y": "X_OR_Y",
    "drag mode": "DRAG_MODE",
    "mutable sprite property": "MUTABLE_SPRITE_PROPERTY",
    "readable sprite property": "READABLE_SPRITE_PROPERTY",
    "time property": "TIME_PROPERTY",
    "finger index": "FINGER_INDEX",
    "random|mouse || other sprite": "RANDOM_MOUSE_OR_OTHER_SPRITE",
    "rotation style": "ROTATION_STYLE",
    "stage zone": "STAGE_ZONE",
    "text bubble color property": "TEXT_BUBBLE_COLOR_PROPERTY",
    "text bubble property": "TEXT_BUBBLE_PROPERTY",
    "sprite effect": "SPRITE_EFFECT",
    "costume": "COSTUME",
    "backdrop": "BACKDROP",
    "costume property": "COSTUME_PROPERTY",
    "myself || other sprite": "MYSELF_OR_OTHER_SPRITE",
    "front|back": "FRONT_BACK",
    "forward|backward": "FORWARD_BACKWARD",
    "infront|behind": "INFRONT_BEHIND",
    "number|name": "NUMBER_NAME",
    "sound": "SOUND",
    "sound effect": "SOUND_EFFECT",
    "blockType": "BLOCK_TYPE",
    "drum": "DRUM",
    "instrument": "INSTRUMENT",
    "note": "NOTE",
    "font": "FONT",
    "on|off": "ON_OFF",
    "expanded|minimized": "EXPANDED_MINIMIZED",
    "vertex count": "VERTEX_COUNT",
    "pen property": "PEN_PROPERTY",
    "animation technique": "ANIMATION_TECHNIQUE",
    "left|center|right": "LEFT_CENTER_RIGHT",
    "video sensing property": "VIDEO_SENSING_PROPERTY",
    "video sensing target": "VIDEO_SENSING_TARGET",
    "video state": "VIDEO_STATE",
    "text to speech voice": "TEXT_TO_SPEECH_VOICE",
    "text to speech language": "TEXT_TO_SPEECH_LANGUAGE",
    "translate language": "TRANSLATE_LANGUAGE",
    "makey key": "MAKEY_KEY",
    "makey sequence": "MAKEY_SEQUENCE",
    "read file mode": "READ_FILE_MODE",
    "file selector mode": "FILE_SELECTOR_MODE",

    
    "broadcast":"BROADCAST",
    "variable":"VARIABLE",
    "list":"LIST",
    "boolean": "ENABLE_DISABLE_SCREEN_REFRESH",
    "opcode": "CUSTOM_OPCODE",
    "reporter name": "REPORTER_NAME",
}

bt_translation = {
    'instruction': "STATEMENT",
    'lastInstruction': "ENDING_STATEMENT",
    
    'stringReporter' : "STRING_REPORTER",
    'numberReporter': "NUMBER_REPORTER",
    'booleanReporter': "BOOLEAN_REPORTER",
    
    'hat': "HAT",
    'dynamic': "DYNAMIC",
    "menu": "MENU",
    "embeddedMenu": "POLYGON_MENU"
}

for cat in ["motion", "looks", "sounds", "events", "control", "sensing", "operators", "variables", "lists", "extension_video_sensing"]:
    exec(f"from {cat} import opcodes")
    
    if   cat == "sounds": block_cat = "sound"
    elif cat == "events": block_cat = "event"
    elif cat == "operators": block_cat = "operator"
    elif cat == "variables": block_cat = "data"
    elif cat == "lists": block_cat = "data"
    else:
        block_cat = cat
    string = "from pypenguin.utility import DualKeyDict\n\nfrom pypenguin.opcode_info import OpcodeInfoGroup, OpcodeInfo, OpcodeType, InputInfo, InputType, DropdownInfo, DropdownType, MenuInfo\n\n" + cat + ' = OpcodeInfoGroup(name="' + cat + '", opcode_info=DualKeyDict({\n'
    for opcode, block in opcodes.items():
        block_string = '    ("'+opcode+'", "'+block["newOpcode"]+'"): OpcodeInfo(\n'
        
        block["inputs"] = {}
        it = block.get("inputTranslation", {})
        for new_input_id, input_type in block["inputTypes"].items():
            new_input_type = original_to_enum_name[input_type]
            if new_input_id in list(it.values()):
                old_input_id = list(it.keys())[list(it.values()).index(new_input_id)]
                block["inputs"][new_input_id] = {"type": new_input_type, "old": old_input_id}
            else:
                block["inputs"][new_input_id] = {"type": new_input_type, "old": new_input_id}
        del block["inputTypes"]
        if "inputTranslation" in block: del block["inputTranslation"]
        
        if "menus" in block:
            for menu in block["menus"]:
                block["inputs"][menu["new"]]["menu"] = f'MenuInfo("{menu["menuOpcode"]}", inner="{menu["inner"]}")'
                block["inputs"][menu["new"]]["old"] = menu["outer"]
            del block["menus"]
        
        block["dropdowns"] = {}
        ot = block.get("optionTranslation", {})
        for new_input_id, input_type in block["optionTypes"].items():
            #print(opcode)
            new_input_type = old_option_type_name_to_enum[input_type]
            if new_input_id in list(ot.values()):
                old_input_id = list(ot.keys())[list(ot.values()).index(new_input_id)]
                block["dropdowns"][new_input_id] = {"type": new_input_type, "old": old_input_id}
            else:
                block["dropdowns"][new_input_id] = {"type": new_input_type, "old": new_input_id}
        del block["optionTypes"]
        if "optionTranslation" in block: del block["optionTranslation"]
        
        if opcode == "event_whenkeypressed":
            print(block)
        
        #print(block)
        for attr, value in block.items():
            if opcode == "event_whenkeypressed": print("HERE", attr)
            match attr:
                case "type": 
                    block_string += '        opcode_type=OpcodeType.' + bt_translation[value] + ',\n'
                case "category": pass
                case "newOpcode": pass
                case "inputs": 
                    if value == {}: continue
                    block_string += '        inputs=DualKeyDict({\n'
                    for old_input_id, input_data in value.items():
                        block_string += f'            ("{input_data["old"]}", "{old_input_id}"): InputInfo(InputType.{input_data["type"]}'
                        if "menu" in input_data:
                            block_string += f', menu={input_data["menu"]}'
                        block_string += '),\n'
                        
                    #raise Exception()
                    block_string += "        }),\n"
                case "dropdowns":
                    if value == {}: continue
                    if opcode == "event_whenkeypressed": print("HERE")
                    block_string += '        dropdowns=DualKeyDict({\n'
                    for old_input_id, input_data in value.items():
                        block_string += f'            ("{input_data["old"]}", "{old_input_id}"): DropdownInfo(DropdownType.{input_data["type"]}'
                        block_string += '),\n'
                        
                    #raise Exception()
                    block_string += "        }),\n"
                #case "inputTypes": block_string += '        "' + value + '",n'
                #case "inputTranslation": block_string += '        blockType="' + value + '",n'
                #case "optionTypes": block_string += '        blockType="' + value + '",n'
                #case "optionTranslation": block_string += '        blockType="' + value + '",n'
                case "canHaveMonitor": block_string += '        can_have_monitor="' + str(value) + '",\n'
                case "fromPenguinMod": pass
                case _: raise AttributeError(attr)
        block_string += "    ),\n"
        if opcode == "event_whenkeypressed":
            print(block_string)
        
        string += block_string
    
    string += "}))"
    #print(string)
    with open("pypenguin/opcode_info/groups/"+cat+".py", "w") as file:
        file.write(string)
