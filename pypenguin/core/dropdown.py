from typing      import Any
from dataclasses import dataclass

from pypenguin.utility     import GreprClass, ValidationConfig, AA_TYPE, AA_JSON_COMPATIBLE, InvalidDropdownValueError
from pypenguin.opcode_info import DropdownType, DropdownValueKind

from pypenguin.core.context import PartialContext, CompleteContext


@dataclass(repr=False)
class SRDropdownValue(GreprClass):
    """
    The second representation for a block dropdown, containing a kind and a value
    """
    _grepr = True
    _grepr_fields = ["kind", "value"]

    kind: DropdownValueKind
    value: Any
    
    @classmethod
    def from_tuple(cls, data: tuple[DropdownValueKind, Any]) -> "SRDropdownValue":
        """
        Deserializes a tuple into a SRDropdownValue
        
        Args:
            data: the raw data
        
        Returns:
            the SRDropdownValue
        """
        return cls(
            kind=data[0],
            value=data[1],
        )

    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRDropdownValue is structurally valid, raise ValidationError if not.
        For exact validation, you should additionally call the validate_value method.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        """
        AA_TYPE(self, path, "kind", DropdownValueKind)
        AA_JSON_COMPATIBLE(self, path, "value")

    def validate_value(self, path: list, dropdown_type: "DropdownType", context: PartialContext | CompleteContext) -> None:
        """
        Ensures the value of a SRDropdownValue is allowed under given circumstances(context),
        raise ValidationError if not. 
        For example, it ensures that only variables are referenced, which actually exist.     
        For structural validation call the validate method.
        
        Args:
            path: the path from the project to itself. Used for better errors
            dropdown_type: the dropdown type as described in the opcode specific information.
            context: Context about parts of the project. Used to validate the values of dropdowns.
        
        Returns:
            None
        """
        possible_values = dropdown_type.calculate_possible_new_dropdown_values(context=context)
        default_kind = dropdown_type.get_default_kind_for_calculation()
        possible_values_string = (
            "No possible values." if possible_values == [] else
            "".join(["\n- "+repr(value) for value in possible_values])
        )
        if (self.kind, self.value) not in possible_values:
            if default_kind is None:
                raise InvalidDropdownValueError(path, f"In this case must be one of these: {possible_values_string}")
            elif self.kind != default_kind:
                raise InvalidDropdownValueError(path, f"If kind is not {default_kind} must be one of these: {possible_values_string}")


