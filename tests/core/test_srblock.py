from copy        import copy, deepcopy
from dataclasses import field
from pytest      import fixture, raises

from pmp_manip.important_consts import NEW_OPCODE_POLYGON
from pmp_manip.opcode_info.api  import DropdownValueKind, OpcodeType, BuiltinInputType, InputMode
from pmp_manip.opcode_info.data import info_api
from pmp_manip.utility          import (
    grepr_dataclass, AbstractTreePath, 
    MANIP_ConversionError,
    MANIP_TypeValidationError, MANIP_RangeValidationError, MANIP_InvalidOpcodeError, MANIP_InvalidBlockShapeError,
    MANIP_UnnecessaryInputError, MANIP_MissingInputError, MANIP_UnnecessaryDropdownError, MANIP_MissingDropdownError,
)

from pmp_manip.core.block_interface import SecondToInterIF, ValidationIF
from pmp_manip.core.block           import (
    get_input_cls_for_input_mode,
    IRBlock, IRInputValue,
    SRScript, SRBlock, SRInputValue, 
    SRBlockAndTextInputValue, SRBlockAndDropdownInputValue, SRBlockAndBoolInputValue,
    SRBlockOnlyInputValue, SRScriptInputValue, SREmbeddedBlockInputValue,
)
from pmp_manip.core.context         import CompleteContext
from pmp_manip.core.dropdown        import SRDropdownValue


from tests.core.constants import ALL_IR_BLOCKS, ALL_SR_SCRIPTS

from tests.utility import execute_attr_validation_tests


@fixture
def info_api_extended1():
    info_api_extended = copy(info_api)
    info_api_extended.opcode_info = copy(info_api.opcode_info) 
    # make sure the internals of the DualKeyDict are shallow copied as well
    from tests._gen_ext_opcode_info_.music import extension
    info_api_extended.add_group(extension)
    return info_api_extended

@fixture
def info_api_extended2():
    info_api_extended = copy(info_api)
    info_api_extended.opcode_info = copy(info_api.opcode_info) 
    # make sure the internals of the DualKeyDict are shallow copied as well
    from tests._gen_ext_opcode_info_.pen import extension
    info_api_extended.add_group(extension)
    return info_api_extended

@fixture
def validation_if():
    return ValidationIF(scripts=ALL_SR_SCRIPTS)

@fixture
def context():
    return CompleteContext(
        scope_variables=[(DropdownValueKind.VARIABLE, "my variable")],
        scope_lists=[(DropdownValueKind.LIST, "my list")],

        global_variables=[(DropdownValueKind.VARIABLE, "my variable")],

        local_variables={},
        local_lists={},

        other_sprites=[],
        backdrops=[],
        costumes=[],
        sounds=[],

        is_stage=False,
    )

@grepr_dataclass(grepr_fields=["_block_ids"])
class TEST_SecondToInterIF(SecondToInterIF):
    _block_ids: list[str] = field(default_factory=list)

    def get_next_block_id(self) -> str:
        block_id = self._block_ids[self._next_block_id_num - 1]
        self._next_block_id_num += 1
        return block_id




def test_get_input_cls_for_input_mode():
    assert get_input_cls_for_input_mode(InputMode.BLOCK_AND_BOOL) is SRBlockAndBoolInputValue



def test_SRScript_validate(validation_if, context):        
    srscript = ALL_SR_SCRIPTS[0]
    srscript.validate(AbstractTreePath(), info_api, validation_if, context)

    execute_attr_validation_tests(
        obj=srscript,
        attr_tests=[
            ("position", 5, MANIP_TypeValidationError),
            ("blocks", {}, MANIP_TypeValidationError),
            ("blocks", [8], MANIP_TypeValidationError),
            ("blocks", [], MANIP_RangeValidationError),
        ],
        validate_func=SRScript.validate,
        func_args=[AbstractTreePath(), info_api, validation_if, context],
    )


def test_SRScript_to_inter():
    sti_if = TEST_SecondToInterIF(scripts=ALL_SR_SCRIPTS, _block_ids=["d", "b", "t", "e", "u", "v"])
    srscript = ALL_SR_SCRIPTS[0]
    top_level_id = srscript.to_inter(
        sti_if=sti_if,
        info_api=info_api,
    )
    assert top_level_id == "d"
    assert sti_if.produced_blocks == {
        id: ALL_IR_BLOCKS[id]
        for id in {"d", "b", "t", "e", "u", "v"}
    }



