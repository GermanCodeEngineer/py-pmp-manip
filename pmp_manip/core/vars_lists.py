from __future__ import annotations
from copy       import copy

from pmp_manip.important_consts import SHA256_SEC_VARIABLE, SHA256_SEC_LIST
from pmp_manip.utility          import (
    string_to_sha256, grepr_dataclass,
    HasGreprValidate,
)



def _variable_sha256(variable_name: str, sprite_name: str): # is needed!
    """
    A shortcut for computing a variable's sha256 hash

    Args:
        variable_name: the name of the variable
        sprite_name: the name of the variable's sprite or None for globals
    
    Returns:
        the variable's sha256 hash
    """
    return string_to_sha256(variable_name, secondary=SHA256_SEC_VARIABLE, tertiary=sprite_name)



def _list_sha256(list_name: str, sprite_name: str): # is needed!
    """
    A shortcut for computing a list's sha256 hash

    Args:
        list_name: the name of the list
        sprite_name: the name of the list's sprite or None for globals
    
    Returns:
        the list's sha256 hash
    """
    return string_to_sha256(list_name, secondary=SHA256_SEC_LIST, tertiary=sprite_name)



@grepr_dataclass()
class SRVariable(HasGreprValidate):
    
    name: str
    current_value: int | float | str | bool | dict[str, int|float|str|bool | dict] # ...
    # Only the above types can be saved in Scratch Project's Variables (JSON limitations)
    # dict is allowed too because some extensions save custom types in it
    # TODO: possibly validate dict contents
    
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

@grepr_dataclass()
class SRList(HasGreprValidate):
    
    name: str
    current_value: list[int | float | str | bool]
    # Only the above types can be saved in Scratch Project's Lists (JSON limitations)

    def to_tuple(self) -> tuple[str, str]:
        """
        Converts a SRList into a list tuple
        
        Returns:
            the list tuple
        """
        return (self.name, copy(self.current_value))


__all__ = ["SRVariable", "SRCloudVariable", "SRList"]

