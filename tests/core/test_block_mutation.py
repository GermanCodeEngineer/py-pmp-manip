from pytest import fixture, raises
from json   import dumps, loads

from pypenguin.utility import DeserializationError, FSCError

from pypenguin.core.block_mutation import (
    FRCustomBlockArgumentMutation, FRCustomBlockMutation,
    FRCustomBlockCallMutation, FRStopScriptMutation,
    SRCustomBlockArgumentMutation, SRCustomBlockMutation,
    SRCustomBlockCallMutation, SRStopScriptMutation
)
from pypenguin.core.custom_block import SRCustomBlockOpcode, SRCustomBlockOptype


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
def api():
    return DummyAPI(
        argument_ids=["|%aQk0nd}|c.tVn$e}ST"],
        argument_names=["boolean"],
        argument_defaults=[dumps(False)],
    )


def test_argument_mutation_from_data_and_step(api):
    colors = ["#FF6680", "#FF4D6A", "#FF3355"]
    data = {
        "tagName": "mutation", 
        "children": [], 
        "color": dumps(colors),
    }
    frmutation = FRCustomBlockArgumentMutation.from_data(data)
    assert frmutation.tag_name == data["tagName"]
    assert frmutation.children == data["children"]
    assert frmutation.color == tuple(colors)
    
    frmutation.store_argument_name("my_arg")
    srmutation = frmutation.step(api)
    assert isinstance(srmutation, SRCustomBlockArgumentMutation)
    assert srmutation.argument_name == "my_arg"
    assert srmutation.color1 == colors[0]
    assert srmutation.color2 == colors[1]
    assert srmutation.color3 == colors[2]

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
    
    srmutation = frmutation.step(api)
    assert isinstance(srmutation, SRCustomBlockMutation)
    custom_opcode = SRCustomBlockOpcode.from_proccode_argument_names(
        proccode=frmutation.proccode,
        argument_names=frmutation.argument_names,
    )
    assert srmutation.custom_opcode == custom_opcode
    assert srmutation.no_screen_refresh == frmutation.warp
    assert srmutation.optype == SRCustomBlockOptype.from_code(frmutation.optype)
    assert srmutation.color1 == frmutation.color[0]
    assert srmutation.color2 == frmutation.color[1]
    assert srmutation.color3 == frmutation.color[2]

def test_custom_block_mutation_invalid_warp_type():
    colors = ["#FF6680", "#FF4D6A", "#FF3355"]
    data = {
        "tagName": "mutation", 
        "children": [], 
        "proccode": "hi bye", 
        "argumentids": dumps([]), 
        "argumentnames": dumps([]), 
        "argumentdefaults": dumps([]), 
        "warp": 123, 
        "returns": dumps(None), 
        "edited": dumps(True), 
        "optype": dumps(None), 
        "color": dumps(colors),
    }
    
    with raises(DeserializationError, match=f"Invalid value for warp: {data['warp']}"):
        FRCustomBlockMutation.from_data(data)
    
    with raises(DeserializationError, match=f"Invalid value for warp: {data['warp']}"):
        FRCustomBlockCallMutation.from_data(data)


def test_custom_block_call_mutation_from_data_and_step(api):
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
    
    srmutation = frmutation.step(api)
    assert isinstance(srmutation, SRCustomBlockCallMutation)
    custom_opcode = SRCustomBlockOpcode.from_proccode_argument_names(
        proccode=frmutation.proccode,
        argument_names=api.argument_names,
    )
    assert srmutation.custom_opcode == custom_opcode

def test_stop_script_mutation_from_data_and_step(api):
    has_next = False
    data = {
        "tagName": "mutation",
        "children": [],
        "hasnext": dumps(has_next),
    }
    frmutation = FRStopScriptMutation.from_data(data)
    assert frmutation.has_next == has_next
    
    srmutation = frmutation.step(api)
    assert isinstance(srmutation, SRStopScriptMutation)
    assert srmutation.is_ending_statement == (not frmutation.has_next)

