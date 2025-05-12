# Utility functions
def grepr(obj, annotate_fields=True, include_attributes=False, *, indent=4):
    def _format(obj, level=0):
        is_compatible = bool(getattr(obj, "_grepr", False))
        if indent is not None:
            level += 1
            prefix = '\n' + indent * level
            sep = ',\n' + indent * level
        else:
            prefix = ''
            sep = ', '
        if isinstance(obj, list):
            if not obj:
                return '[]', True
            return '[%s%s]' % (prefix, sep.join(_format(x, level)[0] for x in obj)), False
        if isinstance(obj, tuple):
            if not obj:
                return '()', True
            if len(obj) <= 2:
                return '(%s)' % (", ".join(_format(x, level)[0] for x in obj)), False
            else:
                return '(%s%s)' % (prefix, sep.join(_format(x, level)[0] for x in obj)), False
        elif isinstance(obj, dict):
            if not obj:
                return '{}', True
            args = [f'{_format(key, level)[0]}: {_format(value, level)[0]}' for key,value in obj.copy().items()]    
            short = '{%s}' % (", ".join(args),)
            return '{%s%s}' % (prefix, sep.join(args)), False
        elif isinstance(obj, DualKeyDict):
            if not obj:
                return 'DKD{}', True
            args = []
            for key1, key2, value in obj.items_key1_key2():
                key1_str, _ = _format(key1, level)
                key2_str, _ = _format(key2, level)
                value_str, _ = _format(value, level)
                args.append(f'{key1_str} / {key2_str}: {value_str}')
            return 'DKD{%s%s}' % (prefix, sep.join(args)), False
        elif is_compatible:
            cls = type(obj)
            args = []
            allsimple = True
            keywords = annotate_fields
            for name in obj._grepr_fields:
                if not hasattr(obj, name):
                    continue
                value = getattr(obj, name)
                value, simple = _format(value, level)
                allsimple = allsimple and simple
                if keywords:
                    args.append('%s=%s' % (name, value))
                else:
                    args.append(value)
            if include_attributes and obj._attributes:
                for name in obj._attributes:
                    try:
                        value = getattr(obj, name)
                    except AttributeError:
                        continue
                    if value is None and getattr(cls, name, ...) is None:
                        continue
                    value, simple = _format(value, level)
                    allsimple = allsimple and simple
                    args.append('%s=%s' % (name, value))
            class_name = getattr(obj, "_grepr_class_name", obj.__class__.__name__)
            if allsimple and len(args) <= 3:
                return '%s(%s)' % (class_name, ', '.join(args)), not args
            return '%s(%s%s)' % (class_name, prefix, sep.join(args)), False
        return repr(obj), True
 
    is_compatible = bool(getattr(obj, "_grepr", False))
    if not(is_compatible) and not(isinstance(obj, (list, dict))):
        return repr(obj)
    if indent is not None and not isinstance(indent, str):
        indent = ' ' * indent
    return _format(obj)[0]

# Files
import zipfile
import os
from pypenguin.utility.errors import PathError

def read_file_of_zip(zip_path, file_path):
    zip_path = ensure_correct_path(zip_path)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        with zip_ref.open(file_path) as file_ref:
            content = file_ref.read().decode("utf-8")
    return content

def ensure_correct_path(_path, target_folder_name="pypenguin"):
    if target_folder_name is not None:
        initial_path = __file__
        current_path = os.path.normpath(initial_path)

        while True:
            base_name = os.path.basename(current_path)
            
            if base_name == target_folder_name and os.path.isdir(current_path):
                break
            
            parent_path = os.path.dirname(current_path)
            
            if parent_path == current_path:
                raise PathError(f"Target folder '{target_folder_name}' not found in the _path '{initial_path}'")
            
            current_path = parent_path

        final_path = os.path.join(current_path, _path)
        return final_path

# Utility Classes
from enum import Enum
from typing import TypeVar, Generic, Iterator

class PypenguinEnum(Enum):
    def __repr__(self):
        return self.__class__.__name__ + "." + self.name

class GreprClass:
    def __repr__(self) -> str:
        return grepr(self)

K1 = TypeVar("K1")
K2 = TypeVar("K2")
V  = TypeVar("V" )

