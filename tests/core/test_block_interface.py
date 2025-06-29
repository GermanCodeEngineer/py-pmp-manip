from copy   import deepcopy
from pytest import fixture, raises

from pypenguin.important_consts import SHA256_SEC_MAIN_ARGUMENT_NAME
from pypenguin.utility          import lists_equal_ignore_order, string_to_sha256, ConversionError, ValidationError

from pypenguin.core.block_interface import FirstToInterIF, InterToFirstIF, SecondReprIF, SecondToInterIF, ValidationIF
from pypenguin.core.block_mutation  import FRCustomBlockMutation, SRCustomBlockMutation
from pypenguin.core.block           import FRBlock, IRBlock
from pypenguin.core.comment         import FRComment
from pypenguin.core.custom_block    import SRCustomBlockOptype, SRCustomBlockOpcode
from pypenguin.core.vars_lists      import variable_sha256, list_sha256

from tests.core.constants import (
    ALL_FR_BLOCKS_CLEAN, ALL_IR_BLOCKS, 
    ALL_SR_SCRIPTS, ALL_SR_BLOCKS, ALL_SR_COMMENTS, SR_BLOCK_CUSTOM_OPCODE,
)


@fixture
def fti_if():
    return FirstToInterIF(
        blocks=ALL_FR_BLOCKS_CLEAN,
        block_comments=ALL_SR_COMMENTS,
    )

@fixture
def itf_if():
    return InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["globvar"],
        global_lists=["globlist"],
        local_vars=["locvar"],
        local_lists=["loclist"],
        sprite_name="some sprite name",
    )

@fixture
def sr_if():
    return SecondReprIF(scripts=ALL_SR_SCRIPTS)

@fixture
def sti_if():
    return SecondToInterIF(scripts=ALL_SR_SCRIPTS)

@fixture
def validation_if():
    return ValidationIF(scripts=ALL_SR_SCRIPTS)



def test_FirstToInterIF_get_block_id_by_parent_id(fti_if: FirstToInterIF):
    assert fti_if.get_block_ids_by_parent_id("c") == {"l", "k"}


def test_FirstToInterIF_get_block(fti_if: FirstToInterIF):
    assert fti_if.get_block("d") == ALL_FR_BLOCKS_CLEAN["d"]

def test_FirstToInterIF_get_block_not_found(fti_if: FirstToInterIF):
    with raises(ConversionError):
        fti_if.get_block("qqq")


def test_FirstToInterIF_schedule_block_deletion(fti_if: FirstToInterIF):
    fti_if_copy = deepcopy(fti_if)
    fti_if_copy.schedule_block_deletion("z")
    assert fti_if_copy.scheduled_block_deletions == ["z"]
    fti_if_copy.scheduled_block_deletions = []
    assert fti_if_copy == fti_if


def test_FirstToInterIF_get_cb_mutation(fti_if: FirstToInterIF):
    fti_if_copy = deepcopy(fti_if)
    assert fti_if_copy.get_cb_mutation("do sth text %s and bool %b") == ALL_FR_BLOCKS_CLEAN["a"].mutation
    with raises(ConversionError):
        fti_if_copy.get_cb_mutation("some %s proccode")
    assert fti_if_copy == fti_if
    


def test_FirstToInterIF_get_comment(fti_if: FirstToInterIF):
    fti_if_copy = deepcopy(fti_if)
    assert fti_if_copy.get_comment("s") == ALL_SR_COMMENTS["s"]
    assert fti_if_copy == fti_if

def test_FirstToInterIF_get_comment_not_found(fti_if: FirstToInterIF):
    fti_if_copy = deepcopy(fti_if)
    with raises(ConversionError):
        fti_if_copy.get_comment("qqq")
    assert fti_if_copy == fti_if


def test_InterToFirstIF_post_init():
    itf_if = InterToFirstIF(
        blocks=ALL_IR_BLOCKS,
        global_vars=["my variable"], global_lists=["my list"],
        local_vars=[], local_lists=[],
        sprite_name="_stage_",
    )
    cb_mutations = {
        "do sth text %s and bool %b": FRCustomBlockMutation(
            tag_name="mutation",
            children=[],
            proccode="do sth text %s and bool %b",
            argument_ids=[
                string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME), 
                string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME),
            ],
            argument_names=["a text arg", "a bool arg"],
            argument_defaults=["", "false"],
            warp=False,
            returns=True,
            edited=True,
            optype="number",
            color=("#FF6680", "#FF4D6A", "#FF3355"),
        ),
    }
    assert itf_if._cb_mutations == cb_mutations

