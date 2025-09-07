from collections.abc import Callable as CallableABC, Iterable
from copy            import copy
from dataclasses     import dataclass
from functools       import wraps
from inspect         import signature
from sys             import modules as sys_modules
from types           import NoneType, UnionType
from typing          import (
    Any, Callable, Union, ParamSpec, TypeVar, NoReturn,
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


def _is_union(tp: object) -> bool:
    return (
        get_origin(tp) is Union  # typing.Union[int, str]
        or isinstance(tp, UnionType)  # new style: int | str
    )
    
def _check_type(value: Any, expected: Any, name: str, path: str = "") -> None:
    """
    Recursively checks that a given value matches the expected type.
    Runtime type enforcement that supports TypeVar, Union, Optional,
    type[T], list[T], tuple[T,...], dict[K,V], Iterable[T].
    Raises TypeError on mismatch.


    Args:
        value: the actual value passed to the function
        expected_type: The type annotation from the function signature
        name: the argument name (for error messages)
        _path: internal path used for nested data reporting

    Raises:
        TypeError: If the value does not match the expected type
    """

    # --- Handle Any ---
    if expected is Any:
        return

    # --- Handle TypeVar ---
    if isinstance(expected, TypeVar):
        if expected.__bound__ is not None:
            return _check_type(value, expected.__bound__, name, path)
        # Unbound TypeVar -> accept anything
        return

    origin = get_origin(expected)
    args = get_args(expected)

    # --- Handle Union / Optional ---
    if _is_union(expected):
        # handle both typing.Union[...] and PEP 604 int | str
        arms = get_args(expected) if get_args(expected) else expected.__args__
        for arm in arms:
            try:
                _check_type(value, arm, name, path)
                return
            except TypeError:
                continue
        raise TypeError(f"{name}{path}: value {value!r} does not match {expected!r}")


    # --- Handle type[T] ---
    if origin is type:
        if not isinstance(value, type):
            raise TypeError(f"{name}{path}: expected a class (type[T]), got {type(value).__name__}")
        target = args[0] if args else object
        # if the inner arg is a TypeVar, reduce to its bound
        if isinstance(target, TypeVar):
            target = target.__bound__ or object
        if _is_union(target):
            targets = tuple(get_args(target))
        else:
            targets = (target,)
        if target is not object and not issubclass(value, targets):
            raise TypeError(f"{name}{path}: {value} is not a subclass of {targets}")
        return

    # --- Handle dict[K,V] ---
    if origin is dict:
        if not isinstance(value, dict):
            raise TypeError(f"{name}{path}: expected dict, got {type(value).__name__}")
        key_t, val_t = args if len(args) == 2 else (Any, Any)
        for k, v in value.items():
            _check_type(k, key_t, name, path + "[key]")
            _check_type(v, val_t, name, path + "[value]")
        return

    # --- Handle tuple[T,...] or fixed tuple ---
    if origin is tuple:
        if not isinstance(value, tuple):
            raise TypeError(f"{name}{path}: expected tuple, got {type(value).__name__}")
        if len(args) == 2 and args[1] is Ellipsis:  # tuple[T, ...]
            elem_t = args[0]
            for i, item in enumerate(value):
                _check_type(item, elem_t, name, path + f"[{i}]")
        elif args:  # tuple[T1, T2, ...]
            if len(value) != len(args):
                raise TypeError(f"{name}{path}: expected tuple of length {len(args)}, got {len(value)}")
            for i, (item, elem_t) in enumerate(zip(value, args)):
                _check_type(item, elem_t, name, path + f"[{i}]")
        return

    # --- Handle list[T], set[T], frozenset[T] ---
    if origin in (list, set, frozenset):
        if not isinstance(value, origin):
            raise TypeError(f"{name}{path}: expected {origin.__name__}, got {type(value).__name__}")
        elem_t = args[0] if args else Any
        for i, item in enumerate(value):
            _check_type(item, elem_t, name, path + f"[{i}]")
        return

    # --- Handle Iterable[T] ---
    if origin is Iterable:
        if not isinstance(value, Iterable):
            raise TypeError(f"{name}{path}: expected Iterable, got {type(value).__name__}")
        elem_t = args[0] if args else Any
        for i, item in enumerate(value):
            _check_type(item, elem_t, name, path + f"[{i}]")
        return

    # --- Fallback: plain class or special typing objects ---
    if origin is None:
        # For a class, check isinstance
        if isinstance(expected, type):
            if not isinstance(value, expected):
                raise TypeError(f"{name}{path}: expected {expected}, got {type(value)}")
        else:
            # For other typing constructs, like NewType, etc.
            try:
                if not isinstance(value, expected):
                    raise TypeError(f"{name}{path}: expected {expected}, got {type(value)}")
            except TypeError:
                # If isinstance fails (e.g., for NewType), raise error
                raise TypeError(f"{name}{path}: value {value!r} does not match expected type {expected}")
        return

    # --- Last fallback: ignore parameterization, just check origin ---
    if not isinstance(value, origin):
        raise TypeError(f"{name}{path}: expected {origin}, got {type(value)}")


def grepr_dataclass(*, grepr_fields: list[str], repr: bool = True,
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
        
        if repr:
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

