class PyPenguinError(Exception):
    pass


class ThanksError(PyPenguinError):
    def __init__(self):
        super().__init__("Your project is unique! It could help me with my research! Please create an issue with your project attached! https://github.com/Fritzforcode/PyPenguinOO/issues/new")

class PathError(PyPenguinError): pass


class ValidationError(PyPenguinError):
    def __init__(self, path: list[str], msg: str, condition: str|None = None):
        path_string = ""
        for item in path:
            if   isinstance(item, str):
                path_string += "." + item
            elif isinstance(item, int):
                path_string += "[" + str(item) + "]"
            else: raise ValueError()
        
        full_message = ""
        if path_string != "":
            full_message += f"At {path_string}: "
        if condition is not None:
            full_message += f"{condition}: "
        full_message += msg
        super().__init__(full_message)
        
class TypeValidationError(ValidationError): pass
class InvalidValueValidationError(ValidationError): pass
class RangeValidationError(ValidationError): pass
class MissingDropdownError(ValidationError): pass
class UnnecessaryDropdownError(ValidationError): pass
