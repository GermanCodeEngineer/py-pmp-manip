from __future__  import annotations
from copy        import copy
from dataclasses import dataclass, fields as get_fields, field as base_field, Field, MISSING, _MISSING_TYPE
from types       import MappingProxyType, NoneType
from typing      import (
    Any, NoReturn, Callable, Iterable, Iterator, SupportsIndex, Any, Protocol,
    overload, get_type_hints, dataclass_transform, TYPE_CHECKING,
)


VALIDATOR_FN = Callable | NoneType # TODO

FIELD_OPTIONS: dict[Field, dict[str, Any]] = {}

def field(*,
        default: Any | _MISSING_TYPE = MISSING, default_factory: Callable[[], Any] | _MISSING_TYPE = MISSING, 
        init: bool = True, grepr: bool = True, hash: bool | NoneType = None, compare: bool = True,
        metadata: MappingProxyType | NoneType = None, kw_only: bool | _MISSING_TYPE = MISSING,

        validate_type: bool = True, validator_fn: VALIDATOR_FN = None,
        validate_require_exist: bool = True, call_subvalidate: bool = False,
    ) -> Field:
    """
    Create a dataclass field with extended validation and representation options.
    
    Wraps the standard dataclass field with additional options:
    - `grepr`: Whether to include in grepr representation
    - `validate_type`: Whether to enforce type checking on this field
    - `validator_fn`: Custom validation function
    - `validate_require_exist`: Whether field must exist during validation
    - `call_subvalidate`: Whether to call validate() method on field values
    
    Raises:
        ValueError: if validator_fn is provided but not callable
    """
    field = base_field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=False,
        hash=hash,
        compare=compare,
        metadata=metadata,
        kw_only=kw_only,
    )
    if (validator_fn is not None) and (not callable(validator_fn)):
        raise ValueError("validator_fn must be a function or callable")
    update_field(field, grepr, validate_type, validator_fn, validate_require_exist, call_subvalidate)
    return field

def update_field(field: Field,
        grepr: bool = True,
        validate_type: bool = True, validator_fn: VALIDATOR_FN = None,
        validate_require_exist: bool = True, call_subvalidate: bool = False,
    ) -> None:
    """Store custom field options for use by @grepr_dataclass validation and representation."""
    if field not in FIELD_OPTIONS:
        FIELD_OPTIONS[field] = dict(
            grepr=grepr,
            validate_type=validate_type,
            validator_fn=validator_fn,
            validate_require_exist=validate_require_exist,
            call_subvalidate=call_subvalidate,
        )

def get_field_options(field: Field) -> dict[str, Any]:
    """Retrieve custom options for a field, ensuring they are registered if not present."""
    update_field(field)
    return FIELD_OPTIONS[field]

