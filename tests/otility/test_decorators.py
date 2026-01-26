from __future__ import annotations
import pytest
from typing import Any

from pmp_manip.otility.decorators import enforce_type, enforce_argument_types
from pmp_manip.otility.errors import MANIPO_TypeValidationError


class TestEnforceType:
    """Test enforce_type function."""
    
    # --- Basic Types ---
    
    def test_enforce_type_int(self):
        """Test int type enforcement."""
        enforce_type(42, int)
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type("42", int)
    
    def test_enforce_type_str(self):
        """Test str type enforcement."""
        enforce_type("hello", str)
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type(42, str)
    
    def test_enforce_type_bool(self):
        """Test bool type enforcement."""
        enforce_type(True, bool)
        # Note: bool is a subclass of int, so we test with non-bool values
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type("True", bool)
    
    def test_enforce_type_float(self):
        """Test float type enforcement."""
        enforce_type(3.14, float)
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type(3, float)
    
    def test_enforce_type_none(self):
        """Test None type enforcement."""
        enforce_type(None, type(None))
        with pytest.raises(MANIPO_TypeValidationError):
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
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type(3.14, int | str)
    
    def test_enforce_type_optional(self):
        """Test optional type enforcement."""
        enforce_type("hello", str | None)
        enforce_type(None, str | None)
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type(42, str | None)
    
    # --- List Types ---
    
    def test_enforce_type_list_basic(self):
        """Test basic list type enforcement."""
        enforce_type([1, 2, 3], list)
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type((1, 2, 3), list)
    
    def test_enforce_type_list_of_int(self):
        """Test list[int] enforcement."""
        enforce_type([1, 2, 3], list[int])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type([1, "2", 3], list[int])
    
    def test_enforce_type_list_of_str(self):
        """Test list[str] enforcement."""
        enforce_type(["a", "b", "c"], list[str])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type(["a", 2, "c"], list[str])
    
    def test_enforce_type_nested_list(self):
        """Test nested list enforcement."""
        enforce_type([[1, 2], [3, 4]], list[list[int]])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type([[1, 2], [3, "4"]], list[list[int]])
    
    def test_enforce_type_empty_list(self):
        """Test empty list enforcement."""
        enforce_type([], list[int])
        enforce_type([], list[str])
    
    # --- Tuple Types ---
    
    def test_enforce_type_tuple_basic(self):
        """Test basic tuple type enforcement."""
        enforce_type((1, 2, 3), tuple)
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type([1, 2, 3], tuple)
    
    def test_enforce_type_tuple_homogeneous(self):
        """Test tuple[int, ...] enforcement."""
        enforce_type((1, 2, 3), tuple[int, ...])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type((1, "2", 3), tuple[int, ...])
    
    def test_enforce_type_tuple_fixed(self):
        """Test fixed-length tuple enforcement."""
        enforce_type((1, "hello", 3.14), tuple[int, str, float])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type((1, "hello"), tuple[int, str, float])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type((1, 2, 3.14), tuple[int, str, float])
    
    # --- Set Types ---
    
    def test_enforce_type_set_basic(self):
        """Test basic set type enforcement."""
        enforce_type({1, 2, 3}, set)
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type([1, 2, 3], set)
    
    def test_enforce_type_set_of_int(self):
        """Test set[int] enforcement."""
        enforce_type({1, 2, 3}, set[int])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type({1, "2", 3}, set[int])
    
    def test_enforce_type_frozenset_of_str(self):
        """Test frozenset[str] enforcement."""
        enforce_type(frozenset(["a", "b"]), frozenset[str])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type(frozenset(["a", 2]), frozenset[str])
    
    # --- Dict Types ---
    
    def test_enforce_type_dict_basic(self):
        """Test basic dict type enforcement."""
        enforce_type({"a": 1}, dict)
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type([("a", 1)], dict)
    
    def test_enforce_type_dict_str_int(self):
        """Test dict[str, int] enforcement."""
        enforce_type({"a": 1, "b": 2}, dict[str, int])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type({1: 1, "b": 2}, dict[str, int])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type({"a": "1", "b": 2}, dict[str, int])
    
    def test_enforce_type_nested_dict(self):
        """Test nested dict enforcement."""
        enforce_type({"a": {"x": 1}}, dict[str, dict[str, int]])
        with pytest.raises(MANIPO_TypeValidationError):
            enforce_type({"a": {"x": "1"}}, dict[str, dict[str, int]])
    
    def test_enforce_type_empty_dict(self):
        """Test empty dict enforcement."""
        enforce_type({}, dict[str, int])


class TestEnforceArgumentTypes:
    """Test enforce_argument_types decorator."""
    
    def test_enforce_argument_types_basic(self):
        """Test basic argument type enforcement."""
        @enforce_argument_types
        def add(a: int, b: int) -> int:
            return a + b
        
        assert add(1, 2) == 3
        with pytest.raises(MANIPO_TypeValidationError):
            add("1", 2)
    
    def test_enforce_argument_types_str(self):
        """Test string argument enforcement."""
        @enforce_argument_types
        def greet(name: str) -> str:
            return f"Hello, {name}"
        
        assert greet("Alice") == "Hello, Alice"
        with pytest.raises(MANIPO_TypeValidationError):
            greet(42)
    
    def test_enforce_argument_types_multiple_args(self):
        """Test enforcement with multiple arguments."""
        @enforce_argument_types
        def process(text: str, count: int, enabled: bool) -> str:
            return text * count if enabled else ""
        
        assert process("a", 3, True) == "aaa"
        assert process("b", 2, False) == ""
        
        with pytest.raises(MANIPO_TypeValidationError):
            process(123, 3, True)
    
    def test_enforce_argument_types_list(self):
        """Test list argument enforcement."""
        @enforce_argument_types
        def sum_list(items: list[int]) -> int:
            return sum(items)
        
        assert sum_list([1, 2, 3]) == 6
        with pytest.raises(MANIPO_TypeValidationError):
            sum_list([1, "2", 3])
    
    def test_enforce_argument_types_optional(self):
        """Test optional argument enforcement."""
        @enforce_argument_types
        def maybe_print(text: str | None) -> None:
            if text is not None:
                print(text)
        
        maybe_print("hello")
        maybe_print(None)
        
        with pytest.raises(MANIPO_TypeValidationError):
            maybe_print(42)
    
    def test_enforce_argument_types_default_args(self):
        """Test enforcement with default arguments."""
        @enforce_argument_types
        def create_list(size: int = 5) -> list:
            return list(range(size))
        
        assert len(create_list()) == 5
        assert len(create_list(3)) == 3
        
        with pytest.raises(MANIPO_TypeValidationError):
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
