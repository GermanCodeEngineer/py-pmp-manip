from pytest import raises, fixture

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

from pmp_manip.ext_info_gen.generator import process_all_menus, generate_block_opcode_info, generate_opcode_info_group


# random collection from mulitple extensions
EXAMPLE_BLOCK_DATA = [
    { # [0]
        "opcode": "compileHat",
        "blockType": "event",
        "text": "Define shader [NAME] using bind group layout [BGL]",
        "isEdgeActivated": False,
        "arguments": {
            "NAME": {
                "type": "string",
                "defaultValue": "myShader"
            },
            "BGL": {
                "defaultValue": "myBindGroupLayout"
            }
        }
    },
    { # [1]
        "opcode": "computeFunc",
        "blockType": "conditional",
        "text": "Computer shader with workgroup size [WGSIZE]",
        "arguments": {
            "WGSIZE": {
                "type": "string",
                "defaultValue": "[1]"
            }
        },
        "branchCount": 1
    },
    { # [2]
        "opcode": "break",
        "blockType": "command",
        "isTerminal": True,
        "text": "break"
    },
    { # [3]
        "opcode": "asNewBroadCastArgBlock",
        "text": "thread  data",
        "blockType": "reporter",
        "disableMonitor": True
    },
    { # [4]
        "opcode": "error",
        "blockType": "reporter",
        "text": "Error"
    },
    { # [5]
        "opcode": "ifElseIf",
        "text": [
            "if [CONDITION1] then",
            "else if [CONDITION2] then"
        ],
        "branchCount": 2,
        "blockType": "conditional",
        "arguments": {
            "CONDITION1": { "type": "Boolean" },
            "CONDITION2": { "type": "Boolean" }
        }
    },
    { # [6]
        "opcode": "ifElseIfElse",
        "text": [
            "if [CONDITION1] then",
            "else if [CONDITION2] then",
            "else",
            "some unecessary text",
        ],
        "branchCount": 3,
        "blockType": "conditional",
        "arguments": {
            "CONDITION1": { "type": "Boolean" },
            "CONDITION2": { "type": "Boolean" }
        }
    },
    { # [7]
        "disableMonitor": True,
        "opcode": "project2DBehindCam",
        "blockType": "Boolean",
        "text": "is [a] behind camera?",
        "arguments": {
            "a": {
                "type": "string",
                "defaultValue": "[0,0,100]"
            }
        }
    },
    { # [8]
        "blockType": "label",
        "text": "Data input blocks"
    },
    { # [9]
        "opcode": "bindGroupLayoutEntry",
        "blockType": "command",
        "text": "Add bind group layout entry with binding [BINDING] for type [TYPE] and descriptor [DESC]",
        "arguments": {
            "BINDING": {
                "type": "number",
                "defaultValue": 0
            },
            "TYPE": {
                "type": "string",
                "menu": "BGLENTRYTYPES",
                "defaultValue": "buffer"
            }
        }
    },
    { # [10]
        "opcode": "setSomeVar",
        "blockType": "command",
        "text": "set some var [VaRiAbLe] to [VaLuE]",
        "arguments": {
            "VaRiAbLe": {"type": "variable"},
            "VaLuE": {"type": "string"}
        }
    },
    { # [11]
        "opcode": "restartFromTheTop",
        "text": "restart from the top [ICON]",
        "blockType": "command",
        "isTerminal": True,
        "arguments": {
            "ICON": {
                "type": "image",
                "dataURI": "static/blocks-media/repeat.svg"
            }
        }
    },
    { # [12]
        "opcode": "bufferEntryDescriptor",
        "blockType": "reporter",
        "text": "Buffer layout entry descriptor with usage type [TYPE]",
        "arguments": {
            "TYPE": {
                "type": "string",
                "menu": "BUFFERENTRYTYPE"
            }
        }
    },
    { # [13]
        "opcode": "variableUsage",
        "blockType": "reporter",
        "text": "Variable usage [USAGE] next [NEXT]",
        "arguments": {
            "USAGE": {
                "type": "string",
                "menu": "VARUSAGE",
                "defaultValue": "read_write"
            },
            "NEXT": {
                "type": "string",
                "defaultValue": ""
            }
        }
    },
]
EXAMPLE_MENU_DATA = {
    "BGLENTRYTYPES": {
        "acceptReporters": True,
        "items": [
            "buffer",
            "storageTexture"
        ]
    },
    "BUFFERENTRYTYPE": {
        "items": [
            "read-only-storage",
            "storage",
            "uniform"
        ]
    },
    "VARUSAGE": [
        "read",
        "write",
        "read_write",
        "function",
        "private",
        "workgroup",
        "uniform",
        "storage"
    ],
}

@fixture
def input_type_cls():
    cls, _ = process_all_menus(EXAMPLE_MENU_DATA)
    return cls

@fixture
def dropdown_type_cls():
    _, cls = process_all_menus(EXAMPLE_MENU_DATA)
    return cls

