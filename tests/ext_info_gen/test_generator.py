from pytest import raises

from pmp_manip.opcode_info.api import (
    OpcodeInfoGroup, OpcodeInfo, OpcodeType, MonitorIdBehaviour,
    InputInfo, InputMode, InputType, BuiltinInputType, MenuInfo,
    DropdownInfo, DropdownType, BuiltinDropdownType, DropdownTypeInfo,
    DropdownValueRule,
)
from pmp_manip.utility         import (
    grepr, DualKeyDict, GEnum,
    PP_ThanksError, PP_TempNotImplementedError, PP_NotImplementedError,
    PP_InvalidCustomMenuError, PP_InvalidCustomBlockError,
    PP_UnknownExtensionAttributeError, 
)

from pmp_manip.ext_info_gen.generator import process_all_menus
    


def test_process_all_menus_valid():
    menu_data = { # mostly copied from https://extensions.penguinmod.com/extensions/derpygamer2142/gpusb3.js
        "TYPES": {
            "acceptReporters": True,
            "items": ["i32", "u32", "f32", "bool", "auto"],
        },
        "VARTYPES": {
            "acceptReporters": False,
            "items": ["var", "let", "const"],
        },
        "FUNCTYPES": [
            "normal", "generator", "async",
            {"text": "(...) => {}", "value": "arrow"},
        ],
        "ARRAYBUFFERS": {
            "acceptReporters": True,
            "items": "getArrayBuffersMenu",
        }, 
    }
    input_type_cls, dropdown_type_cls = process_all_menus(menu_data)
    input_type_members    = {member.name: member.value for member in input_type_cls   }
    dropdown_type_members = {member.name: member.value for member in dropdown_type_cls}
    
    assert set(input_type_members.keys()) == {"TYPES", "ARRAYBUFFERS"}
    assert input_type_members["TYPES"] == (InputMode.BLOCK_AND_DROPDOWN, None, dropdown_type_cls.TYPES, 0)
    assert input_type_members["ARRAYBUFFERS"] == (InputMode.BLOCK_AND_DROPDOWN, None, dropdown_type_cls.ARRAYBUFFERS, 3)

    assert set(dropdown_type_members.keys()) == {"TYPES", "VARTYPES", "FUNCTYPES", "ARRAYBUFFERS"}
    assert dropdown_type_members["TYPES"] == DropdownTypeInfo(
        direct_values=["i32", "u32", "f32", "bool", "auto"],
        rules=[],
        old_direct_values=["i32", "u32", "f32", "bool", "auto"],
        fallback=None,
    )
    assert dropdown_type_members["VARTYPES"] == DropdownTypeInfo(
        direct_values=["var", "let", "const"],
        rules=[],
        old_direct_values=["var", "let", "const"],
        fallback=None,
    )
    assert dropdown_type_members["FUNCTYPES"] == DropdownTypeInfo(
        direct_values=["normal", "generator", "async", "(...) => {}"],
        rules=[],
        old_direct_values=["normal", "generator", "async", "arrow"],
        fallback=None,
    )
    assert dropdown_type_members["ARRAYBUFFERS"] == DropdownTypeInfo(
        direct_values=[],
        rules=[DropdownValueRule.EXTENSION_UNPREDICTABLE],
        old_direct_values=[],
        fallback=None,
    )

def test_process_all_menus_invalid_menu_type():
    with raises(PP_InvalidCustomMenuError):
        process_all_menus({
            "SOME_MENU": (True, ["i32", "u32", "f32", "bool", "auto"])
        })

def test_process_all_menus_invalid_menu_items_type():
    with raises(PP_InvalidCustomMenuError):
        process_all_menus({
            "SOME_MENU": {"items": {"a", "b", "c"}}
        })

def test_process_all_menus_invalid_menu_possible_value_type():
    with raises(PP_InvalidCustomMenuError):
        process_all_menus({
            "SOME_MENU": {"items": [("Hi, How are you?", "hi_1")]}
        })

def test_process_all_menus_missing_items():
    with raises(PP_InvalidCustomMenuError):
        process_all_menus({
            "SOME_MENU": {"acceptReporters": True},
        })

def test_process_all_menus_possible_value_missing_text_value():
    with raises(PP_InvalidCustomMenuError):
        process_all_menus({
            "SOME_MENU": {"items": [{"value": "hi"}]}
        })
    with raises(PP_InvalidCustomMenuError):
        process_all_menus({
            "SOME_MENU": {"items": [{"text": "Hi :)"}]}
        })



def test_generate_block_opcode_info


