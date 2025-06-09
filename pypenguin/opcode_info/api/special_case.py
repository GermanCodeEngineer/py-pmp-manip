from typing import Callable

from pypenguin.utility import grepr_dataclass, PypenguinEnum


class SpecialCaseType(PypenguinEnum):
    """
    Currently impletented kinds of Special Cases. Documentation is included in the source code
    """
    
    ######################################################
    #                    Data Handlers                   # 
    ######################################################
    
    GET_OPCODE_TYPE = 0
    # evaluate opcode type
    # is called when opcode_info.opcode_type is DYNAMIC
    # should NEVER return MENU (or any other pseudo opcode type)
    """
    def example(
        block: "SRBlock|IRBlock", validation_if: "ValidationIF"
    ) -> OpcodeType:
        ...
    """

    GET_ALL_INPUT_IDS_INFO = 1
    # map new and old input id to input information
    # -> DualKeyDict[old, new, InputInfo]
    # fti_if will be None for a IRBlock or SRBlock and the block api for a FRBlock
    """
    def example(
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None"
    ) -> DualKeyDict[str, str, InputType]:
        ...
    """
    
    
    ######################################################
    #                 Behaviour Handlers                 # 
    ######################################################
    
    PRE_FIRST_TO_INTER = 2 # execure before FRBlock.to_inter
    """
    def example(block: "FRBlock", fti_if: "FirstToInterIF") -> "FRBlock":
        ...
    """
     
    FIRST_TO_INTER = 3 # execute instead of FRBlock.to_inter
    """
    def example(block: "FRBlock", fti_if: "FirstToInterIF") -> "IRBlock":
        ...
    """
    
    POST_VALIDATION = 4 # execute after SRBlock.validate
    """
    def example(path: list, block: "SRBlock") -> None:
        ...
    """    

@grepr_dataclass(grepr_fields=["type", "function"])
class SpecialCase:
    """
    Special Cases allows for custom behaviour for special blocks
    """

    type: SpecialCaseType
    function: Callable
    
    def call(self, *args, **kwargs):
        """
        Call a special case and get its return value. Arguments depend on SpecialCaseType
        Parameters:
            *args: positional arguments forwarded to the function
            **kwargs: keyword arguments forwarded to the function

        Returns:
            the return value of the function
        """
        return self.function(*args, **kwargs)


__all__ = ["SpecialCaseType", "SpecialCase"]

