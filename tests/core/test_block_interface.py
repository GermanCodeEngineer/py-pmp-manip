from copy   import deepcopy
from pytest import fixture, raises

from pypenguin.utility import ConversionError, lists_equal_ignore_order

from pypenguin.core.block_interface import FirstToInterIF, ValidationIF
from pypenguin.core.block_mutation  import SRCustomBlockMutation
from pypenguin.core.custom_block    import SRCustomBlockOptype

from tests.core.constants import (
    ALL_FR_BLOCKS_CLEAN, ALL_SR_COMMENTS, ALL_SR_SCRIPTS, ALL_SR_BLOCKS, SR_BLOCK_CUSTOM_OPCODE,
)


@fixture
def fti_if():
    return FirstToInterIF(
        blocks=ALL_FR_BLOCKS_CLEAN,
        block_comments=ALL_SR_COMMENTS,
    )

@fixture
def validation_if():
    return ValidationIF(scripts=ALL_SR_SCRIPTS)



def test_FirstToInterIF_get_block_id_by_parent_id(fti_if: FirstToInterIF):
    assert fti_if.get_block_ids_by_parent_id("c") == {"l", "k"}


def test_FirstToInterIF_get_block(fti_if: FirstToInterIF):
    assert fti_if.get_block("d") == ALL_FR_BLOCKS_CLEAN["d"]


def test_FirstToInterIF_schedule_block_deletion(fti_if: FirstToInterIF):
    ficapi_copy = deepcopy(fti_if)
    ficapi_copy.schedule_block_deletion("z")
    assert ficapi_copy.scheduled_block_deletions == ["z"]


def test_FirstToInterIF_get_cb_mutation(fti_if: FirstToInterIF):
    assert fti_if.get_cb_mutation("do sth text %s and bool %b") == ALL_FR_BLOCKS_CLEAN["a"].mutation
    with raises(ConversionError):
        fti_if.get_cb_mutation("some %s proccode")


def test_FirstToInterIF_get_comment(fti_if: FirstToInterIF):
    assert fti_if.get_comment("j") == ALL_SR_COMMENTS["j"]



def test_ValidationIF_post_init(validation_if: ValidationIF):
    cb_mutations = {
        SR_BLOCK_CUSTOM_OPCODE: SRCustomBlockMutation(
            custom_opcode=SR_BLOCK_CUSTOM_OPCODE,
            no_screen_refresh=False,
            optype=SRCustomBlockOptype.NUMBER_REPORTER,
            main_color="#FF6680",
            prototype_color="#FF4D6A",
            outline_color="#FF3355",
        ),
    }
    assert validation_if.cb_mutations == cb_mutations


def test_ValidationIF_get_all_blocks(validation_if: ValidationIF):
    assert lists_equal_ignore_order(validation_if._get_all_blocks(), ALL_SR_BLOCKS)


def test_ValidationIF_get_cb_mutation(validation_if: ValidationIF):
    assert validation_if.get_cb_mutation(SR_BLOCK_CUSTOM_OPCODE) == validation_if.cb_mutations[SR_BLOCK_CUSTOM_OPCODE]


