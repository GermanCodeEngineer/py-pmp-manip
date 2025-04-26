from typing import Any, TYPE_CHECKING

from utility import GreprClass, PypenguinEnum
from utility import AA_TYPE, AA_JSON_COMPATIBLE, InvalidDropdownValueError

from core.context import PartialContext

if TYPE_CHECKING:
    from core.block import SRInputValue
    from opcode_info import DropdownType

class SRDropdownKind(PypenguinEnum):
    STANDARD       =  0
    VARIABLE       =  1
    LIST           =  2
    BROADCAST_MSG  =  3
    
    STAGE          =  4
    SPRITE         =  5
    MYSELF         =  6
    OBJECT         =  7

    COSTUME        =  8
    BACKDROP       =  9
    SOUND          = 10
    
    FONT           = 11
    SUGGESTED_FONT = 12

    FALLBACK       = 13

@dataclass
class SRDropdownValue(GreprClass):
    _grepr = True
    _grepr_fields = ["kind", "value"]

    kind: SRDropdownKind
    value: Any
    
    def __eq__(self, other) -> bool:
        if isinstance(other, tuple) and (len(other) == 2):
            if (other[0] == self.kind.name) and (other[1] == self.value):
                return True
        return super().__eq__(other)

    def validate(self, path: list) -> None:
        AA_TYPE(self, path, "kind", SRDropdownKind)
        AA_JSON_COMPATIBLE(self, path, "value")
    
    def validate_kind(self, path, kind, message=None) -> None:
        if self.kind != kind:
            if message == None:
                message = f"In this case kind of {self.__class__.__name__} must be {repr(kind)}"
            raise InvalidDropdownValueError(path, message)
    
    def validate_value(self, path: list, dropdown_type: "DropdownType", context: PartialContext, inputs: dict[str, "SRInputValue"]) -> None:
        def make_string(possible_values):
            return (
                "No possible values." if possible_values == [] else
                "".join(["\n- "+repr(value) for value in possible_values])
            )
        
        from opcode_info import DropdownType
        # TODO: get rid of these special cases
        match dropdown_type:
            case DropdownType.BROADCAST:
                self.validate_kind(path, SRDropdownKind.BROADCAST_MSG)
            case DropdownType.VARIABLE:
                possible_values_string = make_string(context.scope_variables)
                if self not in context.scope_variables:
                    raise InvalidDropdownValueError(path, f"Must be a defined variable. In this case one of these: {possible_values_string}")
            case DropdownType.LIST:
                possible_values_string = make_string(context.scope_lists)
                if self not in context.scope_lists:
                    raise InvalidDropdownValueError(path, f"Must be a defined list. In this case one of these: {possible_values_string}")
            case _:
                possible_values = dropdown_type.calculate_possible_new_dropdown_values(
                    context = context,
                    inputs  = inputs,
                )
                default_kind = dropdown_type.get_default_kind()
                possible_values_string = make_string(possible_values)
                if self not in possible_values:
                    if default_kind is None:
                        raise InvalidDropdownValueError(path, f"In this case must be one of these: {possible_values_string}")
                    else:
                        self.validate_kind(path, default_kind, message=f"If kind is not {default_kind} must be on of these: {possible_values_string}")



