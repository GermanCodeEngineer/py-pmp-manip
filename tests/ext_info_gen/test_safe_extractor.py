from ast                    import literal_eval
from colorama               import Fore as ColorFore, Style as ColorStyle
from collections.abc        import Iterator
from pytest                 import raises, warns
from tree_sitter            import Parser, Language, Node, Tree
from tree_sitter_javascript import language as get_js_language_basis
from typing                 import Any
from types                  import NotImplementedType
from warnings               import warn
import pytest
from pmp_manip.ext_info_gen import safe_extractor
from pmp_manip.utility import PP_BadExtensionCodeFormatError

from pmp_manip.utility            import (
    repr_tree, gdumps,
    PP_JsNodeTreeToJsonConversionError, PP_InvalidExtensionCodeSyntaxError, PP_BadExtensionCodeFormatError, PP_InvalidTranslationMessageError,
    PP_UnexpectedPropertyAccessWarning, PP_UnexpectedNotPossibleFeatureWarning,
    NotSetType, NotSet,
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
    with raises(PP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0])
    
    tree = parser.parse("Scratch.x".encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(PP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0])

def test_ts_node_to_json_this_property():
    parser = get_js_parser()
    tree = parser.parse("this.sth".encode())
    expr_statement = tree.root_node.named_children[0]
    with warns(PP_UnexpectedPropertyAccessWarning):
        assert ts_node_to_json(expr_statement.named_children[0]) == None

def test_ts_node_to_json_other_property():
    parser = get_js_parser()
    tree = parser.parse("sth1.sth2".encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(PP_JsNodeTreeToJsonConversionError):
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
    with raises(PP_JsNodeTreeToJsonConversionError):
        ts_node_to_json(expr_statement.named_children[0])
    
    tree = parser.parse('{[""]: 3}'.encode())
    expr_statement = tree.root_node.named_children[0]
    with raises(PP_JsNodeTreeToJsonConversionError):
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
    with warns(PP_UnexpectedNotPossibleFeatureWarning):
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
    with raises(PP_JsNodeTreeToJsonConversionError):
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
    with raises(PP_JsNodeTreeToJsonConversionError):
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
    with raises(PP_BadExtensionCodeFormatError):
        _get_registered_class_name(tree.root_node.named_children)



def test_get_class_def_by_name_and_errors():
    parser = get_js_parser()
    code = "class SomeClass {};\nclass MyExt {};"
    tree = parser.parse(code.encode())
    body = tree.root_node.named_children
    node = _get_class_def_by_name(body, "MyExt")
    assert node.type == "class_declaration"

    with raises(PP_BadExtensionCodeFormatError):
        _get_class_def_by_name(body, "OtherExt")



def test_get_class_method_def_by_name_and_errors():
    parser = get_js_parser()
    code = "class MyExt { someMethod(){}\n myMethod(){} }"
    tree = parser.parse(code.encode())
    class_node = tree.root_node.named_children[0]
    method_node = _get_class_method_def_by_name(class_node, "myMethod")
    assert method_node.type == "method_definition"

    with raises(PP_BadExtensionCodeFormatError):
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
    with raises(PP_InvalidExtensionCodeSyntaxError):
        extract_extension_info_safely(bad_code)

def test_extract_extension_info_safely_missing_getInfo():
    bad_code = "class X { someMethod() {} } Scratch.extensions.register(new X())"
    with raises(PP_BadExtensionCodeFormatError):
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
    with raises(PP_InvalidTranslationMessageError):
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
    with raises(PP_InvalidTranslationMessageError):
        extract_extension_info_safely(bad_code)


def test_extract_extension_info_safely_error_in_parse():
    class Something:
        def encode(self): # to replace str.encode
            return self
    
    with raises(PP_InvalidExtensionCodeSyntaxError):
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
    with raises(PP_BadExtensionCodeFormatError):
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
    with raises(PP_BadExtensionCodeFormatError):
        extract_extension_info_safely(bad_code)

