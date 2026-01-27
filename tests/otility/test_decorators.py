from __future__ import annotations
import pytest
from types import SimpleNamespace
from typing import Any, TypeVar, Literal, NewType, Iterable, Sequence, Mapping

from gceutils import decorators

from gceutils.decorators import enforce_type, enforce_argument_types, TYPE_T
from gceutils.errors import GU_TypeValidationError

T_GLOBAL = TypeVar("T_GLOBAL")
FAKE_TYPEVAR = SimpleNamespace(__module__="typing", __origin__=None, __name__="TypeVar")


class TestEnforceType:
    """Test enforce_type function."""
    
    # --- Basic Types ---
    
    def test_enforce_type_int(self):
        """Test int type enforcement."""
        enforce_type(42, int)
        with pytest.raises(GU_TypeValidationError):
            enforce_type("42", int)
    
    def test_enforce_type_str(self):
        """Test str type enforcement."""
        enforce_type("hello", str)
        with pytest.raises(GU_TypeValidationError):
            enforce_type(42, str)
    
    def test_enforce_type_bool(self):
        """Test bool type enforcement."""
        enforce_type(True, bool)
        # Note: bool is a subclass of int, so we test with non-bool values
        with pytest.raises(GU_TypeValidationError):
            enforce_type("True", bool)
    
    def test_enforce_type_float(self):
        """Test float type enforcement."""
        enforce_type(3.14, float)
        with pytest.raises(GU_TypeValidationError):
            enforce_type(3, float)
    
    def test_enforce_type_none(self):
        """Test None type enforcement."""
        enforce_type(None, type(None))
        with pytest.raises(GU_TypeValidationError):
            enforce_type("None", type(None))
    
    # --- Any Type ---
    
    def test_enforce_type_any(self):
        """Test Any type accepts any value."""
        enforce_type(42, Any)
        enforce_type("hello", Any)
        enforce_type(None, Any)
        enforce_type([1, 2, 3], Any)
    
    # --- Union Types ---
    
    def test_enforce_type_union(self):
        """Test union type enforcement."""
        enforce_type(42, int | str)
        enforce_type("hello", int | str)
        with pytest.raises(GU_TypeValidationError):
            enforce_type(3.14, int | str)
    
    def test_enforce_type_optional(self):
        """Test optional type enforcement."""
        enforce_type("hello", str | None)
        enforce_type(None, str | None)
        with pytest.raises(GU_TypeValidationError):
            enforce_type(42, str | None)
    
    # --- List Types ---
    
    def test_enforce_type_list_basic(self):
        """Test basic list type enforcement."""
        enforce_type([1, 2, 3], list)
        with pytest.raises(GU_TypeValidationError):
            enforce_type((1, 2, 3), list)
    
    def test_enforce_type_list_of_int(self):
        """Test list[int] enforcement."""
        enforce_type([1, 2, 3], list[int])
        with pytest.raises(GU_TypeValidationError):
            enforce_type([1, "2", 3], list[int])
    
    def test_enforce_type_list_of_str(self):
        """Test list[str] enforcement."""
        enforce_type(["a", "b", "c"], list[str])
        with pytest.raises(GU_TypeValidationError):
            enforce_type(["a", 2, "c"], list[str])
    
    def test_enforce_type_nested_list(self):
        """Test nested list enforcement."""
        enforce_type([[1, 2], [3, 4]], list[list[int]])
        with pytest.raises(GU_TypeValidationError):
            enforce_type([[1, 2], [3, "4"]], list[list[int]])
    
    def test_enforce_type_empty_list(self):
        """Test empty list enforcement."""
        enforce_type([], list[int])
        enforce_type([], list[str])
    
    # --- Tuple Types ---
    
    def test_enforce_type_tuple_basic(self):
        """Test basic tuple type enforcement."""
        enforce_type((1, 2, 3), tuple)
        with pytest.raises(GU_TypeValidationError):
            enforce_type([1, 2, 3], tuple)
    
    def test_enforce_type_tuple_homogeneous(self):
        """Test tuple[int, ...] enforcement."""
        enforce_type((1, 2, 3), tuple[int, ...])
        with pytest.raises(GU_TypeValidationError):
            enforce_type((1, "2", 3), tuple[int, ...])
    
    def test_enforce_type_tuple_fixed(self):
        """Test fixed-length tuple enforcement."""
        enforce_type((1, "hello", 3.14), tuple[int, str, float])
        with pytest.raises(GU_TypeValidationError):
            enforce_type((1, "hello"), tuple[int, str, float])
        with pytest.raises(GU_TypeValidationError):
            enforce_type((1, 2, 3.14), tuple[int, str, float])
    
    # --- Set Types ---
    
    def test_enforce_type_set_basic(self):
        """Test basic set type enforcement."""
        enforce_type({1, 2, 3}, set)
        with pytest.raises(GU_TypeValidationError):
            enforce_type([1, 2, 3], set)
    
    def test_enforce_type_set_of_int(self):
        """Test set[int] enforcement."""
        enforce_type({1, 2, 3}, set[int])
        with pytest.raises(GU_TypeValidationError):
            enforce_type({1, "2", 3}, set[int])
    
    def test_enforce_type_frozenset_of_str(self):
        """Test frozenset[str] enforcement."""
        enforce_type(frozenset(["a", "b"]), frozenset[str])
        with pytest.raises(GU_TypeValidationError):
            enforce_type(frozenset(["a", 2]), frozenset[str])
    
    # --- Dict Types ---
    
    def test_enforce_type_dict_basic(self):
        """Test basic dict type enforcement."""
        enforce_type({"a": 1}, dict)
        with pytest.raises(GU_TypeValidationError):
            enforce_type([("a", 1)], dict)
    
    def test_enforce_type_dict_str_int(self):
        """Test dict[str, int] enforcement."""
        enforce_type({"a": 1, "b": 2}, dict[str, int])
        with pytest.raises(GU_TypeValidationError):
            enforce_type({1: 1, "b": 2}, dict[str, int])
        with pytest.raises(GU_TypeValidationError):
            enforce_type({"a": "1", "b": 2}, dict[str, int])
    
    def test_enforce_type_nested_dict(self):
        """Test nested dict enforcement."""
        enforce_type({"a": {"x": 1}}, dict[str, dict[str, int]])
        with pytest.raises(GU_TypeValidationError):
            enforce_type({"a": {"x": "1"}}, dict[str, dict[str, int]])
    
    def test_enforce_type_empty_dict(self):
        """Test empty dict enforcement."""
        enforce_type({}, dict[str, int])

    def test_enforce_type_mapping_and_sequence_and_iterable(self):
        """Cover Mapping/Sequence/Iterable branches including element recursion."""
        enforce_type({"a": 1, "b": 2}, Mapping[str, int])
        with pytest.raises(GU_TypeValidationError):
            enforce_type(123, Mapping[str, int])

        enforce_type([1, 2], Sequence[int])
        with pytest.raises(GU_TypeValidationError):
            enforce_type(123, Sequence[int])

        enforce_type([1, 2], Iterable[int])
        with pytest.raises(GU_TypeValidationError):
            enforce_type(123, Iterable[int])
        # Strings are iterables but should short-circuit element checks
        enforce_type("abc", Iterable[int])

        # Callable branch return path
        from collections.abc import Callable as ABCCallable
        enforce_type(lambda x: x, ABCCallable)

    def test_enforce_type_literal_and_newtype_and_fallback_origin(self):
        """Cover Literal success/failure, NewType TypeError path, and last-origin fallback."""
        enforce_type("x", Literal["x", "y"])
        with pytest.raises(GU_TypeValidationError):
            enforce_type("z", Literal["x", "y"])

        UserId = NewType("UserId", int)
        with pytest.raises(GU_TypeValidationError):
            enforce_type(1, UserId)

        # origin fallback: AsyncGenerator origin, non-instance triggers last raise
        from collections.abc import AsyncGenerator
        with pytest.raises(GU_TypeValidationError):
            enforce_type(1, AsyncGenerator[int, None])

        # origin None with non-type expected where isinstance works (use tuple sentinel)
        enforce_type(1, (int,))
        with pytest.raises(GU_TypeValidationError):
            enforce_type(1, (str,))

        # origin None with non-type expected where isinstance raises TypeError
        with pytest.raises(GU_TypeValidationError):
            enforce_type(1, Ellipsis)

    def test_enforce_type_typevar_bound_and_type_subclass_checks(self):
        """Exercise TypeVar bound and type[T] subclass/union checks."""
        BoundInt = TypeVar("BoundInt", bound=int)
        enforce_type(5, BoundInt)  # should delegate to bound

        with pytest.raises(GU_TypeValidationError):
            enforce_type(str, type[int])

        with pytest.raises(GU_TypeValidationError):
            enforce_type(dict, type[int | str])

        # type[TypeVar] with bound triggers bound extraction
        BoundToInt = TypeVar("BoundToInt", bound=int)
        enforce_type(int, type[BoundToInt])
        with pytest.raises(GU_TypeValidationError):
            enforce_type(str, type[BoundToInt])

        Unbound = TypeVar("Unbound")
        enforce_type(str, type[Unbound])

        with pytest.raises(GU_TypeValidationError):
            enforce_type(5, type[int])

    def test_enforce_type_tuple_and_list_mismatch(self):
        """Cover tuple and list mismatch raises and _repr_type module formatting paths."""
        with pytest.raises(GU_TypeValidationError):
            enforce_type([1, 2, 3], tuple[int, int])

        with pytest.raises(GU_TypeValidationError):
            enforce_type((1, 2, 3), list[int])

        # _repr_type module prefix cases
        from gceutils.base import NotSetType
        assert decorators._repr_type(NotSetType) == "<not set>"
        util_cls = type("U", (), {"__module__": "pmp_manip.utility.mod"})
        assert decorators._repr_type(util_cls) == "pmp_manip.utility.U"
        submod_cls = type("S", (), {"__module__": "pmp_manip.core"})
        assert decorators._repr_type(submod_cls) == "pmp_manip.S"

        other_cls = type("O", (), {"__module__": "tests.custom"})
        assert decorators._repr_type(other_cls) == "tests.custom.O"