@dataclass_transform(
    eq_default = True,
    order_default = True,
    kw_only_default = False,
    frozen_default = False,
    field_specifiers = (field,),
)
def grepr_dataclass(*, grepr: bool = True,
        init: bool = True, eq: bool = True, order: bool = True, 
        unsafe_hash: bool = False, frozen: bool = False, 
        match_args: bool = True, kw_only: bool = False, 
        slots: bool = False, weakref_slot: bool = False,
        forbid_init_only_subcls: bool = False,
        validate: bool = True,
    ):
    """
    A decorator which combines @dataclass and a good representation system.
    Args:
        init...: dataclass parameters (except for order which is True by default here)
        forbid_init_only_subcls: add a __init__ method to raises a NotImplementedError, which tells the user to use it"s subclasses.
        validate: add a validate method which ensures instance field values match type annotations and validation configuration.
    """
    if init: assert not forbid_init_only_subcls

    def decorator[T](cls: T) -> T:
        cls = dataclass(cls, 
            init=init, repr=False, eq=eq,
            order=order, unsafe_hash=unsafe_hash, frozen=frozen,
            match_args=match_args, kw_only=kw_only,
            slots=slots, weakref_slot=weakref_slot,
        )
        for field in get_fields(cls):
            update_field(field)

        if forbid_init_only_subcls:
            def __init__(self, *args, **kwargs) -> None | NoReturn:
                if type(self) is cls:
                    msg = f"Can not initialize parent class {cls!r} directly. Please use the subclasses"
                    suggested_subcls_names = [cls.__name__ for cls in cls.__subclasses__()]
                    if suggested_subcls_names:
                        msg += " "
                        msg += ", ".join(suggested_subcls_names)
                    msg += "."
                    raise NotImplementedError(msg)
            cls.__init__ = __init__
        
        if grepr:
            def grepr_wrapper(self, *args, **kwargs) -> str:
                from gceutils.repr import grepr
                return grepr(self, *args, **kwargs)
            cls.__repr__ = grepr_wrapper
            cls.__has_grepr__ = True
        
        if validate:
            def validate_method(self, path: AbstractTreePath | None = None, *args, **kwargs) -> None:
                from gceutils.decorators import enforce_type
                if path is None:
                    path = AbstractTreePath(start_with_dot=True)

                # Get type hints to resolve string annotations
                type_hints = get_type_hints(type(self))
                
                for field in get_fields(self):
                    options = get_field_options(field)
                    if not options["validate_type"]:
                        continue
                    # Use type hints instead of field.type to handle string annotations
                    expected_type = type_hints.get(field.name, field.type)
                    if hasattr(self, field.name):
                        enforce_type(
                            value=getattr(self, field.name),
                            expected=expected_type,
                            path=path.add_attribute(field.name),
                            notset_as_special=False,
                        )
                    elif options["validate_require_exist"]:
                        enforce_type(
                            value=NotSet,
                            expected=expected_type,
                            path=path.add_attribute(field.name),
                            notset_as_special=True,
                        )
                
                for field in get_fields(self):
                    options = get_field_options(field)
                    if not options["call_subvalidate"]:
                        continue
                    field_value = getattr(self, field.name, None)
                    if callable(getattr(field_value, "validate", None)):
                        field_value.validate(path.add_attribute(field.name), *args, **kwargs)
                
                if callable(getattr(self, "post_validate", None)):
                    self.post_validate(path, *args, **kwargs)
            cls.validate = validate_method
            cls.__has_validate__ = True
            
            # Remove "validate" from abstract methods if present (for ABC compatibility)
            if hasattr(cls, "__abstractmethods__"):
                abstractmethods = set(cls.__abstractmethods__)
                abstractmethods.discard('validate')
                cls.__abstractmethods__ = frozenset(abstractmethods)
        
        return cls
    return decorator

class HasGreprValidate(Protocol):
    """
    Protocol to represent effects of @grepr_dataclass with `grepr=True` and `validate=true`.
    """

    # Needs to be synced with arguments of grepr
    def __repr__(self, /,
        safe_dkd:bool=False, level_offset:int=0, annotate_fields:bool=True,
        vanilla_strings:bool=False, *, indent:int|str|None=4,
    ) -> str:
        """
        Represent a dataclass in a way inspired by ast.dumps using `grepr`.
        """
        # Overriden by @grepr_dataclass
    
    def validate(self, path: AbstractTreePath | None = None, *args, **kwargs) -> None:
        """
        Validate a dataclass.
        First ensures all fields (which do not have `validate_type=False`) to be of the annotated type.
        Second calls and returns the return value of the `post_validate` method with `*args` and `**kwargs` if the class has one.
        
        Raises:
            TypeValidationError(ValidationError): if a field does not match the annotated type.
            Other Errors(subclasses of ValidationError): possibly raised in `post_validate`.
        """
        # Overriden by @grepr_dataclass

class NotSetType:
    """
    An empty placeholder
    """

    def __repr__(self) -> str:
        return "NotSet"

    def __bool__(self) -> bool:
        return False

NotSet = NotSetType()

