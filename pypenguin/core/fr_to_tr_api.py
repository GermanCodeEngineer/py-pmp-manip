from typing import TYPE_CHECKING

from utility import PypenguinClass

if TYPE_CHECKING:
    from core.block          import FRBlock, TRBlock, SRBlock
    from core.comment        import SRAttachedComment
    from core.block_mutation import FRCustomBlockMutation

class FRtoTRAPI(PypenguinClass):
    _grepr = True
    _grepr_fields = ["blocks", "scheduled_block_deletions"]

    blocks: dict[str, "FRBlock"]
    block_comments: dict[str, "SRAttachedComment"]
    scheduled_block_deletions: list[str]    

    def __init__(self, blocks: dict[str, "FRBlock"], block_comments: dict[str, "SRAttachedComment"]):
        self.blocks                    = blocks
        self.block_comments            = block_comments
        self.scheduled_block_deletions = []
    
    def get_all_blocks(self) -> dict[str, "FRBlock"]:
        return self.blocks
    
    def get_block(self, block_id: str) -> "FRBlock":
        return self.get_all_blocks()[block_id]
    
    def schedule_block_deletion(self, block_id: str) -> None:
        self.scheduled_block_deletions.append(block_id)

    def get_cb_mutation(self, proccode: str) -> "FRCustomBlockMutation":
        from core.block_mutation import FRCustomBlockMutation
        for block in self.blocks.values():
            if not isinstance(block.mutation, FRCustomBlockMutation): continue
            if block.mutation.proccode == proccode:
                return block.mutation
        raise ValueError(f"Mutation of proccode {repr(proccode)} not found.")

    def get_comment(self, comment_id: str) -> "SRAttachedComment":
        return self.block_comments[comment_id]
