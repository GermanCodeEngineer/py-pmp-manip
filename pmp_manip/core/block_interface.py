from dataclasses import field

from pmp_manip.utility import grepr_dataclass, number_to_token, MANIP_ConversionError, MANIP_ValidationError

from pmp_manip.core.block_mutation import FRCustomBlockMutation, SRCustomBlockMutation
from pmp_manip.core.block          import FRBlock, IRBlock, SRBlock, SRScript
from pmp_manip.core.comment        import FRComment, SRComment
from pmp_manip.core.custom_block   import SRCustomBlockOpcode
from pmp_manip.core.vars_lists     import _variable_sha256, _list_sha256


@grepr_dataclass(grepr_fields=["blocks", "block_comments", "scheduled_block_deletions"])
class FirstToInterIF:
    """
    An interface which allows the management of other blocks in the same target during conversion from first to intermediate representation
    """

    blocks: dict[str, FRBlock]
    block_comments: dict[str, SRComment]
    scheduled_block_deletions: list[str] = field(default_factory=list)

    def get_block_ids_by_parent_id(self, parent_id: str) -> set[str]:
        """
        Get all ids of the blocks whose parent attribute is parent_id

        Returns:
            the set of block ids
        """
        block_ids = set()
        for block_id_candidate, block_candidate in self.blocks.items():
            if block_candidate.parent == parent_id:
                block_ids.add(block_id_candidate)
        return block_ids

    def get_block(self, block_id: str) -> FRBlock:
        """
        Get a FRBlock in the same target by block id
        
        Returns:
            the requested FRBlock
        """
        if block_id in self.blocks:
            return self.blocks[block_id]
        raise MANIP_ConversionError(f"Block with id {block_id!r} not found")
    
    def schedule_block_deletion(self, block_id: str) -> None:
        """
        Order a FRBlock to be deleted. 
        It will no longer be present in intermediate and second representation
        
        Args:
            block_id: the id of the FRBlock to be deleted
        
        Returns:
            None
        """
        self.scheduled_block_deletions.append(block_id)

    def get_cb_mutation(self, proccode: str) -> "FRCustomBlockMutation":
        """
        Get a FRCustomBlockMutation by its procedure code
        
        Args:
            proccode: the procedure code of the desired FRCustomBlockMutation
        
        Returns:
            the FRCustomBlockMutation
        """
        for block in self.blocks.values():
            if not isinstance(block.mutation, FRCustomBlockMutation): continue
            if block.mutation.proccode == proccode:
                return block.mutation
        raise MANIP_ConversionError(f"Mutation of proccode {proccode!r} not found")

    def get_comment(self, comment_id: str) -> SRComment:
        """
        Get a comment by id
        
        Args:
            comment_id: the id of the desired comment
        
        Returns:
            the comment
        """
        if comment_id in self.block_comments:
            return self.block_comments[comment_id]
        raise MANIP_ConversionError(f"Comment with id {comment_id!r} not found")

