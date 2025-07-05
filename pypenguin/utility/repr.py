from copy        import copy
from dataclasses import dataclass
from enum        import Enum

from pypenguin.utility.dual_key_dict import DualKeyDict


class KeyReprDict(dict):
    """
    Behaves exactly like butilins.dict, only the repr method is different. It only shows keys and not values of the dictionary.
    """
    def __repr__(self):
        keys = ", ".join(repr(key) for key in self.keys())
        return f"{self.__class__.__name__}(keys={{{keys}}})"

def grepr(obj, /, annotate_fields=True, include_attributes=False, *, indent=4):
    def _is_dict(obj):
        return isinstance(obj, dict) and not isinstance(obj, KeyReprDict)
    
    def _grepr(obj, level=0):
        is_compatible = bool(getattr(obj, "_grepr", False))
        if indent is not None:
            level += 1
            prefix = '\n' + indent * level
            sep = ',\n' + indent * level
            end_sep = ',\n' + indent * (level-1)
        else:
            prefix = ''
            sep = ', '
            end_sep = ""
        if isinstance(obj, list):
            if not obj:
                return '[]', True
            return '[%s%s%s]' % (prefix, sep.join(_grepr(x, level)[0] for x in obj), end_sep), False
        if isinstance(obj, tuple):
            if not obj:
                return '()', True
            if len(obj) <= 2:
                return '(%s)' % (", ".join(_grepr(x, level)[0] for x in obj)), False
            else:
                return '(%s%s%s)' % (prefix, sep.join(_grepr(x, level)[0] for x in obj), end_sep), False
        elif _is_dict(obj):
            if not obj:
                return '{}', True
            args = [f'{_grepr(key, level)[0]}: {_grepr(value, level)[0]}' for key,value in obj.copy().items()]    
            return '{%s%s%s}' % (prefix, sep.join(args), end_sep), False
        elif isinstance(obj, str):
            return f'"{obj.replace('"', '\\"')}"', True
        elif isinstance(obj, DualKeyDict):
            if not obj:
                return 'DualKeyDict{}', True
            args = []
            for key1, key2, value in obj.items_key1_key2():
                key1_str, _ = _grepr(key1, level)
                key2_str, _ = _grepr(key2, level)
                value_str, _ = _grepr(value, level)
                args.append(f'{key1_str} / {key2_str}: {value_str}')
            return 'DualKeyDict{%s%s%s}' % (prefix, sep.join(args), end_sep), False
        elif is_compatible:
            cls = type(obj)
            args = []
            allsimple = True
            for name in obj._grepr_fields:
                if not hasattr(obj, name):
                    continue
                value = getattr(obj, name)
                value, simple = _grepr(value, level)
                allsimple = allsimple and simple
                if annotate_fields:
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
                    value, simple = _grepr(value, level)
                    allsimple = allsimple and simple
                    args.append('%s=%s' % (name, value))
            class_name = getattr(obj, "_grepr_class_name", obj.__class__.__name__)
            if allsimple and len(args) <= 3:
                return '%s(%s)' % (class_name, ', '.join(args)), not args
            return '%s(%s%s%s)' % (class_name, prefix, sep.join(args), end_sep), False
        return repr(obj), True
 
    is_compatible = bool(getattr(obj, "_grepr", False))
    if not(is_compatible) and not(isinstance(obj, (list, tuple, str, DualKeyDict)) or _is_dict(obj)):
        return repr(obj)
    if indent is not None and not isinstance(indent, str):
        indent = ' ' * indent
    return _grepr(obj)[0]

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
    def __repr__(self) -> str:
        return self.__class__.__name__ + "." + self.name


__all__ = ["KeyReprDict", "grepr", "grepr_dataclass", "PypenguinEnum"]

