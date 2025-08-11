from ast                    import literal_eval
from colorama               import Fore as ColorFore, Style as ColorStyle
from collections.abc        import Iterator
from tree_sitter            import Parser, Language, Node, Tree
from tree_sitter_javascript import language as get_js_language_basis
from typing                 import Any, Callable
from types                  import NotImplementedType
from warnings               import warn

from pmp_manip.utility            import (
    repr_tree, gdumps,
    MANIP_JsNodeTreeToJsonConversionError, MANIP_InvalidExtensionCodeSyntaxError, MANIP_BadExtensionCodeFormatError, MANIP_InvalidTranslationMessageError,
    MANIP_UnexpectedPropertyAccessWarning, MANIP_UnexpectedNotPossibleFeatureWarning,
    NotSetType, NotSet,
)


SCRATCH_STUB = { # Must be kept in sync with direct_extractor.js
    "ArgumentAlignment": {
        "DEFAULT": None,
        "LEFT": "LEFT",
        "CENTER": "CENTRE",
        "RIGHT": "RIGHT"
    },
    "ArgumentType": {
        "ANGLE": "angle",
        "BOOLEAN": "Boolean",
        "COLOR": "color",
        "NUMBER": "number",
        "STRING": "string",
        "MATRIX": "matrix",
        "NOTE": "note",
        "IMAGE": "image",
        "POLYGON": "polygon",
        "COSTUME": "costume",
        "SOUND": "sound",
        "VARIABLE": "variable",
        "LIST": "list",
        "BROADCAST": "broadcast",
        "SEPERATOR": "seperator"
    },
    "BlockShape": {
        "HEXAGONAL": 1,
        "ROUND": 2,
        "SQUARE": 3,
        "LEAF": 4,
        "PLUS": 5
    },
    "BlockType": {
        "BOOLEAN": "Boolean",
        "BUTTON": "button",
        "LABEL": "label",
        "COMMAND": "command",
        "CONDITIONAL": "conditional",
        "EVENT": "event",
        "HAT": "hat",
        "LOOP": "loop",
        "REPORTER": "reporter",
        "XML": "xml"
    },
    "TargetType": {
        "SPRITE": "sprite",
        "STAGE": "stage"
    },
    "extensions": {
        #"unsandboxed": True , # has not ever been needed, uncomment when needed
        #"isPenguinMod": True, # has not ever been needed, uncomment when needed
        # .register is handled somewhere else
    },
}

_js_parser: Parser | None = None


def get_js_parser() -> Parser:
    """
    Returns the global tree sitter JavaScript Parser instance. Loads the Parser's Language at first execution
    """
    global _js_parser
    if _js_parser is None:
        language = Language(get_js_language_basis())
        _js_parser = Parser(language=language)
    return _js_parser

