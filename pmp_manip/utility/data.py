from difflib import SequenceMatcher
from hashlib import sha256, md5
from json    import dumps
from typing  import Any

from pmp_manip.utility.decorators import grepr_dataclass


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

def string_to_sha256(primary: str, secondary: str|None=None, tertiary: str|None=None) -> str:
    def _string_to_sha256(input_string: str, digits: int) -> str:
        hex_hash = sha256(input_string.encode()).hexdigest()

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
    "NotSetType", "NotSet",
]

