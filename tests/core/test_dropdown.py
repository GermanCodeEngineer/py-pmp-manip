from pytest import fixture, raises

from pypenguin.utility     import ValidationConfig, TypeValidationError, InvalidDropdownValueError
from pypenguin.opcode_info import DropdownType, DropdownValueKind

from pypenguin.core.context import PartialContext
from pypenguin.core.dropdown import SRDropdownValue

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()

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

def test_SRDropdownValue_validate(config):
    dropdown_value = SRDropdownValue(kind=DropdownValueKind.SPRITE, value="Player")
    
    execute_attr_validation_tests(
        obj=dropdown_value,
        attr_tests=[
            ("kind", {}, TypeValidationError),
            ("value", set(), TypeValidationError),
        ],
        validate_func=SRDropdownValue.validate,
        func_args=[[], config],
    )

def test_SRDropdownValue_validate_value(context):
    dropdown_value = SRDropdownValue(kind=DropdownValueKind.SPRITE, value="Player")
    dropdown_value.validate_value([], DropdownType.MOUSE_OR_OTHER_SPRITE, context)

    execute_attr_validation_tests(
        obj=dropdown_value,
        attr_tests=[
            ("value", "a non existing sprite", InvalidDropdownValueError),
        ],
        validate_func=SRDropdownValue.validate_value,
        func_args=[[], DropdownType.MOUSE_OR_OTHER_SPRITE, context],
    )