def test_InterToFirstIF_post_init_same_proccode_twice():
    blocks = deepcopy(ALL_IR_BLOCKS)
    blocks["qqq"] = ALL_IR_BLOCKS["h"]
    with raises(ConversionError):
        InterToFirstIF(
            blocks=blocks,
            global_vars=[], global_lists=[],
            local_vars=[], local_lists=[],
            sprite_name="_stage_",
        )



def test_InterToFirstIF_get_next_block_id(itf_if: InterToFirstIF):
    itf_if_copy = deepcopy(itf_if)
    assert itf_if_copy.get_next_block_id() == "a"
    assert itf_if_copy._next_block_id_num == 2
    itf_if_copy._next_block_id_num -= 1
    assert itf_if_copy == itf_if


def test_InterToFirstIF_schedule_block_addition(itf_if: InterToFirstIF):
    itf_if_copy = deepcopy(itf_if)
    frblock = FRBlock(
        opcode="operator_trueBoolean",
        next=None,
        parent=None,
        inputs={},
        fields={},
        shadow=False,
        top_level=True,
        x=2000,
        y=2000,
    )
    itf_if_copy.schedule_block_addition("qqq", frblock)
    assert itf_if_copy.added_blocks == {"qqq": frblock}
    itf_if_copy.added_blocks = {}
    assert itf_if_copy == itf_if


def test_InterToFirstIF_add_comment(itf_if: InterToFirstIF):
    itf_if_copy = deepcopy(itf_if)
    frcomment = FRComment(
        block_id=None,
        x=1000,
        y=1000,
        width=200,
        height=200,
        minimized=False,
        text="a comment text",
    )
    comment_id = itf_if_copy.add_comment(frcomment)
    assert itf_if_copy.added_comments == {comment_id: frcomment}
    itf_if_copy.added_comments = {}
    itf_if_copy._next_block_id_num -= 1
    assert itf_if_copy == itf_if


