from __future__ import annotations
import inspect
import os
import re
from functools import cached_property
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from pmp_manip.otility import grepr_dataclass, enforce_type, AbstractTreePath, NotSetType

from pmp_manip.utility.errors import MANIP_PathValidationError, MANIP_TypeValidationError, MANIP_RangeValidationError, MANIP_InvalidValueError


def _value_and_descr(obj, attr: str) -> tuple[Any, str]:
    return getattr(obj, attr), f"{attr} of a {_repr_type(obj.__class__)}"

def _repr_type(t: type | Any, notset_as_special: bool = True) -> str:
    """Format a type for display in error messages, similar to validation.py style.
    
    Args:
        t: The type to represent
        notset_as_special: If True, represent NotSetType as '<not set>' instead of the class name
    """
    if not isinstance(t, type):
        # Handle typing constructs
        return str(t)
    if notset_as_special and t is NotSetType:
        return "<not set>"
    if t.__module__ == "builtins":
        return t.__name__
    elif t.__module__.startswith("pmp_manip.utility."): # ignore exact file name
        return f"pmp_manip.utility.{t.__name__}"
    elif t.__module__.startswith("pmp_manip."): # ignore sub module name eg. "core"
        return f"pmp_manip.{t.__name__}"
    else:
        return f"{t.__module__}.{t.__name__}"

def _passes(fn: Callable[..., Any], *args, **kwargs) -> bool:
    try:
        fn(*args, **kwargs)
        return True
    except MANIP_PathValidationError:
        return False

@grepr_dataclass(frozen=True, unsafe_hash=True)
class Validator(Callable[..., None]):
    is_valid_fn: Callable[..., bool]
    error_cls: type[MANIP_PathValidationError]
    create_error_fn: Callable[..., str]
    pre_validate_fn: Callable[..., None] | None = None

    @cached_property
    def is_valid_arg_count(self) -> int:
        return len(inspect.signature(self.is_valid_fn).parameters) + 2 # - attr_value + self, path, attr

    def __call__(self, obj: Any, path: AbstractTreePath, attr: str, *args, condition: str | None = None) -> None:
        if self.pre_validate_fn is not None:
            self.pre_validate_fn(obj, path, attr, *args, condition=condition)
        
        arg_count = len(args) + 3 # self, path, attr
        if arg_count != self.is_valid_arg_count:
            print("a", args)
            raise TypeError(f"Validator expected {self.is_valid_arg_count} positional argument(s) but got {arg_count}")
        
        attr_value, descr = _value_and_descr(obj, attr)
        if not self.is_valid_fn(attr_value, *args):
            raise self.error_cls(path, self.create_error_fn(attr_value, descr, *args), condition)


