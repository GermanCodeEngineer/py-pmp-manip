from __future__ import annotations
import pytest

from pmp_manip.otility.dual_key_dict import DualKeyDict


class TestDualKeyDict:
    """Test DualKeyDict class."""
    
    def test_empty_creation(self):
        """Test creating an empty DualKeyDict."""
        dkd = DualKeyDict()
        assert len(dkd) == 0
    
    def test_set_and_get_by_key1(self):
        """Test setting and getting values by key1."""
        dkd = DualKeyDict()
        dkd.set("key1", "key2", "value")
        assert dkd.get_by_key1("key1") == "value"
    
    def test_set_and_get_by_key2(self):
        """Test setting and getting values by key2."""
        dkd = DualKeyDict()
        dkd.set("key1", "key2", "value")
        assert dkd.get_by_key2("key2") == "value"
    
    def test_set_multiple_values(self):
        """Test setting multiple values."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        dkd.set("c", "z", 3)
        
        assert len(dkd) == 3
        assert dkd.get_by_key1("a") == 1
        assert dkd.get_by_key2("y") == 2
        assert dkd.get_by_key1("c") == 3
    
    def test_overwrite_value(self):
        """Test overwriting an existing value."""
        dkd = DualKeyDict()
        dkd.set("key1", "key2", "old_value")
        dkd.set("key1", "key2", "new_value")
        
        assert dkd.get_by_key1("key1") == "new_value"
        assert dkd.get_by_key2("key2") == "new_value"
    
    def test_get_by_key1_nonexistent(self):
        """Test getting nonexistent value by key1."""
        dkd = DualKeyDict()
        with pytest.raises(KeyError):
            dkd.get_by_key1("nonexistent")
    
    def test_get_by_key2_nonexistent(self):
        """Test getting nonexistent value by key2."""
        dkd = DualKeyDict()
        with pytest.raises(KeyError):
            dkd.get_by_key2("nonexistent")
    
    def test_items_key1_key2(self):
        """Test iterating over items with both keys."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        dkd.set("c", "z", 3)
        
        items = list(dkd.items_key1_key2())
        assert len(items) == 3
        
        # Verify all items are tuples of (key1, key2, value)
        for key1, key2, value in items:
            assert isinstance(key1, str)
            assert isinstance(key2, str)
            assert isinstance(value, int)
    
    def test_iteration_order(self):
        """Test iteration maintains insertion order."""
        dkd = DualKeyDict()
        expected_items = [
            ("a", "x", 1),
            ("b", "y", 2),
            ("c", "z", 3),
        ]
        
        for key1, key2, value in expected_items:
            dkd.set(key1, key2, value)
        
        actual_items = list(dkd.items_key1_key2())
        assert actual_items == expected_items
    
    def test_has_key1(self):
        """Test checking if key1 exists."""
        dkd = DualKeyDict()
        dkd.set("key1", "key2", "value")
        
        assert dkd.has_key1("key1")
        assert not dkd.has_key1("nonexistent")
    
    def test_has_key2(self):
        """Test checking if key2 exists."""
        dkd = DualKeyDict()
        dkd.set("key1", "key2", "value")
        
        assert dkd.has_key2("key2")
        assert not dkd.has_key2("nonexistent")
    
    def test_delete_by_key1(self):
        """Test deleting by key1."""
        dkd = DualKeyDict()
        dkd.set("key1", "key2", "value")
        assert len(dkd) == 1
        
        dkd.delete_by_key1("key1")
        assert len(dkd) == 0
        
        with pytest.raises(KeyError):
            dkd.get_by_key1("key1")
    
    def test_delete_by_key2(self):
        """Test deleting by key2."""
        dkd = DualKeyDict()
        dkd.set("key1", "key2", "value")
        assert len(dkd) == 1
        
        dkd.delete_by_key2("key2")
        assert len(dkd) == 0
        
        with pytest.raises(KeyError):
            dkd.get_by_key2("key2")
    
    def test_clear(self):
        """Test clearing all entries."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        assert len(dkd) == 2
        
        dkd.clear()
        assert len(dkd) == 0
    
    def test_mixed_key_types(self):
        """Test with different key types."""
        dkd = DualKeyDict()
        dkd.set(1, "a", "value1")
        dkd.set("two", 2, "value2")
        dkd.set(3.0, "three", "value3")
        
        assert len(dkd) == 3
        assert dkd.get_by_key1(1) == "value1"
        assert dkd.get_by_key2(2) == "value2"


class TestDualKeyDictRepresentation:
    """Test DualKeyDict string representation."""
    
    def test_repr_empty(self):
        """Test repr of empty DualKeyDict."""
        dkd = DualKeyDict()
        repr_str = repr(dkd)
        assert "DualKeyDict" in repr_str
    
    def test_repr_with_items(self):
        """Test repr of DualKeyDict with items."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        repr_str = repr(dkd)
        assert "DualKeyDict" in repr_str
