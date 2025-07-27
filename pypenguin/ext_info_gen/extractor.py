from base64          import b64decode
from collections.abc import Iterable
from esprima         import parseScript, error as esprima_error
from esprima.nodes   import (
    Node, ExpressionStatement, ClassDeclaration, ClassBody, MethodDefinition, BlockStatement, ReturnStatement,
    CallExpression, StaticMemberExpression, NewExpression, FunctionExpression, ObjectExpression, ArrayExpression, ArrowFunctionExpression,
    Identifier, Literal, Property,
)
from os              import path
from requests        import get as requests_get, RequestException
from typing          import Any
from urllib.parse    import unquote

from pypenguin.utility         import (
    grepr, read_file_text,
    PP_InvalidExtensionCodeSourceError, 
    PP_NetworkFetchError, PP_UnexpectedFetchError, PP_FileFetchError, PP_FileNotFoundError, 
    PP_JsNodeTreeToJsonConversionError, PP_InvalidExtensionCodeSyntaxError, PP_BadExtensionCodeFormatError,    write_file_text, # temporary
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
}
REGISTER_EXTENSION_FUNC_PATTERN = StaticMemberExpression(
    object=StaticMemberExpression(
        object=Identifier(name="Scratch"),
        property=Identifier(name="extensions"),
    ), 
    property=Identifier(name="register"),
).toDict()