@grepr_dataclass(frozen=True, unsafe_hash=True)
class ATPathAttribute(HasGreprValidate):
    """
    Represents an attribute of a visit path. Immutable/Frozen and Hashable.
    """
    value: str

@grepr_dataclass(frozen=True, unsafe_hash=True)
class ATPathIndexOrKey(HasGreprValidate):
    """
    Represents an index or key of a visit path. Immutable/Frozen and Hashable.
    """
    value: str

@grepr_dataclass(frozen=True, unsafe_hash=True, init=False, grepr=False)
class AbstractTreePath(HasGreprValidate):
    """
    Represents a visit path inside an Abstract Object Tree. Immutable/Frozen and Hashable.
    """
    path: tuple[ATPathAttribute | ATPathIndexOrKey, ...] = field(default_factory=tuple)
    start_with_dot: bool = True

    def __init__(self, path: Iterable[ATPathAttribute | ATPathIndexOrKey] = tuple(), start_with_dot: bool = True) -> None:
        try:
            iter(path)
        except TypeError:
            raise ValueError("path must be an iterable of ATPathAttribute or ATPathIndexOrKey items")
        if not all(isinstance(item, (ATPathAttribute, ATPathIndexOrKey)) for item in path):
            raise ValueError("path must be an iterable of ATPathAttribute or ATPathIndexOrKey items")
        self.__dict__["path"] = tuple(path)
        self.__dict__["start_with_dot"] = start_with_dot
    
    def copy(self) -> AbstractTreePath:
        return self.__copy__()
    
    def __copy__(self) -> AbstractTreePath:
        return AbstractTreePath(copy(self.path), start_with_dot=self.start_with_dot)
    
    def add_attribute(self, attr: str) -> AbstractTreePath:
        """
        Adds an attribute to the path. Returns a new instance.
        """
        if not isinstance(attr, str):
            raise ValueError("attr must be a string")
        return AbstractTreePath(self.path + (ATPathAttribute(attr),), start_with_dot=self.start_with_dot)

    def add_index_or_key(self, index_or_key: int | str | Any) -> AbstractTreePath:
        """
        Adds an index or key to the path. Returns a new instance.
        """
        return AbstractTreePath(self.path + (ATPathIndexOrKey(index_or_key),), start_with_dot=self.start_with_dot)
    
    def extend(self, other: AbstractTreePath) -> AbstractTreePath:
        """
        Extend the path by another path. Returns a new instance.
        """
        if not isinstance(other, AbstractTreePath):
            raise ValueError("first argument must be an AbstractTreePath")
        return AbstractTreePath(self.path + other.path, start_with_dot=self.start_with_dot)
    
    def go_up(self, n: int = 1) -> AbstractTreePath:
        """
        Removes the last `n` elements. Returns a new instance.
        """
        if not isinstance(n, int):
            raise ValueError("n must be a int")
        return self[:-n]
    
    def index(self, value: ATPathAttribute | ATPathIndexOrKey) -> int:
        """
        Find the index of an attribute, index or key.
        """
        if not isinstance(value, (ATPathAttribute, ATPathIndexOrKey)):
            raise ValueError("value must be an ATPathAttribute or ATPathIndexOrKey")
        return self.path.index(value)
    
    def __len__(self) -> int:
        return len(self.path)
    
    def __iter__(self) -> Iterator[ATPathAttribute | ATPathIndexOrKey]:
        return iter(self.path)
    
    @overload
    def __getitem__(self, i: SupportsIndex, /) -> ATPathAttribute | ATPathIndexOrKey: ...
    @overload
    def __getitem__(self, i: slice, /) -> AbstractTreePath: ...
    def __getitem__(self, i: SupportsIndex | slice, /) -> ATPathAttribute | ATPathIndexOrKey | AbstractTreePath:
        if not isinstance(i, (SupportsIndex, slice)):
            raise ValueError("first argument must be an index or slice")
        if isinstance(i, slice):
            new_path = self.path.__getitem__(i)
            return AbstractTreePath(new_path, start_with_dot=self.start_with_dot)
        else:
            return self.path.__getitem__(i)
    
    def __add__(self, other: AbstractTreePath, /) -> AbstractTreePath:
        if not isinstance(other, AbstractTreePath):
            raise ValueError("first argument must be an AbstractTreePath")
        return self.extend(other)
    
    def __contains__(self, value: ATPathAttribute | ATPathIndexOrKey) -> bool:
        if not isinstance(value, (ATPathAttribute, ATPathIndexOrKey)):
            raise ValueError("first argument must be an ATPathAttribute or ATPathIndexOrKey")
        return value in self.path
    
    def __reversed__(self) -> Iterator[ATPathAttribute | ATPathIndexOrKey]:
        return reversed(self.path)
        
    def repr_as_python_code(self) -> str:
        path_string = ""
        for item in self.path:
            if   isinstance(item, ATPathAttribute):
                path_string += f".{item.value}"
            elif isinstance(item, ATPathIndexOrKey):
                path_string += f"[{item.value!r}]"
        if not self.start_with_dot:
            path_string = path_string.removeprefix(".")
            # Removes if at the start, else does nothing
        return path_string
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.repr_as_python_code()})"
    
    @overload
    def get_in_tree(self, tree: Any, default: NotSetType = NotSet) -> Any: ...
    @overload
    def get_in_tree[DEFAULT_T](self, tree: Any, default: DEFAULT_T) -> Any | DEFAULT_T: ...
    def get_in_tree[DEFAULT_T](self, tree: Any, default: NotSetType | DEFAULT_T = NotSet) -> Any | DEFAULT_T:
        """
        Dynamically get a node in an arbitrary object tree by this path.
        """
        current_object = tree
        for i, item in enumerate(self):
            if   isinstance(item, ATPathAttribute):
                if isinstance(current_object, dict) and (item.value == "keys()"):
                    # keys can only be accessed with d.keys()[key_index] not d[key]
                    current_object = list(current_object.keys())
                    continue
                try:
                    current_object = getattr(current_object, item.value)
                except (AttributeError, TypeError, Exception) as error:
                    if default is NotSet:
                        raise ValueError(f"Failed to get attribute {item.value!r} of object at path {self[:i]}: {error}") from error
                    return default
            elif isinstance(item, ATPathIndexOrKey):
                try:
                    current_object = current_object[item.value]
                except (IndexError, KeyError, TypeError, Exception) as error:
                    if default is NotSet:
                        raise ValueError(f"Failed to get index or key {item.value!r} of object at path {self[:i]}: {error}") from error
                    return default
        return current_object

    def exists_in_tree(self, tree: Any) -> bool:
        """
        Checks if this path is accessible in an arbitrary object tree.
        """
        try:
            self.get_in_tree(tree)
            return True
        except ValueError:
            return False

    def set_in_tree(self, tree: Any, value: Any) -> None:
        """
        Dynamically set a node in an arbitrary object tree by this path to a value.
        """
        obj = self[:-1].get_in_tree(tree)
        path_item = self[-1]
        if   isinstance(path_item, ATPathAttribute):
            try:
                setattr(obj, path_item.value, value)
            except (AttributeError, TypeError) as error:
                raise type(error)(f"Failed to set attribute {path_item.value!r} of object at path {self}: {error}") from error
        elif isinstance(path_item, ATPathIndexOrKey):
            try:
                obj[path_item.value] = value
            except (IndexError, TypeError) as error:
                raise type(error)(f"Failed to set index or key {path_item.value!r} of object at path {self}: {error}") from error


__all__ = [
    "field", "update_field", "grepr_dataclass", "HasGreprValidate",
    "ATPathAttribute", "ATPathIndexOrKey", "AbstractTreePath",
    "NotSetType", "NotSet",
]