class DualKeyDict(Generic[K1, K2, V]):
    """
    A custom dictionary system, which allows access by key1 or key2.
    """
    def __init__(self, data: dict[tuple[K1, K2], V] | None = None, /) -> None:
        self._values  : dict[K1, V ] = {}
        self._k2_to_k1: dict[K2, K1] = {}
        self._k1_to_k2: dict[K1, K2] = {}
        if data is not None:
            for keys, value in data.items():
                key1, key2 = keys
                self.set(key1, key2, value)

    @classmethod
    def from_same_keys(cls, data: dict[K1, V]) -> "DualKeyDict[K1, K1, V]":
        return DualKeyDict({
            (key, key): value for key, value in data.items()
        })

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DualKeyDict):
            return NotImplemented
        return (self._values == other._values) and (self._k2_to_k1 == other._k2_to_k1) and (self._k1_to_k2 == other._k1_to_k2)

    def __repr__(self) -> str:
        return grepr(self)

    def set(self, key1: K1, key2: K2, value: V) -> None:
        self._values[key1] = value
        self._k2_to_k1[key2] = key1
        self._k1_to_k2[key1] = key2

    def get_by_key1(self, key1: K1) -> V:
        return self._values[key1]

    def get_by_key2(self, key2: K2) -> V:
        key1 = self.get_key1_for_key2(key2)
        return self._values[key1]

    def get_key1_for_key2(self, key2: K2) -> K1:
        return self._k2_to_k1[key2]

    def get_key2_for_key1(self, key1: K1) -> K2:
        return self._k1_to_k2[key1]

    def has_key1(self, key1: K1) -> bool:
        return key1 in self._values
    
    def has_key2(self, key2: K2) -> bool:
        return key2 in self._k2_to_k1

    # Dict-like behavior (explicitly discouraged)
    def __iter__(self):
        raise NotImplementedError("Don't iterate DualKeyDict directly. Use keys_key1, keys_key2, values, items_key1, items_key2 etc.")

    def __contains__(self, key: object) -> bool:
        raise NotImplementedError("Don't check whether a DualKeyDict contains something like a normal dict. Use has_key1 or has_key2 instead.")

    def __len__(self) -> int:
        return len(self._values)

    # Iteration methods
    def keys_key1(self) -> Iterator[K1]:
        return self._values.keys()
    
    def keys_key2(self) -> Iterator[K2]:
        return self._k2_to_k1.keys()
    
    def keys_key1_key2(self) -> Iterator[tuple[K1, K2]]:
        return self._k1_to_k2.items()
    
    def values(self) -> Iterator[V]:
        return self._values.values()
    
    def items_key1(self) -> Iterator[tuple[K1, V]]:
        return self._values.items()

    def items_key2(self) -> Iterator[tuple[K2, V]]:
        for key2 in self._k2_to_k1.keys():
            yield (key2, self.get_by_key2(key2))
    
    def items_key1_key2(self) -> Iterator[tuple[K1, K2, V]]:
        for key2, key1 in self._k2_to_k1.items():
            yield (key1, key2, self.get_by_key1(key1))

# Data Functions
from difflib import SequenceMatcher
from hashlib import sha256

token_charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%()*+,-./:;=?@[]^_`{|}~"
charset_char_count = len(token_charset)

def remove_duplicates(items: list) -> list:
    seen = []
    result = []
    for item in items:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result

def lists_equal_ignore_order(a: list, b: list) -> bool:
    if len(a) != len(b):
        return False

    b_copy = b[:]
    for item in a:
        try:
            b_copy.remove(item)  # uses __eq__, safe for mutable objects
        except ValueError:
            return False
    return not b_copy

def get_closest_matches(string, possible_values: list[str], n: int) -> list[str]:
    similarity_scores = [(item, SequenceMatcher(None, string, item).ratio()) for item in possible_values]
    sorted_matches = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    return [i[0] for i in sorted_matches[:n]]   

def tuplify(obj):
    if isinstance(obj, list):
        return tuple(tuplify(item) for item in obj)
    elif isinstance(obj, dict):
        return {tuplify(key): tuplify(value) for key, value in obj.items()}
    elif isinstance(obj, (set, tuple)):
        return type(obj)(tuplify(item) for item in obj)
    else:
        return obj

def string_to_sha256(primary: str, secondary: str|None=None) -> str:
    def convert(input_string: str, digits: int) -> str:
        hash_object = sha256(input_string.encode())
        hex_hash = hash_object.hexdigest()

        result = []
        for i in range(digits):
            chunk = hex_hash[i * 2:(i * 2) + 2]
            index = int(chunk, 16) % charset_char_count
            result.append(token_charset[index])

        return ''.join(result)

    if secondary is None:
        return convert(primary, digits=20)
    else:
        return convert(primary, digits=16) + convert(secondary, digits=4)