def test_SRBlock_validate(validation_if, context):
    srblock = ALL_SR_SCRIPTS[0].blocks[0]
    srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)

    execute_attr_validation_tests(
        obj=srblock,
        attr_tests=[
            ("opcode", {}, MANIP_TypeValidationError),
            ("opcode", "some_undefined_opcode", MANIP_InvalidOpcodeError),
            ("inputs", {5:6}, MANIP_TypeValidationError),
            ("dropdowns", [], MANIP_TypeValidationError),
            ("comment", 89, MANIP_TypeValidationError),
            ("mutation", "hi", MANIP_TypeValidationError),
        ],
        validate_func=SRBlock.validate,
        func_args=[AbstractTreePath(), info_api, validation_if, context, False],
    )

def test_SRBlock_validate_reporter(validation_if, context):
    srblock = ALL_SR_SCRIPTS[1].blocks[0]
    srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=True, expects_embedded=False)

def test_SRBlock_validate_cb_def(validation_if, context):
    srblock = ALL_SR_SCRIPTS[4].blocks[0]
    srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)   

def test_SRBlock_validate_unexpected_mutation(validation_if, context):
    srblock = copy(ALL_SR_SCRIPTS[0].blocks[1])
    srblock.mutation = {...}
    with raises(MANIP_TypeValidationError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)

def test_SRBlock_validate_missing_mutation(validation_if, context):
    srblock = copy(ALL_SR_SCRIPTS[4].blocks[0])
    srblock.mutation = None
    with raises(MANIP_TypeValidationError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)

def test_SRBlock_validate_invalid_reporter_shape(validation_if, context):
    srblock = ALL_SR_SCRIPTS[0].blocks[0]
    with raises(MANIP_InvalidBlockShapeError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=True, expects_embedded=False)

def test_SRBlock_validate_missing_embedded_block(validation_if, context):
    srblock = ALL_SR_SCRIPTS[10].blocks[0]
    with raises(MANIP_InvalidBlockShapeError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=True)

def test_SRBlock_validate_unexpected_embedded_block(validation_if, context, info_api_extended2):
    srblock = ALL_SR_SCRIPTS[11].blocks[0].inputs["SHAPE"].block
    with raises(MANIP_InvalidBlockShapeError):
        srblock.validate(AbstractTreePath(), info_api_extended2, validation_if, context, expects_reporter=False, expects_embedded=False)

def test_SRBlock_validate_unexpected_input(validation_if, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[6].blocks[0])
    srblock.inputs["SOME_ID"] = SRBlockOnlyInputValue(block=None)
    with raises(MANIP_UnnecessaryInputError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)

def test_SRBlock_validate_missing_input(validation_if, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[6].blocks[0])
    del srblock.inputs["CONDITION"]
    with raises(MANIP_MissingInputError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)

def test_SRBlock_validate_unexpected_dropdown(validation_if, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[2].blocks[0])
    srblock.dropdowns["SOME_ID"] = SRDropdownValue(kind=DropdownValueKind.STANDARD, value="something")
    with raises(MANIP_UnnecessaryDropdownError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=True, expects_embedded=False)

def test_SRBlock_validate_missing_dropdown(validation_if, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[2].blocks[0])
    del srblock.dropdowns["VARIABLE"]
    with raises(MANIP_MissingDropdownError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=True, expects_embedded=False)

def test_SRBlock_validate_post_handler(validation_if, context):
    srblock = ALL_SR_SCRIPTS[3].blocks[0]
    srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)

def test_SRBlock_validate_invalid_input_cls(validation_if, context):
    srblock = deepcopy(ALL_SR_SCRIPTS[0].blocks[0])
    srblock.inputs["MESSAGE"] = SRBlockOnlyInputValue(block=None)
    with raises(MANIP_TypeValidationError):
        srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)

def test_SRBlock_validate_editor_button(validation_if, context):
    srblock = ALL_SR_SCRIPTS[12].blocks[0]
    srblock.validate(AbstractTreePath(), info_api, validation_if, context, expects_reporter=False, expects_embedded=False)


