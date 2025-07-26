from base64          import b64decode
from collections.abc import Iterable
from esprima         import parseScript
from esprima.nodes   import (
    Node, ExpressionStatement, ClassDeclaration, ClassBody, MethodDefinition, BlockStatement, ReturnStatement,
    CallExpression, StaticMemberExpression, NewExpression, FunctionExpression, ObjectExpression, ArrayExpression,
    Identifier, Literal, Property,
)
from os              import path
from requests        import get as requests_get, RequestException
from typing          import Any
from urllib.parse    import unquote

from pypenguin.utility         import (
    grepr, read_file_text,
    UnknownExtensionAttributeError, InvalidExtensionCodeError,
    write_file_text, # temporary
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


def fetch_js_code(extension: str) -> str:
    """
    Fetch the extension's JS code from a file path, HTTPS URL, or JavaScript Data URI

    Args:
        extension: The file path, HTTPS URL, or data URI of the extension code

    Raises:
        ValueError: If the data URI is invalid
        ConnectionError: For any network-related error
        RuntimeError: For any other unexpected error while fetching URL
        FileNotFoundError: If the local file does not exist
        OSError: If the file cannot be read
    """
    if extension.startswith("data:"):
        print("--> Fetching from data URI")
        try:
            meta, encoded = extension.split(",", 1)
            if ";base64" in meta:
                return b64decode(encoded).decode()
            else:
                return unquote(encoded)
        except Exception as error:
            raise ValueError(f"Failed to decode data URI: {error}") from error

    elif extension.startswith("http://") or extension.startswith("https://"):
        print(f"--> Fetching from URL: {extension}")
        try:
            response = requests_get(extension, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as error:
            raise ConnectionError(f"Network error fetching {extension}") from error
        except Exception as error:
            raise RuntimeError(f"Unexpected error while fetching URL") from error

    else:
        print(f"--> Reading from file: {extension}")
        if not path.exists(extension):
            raise FileNotFoundError(f"File not found: {extension}")
        try:
            return read_file_text(extension)
        except OSError as error:
            raise OSError(f"Failed to read file {extension}") from error

def esprima_to_json(node: list[Node] | Node | str | int | float | bool | None) -> Any:
    """
    Recursively converts an Esprima-style object-oriented AST into a plain JSON-compatible Python structure

    Args:
        node: The root AST node or subnode, typically an instance of ObjectExpression, ArrayExpression, Literal,
            Identifier, or a list of nodes

    Returns:
        A Python object representing the JSON-equivalent value: dict, list, str, int, float, bool, or None

    Raises:
        EsprimaToJsonConversionError: If an unsupported node type or a MemberExpression of unexptected format is encountered
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
            raise EsprimaToJsonConversionError("Could not process MemberExpression of unexpected format: {node}") from error

    elif isinstance(node, ObjectExpression):
        result = {}
        for property in node.properties:
            if not isinstance(property, Property):
                raise EsprimaToJsonConversionError(f"Unsupported property type: {type(property)}")
            # Determine key
            if isinstance(property.key, Identifier):
                key = property.key.name
            elif isinstance(property.key, Literal):
                key = property.key.value
            else:
                raise EsprimaToJsonConversionError(f"Unsupported key type: {type(property.key)}")
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
        raise EsprimaToJsonConversionError(f"Unsupported node type: {type(node)}")

def extract_getinfo(js_code: str) -> dict[str, Any]:
    """
    Extract the return value of the getInfo method of the extension class based on the extension's JS code.    
    # TODO: add details when done    
    Args:
        js_code: the file path or https URL or JS Data URI of the extension code
    
    Raises:
        InvalidExtensionCodeError: 
    """


    tree = parseScript(js_code)
    #write_file_text("parsed_ast.lua", repr(tree.body[0]))
    write_file_text("parsed_ast.lua", repr(tree.body[0].body.body[0].value.body.body[0].argument))

    try:
        ext_class_id: Identifier | None = None
        for i, statement in enumerate(reversed(tree.body)): # register is usually last
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

        class_node: Node | None = None
        for statement in reversed(tree.body):
            if isinstance(statement, ClassDeclaration):
                class_id: Identifier = statement.id
                if class_id.name == ext_class_id.name:
                    class_node = statement
                    break
        assert class_node is not None

        class_body: ClassBody = class_node.body
        getInfo_method: FunctionExpression | None = None
        for statement in class_body.body:
            if isinstance(statement, MethodDefinition):
                method_id: Identifier = statement.key
                if method_id.name == "getInfo":
                    assert isinstance(statement.value, FunctionExpression)
                    getInfo_method = statement.value
                    break
        assert getInfo_method is not None

        assert isinstance(getInfo_method.body, BlockStatement)
        last_statement = getInfo_method.body.body[-1]
        assert isinstance(last_statement, ReturnStatement)
        return_value = last_statement.argument
        assert isinstance(return_value, ObjectExpression)
        


    except AssertionError as error:
        raise InvalidExtensionCodeError("Cannot extract extension information: Invalid extension code ") from error
    
    try:
        extension_info = esprima_to_json(return_value)
    except EsprimaToJsonConversionError as error:
        raise InvalidExtensionCodeError("Cannot extract extension information: Invalid extension code: getInfo method should return static value") from error
    return extension_info


__all__ = ["fetch_js_code", "extract_getinfo"]