@grepr_dataclass(grepr_fields=[
    "blocks", 
    "global_vars", "local_vars", "global_lists", "local_lists", "sprite_name", "_next_block_id_num",
    "added_blocks", "added_comments", 
    "_cb_mutations",
])
class InterToFirstIF:
    """
    An interface which allows the management of other blocks in the same target during conversion from first to intermediate representation
    """

    blocks: dict[str, IRBlock]
    global_vars: list[str]
    global_lists: list[str]
    local_vars: list[str]
    local_lists: list[str]
    sprite_name: str | None
    _next_block_id_num: int = 1 # TODO: remove default
    added_blocks: dict[str, FRBlock | tuple] = field(init=False, default_factory=dict)
    added_comments: dict[str, FRComment] = field(init=False, default_factory=dict)
    _cb_mutations: dict[str, "FRCustomBlockMutation"] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        """
        Fetch and store SRCustomBlockMutation's for later
        
        Returns:
            None
        """
        for block in self.blocks.values():
            if isinstance(getattr(block, "mutation", None), SRCustomBlockMutation):
                frmutation: "FRCustomBlockMutation" = block.mutation.to_first(itf_if=self)
                if frmutation.proccode in self._cb_mutations:
                    raise MANIP_ConversionError(f"Two custom blocks cannot be defined with the same proccode(essentially custom opcode text): {frmutation.proccode!r}")
                self._cb_mutations[frmutation.proccode] = frmutation
        
    def get_next_block_id(self, comment=False) -> str:
        """
        Get the next available block reference id
        
        Returns:
            the next available block reference id
        """
        block_id = number_to_token(self._next_block_id_num)
        self._next_block_id_num += 1
        return block_id

    def schedule_block_addition(self, block_id: str, block: FRBlock | tuple) -> None:
        """
        Order a FRBlock to be added by its reference id. 
        It will be present in first representation
        
        Args:
            block_id: the reference id for the block
            block: the FRBlock to add
        
        Returns:
            None
        """
        self.added_blocks[block_id] = block
        
    def add_comment(self, comment: FRComment, floating=False) -> str:
        """
        Order a FRComment to be added and return it's reference id.
        It will be present in first representation
        
        Args:
            comment: the FRComment to add
        
        Returns:
            the reference id of the added FRComment
        """
        comment_id = self.get_next_block_id(comment=True)
        self.added_comments[comment_id] = comment
        return comment_id

    def get_fr_cb_mutation(self, proccode: str) -> "FRCustomBlockMutation":
        """
        Get a SRCustomBlockMutation of the blocks by its procedure code
        
        Args:
            proccode: the procedure code of the desired FRCustomBlockMutation
        
        Returns:
            the FRCustomBlockMutation
        """
        if proccode in self._cb_mutations:
            return self._cb_mutations[proccode]
        raise MANIP_ConversionError(f"Mutation of proccode {proccode!r} not found")

    def get_sr_cb_mutation(self, custom_opcode: SRCustomBlockOpcode) -> "SRCustomBlockMutation":
        """
        Get a SRCustomBlockMutation of the blocks by its SRCustomBlockOpcode
        
        Args:
            custom_opcode: the SRCustomBlockOpcode of the desired SRCustomBlockMutation
        
        Returns:
            the SRCustomBlockMutation
        """
        for block in self.blocks.values():
            if not isinstance(block.mutation, SRCustomBlockMutation): continue
            if block.mutation.custom_opcode == custom_opcode:
                return block.mutation
        raise MANIP_ConversionError(f"Mutation of custom opcode {custom_opcode!r} not found")

    def get_variable_sha256(self, variable_name: str) -> str:
        """
        Get the sha256 hash of a global or local variable
        
        Args:
            variable_name: the variable name
        
        Returns:
            the sha256 hash
        """
        if   variable_name in self.global_vars:
            sprite_name = "_stage_"
        elif variable_name in self.local_vars:
            sprite_name = "_stage_" if self.sprite_name is None else self.sprite_name
        else:
            raise MANIP_ConversionError(f"Variable {variable_name!r} not found")
        return _variable_sha256(variable_name, sprite_name)

    def get_list_sha256(self, list_name: str) -> str:
        """
        Get the sha256 hash of a global or local list
        
        Args:
            list_name: the list name
        
        Returns:
            the sha256 hash
        """
        if   list_name in self.global_lists:
            sprite_name = "_stage_"
        elif list_name in self.local_lists:
            sprite_name = "_stage_" if self.sprite_name is None else self.sprite_name
        else:
            raise MANIP_ConversionError(f"List {list_name!r} not found")
        return _list_sha256(list_name, sprite_name)