def test_InterToFirstIF_get_fr_cb_mutation(itf_if: InterToFirstIF):
    itf_if_copy = deepcopy(itf_if)
    frmutation = itf_if_copy.get_fr_cb_mutation("do sth text %s and bool %b")
    assert frmutation == FRCustomBlockMutation(
        tag_name="mutation",
        children=[],
        proccode="do sth text %s and bool %b",
        argument_ids=[
            string_to_sha256("a text arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME), 
            string_to_sha256("a bool arg", secondary=SHA256_SEC_MAIN_ARGUMENT_NAME),
        ],
        argument_names=["a text arg", "a bool arg"],
        argument_defaults=["", "false"],
        warp=False,
        returns=True,
        edited=True,
        optype="number",
        color=("#FF6680", "#FF4D6A", "#FF3355"),
    )
    with raises(ConversionError):
        itf_if_copy.get_fr_cb_mutation("some %s proccode")
    assert itf_if_copy == itf_if


def test_InterToFirstIF_get_sr_cb_mutation(itf_if: InterToFirstIF):
    itf_if_copy = deepcopy(itf_if)
    srmutation = itf_if_copy.get_sr_cb_mutation(SR_BLOCK_CUSTOM_OPCODE)
    assert srmutation == SRCustomBlockMutation(
        custom_opcode=SR_BLOCK_CUSTOM_OPCODE,
        no_screen_refresh=False,
        optype=SRCustomBlockOptype.NUMBER_REPORTER,
        main_color="#FF6680",
        prototype_color="#FF4D6A",
        outline_color="#FF3355",
    )
    with raises(ConversionError):
        itf_if_copy.get_sr_cb_mutation(SRCustomBlockOpcode(segments=("hi")))
    assert itf_if_copy == itf_if


def test_InterToFirstIF_get_variable_sha256_global(itf_if: InterToFirstIF):
    sha256 = itf_if.get_variable_sha256("globvar")
    assert sha256 == variable_sha256("globvar", sprite_name="_stage_")

def test_InterToFirstIF_get_variable_sha256_local(itf_if: InterToFirstIF):
    sha256 = itf_if.get_variable_sha256("locvar")
    assert sha256 == variable_sha256("locvar", sprite_name=itf_if.sprite_name)

def test_InterToFirstIF_get_variable_sha256_undefined(itf_if: InterToFirstIF):
    with raises(ConversionError):
        itf_if.get_variable_sha256("some undefined var")


def test_InterToFirstIF_get_list_sha256_global(itf_if: InterToFirstIF):
    sha256 = itf_if.get_list_sha256("globlist")
    assert sha256 == list_sha256("globlist", sprite_name="_stage_")

def test_InterToFirstIF_get_list_sha256_local(itf_if: InterToFirstIF):
    sha256 = itf_if.get_list_sha256("loclist")
    assert sha256 == list_sha256("loclist", sprite_name=itf_if.sprite_name)

def test_InterToFirstIF_get_list_sha256_undefined(itf_if: InterToFirstIF):
    with raises(ConversionError):
        itf_if.get_list_sha256("some undefined list")



def test_SecondReprIF_post_init():
    sr_if = SecondReprIF(scripts=ALL_SR_SCRIPTS)
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
    assert sr_if.cb_mutations == cb_mutations

def test_SecondReprIF_post_init_invalid_custom_opcode():
    scripts = deepcopy(ALL_SR_SCRIPTS)
    srmutation: SRCustomBlockMutation = scripts[3].blocks[0].mutation
    srmutation.custom_opcode = 6
    sr_if = SecondReprIF(scripts=scripts)
    assert not lists_equal_ignore_order(sr_if._get_all_blocks(), ALL_SR_BLOCKS)

def test_SecondReprIF_post_init_invalid_inputs():
    scripts = deepcopy(ALL_SR_SCRIPTS)
    scripts[0].blocks[0].inputs = []
    sr_if = SecondReprIF(scripts=scripts)
    assert not lists_equal_ignore_order(sr_if._get_all_blocks(), ALL_SR_BLOCKS)

def test_SecondReprIF_post_init_invalid_substack_blocks():
    scripts = deepcopy(ALL_SR_SCRIPTS)
    scripts[6].blocks[0].inputs["THEN"].blocks = {}
    sr_if = SecondReprIF(scripts=scripts)
    assert not lists_equal_ignore_order(sr_if._get_all_blocks(), ALL_SR_BLOCKS)

def test_SecondReprIF_post_init_invalid_script_blocks():
    scripts = deepcopy(ALL_SR_SCRIPTS)
    scripts[0].blocks = {}
    sr_if = SecondReprIF(scripts=scripts)
    assert not lists_equal_ignore_order(sr_if._get_all_blocks(), ALL_SR_BLOCKS)

def test_SecondReprIF_post_init_invalid_script_block():
    scripts = deepcopy(ALL_SR_SCRIPTS)
    scripts[0].blocks[0] = ...
    sr_if = SecondReprIF(scripts=scripts)
    assert not lists_equal_ignore_order(sr_if._get_all_blocks(), ALL_SR_BLOCKS)


def test_SecondReprIF_get_all_blocks(sr_if: SecondReprIF):
    sr_if_copy = deepcopy(sr_if)
    assert lists_equal_ignore_order(sr_if_copy._get_all_blocks(), ALL_SR_BLOCKS)
    assert sr_if_copy == sr_if



def test_SecondToInterIF_get_next_block_id(sti_if: SecondToInterIF):
    sti_if_copy = deepcopy(sti_if)
    assert sti_if_copy.get_next_block_id() == "a"
    assert sti_if_copy._next_block_id_num == 2
    sti_if_copy._next_block_id_num -= 1
    assert sti_if_copy == sti_if


def test_SecondToInterIF_schedule_block_addition(sti_if: SecondToInterIF):
    sti_if_copy = deepcopy(sti_if)
    irblock = IRBlock(
        opcode="operator_trueBoolean",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=None,
        position=None,
        next=None,
        is_top_level=False,
    ),
    sti_if_copy.schedule_block_addition("a", irblock)
    assert sti_if_copy.produced_blocks == {"a": irblock}
    sti_if_copy.produced_blocks = {}
    assert sti_if_copy == sti_if


def test_SecondToInterIF_get_cb_mutation(sti_if: SecondToInterIF):
    sti_if_copy = deepcopy(sti_if)
    assert sti_if_copy.get_cb_mutation(SR_BLOCK_CUSTOM_OPCODE) == sti_if_copy.cb_mutations[SR_BLOCK_CUSTOM_OPCODE]
    assert sti_if_copy == sti_if

def test_SecondToInterIF_get_cb_mutation_invalid_custom_opcode(sti_if: SecondToInterIF):
    sti_if_copy = deepcopy(sti_if)
    with raises(ConversionError):
        sti_if_copy.get_cb_mutation(SRCustomBlockOpcode(segments=("hi")))
    assert sti_if_copy == sti_if



def test_ValidationIF_get_cb_mutation(validation_if: ValidationIF):
    validation_if_copy = deepcopy(validation_if)
    assert validation_if_copy.get_cb_mutation(SR_BLOCK_CUSTOM_OPCODE) == validation_if.cb_mutations[SR_BLOCK_CUSTOM_OPCODE]
    assert validation_if_copy == validation_if

def test_ValidationIF_get_cb_mutation_invalid_custom_opcode(validation_if: ValidationIF):
    validation_if_copy = deepcopy(validation_if)
    with raises(ValidationError):
        validation_if_copy.get_cb_mutation(SRCustomBlockOpcode(segments=("hi")))
    assert validation_if_copy == validation_if


