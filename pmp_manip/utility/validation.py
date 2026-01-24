from __future__ import annotations
import inspect
import os
import re
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from pmp_manip.otility import AbstractTreePath

from pmp_manip.utility.errors import MANIP_PathValidationError, MANIP_TypeValidationError, MANIP_RangeValidationError, MANIP_InvalidValueError


def _value_and_descr(obj, attr: str) -> tuple[Any, str]:
    return getattr(obj, attr), f"{attr} of a {_repr_type(obj.__class__)}"

def _repr_type(t: type) -> str:
    if t.__module__ == "builtins":
        return t.__name__
    elif t.__module__.startswith("pmp_manip.utility."): # ignore exact file name
        return f"pmp_manip.utility.{t.__name__}"
    elif t.__module__.startswith("pmp_manip."): # ignore sub module name eg. "core"
        return f"pmp_manip.{t.__name__}"
    else:
        return f"{t.__module__}.{t.__name__}"

def _make_validator(
        is_valid_fn: Callable[[Any], bool],
        error_cls: type[MANIP_PathValidationError], create_error_fn: Callable[..., str],
    ):
    is_valid_arg_count = len(inspect.signature(is_valid_fn).parameters) + 2 # - attr_value + self, path, attr

    def validator(self: Any, path: AbstractTreePath, attr: str, *args, condition: str | None = None) -> None:
        arg_count = len(args) + 3 # self, path, attr
        if arg_count != is_valid_arg_count:
            raise TypeError(f"Validator expected {is_valid_arg_count} positional argument(s) but got {arg_count}")
        
        attr_value, descr = _value_and_descr(self, attr)
        if not is_valid_fn(attr_value, *args):
            raise error_cls(path, create_error_fn(attr_value, descr, *args), condition)
    return validator

class ValidateAttribute:
    VA_TYPE = _make_validator(
        is_valid_fn=lambda attr_value, t: isinstance(attr_value, t),
        error_cls=MANIP_TypeValidationError,
        create_error_fn=lambda attr_value, descr, t: f"{descr} must be of type {_repr_type(t)} not {_repr_type(attr_value.__class__)}"
    )

    @staticmethod
    def VDESCR_TYPE(obj, path, descr, value, t, condition=None) -> None:
        if not isinstance(value, t):
            raise MANIP_TypeValidationError(path, f"{descr} must be of type {_repr_type(t)} not {_repr_type(value.__class__)}", condition)

    VA_NONE = _make_validator(
        is_valid_fn=lambda attr_value: attr_value is None,
        error_cls=MANIP_TypeValidationError,
        create_error_fn=lambda attr_value, descr: f"{descr} must be None not {_repr_type(attr_value.__class__)}"
    )

    VA_MIN = _make_validator(
        is_valid_fn=lambda attr_value, min: attr_value >= min,
        error_cls=MANIP_TypeValidationError,
        create_error_fn=lambda attr_value, descr, min: f"{descr} must be at least {min}"
    )

    VA_RANGE = _make_validator(
        is_valid_fn=lambda attr_value, min, max: (attr_value >= min) and (attr_value <= max),
        error_cls=MANIP_RangeValidationError,
        create_error_fn=lambda attr_value, descr, min, max: f"{descr} must be at least {min} and at most {max}"
    )

    VA_MIN_LEN = _make_validator(
        is_valid_fn=lambda attr_value, min_len: len(attr_value) >= min_len,
        error_cls=MANIP_RangeValidationError,
        create_error_fn=lambda attr_value, descr, min_len: f"{descr} must contain at least {min_len} element(s)"
    )
    # HERE

    #@staticmethod
    #def VA_MIN_LEN(obj, path, attr, min_len: int, condition=None):
    #    attr_value, descr = _value_and_descr(obj, attr)
    #    if len(attr_value) < min_len:
    #        raise MANIP_RangeValidationError(path, f"{descr} must contain at least {min_len} element(s)", condition)

    @staticmethod
    def VA_EXACT_LEN(obj, path, attr, length: int, condition=None):
        attr_value, descr = _value_and_descr(obj, attr)
        if len(attr_value) != length:
            raise MANIP_RangeValidationError(path, f"{descr} must contain exactly {length} element(s)", condition)

    @staticmethod
    def VA_BOXED_COORD_PAIR(
        obj, path, attr, 
        min_x: int|float|None, max_x: int|float|None, min_y:int|float|None, max_y: int|float|None, 
        condition=None
    ):
        attr_value, descr = _value_and_descr(obj, attr)
        msg = f"{descr} must be a coordinate pair. It must be a tuple of length 2. Each item must be an int or float. The first coordinate must be in range from {min_x} to {max_x}. The second coordinate must be in range from {min_y} to {max_y} not {attr_value}"
        if (
            (not isinstance(attr_value, tuple)) or (len(attr_value) != 2) 
            or (not isinstance(attr_value[0], (int, float))) 
            or (not isinstance(attr_value[1], (int, float)))
        ):
            raise MANIP_TypeValidationError(path, msg, condition)
        if (
            ((min_x is not None) and (attr_value[0] < min_x)) or ((max_x is not None) and (attr_value[0] > max_x))
            or ((min_y is not None) and (attr_value[1] < min_y)) or ((max_y is not None) and (attr_value[1] > max_y))
        ):
            raise MANIP_RangeValidationError(path, msg, condition)

    @staticmethod
    def VA_EQUAL(obj, path, attr, value, condition=None):
        attr_value, descr = _value_and_descr(obj, attr)
        if attr_value != value:
            raise MANIP_InvalidValueError(path, f"{descr} must be {value!r}", condition)

    @staticmethod
    def VA_NOT_EQUAL(obj, path, attr, value, condition=None):
        attr_value, descr = _value_and_descr(obj, attr)
        if attr_value == value:
            raise MANIP_InvalidValueError(path, f"{descr} must NOT be {value!r}", condition)

    @staticmethod
    def VA_BIGGER_OR_EQUAL(obj, path, attr1, attr2, condition=None):
        attr1_value, attr1_descr = _value_and_descr(obj, attr1)
        attr2_value, attr2_descr = _value_and_descr(obj, attr2)
        if not(attr1_value >= attr2_value):
            raise MANIP_RangeValidationError(path, f"{attr1_descr} must be bigger then or equal to {attr2}", condition)

    @staticmethod
    def VA_NOT_ONE_OF(obj, path, attr, forbidden_values, condition=None):
        attr_value, descr = _value_and_descr(obj, attr)
        if attr_value in forbidden_values:
            raise MANIP_InvalidValueError(path, f"{descr} must not be one of {forbidden_values!r}")

    @staticmethod
    def VA_HEX_COLOR(obj, path, attr, condition=None):
        attr_value, descr = _value_and_descr(obj, attr)
        msg = f"{descr} must be a valid hex color eg. '#FF0956'"
        if not isinstance(attr_value, str):
            raise MANIP_TypeValidationError(path, msg)
        if not bool(re.fullmatch(r'#([0-9a-fA-F]{6})', attr_value)):
            raise MANIP_InvalidValueError(path, msg)

    @staticmethod
    def VA_ALNUM(obj, path, attr, condition=None):
        attr_value, descr = _value_and_descr(obj, attr)
        attr_value: str
        if not attr_value.isalnum():
            raise MANIP_InvalidValueError(path, f"{descr} must contain only alpha-numeric characters")

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