def fetch_js_code(source: str) -> str:
    """
    Fetch the extension's JS code from a file path, HTTPS URL, or JavaScript Data URI

    Args:
        source: The file path, HTTPS URL, or data URI of the extension source code

    Raises:
        PP_InvalidExtensionCodeSourceError: If the data URI is invalid
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
            raise PP_FileFetchError(f"Failed to read file {source}") from error

def esprima_to_json(node: list[Node] | Node | str | int | float | bool | None) -> Any:
    """
    Recursively converts an Esprima-style object-oriented AST into a plain JSON-compatible Python structure

    Args:
        node: The root AST node or subnode, typically an instance of ObjectExpression, ArrayExpression, Literal,
            Identifier, or a list of nodes

    Returns:
        A Python object representing the JSON-equivalent value: dict, list, str, int, float, bool, or None

    Raises:
        PP_JsNodeTreeToJsonConversionError: If an unsupported node type or a MemberExpression of unexptected format is encountered
    """
    if   isinstance(node, StaticMemberExpression):
        try:  # try to handle eg. Scratch.ArgumentType.STRING
            assert isinstance(node.object, StaticMemberExpression)
            inner_expression = node.object
            
            assert isinstance(inner_expression.object, Identifier)
            assert inner_expression.object.name == "Scratch"
            assert isinstance(inner_expression.property, Identifier)
            assert inner_expression.property.name in SCRATCH_STUB

            target_section = SCRATCH_STUB[inner_expression.property.name]
            assert isinstance(node.property, Identifier)
            assert node.property.name in target_section
            return target_section[node.property.name]

        except AssertionError as error:
            raise PP_JsNodeTreeToJsonConversionError("Could not process MemberExpression of unexpected format: {node}") from error

    elif isinstance(node, ObjectExpression):
        result = {}
        for property in node.properties:
            if not isinstance(property, Property):
                raise PP_JsNodeTreeToJsonConversionError(f"Unsupported property type: {type(property)}")
            # Determine key
            if isinstance(property.key, Identifier):
                key = property.key.name
            elif isinstance(property.key, Literal):
                key = property.key.value
            else:
                raise PP_JsNodeTreeToJsonConversionError(f"Unsupported key type: {type(property.key)}")
            # Recurse on value
            value = esprima_to_json(property.value)
            result[key] = value
        return result

    elif isinstance(node, ArrayExpression):
        return [esprima_to_json(elem) for elem in node.elements]

    elif isinstance(node, Literal):
        return node.value

    elif isinstance(node, Identifier):
        return node.name

    elif isinstance(node, (str, int, float, bool, type(None))):
        return node

    elif isinstance(node, Iterable) and not(isinstance(node, StaticMemberExpression)):
        return [esprima_to_json(item) for item in node]

    else:
        raise PP_JsNodeTreeToJsonConversionError(f"Unsupported node type: {type(node)}")

def extract_extension_info(js_code: str) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class based on an AST of the extension's JS code.
    Does NOT actually execute any JavaScript code (for security lol)
    
    Args:
        js_code: the extension source code
    
    Raises:
        PP_InvalidExtensionCodeSyntaxError: if the extension code is syntactically invalid 
        PP_BadExtensionCodeFormatError: if the extension code is badly formatted, so that the extension information cannot be extracted
    """
    def get_main_body(tree: Node) -> list[Node]:
        """
        Get the main code body
        
        Args:
            tree: the JavaScript AST
        
        Raises:
            AssertionError: if the code is not formatted in one of the two expected ways
        """
        if (len(tree.body) == 1) and isinstance(tree.body[0], ExpressionStatement):
            # this handles ((Scratch) => { ... })(Scratch);
            statement: ExpressionStatement = tree.body[0]
            assert isinstance(statement.expression, CallExpression)
            assert isinstance(statement.expression.callee, ArrowFunctionExpression)
            assert isinstance(statement.expression.callee.body, BlockStatement)
            return statement.expression.callee.body.body
        else:
            return tree.body
    
    def get_registered_class_name(code_body: list[Node]) -> str:
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
    
    def get_class_def_by_name(code_body: list[Node], class_name: str) -> ClassDefinition:
        """
        Get a class definition in the code body by its name
        
        Args:
            code_body: the code body to search in
            class_name: the name of the class to search
        
        Raises:
            AssertionError: if class is not found
        """
        class_node: Node | None = None
        for statement in reversed(main_body):
            if isinstance(statement, ClassDeclaration):
                class_id: Identifier = statement.id
                if class_id.name == class_name:
                    class_node = statement
                    break
        assert class_node is not None
        return class_node

    def get_class_method_def_by_name(class_def: ClassDefinition, method_name: str) -> MethodDefinition:
        """
        Get a classes method definition by its name
        
        Args:
            class_def: the definition node of the class
            method_name: the name of the method to search
        
        Raises:
            AssertionError: if method is not found
        """
        class_body: ClassBody = class_node.body
        method_node: MethodDefinition | None = None
        for statement in class_body.body:
            if isinstance(statement, MethodDefinition):
                method_id: Identifier = statement.key
                if method_id.name == method_name:
                    method_node = statement
                    break
        assert method is not None
        return method_node


    try:
        tree = esprima.parseScript(js_code, tolerant=False)
    except esprima_error.Error as error:
        line = getattr(error, "lineNumber", None)
        column = getattr(error, "column", None)
        raise PP_InvalidExtensionCodeSyntaxError(str(error), line, column) from error

    write_file_text("parsed_ast.lua", repr(tree))
    #write_file_text("parsed_ast.lua", repr(tree.body[0].body.body[0].value.body.body[0].argument))
    
    try:
        main_body = get_main_body()
        class_name = get_registered_class_name(main_body)
        class_node = get_class_def_by_name(main_body, class_name)
        getInfo_method = get_class_method_def_by_name(class_node, method_name="getInfo")
        
        getInfo_expression = getInfoMethod.value
        assert isinstance(getInfo_method.value, FunctionExpression)
        assert isinstance(getInfo_expression.body, BlockStatement)
        last_statement = getInfo_expression.body.body[-1]
        assert isinstance(last_statement, ReturnStatement)
        return_value = last_statement.argument
        assert isinstance(return_value, ObjectExpression)

    except AssertionError as error:
        raise PP_BadExtensionCodeFormatError("Cannot extract extension information: Bad extension code format") from error
    
    try:
        extension_info = esprima_to_json(return_value)
    except PP_JsNodeTreeToJsonConversionError as error:
        raise PP_BadExtensionCodeFormatError("Cannot extract extension information: Bad extension code format: getInfo method should return static value") from error
    return extension_info


__all__ = ["fetch_js_code", "extract_extension_info"]

