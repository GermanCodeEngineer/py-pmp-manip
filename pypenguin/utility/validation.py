import json
import re
from typing      import Any
from dataclasses import dataclass

from pypenguin.utility.errors import TypeValidationError, RangeValidationError, InvalidValueError

def value_and_descr(obj, attr) -> tuple[Any, str]:
    return getattr(obj, attr), f"{attr} of a {obj.__class__.__name__}"

def AA_TYPE(obj, path, attr, t, condition=None) -> None:
    attr_value, descr = value_and_descr(obj, attr)
    if not isinstance(attr_value, t):
        raise TypeValidationError(path, f"{descr} must be of type {t.__name__} not {attr_value.__class__.__name__}", condition)

def AA_TYPES(obj, path, attr, ts, condition=None) -> None:
    attr_value, descr = value_and_descr(obj, attr)
    if not isinstance(attr_value, ts):
        types_str = "|".join([t.__name__ for t in ts])
        raise TypeValidationError(path, f"{descr} must be one of types {types_str} not {attr_value.__class__.__name__}", condition)

def AA_NONE(obj, path, attr, condition=None) -> None:
    attr_value, descr = value_and_descr(obj, attr)
    if attr_value is not None:
        raise TypeValidationError(path, f"{descr} must be None", condition)

def AA_NONE_OR_TYPE(obj, path, attr, t, condition=None) -> None:
    attr_value, descr = value_and_descr(obj, attr)
    if (attr_value is not None) and not(isinstance(attr_value, t)):
        raise TypeValidationError(path, f"{descr} must be either None or of type {t.__name__} not of type {attr_value.__class__.__name__}", condition)

def AA_LIST_OF_TYPE(obj, path, attr, t, condition=None) -> None:
    attr_value, descr = value_and_descr(obj, attr)
    msg = f"{descr} must be a list of {t.__name__}"
    if not isinstance(attr_value, list):
        raise TypeValidationError(path, f"{msg} not a {attr_value.__class__.__name__}", condition)
    for item in attr_value:
        if not isinstance(item, t):
            raise TypeValidationError(path, f"{msg} not of {item.__class__.__name__}", condition)

def AA_LIST_OF_TYPES(obj, path, attr, ts, condition=None) -> None:
    attr_value, descr = value_and_descr(obj, attr)
    types_str = "|".join([t.__name__ for t in ts])
    msg = f"{descr} must be a list. Each item must be one of types {types_str}"
    if not isinstance(attr_value, list):
        raise TypeValidationError(path, f"{msg} not a {attr_value.__class__.__name__}", condition)
    for item in attr_value:
        if not isinstance(item, ts):
            raise TypeValidationError(path, f"{msg} not of {item.__class__.__name__}", condition)

def AA_TUPLE_OF_TYPES(obj, path, attr, ts, condition=None) -> None:
    attr_value, descr = value_and_descr(obj, attr)
    types_str = "|".join([t.__name__ for t in ts])
    msg = f"{descr} must be a tuple. Each item must be one of types {types_str}"
    if not isinstance(attr_value, tuple):
        raise TypeValidationError(path, f"{msg} not a {attr_value.__class__.__name__}", condition)
    for item in attr_value:
        if not isinstance(item, ts):
            raise TypeValidationError(path, f"{msg} not of {item.__class__.__name__}", condition)

def AA_DICT_OF_TYPE(obj, path, attr, key_t, value_t, condition=None) -> None:
    attr_value, descr = value_and_descr(obj, attr)
    if not isinstance(attr_value, dict):
        raise TypeValidationError(path, f"{descr} must be a dict. Each key must be of type {key_t.__name__}. Each value must be of type {value_t.__name__}", condition)
    for key, value in attr_value.items():
        if not isinstance(key, key_t):
            raise TypeValidationError(path, f"{descr} must be a dict. Each key must be of type {key_t.__name__} NOT {key.__class__.__name__}. Each value must be of type {value_t.__name__}", condition)
        if not isinstance(value, value_t):
            raise TypeValidationError(path, f"{descr} must be a dict. Each key must be of type {key_t.__name__}. Each value must be of type {value_t.__name__} NOT {value.__class__.__name__}", condition)

