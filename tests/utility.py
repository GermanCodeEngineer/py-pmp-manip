from typing      import Any, Type, Callable, TypeVar
from copy        import copy, deepcopy
from pytest      import raises

from pmp_manip.utility import PP_ValidationError
from pmp_manip.core.block   import FRBlock
from pmp_manip.core.comment import FRComment

_CPMT = TypeVar("_CPMT")

def copymodify(obj: _CPMT, attr: str, value: Any) -> _CPMT:
    """
    Copy an object and modify an attribute
    `copymodify(x, 'y', z)` is equivalent to `x2 = copy.copy(x)\nx2.y = z`
    """
    copied_obj = copy(obj)
    setattr(copied_obj, attr, value)
    return copied_obj

_AVTT = TypeVar("_AVTT")

def execute_attr_validation_tests(
        obj: _AVTT, 
        attr_tests: list[tuple[str, Any, Type[PP_ValidationError]]], 
        validate_func: Callable[[_AVTT], None],
        func_args: list[Any]=[],
    ) -> None:
    """
    Test validation. For every "test" change one attribute to an invalid value and ensure an error is raised

    Args:
        obj: the object to 
        attr_tests: list of tuples, which contain
            - the attribute to change (str)
            - the value for the modified attribute
            - the type of error which is expected to be raised
        validate_func: the function to be called for every test with the modified object and the additional arguments
        func_args: additional arguments to provide to validate_func
    """
    for attr, value, error in attr_tests:
        modified_obj = copymodify(obj, attr, value)
        with raises(error):
            validate_func(modified_obj, *func_args)


def nest_block(all_blocks: dict[str, FRBlock|tuple], all_comments: dict[str, FRComment], current_id: str) -> FRBlock:
    current_block = deepcopy(all_blocks[current_id])
    if current_block.next is not None:
        current_block.next = nest_block(all_blocks, all_comments, current_id=current_block.next)
    current_block.parent = ... # this could cause a difference otherwise
    for input_id, input_value in current_block.inputs.items():
        new_input_value = []
        new_input_value.append(input_value[0])
        for item in input_value[1:]:
            if   isinstance(item, tuple): # an immediate block or text field
                new_input_value.append(item)
            elif isinstance(item, str): # a block reference
                new_input_value.append(nest_block(all_blocks, all_comments, current_id=item))
            else: raise ValueError()
        current_block.inputs[input_id] = tuple(new_input_value)
        if isinstance(current_block.comment, str):
            current_block.comment = all_comments[current_block.comment]
    return current_block

def nest_all_blocks_comments(all_blocks: dict[str, FRBlock|tuple], all_comments: dict[str, FRComment]) -> tuple[list[FRBlock], list[FRComment]]:
    new_scripts = []
    for block_id, block in all_blocks.items():
        if isinstance(block, tuple):
            new_scripts.append(block)
        elif block.top_level:
            new_scripts.append(nest_block(all_blocks, all_comments, current_id=block_id))
    return (new_scripts, list(all_comments.values()))


__all__ = ["copymodify", "execute_attr_validation_tests"]

