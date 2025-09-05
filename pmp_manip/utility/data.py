from copy        import copy
from dataclasses import field
from difflib     import SequenceMatcher
from hashlib     import sha256, md5
from json        import dumps
from typing      import overload, Iterable, Iterator, SupportsIndex, Any

from pmp_manip.utility.decorators import grepr_dataclass, enforce_argument_types
from pmp_manip.utility.errors     import MANIP_ValueError


_TOKEN_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%()*+,-./:;=?@[]^_`{|}~"

def remove_duplicates(items: list) -> list:
    seen = []
    result = []
    for item in items:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result

def get_closest_matches(string, possible_values: list[str], n: int) -> list[str]:
    similarity_scores = [(item, SequenceMatcher(None, string, item).ratio()) for item in possible_values]
    sorted_matches = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    return [i[0] for i in sorted_matches[:n]]   

def tuplify(obj):
    if   isinstance(obj, list):
        return tuple(tuplify(item) for item in obj)
    elif isinstance(obj, dict):
        return {tuplify(key): tuplify(value) for key, value in obj.items()}
    elif isinstance(obj, (set, tuple)):
        return type(obj)(tuplify(item) for item in obj)
    else:
        return obj

def listify(obj):
    if   isinstance(obj, tuple):
        return [listify(item) for item in obj]
    elif isinstance(obj, dict):
        return {listify(key): listify(value) for key, value in obj.items()}
    elif isinstance(obj, (set, list)):
        return type(obj)(tuplify(item) for item in obj)
    else:
        return obj

def gdumps(obj) -> str:
    return dumps(obj, separators=(",", ":"))  # no spaces after commas or colons

def string_to_sha256(primary: str | int | bool, secondary: str|None=None, tertiary: str|None=None) -> str:
    def _string_to_sha256(input_string: str | int | bool, digits: int) -> str:
        hex_hash = sha256(str(input_string).encode()).hexdigest()

        result = []
        for i in range(digits):
            chunk = hex_hash[i * 2:(i * 2) + 2]
            index = int(chunk, 16) % len(_TOKEN_CHARSET)
            result.append(_TOKEN_CHARSET[index])
        return ''.join(result)

    if (secondary is None) and (tertiary is not None):
        raise ValueError("secondary must NOT be None if tertiary is not None")

    # return f"<p={primary!r} s={secondary!r} t={tertiary!r}>" # for debugging
    if   (secondary is     None) and (tertiary is     None):
        return _string_to_sha256(primary  , digits=20)
    elif (secondary is not None) and (tertiary is     None):
        return _string_to_sha256(secondary, digits=4) + _string_to_sha256(primary  , digits=16)
    elif (secondary is not None) and (tertiary is not None):
        return _string_to_sha256(tertiary , digits=4) + _string_to_sha256(secondary, digits=4) + _string_to_sha256(primary, digits=12)
        

def number_to_token(number: int) -> str:
    base = len(_TOKEN_CHARSET)
    result = []
    while number > 0:
        number -= 1
        result.insert(0, _TOKEN_CHARSET[number % base])
        number //= base
    return ''.join(result)

def generate_md5(data: bytes) -> str:
    """
    Generate an MD5 hash for a given bytes object

    Args:
        data: the input data in bytes

    Returns:
        A hexadecimal MD5 hash string
    """
    md5_hash = md5()
    for i in range(0, len(data), 4096):
        md5_hash.update(data[i:i+4096])
    return md5_hash.hexdigest()

@grepr_dataclass(grepr_fields=["length", "hash"])
class ContentFingerprint:
    """
    Represents the fingerprint of string content. Stores length and hash for fast and efficient comparison. 
    """
    
    length: int
    hash: str
    
    @staticmethod
    def hash_value(value: str) -> bytes:
        """
        Hash a value with the chosen hash algorithm (sha256 here)
        
        Args:
            value: the string to hash
        """
        return sha256(value.encode()).hexdigest()
    
    @classmethod
    def from_value(cls, value: str) -> "ContentFingerprint":
        """
        Create the fingerprint of the given value
        
        Args:
            value: the value the created fingerprint will represent
        """
        return cls(
            length=len(value),
            hash=cls.hash_value(value),
        )
    
    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "ContentFingerprint":
        """
        Deserialize the figerprint from JSON
        
        Args:
            data: the json data
        """
        return cls(
            length = data["length"],
            hash   = data["hash"  ],
        )        
    
    def matches(self, value: str) -> bool:
        """
        Return True if the given value has the same length and hash
        
        Args:
            value: the value to compare to
        """
        if len(value) != self.length:
            return False
        if ContentFingerprint.hash_value(value) != self.hash:
            return False
        return True
    
    def to_json(self) -> dict[str, Any]:
        """
        Serialize the figerprint to JSON
        
        """
        return {
            "length": self.length,
            "hash"  : self.hash  ,
        }

@grepr_dataclass(grepr_fields=["value"], frozen=True, unsafe_hash=True)
class ATPathAttribute:
    """
    Represents an attribute of a visit path. Immutable/Frozen and Hashable.
    """
    value: str

@grepr_dataclass(grepr_fields=["value"], frozen=True, unsafe_hash=True)
class ATPathIndexOrKey:
    """
    Represents an index or key of a visit path. Immutable/Frozen and Hashable.
    """
    value: str

@grepr_dataclass(grepr_fields=[], frozen=True, unsafe_hash=True, init=False, repr=False)
class AbstractTreePath:
    """
    Represents a visit path inside an Abstract Object Tree. Immutable/Frozen and Hashable.
    """
    path: tuple[ATPathAttribute | ATPathIndexOrKey, ...] = field(default_factory=tuple)
    
    @enforce_argument_types
    def __init__(self, path: Iterable[ATPathAttribute | ATPathIndexOrKey] = tuple()) -> None:
        self.__dict__["path"] = tuple(path)
    
    def copy(self) -> "AbstractTreePath":
        return self.__copy__()
    
    def __copy__(self) -> "AbstractTreePath":
        return AbstractTreePath(copy(self.path))
    
    @enforce_argument_types
    def add_attribute(self, attr: str) -> "AbstractTreePath":
        """
        Adds an attribute to the path. Returns a new instance.
        """
        return AbstractTreePath(self.path + (ATPathAttribute(attr),))

    @enforce_argument_types
    def add_index_or_key(self, index_or_key: int | str | Any) -> "AbstractTreePath":
        """
        Adds an index or key to the path. Returns a new instance.
        """
        return AbstractTreePath(self.path + (ATPathIndexOrKey(index_or_key),))
    
    @enforce_argument_types
    def extend(self, other: "AbstractTreePath") -> "AbstractTreePath":
        """
        Extend the path by another path. Returns a new instance.
        """
        return AbstractTreePath(self.path + other.path)
    
    @enforce_argument_types
    def go_up(self, n: int = 1) -> "AbstractTreePath":
        """
        Removes the last `n` elements. Returns a new instance.
        """
        return self[:-n]
    
    @enforce_argument_types
    def index(self, value: ATPathAttribute | ATPathIndexOrKey) -> int:
        """
        Find the index of an attribute, index or key.
        """
        return self.path.index(value)
    
    def __len__(self) -> int:
        return len(self.path)
    
    def __iter__(self) -> Iterator[ATPathAttribute | ATPathIndexOrKey]:
        return iter(self.path)
    
    @overload
    def __getitem__(self, i: SupportsIndex, /) -> ATPathAttribute | ATPathIndexOrKey: ...
    @overload
    def __getitem__(self, i: slice, /) -> "AbstractTreePath": ...
    @enforce_argument_types
    def __getitem__(self, i: SupportsIndex | slice, /) -> "ATPathAttribute | ATPathIndexOrKey | AbstractTreePath":
        if isinstance(i, slice):
            new_path = self.path.__getitem__(i)
            return AbstractTreePath(new_path)
        else:
            return self.path.__getitem__(i)
    
    @enforce_argument_types
    def __add__(self, other: "AbstractTreePath") -> "AbstractTreePath":
        return self.extend(other)
    
    @enforce_argument_types
    def __contains__(self, value: ATPathAttribute | ATPathIndexOrKey) -> bool:
        return value in self.path
    
    def __reversed__(self) -> Iterator[ATPathAttribute | ATPathIndexOrKey]:
        return reversed(self.path)
        
    def __repr__(self) -> str:
        path_string = ""
        for item in self.path:
            if   isinstance(item, ATPathAttribute):
                path_string += f".{item.value}"
            elif isinstance(item, ATPathIndexOrKey):
                path_string += f"[{item.value!r}]"
        return f"{type(self).__name__}({path_string})"

class NotSetType:
    """
    An empty placeholder
    """

    def __repr__(self):
        return "NotSet"

NotSet = NotSetType()

__all__ = [
    "remove_duplicates", "get_closest_matches", "tuplify", "listify", "gdumps",
    "string_to_sha256", "number_to_token", "generate_md5", "ContentFingerprint",
    "ATPathAttribute", "ATPathIndexOrKey", "AbstractTreePath", "NotSetType", "NotSet",
]

