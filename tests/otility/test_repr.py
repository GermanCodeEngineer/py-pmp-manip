from __future__ import annotations
import pytest

from pmp_manip.otility.repr import grepr


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
    
    def test_grepr_dict(self):
        """Test grepr with dictionary."""
        result = grepr({"a": 1, "b": 2})
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_grepr_dataclass(self):
        """Test grepr with dataclass."""
        from pmp_manip.otility.base import grepr_dataclass
        
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
        from pmp_manip.otility.base import grepr_dataclass
        
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
        from pmp_manip.otility.base import grepr_dataclass
        
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
        from pmp_manip.otility.base import grepr_dataclass
        
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
