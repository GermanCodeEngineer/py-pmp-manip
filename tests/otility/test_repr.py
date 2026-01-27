from __future__ import annotations
import pytest

from gceutils.repr import grepr
from gceutils.repr import KeyReprDict, GEnum
from gceutils.dual_key_dict import DualKeyDict
from gceutils.base import grepr_dataclass, field


class TestGrepr:
    """Test grepr function."""
    
    def test_grepr_basic_int(self):
        """Test grepr with basic int."""
        result = grepr(42)
        assert "42" in result
    
    def test_grepr_basic_str(self):
        """Test grepr with basic string."""
        result = grepr("hello")
        assert "hello" in result
    
    def test_grepr_basic_list(self):
        """Test grepr with basic list."""
        result = grepr([1, 2, 3])
        assert "1" in result
        assert "2" in result

    def test_grepr_list_multiline_branch(self):
        """Long items force multiline list formatting (allsimple False)."""
        long_items = ["a" * 50, "b" * 50]
        result = grepr(long_items, indent=2)
        assert "\n" in result  # multiline branch used
    
    def test_grepr_dict(self):
        """Test grepr with dictionary."""
        result = grepr({"a": 1, "b": 2})
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_grepr_dataclass(self):
        """Test grepr with dataclass."""
        from gceutils.base import grepr_dataclass
        
        @grepr_dataclass()
        class TestClass:
            name: str
            value: int
        
        obj = TestClass(name="test", value=42)
        result = grepr(obj)
        
        assert "TestClass" in result
        assert "name" in result
        assert "test" in result
    
    def test_grepr_nested_dataclass(self):
        """Test grepr with nested dataclass."""
        from gceutils.base import grepr_dataclass
        
        @grepr_dataclass()
        class Inner:
            value: int
        
        @grepr_dataclass()
        class Outer:
            inner: Inner
        
        obj = Outer(inner=Inner(value=42))
        result = grepr(obj)
        
        assert "Outer" in result
        assert "Inner" in result
        assert "42" in result
    
    def test_grepr_with_level_offset(self):
        """Test grepr with level offset."""
        result1 = grepr(42, level_offset=0)
        result2 = grepr(42, level_offset=2)
        
        # Both should contain the value
        assert "42" in result1
        assert "42" in result2
    
    def test_grepr_safe_dkd_flag(self):
        """Test grepr with safe_dkd flag."""
        result = grepr([1, 2, 3], safe_dkd=True)
        assert isinstance(result, str)
    
    def test_grepr_annotate_fields_flag(self):
        """Test grepr with annotate_fields flag."""
        from gceutils.base import grepr_dataclass
        
        @grepr_dataclass()
        class TestClass:
            value: int
        
        obj = TestClass(value=10)
        result_annotated = grepr(obj, annotate_fields=True)
        result_not_annotated = grepr(obj, annotate_fields=False)
        
        assert isinstance(result_annotated, str)
        assert isinstance(result_not_annotated, str)
    
    def test_grepr_vanilla_strings_flag(self):
        """Test grepr with vanilla_strings flag."""
        result = grepr("test", vanilla_strings=True)
        assert isinstance(result, str)
    
    def test_grepr_indent_option(self):
        """Test grepr with different indent options."""
        @grepr_dataclass()
        class TestClass:
            items: list[int]
        
        obj = TestClass(items=[1, 2, 3])
        
        # Test with different indents
        result_4 = grepr(obj, indent=4)
        result_2 = grepr(obj, indent=2)
        result_none = grepr(obj, indent=None)
        
        assert isinstance(result_4, str)
        assert isinstance(result_2, str)
        assert isinstance(result_none, str)

    def test_keyreprdict_and_empty_collections(self):
        """Ensure KeyReprDict repr and empty collection branches are exercised."""
        kd = KeyReprDict({"a": 1, "b": 2})
        out = repr(kd)
        assert out.startswith("KeyReprDict(keys={")
        assert "1" not in out and "2" not in out  # values hidden

        assert grepr([]) == "[]"
        assert grepr(()) == "()"
        assert grepr(set()) == "{}"
        assert grepr({}) == "{}"

    def test_dual_key_dict_empty_and_safe(self):
        """Cover DualKeyDict empty formatting for safe and non-safe modes."""
        empty = DualKeyDict()
        assert grepr(empty) == "DualKeyDict{}"
        assert grepr(empty, safe_dkd=True) == "DualKeyDict()"

    def test_dual_key_dict_with_values(self):
        """Cover DualKeyDict non-empty formatting for both safe_dkd modes."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)

        unsafe = grepr(dkd)
        assert '"a" / "x": 1' in unsafe and '"b" / "y": 2' in unsafe

        safe = grepr(dkd, safe_dkd=True)
        assert '("a", "x"): 1' in safe and '("b", "y"): 2' in safe

    def test_string_quoting_cases(self):
        """Cover vanilla string escaping/quoting logic with mixed quotes and backslashes."""
        mixed = 'path\\name "quote" and \'tick\''
        out_mixed = grepr(mixed)
        assert out_mixed.startswith("\"")
        assert '\\"' in out_mixed  # double quotes escaped
        assert "\\\\" in out_mixed  # backslash doubled

        double_only = 'hello "world"'
        out_double_only = grepr(double_only)
        assert out_double_only.startswith("'") and out_double_only.endswith("'")

        plain = "simple"
        out_plain = grepr(plain)
        assert out_plain == '"simple"'

    def test_dataclass_grepr_skips_non_grepr_fields(self):
        """When all fields are grepr=False, result should be ClassName()."""
        @grepr_dataclass()
        class Hidden:
            a: int = field(default=1, grepr=False)
            b: int = field(default=2, grepr=False)

        result = grepr(Hidden())
        assert result == "Hidden()"

    def test_dataclass_without_field_annotation_names(self):
        """annotate_fields=False should omit field names in output."""
        @grepr_dataclass()
        class Simple:
            a: int
            b: int

        res = grepr(Simple(1, 2), annotate_fields=False)
        assert res.startswith("Simple(")
        assert "a=" not in res and "b=" not in res

    def test_dataclass_missing_attribute_skips_field(self):
        """Missing attribute triggers hasattr skip path inside grepr."""
        @grepr_dataclass()
        class Missing:
            a: int
            b: int

        obj = Missing(1, 2)
        delattr(obj, "b")

        res = grepr(obj)
        assert "Missing(" in res and "a=" in res and "b=" not in res

    def test_genum_repr(self):
        """Cover GEnum.__repr__ output formatting."""
        class Color(GEnum):
            RED = 1
            BLUE = 2

        assert repr(Color.RED) == "Color.RED"

    def test_fallback_repr_for_unknown_obj(self):
        """Objects outside supported types fall back to built-in repr (indent unchanged)."""
        class Unknown:
            pass
        obj = Unknown()
        assert grepr(obj) == repr(obj)
