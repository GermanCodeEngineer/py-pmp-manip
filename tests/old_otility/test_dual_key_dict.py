from __future__ import annotations
import pytest

from pmp_manip.otility.dual_key_dict import DualKeyDict


class TestDualKeyDict:
    """Test DualKeyDict class."""
    
    def test_empty_creation(self):
        """Test creating empty DualKeyDict."""
        dkd = DualKeyDict()
        assert len(dkd) == 0
    
    def test_set_and_get(self):
        """Test setting and getting values."""
        dkd = DualKeyDict()
        dkd.set("key1", "key2", "value")
        assert dkd.get_by_key1("key1") == "value"
        assert dkd.get_by_key2("key2") == "value"
    
    def test_items_key1_key2(self):
        """Test iterating over items with both keys."""
        dkd = DualKeyDict()
        dkd.set("a", "b", 1)
        dkd.set("c", "d", 2)
        items = list(dkd.items_key1_key2())
        assert len(items) == 2
