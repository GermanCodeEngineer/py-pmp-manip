from __future__  import annotations
from dataclasses import fields as get_fields
from typing      import cast, Generic, TypeVar, Iterable, Any

from gceutils.base       import grepr_dataclass, AbstractTreePath
from gceutils.decorators import enforce_argument_types


INCLUDED_T = TypeVar("INCLUDED_T")
DEFAULT_T = TypeVar("DEFAULT_T")

@grepr_dataclass(frozen=True, unsafe_hash=True)
class TreeVisitor(Generic[INCLUDED_T]):
    """
    Implements the recursive iteration of an arbitrary object tree.
    **NOTE: Only dataclasses can be visited correctly as tree nodes.**
    Non-dataclass objects (except list, tuple, set, frozenset, dict) will not have their attributes traversed.
    """
    included_types: tuple[type[INCLUDED_T], ...]
    
    @enforce_argument_types
    @classmethod
    def create_new_include_only(cls, included: Iterable[type[INCLUDED_T]]) -> TreeVisitor[INCLUDED_T]:
        """
        Create a new tree visitor, which only includes values of the specified types.
        """
        return cls(tuple(included))

    # sadly the most specific signature we can make without a global universe of types:
    @enforce_argument_types
    @classmethod
    def create_new_include_all_except(cls, excluded: Iterable[type[INCLUDED_T]], universe: Iterable[type[INCLUDED_T]]) -> TreeVisitor[INCLUDED_T]:
        """
        Create a new tree visitor, which includes all types from ``universe`` except the specified ``excluded`` ones.
        """
        included = [t for t in universe if t not in excluded]
        return cls(tuple(included))
    
    @staticmethod
    def _get_yield_fields(cls: type[Any]) -> list[str]:
        """
        Get the relevant fields of a dataclass-like node type.
        **NOTE: Only works with dataclasses.**
        """
        try:
            fields = get_fields(cls)
        except TypeError:
            return []
        return [field.name for field in fields]
    
    @classmethod
    def _visit_node_unfiltered(cls,
        obj: Any | list[Any] | tuple[Any] | dict[Any, Any], 
        path: AbstractTreePath,
    ) -> Iterable[tuple[AbstractTreePath, Any]]:
        """
        Run the tree visitor unfiltered on an arbitrary object tree.
        Returns pairs of node path (from tree root to value) and node value.
        **NOTE: Non-dataclass objects (except list, tuple, set, frozenset, dict) will only be yielded as values,
        their attributes will not be traversed.**
        
        Args:
            obj: the object tree to iterate recursively
            path: the path from the tree root to obj
        """
        pairs = []
        if   isinstance(obj, (list, tuple, set, frozenset)):
            for i, item in enumerate(obj):
                current_path = path.add_index_or_key(i)
                pairs.append((current_path, item))
                pairs.extend(cls._visit_node_unfiltered(item, current_path))
        elif isinstance(obj, dict):
            for key, value in obj.items():
                current_path = path.add_index_or_key(key)
                pairs.append((current_path, value))
                pairs.extend(cls._visit_node_unfiltered(value, current_path))
        elif callable(getattr(obj, "_visit_node_unfiltered_", None)):
            # allow defining custom _visit_node_unfiltered_ methods on classes
            pairs.extend(obj._visit_node_unfiltered_(path))
        else:
            fields = cls._get_yield_fields(type(obj))
            for field in fields:
                value = getattr(obj, field)
                if value is not None:
                    current_path = path.add_attribute(field)
                    pairs.append((current_path, value))
                    pairs.extend(cls._visit_node_unfiltered(value, current_path))
        return pairs

    # INCLUDED_T will be inferred as Any by type checkers, no solution possible currently
    @enforce_argument_types
    def visit_tree(self, obj: Any) -> dict[AbstractTreePath, INCLUDED_T]:
        """
        Run the tree visitor recursively on an arbitrary object tree.
        Returns a map from node path (from tree root to value) to node value.
        **NOTE: Non-dataclass objects (except list, tuple, set, frozenset, dict) will only be yielded as values,
        their attributes will not be traversed.**
        """
        unfiltered_pairs = self._visit_node_unfiltered(obj, path=AbstractTreePath())
        filtered_map: dict[AbstractTreePath, INCLUDED_T] = {}
        for path, value in unfiltered_pairs:
            if isinstance(value, self.included_types):
                filtered_map[path] = cast(INCLUDED_T, value)
        return filtered_map


__all__ = ["TreeVisitor"]

