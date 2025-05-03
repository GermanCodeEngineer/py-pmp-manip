from pytest import fixture, raises
from json   import dumps, loads

from utility import DeserializationError, FSCError

from core.block_mutation import (
    FRCustomBlockArgumentMutation, FRCustomBlockMutation,
    FRCustomBlockCallMutation, FRStopScriptMutation,
    SRCustomBlockArgumentMutation, SRCustomBlockMutation,
    SRCustomBlockCallMutation, SRStopScriptMutation
)

class DummyAPI:
    def get_cb_mutation(self, proccode: str) -> FRCustomBlockMutation:
        return FRCustomBlockMutation(
            tag_name="mutation",
            children=[],
            proccode=proccode,
            argument_ids=["|%aQk0nd}|c.tVn$e}ST", "}G[ASqXh*6Yj)lUVOc`q"],
            argument_names=["arg1", "arg2"],
            argument_defaults=["", dumps(False)],
            warp=False,
            returns=True,
            edited=True,
            optype="statement",
            color=("#ffffff", "#aaaaaa", "#000000"),
        )


@fixture
def api():
    return DummyAPI()


def test_argument_mutation_from_data_and_step(api):
    data = {
        "tagName": "mutation",
        "children": [],
        "color": dumps(["#123456", "#abcdef", "#654321"]),
    }
    frmutation = FRCustomBlockArgumentMutation.from_data(data)
    assert frmutation.tag_name == data["mutation"]
    assert frmutation.children == data["children"]
    assert frmutation.color == loads(data["color"])
    
    srmutation.store_argument_name("my_arg")
    srmutation = mutation.step(api)
    assert isinstance(srmutation, SRCustomBlockArgumentMutation)
    assert srmutation.argument_name == "my_arg"
    assert srmutation.color1 == "#123456"
    assert srmutation.color2 == "#abcdef"
    assert srmutation.color3 == "#654321"


def test_argument_mutation_step_without_storing_argument(api):
    data = {
        "tagName": "mutation",
        "children": [],
        "color": dumps(["#111111", "#222222", "#333333"]),
    }
    frmutation = FRCustomBlockArgumentMutation.from_data(data)

    with raises(FSCError):
        frmutation.step(api)


def test_custom_block_mutation_from_data_and_step(api):
    data = {
        "tagName": "mutation",
        "children": [],
        "proccode": "example %s %s",
        "argumentids": dumps(["id1", "id2"]),
        "argumentnames": dumps(["a", "b"]),
        "argumentdefaults": dumps(["x", "y"]),
        "warp": dumps(True),
        "returns": dumps(False),
        "edited": dumps(True),
        "optype": ,
        "color": dumps(["#111", "#222", "#333"]),
    }
    frmutation = FRCustomBlockMutation.from_data(data)
    srmutation = mutation.step(api)

    assert isinstance(srmutation, SRCustomBlockMutation)
    assert srmutation.no_screen_refresh is True
    assert srmutation.optype == SRCustomBlockOptype.,
    assert srmutation.color3 == "#333"


def test_custom_block_call_mutation_from_data_and_step(api):
    data = {
        "tagName": "mutation",
        "children": [],
        "proccode": "use %s",
        "argumentids": dumps(["arg1"]),
        "warp": dumps(False),
        "returns": dumps(True),
        "edited": dumps(True),
        "optype": dumps("stack"),
        "color": dumps(["#001", "#002", "#003"]),
    }
    mutation = FRCustomBlockCallMutation.from_data(data)
    result = mutation.step(api)

    assert isinstance(result, SRCustomBlockCallMutation)
    assert result.custom_opcode.proccode == "use %s"


def test_stop_script_mutation_from_data_and_step():
    data = {
        "tagName": "mutation",
        "children": [],
        "hasnext": dumps(False),
    }
    mutation = FRStopScriptMutation.from_data(data)
    result = mutation.step(None)

    assert isinstance(result, SRStopScriptMutation)
    assert result.is_ending_statement is True


def test_custom_block_mutation_invalid_warp_type():
    data = {
        "tagName": "mutation",
        "children": [],
        "proccode": "broken",
        "argumentids": dumps([]),
        "argumentnames": dumps([]),
        "argumentdefaults": dumps([]),
        "warp": 123,  # invalid type
        "returns": dumps(False),
        "edited": dumps(True),
        "optype": dumps("stack"),
        "color": dumps(["#1", "#2", "#3"]),
    }

    with raises(DeserializationError):
        FRCustomBlockMutation.from_data(data)
