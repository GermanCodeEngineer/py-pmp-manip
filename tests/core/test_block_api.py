from pytest import fixture, raises
from copy   import deepcopy

from pypenguin.utility import FirstToInterConversionError, lists_equal_ignore_order

from pypenguin.core.block_api      import FIConversionAPI, ValidationAPI
from pypenguin.core.block_mutation import (
    SRCustomBlockMutation
)
from pypenguin.core.custom_block   import (
    SRCustomBlockOptype,
)

from tests.core.constants import (
    ALL_FR_BLOCKS_CLEAN, ALL_SR_COMMENTS, ALL_SR_SCRIPTS, ALL_SR_BLOCKS, SR_BLOCK_CUSTOM_OPCODE,
)

@fixture
def ficapi():
    return FIConversionAPI(
        blocks=ALL_FR_BLOCKS_CLEAN,
        block_comments=ALL_SR_COMMENTS,
    )

@fixture
def validation_api():
    return ValidationAPI(scripts=ALL_SR_SCRIPTS)



def test_FICAPI_get_block_id_by_parent_id(ficapi: FIConversionAPI):
    assert ficapi.get_block_ids_by_parent_id("c") == {"l", "k"}


def test_FICAPI_get_block(ficapi: FIConversionAPI):
    assert ficapi.get_block("d") == ALL_FR_BLOCKS_CLEAN["d"]


def test_FICAPI_schedule_block_deletion(ficapi: FIConversionAPI):
    ficapi_copy = deepcopy(ficapi)
    ficapi_copy.schedule_block_deletion("z")
    assert ficapi_copy.scheduled_block_deletions == ["z"]


def test_FICAPI_get_cb_mutation(ficapi: FIConversionAPI):
    assert ficapi.get_cb_mutation("do sth text %s and bool %b") == ALL_FR_BLOCKS_CLEAN["a"].mutation
    with raises(FirstToInterConversionError):
        ficapi.get_cb_mutation("some %s proccode")


def test_FICAPI_get_comment(ficapi: FIConversionAPI):
    assert ficapi.get_comment("j") == ALL_SR_COMMENTS["j"]



def test_ValidationAPI_post_init(validation_api: ValidationAPI):
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
    assert validation_api.cb_mutations == cb_mutations


def test_ValidationAPI_get_all_blocks(validation_api: ValidationAPI):
    assert lists_equal_ignore_order(validation_api._get_all_blocks(), ALL_SR_BLOCKS)


def test_ValidationAPI_get_cb_mutation(validation_api: ValidationAPI):
    assert validation_api.get_cb_mutation(SR_BLOCK_CUSTOM_OPCODE) == validation_api.cb_mutations[SR_BLOCK_CUSTOM_OPCODE]


