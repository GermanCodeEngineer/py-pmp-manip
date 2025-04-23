import json

from utility.errors import TypeValidationError, RangeValidationError

def ASSERT_TYPE(obj, path, descr, t) -> None:
    if not isinstance(obj, t):
        raise TypeValidationError(path, f"{descr} must be of type {t.__name__} not {obj.__class__.__name__}")

def ASSERT_TYPES(obj, path, descr, *ts) -> None:
    if not isinstance(obj, ts):
        types_str = "|".join([t.__name__ for t in ts])
        raise TypeValidationError(path, f"{descr} must be one of types {types_str} not {obj.__class__.__name__}")

def ASSERT_LIST_OF_TYPE(obj, path, descr, t) -> None:
    msg = f"{descr} must be a list of {t.__name__}"
    if not isinstance(obj, list):
        raise TypeValidationError(path, f"{msg} not a {obj.__class__.__name__}")
    for item in obj:
        if not isinstance(item, t):
            raise TypeValidationError(path, f"{msg} not of {item.__class__.__name__}")

def ASSERT_DICT_OF_TYPE(obj, path, descr, key_t, value_t):
    if not isinstance(obj, dict):
        raise TypeValidationError(path, f"{descr} must be a dict. Each key must be of type {key_t.__name__}. Each value must be of type {value_t.__name__}")
    for key, value in obj.items():
        if not isinstance(key, key_t):
            raise TypeValidationError(path, f"{descr} must be a dict. Each key must be of type {key_t.__name__} NOT {key.__class__.__name__}. Each value must be of type {value_t.__name__}")
        if not isinstance(value, value_t):
            raise TypeValidationError(path, f"{descr} must be a dict. Each key must be of type {key_t.__name__}. Each value must be of type {value_t.__name__} NOT {value.__class__.__name__}")

def ASSERT_MIN(obj, path, descr, min):
    if obj < min:
        raise RangeValidationError(path, f"{descr} must be at least {min}")

def ASSERT_MAX(obj, path, descr, max):
    if obj > max:
        raise RangeValidationError(path, f"{descr} must be at most {max}")

def ASSERT_RANGE(obj, path, descr, min, max):
    ASSERT_MIN(obj, path, descr, min)
    ASSERT_MAX(obj, path, descr, max)

def ASSERT_COORD_PAIR(obj, path, descr):
    if (
           (not isinstance(obj, tuple)) or (len(obj) != 2) 
        or (not isinstance(obj[0], (int, float))) 
        or (not isinstance(obj[1], (int, float)))
    ):
        raise TypeValidationError(path, f"{descr} must be a coordinate pair. It must be a tuple of length 2. Each item must be an int or float")

def ASSERT_JSON_COMPATIBLE(obj, path, descr):
    try:
        json.dumps(obj)
        error = None
    except (TypeError, OverflowError):
        error = TypeValidationError(path, f"{descr} must be JSON-compatible")
    if error is not None:
        raise error


def AA_TYPE(obj, path, attr, t) -> None:
    ASSERT_TYPE(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}", t)

def AA_TYPES(obj, path, attr, *ts) -> None:
    ASSERT_TYPES(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}", *ts)

def AA_LIST_OF_TYPE(obj, path, attr, t) -> None:
    ASSERT_LIST_OF_TYPE(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}", t)

def AA_DICT_OF_TYPE(obj, path, attr, key_t, value_t) -> None:
    ASSERT_DICT_OF_TYPE(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}", key_t, value_t)

def AA_MIN(obj, path, attr, min):
    ASSERT_MIN(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}", min)

def AA_MAX(obj, path, attr, max):
    ASSERT_MAX(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}", max)

def AA_RANGE(obj, path, attr, min, max):
    ASSERT_RANGE(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}", min, max)

def AA_COORD_PAIR(obj, path, attr):
    ASSERT_COORD_PAIR(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}")

def AA_JSON_COMPATIBLE(obj, path, attr):
    ASSERT_JSON_COMPATIBLE(getattr(obj, attr), path, f"{attr} of a {obj.__class__.__name__}")

