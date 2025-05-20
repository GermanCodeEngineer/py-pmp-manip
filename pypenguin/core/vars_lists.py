from dataclasses import dataclass

from pypenguin.utility import GreprClass, ValidationConfig
from pypenguin.utility import AA_TYPE, AA_TYPES, AA_LIST_OF_TYPES

@dataclass(repr=False)
class SRVariable(GreprClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
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
        AA_TYPES(self, path, "current_value", (int, float, str, bool)) # Only these can be saved in Scratch Projects

class SRCloudVariable(SRVariable):
    pass

@dataclass(repr=False)
class SRList(GreprClass):
    _grepr = True
    _grepr_fields = ["name", "current_value"]
    
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
        AA_LIST_OF_TYPES(self, path, "current_value", (int, float, str, bool)) # Only these can be saved in Scratch Projects


__all__ = ["SRVariable", "SRCloudVariable", "SRList"]

