from copy import copy
from pytest import fixture, raises

from pmp_manip.core.block import get_input_cls_for_input_mode
from pmp_manip.utility    import (
    get_closest_matches, AbstractTreePath,
    MANIP_InvalidOpcodeError,
)


from pmp_manip.important_consts  import (
    OPCODE_STOP_SCRIPT, OPCODE_POLYGON, OPCODE_CB_CALL,
    OPCODE_EXPANDABLE_IF, OPCODE_EXPANDABLE_MATH,
)
from pmp_manip.opcode_info.api  import (
    OpcodeInfoAPI, OpcodeInfo,
    BuiltinInputType, InputType, BuiltinDropdownType, DropdownType,
    DropdownValueRule, DropdownTypeInfo,
)
from pmp_manip.opcode_info.data import info_api

from pmp_manip.opcode_info.doc_api.main import (
    _repo_link, _inputsrcls_link, _generate_possible_values_string,
    _generate_inputs_section,
    generate_opcode_doc,
)


@fixture
def info_api_extended():
    info_api_extended = copy(info_api)
    info_api_extended.opcode_info = copy(info_api.opcode_info) 
    # make sure the internals of the DualKeyDict are shallow copied as well
    from tests._gen_ext_opcode_info_.pen import extension
    info_api_extended.add_group(extension)
    return info_api_extended


def test_repo_link():
    expected = "https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/path/to/file.abc#my-section"
    assert _repo_link("path/to/file.abc", section="my-section") == expected


def test_inputsrcls_link():
    expected = "[`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)"
    assert _inputsrcls_link(BuiltinInputType.NUMBER) == expected


def test_generate_possible_values_string_normal():
    assert _generate_possible_values_string(BuiltinDropdownType.MOUSE_EDGE_MYSELF_OR_OTHER_SPRITE) == (
        "\n"
        "        * `SRDropdownValue(DropdownValueKind.OBJECT, 'mouse-pointer')`\n"
        "        * `SRDropdownValue(DropdownValueKind.OBJECT, 'edge')`\n"
        "        * `SRDropdownValue(DropdownValueKind.MYSELF, 'myself')`\n"
        "        * `SRDropdownValue(DropdownValueKind.STAGE, 'stage')`"
    )

def test_generate_possible_values_string_no_values():
    assert _generate_possible_values_string(BuiltinDropdownType.EDITOR_BUTTON) == "No possible values"

def test_generate_possible_values_string_unpredictable():
    class MyDropdownType(DropdownType):
        MY_DROPDOWN = DropdownTypeInfo(rules=[DropdownValueRule.EXTENSION_UNPREDICTABLE])
    assert _generate_possible_values_string(MyDropdownType.MY_DROPDOWN) == "Unpredictable. Calculated by extension at runtime in PM-Editor."


def test_generate_inputs_section():
    opcode_info = info_api.get_info_by_old("control_if")
    generated = _generate_inputs_section(
        old_opcode="control_if",
        opcode_namespace="control",
        opcode_info=opcode_info,
    )
    assert generated == (
        "### Inputs\n"+
        "* `CONDITION`\n"+
        "    * type: **BOOLEAN**\n"+
        "    * SR-Class: [`SRBlockAndBoolInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndBoolInputValue)\n"+
        "\n"+
        "* `THEN`\n"+
        "    * type: **SCRIPT**\n"+
        "    * SR-Class: [`SRScriptInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRScriptInputValue)\n"+
        "\n"
    )

def test_generate_inputs_section():
    opcode_info = info_api.get_info_by_old("motion_glideto")
    generated = _generate_inputs_section(
        old_opcode="motion_glideto",
        opcode_namespace="control",
        opcode_info=opcode_info,
    )
    assert generated == (
        "### Inputs\n"+
        "* `CONDITION`\n"+
        "    * type: **BOOLEAN**\n"+
        "    * SR-Class: [`SRBlockAndBoolInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndBoolInputValue)\n"+
        "\n"+
        "* `THEN`\n"+
        "    * type: **SCRIPT**\n"+
        "    * SR-Class: [`SRScriptInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRScriptInputValue)\n"+
        "\n"
    )


