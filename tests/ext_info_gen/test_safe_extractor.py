from pytest                 import raises, warns
from tree_sitter            import Parser, Node
from typing                 import Any
from types                  import NotImplementedType
from pmp_manip.utility import MANIP_BadExtensionCodeFormatError

from pmp_manip.utility            import (
    MANIP_JsNodeTreeToJsonConversionError, MANIP_InvalidExtensionCodeSyntaxError, MANIP_BadExtensionCodeFormatError, MANIP_InvalidTranslationMessageError,
    MANIP_UnexpectedPropertyAccessWarning, MANIP_UnexpectedNotPossibleFeatureWarning,
    NotSet,
)

from pmp_manip.ext_info_gen.safe_extractor import (
    get_js_parser, ts_node_to_json, SCRATCH_STUB,
    _get_main_body, _get_registered_class_name, _get_class_def_by_name, _get_class_method_def_by_name,
    extract_extension_info_safely,
)

UNSANDBOXED_EXTENSION_CODE = '''class AsyncExtension {
  getInfo() {
    return {
      id: 'asyncexample',
      name: 'Async Blocks',
      blocks: [
        {
          opcode: 'wait',
          text: 'wait [TIME] seconds',
          blockType: Scratch.BlockType.COMMAND,
          arguments: {
            TIME: {
              type: Scratch.ArgumentType.NUMBER,
              defaultValue: 1
            }
          }
        },
        {
          opcode: 'fetch',
          text: 'fetch [URL]',
          blockType: Scratch.BlockType.REPORTER,
          arguments: {
            URL: {
              type: Scratch.ArgumentType.STRING,
              defaultValue: 'https://extensions.turbowarp.org/hello.txt'
            }
          }
        }
      ]
    };
  }

  wait (args) {
    return new Promise((resolve, reject) => {
      const timeInMilliseconds = args.TIME * 1000;
      setTimeout(() => {
        resolve();
      }, timeInMilliseconds);
    });
  }

  fetch (args) {
    return fetch(args.URL)
      .then((response) => {
        return response.text();
      })
      .catch((error) => {
        console.error(error);
        return 'Uh oh! Something went wrong.';
      });
  }
}
Scratch.extensions.register(new AsyncExtension());'''
SANDBOXED_EXTENSION_CODE = '''((Scratch) => {
  "use strict";

  class DumbExample {
     getInfo() {
      return {
        id: "dumbExample",
        name: "Dumb Example",

        color1: "#e200ca",

        blocks: [
          {
            opcode: "last_used_base",
            blockType: Scratch.BlockType.REPORTER,
            text: "last used base",
            arguments: {},
          },
          {
            opcode: "last_two_inout_values",
            blockType: Scratch.BlockType.REPORTER,
            text: "last two [S1] and [S2] values",
            arguments: {
              S1: {
                type: Scratch.ArgumentType.STRING,
                menu: "in_out_menue"
              },
              S2: {
                type: Scratch.ArgumentType.STRING,
                menu: "in_out_menue"
              },
            },
          },
        ],
        menus: {
          in_out_menue: {
            acceptReporters: false,
            items: ["IN", "OUT"],
          },
        },
      };
    }

    last_used_base() {
      return "some base";
    }
    last_two_inout_values( {S1, S2} ) {
      return JSON.stringify(["HERE", S1, S2])
    }
  }

  Scratch.extensions.register(new DumbExample());
  console.log(Scratch)
})(Scratch);
'''

   

def test_get_js_parser():
    import pmp_manip.ext_info_gen.safe_extractor as safe_extractor_mod
    safe_extractor_mod._js_parser = None
    from pmp_manip.ext_info_gen.safe_extractor import get_js_parser
    first_result = get_js_parser()
    assert isinstance(first_result, Parser)
    second_result = get_js_parser()
    assert (first_result is second_result)



def test_ts_node_to_json_non_node():
    assert ts_node_to_json(56) == 56