@fixture
def example_opcode_blocks(input_type_cls, dropdown_type_cls):
    return [
        (OpcodeInfo(
            opcode_type=OpcodeType.HAT,
            inputs=DualKeyDict({
                ("NAME", "NAME"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
                ("BGL", "BGL"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::Define shader (NAME) using bind group layout (BGL)"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("WGSIZE", "WGSIZE"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
                ("SUBSTACK", "SUBSTACK"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::Computer shader with workgroup size (WGSIZE) {SUBSTACK}"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.ENDING_STATEMENT,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::break"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::thread data"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=True,
            monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::Error"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("CONDITION1", "CONDITION1"): InputInfo(type=BuiltinInputType.BOOLEAN, menu=None),
                ("CONDITION2", "CONDITION2"): InputInfo(type=BuiltinInputType.BOOLEAN, menu=None),
                ("SUBSTACK", "SUBSTACK"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
                ("SUBSTACK2", "SUBSTACK2"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::if <CONDITION1> then {SUBSTACK} else if <CONDITION2> then {SUBSTACK2}"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("CONDITION1", "CONDITION1"): InputInfo(type=BuiltinInputType.BOOLEAN, menu=None),
                ("CONDITION2", "CONDITION2"): InputInfo(type=BuiltinInputType.BOOLEAN, menu=None),
                ("SUBSTACK", "SUBSTACK"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
                ("SUBSTACK2", "SUBSTACK2"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
                ("SUBSTACK3", "SUBSTACK3"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::if <CONDITION1> then {SUBSTACK} else if <CONDITION2> then {SUBSTACK2} else {SUBSTACK3} some unecessary text"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.BOOLEAN_REPORTER,
            inputs=DualKeyDict({
                ("a", "a"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::is (a) behind camera?"), (None, None), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("BINDING", "BINDING"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
                ("TYPE", "TYPE"): InputInfo(
                    type=input_type_cls.BGLENTRYTYPES,
                    menu=MenuInfo(opcode="someExtension_menu_BGLENTRYTYPES", inner="BGLENTRYTYPES"),
                ),
                ("DESC", "DESC"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::Add bind group layout entry with binding (BINDING) for type ([TYPE]) and descriptor (DESC)"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("VaLuE", "VaLuE"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
            }),
            dropdowns=DualKeyDict({
                ("VaRiAbLe", "VaRiAbLe"): DropdownInfo(type=BuiltinDropdownType.VARIABLE),
            }),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=True,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::set some var [VaRiAbLe] to (VaLuE)"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.ENDING_STATEMENT,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::restart from the top"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict({
                ("TYPE", "TYPE"): DropdownInfo(type=dropdown_type_cls.BUFFERENTRYTYPE),
            }),
            can_have_monitor=True,
            monitor_id_behaviour=MonitorIdBehaviour.OPCFULL_PARAMS,
            has_shadow=False,
            has_variable_id=True,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::Buffer layout entry descriptor with usage type [TYPE]"), 
        (OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict({
                ("NEXT", "NEXT"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
            }),
            dropdowns=DualKeyDict({
                ("USAGE", "USAGE"): DropdownInfo(type=dropdown_type_cls.VARUSAGE),
            }),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=True,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ), "someExtension::Variable usage [USAGE] next (NEXT)")
    ]


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



def test_generate_block_opcode_info_event_with_string_arg_without_type(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[0]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[0]

def test_generate_block_opcode_info_conditional_with_branchCount(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[1]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[1]

def test_generate_block_opcode_info_command_with_isTerminal_no_args(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[2]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[2]

def test_generate_block_opcode_info_reporter_with_disableMonitor_double_space(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[3]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[3]

def test_generate_block_opcode_info_can_have_monitor(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[4]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[4]

def test_generate_block_opcode_info_with_muliple_branches(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[5]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[5]

def test_generate_block_opcode_info_with_higher_branch_count_text_list(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[6]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[6]

def test_generate_block_opcode_info_boolean(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[7]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[7]

def test_generate_block_opcode_info_label(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[8]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[8]

def test_generate_block_opcode_info_with_dict_menu_with_accept_reporters_missing_arg(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[9]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[9]

def test_generate_block_opcode_info_with_variable_arg(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[10]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[10]

def test_generate_block_opcode_info_with_image(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[11]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[11]

def test_generate_block_opcode_info_with_dict_menu_without_accept_reporters(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[12]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[12]

def test_generate_block_opcode_info_with_list_menu(input_type_cls, dropdown_type_cls, example_opcode_blocks):
    block_data = EXAMPLE_BLOCK_DATA[13]
    opcode_block, new_opcode = generate_block_opcode_info(
        block_info=block_data,
        menus=EXAMPLE_MENU_DATA,
        input_type_cls=input_type_cls,
        dropdown_type_cls=dropdown_type_cls,
        extension_id="someExtension",
    )
    assert (opcode_block, new_opcode) == example_opcode_blocks[13]

def test_generate_block_opcode_info_invalid_is_terminal(input_type_cls, dropdown_type_cls):
    block_data = {
        "opcode": "break",
        "blockType": "reporter",
        "isTerminal": True,
        "text": "break"
    }
    with raises(PP_InvalidCustomBlockError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )

def test_generate_block_opcode_info_xml_block(input_type_cls, dropdown_type_cls):
    block_data = {
        "blockType": "xml",
        "xml": ..., # doesn't matter
    }
    with raises(PP_NotImplementedError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )

def test_generate_block_opcode_info_invalid_block_type(input_type_cls, dropdown_type_cls):
    block_data = {
        "blockType": "undefinedBlockType",
    }
    with raises(PP_InvalidCustomBlockError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )

def test_generate_block_opcode_info_unknown_attribute(input_type_cls, dropdown_type_cls):
    block_data = {
        "opcode": "break",
        "blockType": "command",
        "isTerminal": True,
        "text": "break",
        "undefinedProperty": "some value",
    }
    with raises(PP_UnknownExtensionAttributeError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )

def test_generate_block_opcode_info_invalid_menu_arg_type(input_type_cls, dropdown_type_cls):
    block_data = {
        "opcode": "bufferEntryDescriptor",
        "blockType": "reporter",
        "text": "Buffer layout entry descriptor with usage type [TYPE]",
        "arguments": {
            "TYPE": {
                "type": "number",
                "menu": "BUFFERENTRYTYPE"
            }
        }
    }
    with raises(PP_InvalidCustomBlockError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )

def test_generate_block_opcode_info_non_existant_menu_arg(input_type_cls, dropdown_type_cls):
    block_data = {
        "opcode": "bufferEntryDescriptor",
        "blockType": "reporter",
        "text": "Buffer layout entry descriptor with usage type [TYPE]",
        "arguments": {
            "TYPE": {
                "type": "string",
                "menu": "SomeUndefinedMenu"
            }
        }
    }
    with raises(PP_InvalidCustomBlockError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )

def test_generate_block_opcode_info_invalid_branch_count_text(input_type_cls, dropdown_type_cls):
    block_data = {
        "opcode": "ifElseIf",
        "text": [
            "if [CONDITION1] then",
            "else if [CONDITION2] then"
        ],
        "branchCount": 4, # too much
        "blockType": "conditional",
        "arguments": {
            "CONDITION1": { "type": "Boolean" },
            "CONDITION2": { "type": "Boolean" }
        }
    }
    with raises(PP_InvalidCustomBlockError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )

def test_generate_block_opcode_info_with_seperator_arg(input_type_cls, dropdown_type_cls):
    block_data = {
        "opcode": "computeFunc",
        "blockType": "conditional",
        "text": "Computer shader with workgroup size [WGSIZE]",
        "arguments": {
            "WGSIZE": {
                "type": "seperator"
            }
        },
        "branchCount": 1
    }
    with raises(PP_ThanksError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )

def test_generate_block_opcode_info_missing_attribute(input_type_cls, dropdown_type_cls):
    block_data = {
        "blockType": "command",
        "text": "some text",
    }
    with raises(PP_InvalidCustomBlockError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )
    
    block_data = {
        "opcode": "someOpcode",
        "text": "some text",
    }
    with raises(PP_InvalidCustomBlockError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )
    
    block_data = {
        "opcode": "someOpcode",
        "blockType": "command",
    }
    with raises(PP_InvalidCustomBlockError):
        generate_block_opcode_info(
            block_info=block_data,
            menus=EXAMPLE_MENU_DATA,
            input_type_cls=input_type_cls,
            dropdown_type_cls=dropdown_type_cls,
            extension_id="someExtension",
        )



def test_generate_opcode_info_group():
    extension_info = {
        "id": "modasyncexample",
        "name": "Async Blocks",
        "blocks": [
            {
                "opcode": "wait",
                "text": "wait [TIME] seconds",
                "blockType": "command",
                "arguments": {
                    "TIME": {
                        "type": "number",
                        "defaultValue": 1
                    }
                }
            },
            {
                "opcode": "fetch",
                "text": "fetch [URL]",
                "blockType": "reporter",
                "arguments": {
                    "URL": {
                        "type": "string",
                        "defaultValue": "https://extensions.turbowarp.org/hello.txt"
                    }
                }
            },
            {}, # HERE add menu block
        ]
    }
    info_group, input_type_cls, dropdown_type_cls = generate_opcode_info_group(extension_info)

    assert info_group == OpcodeInfoGroup(
        name="modasyncexample",
        opcode_info=DualKeyDict({
            ("modasyncexample_wait", "modasyncexample::wait (TIME) seconds"): OpcodeInfo(
                opcode_type=OpcodeType.STATEMENT,
                inputs=DualKeyDict({
                    ("TIME", "TIME"): InputInfo(type=BuiltinInputType.NUMBER, menu=None),
                }),
                dropdowns=DualKeyDict(),
            ),
            ("modasyncexample_fetch", "modasyncexample::fetch (URL)"): OpcodeInfo(
                opcode_type=OpcodeType.STRING_REPORTER,
                inputs=DualKeyDict({
                    ("URL", "URL"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
                }),
                dropdowns=DualKeyDict(),
            ),
        }),
    )

    input_type_members    = {member.name: member.value for member in input_type_cls   }
    dropdown_type_members = {member.name: member.value for member in dropdown_type_cls}
    assert set(input_type_members   .keys()) == set()
    assert set(dropdown_type_members.keys()) == set()

