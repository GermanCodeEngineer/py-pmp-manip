from json   import dumps
from pytest import fixture, raises

from pypenguin.utility import (
    DeserializationError, ConversionError, ThanksError, 
    ValidationConfig, TypeValidationError, InvalidValueError
)

from pypenguin.core.block_mutation import (
    FRMutation,
    FRCustomBlockArgumentMutation, FRCustomBlockMutation,
    FRCustomBlockCallMutation, FRStopScriptMutation,
    SRCustomBlockArgumentMutation, SRCustomBlockMutation,
    SRCustomBlockCallMutation, SRStopScriptMutation
)
from pypenguin.core.custom_block import SRCustomBlockOpcode, SRCustomBlockOptype

from tests.utility import execute_attr_validation_tests


class DummyAPI:
    argument_ids: list[str]
    argument_names: list[str]
    argument_defaults: list[str]
    
    def __init__(self, 
        argument_ids: list[str], 
        argument_names: list[str], 
        argument_defaults: list[str],
    ):
        self.argument_ids = argument_ids
        self.argument_names = argument_names
        self.argument_defaults = argument_defaults
    
    def get_cb_mutation(self, proccode: str) -> FRCustomBlockMutation:
        return FRCustomBlockMutation(
            tag_name="mutation",
            children=[],
            proccode=proccode,
            argument_ids=self.argument_ids,
            argument_names=self.argument_names,
            argument_defaults=self.argument_defaults,
            warp=False,
            returns=True,
            edited=True,
            optype="statement",
            color=("#ffffff", "#aaaaaa", "#000000"),
        )


@fixture
def api() -> DummyAPI:
    return DummyAPI(
        argument_ids=["|%aQk0nd}|c.tVn$e}ST"],
        argument_names=["boolean"],
        argument_defaults=[dumps(False)],
    )


def test_FRMutation_from_data_and_post_init():
    class DummyFRMutation(FRMutation):
        @classmethod
        def from_data(cls, data) -> "DummyFRMutation":
            return cls(
                tag_name = data["tagName" ],
                children = data["children"],
            )
        def to_second(self, ficapi): pass

    data = {
        "tagName": "mutation",
        "children": [],
    }
    frmutation = DummyFRMutation.from_data(data)
    assert isinstance(frmutation, DummyFRMutation)
    assert frmutation.tag_name == data["tagName"]
    assert frmutation.children == data["children"]

    with raises(ThanksError):
        DummyFRMutation.from_data({
            "tagName": "something else", # invalid
            "children": [],
        })
    
    with raises(ThanksError):
        DummyFRMutation.from_data({
            "tagName": "mutation",
            "children": {}, # invalid
        })


def test_FRCustomBlockArgumentMutation_from_data_and_to_second(api: DummyAPI):
    colors = ["#FF6680", "#FF4D6A", "#FF3355"]
    data = {
        "tagName": "mutation", 
        "children": [], 
        "color": dumps(colors),
    }
    frmutation = FRCustomBlockArgumentMutation.from_data(data)
    assert frmutation.color == tuple(colors)
    
    frmutation.store_argument_name("my_arg")
    srmutation = frmutation.to_second(api)
    assert isinstance(srmutation, SRCustomBlockArgumentMutation)
    assert srmutation.argument_name == "my_arg"
    assert srmutation.main_color == colors[0]
    assert srmutation.prototype_color == colors[1]
    assert srmutation.outline_color == colors[2]

def test_FRCustomBlockArgumentMutation_to_second_without_storing_argument(api: DummyAPI):
    data = {
        "tagName": "mutation",
        "children": [],
        "color": dumps(["#111111", "#222222", "#333333"]),
    }
    frmutation = FRCustomBlockArgumentMutation.from_data(data)

    with raises(ConversionError):
        frmutation.to_second(api)


def test_FRCustomBlockMutation_from_data_and_to_second(api: DummyAPI):
    warp = False
    returns = None
    edited = True
    optype = None
    colors = ["#FF6680", "#FF4D6A", "#FF3355"]
    data = {
        "tagName": "mutation", 
        "children": [], 
        "proccode": "do %b label text", 
        "argumentids": dumps(api.argument_ids), 
        "argumentnames": dumps(api.argument_names), 
        "argumentdefaults": dumps(api.argument_defaults), 
        "warp": dumps(warp), 
        "returns": dumps(returns), 
        "edited": dumps(edited), 
        "optype": dumps(optype), 
        "color": dumps(colors),
    }
    frmutation = FRCustomBlockMutation.from_data(data)
    assert frmutation.proccode == data["proccode"]
    assert frmutation.argument_ids == api.argument_ids
    assert frmutation.argument_names == api.argument_names
    assert frmutation.argument_defaults == api.argument_defaults 
    assert frmutation.warp == warp
    assert frmutation.returns == returns
    assert frmutation.edited == edited
    assert frmutation.optype == optype
    assert frmutation.color == tuple(colors)
    
    srmutation = frmutation.to_second(api)
    assert isinstance(srmutation, SRCustomBlockMutation)
    custom_opcode = SRCustomBlockOpcode.from_proccode_argument_names(
        proccode=frmutation.proccode,
        argument_names=frmutation.argument_names,
    )
    assert srmutation.custom_opcode == custom_opcode
    assert srmutation.no_screen_refresh == frmutation.warp
    assert srmutation.optype == SRCustomBlockOptype.from_code(frmutation.optype)
    assert srmutation.main_color == frmutation.color[0]
    assert srmutation.prototype_color == frmutation.color[1]
    assert srmutation.outline_color == frmutation.color[2]