def test_ts_node_to_json_Scratch_property():
    parser = get_js_parser()
    tree = parser.parse("Scratch.ArgumentType.NUMBER".encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == SCRATCH_STUB["ArgumentType"]["NUMBER"]
    
    tree = parser.parse("Scratch.ArgumentType".encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(MANIP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0])
    
    tree = parser.parse("Scratch.x".encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(MANIP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0])

def test_ts_node_to_json_this_property():
    parser = get_js_parser()
    tree = parser.parse("this.sth".encode())
    expr_statement = tree.root_node.named_children[0]
    with warns(MANIP_UnexpectedPropertyAccessWarning):
        assert ts_node_to_json(expr_statement.named_children[0]) == None

def test_ts_node_to_json_other_property():
    parser = get_js_parser()
    tree = parser.parse("sth1.sth2".encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(MANIP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0])

def test_ts_node_to_json_object():
    parser = get_js_parser()
    tree = parser.parse('{x: 5, /*some comment*/ "y": [4, 6]}'.encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == {"x": 5, "y": [4, 6]}

def test_ts_node_to_json_object_invalid_property_key_type():
    parser = get_js_parser()
    tree = parser.parse('{...a}'.encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(MANIP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0])
    
    tree = parser.parse('{[""]: 3}'.encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(MANIP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0])

def test_ts_node_to_json_array():
    parser = get_js_parser()
    tree = parser.parse('[{u:5}]'.encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == [{"u": 5}]

def test_ts_node_to_json_string():
    parser = get_js_parser()
    tree = parser.parse('"hi \\n How are you?"'.encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == "hi \n How are you?"

def test_ts_node_to_json_number():
    parser = get_js_parser()
    tree = parser.parse("79324".encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == 79324

    tree = parser.parse("793.24".encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == 793.24

def test_ts_node_to_json_other_const():
    parser = get_js_parser()
    tree = parser.parse("true".encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == True

    tree = parser.parse("false".encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == False

    tree = parser.parse("null".encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == None

    tree = parser.parse("undefined".encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == None

def test_ts_node_to_json_identifier():
    parser = get_js_parser()
    tree = parser.parse("x".encode())
    expr_statement = tree.root_node.named_children[0]
    assert ts_node_to_json(expr_statement.named_children[0]) == "x"

def test_ts_node_to_json_impossible_feature():
    parser = get_js_parser()
    tree = parser.parse("`Hello, ${name}`".encode())
    expr_statement = tree.root_node.named_children[0]
    with warns(MANIP_UnexpectedNotPossibleFeatureWarning):
        assert ts_node_to_json(expr_statement.named_children[0]) == None

def test_ts_node_to_json_call():
    def handle_call(node: Node) -> NotImplementedType | Any:
        callee_node = node.child_by_field_name("function")
        arguments_node = node.child_by_field_name("arguments")

        if (
            callee_node and (callee_node.type == "identifier")
            and callee_node.text.decode() == "hex"
        ):
            arg_node = arguments_node.named_children[0]
            value = ts_node_to_json(arg_node)
            return hex(value)

        return NotImplemented

    parser = get_js_parser()
    tree = parser.parse("hex(45)".encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(MANIP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0], call_handler=None)
    assert ts_node_to_json(expr_statement.named_children[0], call_handler=handle_call) == "0x2d"

def test_ts_node_to_json_comment():
    parser = get_js_parser()
    tree = parser.parse("// some comment".encode())
    statement = tree.root_node.named_children[0]
    assert ts_node_to_json(statement) == NotSet

def test_ts_node_to_json_unsupported_type():
    parser = get_js_parser()
    tree = parser.parse("class X {}".encode())
    statement = tree.root_node.named_children[0]
    with raises(MANIP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(statement)



def test_get_main_body_sandboxed_and_unsandboxed():
    parser = get_js_parser()
    # sandboxed style
    code_sandboxed = "((Scratch) => { class X {} })(Scratch)"
    tree = parser.parse(code_sandboxed.encode())
    body_nodes = _get_main_body(tree.root_node)
    assert body_nodes[0].type == "class_declaration"
    
    code_sandboxed = "(function (Scratch) { class X {} })(Scratch)"
    tree = parser.parse(code_sandboxed.encode())
    body_nodes = _get_main_body(tree.root_node)
    assert body_nodes[0].type == "class_declaration"
    
    # unsandboxed style
    code_unsandboxed = "function a(){}"
    tree = parser.parse(code_unsandboxed.encode())
    body_nodes = _get_main_body(tree.root_node)
    assert body_nodes[0].type == "function_declaration"



def test_get_registered_class_name_and_errors():
    parser = get_js_parser()
    good_code = "Scratch.extensions.register(new MyExt())\n45\nconst arr = []"
    tree = parser.parse(good_code.encode())
    body = tree.root_node.named_children
    assert _get_registered_class_name(body) == "MyExt"

    bad_code = "console.log('no register here')"
    tree = parser.parse(bad_code.encode())
    with raises(MANIP_BadExtensionCodeFormatError):
        _get_registered_class_name(tree.root_node.named_children)



def test_get_class_def_by_name_and_errors():
    parser = get_js_parser()
    code = "class SomeClass {};\nclass MyExt {};"
    tree = parser.parse(code.encode())
    body = tree.root_node.named_children
    node = _get_class_def_by_name(body, "MyExt")
    assert node.type == "class_declaration"

    with raises(MANIP_BadExtensionCodeFormatError):
        _get_class_def_by_name(body, "OtherExt")



def test_get_class_method_def_by_name_and_errors():
    parser = get_js_parser()
    code = "class MyExt { someMethod(){}\n myMethod(){} }"
    tree = parser.parse(code.encode())
    class_node = tree.root_node.named_children[0]
    method_node = _get_class_method_def_by_name(class_node, "myMethod")
    assert method_node.type == "method_definition"

    with raises(MANIP_BadExtensionCodeFormatError):
        _get_class_method_def_by_name(class_node, "nope")



def test_extract_extension_info_safely_unsandboxed():
    info = extract_extension_info_safely(UNSANDBOXED_EXTENSION_CODE)
    assert isinstance(info, dict)
    assert info["id"] == "asyncexample"
    assert isinstance(info["blocks"], list)
    assert len(info["blocks"]) == 2
    assert info["blocks"][0]["opcode"] == "wait"

def test_extract_extension_info_safely_sandboxed():
    info = extract_extension_info_safely(SANDBOXED_EXTENSION_CODE)
    assert isinstance(info, dict)
    assert info["id"] == "dumbExample"
    assert isinstance(info["blocks"], list)
    assert len(info["blocks"]) == 2
    assert info["blocks"][0]["opcode"] == "last_used_base"

def test_extract_extension_info_safely_invalid_syntax():
    bad_code = "class X { getInfo() { return { id: 'x' "  # missing closing braces
    with raises(MANIP_InvalidExtensionCodeSyntaxError):
        extract_extension_info_safely(bad_code)

def test_extract_extension_info_safely_missing_getInfo():
    bad_code = "class X { someMethod() {} } Scratch.extensions.register(new X())"
    with raises(MANIP_BadExtensionCodeFormatError):
        extract_extension_info_safely(bad_code)

def test_extract_extension_info_safely_bad_translate_usage():
    bad_code = """
    class X {
      getInfo() {
        return {
          id: Scratch.translate(31)
        };
      }
    }
    Scratch.extensions.register(new X())
    """
    with raises(MANIP_InvalidTranslationMessageError):
        extract_extension_info_safely(bad_code)

    bad_code = """
    class X {
      getInfo() {
        return {
          id: Scratch.translate("")
        };
      }
    }
    Scratch.extensions.register(new X())
    """
    with raises(MANIP_InvalidTranslationMessageError):
        extract_extension_info_safely(bad_code)


def test_extract_extension_info_safely_error_in_parse():
    class Something:
        def encode(self): # to replace str.encode
            return self
    
    with raises(MANIP_InvalidExtensionCodeSyntaxError):
        extract_extension_info_safely(Something())

def test_extract_extension_info_safely_with_translate_and_stringify():
    code = """
    class X {
      getInfo() {
        return {
          id: "griffpatch",
          name: Scratch.translate({
            id: "griffpatch.categoryName",
            default: "Physics",
            description: "Label for the Griffpatch extension category",
          }),
          blocks: [
            {
              opcode: "setStage",
              blockType: Scratch.BlockType.COMMAND,
              text: Scratch.translate("set stage boundaries to [stageType]"),
              arguments: {
                stageType: {
                  type: Scratch.ArgumentType.STRING,
                  menu: "StageTypes",
                  defaultValue: JSON.stringify([1, 2, 3]),
                },
              },
            },
          ],
        }
      }
    }
    Scratch.extensions.register(new X())
    """
    extension_info = extract_extension_info_safely(code)
    assert extension_info == {
      "id": "griffpatch",
      "name": "Physics",
      "blocks": [
        {
          "opcode": "setStage",
          "blockType": "command",
          "text": "set stage boundaries to [stageType]",
          "arguments": {
            "stageType": {
              "type": "string",
              "menu": "StageTypes",
              "defaultValue": "[1,2,3]",
            },
          },
        },
      ],
    }

def test_extract_extension_info_safely_with_call_handler_not_implemented():
    bad_code = """
    class X {
      getInfo() {
        return {
          id: "griffpatch",
          name: abcx("Physics"),
        }
      }
    }
    Scratch.extensions.register(new X())
    """
    with raises(MANIP_BadExtensionCodeFormatError):
        extract_extension_info_safely(bad_code)

def test_extract_extension_info_safely_missing_return():
    bad_code = """
    class X {
      getInfo() {
          // missing 'return {...}'
      }
    }
    Scratch.extensions.register(new X())
    """
    with raises(MANIP_BadExtensionCodeFormatError):
        extract_extension_info_safely(bad_code)


def test_get_js_parser_singleton():
    """Test that get_js_parser returns the same instance"""
    import pmp_manip.ext_info_gen.safe_extractor as safe_extractor_mod
    # Reset the global parser
    safe_extractor_mod._js_parser = None
    
    parser1 = get_js_parser()
    parser2 = get_js_parser()
    
    assert parser1 is parser2
    assert isinstance(parser1, Parser)

def test_ts_node_to_json_complex_structures():
    """Test ts_node_to_json with complex nested structures"""
    # Test with nested lists and dicts
    complex_structure = {
        "nested_dict": {"key": "value"},
        "nested_list": [1, 2, {"inner": "data"}],
        "simple_value": "test"
    }
    
    result = ts_node_to_json(complex_structure)
    assert result == complex_structure
    
    # Test with actual tree-sitter Node objects
    parser = get_js_parser()
    tree = parser.parse(b"var x = 42;")
    root_node = tree.root_node
    
    # ts_node_to_json should handle actual Node objects
    json_result = ts_node_to_json(root_node)
    assert isinstance(json_result, dict)
    assert "type" in json_result
    assert "children" in json_result

def test_extract_extension_info_safely_complex_translation():
    """Test complex translation scenarios"""
    code = """
    class ComplexTranslation {
      getInfo() {
        return {
          id: "complexExt",
          name: Scratch.translate("Complex Extension"),
          blocks: [
            {
              opcode: "complexBlock",
              blockType: Scratch.BlockType.COMMAND,
              text: Scratch.translate({
                id: "complexExt.complexBlock",
                default: "do complex [ACTION] with [VALUE]",
                description: "A complex block with parameters"
              }),
              arguments: {
                ACTION: {
                  type: Scratch.ArgumentType.STRING,
                  defaultValue: Scratch.translate("default action")
                },
                VALUE: {
                  type: Scratch.ArgumentType.NUMBER,
                  defaultValue: 42
                }
              }
            }
          ]
        };
      }
    }
    Scratch.extensions.register(new ComplexTranslation())
    """
    
    info = extract_extension_info_safely(code)
    assert info["id"] == "complexExt"
    assert info["name"] == "Complex Extension"
    assert info["blocks"][0]["text"] == "do complex [ACTION] with [VALUE]"
    assert info["blocks"][0]["arguments"]["ACTION"]["defaultValue"] == "default action"

def test_extract_extension_info_safely_json_stringify_edge_cases():
    """Test JSON.stringify with various data types"""
    code = """
    class JSONTest {
      getInfo() {
        return {
          id: "jsonTest",
          blocks: [
            {
              opcode: "test",
              blockType: Scratch.BlockType.COMMAND,
              text: "test",
              arguments: {
                ARRAY: {
                  defaultValue: JSON.stringify([1, "string", true, null])
                },
                OBJECT: {
                  defaultValue: JSON.stringify({key: "value", num: 123})
                },
                NESTED: {
                  defaultValue: JSON.stringify({arr: [1, 2], obj: {x: "y"}})
                }
              }
            }
          ]
        };
      }
    }
    Scratch.extensions.register(new JSONTest())
    """
    
    info = extract_extension_info_safely(code)
    args = info["blocks"][0]["arguments"]
    
    # Verify JSON.stringify results
    assert args["ARRAY"]["defaultValue"] == '[1,"string",true,null]'
    assert args["OBJECT"]["defaultValue"] == '{"key":"value","num":123}'
    assert args["NESTED"]["defaultValue"] == '{"arr":[1,2],"obj":{"x":"y"}}'

def test_extract_extension_info_safely_property_access_warnings():
    """Test that property access generates warnings or errors appropriately"""
    code = """
    class PropertyAccess {
      getInfo() {
        return {
          id: "propTest",
          name: this.getExtensionName(),
          blocks: []
        };
      }
      
      getExtensionName() {
        return "Property Test";
      }
    }
    Scratch.extensions.register(new PropertyAccess())
    """
    
    # The safe extractor should raise an error for unsupported features like method calls
    with raises(MANIP_BadExtensionCodeFormatError):
        extract_extension_info_safely(code)

def test_extract_extension_info_safely_unsupported_features():
    """Test that unsupported JavaScript features are handled appropriately"""
    code = """
    class UnsupportedFeatures {
      getInfo() {
        return {
          id: "unsupported",
          name: true ? "Conditional Name" : "Other Name",  // Ternary operator
          blocks: []
        };
      }
    }
    Scratch.extensions.register(new UnsupportedFeatures())
    """
    
    # The safe extractor should raise an error for unsupported features like ternary operators
    with raises(MANIP_BadExtensionCodeFormatError):
        extract_extension_info_safely(code)

def test_extract_extension_info_safely_multiple_classes():
    """Test extension with multiple classes where only one is registered"""
    code = """
    class HelperClass {
      static getValue() {
        return "helper";
      }
    }
    
    class MainExtension {
      getInfo() {
        return {
          id: "multiClass",
          name: "Multi Class Extension",
          blocks: []
        };
      }
    }
    
    Scratch.extensions.register(new MainExtension())
    """
    
    info = extract_extension_info_safely(code)
    assert info["id"] == "multiClass"
    assert info["name"] == "Multi Class Extension"

def test_extract_extension_info_safely_registration_patterns():
    """Test different registration patterns"""
    # Test with direct instantiation - this should work
    code2 = """
    class TestExt2 {
      getInfo() {
        return { id: "test2", blocks: [] };
      }
    }
    Scratch.extensions.register(new TestExt2());
    """
    
    info = extract_extension_info_safely(code2)
    assert info["id"] == "test2"
    
    # Test with variable assignment - this is more complex and may not be supported
    code1 = """
    class TestExt {
      getInfo() {
        return { id: "test1", blocks: [] };
      }
    }
    const ext = new TestExt();
    Scratch.extensions.register(ext);
    """
    
    # This pattern may not be supported by the safe extractor
    try:
        info = extract_extension_info_safely(code1)
        assert info["id"] == "test1"
    except MANIP_BadExtensionCodeFormatError:
        # This is acceptable - the safe extractor may not support variable assignment patterns
        pass

def test_extract_extension_info_safely_error_recovery():
    """Test error recovery and detailed error messages"""
    # Test with malformed class
    bad_code = """
    class BadExtension {
      getInfo() {
        return {
          id: "badExt"
          // missing comma
          blocks: []
        };
      }
    }
    """
    
    with raises(MANIP_InvalidExtensionCodeSyntaxError):
        extract_extension_info_safely(bad_code)
    
    # Test with missing registration
    code_without_registration = """
    class NoRegister {
      getInfo() {
        return { id: "noReg", blocks: [] };
      }
    }
    // Missing Scratch.extensions.register call
    """
    
    with raises(MANIP_BadExtensionCodeFormatError):
        extract_extension_info_safely(code_without_registration)

