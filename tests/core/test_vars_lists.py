from pytest import fixture

from pypenguin.important_consts import SHA256_SEC_VARIABLE, SHA256_SEC_LIST
from pypenguin.utility          import string_to_sha256, ValidationConfig, TypeValidationError

from pypenguin.core.vars_lists import variable_sha256, list_sha256, SRVariable, SRCloudVariable, SRList

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()



def test_variable_sha256():
    result = variable_sha256("a var", sprite_name="my sprite")
    expected = string_to_sha256("a var", secondary=SHA256_SEC_VARIABLE, tertiary="my sprite")
    assert result == expected



def test_list_sha256():
    result = list_sha256("a list", sprite_name="_stage_")
    expected = string_to_sha256("a list", secondary=SHA256_SEC_LIST, tertiary=None)
    assert result == expected



def test_SRVariable_validate(config):
    srvariable = SRVariable(
        name="a variable",
        current_value=35,
    )
    srvariable.validate(path=[], config=config)

    execute_attr_validation_tests(
        obj=srvariable,
        attr_tests=[
            ("name", {}, TypeValidationError),
            ("current_value", [], TypeValidationError),
        ],
        validate_func=SRVariable.validate,
        func_args=[[], config],
    )


def test_SRVariable_to_tuple():
    srvariable = SRVariable(
        name="a variable",
        current_value=35,
    )
    assert srvariable.to_tuple() == ("a variable", 35)



def test_SRCloudVariable_to_tuple():
    srvariable = SRCloudVariable(
        name="a variable",
        current_value=35,
    )
    assert srvariable.to_tuple() == ("a variable", 35, True)



def test_SRList_validate(config):
    srlist = SRList(
        name="a list",
        current_value=[5, -6.9, "hi", False],
    )
    srlist.validate(path=[], config=config)

    execute_attr_validation_tests(
        obj=srlist,
        attr_tests=[
            ("name", {}, TypeValidationError),
            ("current_value", {}, TypeValidationError),
        ],
        validate_func=SRList.validate,
        func_args=[[], config],
    )


def test_SRList_to_tuple():
    srlist = SRList(
        name="a list",
        current_value=[5, -6.9, "hi", False],
    )
    assert srlist.to_tuple() == ("a list", [5, -6.9, "hi", False])
