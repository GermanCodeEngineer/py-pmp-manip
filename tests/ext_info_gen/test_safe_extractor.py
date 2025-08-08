from ast                    import literal_eval
from colorama               import Fore as ColorFore, Style as ColorStyle
from collections.abc        import Iterator
from pytest                 import raises, warns
from tree_sitter            import Parser, Language, Node, Tree
from tree_sitter_javascript import language as get_js_language_basis
from typing                 import Any
from types                  import NotImplementedType
from warnings               import warn

from pmp_manip.utility            import (
    repr_tree, gdumps,
    PP_JsNodeTreeToJsonConversionError, PP_InvalidExtensionCodeSyntaxError, PP_BadExtensionCodeFormatError, PP_InvalidTranslationMessageError,
    PP_UnexpectedPropertyAccessWarning, PP_UnexpectedNotPossibleFeatureWarning,
    NotSetType, NotSet,
    write_file_text, # temporary
)

from pmp_manip.ext_info_gen.safe_extractor import get_js_parser, ts_node_to_json, SCRATCH_STUB

EXAMPLE_EXTENSION_CODE = 0
   


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







