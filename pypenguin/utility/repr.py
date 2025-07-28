from aenum       import Enum
from copy        import copy
from dataclasses import dataclass
from typing      import Any

from pypenguin.utility.dual_key_dict import DualKeyDict


class KeyReprDict(dict):
    """
    Behaves exactly like butilins.dict, only the repr method is different. It only shows keys and not values of the dictionary.
    """
    
    def __repr__(self) -> str:
        return grepr(self)

def grepr(obj, /, safe_dkd=False, level_offset=0, annotate_fields=True, include_attributes=False, *, indent=4) -> str:
    def _is_dict(obj):
        return isinstance(obj, dict) and not isinstance(obj, KeyReprDict)
    
    def _grepr(obj, level=level_offset) -> tuple[str, bool]:
        is_compatible = bool(getattr(obj, "_grepr", False))
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
            strings = [_grepr(x, level)[0] for x in obj]
            if len(obj) > 2 and (max(len(s) for s in strings) > 10):
                return f"{opening}{prefix}{sep.join(strings)}{end_sep}{closing}", False
            else:
                return f"{opening}{", ".join(strings)}{closing}", True
        
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
            return f'"{obj.replace('"', '\\"')}"', True
        
        # TODO: add compatability with bytes objects
        
        elif is_compatible:
            args = []
            allsimple = True
            for name in obj._grepr_fields:
                if not hasattr(obj, name):
                    continue
                value = getattr(obj, name)
                value, simple = _grepr(value, level)
                allsimple = allsimple and simple
                if annotate_fields:
                    args.append(f"{name}={value}")
                else:
                    args.append(value)
            class_name = obj.__class__.__name__
            if allsimple and len(args) <= 3:
                return f"{class_name}({", ".join(args)})", not args
            return f"{class_name}({prefix}{sep.join(args)}{end_sep})", False
        return repr(obj), True
 
    is_compatible = bool(getattr(obj, "_grepr", False))
    if is_compatible or isinstance(obj, (list, tuple, set, DualKeyDict, dict, str)):
        if indent is not None and not isinstance(indent, str):
            indent = " " * indent
        return _grepr(obj)[0]
    return repr(obj)

def grepr_dataclass(*, grepr_fields: list[str],
        init: bool = True, eq: bool = True, order: bool = False, 
        unsafe_hash: bool = False, frozen: bool = False, 
        match_args: bool = True, kw_only: bool = False, 
        slots: bool = False, weakref_slot: bool = False,
    ):
    """
    A decorator which combines @dataclass and a good representation system.
    Args:
        grepr_fields: fields for the good repr implementation
        parent_cls: class whose fields will also be included in the good repr impletementation
        init...: dataclass parameters
    """
    def decorator(cls: type):
        def __repr__(self) -> str:
            return grepr(self)
        cls.__repr__ = __repr__
        cls._grepr = True
        nonlocal grepr_fields
        fields = copy(grepr_fields)
        for base in cls.__bases__:
            if not getattr(base, "_grepr", False): continue
            for field in base._grepr_fields:
                if field in fields: continue
                fields.append(field)
        cls._grepr_fields = fields
        cls = dataclass(cls, 
            init=init, repr=False, eq=eq,
            order=order, unsafe_hash=unsafe_hash, frozen=frozen,
            match_args=match_args, kw_only=kw_only,
            slots=slots, weakref_slot=weakref_slot,
        )
        return cls
    return decorator

class PypenguinEnum(Enum):
    name: str
    value: Any

    def __repr__(self) -> str:
        return self.__class__.__name__ + "." + self.name

def repr_tree(node, source_code, indent=0): # TODO: reconsider
    """Nicely formatted repr of a tree-sitter node and its children."""
    indent_str = "  " * indent
    node_type = node.type

    if node.child_count == 0:
        text = source_code[node.start_byte:node.end_byte].decode("utf8")
        return f"{indent_str}{node_type} ({repr(text)})"

    lines = [f"{indent_str}{node_type}:"]
    for child in node.children:
        lines.append(repr_tree(child, source_code, indent + 1))
    return "\n".join(lines)


__all__ = ["KeyReprDict", "grepr", "grepr_dataclass", "PypenguinEnum", "repr_tree"]

