from __future__ import annotations
from collections.abc import Callable as ABCCallable, Iterable, Mapping, Sequence
from typing import Any, Literal
import pytest

from pmp_manip.utility.decorators import _check_type, enforce_argument_types


class TestCheckType:
    """Test the _check_type function for various type scenarios."""
    
    # --- Basic Types ---
    
    def test_basic_int(self):
        """Test basic int type checking."""
        _check_type(42, int, "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type("42", int, "value")
    
    def test_basic_str(self):
        """Test basic str type checking."""
        _check_type("hello", str, "value")
        with pytest.raises(TypeError, match="expected str"):
            _check_type(42, str, "value")
    
    def test_basic_bool(self):
        """Test basic bool type checking."""
        _check_type(True, bool, "value")
        with pytest.raises(TypeError, match="expected bool"):
            _check_type(1, bool, "value")
    
    def test_basic_float(self):
        """Test basic float type checking."""
        _check_type(3.14, float, "value")
        with pytest.raises(TypeError, match="expected float"):
            _check_type(3, float, "value")
    
    # --- Any Type ---
    
    def test_any_accepts_anything(self):
        """Test that Any type accepts any value."""
        _check_type(42, Any, "value")
        _check_type("hello", Any, "value")
        _check_type([1, 2, 3], Any, "value")
        _check_type(None, Any, "value")
    
    # --- Union Types ---
    
    def test_union_int_or_str(self):
        """Test Union[int, str] type checking."""
        _check_type(42, int | str, "value")
        _check_type("hello", int | str, "value")
        with pytest.raises(TypeError, match="does not match"):
            _check_type(3.14, int | str, "value")
    
    def test_optional(self):
        """Test Optional (Union with None) type checking."""
        _check_type("hello", str | None, "value")
        _check_type(None, str | None, "value")
        with pytest.raises(TypeError, match="does not match"):
            _check_type(42, str | None, "value")
    
    # --- List Types ---
    
    def test_list_basic(self):
        """Test basic list type checking."""
        _check_type([1, 2, 3], list, "value")
        with pytest.raises(TypeError, match="expected list"):
            _check_type((1, 2, 3), list, "value")
    
    def test_list_of_int(self):
        """Test list[int] type checking."""
        _check_type([1, 2, 3], list[int], "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type([1, "2", 3], list[int], "value")
    
    def test_list_of_str(self):
        """Test list[str] type checking."""
        _check_type(["a", "b", "c"], list[str], "value")
        with pytest.raises(TypeError, match="expected str"):
            _check_type(["a", 2, "c"], list[str], "value")
    
    def test_nested_list(self):
        """Test nested list type checking."""
        _check_type([[1, 2], [3, 4]], list[list[int]], "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type([[1, 2], [3, "4"]], list[list[int]], "value")
    
    def test_empty_list(self):
        """Test empty list type checking."""
        _check_type([], list[int], "value")
    
    # --- Tuple Types ---
    
    def test_tuple_basic(self):
        """Test basic tuple type checking."""
        _check_type((1, 2, 3), tuple, "value")
        with pytest.raises(TypeError, match="expected tuple"):
            _check_type([1, 2, 3], tuple, "value")
    
    def test_tuple_homogeneous(self):
        """Test tuple[int, ...] (homogeneous variable-length) type checking."""
        _check_type((1, 2, 3), tuple[int, ...], "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type((1, "2", 3), tuple[int, ...], "value")
    
    def test_tuple_fixed(self):
        """Test tuple[int, str, float] (fixed-length) type checking."""
        _check_type((1, "hello", 3.14), tuple[int, str, float], "value")
        with pytest.raises(TypeError, match="expected tuple of length 3"):
            _check_type((1, "hello"), tuple[int, str, float], "value")
        with pytest.raises(TypeError, match="expected str"):
            _check_type((1, 2, 3.14), tuple[int, str, float], "value")
    
    # --- Set Types ---
    
    def test_set_of_int(self):
        """Test set[int] type checking."""
        _check_type({1, 2, 3}, set[int], "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type({1, "2", 3}, set[int], "value")
    
    def test_frozenset_of_str(self):
        """Test frozenset[str] type checking."""
        _check_type(frozenset(["a", "b"]), frozenset[str], "value")
        with pytest.raises(TypeError, match="expected str"):
            _check_type(frozenset(["a", 2]), frozenset[str], "value")
    
    # --- Dict Types ---
    
    def test_dict_basic(self):
        """Test basic dict type checking."""
        _check_type({"a": 1}, dict, "value")
        with pytest.raises(TypeError, match="expected dict"):
            _check_type([("a", 1)], dict, "value")
    
    def test_dict_str_int(self):
        """Test dict[str, int] type checking."""
        _check_type({"a": 1, "b": 2}, dict[str, int], "value")
        with pytest.raises(TypeError, match="expected str"):
            _check_type({1: 1, "b": 2}, dict[str, int], "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type({"a": "1", "b": 2}, dict[str, int], "value")
    
    def test_nested_dict(self):
        """Test nested dict type checking."""
        _check_type({"a": {"x": 1}}, dict[str, dict[str, int]], "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type({"a": {"x": "1"}}, dict[str, dict[str, int]], "value")
    
    # --- Callable Types ---
    
    def test_callable_function(self):
        """Test Callable type checking with functions."""
        def my_func():
            pass
        _check_type(my_func, ABCCallable, "value")
        with pytest.raises(TypeError, match="expected Callable"):
            _check_type("not callable", ABCCallable, "value")
    
    def test_callable_lambda(self):
        """Test Callable type checking with lambdas."""
        _check_type(lambda x: x, ABCCallable, "value")
    
    def test_callable_class(self):
        """Test Callable type checking with classes."""
        class MyClass:
            pass
        _check_type(MyClass, ABCCallable, "value")
    
    def test_callable_instance_with_call(self):
        """Test Callable type checking with callable instances."""
        class CallableClass:
            def __call__(self):
                pass
        _check_type(CallableClass(), ABCCallable, "value")
    
    # --- Iterable Types ---
    
    def test_iterable_list(self):
        """Test Iterable[int] with list."""
        _check_type([1, 2, 3], Iterable[int], "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type([1, "2", 3], Iterable[int], "value")
    
    def test_iterable_string_skipped(self):
        """Test that Iterable[str] doesn't validate each character in a string."""
        # Strings are iterable but should be skipped to avoid char-by-char validation
        _check_type("hello", Iterable[str], "value")
        _check_type("hello", Iterable[int], "value")  # Should pass, not checking chars
    
    def test_iterable_generator(self):
        """Test Iterable with generator."""
        def gen():
            yield 1
            yield 2
        # Note: This will consume the generator
        _check_type(gen(), Iterable[int], "value")
    
    # --- Mapping Types ---
    
    def test_mapping_dict(self):
        """Test Mapping[str, int] with dict."""
        _check_type({"a": 1, "b": 2}, Mapping[str, int], "value")
        with pytest.raises(TypeError, match="expected str"):
            _check_type({1: 1}, Mapping[str, int], "value")
    
    # --- Sequence Types ---
    
    def test_sequence_list(self):
        """Test Sequence[int] with list."""
        _check_type([1, 2, 3], Sequence[int], "value")
        with pytest.raises(TypeError, match="expected int"):
            _check_type([1, "2", 3], Sequence[int], "value")
    
    def test_sequence_tuple(self):
        """Test Sequence[str] with tuple."""
        _check_type(("a", "b"), Sequence[str], "value")
    
    def test_sequence_string(self):
        """Test Sequence[str] with string."""
        _check_type("hello", Sequence[str], "value")
    
    # --- Literal Types ---
    
    def test_literal_match(self):
        """Test Literal type checking with matching value."""
        _check_type("red", Literal["red", "green", "blue"], "value")
        _check_type(1, Literal[1, 2, 3], "value")
    
    def test_literal_no_match(self):
        """Test Literal type checking with non-matching value."""
        with pytest.raises(TypeError, match="not in Literal"):
            _check_type("yellow", Literal["red", "green", "blue"], "value")
        with pytest.raises(TypeError, match="not in Literal"):
            _check_type(4, Literal[1, 2, 3], "value")
    
    # --- type[T] ---
    
    def test_type_basic(self):
        """Test type[T] checking."""
        _check_type(int, type[int], "value")
        _check_type(str, type[str], "value")
        with pytest.raises(TypeError, match="expected a class"):
            _check_type(42, type[int], "value")
    
    def test_type_subclass(self):
        """Test type[T] with subclass checking."""
        class Base:
            pass
        class Derived(Base):
            pass
        _check_type(Derived, type[Base], "value")
        _check_type(Base, type[Base], "value")
        with pytest.raises(TypeError, match="not a subclass"):
            _check_type(int, type[Base], "value")
    
    # --- Complex Nested Types ---
    
    def test_complex_nested(self):
        """Test complex nested type structures."""
        value = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25},
            ],
            "count": 2
        }
        expected = dict[str, list[dict[str, str | int]] | int]
        _check_type(value, expected, "value")
    
    def test_list_of_unions(self):
        """Test list of union types."""
        _check_type([1, "hello", 2, "world"], list[int | str], "value")
        with pytest.raises(TypeError, match="does not match"):
            _check_type([1, "hello", 3.14], list[int | str], "value")
    
    # --- Error Messages ---
    
    def test_error_path_tracking(self):
        """Test that error messages include path information."""
        with pytest.raises(TypeError, match=r"value\[1\]"):
            _check_type([1, "2", 3], list[int], "value")
        with pytest.raises(TypeError, match=r"value\[key\]"):
            _check_type({1: "a"}, dict[str, str], "value")
        with pytest.raises(TypeError, match=r"value\[value\]"):
            _check_type({"a": 1}, dict[str, str], "value")


class TestEnforceArgumentTypes:
    """Test the enforce_argument_types decorator."""
    
    def test_simple_function(self):
        """Test decorator on simple function."""
        @enforce_argument_types
        def add(a: int, b: int) -> int:
            return a + b
        
        assert add(1, 2) == 3
        with pytest.raises(TypeError):
            add("1", 2)
        with pytest.raises(TypeError):
            add(1, "2")
    
    def test_with_default_args(self):
        """Test decorator with default arguments."""
        @enforce_argument_types
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"
        
        assert greet("Alice") == "Hello, Alice!"
        assert greet("Bob", "Hi") == "Hi, Bob!"
        with pytest.raises(TypeError):
            greet(123)
    
    def test_with_optional(self):
        """Test decorator with Optional types."""
        @enforce_argument_types
        def process(value: str | None) -> str:
            return value or "default"
        
        assert process("test") == "test"
        assert process(None) == "default"
        with pytest.raises(TypeError):
            process(123)
    
    def test_with_list_type(self):
        """Test decorator with list types."""
        @enforce_argument_types
        def sum_list(numbers: list[int]) -> int:
            return sum(numbers)
        
        assert sum_list([1, 2, 3]) == 6
        with pytest.raises(TypeError):
            sum_list([1, "2", 3])
    
    def test_instance_method(self):
        """Test decorator on instance method."""
        class Calculator:
            @enforce_argument_types
            def add(self, a: int, b: int) -> int:
                return a + b
        
        calc = Calculator()
        assert calc.add(1, 2) == 3
        with pytest.raises(TypeError):
            calc.add("1", 2)
    
    def test_class_method(self):
        """Test decorator on class method."""
        class Factory:
            value = 10
            
            @classmethod
            @enforce_argument_types
            def create(cls, name: str) -> str:
                return f"{name}_{cls.value}"
        
        assert Factory.create("test") == "test_10"
        with pytest.raises(TypeError):
            Factory.create(123)
    
    def test_static_method(self):
        """Test decorator on static method."""
        class Utils:
            @staticmethod
            @enforce_argument_types
            def multiply(a: int, b: int) -> int:
                return a * b
        
        assert Utils.multiply(3, 4) == 12
        with pytest.raises(TypeError):
            Utils.multiply("3", 4)
    
    def test_with_any(self):
        """Test decorator with Any type."""
        @enforce_argument_types
        def accept_anything(value: Any) -> Any:
            return value
        
        assert accept_anything(1) == 1
        assert accept_anything("hello") == "hello"
        assert accept_anything([1, 2, 3]) == [1, 2, 3]
    
    def test_with_callable(self):
        """Test decorator with Callable type."""
        @enforce_argument_types
        def apply(func: ABCCallable, value: int) -> Any:
            return func(value)
        
        assert apply(lambda x: x * 2, 5) == 10
        with pytest.raises(TypeError):
            apply("not a function", 5)
    
    def test_kwargs(self):
        """Test decorator with keyword arguments."""
        @enforce_argument_types
        def create_user(name: str, age: int, active: bool = True) -> dict:
            return {"name": name, "age": age, "active": active}
        
        assert create_user(name="Alice", age=30) == {"name": "Alice", "age": 30, "active": True}
        assert create_user("Bob", 25, False) == {"name": "Bob", "age": 25, "active": False}
        with pytest.raises(TypeError):
            create_user(name=123, age=30)