def test_SRBlock_validate_opcode_type():
    reporter_tests = [
        (True , 0b000), (True , 0b001), (True , 0b010), (True , 0b011),
        (True , 0b100), (True , 0b101), (True , 0b110), (False, 0b111),
    ]
    sub_tests = [ # should_raise, (is_top_level, is_first, is_last)
        (OpcodeType.STATEMENT       , [
            (False, 0b000), (False, 0b001), (False, 0b010), (False, 0b011),
            (False, 0b100), (False, 0b101), (False, 0b110), (False, 0b111),
        ]),
        (OpcodeType.ENDING_STATEMENT, [
            (True , 0b000), (False, 0b001), (True , 0b010), (False, 0b011),
            (True , 0b100), (False, 0b101), (True , 0b110), (False, 0b111),
        ]),
        (OpcodeType.HAT             , [
            (True , 0b000), (True , 0b001), (True , 0b010), (True , 0b011),
            (True , 0b100), (True , 0b101), (False, 0b110), (False, 0b111),
        ]),
        (OpcodeType.STRING_REPORTER , reporter_tests),
        (OpcodeType.NUMBER_REPORTER , reporter_tests),
        (OpcodeType.BOOLEAN_REPORTER, reporter_tests),
        (OpcodeType.EMBEDDED        , [
            (False, 0b000), (False, 0b001), (False, 0b010), (False, 0b011),
            (False, 0b100), (False, 0b101), (False, 0b110), (False, 0b111),
        ]),
    ]
    for opcode_type, items in sub_tests:
        for should_raise, flags in items:
            is_top_level = bool((flags        )//0b100)
            is_first     = bool((flags % 0b100)//0b010)
            is_last      = bool((flags % 0b010)//0b001)
            if should_raise:
                with raises(MANIP_InvalidBlockShapeError):
                    SRBlock.validate_opcode_type(
                        path         = AbstractTreePath(),
                        opcode_type  = opcode_type,
                        is_top_level = is_top_level,
                        is_first     = is_first,
                        is_last      = is_last,
                    )
            else:
                SRBlock.validate_opcode_type(
                    path         = AbstractTreePath(),
                    opcode_type  = opcode_type,
                    is_top_level = is_top_level,
                    is_first     = is_first,
                    is_last      = is_last,
                )


def test_SRBlock_find_broadcast_messages_send():
    srblock = ALL_SR_SCRIPTS[0].blocks[0]
    assert srblock.find_broadcast_messages() == ["my message"]

def test_SRBlock_find_broadcast_messages_receive():
    srblock = ALL_SR_SCRIPTS[8].blocks[0]
    assert srblock.find_broadcast_messages() == ["my message"]

def test_SRBlock_find_broadcast_messages_script_none():
    srblock = ALL_SR_SCRIPTS[6].blocks[0]
    assert srblock.find_broadcast_messages() == []



def test_SRBlock_to_inter_block_and_text_block_and_bool():
    sti_if = TEST_SecondToInterIF(scripts=ALL_SR_SCRIPTS, _block_ids=["k", "l", "x"])
    script = ALL_SR_SCRIPTS[4]
    srblock = script.blocks[0]
    irblock = srblock.to_inter(
        sti_if=sti_if,
        info_api=info_api,
        next=None,
        position=script.position,
        is_top_level=True,
    )
    assert irblock == ALL_IR_BLOCKS["c"]
    assert sti_if.produced_blocks == {
        id: ALL_IR_BLOCKS[id]
        for id in {"k", "l", "x"}
    }

def test_SRBlock_to_inter_script_block1():
    sti_if = TEST_SecondToInterIF(scripts=ALL_SR_SCRIPTS, _block_ids=[])
    script = ALL_SR_SCRIPTS[0]
    srblock = script.blocks[0]
    irblock = srblock.to_inter(
        sti_if=sti_if,
        info_api=info_api,
        next="b",
        position=script.position,
        is_top_level=True,
    )
    assert irblock == ALL_IR_BLOCKS["d"]
    assert sti_if.produced_blocks == {
        id: ALL_IR_BLOCKS[id]
        for id in {}
    }

def test_SRBlock_to_inter_script_block2_and_menu():
    sti_if = TEST_SecondToInterIF(scripts=ALL_SR_SCRIPTS, _block_ids=["e"])
    script = ALL_SR_SCRIPTS[0]
    srblock = script.blocks[1]
    irblock = srblock.to_inter(
        sti_if=sti_if,
        info_api=info_api,
        next="t",
        position=None,
        is_top_level=False,
    )
    assert irblock == ALL_IR_BLOCKS["b"]
    assert sti_if.produced_blocks == {
        id: ALL_IR_BLOCKS[id]
        for id in {"e"}
    }


def test_SRBlock_to_inter_substack():
    sti_if = TEST_SecondToInterIF(scripts=ALL_SR_SCRIPTS, _block_ids=["y", "o", "q"])
    script = ALL_SR_SCRIPTS[6]
    srblock = script.blocks[0]
    irblock = srblock.to_inter(
        sti_if=sti_if,
        info_api=info_api,
        next=None,
        position=script.position,
        is_top_level=True,
    )
    assert irblock == ALL_IR_BLOCKS["n"]
    assert sti_if.produced_blocks == {
        id: ALL_IR_BLOCKS[id]
        for id in {"y", "o", "q"}
    }

def test_SRBlock_to_inter_immediate_block():
    sti_if = TEST_SecondToInterIF(scripts=ALL_SR_SCRIPTS, _block_ids=["g"])
    script = ALL_SR_SCRIPTS[1]
    srblock = script.blocks[0]
    irblock = srblock.to_inter(
        sti_if=sti_if,
        info_api=info_api,
        next=None,
        position=script.position,
        is_top_level=True,
    )
    assert irblock == ALL_IR_BLOCKS["f"]
    assert sti_if.produced_blocks == {
        id: ALL_IR_BLOCKS[id]
        for id in {"g"}
    }

def test_SRBlock_to_inter_dropdown():
    sti_if = TEST_SecondToInterIF(scripts=ALL_SR_SCRIPTS, _block_ids=[])
    script = ALL_SR_SCRIPTS[7]
    srblock = script.blocks[0]
    irblock = srblock.to_inter(
        sti_if=sti_if,
        info_api=info_api,
        next=None,
        position=script.position,
        is_top_level=True,
    )
    assert irblock == ALL_IR_BLOCKS["r"]
    assert sti_if.produced_blocks == {
        id: ALL_IR_BLOCKS[id]
        for id in {}
    }

def test_SRBlock_to_inter_invalid_sub_script():
    sti_if = TEST_SecondToInterIF(scripts=ALL_SR_SCRIPTS, _block_ids=["y"]) # "y": needed for generated checkbox block
    script = ALL_SR_SCRIPTS[6]
    srblock = deepcopy(script.blocks[0])
    srblock.inputs["THEN"].blocks = ["some invalid stuff"]
    with raises(MANIP_ConversionError):
        srblock.to_inter(
            sti_if=sti_if,
            info_api=info_api,
            next=None,
            position=script.position,
            is_top_level=True,
        )

def test_SRBlock_to_inter_block_and_menu_text(info_api_extended1):
    # this test uses the scratch music extension and a seperate blocks/scripts environment
    sti_if = TEST_SecondToInterIF(scripts=[], _block_ids=["a", "b"])
    script = SRScript(
        position=(311, 505), 
        blocks=[
            SRBlock(
                opcode="&music::play note ([NOTE]) for (BEATS) beats",
                inputs={
                    "NOTE": SRBlockAndDropdownInputValue(
                        block=None,
                        dropdown=SRDropdownValue(kind=DropdownValueKind.STANDARD, value="60"),
                    ),
                    "BEATS": SRBlockAndTextInputValue(block=None, immediate="0.25"),
                },
                dropdowns={},
                comment=None,
                mutation=None,
            )
        ]
    )
    srblock = script.blocks[0]
    irblock = srblock.to_inter(
        sti_if=sti_if,
        info_api=info_api_extended1,
        next=None,
        position=script.position,
        is_top_level=True,
    )
    assert irblock == IRBlock(
        opcode="music_playNoteForBeats",
        inputs={
            "NOTE": IRInputValue(
                mode=InputMode.BLOCK_AND_MENU_TEXT,
                references=["a"],
                immediate_block=None,
                text=None,
            ),
            "BEATS": IRInputValue(
                mode=InputMode.BLOCK_AND_TEXT,
                references=[],
                immediate_block=None,
                text="0.25",
            ),
        },
        dropdowns={},
        comment=None,
        mutation=None,
        position=(311, 505),
        next=None,
        is_top_level=True,
    )
    assert sti_if.produced_blocks == {
        "a": IRBlock(
            opcode="note",
            inputs={},
            dropdowns={
                "NOTE": "60",
            },
            comment=None,
            mutation=None,
            position=None,
            next=None,
            is_top_level=False,
        )
    }

def test_SRBlock_to_inter_block_only():
    sti_if = TEST_SecondToInterIF(scripts=[], _block_ids=["C", "B"])
    script = ALL_SR_SCRIPTS[10]
    srblock = script.blocks[0]
    irblock = srblock.to_inter(
        sti_if=sti_if,
        info_api=info_api,
        next=None,
        position=script.position,
        is_top_level=True,
    )
    assert irblock == ALL_IR_BLOCKS["B"]
    assert sti_if.produced_blocks == {
        id: ALL_IR_BLOCKS[id]
        for id in {"C"}
    }


def test_SRInputValue_from_mode_block_and_text():
    input_value = SRInputValue.from_mode(
        mode=InputMode.BLOCK_AND_TEXT,
        block=ALL_SR_SCRIPTS[1].blocks[0],
        immediate="hi :)",
    )
    assert input_value == SRBlockAndTextInputValue(
        block=ALL_SR_SCRIPTS[1].blocks[0],
        immediate="hi :)"
    )


def test_SRInputValue_from_mode_block_and_dropdown():
    input_value1 = SRInputValue.from_mode(
        mode=InputMode.BLOCK_AND_DROPDOWN,
        block=ALL_SR_SCRIPTS[1].blocks[0],
        dropdown=SRDropdownValue(kind=DropdownValueKind.OBJECT, value="mouse-pointer"),
    )
    input_value2 = SRInputValue.from_mode(
        mode=InputMode.BLOCK_AND_BROADCAST_DROPDOWN,
        block=ALL_SR_SCRIPTS[1].blocks[0],
        dropdown=SRDropdownValue(kind=DropdownValueKind.OBJECT, value="mouse-pointer"),
    )
    assert input_value1 == SRBlockAndDropdownInputValue(
        block=ALL_SR_SCRIPTS[1].blocks[0],
        dropdown=SRDropdownValue(kind=DropdownValueKind.OBJECT, value="mouse-pointer"),
    )
    assert input_value1 == input_value2

def test_SRInputValue_from_mode_block_only():
    input_value = SRInputValue.from_mode(
        mode=InputMode.BLOCK_ONLY,
        block=ALL_SR_SCRIPTS[1].blocks[0],
    )
    assert input_value == SRBlockOnlyInputValue(
        block=ALL_SR_SCRIPTS[1].blocks[0],
    )

def test_SRInputValue_from_mode_script():
    input_value = SRInputValue.from_mode(
        mode=InputMode.SCRIPT,
        blocks=ALL_SR_SCRIPTS[6].blocks[0].inputs["THEN"].blocks,
    )
    assert input_value == SRScriptInputValue(
        blocks=ALL_SR_SCRIPTS[6].blocks[0].inputs["THEN"].blocks,
    )


def test_SRInputValue_validate_block(validation_if, context):
    input_value = SRBlockAndDropdownInputValue(
        block=ALL_SR_SCRIPTS[5].blocks[0],
        dropdown=SRDropdownValue(kind=DropdownValueKind.BROADCAST_MSG, value="my message"),
    )
    input_value._validate_block(AbstractTreePath(), info_api, validation_if, context)


def test_SRBlockAndTextInputValue_validate(validation_if, context):
    input_type = BuiltinInputType.TEXT
    input_value = SRBlockAndTextInputValue(
        block=ALL_SR_SCRIPTS[1].blocks[0],
        immediate="some random text",
    )
    input_value.validate(AbstractTreePath(), info_api, validation_if, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("block", 5, MANIP_TypeValidationError),
            ("immediate", {}, MANIP_TypeValidationError),
        ],
        validate_func=SRBlockAndTextInputValue.validate,
        func_args=[AbstractTreePath(), info_api, validation_if, context, input_type],
    )

def test_SRBlockAndDropdownInputValue_validate(validation_if, context):
    input_type = BuiltinInputType.MOUSE_OR_OTHER_SPRITE
    input_value = SRBlockAndDropdownInputValue(
        block=ALL_SR_SCRIPTS[5].blocks[0],
        dropdown=SRDropdownValue(kind=DropdownValueKind.OBJECT, value="mouse-pointer"),
    )
    input_value.validate(AbstractTreePath(), info_api, validation_if, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("block", 5, MANIP_TypeValidationError),
            ("dropdown", {}, MANIP_TypeValidationError),
        ],
        validate_func=SRBlockAndDropdownInputValue.validate,
        func_args=[AbstractTreePath(), info_api, validation_if, context, input_type],
    )

def test_SRBlockAndBoolInputValue_validate(validation_if, context):
    input_type = BuiltinInputType.BOOLEAN
    input_value = SRBlockAndBoolInputValue(
        block=ALL_SR_SCRIPTS[1].blocks[0],
        immediate=True,
    )
    input_value.validate(AbstractTreePath(), info_api, validation_if, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("block", 5.7, MANIP_TypeValidationError),
            ("immediate", "hi", MANIP_TypeValidationError),
        ],
        validate_func=SRBlockAndBoolInputValue.validate,
        func_args=[AbstractTreePath(), info_api, validation_if, context, input_type],
    )

