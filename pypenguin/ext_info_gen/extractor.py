from ast             import literal_eval
from base64          import b64decode
from collections.abc import Iterable
from colorama        import Fore as ColorFore, Style as ColorStyle
#from esprima         import parseScript, Error as EsprimaError
from esprima.nodes   import (
    Node, Script, ExpressionStatement, ClassDeclaration, ClassBody, MethodDefinition, 
    BlockStatement, ReturnStatement,
    CallExpression, StaticMemberExpression, NewExpression, FunctionExpression, 
    ObjectExpression, ArrayExpression, ArrowFunctionExpression, ThisExpression, 
    Identifier, Literal, TemplateLiteral, Property,
)
from os              import path
from requests        import get as requests_get, RequestException
from tree_sitter     import Node
from typing          import Any, Callable
from types           import NotImplementedType
from urllib.parse    import unquote
from warnings        import warn

from pypenguin.tree_sitter_loader import get_js_parser
from pypenguin.utility            import (
    read_file_text,
    PP_InvalidExtensionCodeSourceError, 
    PP_NetworkFetchError, PP_UnexpectedFetchError, PP_FileFetchError, PP_FileNotFoundError, 
    PP_JsNodeTreeToJsonConversionError, PP_InvalidExtensionCodeSyntaxError, PP_BadExtensionCodeFormatError,    PP_InvalidTranslationMessageError,
    PP_UnexpectedPropertyAccessWarning, PP_UnexpectedTemplateLiteralWarning,
    write_file_text, repr_tree, # temporary
)


SCRATCH_STUB = {
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
        #"unsandboxed": True , # hasn't ever been needed, uncomment when needed
        #"isPenguinMod": True, # hasn't ever been needed, uncomment when needed
        # .register is handled somewhere else
    },
}
REGISTER_EXTENSION_FUNC_PATTERN = StaticMemberExpression(
    object=StaticMemberExpression(
        object=Identifier(name="Scratch"),
        property=Identifier(name="extensions"),
    ), 
    property=Identifier(name="register"),
).toDict()
TRANSLATE_FUNC_PATTERN = StaticMemberExpression(
    object=Identifier(name="Scratch"),
    property=Identifier(name="translate"),
).toDict()


