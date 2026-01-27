from __future__ import annotations
import pytest

from gceutils.dual_key_dict import DualKeyDict


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


class TestDualKeyDictFromMethods:
    """Test DualKeyDict factory methods."""
    
    def test_from_single_key_value(self):
        """Test creating DualKeyDict from single key-value pairs."""
        data = [("a", 1), ("b", 2), ("c", 3)]
        dkd = DualKeyDict.from_single_key_value(data)
        
        assert len(dkd) == 3
        assert dkd.get_by_key1("a") == 1
        assert dkd.get_by_key2("b") == 2
        assert dkd.has_key1("c")
        assert dkd.has_key2("c")
    
    def test_from_both_keys(self):
        """Test creating DualKeyDict from both keys with single value."""
        data = [("a", "x"), ("b", "y"), ("c", "z")]
        dkd = DualKeyDict.from_both_keys(data, "same_value")
        
        assert len(dkd) == 3
        assert dkd.get_by_key1("a") == "same_value"
        assert dkd.get_by_key2("y") == "same_value"
    
    def test_init_from_dict(self):
        """Test initializing DualKeyDict from dictionary."""
        data = {
            ("a", "x"): 1,
            ("b", "y"): 2,
            ("c", "z"): 3,
        }
        dkd = DualKeyDict(data)
        
        assert len(dkd) == 3
        assert dkd.get_by_key1("a") == 1
        assert dkd.get_by_key2("y") == 2


class TestDualKeyDictUpdate:
    """Test update and change methods."""
    
    def test_update_by_key1(self):
        """Test updating value by key1."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.update_by_key1("a", 10)
        
        assert dkd.get_by_key1("a") == 10
        assert dkd.get_by_key2("x") == 10
    
    def test_update_by_key1_nonexistent(self):
        """Test updating nonexistent key1 raises error."""
        dkd = DualKeyDict()
        
        with pytest.raises(KeyError):
            dkd.update_by_key1("nonexistent", 100)
    
    def test_update_by_key2(self):
        """Test updating value by key2."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.update_by_key2("x", 20)
        
        assert dkd.get_by_key1("a") == 20
        assert dkd.get_by_key2("x") == 20
    
    def test_update_by_key2_nonexistent(self):
        """Test updating nonexistent key2 raises error."""
        dkd = DualKeyDict()
        
        with pytest.raises(KeyError):
            dkd.update_by_key2("nonexistent", 100)
    
    def test_update_method_with_conflict(self):
        """Test update method raises on conflict."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        
        dkd2 = DualKeyDict()
        dkd2.set("a", "y", 2)  # Same key1, different key2
        
        with pytest.raises(ValueError):
            dkd1.update(dkd2)
    
    def test_change_key1_by_key2(self):
        """Test changing key1 while keeping key2."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        dkd.change_key1_by_key2("x", "new_a")
        
        assert dkd.get_by_key1("new_a") == 1
        assert dkd.get_by_key2("x") == 1
        assert not dkd.has_key1("a")
    
    def test_change_key2_by_key1(self):
        """Test changing key2 while keeping key1."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        dkd.change_key2_by_key1("a", "new_x")
        
        assert dkd.get_by_key1("a") == 1
        assert dkd.get_by_key2("new_x") == 1
        assert not dkd.has_key2("x")
    
    def test_change_key1_key2_by_key1(self):
        """Test changing both keys using key1."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        dkd.change_key1_key2_by_key1("a", "new_a", "new_x")
        
        assert dkd.get_by_key1("new_a") == 1
        assert dkd.get_by_key2("new_x") == 1
    
    def test_change_key1_key2_by_key2(self):
        """Test changing both keys using key2."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        dkd.change_key1_key2_by_key2("x", "new_a", "new_x")
        
        assert dkd.get_by_key1("new_a") == 1
        assert dkd.get_by_key2("new_x") == 1


class TestDualKeyDictCopy:
    """Test copy methods."""
    
    def test_copy(self):
        """Test shallow copy."""
        dkd = DualKeyDict()
        dkd.set("a", "x", [1, 2, 3])
        
        dkd_copy = dkd.copy()
        
        assert len(dkd_copy) == 1
        assert dkd_copy.get_by_key1("a") == [1, 2, 3]
        assert dkd_copy is not dkd
    
    def test_copy_dunder(self):
        """Test __copy__ method."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        dkd_copy = dkd.__copy__()
        
        assert dkd_copy.get_by_key1("a") == 1
        assert dkd_copy is not dkd
    
    def test_deepcopy(self):
        """Test deep copy."""
        dkd = DualKeyDict()
        dkd.set("a", "x", [1, 2, 3])
        
        dkd_deepcopy = dkd.deepcopy()
        
        assert dkd_deepcopy.get_by_key1("a") == [1, 2, 3]
        assert dkd_deepcopy is not dkd