class ValidateAttribute:
    VA_TYPE = Validator(
        is_valid_fn=lambda attr_value, t: _passes(enforce_type, attr_value, t),
        error_cls=MANIP_TypeValidationError,
        create_error_fn=lambda attr_value, descr, t: f"{descr} must be of type {_repr_type(t)} not {_repr_type(attr_value.__class__)}"
    )

    @staticmethod
    def VDESCR_TYPE(obj, path, descr, value, t, condition=None) -> None:
        if not isinstance(value, t):
            raise MANIP_TypeValidationError(path, f"{descr} must be of type {_repr_type(t)} not {_repr_type(value.__class__)}", condition)

    VA_MIN = Validator(
        is_valid_fn=lambda attr_value, min: attr_value >= min,
        error_cls=MANIP_RangeValidationError,
        create_error_fn=lambda attr_value, descr, min: f"{descr} must be at least {min}"
    )

    VA_RANGE = Validator(
        is_valid_fn=lambda attr_value, min, max: (attr_value >= min) and (attr_value <= max),
        error_cls=MANIP_RangeValidationError,
        create_error_fn=lambda attr_value, descr, min, max: f"{descr} must be at least {min} and at most {max}"
    )

    VA_MIN_LEN = Validator(
        is_valid_fn=lambda attr_value, min_len: len(attr_value) >= min_len,
        error_cls=MANIP_RangeValidationError,
        create_error_fn=lambda attr_value, descr, min_len: f"{descr} must contain at least {min_len} element(s)"
    )

    VA_EXACT_LEN = Validator(
        is_valid_fn=lambda attr_value, length: len(attr_value) == length,
        error_cls=MANIP_RangeValidationError,
        create_error_fn=lambda attr_value, descr, length: f"{descr} must contain exactly {length} element(s)"
    )

    VA_BOXED_COORD_PAIR = Validator(
        pre_validate_fn=lambda obj, path, attr, min_x, max_x, min_y, max_y, condition=None: (
            ValidateAttribute.VA_TYPE(obj, path, attr, tuple[int|float, int|float], condition=condition),
        ),
        is_valid_fn=lambda attr_value, min_x, max_x, min_y, max_y: (
                ((min_x is None) or (attr_value[0] >= min_x))
            and ((max_x is None) or (attr_value[0] <= max_x))
            and ((min_y is None) or (attr_value[1] >= min_y))
            and ((max_y is None) or (attr_value[1] <= max_y))
        ),
        error_cls=MANIP_RangeValidationError,
        create_error_fn=lambda attr_value, descr, min_x, max_x, min_y, max_y: (
            f"{descr} must be a coordinate pair(i.e. tuple of length 2). Each item must be an int or float. "
            f"The first coordinate must be in range from {min_x} to {max_x}. The second coordinate must be in "
            f"range from {min_y} to {max_y} not {attr_value}"
        )
    )

    VA_EQUAL = Validator(
        is_valid_fn=lambda attr_value, value: attr_value == value,
        error_cls=MANIP_InvalidValueError,
        create_error_fn=lambda attr_value, descr, value: f"{descr} must be {value!r}"
    )

    VA_NOT_EQUAL = Validator(
        is_valid_fn=lambda attr_value, value: attr_value != value,
        error_cls=MANIP_InvalidValueError,
        create_error_fn=lambda attr_value, descr, value: f"{descr} must NOT be {value!r}"
    )

    @staticmethod
    def VA_BIGGER_OR_EQUAL(obj, path, attr1, attr2, condition=None):
        attr1_value, attr1_descr = _value_and_descr(obj, attr1)
        attr2_value, attr2_descr = _value_and_descr(obj, attr2)
        if not(attr1_value >= attr2_value):
            raise MANIP_RangeValidationError(path, f"{attr1_descr} must be bigger then or equal to {attr2}", condition)

    VA_NOT_ONE_OF = Validator(
        is_valid_fn=lambda attr_value, forbidden_values: attr_value not in forbidden_values,
        error_cls=MANIP_InvalidValueError,
        create_error_fn=lambda attr_value, descr, forbidden_values: f"{descr} must not be one of {forbidden_values!r}"
    )

    VA_HEX_COLOR = Validator(
        is_valid_fn=lambda attr_value: isinstance(attr_value, str) and bool(re.fullmatch(r'#([0-9a-fA-F]{6})', attr_value)),
        error_cls=MANIP_InvalidValueError,
        create_error_fn=lambda attr_value, descr: f"{descr} must be a valid hex color eg. '#FF0956'"
    )

    VA_ALNUM = Validator(
        is_valid_fn=lambda attr_value: isinstance(attr_value, str) and attr_value.isalnum(),
        error_cls=MANIP_InvalidValueError,
        create_error_fn=lambda attr_value, descr: f"{descr} must contain only alpha-numeric characters"
    )

def is_valid_js_data_uri(s) -> bool:
    pattern = r"^data:application/javascript(;charset=[^,]+)?,.*"
    return re.match(pattern, s) is not None

def is_valid_directory_path(path_str: str) -> bool:
    path = Path(path_str)

    if path.exists():
        return path.is_dir()
    
    try:
        # Try to find a parent directory that exists
        parent = path.parent
        while not parent.exists():
            parent = parent.parent
        return os.access(parent, os.W_OK)
    except Exception:
        return False

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return (
            result.scheme in {"https", "http"} and
            bool(result.netloc) and
            "." in result.netloc  # rudimentary domain check
        )
    except Exception:
        return False


__all__ = [
    "ValidateAttribute",
    "is_valid_js_data_uri", "is_valid_directory_path", "is_valid_url",
]

