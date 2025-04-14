from enum import Enum
from customization_handler import CEventBlockAPI

class SRCustomOpcode:
    _grepr = True
    _grepr_fields = ["proccode", "arguments"]

    proccode: str
    arguments: dict[str, "SRCustomArgumentType"]

    def __init__(self, proccode: str, argument_ids: list[str], argument_names: list[str], argument_defaults: list[str]):
        self.proccode = proccode
        self.arguments = {
            name: SRCustomArgumentType.get_by_default(default)
            for name, default in zip(argument_names, argument_defaults)
        }
        

class SRCustomArgumentType(Enum):
    STRING_NUMBER = 0
    BOOLEAN       = 1

    @staticmethod
    def get_by_default(default):
        match default:
            case "":
                return SRCustomArgumentType.STRING_NUMBER
            case "false":
                return SRCustomArgumentType.BOOLEAN
            case _:
                raise ValueError()


def INSTEAD__CB_DEF(manager: CEventBlockAPI, block):
    import json
    from custom_block import SRCustomOpcode
    prototype_id    = block.inputs["custom_block"][1]
    prototype_block = manager.get_block(prototype_id)

    mutation        = prototype_block.mutation
    customOpcode    = SRCustomOpcode(
        proccode       = mutation.proccode, 
        argument_names = mutation.argument_names,
    )

    # Find out which block type the custom block is
    match mutation.optype:
        case None       : blockType = "instruction"
        case "statement": blockType = "instruction"
        case "end"      : blockType = "lastInstruction"
        case "string"   : blockType = "textReporter"
        case "number"   : blockType = "numberReporter"
        case "boolean"  : blockType = "booleanReporter"
    warp = mutation["warp"] if isinstance(mutation["warp"], bool) else json.loads(mutation["warp"]) # Wether "no screen refresh is ticked"

    newBlockData = {
        "opcode": "define custom block",
        "inputs": {},
        "options": {
            "customOpcode"   : customOpcode,
            "noScreenRefresh": warp,
            "blockType"      : blockType,
        },
        "_info_"      : {
            "next"    : block["next"],
            "topLevel": block["topLevel"],
        },
    }
    if "comment" in block:
        newBlockData["comment"] = block["comment"]

    # Mark the prototype and the arguments display blocks to be deleted in the future
    prototype_block["doDelete"] = True

    for blockData in manager.get_all_blocks().values():
        if blockData["parent"] == prototype_id:
            blockData["doDelete"] = True

    return newBlockData
    #manager.schedule_block_removal()

