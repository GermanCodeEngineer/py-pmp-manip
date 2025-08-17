from copy import copy

from pmp_manip.important_consts import SHA256_SEC_VARIABLE, SHA256_SEC_LIST
from pmp_manip.utility          import string_to_sha256, grepr_dataclass, AA_TYPE, AA_TYPES, AA_LIST_OF_TYPES



def _variable_sha256(variable_name: str, sprite_name: str):
    """
    A shortcut for computing a variable's sha256 hash

    Args:
        variable_name: the name of the variable
        sprite_name: the name of the variable's sprite or None for globals
    
    Returns:
        the variable's sha256 hash
    """
    return string_to_sha256(variable_name, secondary=SHA256_SEC_VARIABLE, tertiary=sprite_name)



def _list_sha256(list_name: str, sprite_name: str):
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

    def validate(self, path: list) -> None:
        """
        Ensure a SRVariable is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRVariable is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPES(self, path, "current_value", (int, float, str, bool))
        # Only the above types can be saved in Scratch Project's Variables (JSON limitations)
    
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

    def validate(self, path: list):
        """
        Ensure a SRList is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRList is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_LIST_OF_TYPES(self, path, "current_value", (int, float, str, bool))
        # Only the above types can be saved in Scratch Project's Lists (JSON limitations)

    def to_tuple(self) -> tuple[str, str]:
        """
        Converts a SRList into a list tuple
        
        Returns:
            the list tuple
        """
        return (self.name, copy(self.current_value))


__all__ = ["SRVariable", "SRCloudVariable", "SRList"]

