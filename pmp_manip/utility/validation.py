import json
import os
import re
from typing       import Any
from pathlib      import Path
from urllib.parse import urlparse

from pmp_manip.utility.errors import MANIP_TypeValidationError, MANIP_RangeValidationError, MANIP_InvalidValueError


def _value_and_descr(obj, attr: str) -> tuple[Any, str]:
    return getattr(obj, attr), f"{attr} of a {_repr_type(obj.__class__)}"

def _repr_type(t: type) -> str:
    if t.__module__ == "builtins":
        return t.__name__
    elif t.__module__.startswith("pmp_manip."): # ignore sub module name eg. "core"
        return f"pmp_manip.{t.__name__}"
    else:
        return f"{t.__module__}.{t.__name__}"

def AA_TYPE(obj, path, attr, t, condition=None) -> None:
    attr_value, descr = _value_and_descr(obj, attr)
    if not isinstance(attr_value, t):
        raise MANIP_TypeValidationError(path, f"{descr} must be of type {_repr_type(t)} not {_repr_type(attr_value.__class__)}", condition)

def AA_TYPES(obj, path, attr, ts, condition=None) -> None:
    assert len(ts) >= 1
    if len(ts) == 1:
        return AA_TYPE(obj, path, attr, ts[0], condition=condition)
    attr_value, descr = _value_and_descr(obj, attr)
    if not isinstance(attr_value, ts):
        types_str = "|".join([_repr_type(t) for t in ts])
        raise MANIP_TypeValidationError(path, f"{descr} must be one of types {types_str} not {_repr_type(attr_value.__class__)}", condition)

def AA_NONE(obj, path, attr, condition=None) -> None:
    attr_value, descr = _value_and_descr(obj, attr)
    if attr_value is not None:
        raise MANIP_TypeValidationError(path, f"{descr} must be None", condition)

def AA_NONE_OR_TYPE(obj, path, attr, t, condition=None) -> None:
    attr_value, descr = _value_and_descr(obj, attr)
    if (attr_value is not None) and not(isinstance(attr_value, t)):
        raise MANIP_TypeValidationError(path, f"{descr} must be either None or of type {_repr_type(t)} not of type {_repr_type(attr_value.__class__)}", condition)

def AA_LIST_OF_TYPE(obj, path, attr, t, condition=None) -> None:
    attr_value, descr = _value_and_descr(obj, attr)
    msg = f"{descr} must be a list of {_repr_type(t)}"
    if not isinstance(attr_value, list):
        raise MANIP_TypeValidationError(path, f"{msg} not a {_repr_type(attr_value.__class__)}", condition)
    for item in attr_value:
        if not isinstance(item, t):
            raise MANIP_TypeValidationError(path, f"{msg} not of {_repr_type(item.__class__)}", condition)

def AA_LIST_OF_TYPES(obj, path, attr, ts, condition=None) -> None:
    attr_value, descr = _value_and_descr(obj, attr)
    types_str = "|".join([_repr_type(t) for t in ts])
    msg = f"{descr} must be a list. Each item must be one of types {types_str}"
    if not isinstance(attr_value, list):
        raise MANIP_TypeValidationError(path, f"{msg} not a {_repr_type(attr_value.__class__)}", condition)
    for item in attr_value:
        if not isinstance(item, ts):
            raise MANIP_TypeValidationError(path, f"{msg} not of {_repr_type(item.__class__)}", condition)

def AA_TUPLE_OF_TYPES(obj, path, attr, ts, condition=None) -> None:
    attr_value, descr = _value_and_descr(obj, attr)
    types_str = "|".join([_repr_type(t) for t in ts])
    msg = f"{descr} must be a tuple. Each item must be one of types {types_str}"
    if not isinstance(attr_value, tuple):
        raise MANIP_TypeValidationError(path, f"{msg} not a {_repr_type(attr_value.__class__)}", condition)
    for item in attr_value:
        if not isinstance(item, ts):
            raise MANIP_TypeValidationError(path, f"{msg} not of {_repr_type(item.__class__)}", condition)

def AA_DICT_OF_TYPE(obj, path, attr, key_t, value_t, condition=None) -> None:
    attr_value, descr = _value_and_descr(obj, attr)
    if not isinstance(attr_value, dict):
        raise MANIP_TypeValidationError(path, f"{descr} must be a dict NOT a {_repr_type(attr_value.__class__)}. Each key must be of type {_repr_type(key_t)}. Each value must be of type {_repr_type(value_t)}", condition)
    for key, value in attr_value.items():
        if not isinstance(key, key_t):
            raise MANIP_TypeValidationError(path, f"{descr} must be a dict. Each key must be of type {_repr_type(key_t)} NOT {_repr_type(key.__class__)}. Each value must be of type {_repr_type(value_t)}", condition)
        if not isinstance(value, value_t):
            raise MANIP_TypeValidationError(path, f"{descr} must be a dict. Each key must be of type {_repr_type(key_t)}. Each value must be of type {_repr_type(value_t)} NOT {_repr_type(value.__class__)}", condition)

