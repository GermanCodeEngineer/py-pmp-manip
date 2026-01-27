from __future__ import annotations
from copy       import copy, deepcopy
from typing     import Generic, Iterable, Iterator, NoReturn, TypeVar

from gceutils.decorators import enforce_argument_types


_K1 =  TypeVar("_K1")
_K2 =  TypeVar("_K2")
_V  =  TypeVar("_V")

class DualKeyDict(Generic[_K1, _K2, _V]):
    """
    A custom dictionary system, which allows access by key1 or key2
    """
    
    
    @enforce_argument_types
    def __init__(self, iterable: dict[tuple[_K1, _K2], _V] | None = None, /) -> None:
        """Initialize a DualKeyDict from an optional dictionary of (key1, key2): value mappings."""
        self._values  : dict[_K1, _V ] = {}
        self._k2_to_k1: dict[_K2, _K1] = {}
        self._k1_to_k2: dict[_K1, _K2] = {}
        if iterable is not None:
            for keys, value in iterable.items():
                key1, key2 = keys
                self.set(key1, key2, value)
    
    @enforce_argument_types
    @classmethod
    def from_single_key_value(cls, iterable: Iterable[tuple[_K1, _V]], /) -> DualKeyDict[_K1, _K1, _V]:
        """Create a DualKeyDict where both key1 and key2 are the same."""
        return DualKeyDict({
            (key, key): value for key, value in iterable
        })
    
    @enforce_argument_types
    @classmethod
    def from_both_keys(cls, iterable: Iterable[tuple[_K1, _K2]], value: _V, /) -> DualKeyDict[_K1, _K2, _V]:
        """Create a DualKeyDict where all entries share the same value."""
        return DualKeyDict({
            (key1, key2): value for key1, key2 in iterable
        })
    
    
    # Copy methods
    def copy(self) -> DualKeyDict[_K1, _K2, _V]:
        """Create a shallow copy of this DualKeyDict."""
        return self.__copy__()
    
    def __copy__(self) -> DualKeyDict[_K1, _K2, _V]:
        """Create a shallow copy of this DualKeyDict."""
        new = DualKeyDict()
        new._values   = copy(self._values)
        new._k2_to_k1 = copy(self._k2_to_k1)
        new._k1_to_k2 = copy(self._k1_to_k2)
        return new
    
    def deepcopy(self) -> DualKeyDict[_K1, _K2, _V]:
        """Create a deep copy of this DualKeyDict."""
        return deepcopy(self)


    # Value Update methods
    @enforce_argument_types
    def set(self, key1: _K1, key2: _K2, value: _V) -> None:
        """Set a value with both key1 and key2. Raises ValueError if either key already exists with a different partner key."""
        has_key1 = self.has_key1(key1)
        has_key2 = self.has_key2(key2)
        
        if  has_key1 and not(has_key2):
            real_key2 = self.get_key2_for_key1(key1)
            raise ValueError(f"key1 {key1!r} already exists with different key2 {real_key2!r}")
        elif has_key2 and not(has_key1):
            real_key1 = self.get_key1_for_key2(key2)
            raise ValueError(f"key2 {key2!r} already exists with different key1 {real_key1!r}")
        elif has_key1 and (self.get_key2_for_key1(key1) != key2):
            real_key2 = self.get_key2_for_key1(key1)
            raise ValueError(f"key1 {key1!r} exists with different key2 {real_key2!r}")
            
        self._values  [key1] = value
        self._k2_to_k1[key2] = key1
        self._k1_to_k2[key1] = key2
    
    @enforce_argument_types
    def update_by_key1(self, key1: _K1, value: _V) -> None:
        """Update the value for an existing key1. Raises KeyError if key1 does not exist."""
        if not self.has_key1(key1):
            raise KeyError("`update_by_key1` can not be used to add a new entry. Please use `set` instead")
        self._values[key1] = value

    @enforce_argument_types
    def update_by_key2(self, key2: _K2, value: _V) -> None:
        """Update the value for an existing key2. Raises KeyError if key2 does not exist."""
        if not self.has_key2(key2):
            raise KeyError("`update_by_key2` can not be used to add a new entry. Please use `set` instead")
        key1 = self.get_key1_for_key2(key2)
        self._values[key1] = value
    
    @enforce_argument_types
    def update[_ARG_K1, _ARG_K2, _ARG_V](self, value: DualKeyDict[_ARG_K1, _ARG_K2, _ARG_V], /) -> DualKeyDict[_K1|_ARG_K1, _K2|_ARG_K2, _V|_ARG_V]:
        """Merge another DualKeyDict into this one. Raises ValueError if keys conflict."""
        return self.__ior__(value)
    
    def clear(self) -> None:
        """Remove all entries from the dictionary."""
        self._values  : dict[_K1, _V ] = {}
        self._k2_to_k1: dict[_K2, _K1] = {}
        self._k1_to_k2: dict[_K1, _K2] = {}


    # Value Access methods
    @enforce_argument_types
    def get_by_key1(self, key1: _K1) -> _V:
        """Get the value associated with key1. Raises KeyError if key1 does not exist."""
        try:
            return self._values[key1]
        except KeyError: pass
        raise KeyError(f"key1 {key1!r} does not exist")

    @enforce_argument_types
    def get_by_key2(self, key2: _K2) -> _V:
        """Get the value associated with key2. Raises KeyError if key2 does not exist."""
        key1 = self.get_key1_for_key2(key2) # we can just let a KeyError raise and not do it ourselves
        return self._values[key1]

    @enforce_argument_types
    def get_by_key1_with_default[_ARG](self, key1: _K1, default: _ARG) -> _V | _ARG:
        """Get the value associated with key1, or return default if key1 does not exist."""
        try:
            return self.get_by_key1(key1)
        except KeyError:
            return default

    @enforce_argument_types
    def get_by_key2_with_default[_ARG](self, key2: _K2, default: _ARG) -> _V | _ARG:
        """Get the value associated with key2, or return default if key2 does not exist."""
        try:
            return self.get_by_key2(key2)
        except KeyError:
            return default

    
    # Value Delete methods
    @enforce_argument_types
    def delete_by_key1(self, key1: _K1) -> None:
        """Delete the entry associated with key1. Raises KeyError if key1 does not exist."""
        self.pop_by_key1(key1)

    @enforce_argument_types
    def delete_by_key2(self, key2: _K2) -> None:
        """Delete the entry associated with key2. Raises KeyError if key2 does not exist."""
        self.pop_by_key2(key2)
    
    
    # Value Pop methods
    @enforce_argument_types
    def pop_by_key1(self, key1: _K1) -> _V:
        """Remove and return the value associated with key1. Raises KeyError if key1 does not exist."""
        try:
            key2 = self._k1_to_k2.pop(key1)
        except KeyError: pass
        else:
            self._k2_to_k1.pop(key2)
            return self._values.pop(key1)
        raise KeyError(f"key1 {key1!r} does not exist")

    @enforce_argument_types
    def pop_by_key2(self, key2: _K2) -> _V:
        """Remove and return the value associated with key2. Raises KeyError if key2 does not exist."""
        try:
            key1 = self._k2_to_k1.pop(key2)
        except KeyError: pass
        else:
            self._k1_to_k2.pop(key1)
            return self._values.pop(key1)
        raise KeyError(f"key2 {key2!r} does not exist")

    @enforce_argument_types
    def pop_by_key1_with_default[_ARG](self, key1: _K1, default: _ARG) -> _V | _ARG:
        """Remove and return the value associated with key1, or return default if key1 does not exist."""
        try:
            return self.pop_by_key1(key1)
        except KeyError:
            return default

    @enforce_argument_types
    def pop_by_key2_with_default[_ARG](self, key2: _K2, default: _ARG) -> _V | _ARG:
        """Remove and return the value associated with key2, or return default if key2 does not exist."""
        try:
            return self.pop_by_key2(key2)
        except KeyError:
            return default

    
    # Key Update methods
    @enforce_argument_types
    def change_key1_by_key2(self, key2: _K2, new_key1: _K1) -> None:
        """Change key1 while keeping key2 the same. Raises KeyError or ValueError on conflicts."""
        if not self.has_key2(key2):
            raise KeyError(f"key2 {key2!r} does not exist")
        if self.has_key1(new_key1):
            real_key2 = self.get_key2_for_key1(new_key1)
            raise ValueError(f"new key1 {new_key1!r} already exists with different key2 {real_key2!r}")
        value = self.pop_by_key2(key2)
        self.set(new_key1, key2, value)
    
    @enforce_argument_types
    def change_key2_by_key1(self, key1: _K1, new_key2: _K2) -> None:
        """Change key2 while keeping key1 the same. Raises KeyError or ValueError on conflicts."""
        if not self.has_key1(key1):
            raise KeyError(f"key1 {key1!r} does not exist")
        if self.has_key2(new_key2):
            real_key1 = self.get_key1_for_key2(new_key2)
            raise ValueError(f"new key2 {new_key2!r} already exists with different key1 {real_key1!r}")
        value = self.pop_by_key1(key1)
        self.set(key1, new_key2, value)        


    @enforce_argument_types
    def change_key1_key2_by_key1(self, old_key1: _K1, new_key1: _K1, new_key2: _K2) -> None:
        """Change both keys using old_key1 to identify the entry. Raises KeyError or ValueError on conflicts."""
        if not self.has_key1(old_key1):
            raise KeyError(f"old key1 {old_key1!r} does not exist")
        if self.has_key1(new_key1):
            real_key2 = self.get_key2_for_key1(new_key1)
            raise ValueError(f"new key1 {new_key1!r} already exists with different key2 {real_key2!r}")
        if self.has_key2(new_key2):
            real_key1 = self.get_key1_for_key2(new_key2)
            raise ValueError(f"new key2 {new_key2!r} already exists with different key1 {real_key1!r}")
        value = self.pop_by_key1(old_key1)
        self.set(new_key1, new_key2, value)        

    @enforce_argument_types
    def change_key1_key2_by_key2(self, old_key2: _K2, new_key1: _K1, new_key2: _K2) -> None:
        """Change both keys using old_key2 to identify the entry. Raises KeyError or ValueError on conflicts."""
        if not self.has_key2(old_key2):
            raise KeyError(f"old key2 {old_key2!r} does not exist")
        if self.has_key1(new_key1):
            real_key2 = self.get_key2_for_key1(new_key1)
            raise ValueError(f"new key1 {new_key1!r} already exists with different key2 {real_key2!r}")
        if self.has_key2(new_key2):
            real_key1 = self.get_key1_for_key2(new_key2)
            raise ValueError(f"new key2 {new_key2!r} already exists with different key1 {real_key1!r}")
        value = self.pop_by_key2(old_key2)
        self.set(new_key1, new_key2, value)
    

    # Key Access methods
    @enforce_argument_types
    def has_key1(self, key1: _K1) -> bool:
        """Check if key1 exists in the dictionary."""
        return key1 in self._values
    
    @enforce_argument_types
    def has_key2(self, key2: _K2) -> bool:
        """Check if key2 exists in the dictionary."""
        return key2 in self._k2_to_k1

    @enforce_argument_types
    def get_key1_for_key2(self, key2: _K2) -> _K1:
        """Get key1 paired with the given key2. Raises KeyError if key2 does not exist."""
        try:
            return self._k2_to_k1[key2]
        except KeyError: pass
        raise KeyError(f"key2 {key2!r} does not exist")

    @enforce_argument_types
    def get_key2_for_key1(self, key1: _K1) -> _K2:
        """Get key2 paired with the given key1. Raises KeyError if key1 does not exist."""
        try:
            return self._k1_to_k2[key1]
        except KeyError: pass
        raise KeyError(f"key1 {key1!r} does not exist")


    # Iteration methods
    def keys_key1(self) -> Iterable[_K1]:
        """Return an iterable of all key1 values."""
        return self._values.keys()

    def keys_key2(self) -> Iterable[_K2]:
        """Return an iterable of all key2 values."""
        return self._k2_to_k1.keys()

    def keys_key1_key2(self) -> Iterable[tuple[_K1, _K2]]:
        """Return an iterable of (key1, key2) tuples."""
        return self._k1_to_k2.items()

    def keys_key2_key1(self) -> Iterable[tuple[_K2, _K1]]:
        """Return an iterable of (key2, key1) tuples."""
        return self._k2_to_k1.items()


    def values(self) -> Iterable[_V]:
        """Return an iterable of all values."""
        return self._values.values()
    
    
    def items_key1(self) -> Iterable[tuple[_K1, _V]]:
        """Return an iterable of (key1, value) tuples."""
        return self._values.items()

    def items_key2(self) -> Iterator[tuple[_K2, _V]]:
        """Return an iterator of (key2, value) tuples."""
        for key2 in self._k2_to_k1.keys():
            yield (key2, self.get_by_key2(key2))

    def items_key1_key2(self) -> Iterator[tuple[_K1, _K2, _V]]:
        """Return an iterator of (key1, key2, value) tuples."""
        for key1, key2 in self._k1_to_k2.items():
            yield (key1, key2, self.get_by_key1(key1))

    def items_key2_key1(self) -> Iterator[tuple[_K2, _K1, _V]]:
        """Return an iterator of (key2, key1, value) tuples."""
        for key2, key1 in self._k2_to_k1.items():
            yield (key2, key1, self.get_by_key1(key1))
    

    # Allowed dunder methods
    def __len__(self) -> int:
        """Return the number of entries in the dictionary."""
        return len(self._values)

    def __eq__(self, other: object, /) -> bool:
        """Check equality with another DualKeyDict."""
        if not isinstance(other, DualKeyDict):
            return NotImplemented
        return (self._values == other._values) and (self._k2_to_k1 == other._k2_to_k1) and (self._k1_to_k2 == other._k1_to_k2)

    def __repr__(self) -> str:
        """Return a detailed string representation of the DualKeyDict."""
        from gceutils.repr import grepr
        return grepr(self)
    
    def __bool__(self) -> bool:
        """Return True if the dictionary is non-empty, False otherwise."""
        return bool(len(self))

    @enforce_argument_types
    def __or__[_ARG_K1, _ARG_K2, _ARG_V](self, value: DualKeyDict[_ARG_K1, _ARG_K2, _ARG_V], /) -> DualKeyDict[_K1|_ARG_K1, _K2|_ARG_K2, _V|_ARG_V]:
        """Return a new DualKeyDict with merged contents using the | operator."""
        copy = self.copy()
        return copy.__ior__(value)

    @enforce_argument_types
    def __ror__[_ARG_K1, _ARG_K2, _ARG_V](self, value: DualKeyDict[_ARG_K1, _ARG_K2, _ARG_V], /) -> DualKeyDict[_K1|_ARG_K1, _K2|_ARG_K2, _V|_ARG_V]:
        """Return a new DualKeyDict with merged contents using the | operator (right operand)."""
        copy = self.copy()
        return copy.__ior__(value)

    @enforce_argument_types
    def __ior__[_ARG_K1, _ARG_K2, _ARG_V](self, value: DualKeyDict[_ARG_K1, _ARG_K2, _ARG_V], /) -> DualKeyDict[_K1|_ARG_K1, _K2|_ARG_K2, _V|_ARG_V]:
        """Merge another DualKeyDict into this one using the |= operator. Raises ValueError on key conflicts."""
        for key1, key2, evalue in value.items_key1_key2():
            has_key1 = self.has_key1(key1)
            has_key2 = self.has_key2(key2)
            
            if  has_key1 and not(has_key2):
                real_key2 = self.get_key2_for_key1(key1)
                raise ValueError(f"key1 {key1!r} already exists in DualKeyDict with different key2 {real_key2!r}")
            elif has_key2 and not(has_key1):
                real_key1 = self.get_key1_for_key2(key2)
                raise ValueError(f"key2 {key2!r} already exists in DualKeyDict with different key1 {real_key1!r}")
            elif self.get_key2_for_key1(key1) != key2:
                real_key2 = self.get_key2_for_key1(key1)
                raise ValueError(f"key1 {key1!r} exists in DualKeyDict with different key2 {real_key2!r}")
            
            self._values  [key1] = evalue
            self._k2_to_k1[key2] = key1
            self._k1_to_k2[key1] = key2
    
    
    # Forbidden dunder methods
    def __getitem__(self, key, /) -> NoReturn:
        """Forbidden: use get_by_key1() or get_by_key2() instead."""
        raise NotImplementedError("Can not use getitem syntax (`map[key]`) on a DualKeyDict, as there are two sets of keys. Use `get_by_key1`, `get_by_key2` instead")

    def __setitem__(self, key, value, /) -> NoReturn:
        """Forbidden: use set(), update_by_key1(), or update_by_key2() instead."""
        raise NotImplementedError("Can not use setitem syntax (`map[key] = value`) on a DualKeyDict, as there are two sets of keys. Use `set`, `update_by_key1`, `update_by_key2` instead")

    def __delitem__(self, key, /) -> NoReturn:
        """Forbidden: use delete_by_key1() or delete_by_key2() instead."""
        raise NotImplementedError("Can not use delitem syntax (`del map[key]`) on a DualKeyDict, as there are two sets of keys. Use `delete_by_key1`, `delete_by_key2` instead")
        
    def __iter__(self) -> NoReturn:
        """Forbidden: use keys_key1(), keys_key2(), values(), items_key1(), items_key2() etc. instead."""
        raise NotImplementedError("Can not iterate DualKeyDict directly. Use `keys_key1`, `keys_key2, `values`, `items_key1`, `items_key2` etc. instead")

    def __reversed__(self) -> NoReturn:
        """Forbidden: use keys_key1(), keys_key2(), values(), items_key1(), items_key2() etc. instead."""
        raise NotImplementedError("Can not iterate DualKeyDict directly. Use `keys_key1`, `keys_key2, `values`, `items_key1`, `items_key2` etc. instead")

    def __contains__(self, key, /) -> NoReturn:
        """Forbidden: use has_key1() or has_key2() instead."""
        raise NotImplementedError("Can not check whether a DualKeyDict contains a key, as there are two sets of keys. Use `has_key1` or `has_key2` instead")


__all__ = ["DualKeyDict"]

