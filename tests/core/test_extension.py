from pypenguin.utility import InvalidValueError

from pypenguin.core.extension import SRExtension, SRCustomExtension

from tests.utility import execute_attr_validation_tests



def test_SRExtension_validate():
    extension = SRExtension(id="videoSensing")
    extension.validate([])

    execute_attr_validation_tests(
        obj=extension,
        attr_tests=[
            ("id", "some-invalid-id", InvalidValueError),
        ],
        validate_func=SRExtension.validate,
        func_args=[[]]
    )



def test_SRCustomExtension_validate_url():
    extension = SRCustomExtension(id="truefantombase", url="https://extensions.turbowarp.org/true-fantom/base.js")
    extension.validate([])

    execute_attr_validation_tests(
        obj=extension,
        attr_tests=[
            ("url", "x://a.b.c", InvalidValueError),
        ],
        validate_func=SRCustomExtension.validate,
        func_args=[[]]
    )

def test_SRCustomExtension_validate_js_uri():
    extension = SRCustomExtension(id="truefantombase", url="data:application/javascript,class%20HelloWorld%20%7B%0A%20%20getInfo%28%29%20%7B%0A%20%20%20%20return%20%7B%0A%20%20%20%20%20%20id%3A%20%27helloworld%27%2C%0A%20%20%20%20%20%20name%3A%20%27It%20works%21%27%2C%0A%20%20%20%20%20%20blocks%3A%20%5B%0A%20%20%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%20%20opcode%3A%20%27hello%27%2C%0A%20%20%20%20%20%20%20%20%20%20blockType%3A%20Scratch.BlockType.REPORTER%2C%0A%20%20%20%20%20%20%20%20%20%20text%3A%20%27Hello%21%27%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%5D%0A%20%20%20%20%7D%3B%0A%20%20%7D%0A%0A%20%20hello%28%29%20%7B%0A%20%20%20%20return%20%27World%21%27%3B%0A%20%20%7D%0A%7D%0A%0AScratch.extensions.register%28new%20HelloWorld%28%29%29%3B")
    extension.validate([])

    execute_attr_validation_tests(
        obj=extension,
        attr_tests=[
            ("url", "x:a/b,Lorem%20ipsum%20dolor%20sit%20amet%2C%20consetetur%20sadipscing%20elitr%2C%20sed%20diam", InvalidValueError),
        ],
        validate_func=SRCustomExtension.validate,
        func_args=[[]]
    )