class TestEnforceArgumentTypes:
    """Test enforce_argument_types decorator."""
    
    def test_enforce_argument_types_basic(self):
        """Test basic argument type enforcement."""
        @enforce_argument_types
        def add(a: int, b: int) -> int:
            return a + b
        
        assert add(1, 2) == 3
        with pytest.raises(GU_TypeValidationError):
            add("1", 2)
    
    def test_enforce_argument_types_str(self):
        """Test string argument enforcement."""
        @enforce_argument_types
        def greet(name: str) -> str:
            return f"Hello, {name}"
        
        assert greet("Alice") == "Hello, Alice"
        with pytest.raises(GU_TypeValidationError):
            greet(42)
    
    def test_enforce_argument_types_multiple_args(self):
        """Test enforcement with multiple arguments."""
        @enforce_argument_types
        def process(text: str, count: int, enabled: bool) -> str:
            return text * count if enabled else ""
        
        assert process("a", 3, True) == "aaa"
        assert process("b", 2, False) == ""
        
        with pytest.raises(GU_TypeValidationError):
            process(123, 3, True)
    
    def test_enforce_argument_types_list(self):
        """Test list argument enforcement."""
        @enforce_argument_types
        def sum_list(items: list[int]) -> int:
            return sum(items)
        
        assert sum_list([1, 2, 3]) == 6
        with pytest.raises(GU_TypeValidationError):
            sum_list([1, "2", 3])
    
    def test_enforce_argument_types_optional(self):
        """Test optional argument enforcement."""
        @enforce_argument_types
        def maybe_print(text: str | None) -> None:
            if text is not None:
                print(text)
        
        maybe_print("hello")
        maybe_print(None)
        
        with pytest.raises(GU_TypeValidationError):
            maybe_print(42)
    
    def test_enforce_argument_types_default_args(self):
        """Test enforcement with default arguments."""
        @enforce_argument_types
        def create_list(size: int = 5) -> list:
            return list(range(size))
        
        assert len(create_list()) == 5
        assert len(create_list(3)) == 3
        
        with pytest.raises(GU_TypeValidationError):
            create_list("5")
    
    def test_enforce_argument_types_no_annotations(self):
        """Test that functions without annotations work fine."""
        @enforce_argument_types
        def add(a, b):
            return a + b
        
        assert add(1, 2) == 3
        assert add("a", "b") == "ab"
    
    def test_enforce_argument_types_any(self):
        """Test Any type in function arguments."""
        @enforce_argument_types
        def accept_anything(value: Any) -> Any:
            return value
        
        assert accept_anything(42) == 42
        assert accept_anything("hello") == "hello"
        assert accept_anything(None) is None

    def test_enforce_argument_types_typevar_skips(self, monkeypatch):
        """TypeVar annotations are ignored by enforcement (skip branch)."""
        calls: list[tuple] = []
        monkeypatch.setattr(decorators, "enforce_type", lambda *args, **kwargs: calls.append(args))

        @enforce_argument_types
        def echo(value: T_GLOBAL) -> T_GLOBAL:
            return value

        assert echo(1) == 1
        assert echo("s") == "s"  # no GU_TypeValidationError despite annotation

        @enforce_argument_types
        def takes_typevar(value: TYPE_T):
            return value

        assert takes_typevar(123) == 123  # TYPE_T is a TypeVar; branch should skip
        assert calls == []  # enforce_type never called when TypeVar annotations are encountered

    def test_enforce_argument_types_typing_typevar_marker(self):
        """Object mimicking typing.TypeVar bypasses enforcement via first skip check."""
        @enforce_argument_types
        def take_fake(value: FAKE_TYPEVAR):
            return value

        assert take_fake("ok") == "ok"

    def test_enforce_argument_types_methods_and_classmethods(self):
        """Cover skip_first logic plus classmethod/staticmethod handling."""

        class Greeter:
            @enforce_argument_types
            def inst(self, value: int) -> int:
                return value

            @classmethod
            @enforce_argument_types
            def cls_method(cls, value: str) -> str:
                return value

            @staticmethod
            @enforce_argument_types
            def static_method(value: bool) -> bool:
                return value

        g = Greeter()
        assert g.inst(3) == 3
        with pytest.raises(GU_TypeValidationError):
            g.inst("x")

        assert Greeter.cls_method("hi") == "hi"
        with pytest.raises(GU_TypeValidationError):
            Greeter.cls_method(123)

        assert Greeter.static_method(True) is True
        with pytest.raises(GU_TypeValidationError):
            Greeter.static_method("nope")
