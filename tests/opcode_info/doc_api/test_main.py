from pmp_manip.core.block import get_input_cls_for_input_mode
from pmp_manip.utility    import (
    get_closest_matches, AbstractTreePath,
    MANIP_InvalidOpcodeError,
)


from pmp_manip.important_consts import (
    OPCODE_STOP_SCRIPT, OPCODE_POLYGON, OPCODE_CB_CALL,
    OPCODE_EXPANDABLE_IF, OPCODE_EXPANDABLE_MATH,
)
from pmp_manip.opcode_info.api import (
    OpcodeInfoAPI, OpcodeInfo,
    BuiltinInputType, InputType, BuiltinDropdownType, DropdownType,
    DropdownValueRule,
)

from pmp_manip.opcode_info.doc_api.main import (
    _repo_link, _inputsrcls_link, _generate_possible_values_string,
    _generate_inputs_section,
    generate_opcode_doc,
)


def test_repo_link():
    expected = "https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/path/to/file.abc#my-section"
    assert _repo_link("path/to/file.abc", section="my-section") == expected



def test_inputsrcls_link():
    expected = "[`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)"
    assert _inputsrcls_link(BuiltinInputType.NUMBER) == expected




