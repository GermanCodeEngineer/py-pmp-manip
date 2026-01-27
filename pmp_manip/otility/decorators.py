from __future__      import annotations
from collections.abc import Iterable, Callable as ABCCallable, Mapping, Sequence
from functools       import wraps
from inspect         import signature
from sys             import modules as sys_modules
from types           import UnionType
from typing          import (
    Any, Literal, Callable, Union, ParamSpec, TypeVar,
    get_origin, get_args, get_type_hints,
)

from gceutils.base import AbstractTreePath


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
                if (getattr(expected_type, "__module__", None) == "typing") and \
                    (getattr(expected_type, "__origin__", None) is None) and \
                    (getattr(expected_type, "__name__", None) == "TypeVar"):
                    continue
                if type(expected_type).__name__ == "TypeVar":
                    continue
                enforce_type(value, expected_type, path=AbstractTreePath(start_with_dot=False).add_attribute(name))

        return func(*args, **kwargs)

    return wrapper


def _is_union(tp: object) -> bool:
    return (
        get_origin(tp) is Union  # typing.Union[int, str]
        or isinstance(tp, UnionType)  # new style: int | str
    )

def _repr_type(t: type | Any, notset_as_special: bool = True) -> str:
    """Format a type for display in error messages, similar to validation.py style.
    
    Args:
        t: The type to represent
        notset_as_special: If True, represent NotSetType as '<not set>' instead of the class name
    """
    from gceutils.base import NotSetType
    
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

