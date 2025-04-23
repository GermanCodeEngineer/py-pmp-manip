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
        elif isinstance(obj, dict):
            if not obj:
                return '{}', True
            args = [f'{_format(key, level)[0]}: {_format(value, level)[0]}' for key,value in obj.copy().items()]    
            short = '{%s}' % (", ".join(args),)
            return '{%s%s}' % (prefix, sep.join(args)), False
        elif is_compatible:
            cls = type(obj)
            args = []
            allsimple = True
            keywords = annotate_fields
            for name in obj._grepr_fields:
                try:
                    value = getattr(obj, name)
                except AttributeError:
                    keywords = True
                    continue
                if value is None and getattr(cls, name, ...) is None:
                    keywords = True
                    continue
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


def gprint(*objects, sep=" ", end="\n"):
    print(
        *(grepr(obj) for obj in objects),
        sep=sep,
        end=end,
    )



# Files
import zipfile
import os
from .errors import PathError

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

class PypenguinClass:
    def __eq__(self, other) -> bool:
        if not getattr(self, "_grepr", False):
            return NotImplemented
        if type(self) != type(other):
            return False
        for field in self._grepr_fields:
            if getattr(self, field) != getattr(other, field):
                return False 
        return True

class PypenguinEnum(Enum):
    def __repr__(self):
        return self.__class__.__name__ + "." + self.name

# Data Functions

def remove_duplicates(items: list):
    seen = []
    result = []
    for item in items:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result
