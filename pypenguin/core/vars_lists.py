from pypenguin.utility import grepr_dataclass, ValidationConfig, AA_TYPE, AA_TYPES, AA_LIST_OF_TYPES


@grepr_dataclass(grepr_fields=["name", "current_value"])
class SRVariable:
    
    name: str
    current_value: int | float | str | bool

    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRVariable is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRVariable is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPES(self, path, "current_value", (int, float, str, bool))
        # Only the above types can be saved in Scratch Projects
    
    def to_tuple(self) -> tuple[str, str]:
        """
        Converts a SRVariable into a variable tuple
        # TODO: add tests
        
        Returns:
            the variable tuple
        """
        return (self.name, self.current_value)

class SRCloudVariable(SRVariable):
    def to_tuple(self) -> tuple[str, str]:
        """
        Converts a SRCloudVariable into a variable tuple
        # TODO: add tests
        
        Returns:
            the variable tuple
        """
        return (self.name, self.current_value, True)

@grepr_dataclass(grepr_fields=["name", "current_value"])
class SRList:
    
    name: str
    current_value: list[int | float | str | bool]

    def validate(self, path: list, config: ValidationConfig):
        """
        Ensure a SRList is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRList is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_LIST_OF_TYPES(self, path, "current_value", (int, float, str, bool))
        # Only the above types can be saved in Scratch Projects

    def to_tuple(self) -> tuple[str, str]:
        """
        Converts a SRList into a list tuple
        # TODO: add tests
        
        Returns:
            the list tuple
        """
        return (self.name, self.current_value)


__all__ = ["SRVariable", "SRCloudVariable", "SRList"]

