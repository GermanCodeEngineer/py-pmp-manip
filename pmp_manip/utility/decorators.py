from collections.abc import Callable as CallableABC
from copy            import copy
from dataclasses     import dataclass
from functools       import wraps
from inspect         import signature
from types           import NoneType, UnionType
from typing          import get_type_hints, get_origin, get_args, Callable, Any

from pmp_manip.utility.dual_key_dict import DualKeyDict
from pmp_manip.utility.repr          import grepr


def enforce_argument_types(func: Callable) -> Callable:
    """
    Decorator that enforces runtime type checks on function arguments
    based on the function's type annotations

    This supports deep validation for:
    - Built-in containers (list, tuple, set, dict)
    - Union types (`int | str`)
    - Optional types (`str | None`)
    - Callable (verifies the object is callable)
    - Custom DualKeyDict[K1, K2, V]

    Args:
        func: the function to wrap

    Raises:
        TypeError: if any argument does not match its annotated type
    """
    sig = signature(func)
    type_hints = get_type_hints(func)

    @wraps(func)
    def decorator(*args, **kwargs) -> Any:
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            if name in type_hints:
                expected_type = type_hints[name]
                _check_type(value, expected_type, name)

        return func(*args, **kwargs)

    return decorator

def _check_type(value, expected_type, name, _path="") -> None:
    """
    Recursively checks that a given value matches the expected type

    Supports:
    - Basic types: int, str, etc.
    - Generic containers: list[T], tuple[T1, T2], set[T], dict[K, V]
    - Union types: int | str
    - Optional types: str | None
    - Callable: ensures the value is callable
    - DualKeyDict[K1, K2, V]: verifies all keys and values

    Args:
        value: The actual value passed to the function
        expected_type: The type annotation from the function signature
        name: The argument name (for error messages)
        _path: Internal path used for nested data reporting

    Raises:
        TypeError: if the value does not match the expected type
    """
    origin = get_origin(expected_type)
    args = get_args(expected_type)
    label = f"argument '{name}'{_path}"

    # Basic types
    if origin is None:
        if not isinstance(value, expected_type):
            raise TypeError(f"{label} must be {expected_type}, got {type(value)}")
        return

    # Union types (int | str | None etc.)
    if origin is NoneType or origin is type(None):
        if value is not None:
            raise TypeError(f"{label} must be None, got {type(value)}")
        return

    if origin is None and expected_type is Any:
        return  # skip check for Any

    if origin is type(None):
        if value is not None:
            raise TypeError(f"{label} must be None, got {type(value)}")
        return

    if origin is Callable or origin is CallableABC:
        if not callable(value):
            raise TypeError(f"{label} must be callable, got {type(value)}")
        return

    # Union (int | str)
    if origin is UnionType:  # Python 3.10+
        for subtype in args:
            try:
                _check_type(value, subtype, name, _path)
                return
            except TypeError:
                continue
        raise TypeError(f"{label} must be one of {args}, got {type(value)}")

    # list[T]
    if origin is list:
        if not isinstance(value, list):
            raise TypeError(f"{label} must be a list, got {type(value)}")
        if args:
            for i, item in enumerate(value):
                _check_type(item, args[0], name, _path + f"[{i}]")
        return

    # tuple[T1, T2, ...] or tuple[T, ...]
    if origin is tuple:
        if not isinstance(value, tuple):
            raise TypeError(f"{label} must be a tuple, got {type(value)}")
        if args:
            if len(args) == 2 and args[1] is Ellipsis:
                for i, item in enumerate(value):
                    _check_type(item, args[0], name, _path + f"[{i}]")
            else:
                if len(value) != len(args):
                    raise TypeError(f"{label} expects {len(args)} elements, got {len(value)}")
                for i, (item, subtype) in enumerate(zip(value, args)):
                    _check_type(item, subtype, name, _path + f"[{i}]")
        return

    # set[T]
    if origin is set:
        if not isinstance(value, set):
            raise TypeError(f"{label} must be a set, got {type(value)}")
        if args:
            for i, item in enumerate(value):
                _check_type(item, args[0], name, _path + f"[{i}]")
        return

    # dict[K, V]
    if origin is dict:
        if not isinstance(value, dict):
            raise TypeError(f"{label} must be a dict, got {type(value)}")
        if args:
            k_type, v_type = args
            for k, v in value.items():
                _check_type(k, k_type, name, _path + f"[key={k!r}]")
                _check_type(v, v_type, name, _path + f"[key={k!r}]")
        return

    # DualKeyDict[K1, K2, V]
    if origin is DualKeyDict:
        if not isinstance(value, DualKeyDict):
            raise TypeError(f"{label} must be a DualKeyDict, got {type(value)}")
        if args:
            k1_type, k2_type, v_type = args
            for k1, k2, v in value.items_key1_key2():
                _check_type(k1, k1_type, name, _path + f"[key1={k1!r}]")
                _check_type(k2, k2_type, name, _path + f"[key2={k2!r}]")
                _check_type(v, v_type, name, _path + f"[key1={k1!r}, key2={k2!r}]")
        return

    # Fallback
    if not isinstance(value, expected_type):
        raise TypeError(f"{label} must be {expected_type}, got {type(value)}")

def grepr_dataclass(*, grepr_fields: list[str],
        init: bool = True, eq: bool = True, order: bool = False, 
        unsafe_hash: bool = False, frozen: bool = False, 
        match_args: bool = True, kw_only: bool = False, 
        slots: bool = False, weakref_slot: bool = False,
    ):
    """
    A decorator which combines @dataclass and a good representation system.
    Args:
        grepr_fields: fields for the good repr implementation
        parent_cls: class whose fields will also be included in the good repr impletementation
        init...: dataclass parameters
    """
    def decorator(cls: type):
        def __repr__(self) -> str:
            return grepr(self)
        cls.__repr__ = __repr__
        cls._grepr = True
        nonlocal grepr_fields
        fields = copy(grepr_fields)
        for base in cls.__bases__:
            if not getattr(base, "_grepr", False): continue
            for field in base._grepr_fields:
                if field in fields: continue
                fields.append(field)
        cls._grepr_fields = fields
        cls = dataclass(cls, 
            init=init, repr=False, eq=eq,
            order=order, unsafe_hash=unsafe_hash, frozen=frozen,
            match_args=match_args, kw_only=kw_only,
            slots=slots, weakref_slot=weakref_slot,
        )
        return cls
    return decorator


__all__ = ["enforce_argument_types", "grepr_dataclass"]

