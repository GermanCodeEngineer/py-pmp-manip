from dataclasses import field

from pypenguin.utility import grepr_dataclass, FirstToInterConversionError, ValidationError

from pypenguin.core.custom_block import SRCustomBlockOpcode

from pypenguin.core.block          import FRBlock, SRBlock, SRScript
from pypenguin.core.comment        import SRComment
from pypenguin.core.block_mutation import FRCustomBlockMutation, SRCustomBlockMutation

@grepr_dataclass(grepr_fields=["blocks", "scheduled_block_deletions"])
class FIConversionAPI:
    """
    An API which allows the access to other blocks in the same target during **conversion** from **f**irst to **i**ntermediate representation
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
        Get a block in the same target by block id
        
        Returns:
            the requested block
        """
        if block_id in self.blocks:
            return self.blocks[block_id]
        raise FirstToInterConversionError(f"Block with id {repr(block_id)} not found")
    
    def schedule_block_deletion(self, block_id: str) -> None:
        """
        Order a block to be deleted. 
        It will no longer be present in Temporary and Second Representation
        
        Args:
            block_id: the id of the block to be deleted
        
        Returns:
            None
        """
        self.scheduled_block_deletions.append(block_id)

    def get_cb_mutation(self, proccode: str) -> "FRCustomBlockMutation":
        """
        Get a custom block mutation by its procedure code
        
        Args:
            proccode: the procedure code of the desired mutation
        
        Returns:
            the custom block mutation
        """
        for block in self.blocks.values():
            if not isinstance(block.mutation, FRCustomBlockMutation): continue
            if block.mutation.proccode == proccode:
                return block.mutation
        raise FirstToInterConversionError(f"Mutation of proccode {repr(proccode)} not found")

    def get_comment(self, comment_id: str) -> SRComment:
        """
        Get a comment by id
        
        Args:
            comment_id: the id of the desired comment
        
        Returns:
            the comment
        """
        if comment_id in self.blocks:
            return self.block_comments[comment_id]
        raise FirstToInterConversionError(f"Comment with id {repr(comment_id)} not found")

@grepr_dataclass(grepr_fields=["scripts", "cb_mutations:"])
class ValidationAPI:
    """
    An API which allows the access to other blocks in the same target during validation
    """

    scripts: list["SRScript"]
    cb_mutations: dict[SRCustomBlockOpcode, "SRCustomBlockMutation"] = field(init=False)
    # Safe access is needed because blocks haven't actually been validated yet (see get_all_blocks)
    
    def __post_init__(self) -> None:
        """
        Fetch and store custom block mutations for later
        
        Returns:
            None
        """
        all_blocks = self._get_all_blocks()
        self.cb_mutations = {}
        for block in all_blocks:
            if not isinstance(getattr(block, "mutation", None), SRCustomBlockMutation):
                continue
            mutation: SRCustomBlockMutation = block.mutation
            if not isinstance(getattr(mutation, "custom_opcode", None), SRCustomBlockOpcode):
                continue
            self.cb_mutations[mutation.custom_opcode] = mutation

    def _get_all_blocks(self) -> list["SRBlock"]:
        """
        *[Internal Method]* Get all blocks in the same target
        
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
    
    def get_cb_mutation(self, custom_opcode: SRCustomBlockOpcode) -> "SRCustomBlockMutation":
        """
        Get a custom block mutation by its custom opcode
        
        Args:
            custom_opcode: the custom opcode of the desired mutation
        
        Returns:
            the custom block mutation
        """
        if custom_opcode in self.cb_mutations:
            return self.cb_mutations[custom_opcode]
        raise ValidationError(f"Mutation of custom_opcode {custom_opcode} not found")


__all__ = ["FIConversionAPI", "ValidationAPI"]

