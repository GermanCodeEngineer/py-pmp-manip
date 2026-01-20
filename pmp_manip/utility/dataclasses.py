from __future__  import annotations
from dataclasses import dataclass, fields as get_fields, field as base_field, Field, MISSING, _MISSING_TYPE, replace
from types       import MappingProxyType, NoneType
from typing      import Any, NoReturn, Callable, TYPE_CHECKING


if TYPE_CHECKING: from pmp_manip.utility.data import AbstractTreePath
from pmp_manip.utility.decorators import enforce_argument_types
from pmp_manip.utility.repr       import grepr as good_repr


VALIDATOR_FN = Callable | NoneType # TODO

FIELD_OPTIONS = {}

@enforce_argument_types
def field(*,
        default: Any | _MISSING_TYPE = MISSING, default_factory: Callable[[], Any] | _MISSING_TYPE = MISSING, 
        init: bool = True, grepr: bool = True, hash: bool | NoneType = None, compare: bool = True,
        metadata: MappingProxyType | NoneType = None, kw_only: bool | _MISSING_TYPE = MISSING,

        validate_type: bool = True, validator_fn: VALIDATOR_FN = None,
    ) -> Field:
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
    update_field(field, grepr, validate_type, validator_fn)
    return field

def update_field(field: Field,
        grepr: bool = True, 
        validate_type: bool = True, validator_fn: VALIDATOR_FN = None,
    ) -> None:
    # Replace field metadata if needed (creates new mappingproxy)
    if field not in FIELD_OPTIONS:
        FIELD_OPTIONS[field] = {
            "grepr": grepr,
            "validate_type": validate_type,
            "validator_fn": validator_fn,
        }

def get_field_options(field: Field) -> dict[str, Any]:
    update_field(field)
    return FIELD_OPTIONS[field]

def grepr_dataclass(*, grepr: bool = True,
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
            cls.__repr__ = good_repr
            cls.__has_grepr__ = True
        
        if validate:
            def validate_method(self, path: AbstractTreePath | None = None, *args, **kwargs) -> None:
                from pmp_manip.utility.data import AbstractTreePath
                if path is None:
                    path = AbstractTreePath()
                for field in get_fields(self):
                    options = get_field_options(field)
                    if not options["validate_type"]:
                        continue
                    
                if callable(getattr(self, "post_validate", None)):
                    self.post_validate(path, *args, **kwargs)
            cls.validate = validate_method
            cls.__has_validate__ = True
        
        return cls
    return decorator


__all__ = ["field", "update_field", "grepr_dataclass"]