def AA_MIN(obj, path, attr, min, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    if attr_value < min:
        raise RangeValidationError(path, f"{descr} must be at least {min}", condition)

def AA_MAX(obj, path, attr, max, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    if attr_value > max:
        raise RangeValidationError(path, f"{descr} must be at most {max}", condition)

def AA_RANGE(obj, path, attr, min, max, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    if (attr_value < min) or (attr_value > max):
        raise RangeValidationError(path, f"{descr} must be at least {min} and at most {max}", condition)

def AA_MIN_LEN(obj, path, attr, min_len: int, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    if len(attr_value) < min_len:
        raise RangeValidationError(path, f"{descr} must contain at least {min_len} element(s)")

def AA_COORD_PAIR(obj, path, attr, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    if (
           (not isinstance(attr_value, tuple)) or (len(attr_value) != 2) 
        or (not isinstance(attr_value[0], (int, float))) 
        or (not isinstance(attr_value[1], (int, float)))
    ):
        raise TypeValidationError(path, f"{descr} must be a coordinate pair. It must be a tuple of length 2. Each item must be an int or float", condition)

def AA_BOXED_COORD_PAIR(obj, path, attr, 
        min_x: int|float, max_x: int|float, min_y:int|float, max_y: int|float, 
    condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    if (
           (not isinstance(attr_value, tuple)) or (len(attr_value) != 2) 
        or (not isinstance(attr_value[0], (int, float))) 
        or (not isinstance(attr_value[1], (int, float)))
        or (attr_value[0] < min_x) or (attr_value[0] > max_x)
        or (attr_value[1] < min_y) or (attr_value[1] > max_y)
    ):
        raise TypeValidationError(path, f"{descr} must be a coordinate pair. It must be a tuple of length 2. Each item must be an int or float. The first coordinate must be in range from {min_x} to {max_x}. The second coordinate must be in range from {min_y} to {max_y} not {attr_value}", condition)

def AA_JSON_COMPATIBLE(obj, path, attr, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    try:
        json.dumps(attr_value)
        error = None
    except (TypeError, OverflowError):
        error = TypeValidationError(path, f"{descr} must be JSON-compatible", condition)
    if error is not None: # Trick to avoid "during handling of above exception"
        raise error

def AA_EQUAL(obj, path, attr, value, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    if attr_value != value:
        raise InvalidValueError(path, f"{descr} must be {value}", condition)

def AA_BIGGER_OR_EQUAL(obj, path, attr1, attr2, condition=None):
    attr1_value, attr1_descr = value_and_descr(obj, attr1)
    attr2_value, attr2_descr = value_and_descr(obj, attr2)
    if not(attr1_value >= attr2_value):
        raise RangeValidationError(path, f"{attr1_descr} must be bigger then or equal to {attr2}", condition)

def AA_NOT_ONE_OF(obj, path, attr, forbidden_values, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    if attr_value in forbidden_values:
        raise InvalidValueError(path, f"{descr} must not be one of {repr(forbidden_values)}")

def AA_HEX_COLOR(obj, path, attr, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    msg = f"{descr} must be a valid hex color eg. '#FF0956'"
    if not isinstance(attr_value, str):
        raise TypeValidationError(path, msg)
    if not bool(re.fullmatch(r'#([0-9a-fA-F]{6})', attr_value)):
        raise InvalidValueError(path, msg)

def AA_ALNUM(obj, path, attr, condition=None):
    attr_value, descr = value_and_descr(obj, attr)
    attr_value: str
    if not attr_value.isalnum():
        raise InvalidValueError(path, f"{descr} must contain only alpha-numeric characters")

from urllib.parse import urlparse

def is_valid_js_data_uri(s) -> bool:
    pattern = r"^data:application/javascript(;charset=[^,]+)?,.*"
    return re.match(pattern, s) is not None

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

@dataclass
class ValidationConfig:
    raise_when_monitor_position_outside_stage: bool = True
    raise_when_monitor_bigger_then_stage: bool = True