def AA_MIN(obj, path, attr, min, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if attr_value < min:
        raise MANIP_RangeValidationError(path, f"{descr} must be at least {min}", condition)

def AA_MAX(obj, path, attr, max, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if attr_value > max:
        raise MANIP_RangeValidationError(path, f"{descr} must be at most {max}", condition)

def AA_RANGE(obj, path, attr, min, max, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if (attr_value < min) or (attr_value > max):
        raise MANIP_RangeValidationError(path, f"{descr} must be at least {min} and at most {max}", condition)

def AA_MIN_LEN(obj, path, attr, min_len: int, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if len(attr_value) < min_len:
        raise MANIP_RangeValidationError(path, f"{descr} must contain at least {min_len} element(s)")

def AA_EXACT_LEN(obj, path, attr, length: int, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if len(attr_value) != length:
        raise MANIP_RangeValidationError(path, f"{descr} must contain exactly {length} element(s)")

def AA_COORD_PAIR(obj, path, attr, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if (
           (not isinstance(attr_value, tuple)) or (len(attr_value) != 2) 
        or (not isinstance(attr_value[0], (int, float))) 
        or (not isinstance(attr_value[1], (int, float)))
    ):
        raise MANIP_TypeValidationError(path, f"{descr} must be a coordinate pair. It must be a tuple of length 2. Each item must be an int or float", condition)

def AA_BOXED_COORD_PAIR(
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

def AA_JSON_COMPATIBLE(obj, path, attr, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    try:
        json.dumps(attr_value)
        error = None
    except (TypeError, OverflowError):
        error = MANIP_TypeValidationError(path, f"{descr} must be JSON-compatible", condition)
    if error is not None: # Trick to avoid "during handling of above exception"
        raise error

def AA_EQUAL(obj, path, attr, value, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if attr_value != value:
        raise MANIP_InvalidValueError(path, f"{descr} must be {value!r}", condition)

def AA_NOT_EQUAL(obj, path, attr, value, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if attr_value == value:
        raise MANIP_InvalidValueError(path, f"{descr} must NOT be {value!r}", condition)

def AA_BIGGER_OR_EQUAL(obj, path, attr1, attr2, condition=None):
    attr1_value, attr1_descr = _value_and_descr(obj, attr1)
    attr2_value, attr2_descr = _value_and_descr(obj, attr2)
    if not(attr1_value >= attr2_value):
        raise MANIP_RangeValidationError(path, f"{attr1_descr} must be bigger then or equal to {attr2}", condition)

def AA_NOT_ONE_OF(obj, path, attr, forbidden_values, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    if attr_value in forbidden_values:
        raise MANIP_InvalidValueError(path, f"{descr} must not be one of {forbidden_values!r}")

def AA_HEX_COLOR(obj, path, attr, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    msg = f"{descr} must be a valid hex color eg. '#FF0956'"
    if not isinstance(attr_value, str):
        raise MANIP_TypeValidationError(path, msg)
    if not bool(re.fullmatch(r'#([0-9a-fA-F]{6})', attr_value)):
        raise MANIP_InvalidValueError(path, msg)

def AA_ALNUM(obj, path, attr, condition=None):
    attr_value, descr = _value_and_descr(obj, attr)
    attr_value: str
    if not attr_value.isalnum():
        raise MANIP_InvalidValueError(path, f"{descr} must contain only alpha-numeric characters")

def AA_NONE_OR_CALLABLE(obj, path, attr, condition=None) -> None:
    attr_value, descr = _value_and_descr(obj, attr)
    if (attr_value is not None) and not(callable(attr_value)):
        raise MANIP_TypeValidationError(path, f"{descr} must be None or a callable object(e.g. function, lambda) not {_repr_type(attr_value.__class__)}", condition)

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
    "AA_TYPE", "AA_TYPES", "AA_NONE", "AA_NONE_OR_TYPE", 
    "AA_LIST_OF_TYPE", "AA_LIST_OF_TYPES", "AA_TUPLE_OF_TYPES", "AA_DICT_OF_TYPE",
    "AA_MIN", "AA_MAX", "AA_RANGE", "AA_MIN_LEN", "AA_EXACT_LEN", "AA_COORD_PAIR", "AA_BOXED_COORD_PAIR",
    "AA_JSON_COMPATIBLE", "AA_HEX_COLOR", "AA_ALNUM", "AA_NONE_OR_CALLABLE",
    "AA_EQUAL", "AA_NOT_EQUAL", "AA_BIGGER_OR_EQUAL", "AA_NOT_ONE_OF", 
    "is_valid_js_data_uri", "is_valid_directory_path", "is_valid_url",
]

