class PyPenguinError(Exception):
    pass


class ThanksError(PyPenguinError):
    def __init__(self):
        super().__init__("Your project is unique! It could help me with my research! Please create an issue with your project attached! https://github.com/Fritzforcode/PyPenguinOO/issues/new")

class PathError(PyPenguinError): pass


class ValidationError(PyPenguinError):
    def __init__(self, path: list[str], msg: str):
        path_string = ""
        for item in path:
            if   isinstance(item, str):
                path_string += "." + item
            elif isinstance(item, int):
                path_string += "[" + str(item) + "]"
            else: raise ValueError()
        super().__init__(msg if path_string == "" else f"At {path_string}: {msg}")
        
class TypeValidationError(ValidationError): pass
class RangeValidationError(ValidationError): pass
