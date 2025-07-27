from typing import Any

from pypenguin.opcode_info.api import DropdownType, DropdownValueKind
from pypenguin.utility         import grepr_dataclass, AA_TYPE, AA_JSON_COMPATIBLE, PP_InvalidDropdownValueError

from pypenguin.core.context import PartialContext, CompleteContext


@grepr_dataclass(grepr_fields=["kind", "value"])
class SRDropdownValue:
    """
    The second representation for a block dropdown, containing a kind and a value
    """

    kind: DropdownValueKind
    value: Any
    
    @classmethod
    def from_tuple(cls, data: tuple[DropdownValueKind, Any]) -> "SRDropdownValue":
        """
        Deserializes a tuple into a SRDropdownValue
        
        Args:
            data: the tuple of (kind, value)
        
        Returns:
            the SRDropdownValue
        """
        return cls(
            kind=data[0],
            value=data[1],
        )

    def to_tuple(self) -> tuple[DropdownValueKind, Any]:
        """
        Serializes a SRDropdownValue into a tuple
        
        Returns:
            the tuple of (kind, value)
        """
        return (self.kind, self.value)

    def validate(self, path: list) -> None:
        """
        Ensure a SRDropdownValue is structurally valid, raise PP_ValidationError if not
        For exact validation, you should additionally call the validate_value method
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            PP_ValidationError: if the SRDropdownValue is invalid
        """
        AA_TYPE(self, path, "kind", DropdownValueKind)
        AA_JSON_COMPATIBLE(self, path, "value")

    def validate_value(self, 
        path: list, 
        dropdown_type: "DropdownType", 
        context: PartialContext | CompleteContext,
    ) -> None:
        """
        Ensures the value of a SRDropdownValue is allowed under given circumstances(context),
        raise PP_ValidationError if not. 
        For example, it ensures that only variables are referenced, which actually exist.     
        For structural validation call the validate method
        
        Args:
            path: the path from the project to itself. Used for better error messages
            dropdown_type: the dropdown type as described in the opcode specific information
            context: Context about parts of the project. Used to validate the values of dropdowns
        
        Returns:
            None
        
        Raises:
            PP_InvalidDropdownValueError(PP_ValidationError): if the value is invalid in the specific situation
        """
        possible_values = dropdown_type.calculate_possible_new_dropdown_values(context=context)
        default_kind = dropdown_type.calculation_default_kind
        possible_values_string = (
            "No possible values" if possible_values == [] else
            "".join(["\n- "+repr(value) for value in possible_values])
        )
        tuple_value = self.to_tuple()
        if tuple_value not in possible_values:
            if default_kind is None:
                raise PP_InvalidDropdownValueError(path, f"In this case must be one of these: {possible_values_string}")
            elif self.kind is not default_kind:
                raise PP_InvalidDropdownValueError(
                    path, f"Either kind must be {default_kind} or (kind, value) must be one of these: {possible_values_string}"
                )
        post_validate_func = dropdown_type.post_validate_func
        if post_validate_func is not None:
            valid, error_msg = post_validate_func(tuple_value)
            if not valid:
                raise PP_InvalidDropdownValueError(path, error_msg)


__all__ = ["SRDropdownValue"]

