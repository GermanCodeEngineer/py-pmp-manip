from pytest import fixture, raises

from pypenguin.utility import ValidationConfig, TypeValidationError, InvalidValueError

from pypenguin.core.vars_lists import SRVariable, SRList

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()



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

