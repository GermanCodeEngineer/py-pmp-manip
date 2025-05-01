class PyPenguinError(Exception):
    pass


class ThanksError(PyPenguinError):
    def __init__(self):
        super().__init__("Your project is unique! It could help me with my research! Please create an issue with your project attached! https://github.com/Fritzforcode/PyPenguinOO/issues/new")

class PathError(PyPenguinError): pass

###############################################################
#                  ERRORS FOR DESERIALIZATION                 #
###############################################################

class DeserializationError(PyPenguinError):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Issue during deserialization: {msg}")

###############################################################
#                ERRORS FOR FR TO SR CONVERSION               #
###############################################################

class FSCError(PyPenguinError): # First (Representation) -> Second (Representation) Conversion
    def __init__(self, msg: str) -> None:
        super().__init__(f"Issue during first to second representation conversion: {msg}")

###############################################################
#                    ERRORS FOR VALIDATION                    #
###############################################################

def generate_path_string(path: list) -> str:
    path_string = ""
    for item in path:
        if   isinstance(item, str):
            path_string += "." + item
        elif isinstance(item, int):
            path_string += "[" + str(item) + "]"
        elif isinstance(item, tuple) and (len(item) == 1) and isinstance(item[0], str):
            path_string += "[" + repr(item[0]) + "]"
        else: raise ValueError()
    return path_string

class ValidationError(PyPenguinError): pass

class PathValidationError(ValidationError):
    def __init__(self, path: list, msg: str, condition: str|None = None) -> None:
        path_string = generate_path_string(path)
        full_message = ""
        if path_string != "":
            full_message += f"At {path_string}: "
        if condition is not None:
            full_message += f"{condition}: "
        full_message += msg
        super().__init__(full_message)
    
class TypeValidationError(PathValidationError): pass
class InvalidValueError(PathValidationError): pass
class RangeValidationError(PathValidationError): pass

class MissingInputError(PathValidationError): pass
class UnnecessaryInputError(PathValidationError): pass
class MissingDropdownError(PathValidationError): pass
class UnnecessaryDropdownError(PathValidationError): pass

class InvalidDropdownValueError(PathValidationError): pass

class InvalidOpcodeError(PathValidationError): pass
class InvalidBlockShapeError(PathValidationError): pass

class LayerOrderError(PathValidationError): pass

class SameValueTwiceError(ValidationError):
    def __init__(self, path1: list, path2: list, msg: str, condition: str|None = None) -> None:
        path1_string = generate_path_string(path1)
        path2_string = generate_path_string(path2)
        full_message = f"At {path1_string} and {path2_string}: "
        if condition is not None:
            full_message += f"{condition}: "
        full_message += msg
        super().__init__(full_message)

class SameNameTwiceError(SameValueTwiceError): pass
class SameNumberTwiceError(SameValueTwiceError): pass

