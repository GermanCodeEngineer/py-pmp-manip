from typing      import Any, Type, Callable, TypeVar
from types       import MethodType
from copy        import copy
from pytest      import raises

from pypenguin.utility import ValidationError

CPM = TypeVar("CPM")

def copymodify(obj: CPM, attr: str, value: Any) -> CPM:
    """
    Copy an object and modify an attribute
    `copymodify(x, 'y', z)` is equivalent to `x2 = copy.copy(x)\nx2.y = z`
    """
    if isinstance(getattr(obj, "_copymodify_", None), MethodType):
        return obj._copymodify_(attr, value)
    copied_obj = copy(obj)
    setattr(copied_obj, attr, value)
    return copied_obj

AVT = TypeVar("AVT")

def execute_attr_validation_tests(
        obj: AVT, 
        attr_tests: list[tuple[str, Any, Type[ValidationError]]], 
        validate_func: Callable[[AVT], None],
        func_args: list[Any]=[],
    ) -> None:
    """
    Test validation. For every "test" change one attribute to an invalid value and ensure an error is raised

    Args:
        obj: the object to 
        attr_tests: list of tuples, which contain
            - the attribute to change (str)
            - the value for the modified attribute
            - the type of error which is expected to be raised
        validate_func: the function to be called for every test with the modified object and the additional arguments
        func_args: additional arguments to provide to validate_func
    """
    for attr, value, error in attr_tests:
        modified_obj = copymodify(obj, attr, value)
        with raises(error):
            validate_func(modified_obj, *func_args)
