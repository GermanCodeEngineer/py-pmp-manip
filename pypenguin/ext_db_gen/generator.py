import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))); del sys, os

from subprocess import run as run_subprocess
from typing     import Any
from json       import loads

from pypenguin.opcode_info.api import OpcodeInfoGroup, OpcodeInfo
from pypenguin.utility         import grepr, DualKeyDict

def extract_getinfo(ext_file: str) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class.
    A node subprocess is run, which lets the outer code run and then calls and logs the return value of the getInfo method of the extension class.
    
    Args:
        the file path or https URL or JS Data URI of the extension code
    
    """
    result = run_subprocess(
        ["node", "pypenguin/ext_db_gen/extractor.js", ext_file],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return loads(result.stdout)
    # Returned properties:
    #     ["id", "name", "color1", "menuIconURI", "blocks", "menus"])
    # Of these:
    #     Irrelevant: ["id", "name", "color1", "menuIconURI"]
    #     Relevant:   ["blocks", "menus"]

def generate_block_opcode_info(block_info: dict[str, Any]) -> OpcodeInfo:
    # TODO: docstring
    print()
    print()
    print("CURRENT BLOCK", grepr(block_info))
    
    # block_type to opcode_type:
    {
        "command": OpcodeType.STATEMENT,
        "reporter": OpcodeType.STRING_REPORTER,
        "Boolean": OpcodeType.BOOLEAN_REPORTER,
        "hat": OpcodeType.HAT,
        "event": OpcodeType.HAT,
        "conditional": OpcodeType.STATEMENT, # but needs to add a subscript at the end or smth
        "loop": OpcodeType.STATEMENT, # same
        "label": None, # IGNORE, not really a block
        "button": None, # IGNORE, not really a block
        "xml": None, # Not Supported
    }
    
    opcode_info = OpcodeInfo(
        opcode_type: OpcodeType
        inputs: DualKeyDict[str, str, InputInfo] = field(default_factory=DualKeyDict)
        dropdowns: DualKeyDict[str, str, DropdownInfo] = field(default_factory=DualKeyDict)
        can_have_monitor: bool = False
        monitor_id_behaviour: MonitorIdBehaviour | None = None
        has_shadow: bool = None
        special_cases: dict[SpecialCaseType, SpecialCase] = field(default_factory=dict)
        old_mutation_cls: Type["FRMutation"] | None = field(init=False, default_factory=type(None))
        new_mutation_cls: Type["SRMutation"] | None = field(init=False, default_factory=type(None))
    )
    raise Exception("HALT")

def generate_opcode_info_group(extension_info: dict[str, Any]) -> OpcodeInfoGroup:
    # TODO: docstring
    print(grepr(extension_info))
    info_group = OpcodeInfoGroup(
        name=extension_info["id"], # TODO: get correct name
        opcode_info=DualKeyDict(),
    )
    for block_info in extension_info["blocks"]:
        generate_block_opcode_info(block_info)

extension_info = extract_getinfo("pypenguin/ext_db_gen/example.js")
generate_opcode_info_group(extension_info)

