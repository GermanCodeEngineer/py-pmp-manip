import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import warnings
warnings.warn("The database conversion was discontinued. If you continue, changes will be overwritten!", category=DeprecationWarning)
proceed = input("Do you want to continue? [y/N]: ").strip().lower()
if proceed != 'y':
    print("Aborted.")
    exit(1)
print("Proceeding...")

# Keep these unchanged
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

def format_inputs(block: dict) -> str:
    input_translation = block.pop("inputTranslation", {})
    inputs = block.pop("inputTypes", {})
    menus = block.pop("menus", [])

    input_lines = []
    processed_inputs = {}

    for new_id, input_type in inputs.items():
        new_type = original_to_enum_name[input_type]
        old_id = next((k for k, v in input_translation.items() if v == new_id), new_id)
        processed_inputs[new_id] = {"type": new_type, "old": old_id}

    for menu in menus:
        entry = processed_inputs.get(menu["new"], {})
        entry["menu"] = f'MenuInfo("{menu["menuOpcode"]}", inner="{menu["inner"]}")'
        entry["old"] = menu["outer"]
        processed_inputs[menu["new"]] = entry

    if not processed_inputs:
        return "", {}

    input_lines.append("        inputs=DualKeyDict({")
    for new_id, data in processed_inputs.items():
        menu_str = f', menu={data["menu"]}' if "menu" in data else ""
        input_lines.append(
            f'            ("{data["old"]}", "{new_id}"): InputInfo(InputType.{data["type"]}{menu_str}),'
        )
    input_lines.append("        }),")

    return "\n".join(input_lines), processed_inputs


def format_dropdowns(block: dict) -> str:
    option_translation = block.pop("optionTranslation", {})
    dropdowns = block.pop("optionTypes", {})

    if not dropdowns:
        return ""

    lines = ["        dropdowns=DualKeyDict({"]
    for new_id, input_type in dropdowns.items():
        new_type = old_option_type_name_to_enum[input_type]
        old_id = next((k for k, v in option_translation.items() if v == new_id), new_id)
        lines.append(
            f'            ("{old_id}", "{new_id}"): DropdownInfo(DropdownType.{new_type}),'
        )
    lines.append("        }),")

    return "\n".join(lines)


def process_block(opcode: str, block: dict) -> str:
    new_opcode = block["newOpcode"]
    block_str = f'    ("{opcode}", "{new_opcode}"): OpcodeInfo(\n'

    if "type" in block:
        block_str += f'        opcode_type=OpcodeType.{bt_translation[block["type"]]},\n'

    input_str, _ = format_inputs(block)
    dropdown_str = format_dropdowns(block)

    if input_str:
        block_str += f"{input_str}\n"
    if dropdown_str:
        block_str += f"{dropdown_str}\n"

    if block.get("canHaveMonitor") is not None:
        block_str += f'        can_have_monitor="{block["canHaveMonitor"]}",\n'

    block_str += "    ),\n"
    return block_str


def generate_file(cat: str, opcodes: dict) -> None:
    if   cat.startswith("extension_"):
        good_cat = f"scratch_{cat.removeprefix("extension_")}"
    elif cat.startswith("tw_"):
        good_cat = f"tw_{cat.removeprefix("tw_")}"
    elif cat.startswith("pm_"):
        good_cat = f"pm_{cat.removeprefix("pm_")}"
    elif cat.startswith("link_"):
        good_cat = f"link_{cat.removeprefix("link_")}"
    else:
        good_cat =f"c_{cat}"
    content = [
        "from pypenguin.opcode_info.data_imports import *",
        "",
        f'{good_cat} = OpcodeInfoGroup(name="{good_cat}", opcode_info=DualKeyDict({{'
    ]

    for opcode, block in opcodes.items():  # type: ignore
        content.append(process_block(opcode, block))

    content.append("}))")
    with open(f"pypenguin/opcode_info/data/{good_cat}.py", "w") as f:
        f.write("\n".join(content))


# Main execution
for cat in [
    "motion", "looks", "sounds", "events", "control", "sensing", "operators", "variables", "lists",
    "extension_makey_makey", "extension_music", "extension_pen", "extension_text_to_speech", "extension_text", "extension_translate", "extension_video_sensing",
    "tw_files", "tw_temporary_variables",
    "pm_json",
    "link_bitwise",
]:
    exec(f"from {cat} import opcodes")  # Imports dynamically
    generate_file(cat, opcodes) # type: ignore