def ts_node_to_json(
    node: Node | str | int | float | bool | None, 
    call_handler: Callable[[Node], Any | NotImplementedType] | None = None,
) -> Any | NotSetType:
    """
    Recursively converts a tree sitter Syntax Tree into a plain JSON-compatible Python structure

    Args:
        node: the root node or a subnode
        call_handler: a callable handling call expression nodes (should return NotImplemented if node not addressed by handler)

    Returns:
        A Python object representing the JSON-equivalent value: dict, list, str, int, float, bool, or None

    Raises:
        MANIP_JsNodeTreeToJsonConversionError: If an unsupported node type or a member expression of unexptected format is encountered
    
    Warnings:
        MANIP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed
        MANIP_UnexpectedNotPossibleFeatureWarning: if a impossible to implement feature is used (eg. ternary expr)
    """

    if isinstance(node, (str, int, float, bool, type(None))):
        return node

    if node.type == "member_expression":
        # try to handle eg. Scratch.ArgumentType.STRING
        object_node = node.child_by_field_name("object")
        property_node = node.child_by_field_name("property")

        if object_node.type == "member_expression":
            inner_obj = object_node.child_by_field_name("object")
            inner_prop = object_node.child_by_field_name("property")
            if (inner_obj.type in {"identifier", "property_identifier"}) and (inner_obj.text.decode() == "Scratch"):
                outer_key = inner_prop.text.decode()
                inner_key = property_node.text.decode()
                if (outer_key in SCRATCH_STUB) and (inner_key in SCRATCH_STUB[outer_key]):
                    return SCRATCH_STUB[outer_key][inner_key]

        elif object_node.type == "this":
            warn(f"{ColorFore.YELLOW}Tried to access property of 'this': {property_node.text.decode()}. "
                 f"Defaulting to None{ColorStyle.RESET_ALL}", MANIP_UnexpectedPropertyAccessWarning)
            return None

        raise MANIP_JsNodeTreeToJsonConversionError(f"Unsupported member expression format:\n{repr_tree(node, indent=1)}")

    elif node.type == "object":
        result = {}
        for prop in node.named_children:
            if   prop.type == "comment": continue
            elif prop.type != "pair":
                raise MANIP_JsNodeTreeToJsonConversionError(f"Unsupported property type: {prop.type}")

            key_node = prop.child_by_field_name("key")
            value_node = prop.child_by_field_name("value")

            if key_node.type in {"identifier", "property_identifier"}:
                key = key_node.text.decode()
            elif key_node.type == "string":
                key = literal_eval(key_node.text.decode().replace('`', '"'))
            else:
                raise MANIP_JsNodeTreeToJsonConversionError(f"Unsupported key type: {key_node.type}")

            result[key] = ts_node_to_json(value_node, call_handler) # cant return NotSet
        return result

    elif node.type == "array":
        array = []
        for child in node.named_children:
            result = ts_node_to_json(child, call_handler)
            if result is not NotSet:
                array.append(result)
        return array

    elif node.type == "string":
        return literal_eval(node.text.decode())
    
    elif node.type == "number":
        code = node.text.decode()
        return float(code) if "." in code else int(code)
    elif node.type == "true":
        return True
    elif node.type == "false":
        return False
    elif node.type == "null":
        return None
    elif node.type == "undefined":
        return None

    elif node.type == "identifier":
        return node.text.decode()

    elif node.type in {
        "template_string", 
        "ternary_expression", "binary_expression", "unary_expression"
    }:
        warn(f"{ColorFore.YELLOW}Not Implementable Feature {node.type!r} encountered. Defaulting to None{ColorStyle.RESET_ALL}", MANIP_UnexpectedNotPossibleFeatureWarning)
        return None
        # I am assuming/hoping that only less/not relevant properties are generated with these features

    elif (node.type == "call_expression") and bool(call_handler):
        value = call_handler(node)
        if value is not NotImplemented:
            return value
    
    elif (node.type == "comment"):
        return NotSet

    raise MANIP_JsNodeTreeToJsonConversionError(f"Unsupported node type: {node.type}")

def _get_main_body(root_node: Node) -> list[Node]:
    """
    Get the main code body
    
    Args:
        root_node: the JavaScript Syntax Tree
    """
    # Check for IIFE '((Scratch) => {...})(Scratch)' (sandboxed style)
    if root_node.type == "program":
        last = root_node.children[-1]
        if last.type == "expression_statement" and last.named_children:
            expr = last.named_children[0]
            if expr.type == "call_expression":
                func = expr.child_by_field_name("function")
                if   func and func.type == "parenthesized_expression":
                    func = func.named_children[0]
                if   func and func.type == "arrow_function":
                    body = func.child_by_field_name("body")
                    if body and body.type == "statement_block":
                        return body.named_children
                elif func and func.type == "function_expression":
                    body = func.child_by_field_name("body")
                    if body and body.type == "statement_block":
                        return body.named_children

    # Otherwise assume unsandboxed style
    return root_node.named_children

def _get_registered_class_name(code_body: list[Node]) -> str:
    """
    Get the name of the class, whose instance is registered with Scratch.extensions.register 
    
    Args:
        code_body: the code body to search in
    
    Raises:
        MANIP_BadExtensionCodeFormatError: if the code is not formatted like expected or the register call is not found
    """
    for statement in reversed(code_body): # register() is usually last
        if statement.type != "expression_statement":
            continue
        expr = statement.named_children[0]
        if expr.type != "call_expression":
            continue
        callee = expr.child_by_field_name("function")
        if callee and callee.type == "member_expression":
            if callee.text.decode() == "Scratch.extensions.register":
                arg = expr.child_by_field_name("arguments").named_children[0]
                if arg.type == "new_expression":
                    class_id = arg.child_by_field_name("constructor")
                    return class_id.text.decode()
    raise MANIP_BadExtensionCodeFormatError("Could not find registered class name")

def _get_class_def_by_name(code_body: list[Node], class_name: str) -> Node:
    """
    Get a class definition in the code body by its name
    
    Args:
        code_body: the code body to search in
        class_name: the name of the class to search
    
    Raises:
        MANIP_BadExtensionCodeFormatError: if the class is not found
    """
    for statement in code_body:
        if statement.type == "class_declaration":
            id_node = statement.child_by_field_name("name")
            if id_node and (id_node.text.decode() == class_name):
                return statement
    raise MANIP_BadExtensionCodeFormatError(f"Class {class_name!r} not found")

def _get_class_method_def_by_name(class_node: Node, method_name: str) -> Node:
    """
    Get a classes method definition by its name
    
    Args:
        class_node: the definition node of the class
        method_name: the name of the method to search
    
    Raises:
        MANIP_BadExtensionCodeFormatError: if the method is not found
    """
    body = class_node.child_by_field_name("body")
    for item in body.named_children:
        if item.type == "method_definition":
            name_node = item.child_by_field_name("name")
            if name_node.text.decode() == method_name:
                return item
    raise MANIP_BadExtensionCodeFormatError(f"Method {method_name!r} not found")
    