def enforce_type(value: Any, expected: Any, path: AbstractTreePath | None = None, condition: str | None = None, notset_as_special: bool = True) -> None:
    """
    Recursively checks that a given value matches the expected type.
    Runtime type enforcement that supports TypeVar, Union, Optional,
    type[T], list[T], tuple[T,...], dict[K,V], set[T], frozenset[T],
    Iterable[T], Sequence[T], Mapping[K,V], Callable, and Literal.
    Raises GU_TypeValidationError on mismatch.

    Args:
        value: the actual value passed to the function
        expected: The type annotation from the function signature
        path: AbstractTreePath for tracking location in nested data structures
        condition: Optional context for why this type is required (e.g., "because it's an instance of X")
        notset_as_special: If True, represent NotSetType as "<not set>" instead of the class name in error messages

    Raises:
        GU_TypeValidationError: If the value does not match the expected type
    """
    from gceutils.errors import GU_TypeValidationError
    
    if path is None:
        path = AbstractTreePath()
    
    # --- Handle Any ---
    if expected is Any:
        return

    # --- Handle TypeVar ---
    if isinstance(expected, TypeVar):
        if expected.__bound__ is not None:
            return enforce_type(value, expected.__bound__, path, condition)
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
                enforce_type(value, arm, path, condition, notset_as_special)
                return
            except GU_TypeValidationError:
                continue
        raise GU_TypeValidationError(
            path,
            f"must be one of types {_repr_type(expected, notset_as_special)} not {_repr_type(type(value), notset_as_special)}",
            condition
        )


    # --- Handle type[T] ---
    if origin is type:
        if not isinstance(value, type):
            raise GU_TypeValidationError(
                path,
                f"must be a class (type[T]) not {_repr_type(type(value), notset_as_special)}",
                condition
            )
        target = args[0] if args else object
        # if the inner arg is a TypeVar, reduce to its bound
        if isinstance(target, TypeVar):
            target = target.__bound__ or object
        if _is_union(target):
            targets = tuple(get_args(target))
        else:
            targets = (target,)
        if target is not object and not issubclass(value, targets):
            raise GU_TypeValidationError(
                path,
                f"must be a subclass of {targets} not {value}",
                condition
            )
        return

    # --- Handle dict[K,V] ---
    if origin is dict:
        key_t = args[0] if len(args) >= 1 else Any
        val_t = args[1] if len(args) >= 2 else Any
        if not isinstance(value, dict):
            raise GU_TypeValidationError(
                path,
                f"must be a dict not {_repr_type(type(value), notset_as_special)}",
                condition
            )
        keys_path = path.add_attribute("keys()")
        for i, (k, v) in enumerate(value.items()):
            enforce_type(k, key_t, keys_path.add_index_or_key(i), condition, notset_as_special)
            enforce_type(v, val_t, path.add_index_or_key(k), condition, notset_as_special)
        return

    # --- Handle tuple[T,...] or fixed tuple ---
    if origin is tuple:
        if not isinstance(value, tuple):
            raise GU_TypeValidationError(
                path,
                f"must be a tuple not {_repr_type(type(value), notset_as_special)}",
                condition
            )
        if len(args) == 2 and args[1] is Ellipsis:  # tuple[T, ...]
            elem_t = args[0]
            for i, item in enumerate(value):
                enforce_type(item, elem_t, path.add_index_or_key(i), condition, notset_as_special)
        elif args:  # tuple[T1, T2, ...]
            if len(value) != len(args):
                raise GU_TypeValidationError(
                    path,
                    f"must be a tuple of length {len(args)} not length {len(value)}",
                    condition
                )
            for i, (item, elem_t) in enumerate(zip(value, args)):
                enforce_type(item, elem_t, path.add_index_or_key(i), condition, notset_as_special)
        return

    # --- Handle list[T], set[T], frozenset[T] ---
    if origin in (list, set, frozenset):
        if not isinstance(value, origin):
            raise GU_TypeValidationError(
                path,
                f"must be a {origin.__name__} not {_repr_type(type(value), notset_as_special)}",
                condition
            )
        elem_t = args[0] if args else Any
        for i, item in enumerate(value):
            enforce_type(item, elem_t, path.add_index_or_key(i), condition, notset_as_special)
        return

    # --- Handle Callable ---
    if origin is ABCCallable or (origin is None and expected is ABCCallable):
        if not callable(value):
            raise GU_TypeValidationError(
                path,
                f"must be Callable not non-callable {_repr_type(type(value), notset_as_special)}",
                condition
            )
        # Note: We don't validate argument/return types for Callable[[int], str]
        # as that would require runtime signature inspection
        return

    # --- Handle Mapping[K, V] ---
    if origin is Mapping:
        key_t = args[0] if len(args) >= 1 else Any
        val_t = args[1] if len(args) >= 2 else Any
        if not isinstance(value, Mapping):
            raise GU_TypeValidationError(
                path,
                f"must be a Mapping not {_repr_type(type(value), notset_as_special)}",
                condition
            )
        keys_path = path.add_attribute("keys()")
        for i, (k, v) in enumerate(value.items()):
            enforce_type(k, key_t, keys_path.add_index_or_key(i), condition, notset_as_special)
            enforce_type(v, val_t, path.add_index_or_key(k), condition, notset_as_special)
        return

    # --- Handle Sequence[T] ---
    if origin is Sequence:
        if not isinstance(value, Sequence):
            raise GU_TypeValidationError(
                path,
                f"must be a Sequence not {_repr_type(type(value), notset_as_special)}",
                condition
            )
        elem_t = args[0] if args else Any
        for i, item in enumerate(value):
            enforce_type(item, elem_t, path.add_index_or_key(i), condition, notset_as_special)
        return

    # --- Handle Iterable[T] (excluding str/bytes to avoid char-by-char validation) ---
    if origin is Iterable:
        if not isinstance(value, Iterable):
            raise GU_TypeValidationError(
                path,
                f"must be an Iterable not {_repr_type(type(value), notset_as_special)}",
                condition
            )
        # Skip validation for strings/bytes - they're iterable but usually not intended
        # for element-wise type checking
        if isinstance(value, (str, bytes)):
            return
        elem_t = args[0] if args else Any
        for i, item in enumerate(value):
            enforce_type(item, elem_t, path.add_index_or_key(i), condition, notset_as_special)
        return

    # --- Handle Literal[V, ...] ---
    if origin is Literal:
        if value not in args:
            raise GU_TypeValidationError(
                path,
                f"must be one of Literal{args} not {value!r}",
                condition
            )
        return

    # --- Fallback: plain class or special typing objects ---
    if origin is None:
        # For a class, check isinstance
        if isinstance(expected, type):
            if not isinstance(value, expected):
                raise GU_TypeValidationError(
                    path,
                    f"must be of type {_repr_type(expected, notset_as_special)} not {_repr_type(type(value), notset_as_special)}",
                    condition
                )
        else:
            # For other typing constructs, like NewType, etc.
            try:
                if not isinstance(value, expected):
                    raise GU_TypeValidationError(
                        path,
                        f"must be of type {expected} not {_repr_type(type(value), notset_as_special)}",
                        condition
                    )
            except TypeError:
                # If isinstance fails (e.g., for NewType), raise error
                raise GU_TypeValidationError(
                    path,
                    f"must be of type {expected} not {_repr_type(type(value), notset_as_special)}",
                    condition
                )
        return

    # --- Last fallback: ignore parameterization, just check origin ---
    if not isinstance(value, origin):
        origin_name = getattr(origin, "__name__", str(origin))
        raise GU_TypeValidationError(
            path,
            f"must be of type {origin_name} not {_repr_type(type(value), notset_as_special)}",
            condition
        )


__all__ = ["enforce_argument_types", "enforce_type"]

