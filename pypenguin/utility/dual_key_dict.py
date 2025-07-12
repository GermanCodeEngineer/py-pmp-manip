from copy   import copy
from typing import TypeVar, Generic, Iterator, Iterable, Any


_K1 = TypeVar("_K1")
_K2 = TypeVar("_K2")
_V  = TypeVar("_V" )

class DualKeyDict(Generic[_K1, _K2, _V]):
    """
    A custom dictionary system, which allows access by key1 or key2
    """
    def __init__(self, data: dict[tuple[_K1, _K2], _V] | None = None, /) -> None:
        self._values  : dict[_K1, _V ] = {}
        self._k2_to_k1: dict[_K2, _K1] = {}
        self._k1_to_k2: dict[_K1, _K2] = {}
        if data is not None:
            for keys, value in data.items():
                key1, key2 = keys
                self.set(key1, key2, value)

    @classmethod
    def from_same_keys(cls, data: dict[_K1, _V]) -> "DualKeyDict[_K1, _K1, _V]":
        return DualKeyDict({
            (key, key): value for key, value in data.items()
        })

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DualKeyDict):
            return NotImplemented
        return (self._values == other._values) and (self._k2_to_k1 == other._k2_to_k1) and (self._k1_to_k2 == other._k1_to_k2)

    def __repr__(self) -> str:
        from pypenguin.utility.repr import grepr
        return grepr(self)

    def set(self, key1: _K1, key2: _K2, value: _V) -> None:
        self._values[key1] = value
        self._k2_to_k1[key2] = key1
        self._k1_to_k2[key1] = key2
    
    def delete_by_key1(self, key1: _K1) -> None:
        key2 = self._k1_to_k2.pop(key1)
        self._k2_to_k1.pop(key2)
        self._values.pop(key1)

    def delete_by_key2(self, key2: _K2) -> None:
        key1 = self._k2_to_k1.pop(key2)
        self._k1_to_k2.pop(key1)
        self._values.pop(key1)

    def get_by_key1(self, key1: _K1) -> _V:
        return self._values[key1]

    def get_by_key2(self, key2: _K2) -> _V:
        key1 = self.get_key1_for_key2(key2)
        return self._values[key1]

    def get_key1_for_key2(self, key2: _K2) -> _K1:
        return self._k2_to_k1[key2]

    def get_key2_for_key1(self, key1: _K1) -> _K2:
        return self._k1_to_k2[key1]

    def has_key1(self, key1: _K1) -> bool:
        return key1 in self._values
    
    def has_key2(self, key2: _K2) -> bool:
        return key2 in self._k2_to_k1

    # Dict-like behavior (explicitly discouraged)
    def __iter__(self):
        raise NotImplementedError("Don't iterate DualKeyDict directly. Use keys_key1, keys_key2, values, items_key1, items_key2 etc")

    def __contains__(self, key: Any) -> bool:
        raise NotImplementedError("Don't check whether a DualKeyDict contains something like a normal dict. Use has_key1 or has_key2 instead")

    # Dict-like behavior
    def __len__(self) -> int:
        return len(self._values)

    def __bool__(self) -> bool:
        return bool(len(self))
    
    def __copy__(self) -> "DualKeyDict":
        new = DualKeyDict()
        new._values   = copy(self._values)
        new._k2_to_k1 = copy(self._k2_to_k1)
        new._k1_to_k2 = copy(self._k1_to_k2)
        return new
    
    # Iteration methods
    def keys_key1(self) -> Iterator[_K1]:
        return self._values.keys()
    
    def keys_key2(self) -> Iterator[_K2]:
        return self._k2_to_k1.keys()
    
    def keys_key1_key2(self) -> Iterator[tuple[_K1, _K2]]:
        return self._k1_to_k2.items()
    
    def keys_key2_key1(self) -> Iterator[tuple[_K2, _K1]]:
        return self._k2_to_k1.items()
    
    def values(self) -> Iterator[_V]:
        return self._values.values()
    
    def items_key1(self) -> Iterator[tuple[_K1, _V]]:
        return self._values.items()

    def items_key2(self) -> Iterator[tuple[_K2, _V]]:
        for key2 in self._k2_to_k1.keys():
            yield (key2, self.get_by_key2(key2))
    
    def items_key1_key2(self) -> Iterator[tuple[_K1, _K2, _V]]:
        for key1, key2 in self._k1_to_k2.items():
            yield (key1, key2, self.get_by_key1(key1))
    
    def items_key2_key1(self) -> Iterator[tuple[_K2, _K1, _V]]:
        for key2, key1 in self._k2_to_k1.items():
            yield (key2, key1, self.get_by_key1(key1))


__all__ = ["DualKeyDict"]

