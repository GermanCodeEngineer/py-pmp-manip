for cat in ["motion"]:#, "looks"]:#, "sounds", "events"]:#, "control", "sensing", "operators", "variables", "lists"]:
    exec(f"from {cat} import opcodes")
    
    string = cat + ' = BlockSet(name="' + cat + '", blocks={\n'
    for opcode, block in opcodes.items():
        block_string = f'    "{opcode.removeprefix(cat+"_")}": BlockData(\n'
        
        block["inputs"] = {}
        it = block.get("inputTranslation", {})
        for new_input_id, input_type in block["inputTypes"].items():
            if new_input_id in list(it.values()):
                old_input_id = list(it.keys())[list(it.values()).index(new_input_id)]
                block["inputs"][new_input_id] = {"type": input_type, "old": old_input_id}
            else:
                block["inputs"][new_input_id] = {"type": input_type, "old": new_input_id}
        del block["inputTypes"]
        if "inputTranslation" in block: del block["inputTranslation"]
        
        if "menus" in block:
            for menu in block["menus"]:
                block["inputs"][menu["new"]]["menu"] = f'MenuData("{menu["menuOpcode"]}", inner="{menu["inner"]}")'
                block["inputs"][menu["new"]]["old"] = menu["outer"]
            del block["menus"]
        
        block["dropdowns"] = {}
        ot = block.get("optionTranslation", {})
        for new_input_id, input_type in block["optionTypes"].items():
            if new_input_id in list(ot.values()):
                old_input_id = list(ot.keys())[list(ot.values()).index(new_input_id)]
                block["dropdowns"][new_input_id] = {"type": input_type, "old": old_input_id}
            else:
                block["dropdowns"][new_input_id] = {"type": input_type, "old": new_input_id}
        del block["optionTypes"]
        if "optionTranslation" in block: del block["optionTranslation"]
        
        #print(block)
        for attr, value in block.items():
            match attr:
                case "type": block_string += '        block_type="' + value + '",\n'
                case "category": pass
                case "newOpcode": block_string += '        new_opcode="' + value + '",\n'
                case "inputs": 
                    if value == {}: break
                    block_string += '        inputs={\n'
                    for old_input_id, input_data in value.items():
                        block_string += f'            "{old_input_id}": InputData("{input_data["type"]}"'
                        if "old" in input_data:
                            block_string += f', old="{input_data["old"]}"'
                        if "menu" in input_data:
                            block_string += f', menu={input_data["menu"]}'
                        block_string += '),\n'
                        
                    #raise Exception()
                    block_string += "        },\n"
                case "dropdowns":
                    if value == {}: break
                    block_string += '        dropdowns={\n'
                    for old_input_id, input_data in value.items():
                        block_string += f'            "{old_input_id}": DropdownData("{input_data["type"]}"'
                        if "old" in input_data:
                            block_string += f', old="{input_data["old"]}"'
                        block_string += '),\n'
                        
                    #raise Exception()
                    block_string += "        },\n"
                #case "inputTypes": block_string += '        "' + value + '",n'
                #case "inputTranslation": block_string += '        blockType="' + value + '",n'
                #case "optionTypes": block_string += '        blockType="' + value + '",n'
                #case "optionTranslation": block_string += '        blockType="' + value + '",n'
                case "canHaveMonitor": block_string += '        can_have_monitor="' + str(value) + '",\n'
                case "fromPenguinMod": pass
                case _: raise AttributeError(attr)
        block_string += "    ),\n"
        string += block_string
    
    string += "})"
    print("from b,ocksets.blockset import BlockSet, BlockData, InputData, MenuData, DropdownData\n")
    print(string)
    input()
