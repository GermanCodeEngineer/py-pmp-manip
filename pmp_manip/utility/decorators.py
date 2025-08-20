from collections.abc import Callable as CallableABC
from copy            import copy
from dataclasses     import dataclass
from functools       import wraps
from inspect         import signature
from sys             import modules as sys_modules
from types           import NoneType, UnionType
from typing          import (
    Any, Callable, ParamSpec, TypeVar, NoReturn,
    get_origin, get_args, get_type_hints,
)


from pmp_manip.utility.repr import grepr


PARAM_SPEC = ParamSpec("PARAM_SPEC")
RETURN_T = TypeVar("RETURN_T")
TYPE_T = TypeVar("TYPE_T", bound=type)


def enforce_argument_types(func: Callable[PARAM_SPEC, RETURN_T]) -> Callable[PARAM_SPEC, RETURN_T]:
    """
    Decorator that enforces runtime type checks on function arguments
    based on the function's type annotations

    This supports deep validation for:
    - Built-in containers (list, tuple, set, dict)
    - Union types (`int | str`)
    - Optional types (`str | None`)
    - Callable (verifies the object is callable)
    - Custom DualKeyDict[K1, K2, V]

    Works with:
    - Functions
    - Instance methods
    - Class methods
    - Static methods

    Args:
        func: the function to wrap

    Raises:
        TypeError: if any argument does not match its annotated type
    """
    # Unwrap and rewrap classmethod/staticmethod
    
    if isinstance(func, (classmethod, staticmethod)):
        original_func = func.__func__
        wrapped = enforce_argument_types(original_func)
        return type(func)(wrapped)

    sig = signature(func)

    @wraps(func)
    def wrapper(*args: PARAM_SPEC.args, **kwargs: PARAM_SPEC.kwargs) -> RETURN_T:
        type_hints = get_type_hints(func, globalns=sys_modules[func.__module__].__dict__)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        skip_first = False
        if bound_args.arguments:
            first_name = next(iter(bound_args.arguments))
            if first_name in ("self", "cls"):
                skip_first = True

        for i, (name, value) in enumerate(bound_args.arguments.items()):
            if skip_first and i == 0:
                continue
            if name in type_hints:
                expected_type = type_hints[name]
                # Ignore TypeVar type hints
                if getattr(expected_type, "__module__", None) == "typing" and getattr(expected_type, "__origin__", None) is None and getattr(expected_type, "__name__", None) == "TypeVar":
                    continue
                if type(expected_type).__name__ == "TypeVar":
                    continue
                _check_type(value, expected_type, name)

        return func(*args, **kwargs)

    return wrapper


def _check_type(value: Any, expected_type: Any, name: str, _path: str = "") -> None:
    """
    Recursively checks that a given value matches the expected type.

    Args:
        value: the actual value passed to the function
        expected_type: The type annotation from the function signature
        name: the argument name (for error messages)
        _path: internal path used for nested data reporting

    Raises:
        TypeError: If the value does not match the expected type
    """
    from collections.abc import Iterable as IterableABC
    from pmp_manip.utility.dual_key_dict import DualKeyDict
    origin = get_origin(expected_type)
    args = get_args(expected_type)
    label = f"argument '{name}'{_path}"

    # Any
    if expected_type is Any:
        return

    # NoneType
    if expected_type is NoneType:
        if value is not None:
            raise TypeError(f"{label} must be None, got {type(value)}")
        return

    # Ignore TypeVar
    if isinstance(expected_type, TypeVar) or type(expected_type).__name__ == "TypeVar":
        return

    # Non-generic types
    if origin is None:
        # Ignore typing generics (e.g., list[int])
        if hasattr(expected_type, "__origin__") and expected_type.__origin__ is not None:
            return
        # Ignore TypeVar (redundant, but safe)
        if isinstance(expected_type, TypeVar) or type(expected_type).__name__ == "TypeVar":
            return
        if not isinstance(value, expected_type):
            raise TypeError(f"{label} must be {expected_type}, got {type(value)}")
        return

    # Callable
    if origin in (Callable, CallableABC):
        if not callable(value):
            raise TypeError(f"{label} must be callable, got {type(value)}")
        return

    # Union (including Optional)
    if origin is UnionType:  # Python 3.10+ syntax `|`
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

    # Iterable[T]
    if origin in (IterableABC,):
        if not isinstance(value, IterableABC):
            raise TypeError(f"{label} must be an Iterable, got {type(value)}")
        if args:
            for i, item in enumerate(value):
                _check_type(item, args[0], name, _path + f"[{i}]")
        return

    # Fallback
    if not isinstance(value, expected_type):
        raise TypeError(f"{label} must be {expected_type}, got {type(value)}")

def grepr_dataclass(*, grepr_fields: list[str],
        init: bool = True, eq: bool = True, order: bool = True, 
        unsafe_hash: bool = False, frozen: bool = False, 
        match_args: bool = True, kw_only: bool = False, 
        slots: bool = False, weakref_slot: bool = False,
        forbid_init_only_subcls: bool = False,
        suggested_subcls_names: list[str] | None = None,
    ):
    """
    A decorator which combines @dataclass and a good representation system.
    Args:
        grepr_fields: fields for the good repr implementation
        init...: dataclass parameters (except for order which is True by default here)
        forbid_init_only_subcls: add a __init__ method to raises a NotImplementedError, which tells the user to use the subclasses.
    """
    if init: assert not forbid_init_only_subcls
    if init: assert suggested_subcls_names is None
    def decorator(cls: TYPE_T) -> TYPE_T:
        if forbid_init_only_subcls:
            def __init__(self, *args, **kwargs) -> None | NoReturn:
                if type(self) is cls:
                    msg = f"Can not initialize parent class {cls!r} directly. Please use the subclasses"
                    if suggested_subcls_names:
                        msg += " "
                        msg += ", ".join(suggested_subcls_names)
                    msg += "."
                    raise NotImplementedError(msg)
            cls.__init__ = __init__

        def __repr__(self, *args, **kwargs) -> str:
            return grepr(self, *args, **kwargs)
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

