from __future__      import annotations
from dataclasses     import dataclass, fields as get_fields, field as base_field, MISSING
from types           import MappingProxyType
from typing          import Any, NoReturn, Callable


from pmp_manip.utility.data import AbstractTreePath, NotSetType, NotSet
from pmp_manip.utility.repr import grepr


def field(*,
        default: Any | NotSetType = NotSet, default_factory: Callable | NotSetType = NotSet, 
        init: bool = True, repr: bool = True, hash: bool | NotSetType = NotSet, compare: bool = True,
        metadata: MappingProxyType | NotSetType = NotSet, kw_only: bool | NotSetType = NotSet,
    ):
    if default is NotSet: default = MISSING
    if default_factory is NotSet: default_factory = MISSING
    if hash is NotSet: hash = None
    if metadata is NotSet: metadata = None
    if kw_only is NotSet: kw_only = MISSING
    
    base_field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        kw_only=kw_only,
    )
        


def grepr_dataclass(*, repr: bool = True,
        init: bool = True, eq: bool = True, order: bool = True, 
        unsafe_hash: bool = False, frozen: bool = False, 
        match_args: bool = True, kw_only: bool = False, 
        slots: bool = False, weakref_slot: bool = False,
        forbid_init_only_subcls: bool = False,
        validate: bool = False,
    ):
    """
    A decorator which combines @dataclass and a good representation system.
    Args:
        init...: dataclass parameters (except for order which is True by default here)
        forbid_init_only_subcls: add a __init__ method to raises a NotImplementedError, which tells the user to use it's subclasses.
        validate: add a validate method which ensures instance field values match type annotations and validation configuration.
    """
    if init: assert not forbid_init_only_subcls

    def decorator[T](cls: T) -> T:
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
        
        if repr:
            cls.__repr__ = grepr
            cls.__has_grepr__ = True

        cls = dataclass(cls, 
            init=init, repr=False, eq=eq,
            order=order, unsafe_hash=unsafe_hash, frozen=frozen,
            match_args=match_args, kw_only=kw_only,
            slots=slots, weakref_slot=weakref_slot,
        )
        
        if validate:
            def validate_method(self, path: AbstractTreePath = AbstractTreePath(), *args, **kwargs) -> None:
                for field in get_fields(self):
                    pass
                if callable(getattr(self, "post_validate", None)):
                    self.post_validate(path, *args, **kwargs)
            cls.validate = validate_method
            cls.__has_validate__ = True
        
        return cls
    return decorator


__all__ = ["grepr_dataclass"]

