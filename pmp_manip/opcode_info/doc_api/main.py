#from abc         import ABC, abstractmethod

from pmp_manip.utility          import (
    enforce_argument_types, get_closest_matches, AbstractTreePath,
    MANIP_InvalidOpcodeError,
)


from pmp_manip.opcode_info.api import OpcodeInfoAPI

def _as_code(text: str) -> str:
    if "`" in text:
        return f"<code>{text}</code>"
    else:
        return f"`{text}`"

def _generate_opcode_block_doc() -> str:
    pass

def _generate_opcode_monitor_doc() -> str:
    pass

@enforce_argument_types
def generate_opcode_doc(info_api: OpcodeInfoAPI, new_opcode: str) -> str:
    """
    Generate documentation about a block and or monitor opcode in Markdown(md) format.

    Args:
        info_api: the opcode info api used to fetch information about opcodes
        new_opcode: the new opcode i.e. kind of block
    """
    opcode_info = info_api.get_info_by_new_safe(new_opcode)
    if opcode_info is None:
        closest_matches = get_closest_matches(new_opcode, info_api.all_new, n=10)
        msg = (
            f"Unknown new opcode {new_opcode!r}. "
            f"The closest matches are: \n  - "+"\n  - ".join([repr(m) for m in closest_matches])
        )
        raise MANIP_InvalidOpcodeError(AbstractTreePath(), msg)

    opcode_block_doc = _generate_opcode_block_doc()
    opcode_monitor_doc = _generate_opcode_monitor_doc()
    new_opcode="&control::if <CONDI`TION> then {THEN} else {ELSE}"
    opcode_prefix, opcode_text = new_opcode.removeprefix("&").split("::")
    return (
        f"## Documentation for opcode {_as_code(opcode_text)}({opcode_prefix})\n"
        f""
    )
    



#__all__ = []

