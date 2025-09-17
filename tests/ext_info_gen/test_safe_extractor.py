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


# Additional comprehensive tests for safe extractor functionality

def test_ts_node_to_json_complex_objects():
    """Test complex object structures in JavaScript AST"""
    parser = get_js_parser()
    
    # Test nested objects
    nested_code = """{
        outer: {
            inner: {
                value: 42,
                list: [1, 2, 3]
            }
        }
    }"""
    tree = parser.parse(nested_code.encode())
    expr_statement = tree.root_node.named_children[0]
    result = ts_node_to_json(expr_statement.named_children[0])
    
    expected = {
        "outer": {
            "inner": {
                "value": 42,
                "list": [1, 2, 3]
            }
        }
    }
    assert result == expected

def test_ts_node_to_json_arrays_with_different_types():
    """Test arrays containing different JavaScript types"""
    parser = get_js_parser()
    
    mixed_array = '[42, "string", true, null, {key: "value"}]'
    tree = parser.parse(mixed_array.encode())
    expr_statement = tree.root_node.named_children[0]
    result = ts_node_to_json(expr_statement.named_children[0])
    
    expected = [42, "string", True, None, {"key": "value"}]
    assert result == expected

def test_extract_extension_info_safely_complex_extensions():
    """Test safe extraction with complex, realistic extension structures"""
    
    complex_extension = '''
    class ComplexExtension {
        getInfo() {
            return {
                id: "complex",
                name: "Complex Extension",
                color1: "#FF0000",
                menuIconURI: "data:image/svg+xml;base64,PHN2Zw==",
                blocks: [
                    {
                        opcode: "multiArgumentBlock",
                        blockType: Scratch.BlockType.COMMAND,
                        text: "do [ACTION] with [VALUE] and [OPTION]",
                        arguments: {
                            ACTION: {
                                type: Scratch.ArgumentType.STRING,
                                defaultValue: "something"
                            },
                            VALUE: {
                                type: Scratch.ArgumentType.NUMBER,
                                defaultValue: 10
                            },
                            OPTION: {
                                type: Scratch.ArgumentType.STRING,
                                menu: "optionMenu"
                            }
                        }
                    },
                    {
                        opcode: "reporterBlock",
                        blockType: Scratch.BlockType.REPORTER,
                        text: "get [PROPERTY]",
                        arguments: {
                            PROPERTY: {
                                type: Scratch.ArgumentType.STRING,
                                menu: "propertyMenu"
                            }
                        }
                    }
                ],
                menus: {
                    optionMenu: {
                        acceptReporters: true,
                        items: ["option1", "option2", "option3"]
                    },
                    propertyMenu: {
                        items: [
                            {text: "Width", value: "width"},
                            {text: "Height", value: "height"}
                        ]
                    }
                }
            };
        }
    }
    Scratch.extensions.register(new ComplexExtension());
    '''
    
    result = extract_extension_info_safely(complex_extension)
    
    assert result["id"] == "complex"
    assert len(result["blocks"]) == 2
    assert "menus" in result
    assert "optionMenu" in result["menus"]
    assert "propertyMenu" in result["menus"]

def test_extract_extension_info_safely_with_comments():
    """Test extraction with JavaScript comments"""
    
    commented_extension = '''
    // This is a test extension
    class TestExtension {
        // Get extension information
        getInfo() {
            return {
                id: "test", // Extension ID
                name: "Test Extension", /* Extension name */
                blocks: [
                    // First block
                    {
                        opcode: "testBlock",
                        blockType: Scratch.BlockType.COMMAND,
                        text: "test command"
                    }
                    // More blocks could go here
                ]
            };
        }
    }
    
    // Register the extension
    Scratch.extensions.register(new TestExtension());
    '''
    
    result = extract_extension_info_safely(commented_extension)
    assert result["id"] == "test"
    assert len(result["blocks"]) == 1

def test_extract_extension_info_safely_syntax_error_reporting():
    """Test detailed syntax error reporting"""
    
    syntax_error_code = '''
    class BadExtension {
        getInfo() {
            return {
                id: "bad",
                blocks: [
                    {
                        opcode: "badBlock"
                        // Missing comma here causes syntax error
                        blockType: Scratch.BlockType.COMMAND
                    }
                ]
            };
        }
    }
    '''
    
    with raises(MANIP_InvalidExtensionCodeSyntaxError) as exc_info:
        extract_extension_info_safely(syntax_error_code)
    
    error_message = str(exc_info.value)
    assert "Syntax error(s) detected:" in error_message
    assert "At line" in error_message

