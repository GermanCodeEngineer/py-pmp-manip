from pytest import fixture, raises
from copy   import copy

from pypenguin.utility import FSCError, lists_equal_ignore_order
from pypenguin.opcode_info import DropdownValueKind, InputMode

from pypenguin.core.block_api      import FTCAPI, ValidationAPI
from pypenguin.core.block          import (
    FRBlock, IRBlock, IRBlockReference, IRInputValue,
    SRBlock, SRScript, 
    SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, SRBlockOnlyInputValue, 
    SRDropdownValue,
)
from pypenguin.core.block_mutation import (
    FRCustomBlockMutation, FRCustomBlockCallMutation,
    FRCustomBlockArgumentMutation,
    SRCustomBlockMutation, SRCustomBlockCallMutation,
    SRCustomBlockArgumentMutation, SRStopScriptMutation,
)
from pypenguin.core.comment        import SRComment
from pypenguin.core.custom_block   import (
    SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType,
    SRCustomBlockOptype,
)

from tests.core.constants import (
    ALL_FR_BLOCKS, ALL_SR_COMMENTS, ALL_SR_SCRIPTS, ALL_SR_BLOCKS, SR_BLOCK_CUSTOM_OPCODE,
)

@fixture
def ftcapi():
    return FTCAPI(
        blocks=ALL_FR_BLOCKS,
        block_comments=ALL_SR_COMMENTS,
    )

@fixture
def vapi():
    return ValidationAPI(scripts=ALL_SR_SCRIPTS)


def test_ftcapi_get_all_blocks(ftcapi: FTCAPI):
    assert ftcapi.get_all_blocks() == ALL_FR_BLOCKS

def test_ftcapi_get_blocks(ftcapi: FTCAPI):
    assert ftcapi.get_block("d") == ALL_FR_BLOCKS["d"]

def test_ftcapi_schedule_block_deletion(ftcapi: FTCAPI):
    ftcapi_copy = copy(ftcapi)
    ftcapi_copy.schedule_block_deletion("z")
    assert ftcapi_copy.scheduled_block_deletions == ["z"]

def test_ftcapi_get_cb_mutation(ftcapi: FTCAPI):
    assert ftcapi.get_cb_mutation("do sth text %s and bool %b") == ALL_FR_BLOCKS["a"].mutation
    with raises(FSCError):
        ftcapi.get_cb_mutation("some %s proccode")

def test_ftcapi_get_comment(ftcapi: FTCAPI):
    assert ftcapi.get_comment("j") == ALL_SR_COMMENTS["j"]


def test_vapi_post_init(vapi: ValidationAPI):
    cb_mutations = {
        SR_BLOCK_CUSTOM_OPCODE: SRCustomBlockMutation(
            custom_opcode=SR_BLOCK_CUSTOM_OPCODE,
            no_screen_refresh=False,
            optype=SRCustomBlockOptype.NUMBER_REPORTER,
            color1="#FF6680",
            color2="#FF4D6A",
            color3="#FF3355",
        ),
    }
    assert vapi.cb_mutations == cb_mutations


def test_vapi_get_all_blocks(vapi: ValidationAPI):
    assert lists_equal_ignore_order(vapi.get_all_blocks(), ALL_SR_BLOCKS)

def test_vapi_get_cb_mutation(vapi: ValidationAPI):
    assert vapi.get_cb_mutation(SR_BLOCK_CUSTOM_OPCODE) == vapi.cb_mutations[SR_BLOCK_CUSTOM_OPCODE]


