from pypenguin.utility import TypeValidationError, InvalidValueError

from pypenguin.core.comment import FRComment, SRComment

from tests.utility import execute_attr_validation_tests


RAW_COMMENT_DATA_ATTACHED = {
    "blockId": "a",
    "x": 100,
    "y": 200,
    "width": 150,
    "height": 80,
    "minimized": False,
    "text": "This is an attached comment",
}

RAW_COMMENT_DATA_FLOATING = {
    "blockId": None,
    "x": 10,
    "y": 20,
    "width": 52,
    "height": 32,
    "minimized": True,
    "text": "Floating comment here",
}


def test_FRComment_from_data():
    data = RAW_COMMENT_DATA_ATTACHED
    frcomment = FRComment.from_data(data)
    assert frcomment.block_id == data["blockId"]
    assert frcomment.x == data["x"]
    assert frcomment.y == data["y"]
    assert frcomment.width == data["width"]
    assert frcomment.height == data["height"]
    assert frcomment.minimized == data["minimized"]
    assert frcomment.text == data["text"]


def test_FRComment_to_data():
    frcomment = FRComment(
        block_id=None,
        x=10,
        y=20,
        width=52,
        height=32,
        minimized=True,
        text="Floating comment here",
    )
    assert frcomment.to_data() == RAW_COMMENT_DATA_FLOATING


def test_FRComment_to_second_attached():
    frcomment = FRComment.from_data(RAW_COMMENT_DATA_ATTACHED)
    is_attached, srcomment = frcomment.to_second()
    assert is_attached is True
    assert isinstance(srcomment, SRComment)
    assert srcomment.position == (frcomment.x, frcomment.y)
    assert srcomment.size == (frcomment.width, frcomment.height)
    assert srcomment.is_minimized == frcomment.minimized
    assert srcomment.text == frcomment.text

def test_FRComment_to_second_floating():
    frcomment = FRComment.from_data(RAW_COMMENT_DATA_FLOATING)
    is_attached, srcomment = frcomment.to_second()
    assert is_attached is False
    assert isinstance(srcomment, SRComment)
    assert srcomment.position == (frcomment.x, frcomment.y)
    assert srcomment.size == (frcomment.width, frcomment.height)
    assert srcomment.is_minimized == frcomment.minimized
    assert srcomment.text == frcomment.text



def test_SRComment_validate():
    srcomment = SRComment(
        position=(10, 10),
        size=(52, 32),
        is_minimized=False,
        text="Comment text",
    )
    srcomment.validate(path=[])

    execute_attr_validation_tests(
        obj=srcomment,
        attr_tests=[
            ("position", [10], TypeValidationError),
            ("size", 50, TypeValidationError),
            ("size", (30, 30), InvalidValueError),  # Too small
            ("is_minimized", "nope", TypeValidationError),
            ("text", {}, TypeValidationError),
        ],
        validate_func=SRComment.validate,
        func_args=[[]],
    )


def test_SRComment_to_first():
    srcomment = SRComment(
        position=(100, 200),
        size=(150, 80),
        is_minimized=True,
        text="hi :)",
    )
    assert srcomment.to_first(block_id="qqq") == FRComment(
        block_id="qqq",
        x=100,
        y=200,
        width=150,
        height=80,
        minimized=True,
        text="hi :)",
    )

