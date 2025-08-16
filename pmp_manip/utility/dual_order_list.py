from copy   import deepcopy
from typing import TypeVar, Generic, Iterable, NoReturn, Any

from pmp_manip.utility.decorators    import enforce_argument_types
from pmp_manip.utility.dual_index_dict import DualindexDict
from pmp_manip.utility.errors        import MANIP_ValueError, MANIP_IndexError


_IT = TypeVar("_IT") # Item Type
# For method arguments:
#_ARG = TypeVar("_ARG")

class DualOrderList(Generic[_IT]):
    """
    A custom list system, which allows the same elements to be accessable in two orders
    """
    
    
    # Initialization methods
    @enforce_argument_types
    def __init__(self, iterable: DualindexDict[int, int, _IT] | None = None) -> None:
        max_index = len(iterable) - 1
        if iterable is None:
            self._contents: DualindexDict[int, int, _IT] = DualindexDict()
        else:
            for index1, index2 in iterable.items_key1_key2():
                if not isinstance(index1, int):
                    raise MANIP_ValueError(f"All index1's and index2's must be integers, not {type(index1)!r}: {index1}")
                if (index1 < 0) or (index1 > max_index):
                    raise MANIP_ValueError(f"All index1's and index2's must be positive integers and at most {max_index!r}(len-1): {index1}")
                
                if not isinstance(index2, int):
                    raise MANIP_ValueError(f"All index1's and index2's must be integers, not {type(index2)!r}: {index2}")
                if (index2 < 0) or (index2 > max_index):
                    raise MANIP_ValueError(f"All index1's and index2's must be positive integers and at most {max_index!r}(len-1): {index2}")
             
             self._contents: DualindexDict[int, int, _IT] = iterable.copy()

    
    @enforce_argument_types
    @classmethod
    def from_single_order(cls, iterable: Iterable[_IT]) -> "DualOrderList[_IT]":
        dkd = DualindexDict.from_single_index_value(enumerate(iterable))
        return DualOrderList(dkd)

    @enforce_argument_types
    @classmethod
    def from_single_order_and_index_list(cls, iterable: Iterable[_IT], index_map: list[int]) -> "DualOrderList[_IT]":
        """
        Example: 
        - iterable: ["a", "b", "c"]
        - index_map: [1, 0, 2]  => index in index_map = index in Order2; item = index of target value in main iterable
        => Order1: ["a", "b", "c"]
        => Order2: ["b", "a", "c"]
        """
        iterable = list(iterable)
        dkd = DualindexDict()
        for order2_index, order1_index in enumerate(index_map):
            value = iterable[order1_index]
            dkd.set(order1_index, order2_index, value)
        return DualOrderList(dkd)
    
    
    # Copy methods
    def copy(self) -> "DualOrderList[_IT]":
        return self.__copy__()
    
    def __copy__(self) -> "DualOrderList[_IT]":
        return DualOrderList(self._contents) # __init__ copies anyway
    
    def deepcopy(self) -> "DualOrderList[_IT]":
        return self.__deepcopy__()
    
    def __deepcopy__(self) -> "DualOrderList[_IT]":
        return DualOrderList(deepcopy(self._contents))


    # Value Update methods
    def append(self, object: _IT) -> None:
        index = len(self._contents)
        self._contents.set(index, index, object)
    
    @enforce_argument_types
    def extend(self, object: "DualOrderList[_IT]") -> None:
        offset = len(self)
        for index1, index2, value in object._contents.items_key1_key2():
            self._contents.set(index1 + offset, index2 + offset, value)
    
    @enforce_argument_types
    def set(self, index1: int, index2: int, value: _IT) -> None:
        has_index1 = self.has_index(index1)
        has_index2 = self.has_index(index2)
        
        if  has_index1 and not(has_index2):
            real_index2 = self.get_index2_for_index1(index1)
            raise MANIP_ValueError(f"index1 {index1!r} already exists with different index2 {real_index2!r}")
        elif has_index2 and not(has_index1):
            real_index1 = self.get_index1_for_index2(index2)
            raise MANIP_ValueError(f"index2 {index2!r} already exists with different index1 {real_index1!r}")
        elif has_index1 and (self.get_index2_for_index1(index1) != index2):
            real_index2 = self.get_index2_for_index1(index1)
            raise MANIP_ValueError(f"index1 {index1!r} exists with different index2 {real_index2!r}")
    
    @enforce_argument_types
    def update_by_index1(self, index1: int, value: _IT) -> None:
        if not self.has_index(index1):
            raise MANIP_IndexError("`update_by_index1` can not be used to add a new entry. Please use `set` or `append` instead")
        self._contents.update_by_key1(index1, value) = value

    @enforce_argument_types
    def update_by_index2(self, index2: int, value: _IT) -> None:
        if not self.has_index(index2):
            raise MANIP_IndexError("`update_by_index2` can not be used to add a new entry. Please use `set` or `append` instead")
        self._contents.update_by_key1(index2, value) = value


    # Value Access methods
    @enforce_argument_types
    def get_by_index1(self, index1: int) -> _IT:
        try:
            return self._contents.get_by_key1(index1)
        except MANIP_KeyError: pass
        raise MANIP_IndexError(f"DualOrderList index1 out of range: {index1}")

    @enforce_argument_types
    def get_by_index2(self, index2: int) -> _IT:
        try:
            return self._contents.get_by_key2(index2)
        except MANIP_KeyError: pass
        raise MANIP_IndexError(f"DualOrderList index2 out of range: {index2}")
    
    # Value Delete methods
    @enforce_argument_types
    def delete_by_index1(self, index1: int) -> None:
        self.pop_by_index1(index1)

    @enforce_argument_types
    def delete_by_index2(self, index2: int) -> None:
        self.pop_by_index2(index2)
    
    
    # Value Pop methods
    @enforce_argument_types
    def pop_by_index1(self, index1: int) -> _IT:
        try:
            return self._contents.pop_by_key1(index1)
        except MANIP_KeyError: pass
        raise MANIP_IndexError(f"index1 {index1!r} does not exist")

    @enforce_argument_types
    def pop_by_index2(self, index2: int) -> _IT:
        try:
            return self._contents.pop_by_key2(index2)
        except MANIP_KeyError: pass
        raise MANIP_IndexError(f"index2 {index2!r} does not exist")
    
    # Index Update methods
    @enforce_argument_types
    def change_index1_by_index2(self, index2: int, new_index1: int) -> None:
        if not self.has_index(index2):
            raise MANIP_IndexError(f"index2 {index2!r} does not exist")
        if self.has_index1(new_index1):
            real_index2 = self.get_index2_for_index1(new_index1)
            raise MANIP_ValueError(f"new index1 {new_index1!r} already exists with different index2 {real_index2!r}")
        value = self.pop_by_index2(index2)
        self.set(new_index1, index2, value)
    
    @enforce_argument_types
    def change_index2_by_index1(self, index1: int, new_index2: int) -> None:
        if not self.has_index1(index1):
            raise MANIP_IndexError(f"index1 {index1!r} does not exist")
        if self.has_index2(new_index2):
            real_index1 = self.get_index1_for_index2(new_index2)
            raise MANIP_ValueError(f"new index2 {new_index2!r} already exists with different index1 {real_index1!r}")
        value = self.pop_by_index1(index1)
        self.set(index1, new_index2, value)        


    @enforce_argument_types
    def change_index1_index2_by_index1(self, old_index1: int, new_index1: int, new_index2: int) -> None:
        if not self.has_index1(old_index1):
            raise MANIP_IndexError(f"old index1 {old_index1!r} does not exist")
        if self.has_index1(new_index1):
            real_index2 = self.get_index2_for_index1(new_index1)
            raise MANIP_ValueError(f"new index1 {new_index1!r} already exists with different index2 {real_index2!r}")
        if self.has_index2(new_index2):
            real_index1 = self.get_index1_for_index2(new_index2)
            raise MANIP_ValueError(f"new index2 {new_index2!r} already exists with different index1 {real_index1!r}")
        value = self.pop_by_index1(old_index1)
        self.set(new_index1, new_index2, value)        

    @enforce_argument_types
    def change_index1_index2_by_index2(self, old_index2: int, new_index1: int, new_index2: int) -> None:
        if not self.has_index2(old_index2):
            raise MANIP_IndexError(f"old index2 {old_index2!r} does not exist")
        if self.has_index1(new_index1):
            real_index2 = self.get_index2_for_index1(new_index1)
            raise MANIP_ValueError(f"new index1 {new_index1!r} already exists with different index2 {real_index2!r}")
        if self.has_index2(new_index2):
            real_index1 = self.get_index1_for_index2(new_index2)
            raise MANIP_ValueError(f"new index2 {new_index2!r} already exists with different index1 {real_index1!r}")
        value = self.pop_by_index2(old_index2)
        self.set(new_index1, new_index2, value)
    

    # Index Access methods
    @enforce_argument_types
    def normalize_index(self, index: int, tolerant: bool = False, suffix: str = "") -> int:
        if index < 0:
            lindex = index + len(self)
        else:
            lindex = index
        
        if not(tolerant) and ((lindex < 0) or (lindex > len(self))):
            raise MANIP_IndexError(f"DualOrderList index{suffix} out of range: {index}")
        else:
            return lindex
    
    @enforce_argument_types
    def has_index(self, index: int) -> bool:
        try:
            self.normalize_index(index, tolerant=False)
            return True
        except MANIP_IndexError:
            return False
    
    """def get_index1_for_index2(self, index2: int) -> int:
        try:
            return self.int_toint[index2]
        except indexError: pass
        raise MANIP_IndexError(f"index2 {index2!r} does not exist")

    def get_index2_for_index1(self, index1: int) -> int:
        try:
            return self.int_toint[index1]
        except indexError: pass
        raise MANIP_IndexError(f"index1 {index1!r} does not exist")


    # Iteration methods
    def indexs_index1(self) -> Iterable[int]:
        return self._values.indexs()

    def indexs_index2(self) -> Iterable[int]:
        return self.int_toint.indexs()

    def indexs_index1_index2(self) -> Iterable[tuple[int, int]]:
        return self.int_toint.items()

    def indexs_index2_index1(self) -> Iterable[tuple[int, int]]:
        return self.int_toint.items()


    def values(self) -> Iterable[_IT]:
        return self._values.values()
    
    
    def items_index1(self) -> Iterable[tuple[int, _IT]]:
        return self._values.items()

    def items_index2(self) -> Iterable[tuple[int, _IT]]:
        for index2 in self.int_toint.indexs():
            yield (index2, self.get_by_index2(index2))

    def items_index1_index2(self) -> Iterable[tuple[int, int, _IT]]:
        for index1, index2 in self.int_toint.items():
            yield (index1, index2, self.get_by_index1(index1))

    def items_index2_index1(self) -> Iterable[tuple[int, int, _IT]]:
        for index2, index1 in self.int_toint.items():
            yield (index2, index1, self.get_by_index1(index1))
    

    # Allowed dunder methods
    def __len__(self) -> int:
        return len(self._values)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DualindexDict):
            return NotImplemented
        return (self._values == other._values) and (self.int_toint == other.int_toint) and (self.int_toint == other.int_toint)

    def __repr__(self) -> str:
        from pmp_manip.utility.repr import grepr
        return grepr(self)
    
    def __bool__(self) -> bool:
        return bool(len(self))

    def __or__(self, value: "DualindexDict[_ARGint, _ARGint, _ARG_IT]") -> "DualindexDict[int|_ARGint, int|_ARGint, _IT|_ARG_IT]":
        copy = self.copy()
        return copy.__ior__(value)

    def __ror__(self, value: "DualindexDict[_ARGint, _ARGint, _ARG_IT]") -> "DualindexDict[int|_ARGint, int|_ARGint, _IT|_ARG_IT]":
        copy = self.copy()
        return copy.__ior__(value)

    def __ior__(self, value: "DualindexDict[_ARGint, _ARGint, _ARG_IT]") -> "DualindexDict[int|_ARGint, int|_ARGint, _IT|_ARG_IT]":
        if not isinstance(value, DualindexDict):
            raise MANIP_ValueError(f"only argument must be DualindexDict, not {type(value)!r}")
        for index1, index2, evalue in value.items_index1_index2():
            has_index1 = self.has_index1(index1)
            has_index2 = self.has_index2(index2)
            
            if  has_index1 and not(has_index2):
                real_index2 = self.get_index2_for_index1(index1)
                raise MANIP_ValueError(f"index1 {index1!r} already exists in DualindexDict with different index2 {real_index2!r}")
            elif has_index2 and not(has_index1):
                real_index1 = self.get_index1_for_index2(index2)
                raise MANIP_ValueError(f"index2 {index2!r} already exists in DualindexDict with different index1 {real_index1!r}")
            elif self.get_index2_for_index1(index1) != index2:
                real_index2 = self.get_index2_for_index1(index1)
                raise MANIP_ValueError(f"index1 {index1!r} exists in DualindexDict with different index2 {real_index2!r}")
            
            self._values  [index1] = evalue
            self.int_toint[index2] = index1
            self.int_toint[index1] = index2
    
    
    # Forbidden dunder methods
    def __getitem__(self, index) -> NoReturn:
        raise NotImplementedError("Can not use getitem syntax (`map[index]`) on a DualindexDict, as there are two sets of indexs. Use `get_by_index1`, `get_by_index2` instead")

    def __setitem__(self, index, value) -> NoReturn:
        raise NotImplementedError("Can not use setitem syntax (`map[index] = value`) on a DualindexDict, as there are two sets of indexs. Use `set`, `update_by_index1`, `update_by_index2` instead")

    def __delitem__(self, index) -> NoReturn:
        raise NotImplementedError("Can not use delitem syntax (`del map[index]`) on a DualindexDict, as there are two sets of indexs. Use `delete_by_index1`, `delete_by_index2` instead")
        
    def __iter__(self) -> NoReturn:
        raise NotImplementedError("Can not iterate DualindexDict directly. Use `indexs_index1`, `indexs_index2, `values`, `items_index1`, `items_index2` etc. instead")

    def __reversed__(self) -> NoReturn:
        raise NotImplementedError("Can not iterate DualindexDict directly. Use `indexs_index1`, `indexs_index2, `values`, `items_index1`, `items_index2` etc. instead")

    def __contains__(self, index) -> NoReturn:
        raise NotImplementedError("Can not check whether a DualindexDict contains a index, as there are two sets of indexs. Use `has_index1` or `has_index2` instead")"""


__all__ = ["DualOrderList"]