@grepr_dataclass(grepr_fields=["scripts", "cb_mutations"])
class SecondReprIF:
    """
    ABC for an interface which holds scripts in second representation
    """

    scripts: list["SRScript"]
    cb_mutations: dict[SRCustomBlockOpcode, "SRCustomBlockMutation"] = field(init=False, default_factory=dict)
    # Safe access is needed because blocks have not actually been validated yet (see get_all_blocks)
    
    def __post_init__(self) -> None:
        """
        Fetch and store SRCustomBlockMutation's for later
        
        Returns:
            None
        """
        all_blocks = self._get_all_blocks()
        for block in all_blocks:
            if not isinstance(getattr(block, "mutation", None), SRCustomBlockMutation):
                continue
            mutation: SRCustomBlockMutation = block.mutation
            if not isinstance(getattr(mutation, "custom_opcode", None), SRCustomBlockOpcode):
                continue
            self.cb_mutations[mutation.custom_opcode] = mutation

    def _get_all_blocks(self) -> list["SRBlock"]:
        """
        Get all blocks in the same target
        
        Returns:
            all blocks in the target 
        """
        def recursive_block_search(block: "SRBlock") -> None:
            blocks.append(block)
            if not isinstance(getattr(block, "inputs", None), dict):
                return
            for input in block.inputs.values(): 
                if isinstance(getattr(input, "block", None), SRBlock):
                    recursive_block_search(input.block)
                if isinstance(getattr(input, "blocks", None), list):
                    [recursive_block_search(sub_block) for sub_block in input.blocks if isinstance(sub_block, SRBlock)]
        
        blocks = []
        for script in self.scripts:
            if not isinstance(getattr(script, "blocks", None), list):
                continue
            for block in script.blocks:
                if not isinstance(block, SRBlock):
                    continue
                recursive_block_search(block)
        return blocks

@grepr_dataclass(grepr_fields=["added_blocks", "_next_block_id_num"])
class SecondToInterIF(SecondReprIF):
    """
    An interface which allows the management of other blocks in the same target during conversion from second to intermediate representation
    """

    produced_blocks: dict[str, IRBlock] = field(default_factory=dict)
    _next_block_id_num: int = 1

    def get_next_block_id(self) -> str:
        """
        Get the next available block reference id
        
        Returns:
            the next available block reference id
        """
        block_id = number_to_token(self._next_block_id_num)
        self._next_block_id_num += 1
        return block_id

    def schedule_block_addition(self, block_id: str, block: IRBlock) -> None:
        """
        Order a IRBlock to be added by its reference id. 
        It will be present in intermediate representation
        
        Args:
            block_id: the reference id for the block
            block: the IRBlock to add
        
        Returns:
            None
        """
        self.produced_blocks[block_id] = block
    
    def get_cb_mutation(self, custom_opcode: SRCustomBlockOpcode) -> "SRCustomBlockMutation":
        """
        Get a SRCustomBlockMutation by its SRCustomBlockOpcode
        
        Args:
            custom_opcode: the SRCustomBlockOpcode of the desired SRCustomBlockMutation
        
        Returns:
            the SRCustomBlockMutation
        """
        if custom_opcode in self.cb_mutations:
            return self.cb_mutations[custom_opcode]
        raise MANIP_ConversionError(f"Mutation of custom_opcode {custom_opcode!r} not found")


class ValidationIF(SecondReprIF):
    """
    An interface which allows the management of other blocks in the same target during validation
    """

    def get_cb_mutation(self, custom_opcode: SRCustomBlockOpcode) -> "SRCustomBlockMutation":
        """
        Get a SRCustomBlockMutation by its SRCustomBlockOpcode
        
        Args:
            custom_opcode: the SRCustomBlockOpcode of the desired SRCustomBlockMutation
        
        Returns:
            the SRCustomBlockMutation
        """
        if custom_opcode in self.cb_mutations:
            return self.cb_mutations[custom_opcode]
        raise MANIP_ValidationError(f"Mutation of custom_opcode {custom_opcode!r} not found")


__all__ = ["FirstToInterIF", "InterToFirstIF", "SecondReprIF", "SecondToInterIF", "ValidationIF"]

