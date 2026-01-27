from __future__ import annotations
import pytest
from pathlib import Path

from gceutils.tree_tools import TreeVisitor


class TestTreeVisitor:
    """Test TreeVisitor class."""
    
    def test_create_include_only(self):
        """Test creating TreeVisitor with include_only."""
        visitor = TreeVisitor.create_new_include_only([str, int])
        assert str in visitor.included_types
        assert int in visitor.included_types
    
    def test_create_include_all_except(self):
        """Test creating TreeVisitor with include_all_except."""
        universe = [str, int, float, bool]
        excluded = [bool]
        visitor = TreeVisitor.create_new_include_all_except(excluded, universe)
        assert str in visitor.included_types
        assert int in visitor.included_types
        assert float in visitor.included_types
        assert bool not in visitor.included_types
    
    def test_visit_simple_list(self):
        """Test visiting a simple list."""
        visitor = TreeVisitor.create_new_include_only([int])
        tree = [1, 2, 3]
        result = visitor.visit_tree(tree)
        
        # Should find all integers
        assert len(result) == 3
    
    def test_visit_nested_list(self):
        """Test visiting a nested list."""
        visitor = TreeVisitor.create_new_include_only([int])
        tree = [[1, 2], [3, 4]]
        result = visitor.visit_tree(tree)
        
        # Should find all integers
        assert len(result) == 4
    
    def test_visit_dict(self):
        """Test visiting a dictionary."""
        visitor = TreeVisitor.create_new_include_only([str])
        tree = {"a": "hello", "b": "world"}
        result = visitor.visit_tree(tree)
        
        # Should find string values and keys
        assert len(result) >= 2
    
    def test_visit_mixed_structure(self):
        """Test visiting mixed nested structure."""
        visitor = TreeVisitor.create_new_include_only([int, str])
        tree = {
            "items": [1, 2, 3],
            "names": ["a", "b"],
            "data": {"x": 10, "y": 20}
        }
        result = visitor.visit_tree(tree)
        
        # Should find all ints and strings
        assert len(result) > 0
    
    def test_visit_set(self):
        """Test visiting a set."""
        visitor = TreeVisitor.create_new_include_only([int])
        tree = {1, 2, 3}
        result = visitor.visit_tree(tree)
        
        # Should find all integers
        assert len(result) == 3
    
    def test_visit_frozenset(self):
        """Test visiting a frozenset."""
        visitor = TreeVisitor.create_new_include_only([str])
        tree = frozenset(["a", "b", "c"])
        result = visitor.visit_tree(tree)
        
        # Should find all strings
        assert len(result) == 3
    
    def test_visit_tuple(self):
        """Test visiting a tuple."""
        visitor = TreeVisitor.create_new_include_only([int])
        tree = (1, 2, 3)
        result = visitor.visit_tree(tree)
        
        # Should find all integers
        assert len(result) == 3
    
    def test_visit_empty_collections(self):
        """Test visiting empty collections."""
        visitor = TreeVisitor.create_new_include_only([int])
        
        result1 = visitor.visit_tree([])
        assert len(result1) == 0
        
        result2 = visitor.visit_tree({})
        assert len(result2) == 0
        
        result3 = visitor.visit_tree(set())
        assert len(result3) == 0
    
    def test_visit_excludes_unwanted_types(self):
        """Test that unwanted types are excluded."""
        visitor = TreeVisitor.create_new_include_only([str])
        tree = [1, "hello", 2.5, "world"]
        result = visitor.visit_tree(tree)
        
        # Should only find strings
        for value in result.values():
            assert isinstance(value, str)
    
    def test_visit_paths_different(self):
        """Test that different paths are distinguished."""
        visitor = TreeVisitor.create_new_include_only([int])
        tree = {
            "list": [1, 2],
            "tuple": (3, 4)
        }
        result = visitor.visit_tree(tree)
        
        # Should find 4 integers with different paths
        assert len(result) == 4
        paths = list(result.keys())
        assert len(set(str(p) for p in paths)) == 4


class TestTreeVisitorDataclass:
    """Test TreeVisitor with dataclasses."""
    
    def test_visit_dataclass_basic(self):
        """Test visiting a simple dataclass."""
        from gceutils.base import grepr_dataclass
        
        @grepr_dataclass()
        class Person:
            name: str
            age: int
        
        visitor = TreeVisitor.create_new_include_only([str, int])
        person = Person(name="Alice", age=30)
        result = visitor.visit_tree(person)
        
        # Should find name and age
        assert len(result) >= 2
    
    def test_visit_nested_dataclass(self):
        """Test visiting nested dataclasses."""
        from gceutils.base import grepr_dataclass
        
        @grepr_dataclass()
        class Address:
            street: str
            city: str
        
        @grepr_dataclass()
        class Person:
            name: str
            address: Address
        
        visitor = TreeVisitor.create_new_include_only([str])
        person = Person(
            name="Bob",
            address=Address(street="123 Main St", city="Springfield")
        )
        result = visitor.visit_tree(person)
        
        # Should find all strings
        assert len(result) >= 3
    
    def test_visit_dataclass_with_list(self):
        """Test visiting dataclass containing lists."""
        from gceutils.base import grepr_dataclass
        
        @grepr_dataclass()
        class Team:
            name: str
            members: list[str]
        
        visitor = TreeVisitor.create_new_include_only([str])
        team = Team(name="A-Team", members=["Alice", "Bob", "Charlie"])
        result = visitor.visit_tree(team)
        
        # Should find team name and all member names
        assert len(result) >= 4


class TestTreeVisitorWithCustom:
    """Test TreeVisitor with custom _visit_node_unfiltered_ methods."""
    
    def test_visit_custom_visit_method(self):
        """Test visiting object with custom _visit_node_unfiltered_ method."""
        from gceutils.base import grepr_dataclass
        
        class CustomObject:
            def __init__(self, values):
                self.values = values
            
            def _visit_node_unfiltered_(self, path):
                # Custom visit method that yields values
                from gceutils.base import AbstractTreePath
                pairs = []
                for i, val in enumerate(self.values):
                    new_path = path.add_index_or_key(i)
                    pairs.append((new_path, val))
                return pairs
        
        visitor = TreeVisitor.create_new_include_only([int, str])
        obj = CustomObject([1, "hello", 2, "world"])
        result = visitor.visit_tree(obj)
        
        # Should find all values through custom method
        assert len(result) >= 4
    
    def test_visit_non_dataclass_no_traversal(self):
        """Test that non-dataclass, non-collection objects don't have attributes traversed."""
        
        class PlainClass:
            def __init__(self):
                self.attr1 = "hidden"
                self.attr2 = 42
        
        visitor = TreeVisitor.create_new_include_only([str, int])
        obj = PlainClass()
        result = visitor.visit_tree(obj)
        
        # Should not traverse attributes of plain class (not a dataclass)
        assert len(result) == 0
