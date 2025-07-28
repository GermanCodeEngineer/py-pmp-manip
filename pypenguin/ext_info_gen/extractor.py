from ast             import literal_eval
from base64          import b64decode
from colorama        import Fore as ColorFore, Style as ColorStyle
from collections.abc import Iterator
from os              import path
from requests        import get as requests_get, RequestException
from tree_sitter     import Node, Tree
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
    NotSetType, NotSet,
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
    call_handler=None,
) -> Any | NotSetType:
    """
    Recursively converts a tree sitter Syntax Tree into a plain JSON-compatible Python structure

    Args:
        node: the root node or a subnode
        call_handler: a callable handling call expression nodes (should return NotImplemented if node not addressed by handler)

    Returns:
        A Python object representing the JSON-equivalent value: dict, list, str, int, float, bool, or None

    Raises:
        PP_JsNodeTreeToJsonConversionError: If an unsupported node type or a member expression of unexptected format is encountered
    
    Warnings:
        PP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed
        PP_UnexpectedTemplateLiteralWarning: if a template literal is used
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
                 f"Defaulting to None{ColorStyle.RESET_ALL}", PP_UnexpectedPropertyAccessWarning)
            return None

        raise PP_JsNodeTreeToJsonConversionError(f"Unsupported member expression format: {node.sexp()}")

    elif node.type == "object":
        result = {}
        for prop in node.named_children:
            if   prop.type == "comment": continue
            elif prop.type != "pair":
                raise PP_JsNodeTreeToJsonConversionError(f"Unsupported property type: {prop.type}")

            key_node = prop.child_by_field_name("key")
            value_node = prop.child_by_field_name("value")

            if key_node.type in {"identifier", "property_identifier"}:
                key = key_node.text.decode()
            elif key_node.type == "string":
                key = literal_eval(key_node.text.decode().replace('`', '"'))
            else:
                raise PP_JsNodeTreeToJsonConversionError(f"Unsupported key type: {key_node.type}")

            result[key] = ts_node_to_json(value_node, call_handler) # cant return NotSet
        return result

    elif node.type == "array":
        return [ts_node_to_json(child, call_handler) for child in node.named_children if child is not NotSet]

    elif node.type == "string":
        return literal_eval(node.text.decode().replace('`', '"'))
    
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

    elif node.type == "template_string":
        warn(f"{ColorFore.YELLOW}Template literal encountered. Defaulting to None{ColorStyle.RESET_ALL}", PP_UnexpectedTemplateLiteralWarning)
        return None

    elif (node.type == "call_expression") and bool(call_handler):
        value = call_handler(node)
        if value is not NotImplemented:
            return value
    
    elif (node.type == "comment"):
        return NotSet

    print(node.text.decode())
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
    def get_main_body(root_node: Node) -> list[Node]:
        """
        Get the main code body
        
        Args:
            root_node: the JavaScript Syntax Tree
        """
        # Check for IIFE '((Scratch) => {...})(Scratch)'(sandboxed style)
        if root_node.type == "program":
            last = root_node.children[-1]
            if last.type == "expression_statement" and last.named_children:
                expr = last.named_children[0]
                if expr.type == "call_expression":
                    func = expr.child_by_field_name("function")
                    if func.type == "parenthesized_expression":
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
    
    def get_registered_class_name(code_body: list[Node]) -> str:
        """
        Get the name of the class, whose instance is registered with Scratch.extensions.register 
        
        Args:
            code_body: the code body to search in
        
        Raises:
            PP_BadExtensionCodeFormatError: if the code is not formatted like expected or the register call is not found
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
        raise PP_BadExtensionCodeFormatError("Could not find registered class name")

    def get_class_def_by_name(code_body: list[Node], class_name: str) -> Node:
        """
        Get a class definition in the code body by its name
        
        Args:
            code_body: the code body to search in
            class_name: the name of the class to search
        
        Raises:
            PP_BadExtensionCodeFormatError: if the class is not found
        """
        for statement in code_body:
            if statement.type == "class_declaration":
                id_node = statement.child_by_field_name("name")
                if id_node and (id_node.text.decode() == class_name):
                    return statement
        raise PP_BadExtensionCodeFormatError(f"Class '{class_name}' not found")
    
    def get_class_method_def_by_name(class_node: Node, method_name: str) -> Node:
        """
        Get a classes method definition by its name
        
        Args:
            class_node: the definition node of the class
            method_name: the name of the method to search
        
        Raises:
            PP_BadExtensionCodeFormatError: if the method is not found
        """
        body = class_node.child_by_field_name("body")
        for item in body.named_children:
            if item.type == "method_definition":
                name_node = item.child_by_field_name("name")
                if name_node.text.decode() == method_name:
                    return item
        raise PP_BadExtensionCodeFormatError(f"Method '{method_name}' not found")
    
    def find_error_nodes(node: Node) -> Iterator[Node]:
        if node.type == "ERROR":
            yield node
        for child in node.children:
            yield from find_error_nodes(child)

    parser = get_js_parser()
    try:
        tree: Tree = parser.parse(js_code.encode())
        root_node = tree.root_node
    except Exception as error:
        raise PP_InvalidExtensionCodeSyntaxError(str(error)) from error # unlikely, but for safety
    if root_node.has_error:
        message_lines = ["Syntax error(s) detected:"]
        error_nodes = find_error_nodes(root_node)
        for error_node in error_nodes:
            line, col = error_node.start_point
            code_seg = error_node.text.decode()[:50].replace("\n", "\\n")
            message_lines.append(f"    At line {line}, col {col}: {code_seg}")
        raise PP_InvalidExtensionCodeSyntaxError("\n".join(message_lines))    
    
    write_file_text("parsed_ast.lua", repr_tree(root_node, js_code.encode()))
    #write_file_text("parsed_ast.lua", repr(root.body[0].body.body[0].value.body.body[0].argument))
    #raise Exception(r"$\/\$STOP$/\/$")
            
   
    try:
        main_body = get_main_body(root_node)
        print("####", ("\n"+100*"="+"\n").join([x.text.decode()[:200] for x in main_body]))
        class_name = get_registered_class_name(main_body)
        class_node = get_class_def_by_name(main_body, class_name)
        getInfo_method = get_class_method_def_by_name(class_node, method_name="getInfo")

        getInfo_func_expr = getInfo_method.child_by_field_name("body")
        assert (getInfo_func_expr is not None) and (getInfo_func_expr.type == "statement_block"), "Invalid getInfo method declaration"

        last_statement = getInfo_func_expr.named_children[-1]
        assert last_statement.type == "return_statement", "getInfo method is missing final return statement"

        return_value = last_statement.named_children[0]
        assert (return_value is not None) and (return_value.type == "object"), "Invalid or Failed to process getInfo return value"

    except AssertionError as error:
        raise PP_BadExtensionCodeFormatError(f"Cannot extract extension information: Bad extension code format: {error}") from error

    def handle_call(node: Node) -> NotImplementedType | str:
        if node.type != "call_expression":
            return NotImplemented

        callee = node.child_by_field_name("function")
        arguments_node = node.child_by_field_name("arguments")

        if (
            callee and (callee.type == "member_expression")
            and arguments_node and (arguments_node.named_child_count == 1)
        ):
            # Match Scratch.translate(...)
            object_node = callee.child_by_field_name("object")
            property_node = callee.child_by_field_name("property")

            if (
                object_node and (object_node.type == "identifier") and (object_node.text.decode() == "Scratch") and
                property_node and (property_node.type == "property_identifier") and (property_node.text.decode() == "translate")
            ):
                arg_node = arguments_node.named_children[0]
                message = ts_node_to_json(arg_node, js_code)

                if isinstance(message, dict):
                    message = message.get("default", "")
                elif isinstance(message, str):
                    pass  # already fine
                else:
                    pass  # will trigger error below if needed

                if not isinstance(message, str) or not message:
                    raise PP_InvalidTranslationMessageError(f"Invalid or empty message passed to Scratch.translate: {repr(message)}")

                return message

        return NotImplemented

    try:
        extension_info = ts_node_to_json(return_value, call_handler=handle_call)
    except PP_JsNodeTreeToJsonConversionError as error:
        raise PP_BadExtensionCodeFormatError(f"Cannot extract extension information: Bad extension code format: getInfo method should return static value: \n{error}") from error
    return extension_info


__all__ = ["fetch_js_code", "extract_extension_info"]

