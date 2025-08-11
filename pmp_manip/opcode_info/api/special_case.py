from typing import Callable

from pmp_manip.utility import grepr_dataclass, GEnum


class SpecialCaseType(GEnum):
    """
    Currently impletented kinds of Special Cases. Documentation is included in the source code
    """

    ######################################################
    #                 General Information                #
    ######################################################
    """
    Function Arguments explained:
        block: the block to convert, edit or use as context
        block_id: the reference id of the block
        ...if: an interface used to manage or get information about other blocks
        path: the path to the block from the project root
    
    Tipps:
        if the given block is modified it should first be copied using copy.copy/copy.deepcopy
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
    #         Representation Conversion Handlers         #
    ######################################################
    
    PRE_FIRST_TO_INTER = 2
    # execure before FRBlock.to_inter
    """
    def example(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "FRBlock":
        ...
    """
     
    INSTEAD_FIRST_TO_INTER = 3
    # execute instead of FRBlock.to_inter
    """
    def example(block: "FRBlock", block_id: str, fti_if: "FirstToInterIF") -> "IRBlock":
        ...
    """

    POST_INTER_TO_FIRST = 4
    # execure after IRBlock.to_first
    """
    def example(block: "FRBlock", block_id: str, itf_if: "InterToFirstIF") -> "FRBlock":
        ...
    """
    

    ######################################################
    #                   Static Handlers                  #
    ######################################################

    POST_VALIDATION = 6
    # execute after SRBlock.validate
    # should raise subclass of MANIP_ValidationError if invalid
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
        # TODO: create better handler, specific for each SpecialCaseType
        Call a special case and get its return value. Arguments depend on SpecialCaseType
        Parameters:
            *args: positional arguments forwarded to the function
            **kwargs: keyword arguments forwarded to the function

        Returns:
            the return value of the function
        """
        return self.function(*args, **kwargs)


__all__ = ["SpecialCaseType", "SpecialCase"]