def fetch_js_code(source: str) -> str:
    """
    Fetch the extension's JS code from a file path, HTTPS URL, or JavaScript Data URI

    Args:
        source: The file path, HTTPS URL, or data URI of the extension source code

    Raises:
        PP_InvalidExtensionCodeSourceError: If the source data URI is invalid
        PP_NetworkFetchError: For any network-related error
        PP_UnexpectedFetchError: For any other unexpected error while fetching URL
        PP_FileNotFoundError: If the local file does not exist
        PP_FileFetchError: If the file cannot be read
    """
    if source.startswith("data:"):
        print("--> Fetching from data URI")
        try:
            meta, encoded = source.split(",", 1)
            if ";base64" in meta:
                return b64decode(encoded).decode()
            else:
                return unquote(encoded)
        except Exception as error:
            raise PP_InvalidExtensionCodeSourceError(f"Failed to decode data URI: {error}") from error

    elif source.startswith("http://") or source.startswith("https://"):
        print(f"--> Fetching from URL: {source}")
        try:
            response = requests_get(source, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as error:
            raise PP_NetworkFetchError(f"Network error fetching {source}: {error}") from error
        except Exception as error:
            raise PP_UnexpectedFetchError(f"Unexpected error while fetching {source}: {error}") from error

    else:
        print(f"--> Reading from file: {source}")
        if not path.exists(source):
            raise PP_FileNotFoundError(f"File not found: {source}")
        try:
            return read_file_text(source)
        except Exception as error:
            raise PP_FileFetchError(f"Failed to read file {source}: {error}") from error

def ts_node_to_json(
    node: Node | str | int | float | bool | None, 
    source_code: str, 
    call_handler=None,
) -> Any:
    """
    Recursively converts a tree sitter Syntax Tree into a plain JSON-compatible Python structure

    Args:
        node: the root node or a subnode
        source_code: the node tree's original source code
        call_handler: a callable handling call expression nodes (should return NotImplemented if node not addressed by handler)

    Returns:
        A Python object representing the JSON-equivalent value: dict, list, str, int, float, bool, or None

    Raises:
        PP_JsNodeTreeToJsonConversionError: If an unsupported node type or a member expression of unexptected format is encountered
    
    Warnings:
        PP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed
        PP_UnexpectedTemplateLiteralWarning: if a template literal is used
    """
    def get_code(node: Node) -> str:
        nonlocal source:code
        return source_code[node.start_byte : node.end_byte]
    
    if isinstance(node, (str, int, float, bool, type(None))):
        return node

    if node.type == "member_expression":
        # try to handle eg. Scratch.ArgumentType.STRING
        object_node = node.child_by_field_name("object")
        property_node = node.child_by_field_name("property")

        if object_node.type == "member_expression":
            inner_obj = object_node.child_by_field_name("object")
            inner_prop = object_node.child_by_field_name("property")
            if inner_obj.type == "identifier" and get_code(inner_obj) == "Scratch":
                outer_key = get_code(property_node)
                inner_key = get_code(inner_prop)
                if (outer_key in SCRATCH_STUB) and (inner_key in SCRATCH_STUB[outer_key]):
                    return SCRATCH_STUB[outer_key][inner_key]

        elif object_node.type == "this":
            warn(f"{ColorFore.YELLOW}Tried to access property of 'this': {property_node.text.decode()}, Defaulting to None{ColorStyle.RESET_ALL}", PP_UnexpectedPropertyAccessWarning)
            return None

        raise PP_JsNodeTreeToJsonConversionError(f"Unsupported member expression format: {node.sexp()}")

    elif node.type == "object":
        result = {}
        for prop in node.named_children:
            if prop.type != "pair":
                raise PP_JsNodeTreeToJsonConversionError(f"Unsupported property type: {prop.type}")

            key_node = prop.child_by_field_name("key")
            value_node = prop.child_by_field_name("value")

            if key_node.type == "identifier":
                key = get_code(key_node)
            elif key_node.type == "string":
                key = literal_eval(get_code(key_node).replace('`', '"'))
            else:
                raise PP_JsNodeTreeToJsonConversionError(f"Unsupported key type: {key_node.type}")

            result[key] = ts_node_to_json(value_node, source_code, call_handler)
        return result

    elif node.type == "array":
        return [ts_node_to_json(child, source_code, call_handler) for child in node.named_children]

    elif node.type == "string":
        return literal_eval(get_code(node).replace('`', '"'))
    
    elif node.type == "number":
        code = get_code(node)
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
        return get_code(node)

    elif node.type == "template_string":
        warn("{ColorFore.YELLOW}Template literal encountered. Defaulting to None{ColorStyle.RESET_ALL}", PP_UnexpectedTemplateLiteralWarning)
        return None

    elif (node.type == "call_expression") and bool(call_handler):
        value = call_handler(node)
        if value is not NotImplemented:
            return value

    raise PP_JsNodeTreeToJsonConversionError(f"Unsupported node type: {node.type}")

def extract_extension_info(js_code: str) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class based on an AST of the extension's JS code.
    Does NOT actually execute any JavaScript code (for security lol)
    
    Args:
        js_code: the extension source code
    
    Raises:
        PP_InvalidExtensionCodeSyntaxError: if the extension code is syntactically invalid 
        PP_BadExtensionCodeFormatError: if the extension code is badly formatted, so that the extension information cannot be extracted
        PP_InvalidTranslationMessageError: if Scratch.translate is called with an invalid message
    
    Warnings:
        PP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed in the getInfo method
        PP_UnexpectedTemplateLiteralWarning: if a template literal is used in the getInfo method
    """
    def get_main_body(root: Node) -> list[Node]:
        """
        Get the main code body
        
        Args:
            root: the JavaScript Syntax Tree
        
        Raises:
            AssertionError: if the code is not formatted in one of the two expected ways
        """
        # Check for IIFE '((Scratch) => {...})(Scratch)'(sandboxed style)
        if root.type == "program":
            last = root.children[-1]
            if last.type == "expression_statement" and last.named_children:
                expr = last.named_children[0]
                if expr.type == "call_expression":
                    func = expr.child_by_field_name("function")
                    if func and func.type == "arrow_function":
                        body = func.child_by_field_name("body")
                        if body.type == "statement_block":
                            return body.named_children
        # Otherwise assume unsandboxed style
        return root.named_children
    
    def get_registered_class_name(code_body: list[Node]) -> str: # STOPPED HERE: convert rest of function
        """
        Get the name of the class, whose instance is registered with Scratch.extensions.register 
        
        Args:
            code_body: the code body to search in
        
        Raises:
            AssertionError: if the code is not formatted like expected or the register call is not found
        """
        ext_class_id: Identifier | None = None
        for i, statement in enumerate(reversed(main_body)): # register is usually last
            if isinstance(statement, ExpressionStatement):
                if isinstance(statement.expression, CallExpression):
                    callee: Node = statement.expression.callee
                    if callee.toDict() == REGISTER_EXTENSION_FUNC_PATTERN:
                        arguments: list[Node] = statement.expression.arguments
                        assert len(arguments) == 1
                        argument = arguments[0]
                        assert isinstance(argument, NewExpression)
                        assert isinstance(argument.callee, Identifier)
                        ext_class_id = argument.callee
                        break
        assert ext_class_id is not None
        return ext_class_id.name
    
    def get_class_def_by_name(code_body: list[Node], class_name: str) -> ClassDeclaration:
        """
        Get a class definition in the code body by its name
        
        Args:
            code_body: the code body to search in
            class_name: the name of the class to search
        
        Raises:
            AssertionError: if class is not found
        """
        class_node: Node | None = None
        for statement in reversed(code_body):
            if isinstance(statement, ClassDeclaration):
                class_id: Identifier = statement.id
                if class_id.name == class_name:
                    class_node = statement
                    break
        assert class_node is not None
        return class_node

    def get_class_method_def_by_name(class_def: ClassDeclaration, method_name: str) -> MethodDefinition:
        """
        Get a classes method definition by its name
        
        Args:
            class_def: the definition node of the class
            method_name: the name of the method to search
        
        Raises:
            AssertionError: if method is not found
        """
        class_body: ClassBody = class_def.body
        method_node: MethodDefinition | None = None
        for statement in class_body.body:
            if isinstance(statement, MethodDefinition):
                method_id: Identifier = statement.key
                if method_id.name == method_name:
                    method_node = statement
                    break
        assert method_node is not None
        return method_node
    
    parser = get_js_parser()
    try:
        tree = parser.parse(js_code.encode()).root_node
    except EsprimaError as error:
        line = getattr(error, "lineNumber", None)
        column = getattr(error, "column", None)
        raise PP_InvalidExtensionCodeSyntaxError(str(error), line, column) from error
    
    write_file_text("parsed_ast.lua", repr_tree(tree, js_code.encode()))
    #write_file_text("parsed_ast.lua", repr(tree.body[0].body.body[0].value.body.body[0].argument))
    #raise Exception(r"$\/\$STOP$/\/$")
            
    try:
        main_body = get_main_body(tree)
        class_name = get_registered_class_name(main_body)
        class_node = get_class_def_by_name(main_body, class_name)
        getInfo_method = get_class_method_def_by_name(class_node, method_name="getInfo")
        
        getInfo_expression = getInfo_method.value
        assert isinstance(getInfo_expression, FunctionExpression)
        assert isinstance(getInfo_expression.body, BlockStatement)
        last_statement = getInfo_expression.body.body[-1]
        assert isinstance(last_statement, ReturnStatement)
        return_value = last_statement.argument
        assert isinstance(return_value, ObjectExpression)

    except AssertionError as error:
        raise PP_BadExtensionCodeFormatError("Cannot extract extension information: Bad extension code format") from error
    
    def handle_call(node: CallExpression) -> NotImplementedType | None:
        if isinstance(node.callee, StaticMemberExpression):
            if (node.callee.toDict() == TRANSLATE_FUNC_PATTERN) and (len(node.arguments) == 1):
                message = esprima_to_json(node.arguments[0])
                if   isinstance(message, dict):
                    message = message.get("default", "")
                elif isinstance(message, str):
                    pass # already in expected format
                else:
                    pass # just keep it, error will raise
                
                if not(isinstance(message, str)) or not(message):
                    raise PP_InvalidTranslationMessageError(f"Invalid or empty message was passed to Scratch.translate: {repr(message)}");
                return message # just return the default value in english, the whole project is english anyway                
        return NotImplementedError

    try:
        extension_info = esprima_to_json(return_value, call_handler=handle_call)
    except PP_JsNodeTreeToJsonConversionError as error:
        raise PP_BadExtensionCodeFormatError("Cannot extract extension information: Bad extension code format: getInfo method should return static value") from error
    return extension_info


__all__ = ["fetch_js_code", "extract_extension_info"]

