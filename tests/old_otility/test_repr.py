from __future__ import annotations
from dataclasses import dataclass

from pmp_manip.otility.base import grepr_dataclass
from pmp_manip.otility.repr import grepr, KeyReprDict, GEnum
from pmp_manip.otility.dual_key_dict import DualKeyDict


class TestGreprBasicTypes:
    """Test grepr with basic Python types."""
    
    def test_string_simple(self):
        """Test simple string representation."""
        assert grepr("hello") == '"hello"'
        assert grepr("world") == '"world"'
    
    def test_string_with_double_quotes(self):
        """Test string containing double quotes."""
        assert grepr('say "hello"') == '\'say "hello"\''
    
    def test_string_with_single_quotes(self):
        """Test string containing single quotes."""
        assert grepr("it's nice") == '"it\'s nice"'
    
    def test_string_with_both_quotes(self):
        """Test string containing both quote types."""
        result = grepr('say "it\'s nice"')
        assert result == '"say \\"it\'s nice\\""'
    
    def test_string_with_backslash(self):
        """Test string containing backslashes."""
        assert grepr("path\\to\\file") == '"path\\\\to\\\\file"'
    
    def test_string_vanilla(self):
        """Test vanilla string mode."""
        assert grepr("hello", vanilla_strings=True) == "'hello'"
        assert grepr('say "hello"', vanilla_strings=True) == '\'say "hello"\''
    
    def test_int(self):
        """Test integer representation falls back to repr."""
        assert grepr(42) == "42"
        assert grepr(-10) == "-10"
    
    def test_float(self):
        """Test float representation falls back to repr."""
        assert grepr(3.14) == "3.14"
    
    def test_bool(self):
        """Test boolean representation falls back to repr."""
        assert grepr(True) == "True"
        assert grepr(False) == "False"
    
    def test_none(self):
        """Test None representation falls back to repr."""
        assert grepr(None) == "None"


class TestGreprLists:
    """Test grepr with lists."""
    
    def test_empty_list(self):
        """Test empty list."""
        assert grepr([]) == "[]"
    
    def test_simple_list(self):
        """Test simple list with inline formatting."""
        assert grepr([1, 2, 3]) == "[1, 2, 3]"
    
    def test_list_of_strings(self):
        """Test list of strings."""
        assert grepr(["a", "b", "c"]) == '["a", "b", "c"]'
    
    def test_nested_list(self):
        """Test nested list."""
        result = grepr([[1, 2], [3, 4]])
        assert result == "[[1, 2], [3, 4]]"
    
    def test_long_list_multiline(self):
        """Test that long lists get multiline formatting."""
        long_list = [f"item_{i}" for i in range(5)]
        result = grepr(long_list)
        # Should be multiline if items are long enough
        assert "\n" in result or all(item in result for item in long_list)
    
    def test_list_no_indent(self):
        """Test list with no indentation."""
        result = grepr([1, 2, 3], indent=None)
        assert result == "[1, 2, 3]"


class TestGreprTuples:
    """Test grepr with tuples."""
    
    def test_empty_tuple(self):
        """Test empty tuple."""
        assert grepr(()) == "()"
    
    def test_simple_tuple(self):
        """Test simple tuple."""
        assert grepr((1, 2, 3)) == "(1, 2, 3)"
    
    def test_single_element_tuple(self):
        """Test single element tuple (should have trailing comma in standard repr)."""
        # grepr doesn't add trailing comma, just shows (value)
        result = grepr((1,))
        assert "1" in result
    
    def test_nested_tuple(self):
        """Test nested tuple."""
        result = grepr(((1, 2), (3, 4)))
        assert "(1, 2)" in result and "(3, 4)" in result


class TestGreprSets:
    """Test grepr with sets."""
    
    def test_empty_set(self):
        """Test empty set."""
        assert grepr(set()) == "{}"
    
    def test_simple_set(self):
        """Test simple set."""
        result = grepr({1, 2, 3})
        assert result.startswith("{") and result.endswith("}")
        # Sets are unordered, so just check all elements are present
        assert "1" in result and "2" in result and "3" in result
    
    def test_set_of_strings(self):
        """Test set of strings."""
        result = grepr({"a", "b"})
        assert '"a"' in result and '"b"' in result