def test_FRCustomBlockCallMutation_from_data_and_to_second(api: DummyAPI):
    warp = False
    returns = None
    edited = True
    optype = None
    colors = ["#FF6680", "#FF4D6A", "#FF3355"]
    data = {
        "tagName": "mutation", 
        "children": [], 
        "proccode": "do %b label text", 
        "argumentids": dumps(api.argument_ids), 
        "warp": dumps(warp), 
        "returns": dumps(returns), 
        "edited": dumps(edited), 
        "optype": dumps(optype), 
        "color": dumps(colors),
    }
    frmutation = FRCustomBlockCallMutation.from_data(data)
    assert frmutation.proccode == data["proccode"]
    assert frmutation.argument_ids == api.argument_ids
    assert frmutation.warp == warp
    assert frmutation.returns == returns
    assert frmutation.edited == edited
    assert frmutation.optype == optype
    assert frmutation.color == tuple(colors)
    
    srmutation = frmutation.to_second(api)
    assert isinstance(srmutation, SRCustomBlockCallMutation)
    custom_opcode = SRCustomBlockOpcode.from_proccode_argument_names(
        proccode=frmutation.proccode,
        argument_names=api.argument_names,
    )
    assert srmutation.custom_opcode == custom_opcode


def test_FRCustomBlockMutation_warp():
    colors = ["#FF6680", "#FF4D6A", "#FF3355"]
    data = {
        "tagName": "mutation", 
        "children": [], 
        "proccode": "hi bye", 
        "argumentids": dumps([]), 
        "argumentnames": dumps([]), 
        "argumentdefaults": dumps([]), 
        "warp": ..., 
        "returns": dumps(None), 
        "edited": dumps(True), 
        "optype": dumps(None), 
        "color": dumps(colors),
    }
    
    FRCustomBlockMutation    .from_data(data | {"warp": dumps(True )})
    FRCustomBlockCallMutation.from_data(data | {"warp": dumps(False)})

    FRCustomBlockMutation    .from_data(data | {"warp": True })
    FRCustomBlockCallMutation.from_data(data | {"warp": False})

    with raises(DeserializationError):
        FRCustomBlockMutation    .from_data(data | {"warp": 123})
    with raises(DeserializationError):
        FRCustomBlockCallMutation.from_data(data | {"warp": []})
    

def test_FRStopScriptMutation_from_data_and_to_second(api: DummyAPI):
    has_next = False
    data = {
        "tagName": "mutation",
        "children": [],
        "hasnext": dumps(has_next),
    }
    frmutation = FRStopScriptMutation.from_data(data)
    assert frmutation.has_next == has_next
    
    srmutation = frmutation.to_second(api)
    assert isinstance(srmutation, SRStopScriptMutation)
    assert srmutation.is_ending_statement == (not frmutation.has_next)

@fixture
def config():
    return ValidationConfig()

def test_SRCustomBlockArgumentMutation_validate(config):
    srmutation = SRCustomBlockArgumentMutation(
        argument_name="my argument",
        main_color="#f8e43a",
        prototype_color="#c38d12",
        outline_color="#e9d563",
    )
    srmutation.validate(path=[], config=config)
    
    execute_attr_validation_tests(
        obj=srmutation,
        attr_tests=[
            ("argument_name", 5, TypeValidationError),
            ("main_color", {}, TypeValidationError),
            ("main_color", "", InvalidValueError),
            ("prototype_color", [], TypeValidationError),
            ("prototype_color", "#abc", InvalidValueError),
            ("outline_color", (), TypeValidationError),
            ("outline_color", "255", InvalidValueError),
        ],
        validate_func=SRCustomBlockArgumentMutation.validate,
        func_args=[[], config],
    )

def test_SRCustomBlockMutation_validate(config):
    srmutation = SRCustomBlockMutation(
        custom_opcode=SRCustomBlockOpcode(segments=("hi",)),
        no_screen_refresh=True,
        optype=SRCustomBlockOptype.STRING_REPORTER,
        main_color="#f8e43a",
        prototype_color="#c38d12",
        outline_color="#e9d563",
    )

    srmutation.validate(path=[], config=config)
    
    execute_attr_validation_tests(
        obj=srmutation,
        attr_tests=[
            ("custom_opcode", "some custom opcode", TypeValidationError),
            ("no_screen_refresh", None, TypeValidationError),
            ("main_color", {}, TypeValidationError),
            ("main_color", "", InvalidValueError),
            ("prototype_color", [], TypeValidationError),
            ("prototype_color", "#abc", InvalidValueError),
            ("outline_color", (), TypeValidationError),
            ("outline_color", "255", InvalidValueError),
        ],
        validate_func=SRCustomBlockMutation.validate,
        func_args=[[], config],
    )
    
    
def test_SRCustomBlockCallMutation_validate(config):
    srmutation = SRCustomBlockCallMutation(
        custom_opcode=SRCustomBlockOpcode(segments=("hi",)),
    )

    srmutation.validate(path=[], config=config)
    
    execute_attr_validation_tests(
        obj=srmutation,
        attr_tests=[
            ("custom_opcode", "some custom opcode", TypeValidationError),
        ],
        validate_func=SRCustomBlockCallMutation.validate,
        func_args=[[], config],
    )

def test_SRStopScriptMutation_validate(config):
    srmutation = SRStopScriptMutation(
        is_ending_statement=True,
    )

    srmutation.validate(path=[], config=config)

    execute_attr_validation_tests(
        obj=srmutation,
        attr_tests=[
            ("is_ending_statement", {...}, TypeValidationError),
        ],
        validate_func=SRStopScriptMutation.validate,
        func_args=[[], config],
    )
    