class TestDualKeyDictPop:
    """Test pop methods."""
    
    def test_pop_by_key1(self):
        """Test popping by key1."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        value = dkd.pop_by_key1("a")
        
        assert value == 1
        assert len(dkd) == 1
        assert not dkd.has_key1("a")
        assert not dkd.has_key2("x")
    
    def test_pop_by_key1_nonexistent(self):
        """Test popping nonexistent key1."""
        dkd = DualKeyDict()
        
        with pytest.raises(KeyError):
            dkd.pop_by_key1("nonexistent")
    
    def test_pop_by_key2(self):
        """Test popping by key2."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        value = dkd.pop_by_key2("y")
        
        assert value == 2
        assert len(dkd) == 1
        assert not dkd.has_key1("b")
        assert not dkd.has_key2("y")
    
    def test_pop_by_key2_nonexistent(self):
        """Test popping nonexistent key2."""
        dkd = DualKeyDict()
        
        with pytest.raises(KeyError):
            dkd.pop_by_key2("nonexistent")
    
    def test_pop_by_key1_with_default(self):
        """Test pop with default."""
        dkd = DualKeyDict()
        
        result = dkd.pop_by_key1_with_default("nonexistent", "default_value")
        
        assert result == "default_value"
    
    def test_pop_by_key2_with_default(self):
        """Test pop by key2 with default."""
        dkd = DualKeyDict()
        
        result = dkd.pop_by_key2_with_default("nonexistent", "default_value")
        
        assert result == "default_value"


class TestDualKeyDictGetDefault:
    """Test get with default methods."""
    
    def test_get_by_key1_with_default_exists(self):
        """Test get with default when key exists."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        result = dkd.get_by_key1_with_default("a", "default")
        
        assert result == 1
    
    def test_get_by_key1_with_default_missing(self):
        """Test get with default when key missing."""
        dkd = DualKeyDict()
        
        result = dkd.get_by_key1_with_default("nonexistent", "default")
        
        assert result == "default"
    
    def test_get_by_key2_with_default_exists(self):
        """Test get by key2 with default when key exists."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        result = dkd.get_by_key2_with_default("x", "default")
        
        assert result == 1
    
    def test_get_by_key2_with_default_missing(self):
        """Test get by key2 with default when key missing."""
        dkd = DualKeyDict()
        
        result = dkd.get_by_key2_with_default("nonexistent", "default")
        
        assert result == "default"


class TestDualKeyDictKeys:
    """Test key iteration methods."""
    
    def test_keys_key1(self):
        """Test getting key1 keys."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        keys = list(dkd.keys_key1())
        assert "a" in keys
        assert "b" in keys
    
    def test_keys_key2(self):
        """Test getting key2 keys."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        keys = list(dkd.keys_key2())
        assert "x" in keys
        assert "y" in keys
    
    def test_keys_key1_key2(self):
        """Test getting both keys."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        pairs = list(dkd.keys_key1_key2())
        assert ("a", "x") in pairs
        assert ("b", "y") in pairs
    
    def test_keys_key2_key1(self):
        """Test getting both keys reversed."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        pairs = list(dkd.keys_key2_key1())
        assert ("x", "a") in pairs
        assert ("y", "b") in pairs


