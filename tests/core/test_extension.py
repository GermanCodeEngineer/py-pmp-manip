from pytest import fixture

from pypenguin.utility import ValidationConfig, InvalidValueError

from pypenguin.core.extension import SRExtension, SRCustomExtension

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()



def test_SRExtension_validate(config):
    extension = SRExtension(id="videoSensing")
    extension.validate([], config)

    execute_attr_validation_tests(
        obj=extension,
        attr_tests=[
            ("id", "some-invalid-id", InvalidValueError),
        ],
        validate_func=SRExtension.validate,
        func_args=[[], config]
    )



def test_SRCustomExtension_validate(config):
    extension = SRExtension(id="jgJSON", url="https://extensions.turbowarp.org/true-fantom/base.js")
    extension.validate([], config)

    execute_attr_validation_tests(
        obj=extension,
        attr_tests=[
            ("id", "some-invalid-id", InvalidValueError),
        ],
        validate_func=SRExtension.validate,
        func_args=[[], config]
    )