def extract_extension_info_safely(js_code: str) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class based on an AST of the extension's JS code.
    Does NOT actually execute any JavaScript code (for security lol)
    
    Args:
        js_code: the extension source code
    
    Raises:
        MANIP_InvalidExtensionCodeSyntaxError: if the extension code is syntactically invalid 
        MANIP_BadExtensionCodeFormatError: if the extension code is badly formatted, so that the extension information cannot be extracted
        MANIP_InvalidTranslationMessageError: if Scratch.translate is called with an invalid message
    
    Warnings:
        MANIP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed in the getInfo method
        MANIP_UnexpectedNotPossibleFeatureWarning: if a impossible to implement feature is used (eg. ternary expr) in the getInfo method
    """
    def find_error_nodes(node: Node) -> Iterator[Node]:
        if node.type == "ERROR":
            yield node
        for child in node.children:
            yield from find_error_nodes(child)

    parser = get_js_parser()
    try:
        tree: Tree = parser.parse(js_code.encode())
        root_node = tree.root_node
    except (TypeError, ValueError, RuntimeError) as error:
        raise MANIP_InvalidExtensionCodeSyntaxError(str(error)) from error # unlikely, but for safety
    if root_node.has_error:
        message_lines = ["Syntax error(s) detected:"]
        error_nodes = find_error_nodes(root_node)
        for error_node in error_nodes:
            line, col = error_node.start_point
            code_seg = error_node.text.decode()[:50].replace("\n", "\\n")
            message_lines.append(f"    At line {line}, col {col}: {code_seg}")
        raise MANIP_InvalidExtensionCodeSyntaxError("\n".join(message_lines))    
    
   
    try:
        main_body = _get_main_body(root_node)
        class_name = _get_registered_class_name(main_body)
        class_node = _get_class_def_by_name(main_body, class_name)
        getInfo_method = _get_class_method_def_by_name(class_node, method_name="getInfo")

        getInfo_func_expr = getInfo_method.child_by_field_name("body")
        assert (getInfo_func_expr is not None) and (getInfo_func_expr.type == "statement_block"), "Invalid getInfo method declaration"

        last_statement = getInfo_func_expr.named_children[-1]
        assert last_statement.type == "return_statement", "getInfo method is missing final return statement"

        return_value = last_statement.named_children[0]
        assert (return_value is not None) and (return_value.type == "object"), "Invalid or Failed to process getInfo return value"

    except AssertionError as error:
        raise MANIP_BadExtensionCodeFormatError(f"Cannot extract extension information: Bad extension code format: {error}") from error
    
    def handle_Scratch_translate(arguments_node: Node) -> str:
        arg_node = arguments_node.named_children[0]
        message = ts_node_to_json(arg_node)

        if isinstance(message, dict):
            message = message.get("default", "")
        elif isinstance(message, str):
            pass  # already fine
        else:
            pass  # will trigger error below if needed

        if not(isinstance(message, str)) or not(message):
            raise MANIP_InvalidTranslationMessageError(f"Invalid or empty message passed to Scratch.translate: {message}")

        return message
    
    def handle_JSON_stringify(arguments_node: Node) -> str:
        arg_node = arguments_node.named_children[0]
        value = ts_node_to_json(arg_node)
        return gdumps(value)
    
    def handle_call(node: Node) -> NotImplementedType | Any:
        callee_node = node.child_by_field_name("function")
        arguments_node = node.child_by_field_name("arguments")

        if (
            callee_node and (callee_node.type == "member_expression")
            and arguments_node and (arguments_node.named_child_count == 1)
        ):
            object_node = callee_node.child_by_field_name("object")
            property_node = callee_node.child_by_field_name("property")
            
            if (
                object_node and (object_node.type == "identifier") and
                property_node and (property_node.type == "property_identifier")
            ):
                object_name   = object_node.text.decode()
                property_name = property_node.text.decode()
                if   (object_name == "Scratch") and (property_name == "translate"):
                    return handle_Scratch_translate(arguments_node)
                elif (object_name == "JSON") and (property_name == "stringify"):
                    return handle_JSON_stringify(arguments_node)

        return NotImplemented

    try:
        extension_info = ts_node_to_json(return_value, call_handler=handle_call)
    except MANIP_JsNodeTreeToJsonConversionError as error:
        raise MANIP_BadExtensionCodeFormatError(f"Cannot extract extension information: Bad extension code format: getInfo method should return static value: \n{error}") from error
    return extension_info


__all__ = ["extract_extension_info_safely"]