class TestDualKeyDictItems:
    """Test item iteration methods."""
    
    def test_items_key1(self):
        """Test items by key1."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        items = list(dkd.items_key1())
        assert ("a", 1) in items
        assert ("b", 2) in items
    
    def test_items_key2(self):
        """Test items by key2."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        items = list(dkd.items_key2())
        assert ("x", 1) in items
        assert ("y", 2) in items
    
    def test_items_key2_key1(self):
        """Test items by key2, key1."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        items = list(dkd.items_key2_key1())
        assert ("x", "a", 1) in items
        assert ("y", "b", 2) in items


class TestDualKeyDictValues:
    """Test value iteration."""
    
    def test_values(self):
        """Test getting all values."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        dkd.set("c", "z", 3)
        
        values = list(dkd.values())
        assert 1 in values
        assert 2 in values
        assert 3 in values


class TestDualKeyDictOperators:
    """Test operator overloading."""
    
    def test_bool_empty(self):
        """Test bool of empty DualKeyDict."""
        dkd = DualKeyDict()
        assert not dkd
    
    def test_bool_non_empty(self):
        """Test bool of non-empty DualKeyDict."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        assert dkd
    
    def test_or_operator_conflict(self):
        """Test | operator with conflicting keys."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        
        dkd2 = DualKeyDict()
        dkd2.set("a", "y", 2)  # Same key1, different key2
        
        with pytest.raises(ValueError):
            result = dkd1 | dkd2
    
    def test_ror_operator_conflict(self):
        """Test __ror__ operator with conflicting keys."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        
        dkd2 = DualKeyDict()
        dkd2.set("a", "y", 2)  # Same key1, different key2
        
        with pytest.raises(ValueError):
            result = dkd2.__ror__(dkd1)
    
    def test_ior_operator_conflict(self):
        """Test |= operator with conflicting keys."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        
        dkd2 = DualKeyDict()
        dkd2.set("a", "y", 2)  # Same key1, different key2
        
        with pytest.raises(ValueError):
            dkd1 |= dkd2
    
    def test_eq(self):
        """Test equality."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        
        dkd2 = DualKeyDict()
        dkd2.set("a", "x", 1)
        
        assert dkd1 == dkd2
    
    def test_eq_different(self):
        """Test inequality."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        
        dkd2 = DualKeyDict()
        dkd2.set("b", "y", 2)
        
        assert dkd1 != dkd2
    
    def test_eq_not_dualkey(self):
        """Test equality with non-DualKeyDict."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        result = dkd.__eq__({})
        assert result == NotImplemented


class TestDualKeyDictForbidden:
    """Test forbidden operations."""
    
    def test_getitem_raises(self):
        """Test that __getitem__ raises NotImplementedError."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        with pytest.raises(NotImplementedError):
            _ = dkd["a"]
    
    def test_setitem_raises(self):
        """Test that __setitem__ raises NotImplementedError."""
        dkd = DualKeyDict()
        
        with pytest.raises(NotImplementedError):
            dkd["a"] = 1
    
    def test_delitem_raises(self):
        """Test that __delitem__ raises NotImplementedError."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        with pytest.raises(NotImplementedError):
            del dkd["a"]
    
    def test_iter_raises(self):
        """Test that __iter__ raises NotImplementedError."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        with pytest.raises(NotImplementedError):
            for _ in dkd:
                pass
    
    def test_reversed_raises(self):
        """Test that __reversed__ raises NotImplementedError."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        with pytest.raises(NotImplementedError):
            for _ in reversed(dkd):
                pass
    
    def test_contains_raises(self):
        """Test that __contains__ raises NotImplementedError."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        with pytest.raises(NotImplementedError):
            "a" in dkd


