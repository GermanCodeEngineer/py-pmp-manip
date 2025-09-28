from copy import copy
from pytest import fixture, raises

from pmp_manip.utility import MANIP_UnknownOpcodeError


from pmp_manip.important_consts  import (
    OPCODE_STOP_SCRIPT, OPCODE_POLYGON, OPCODE_CB_CALL,
    OPCODE_EXPANDABLE_IF, OPCODE_EXPANDABLE_MATH,
)
from pmp_manip.opcode_info.api  import (
    BuiltinInputType, BuiltinDropdownType, DropdownType,
    DropdownValueRule, DropdownTypeInfo,
)
from pmp_manip.opcode_info.data import info_api

from pmp_manip.opcode_info.doc_api.main import (
    _repo_link, _inputsrcls_link, _generate_possible_values_string,
    _generate_inputs_section, _generate_block_shape_section,
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
    assert _generate_possible_values_string(BuiltinDropdownType.EDITOR_BUTTON) == "No guessed possible values"

def test_generate_possible_values_string_unpredictable():
    class MyDropdownType(DropdownType):
        MY_DROPDOWN = DropdownTypeInfo(rules=[DropdownValueRule.EXTENSION_UNPREDICTABLE])
    assert _generate_possible_values_string(MyDropdownType.MY_DROPDOWN) == "Unpredictable. Calculated by extension at runtime in PM-Editor."


def test_generate_inputs_section_main():
    opcode_info = info_api.get_info_by_old("motion_glideto")
    generated = _generate_inputs_section(
        old_opcode="motion_glideto",
        opcode_namespace="motion",
        opcode_info=opcode_info,
    )
    assert generated == (
        "### Inputs\n"+
        "* `SECONDS`\n"+
        "    * type: **NUMBER**\n"+
        "    * SR-Class: [`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)\n"+
        "* `TARGET`\n"+
        "    * type: **RANDOM_MOUSE_OR_OTHER_SPRITE**\n"+
        "    * SR-Class: [`SRBlockAndDropdownInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndDropdownInputValue)\n"+
        "    * possible values for `.dropdown`:\n"+
        "        * `SRDropdownValue(DropdownValueKind.OBJECT, 'random position')`\n"+
        "        * `SRDropdownValue(DropdownValueKind.OBJECT, 'mouse-pointer')`\n"
    )

def test_generate_inputs_section_cb_call():
    opcode_info = info_api.get_info_by_old(OPCODE_CB_CALL)
    generated = _generate_inputs_section(
        old_opcode=OPCODE_CB_CALL,
        opcode_namespace="customblocks",
        opcode_info=opcode_info,
    )
    assert generated == (
        "### Inputs\n"+
        "Depends on the inputs of the custom block to call.\n"+
        "* all inputs\n"+
        "    * type: **TEXT** or **BOOLEAN**\n"+
        "    * SR-Class: [`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)\n"
    )

def test_generate_inputs_section_polygon():
    opcode_info = info_api.get_info_by_old(OPCODE_POLYGON)
    generated = _generate_inputs_section(
        old_opcode=OPCODE_POLYGON,
        opcode_namespace="special",
        opcode_info=opcode_info,
    )
    assert generated == (
        "### Inputs\n"+
        "Depends on how many coordinate pairs the parent block expects. "+
        "format of keys: `X1`...`Xn`, `Y1`...`Yn`\n"+
        "* `X1`...`Xn`\n"+
        "    * type: **NUMBER**\n"+ 
        "    * SR-Class: [`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)\n"+
        "* `Y1`...`Yn`\n"+
        "    * type: **NUMBER**\n"+ 
        "    * SR-Class: [`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)\n"
    )

def test_generate_inputs_section_expandable_if():
    opcode_info = info_api.get_info_by_old(OPCODE_EXPANDABLE_IF)
    generated = _generate_inputs_section(
        old_opcode=OPCODE_EXPANDABLE_IF,
        opcode_namespace="control",
        opcode_info=opcode_info,
    )
    assert generated == (
        "### Inputs\n"+
        "Depends on how many branches the block has. "+
        "format of keys: `CONDITION1`...`CONDITIONn`, `THEN1`...`THENn`, `ELSE` if it has an else branch\n"+
        "* `CONDITION1`...`CONDITIONn`\n"+
        "    * type: **BOOLEAN**\n"+ 
        "    * SR-Class: [`SRBlockAndBoolInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndBoolInputValue)\n"+
        "* `THEN1`...`THENn`\n"+
        "    * type: **SCRIPT**\n"+ 
        "    * SR-Class: [`SRScriptInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRScriptInputValue)\n"+
        "* (`ELSE`)\n"+
        "    * type: **SCRIPT**\n"+ 
        "    * SR-Class: [`SRScriptInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRScriptInputValue)\n"
    )

def test_generate_inputs_section_expandable_math():
    opcode_info = info_api.get_info_by_old(OPCODE_EXPANDABLE_MATH)
    generated = _generate_inputs_section(
        old_opcode=OPCODE_EXPANDABLE_MATH,
        opcode_namespace="operators",
        opcode_info=opcode_info,
    )
    assert generated == (
        "### Inputs\n"+
        "Depends on how many operations the block does. "+
        "format of keys: `OPERAND1`...`OPERANDn`\n"+
        "* `OPERAND1`...`OPERANDn`\n"+
        "    * type: **NUMBER**\n"+ 
        "    * SR-Class: [`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)\n"
    )

def test_generate_inputs_section_no_inputs():
    opcode_info = info_api.get_info_by_old("sensing_mousex")
    generated = _generate_inputs_section(
        old_opcode="sensing_mousex",
        opcode_namespace="sensing",
        opcode_info=opcode_info,
    )
    assert generated == "### Inputs: /\n"


def test_generate_block_shape_section_main():
    opcode_info = info_api.get_info_by_old("motion_glideto")
    generated = _generate_block_shape_section(
        old_opcode="motion_glideto",
        opcode_type=opcode_info.opcode_type,
    )
    assert generated == (
        "### Block Shape\n"+
        "* [**STATEMENT**](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/block_shape.md#STATEMENT)\n"
    )

def test_generate_block_shape_section_stop_script():
    opcode_info = info_api.get_info_by_old(OPCODE_STOP_SCRIPT)
    generated = _generate_block_shape_section(
        old_opcode=OPCODE_STOP_SCRIPT,
        opcode_type=opcode_info.opcode_type,
    )
    assert generated == (
        "### Block Shape\n"+
        "* [**DYNAMIC**](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/block_shape.md#DYNAMIC)\n"+
        "* Flexible. Can be **ENDING_STATEMENT or STATEMENT** depending on the menu dropdown.\n"
    )

def test_generate_block_shape_section_cb_call():
    opcode_info = info_api.get_info_by_old(OPCODE_CB_CALL)
    generated = _generate_block_shape_section(
        old_opcode=OPCODE_CB_CALL,
        opcode_type=opcode_info.opcode_type,
    )
    assert generated == (
        "### Block Shape\n"+
        "* [**DYNAMIC**](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/block_shape.md#DYNAMIC)\n"+
        "* Flexible. Can be **STATEMENT, ENDING_STATEMENT, STRING_REPORTER, NUMBER_REPORTER, BOOLEAN_REPORTER** matches the shape of the custom block to call.\n"
    )


def test_generate_opcode_doc_main():
    generated = generate_opcode_doc(info_api, new_opcode="&motion::glide (SECONDS) secs to ([TARGET])")
    assert generated == (
        '## Documentation for opcode `glide (SECONDS) secs to ([TARGET])`(motion)\n'+
        "### Block Shape\n"+
        "* [**STATEMENT**](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/block_shape.md#STATEMENT)\n"
        "### Inputs\n"+
        "* `SECONDS`\n"+
        "    * type: **NUMBER**\n"+
        "    * SR-Class: [`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)\n"+
        "* `TARGET`\n"+
        "    * type: **RANDOM_MOUSE_OR_OTHER_SPRITE**\n"+
        "    * SR-Class: [`SRBlockAndDropdownInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndDropdownInputValue)\n"+
        "    * possible values for `.dropdown`:\n"+
        "        * `SRDropdownValue(DropdownValueKind.OBJECT, 'random position')`\n"+
        "        * `SRDropdownValue(DropdownValueKind.OBJECT, 'mouse-pointer')`\n"+
        "### Dropdowns: /\n"+
        "### Mutation: /\n"+
        "### Monitor: /\n"
    )

def test_generate_opcode_doc_unknown_upcode():
    with raises(MANIP_UnknownOpcodeError):
        generate_opcode_doc(info_api, new_opcode="&someExt::some (STUFF) with [OPTION]")

def test_generate_opcode_doc_dropdowns_monitor():
    generated = generate_opcode_doc(info_api, new_opcode="&variables::value of [VARIABLE]")
    assert generated == (
        '## Documentation for opcode `value of [VARIABLE]`(variables)\n'+
        "### Block Shape\n"+
        "* [**STRING_REPORTER**](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/block_shape.md#STRING_REPORTER)\n"+
        "### Inputs: /\n"+
        "### Dropdowns\n"+
        "* `VARIABLE`\n"+
        "    * type: **VARIABLE**\n"+
        "    * possible values: No guessed possible values\n"+
        "### Mutation: /\n"+
        "### Monitor\n"+
        "[Monitors](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRMonitor) with this opcode can exist.\n"
    )

def test_generate_opcode_doc_editor_button_monitor():
    generated = generate_opcode_doc(info_api, new_opcode="&control::{{EXPANDABLE IF-THEN-ELSE CHAIN}}")
    assert generated == (
        '## Documentation for opcode `{{EXPANDABLE IF-THEN-ELSE CHAIN}}`(control)\n'+
        "### Block Shape\n"+
        "* [**STATEMENT**](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/block_shape.md#STATEMENT)\n"+
        "### Inputs\n"+
        "Depends on how many branches the block has. "+
        "format of keys: `CONDITION1`...`CONDITIONn`, `THEN1`...`THENn`, `ELSE` if it has an else branch\n"+
        "* `CONDITION1`...`CONDITIONn`\n"+
        "    * type: **BOOLEAN**\n"+ 
        "    * SR-Class: [`SRBlockAndBoolInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndBoolInputValue)\n"+
        "* `THEN1`...`THENn`\n"+
        "    * type: **SCRIPT**\n"+ 
        "    * SR-Class: [`SRScriptInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRScriptInputValue)\n"+
        "* (`ELSE`)\n"+
        "    * type: **SCRIPT**\n"+ 
        "    * SR-Class: [`SRScriptInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRScriptInputValue)\n"+
        "### Dropdowns: /\n"+
        "### Mutation\n"+
        "An instance of [`SRExpandableIfMutation`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRExpandableIfMutation).\n"+
        "### Monitor: /\n"
    )
