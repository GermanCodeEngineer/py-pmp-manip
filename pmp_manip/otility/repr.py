from __future__  import annotations
from dataclasses import fields
from enum        import Enum
from typing      import Any

from gceutils.dual_key_dict import DualKeyDict


class KeyReprDict(dict):
    """Dict subclass that displays only its keys in repr, not values. Inherits all dict functionality."""
    
    def __repr__(self) -> str:
        return grepr(self)

def grepr(obj, /,
        safe_dkd:bool=False, level_offset:int=0, annotate_fields:bool=True,
        vanilla_strings:bool=False, *, indent:int|str|None=4,
    ) -> str:
    """
    Generate a custom string representation of an object with enhanced formatting.
    
    Provides pretty-printed output for dataclasses, collections, DualKeyDict, and nested structures.
    By default, dataclass fields marked with grepr=False are excluded from output.
    
    Returns:
        str: Formatted representation of the object
        
    Args:
        safe_dkd: If True, represent DualKeyDict using dict notation; otherwise use custom notation
        level_offset: Initial indentation level for nested structures
        annotate_fields: Include field names in dataclass representations
        vanilla_strings: If True, use repr() for strings; otherwise use custom quoting
        indent: Number of spaces (int) or indent string for multi-line formatting; None for single-line
    """
    from gceutils.base import get_field_options
    def _grepr(obj, level=level_offset) -> tuple[str, bool]:
        is_compatible = bool(getattr(obj, "__has_grepr__", False)) and not(isinstance(obj, type))
        if indent is not None:
            level += 1
            prefix = "\n" + indent * level
            sep = ",\n" + indent * level
            end_sep = ",\n" + indent * (level-1)
        else:
            prefix = ""
            sep = ", "
            end_sep = ""
        
        if isinstance(obj, (list, tuple, set)):
            opening, closing = (
                     ("[", "]") if isinstance(obj, list) 
                else ("(", ")") if isinstance(obj, tuple)
                else ("{", "}")
            )
            
            if not obj:
                return f"{opening}{closing}", True
            
            strings = []
            allsimple = True
            for i, item in enumerate(obj):
                item_s, simple = _grepr(item, level)
                allsimple = allsimple and simple and (len(item_s) <= 40)
                strings.append(item_s)

            if allsimple:
                return f"{opening}{", ".join(strings)}{closing}", True
            else:
                return f"{opening}{prefix}{sep.join(strings)}{end_sep}{closing}", False
        
        elif isinstance(obj, DualKeyDict):
            if not obj:
                return ("DualKeyDict()" if safe_dkd else "DualKeyDict{}"), True
            args = []
            for key1, key2, value in obj.items_key1_key2():
                key1_str, _ = _grepr(key1, level)
                key2_str, _ = _grepr(key2, level)
                value_str, _ = _grepr(value, level)
                args.append((key1_str, key2_str, value_str))
            if safe_dkd:
                strings = [f"({key1_str}, {key2_str}): {value_str}" for key1_str, key2_str, value_str in args]
                fmt = "DualKeyDict({%s})"
            else:
                strings = [f"{key1_str} / {key2_str}: {value_str}" for key1_str, key2_str, value_str in args]
                fmt = "DualKeyDict{%s}"
            return fmt % f"{prefix}{sep.join(strings)}{end_sep}", False
        
        elif isinstance(obj, KeyReprDict): # must come before isinstance(obj, dict)
            keys_str, is_simple = _grepr(tuple(obj.keys()), level-1)
            keys_str = "{" + keys_str.removeprefix("(").removesuffix(")") + "}"
            # Above: Avoid loss of key order
            return f"KeyReprDict(keys={keys_str})", is_simple
        
        elif isinstance(obj, dict):
            if not obj:
                return "{}", True
            args = [f"{_grepr(key, level)[0]}: {_grepr(value, level)[0]}" for key,value in obj.items()]    
            return "{" + f"{prefix}{sep.join(args)}{end_sep}" + "}", False
         
        elif isinstance(obj, str):
            if vanilla_strings:
                return repr(obj), True
            
            obj = obj.replace("\\", "\\\\")
            if '"' in obj:
                if "'" in obj:
                    return f'"{obj.replace('"', '\\"')}"', True
                else:
                    return f"'{obj}'", True
            else:
                return f'"{obj}"', True
        
        # TODO: add compatability with bytes objects
        
        elif is_compatible:
            args = []
            allsimple = True
            for field in fields(obj):
                options = get_field_options(field)
                if not options["grepr"]:
                    continue
                if not hasattr(obj, field.name):
                    continue
                value = getattr(obj, field.name)
                value, simple = _grepr(value, level)
                allsimple = allsimple and simple
                if annotate_fields:
                    args.append(f"{field.name}={value}")
                else:
                    args.append(value)
            class_name = obj.__class__.__name__
            if allsimple and len(args) <= 3:
                return f"{class_name}({", ".join(args)})", not args
            return f"{class_name}({prefix}{sep.join(args)}{end_sep})", False
        return repr(obj), True
 
    is_compatible = bool(getattr(obj, "__has_grepr__", False)) and not(isinstance(obj, type))
    if is_compatible or isinstance(obj, (list, tuple, set, DualKeyDict, dict, str)):
        if indent is not None and not isinstance(indent, str):
            indent = " " * indent
        return _grepr(obj)[0]
    return repr(obj)

class GEnum(Enum):
    """Base class for enums with enhanced repr."""
    name: str
    value: Any

    def __repr__(self) -> str:
        return self.__class__.__name__ + "." + self.name


__all__ = ["KeyReprDict", "grepr", "GEnum"]

