from pytest import fixture, raises
from copy   import copy

from pypenguin.utility            import tuplify, FSCError, ValidationError, DeserializationError
#from pypenguin.opcode_info        import OpcodeInfoAPI
from pypenguin.opcode_info.groups import info_api

from pypenguin.core.block          import FRBlock
from pypenguin.core.block_mutation import FRCustomBlockMutation

# FRBlock
def test_frblock_from_data_1():
    data = {
        "opcode": "event_broadcast",
        "next": None,
        "parent": None,
        "inputs": {
            "BROADCAST_INPUT": [
                1, [11, "hbn", "ajUzOI^,`@L4q@F6iXUp"],
            ],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 107,
        "y": 313,
    }
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.opcode    == data["opcode"]
    assert frblock.next      == data["next"]
    assert frblock.parent    == data["parent"]
    assert frblock.inputs    == tuplify(data["inputs"])
    assert frblock.fields    == tuplify(data["fields"])
    assert frblock.shadow    == data["shadow"]
    assert frblock.top_level == data["topLevel"]

def test_frblock_from_data_2():
    data = {
        "opcode": "motion_glideto", 
        "next": None, 
        "parent": None, 
        "inputs": {
            "SECS": [1, [4, "1"]], 
            "TO": [1, "k"],
        }, 
        "fields": {}, 
        "shadow": False, 
        "topLevel": False, 
        "comment": "j",
    }

def test_frblock_from_data_invalid_mutation():
    data = {
        "opcode": "event_broadcast",
        "next": None,
        "parent": None,
        "inputs": {
            "BROADCAST_INPUT": [
                1, [11, "hbn", "ajUzOI^,`@L4q@F6iXUp"],
            ],
        },
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 107,
        "y": 313,
        "mutation": {...},
    }
    with raises(DeserializationError):
        FRBlock.from_data(data, info_api=info_api)

def test_frblock_from_data_missing_mutation():
    data = {
        "opcode": "argument_reporter_boolean",
        "next": None,
        "parent": "a",
        "inputs": {},
        "fields": {
            "VALUE": ["boolean", "|%?~)R0k:KB.c`h[qvn("],
        },
        "shadow": True,
        "topLevel": False,
    }
    with raises(DeserializationError):
        FRBlock.from_data(data, info_api=info_api)

def test_frblock_from_data_valid_mutation():
    data = {
        "opcode": "procedures_prototype",
        "next": None,
        "parent": "h",
        "inputs": {
            "}G[ASqXh*6Yj)lUVOc`q": [
                1,
                "p"
            ],
            "@#z0NEJ4p%{?+(BDp~@F": [
                1,
                "q"
            ]
        },
        "fields": {},
        "shadow": True,
        "topLevel": False,
        "mutation": {
            "tagName": "mutation",
            "children": [],
            "proccode": "rep %b %s",
            "argumentids": "[\"}G[ASqXh*6Yj)lUVOc`q\",\"@#z0NEJ4p%{?+(BDp~@F\"]",
            "argumentnames": "[\"booleano\",\"number in\"]",
            "argumentdefaults": "[\"false\",\"\"]",
            "warp": "true",
            "returns": "true",
            "edited": "true",
            "optype": "\"string\"",
            "color": "[\"#FF6680\",\"#FF4D6A\",\"#FF3355\"]"
        }
    }
    frblock = FRBlock.from_data(data, info_api=info_api)
    assert isinstance(frblock, FRBlock)
    assert frblock.mutation == FRCustomBlockMutation.from_data(data["mutation"])