def test_extract_extension_info_safely_function_style():
    """Test extraction with function-style extension (limited support)"""
    
    # The safe extractor expects class-style extensions, not function-style
    # This test verifies that function-style extensions are properly rejected
    function_extension = '''
    (function(Scratch) {
        function FunctionExtension() {}
        
        FunctionExtension.prototype.getInfo = function() {
            return {
                id: "function",
                name: "Function Extension",
                blocks: []
            };
        };
        
        Scratch.extensions.register(new FunctionExtension());
    })(Scratch);
    '''
    
    # Function-style extensions are not supported by the safe extractor
    with raises(MANIP_BadExtensionCodeFormatError):
        extract_extension_info_safely(function_extension)

def test_extract_extension_info_safely_translation_edge_cases():
    """Test edge cases in Scratch.translate handling"""
    
    translation_extension = '''
    class TranslationExtension {
        getInfo() {
            return {
                id: "translation",
                name: Scratch.translate({
                    default: "Translation Test",
                    description: "Test extension for translations"
                }),
                blocks: [
                    {
                        opcode: "translatedBlock",
                        blockType: Scratch.BlockType.COMMAND,
                        text: Scratch.translate("execute command")
                    }
                ]
            };
        }
    }
    Scratch.extensions.register(new TranslationExtension());
    '''
    
    result = extract_extension_info_safely(translation_extension)
    assert result["name"] == "Translation Test"
    assert result["blocks"][0]["text"] == "execute command"

def test_get_main_body_edge_cases():
    """Test edge cases in main body extraction"""
    parser = get_js_parser()
    
    # Test with arrow function in parentheses
    arrow_code = "((Scratch) => { class Test {} })(Scratch)"
    tree = parser.parse(arrow_code.encode())
    body_nodes = _get_main_body(tree.root_node)
    assert body_nodes[0].type == "class_declaration"
    
    # Test with regular function expression
    func_code = "(function(Scratch) { class Test {} })(Scratch)"
    tree = parser.parse(func_code.encode())
    body_nodes = _get_main_body(tree.root_node)
    assert body_nodes[0].type == "class_declaration"

def test_extract_extension_info_safely_json_stringify_usage():
    """Test handling of JSON.stringify calls"""
    
    stringify_extension = '''
    class StringifyExtension {
        getInfo() {
            const config = {setting: "value"};
            return {
                id: "stringify",
                name: "Stringify Test",
                blocks: [
                    {
                        opcode: "configBlock",
                        blockType: Scratch.BlockType.REPORTER,
                        text: "config as string",
                        arguments: {
                            CONFIG: {
                                type: Scratch.ArgumentType.STRING,
                                defaultValue: JSON.stringify(config)
                            }
                        }
                    }
                ]
            };
        }
    }
    Scratch.extensions.register(new StringifyExtension());
    '''
    
    result = extract_extension_info_safely(stringify_extension)
    default_value = result["blocks"][0]["arguments"]["CONFIG"]["defaultValue"]
    # The safe extractor sees 'config' as an identifier, not the object value
    assert default_value == '"config"'

def test_extract_extension_info_safely_malformed_structures():
    """Test handling of malformed but syntactically valid structures"""
    
    # Test with missing required fields but valid return statement (no comments after return)
    minimal_extension = '''
    class MinimalExtension {
        getInfo() {
            return {};
        }
    }
    Scratch.extensions.register(new MinimalExtension());
    '''
    
    result = extract_extension_info_safely(minimal_extension)
    assert isinstance(result, dict)
    assert result == {}
    
    # Test with truly malformed structure (missing return)
    malformed_extension = '''
    class MalformedExtension {
        getInfo() {
            const info = {};
            // Missing return statement - this should fail
        }
    }
    Scratch.extensions.register(new MalformedExtension());
    '''
    
    with raises(MANIP_BadExtensionCodeFormatError):
        extract_extension_info_safely(malformed_extension)

def test_ts_node_to_json_with_complex_call_handler():
    """Test complex call handler scenarios"""
    
    def complex_call_handler(node):
        callee_node = node.child_by_field_name("function")
        if callee_node and callee_node.type == "member_expression":
            obj = callee_node.child_by_field_name("object")
            prop = callee_node.child_by_field_name("property")
            if obj and prop:
                obj_name = obj.text.decode()
                prop_name = prop.text.decode()
                if obj_name == "Math" and prop_name == "max":
                    args_node = node.child_by_field_name("arguments")
                    args = [ts_node_to_json(arg) for arg in args_node.named_children]
                    return max(args) if args else 0
        return NotImplemented
    
    parser = get_js_parser()
    tree = parser.parse("Math.max(10, 20, 5)".encode())
    expr_statement = tree.root_node.named_children[0]
    result = ts_node_to_json(expr_statement.named_children[0], call_handler=complex_call_handler)
    
    assert result == 20

