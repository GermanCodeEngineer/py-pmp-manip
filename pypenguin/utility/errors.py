class PyPenguinError(Exception):
    pass

class ThanksError(PyPenguinError):
    def __init__(self):
        super().__init__("Your project is special! It could help me with research! Please create an issue with your project attached! https://github.com/Fritzforcode/PyPenguinOO/issues/new")

class PathError(PyPenguinError):
    pass