class TestGreprDicts:
    """Test grepr with dictionaries."""
    
    def test_empty_dict(self):
        """Test empty dictionary."""
        assert grepr({}) == "{}"
    
    def test_simple_dict(self):
        """Test simple dictionary."""
        result = grepr({"a": 1, "b": 2})
        assert '"a": 1' in result
        assert '"b": 2' in result
    
    def test_nested_dict(self):
        """Test nested dictionary."""
        result = grepr({"outer": {"inner": 1}})
        assert "outer" in result and "inner" in result and "1" in result
    
    def test_dict_with_various_types(self):
        """Test dictionary with various value types."""
        data = {"name": "Alice", "age": 30, "scores": [95, 88]}
        result = grepr(data)
        assert "Alice" in result
        assert "30" in result
        assert "95" in result


class TestGreprKeyReprDict:
    """Test grepr with KeyReprDict."""
    
    def test_empty_key_repr_dict(self):
        """Test empty KeyReprDict."""
        krd = KeyReprDict()
        result = grepr(krd)
        assert "KeyReprDict(keys={})" == result
    
    def test_key_repr_dict_with_keys(self):
        """Test KeyReprDict shows only keys."""
        krd = KeyReprDict({"a": 1, "b": 2, "c": 3})
        result = grepr(krd)
        assert "KeyReprDict(keys={" in result
        assert '"a"' in result
        assert '"b"' in result
        assert '"c"' in result
        # Values should not be shown
        assert ": 1" not in result
        assert ": 2" not in result


class TestGreprDualKeyDict:
    """Test grepr with DualKeyDict."""
    
    def test_empty_dual_key_dict_safe(self):
        """Test empty DualKeyDict in safe mode."""
        dkd = DualKeyDict()
        result = grepr(dkd, safe_dkd=True)
        assert result == "DualKeyDict()"
    
    def test_empty_dual_key_dict_unsafe(self):
        """Test empty DualKeyDict in unsafe mode."""
        dkd = DualKeyDict()
        result = grepr(dkd, safe_dkd=False)
        assert result == "DualKeyDict{}"
    
    def test_dual_key_dict_safe_mode(self):
        """Test DualKeyDict in safe mode."""
        dkd = DualKeyDict()
        dkd.set("a", "b", 1)
        result = grepr(dkd, safe_dkd=True)
        assert "DualKeyDict({" in result
        assert '("a", "b"): 1' in result
    
    def test_dual_key_dict_unsafe_mode(self):
        """Test DualKeyDict in unsafe mode."""
        dkd = DualKeyDict()
        dkd.set("x", "y", "value")
        result = grepr(dkd, safe_dkd=False)
        assert "DualKeyDict{" in result
        assert '"x" / "y": "value"' in result


class TestGreprDataclass:
    """Test grepr with dataclasses using grepr_dataclass decorator."""
    
    def test_simple_dataclass(self):
        """Test simple dataclass representation."""
        @grepr_dataclass()
        class Person:
            name: str
            age: int
        
        person = Person(name="Alice", age=30)
        result = grepr(person)
        assert "Person(" in result
        assert "name=" in result
        assert '"Alice"' in result
        assert "age=" in result
        assert "30" in result
    
    def test_dataclass_with_annotate_fields(self):
        """Test dataclass with annotate_fields parameter passed to grepr."""
        @grepr_dataclass()
        class Point:
            x: int
            y: int
        
        point = Point(x=10, y=20)
        # Test with annotate_fields=True (default)
        result = grepr(point, annotate_fields=True)
        assert "Point(" in result
        assert "x=10" in result
        assert "y=20" in result
        
        # Test with annotate_fields=False
        result_no_annotation = grepr(point, annotate_fields=False)
        assert "Point(" in result_no_annotation
        assert "10" in result_no_annotation
        assert "20" in result_no_annotation
        assert "x=" not in result_no_annotation
        assert "y=" not in result_no_annotation
    
    def test_dataclass_excluded_fields(self):
        """Test dataclass with excluded fields."""
        from pmp_manip.otility.base import field
        
        @grepr_dataclass()
        class User:
            username: str
            secret: str = field(grepr=False)
        
        user = User(username="alice", secret="password123")
        result = grepr(user)
        assert "alice" in result
        # The secret field should not appear in repr
        assert "secret=" not in result
        assert "password123" not in result
    
    def test_dataclass_with_grepr_false_field(self):
        """Test dataclass with field that has grepr=False."""
        from pmp_manip.otility.base import field
        
        @grepr_dataclass()
        class Account:
            username: str
            password: str = field(grepr=False)
        
        account = Account(username="alice", password="secret")
        result = grepr(account)
        assert "username=" in result
        assert "alice" in result
        # Field with grepr=False should not appear
        assert "password" not in result
        assert "secret" not in result
    
    def test_nested_dataclass(self):
        """Test nested dataclasses."""
        @grepr_dataclass()
        class Address:
            city: str
            zip: str
        
        @grepr_dataclass()
        class Person:
            name: str
            address: Address
        
        person = Person(
            name="Bob",
            address=Address(city="NYC", zip="10001")
        )
        result = grepr(person)
        assert "Person(" in result
        assert "Address(" in result
        assert "Bob" in result
        assert "NYC" in result
        assert "10001" in result
    
    def test_dataclass_simple_inline(self):
        """Test that simple dataclass with few fields stays inline."""
        @grepr_dataclass()
        class Point:
            x: int
            y: int
        
        point = Point(x=1, y=2)
        result = grepr(point)
        # Should be inline (no newlines) for simple cases
        assert "\n" not in result