class TestDualKeyDictErrors:
    """Test error conditions."""
    
    def test_set_duplicate_same_keys(self):
        """Test overwriting when both keys match (should succeed)."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        # This should succeed (overwrite)
        dkd.set("a", "x", 100)
        
        assert dkd.get_by_key1("a") == 100
        assert dkd.get_by_key2("x") == 100
        assert len(dkd) == 1
    
    def test_set_conflicting_key2(self):
        """Test setting with conflicting key2."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        with pytest.raises(ValueError):
            dkd.set("b", "x", 2)  # key2 "x" exists with key1 "a", not "b"
    
    def test_change_key1_to_existing(self):
        """Test changing key1 to one that already exists."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        with pytest.raises(ValueError):
            dkd.change_key1_by_key2("x", "b")
    
    def test_change_key2_to_existing(self):
        """Test changing key2 to one that already exists."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        with pytest.raises(ValueError):
            dkd.change_key2_by_key1("a", "y")

    def test_set_key2_exists_different_key1(self):
        """Test set when key2 exists with different key1 (line 70-72)."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        # Trying to set with key2 "x" but different key1 "b"
        with pytest.raises(ValueError, match=r"key2 'x' already exists with different key1 'a'"):
            dkd.set("b", "x", 2)
    
    def test_set_key1_exists_different_key2(self):
        """Test set when key1 exists with different key2 (line 68-69)."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        # Trying to set with key1 "a" but different key2 "y"
        with pytest.raises(ValueError, match=r"key1 'a' already exists with different key2 'x'"):
            dkd.set("a", "y", 2)

    def test_set_key1_conflict_when_key2_used_elsewhere(self):
        """Test set third-branch conflict: key1 exists, key2 belongs to someone else (lines 73-75)."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)

        # key1 "a" already maps to "x"; introducing pair ("a", "y") should hit third branch
        with pytest.raises(ValueError, match=r"key1 'a' exists with different key2 'x'"):
            dkd.set("a", "y", 99)
    
    def test_set_overwrites_when_keys_match(self):
        """Test that set() properly overwrites when both keys match (lines 74-75)."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        # Overwrite with same keys, different value - this exercises lines 74-75
        dkd.set("a", "x", 100)
        
        assert dkd.get_by_key1("a") == 100
        assert dkd.get_by_key2("x") == 100
        assert len(dkd) == 1
    
    def test_get_key2_for_key1_nonexistent(self):
        """Test get_key2_for_key1 with nonexistent key (lines 250-251)."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        # Try to get key2 for nonexistent key1
        with pytest.raises(KeyError):
            dkd.get_key2_for_key1("nonexistent")
    
    def test_get_key1_for_key2_nonexistent(self):
        """Test get_key1_for_key2 with nonexistent key (symmetric to above)."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        # Try to get key1 for nonexistent key2
        with pytest.raises(KeyError):
            dkd.get_key1_for_key2("nonexistent")
    
    def test_ior_with_matching_keys(self):
        """Test __ior__ when both keys exist but match (lines 327-328)."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        dkd1.set("b", "y", 2)
        
        dkd2 = DualKeyDict()
        dkd2.set("a", "x", 100)  # Same key pair, different value
        
        # This should succeed - updating value (line 327-328 check passes, line 329 executes)
        dkd1.__ior__(dkd2)
        assert dkd1.get_by_key1("a") == 100
        assert len(dkd1) == 2

    def test_ior_key1_and_key2_both_present_mismatch(self):
        """Test __ior__ third branch: key1 exists, key2 mapped to different key1 (lines 327-328)."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        dkd1.set("b", "y", 2)

        dkd2 = DualKeyDict()
        dkd2.set("a", "y", 5)  # key1 matches existing, key2 belongs to b

        with pytest.raises(ValueError, match=r"key1 'a' exists in DualKeyDict with different key2 'x'"):
            dkd1.__ior__(dkd2)
    
    def test_change_nonexistent_key1(self):
        """Test changing nonexistent key1."""
        dkd = DualKeyDict()
        
        with pytest.raises(KeyError):
            dkd.change_key1_by_key2("nonexistent", "new_a")
    
    def test_change_nonexistent_key2(self):
        """Test changing nonexistent key2."""
        dkd = DualKeyDict()
        
        with pytest.raises(KeyError):
            dkd.change_key2_by_key1("nonexistent", "new_x")
    
    def test_ior_with_key1_key2_mismatch(self):
        """Test __ior__ when both keys exist but with conflicting values."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        dkd1.set("b", "y", 2)
        
        dkd2 = DualKeyDict()
        dkd2.set("a", "z", 3)  # key1 "a" exists with key2 "x", not "z"
        
        with pytest.raises(ValueError):
            dkd1 |= dkd2
    
    def test_ior_with_key2_conflict(self):
        """Test __ior__ when key2 exists with different key1."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        
        dkd2 = DualKeyDict()
        dkd2.set("b", "x", 2)  # key2 "x" exists with key1 "a", not "b"
        
        with pytest.raises(ValueError):
            dkd1 |= dkd2
    
    def test_set_duplicate_same_keys(self):
        """Test overwriting when both keys match (should succeed)."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        
        # This should succeed (overwrite)
        dkd.set("a", "x", 100)
        
        assert dkd.get_by_key1("a") == 100
        assert dkd.get_by_key2("x") == 100
        assert len(dkd) == 1
    
    def test_ior_both_match_same_value(self):
        """Test __ior__ when both dicts have same key pair with same value."""
        dkd1 = DualKeyDict()
        dkd1.set("a", "x", 1)
        orig_len = len(dkd1)
        
        dkd2 = DualKeyDict()
        dkd2.set("a", "x", 1)  # Same pair and value
        
        # Call __ior__ directly
        dkd1.__ior__(dkd2)
        assert len(dkd1) == orig_len
        assert dkd1.get_by_key1("a") == 1
    
    def test_change_key1_key2_conflicts_key1(self):
        """Test change_key1_key2_by_key1 with existing new_key1."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        with pytest.raises(ValueError):
            dkd.change_key1_key2_by_key1("a", "b", "z")
    
    def test_change_key1_key2_conflicts_key2(self):
        """Test change_key1_key2_by_key1 with existing new_key2."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        with pytest.raises(ValueError):
            dkd.change_key1_key2_by_key1("a", "c", "y")
    
    def test_change_key1_key2_by_key1_nonexistent(self):
        """Test change_key1_key2_by_key1 with nonexistent old_key1."""
        dkd = DualKeyDict()
        
        with pytest.raises(KeyError):
            dkd.change_key1_key2_by_key1("nonexistent", "new", "keys")
    
    def test_change_key1_key2_by_key2_conflicts_key1(self):
        """Test change_key1_key2_by_key2 with existing new_key1."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        with pytest.raises(ValueError):
            dkd.change_key1_key2_by_key2("x", "b", "z")
    
    def test_change_key1_key2_by_key2_conflicts_key2(self):
        """Test change_key1_key2_by_key2 with existing new_key2."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        with pytest.raises(ValueError):
            dkd.change_key1_key2_by_key2("x", "c", "y")
    
    def test_change_key1_key2_by_key2_nonexistent(self):
        """Test change_key1_key2_by_key2 with nonexistent old_key2."""
        dkd = DualKeyDict()
        
        with pytest.raises(KeyError):
            dkd.change_key1_key2_by_key2("nonexistent", "new", "keys")
    
    def test_change_key1_to_existing(self):
        """Test changing key1 to one that already exists."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        with pytest.raises(ValueError):
            dkd.change_key1_by_key2("x", "b")
    
    def test_change_key2_to_existing(self):
        """Test changing key2 to one that already exists."""
        dkd = DualKeyDict()
        dkd.set("a", "x", 1)
        dkd.set("b", "y", 2)
        
        with pytest.raises(ValueError):
            dkd.change_key2_by_key1("a", "y")
