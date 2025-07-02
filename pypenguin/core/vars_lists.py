from pypenguin.important_consts import SHA256_SEC_VARIABLE, SHA256_SEC_LIST
from pypenguin.utility          import string_to_sha256, grepr_dataclass, ValidationConfig, AA_TYPE, AA_TYPES, AA_LIST_OF_TYPES



def variable_sha256(variable_name: str, sprite_name: str):
    """
    A shortcut for computing a variable's sha256 hash

    Args:
        variable_name: the name of the variable
        sprite_name: the name of the variable's sprite or None for globals
    
    Returns:
        the variable's sha256 hash
    """
    return string_to_sha256(variable_name, secondary=SHA256_SEC_VARIABLE, tertiary=sprite_name)



def list_sha256(list_name: str, sprite_name: str):
    """
    A shortcut for computing a list's sha256 hash

    Args:
        list_name: the name of the list
        sprite_name: the name of the list's sprite or None for globals
    
    Returns:
        the list's sha256 hash
    """
    return string_to_sha256(list_name, secondary=SHA256_SEC_LIST, tertiary=sprite_name)



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
        
        Returns:
            the variable tuple
        """
        return (self.name, self.current_value)

class SRCloudVariable(SRVariable):
    def to_tuple(self) -> tuple[str, str, bool]:
        """
        Converts a SRCloudVariable into a variable tuple
        
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
        
        Returns:
            the list tuple
        """
        return (self.name, self.current_value)


__all__ = ["variable_sha256", "list_sha256", "SRVariable", "SRCloudVariable", "SRList"]

