from typing      import Any
from dataclasses import dataclass

from utility     import GreprClass, ValidationConfig
from utility     import AA_TYPE, AA_JSON_COMPATIBLE, InvalidDropdownValueError
from opcode_info import DropdownType, DropdownValueKind

from core.context import PartialContext


@dataclass(repr=False)
class SRDropdownValue(GreprClass):
    _grepr = True
    _grepr_fields = ["kind", "value"]

    kind: DropdownValueKind
    value: Any
    
    @classmethod
    def from_tuple(cls, data: tuple[DropdownValueKind, Any]) -> "SRDropdownValue":
        return cls(
            kind=data[0],
            value=data[1],
        )

    def validate(self, path: list, config: ValidationConfig) -> None:
        AA_TYPE(self, path, "kind", DropdownValueKind)
        AA_JSON_COMPATIBLE(self, path, "value")

    def validate_value(self, path: list, dropdown_type: "DropdownType", context: PartialContext) -> None:
        def make_string(possible_values):
            return (
                "No possible values." if possible_values == [] else
                "".join(["\n- "+repr(value) for value in possible_values])
            )
        
        possible_values = dropdown_type.calculate_possible_new_dropdown_values(context = context)
        default_kind = dropdown_type.get_default_kind()
        possible_values_string = make_string(possible_values)
        if (self.kind, self.value) not in possible_values:
            if default_kind is None:
                raise InvalidDropdownValueError(path, f"In this case must be one of these: {possible_values_string}")
            else:
                self.validate_kind(path, default_kind, message=f"If kind is not {default_kind} must be one of these: {possible_values_string}")
    
    def validate_kind(self, path, kind, message=None) -> None:
        if self.kind != kind:
            if message == None:
                message = f"In this case, kind of {self.__class__.__name__} must be {repr(kind)}"
            raise InvalidDropdownValueError(path, message)
    