def test_SRBlockOnlyInputValue_validate(validation_if, context):
    input_type = BuiltinInputType.BOOLEAN
    input_value = SRBlockOnlyInputValue(
        block=None,
    )
    input_value.validate(AbstractTreePath(), info_api, validation_if, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("block", 5, MANIP_TypeValidationError),
        ],
        validate_func=SRBlockOnlyInputValue.validate,
        func_args=[AbstractTreePath(), info_api, validation_if, context, input_type],
    )

def test_SRScriptInputValue_validate(validation_if, context):
    input_type = BuiltinInputType.SCRIPT
    input_value = SRScriptInputValue(
        blocks=ALL_SR_SCRIPTS[0].blocks,
    )
    input_value.validate(AbstractTreePath(), info_api, validation_if, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("blocks", 9, MANIP_TypeValidationError),
            ("blocks", [{}], MANIP_TypeValidationError),
        ],
        validate_func=SRScriptInputValue.validate,
        func_args=[AbstractTreePath(), info_api, validation_if, context, input_type],
    )

def test_SREmbeddedBlockInputValue_validate(validation_if, context):
    input_type = BuiltinInputType.POLYGON
    input_value = SREmbeddedBlockInputValue(
        block=SRBlock(
            opcode=NEW_OPCODE_POLYGON,
            inputs={
                "X1": SRBlockAndTextInputValue(block=None, immediate="-43.30127018922194"),
                "Y1": SRBlockAndTextInputValue(block=None, immediate="-24.999999999999996"),
                "X2": SRBlockAndTextInputValue(block=None, immediate="43.30127018922194"),
                "Y2": SRBlockAndTextInputValue(block=None, immediate="-24.999999999999996"),
                "X3": SRBlockAndTextInputValue(block=None, immediate="3.061616997868383e-15"),
                "Y3": SRBlockAndTextInputValue(block=None, immediate="50"),
            },
            dropdowns={
                "UNTOUCHED": SRDropdownValue(kind=DropdownValueKind.STANDARD, value=False),
            },
            comment=None,
            mutation=None,
        ),
    )
    input_value.validate(AbstractTreePath(), info_api, validation_if, context, input_type)
    
    execute_attr_validation_tests(
        obj=input_value,
        attr_tests=[
            ("block", 7, MANIP_TypeValidationError),
            ("block", None, MANIP_TypeValidationError),
        ],
        validate_func=SREmbeddedBlockInputValue.validate,
        func_args=[AbstractTreePath(), info_api, validation_if, context, input_type],
    )