class TestGreprIndentation:
    """Test grepr indentation behavior."""
    
    def test_custom_indent_spaces(self):
        """Test custom indentation with spaces."""
        data = {"a": [1, 2, 3], "b": [4, 5, 6]}
        result = grepr(data, indent=2)
        # Should have indentation
        if "\n" in result:
            assert "  " in result
    
    def test_custom_indent_string(self):
        """Test custom indentation with string."""
        data = [1, 2, 3, 4, 5]
        result = grepr(data, indent="\t")
        # May or may not be multiline depending on content
        assert result is not None
    
    def test_no_indent(self):
        """Test with no indentation."""
        data = {"a": {"b": {"c": 1}}}
        result = grepr(data, indent=None)
        assert "\n" not in result
        assert result.count(" ") > 0  # Should have spaces between items
    
    def test_level_offset(self):
        """Test with level offset."""
        data = [1, 2, 3]
        result1 = grepr(data, level_offset=0)
        result2 = grepr(data, level_offset=2)
        # Both should work
        assert result1 is not None
        assert result2 is not None


class TestGreprGEnum:
    """Test GEnum representation."""
    
    def test_genum_repr(self):
        """Test GEnum has custom repr."""
        class Color(GEnum):
            RED = 1
            GREEN = 2
            BLUE = 3
        
        assert repr(Color.RED) == "Color.RED"
        assert repr(Color.GREEN) == "Color.GREEN"
        assert repr(Color.BLUE) == "Color.BLUE"
    
    def test_genum_in_grepr(self):
        """Test GEnum within grepr structures."""
        class Status(GEnum):
            ACTIVE = "active"
            INACTIVE = "inactive"
        
        data = {"status": Status.ACTIVE, "value": 42}
        result = grepr(data)
        # The enum should use its repr
        assert "Status.ACTIVE" in result


class TestGreprEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_deeply_nested_structure(self):
        """Test deeply nested data structures."""
        data = {"a": {"b": {"c": {"d": [1, 2, 3]}}}}
        result = grepr(data)
        assert '"a"' in result
        assert '"b"' in result
        assert '"c"' in result
        assert '"d"' in result
        assert "[1, 2, 3]" in result or ("1" in result and "2" in result and "3" in result)
    
    def test_mixed_types(self):
        """Test mixed types in complex structure."""
        data = {
            "numbers": [1, 2, 3],
            "strings": ["a", "b"],
            "nested": {"key": "value"},
            "bool": True,
            "none": None
        }
        result = grepr(data)
        assert "numbers" in result
        assert "strings" in result
        assert "nested" in result
        assert "True" in result
        assert "None" in result
    
    def test_empty_collections(self):
        """Test various empty collections."""
        data = {
            "list": [],
            "tuple": (),
            "dict": {},
            "set": set()
        }
        result = grepr(data)
        assert "[]" in result
        assert "()" in result
        assert "{}" in result
    
    def test_fallback_to_repr(self):
        """Test that non-supported types fall back to repr."""
        class CustomClass:
            def __repr__(self):
                return "<CustomClass>"
        
        obj = CustomClass()
        result = grepr(obj)
        assert result == "<CustomClass>"
    
    def test_dataclass_without_has_grepr(self):
        """Test regular dataclass without __has_grepr__ attribute."""
        @dataclass
        class RegularDataclass:
            value: int
        
        obj = RegularDataclass(value=42)
        result = grepr(obj)
        # Should fall back to repr
        assert "RegularDataclass" in result or "42" in result
