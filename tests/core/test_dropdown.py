from pytest import fixture, raises

from pypenguin.opcode_info.api import BuiltinDropdownType, DropdownValueKind
from pypenguin.utility         import PP_TypeValidationError, PP_InvalidDropdownValueError

from pypenguin.core.context  import PartialContext
from pypenguin.core.dropdown import SRDropdownValue

from tests.utility import execute_attr_validation_tests

@fixture
def context():
    my_variable = (DropdownValueKind.VARIABLE, "my variable")
    my_sprite_variable = (DropdownValueKind.VARIABLE, "my sprite variable")
    my_list = (DropdownValueKind.LIST, "my list")
    my_sprite_list = (DropdownValueKind.LIST, "my sprite list")
    return PartialContext(
        scope_variables=[my_variable, my_sprite_variable],
        scope_lists=[my_list, my_sprite_list],

        all_sprite_variables=[my_variable],

        sprite_only_variables=[my_sprite_variable],
        sprite_only_lists=[my_sprite_list],

        other_sprites=[(DropdownValueKind.SPRITE, "Sprite2"), (DropdownValueKind.SPRITE, "Player")],
        backdrops=[(DropdownValueKind.BACKDROP, "intro"), (DropdownValueKind.BACKDROP, "scene1")],
    )



def test_SRDropdownValue_from_tuple():
    dropdown_value = SRDropdownValue.from_tuple((DropdownValueKind.SPRITE, "Player"))
    assert isinstance(dropdown_value, SRDropdownValue)
    assert dropdown_value.kind == DropdownValueKind.SPRITE
    assert dropdown_value.value == "Player"

def test_SRDropdownValue_to_tuple():
    dropdown_value = SRDropdownValue(kind=DropdownValueKind.SPRITE, value="Player")
    assert dropdown_value.to_tuple() == (DropdownValueKind.SPRITE, "Player")



def test_SRDropdownValue_validate():
    dropdown_value = SRDropdownValue(kind=DropdownValueKind.SPRITE, value="Player")
    
    execute_attr_validation_tests(
        obj=dropdown_value,
        attr_tests=[
            ("kind", {}, PP_TypeValidationError),
            ("value", set(), PP_TypeValidationError),
        ],
        validate_func=SRDropdownValue.validate,
        func_args=[[]],
    )


def test_SRDropdownValue_validate_value(context):
    dropdown_value = SRDropdownValue(kind=DropdownValueKind.SPRITE, value="Player")
    dropdown_value.validate_value([], BuiltinDropdownType.MOUSE_OR_OTHER_SPRITE, context)

    execute_attr_validation_tests(
        obj=dropdown_value,
        attr_tests=[
            ("value", "a non existing sprite", PP_InvalidDropdownValueError),
        ],
        validate_func=SRDropdownValue.validate_value,
        func_args=[[], BuiltinDropdownType.MOUSE_OR_OTHER_SPRITE, context],
    )

    dropdown_value = SRDropdownValue(kind=DropdownValueKind.SOUND, value="a message")
    with raises(PP_InvalidDropdownValueError):
        dropdown_value.validate_value([], BuiltinDropdownType.BROADCAST, context)

def test_SRDropdownValue_validate_value_with_post_validate_func(context):
    dropdown_value = SRDropdownValue(kind=DropdownValueKind.STANDARD, value="1011100011001100110100111")
    dropdown_value.validate_value([], BuiltinDropdownType.MATRIX, context)

    dropdown_value = SRDropdownValue(kind=DropdownValueKind.STANDARD, value="10110") # too short
    with raises(PP_InvalidDropdownValueError):
        dropdown_value.validate_value([], BuiltinDropdownType.MATRIX, context)
    
    dropdown_value = SRDropdownValue(kind=DropdownValueKind.STANDARD, value="2112022311310111012121112") # only 0 or 1 are allowed
    with raises(PP_InvalidDropdownValueError):
        dropdown_value.validate_value([], BuiltinDropdownType.MATRIX, context)


