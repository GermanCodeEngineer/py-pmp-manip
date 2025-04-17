from typing import Iterable

from block_info.basis import *

class BlockInfoApi:
    _grepr = True
    _grepr_fields = ["block_info_sets"]

    block_info_sets: list[BlockInfoSet]
    
    def __init__(self):
        self.block_info_sets = []

    def add_block_info_set(self, block_info_set: BlockInfoSet):
        for other_set in self.block_info_sets:
            if other_set.name == block_info_set.name:
                raise ValueError(f"A BlockInfoSet called {repr(block_info_set)} was alredy added")
        self.block_info_sets.append(block_info_set)

    def get_set_by_name(self, name: str) -> BlockInfoSet:
        for block_info_set in self.block_info_sets:
            if block_info_set.name == name:
                return block_info_set
        raise ValueError(f"Couldn't find BlockInfoSet {repr(name)}")
    
    def get_sets_by_prefix(self, prefix: str) -> Iterable[BlockInfoSet]:
        for block_info_set in self.block_info_sets:
            if block_info_set.uses_prefix(prefix):
                yield block_info_set
        
    def get_info_by_opcode(self, opcode: str) -> BlockInfo:
        opcode_prefix = opcode[:opcode.index("_")]
        main_opcode = opcode[opcode.index("_")+1:]
        generator = self.get_sets_by_prefix(opcode_prefix)
        for block_info_set in generator:
            from utility import gprint
            block_info = block_info_set.get_block_info(main_opcode, default_none=True)
            if block_info is not None:
                return block_info
        raise ValueError(f"Couldn't find BlockInfo by opcode {repr(opcode)}")


from block_info.motion    import motion
from block_info.looks     import looks
from block_info.sounds    import sounds
from block_info.events    import events
from block_info.control   import control
from block_info.sensing   import sensing
from block_info.operators import operators
from block_info.variables import variables
from block_info.lists     import lists
from block_opcodes        import *

motion.add_block("goto_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#REACHABLE TARGET MENU (GO)",
))
motion.add_block("glideto_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#REACHABLE TARGET MENU (GLIDE)",
))
motion.add_block("pointtowards_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#OBSERVABLE TARGET MENU",
))

looks.add_block("costume", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#COSTUME MENU",
))
looks.add_block("backdrops", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#BACKDROP MENU",
))
looks.add_block("getinput_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#COSTUME PROPERTY MENU",
))
looks.add_block("changeVisibilityOfSprite_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#SHOW/HIDE SPRITE MENU",
))
looks.add_block("getOtherSpriteVisible_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#IS SPRITE VISIBLE MENU",
))

sounds.add_block("sounds_menu", BlockInfo( # this is certainly correct.
    block_type=BlockType.MENU,
    new_opcode="#SOUND MENU",
))

control.add_block("stop_sprite_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#STOP SPRITE MENU",
))
control.add_block("create_clone_of_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#CLONE TARGET MENU",
))
control.add_block("run_as_sprite_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#RUN AS SPRITE MENU",
))

sensing.add_block("touchingobjectmenu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#TOUCHING OBJECT MENU",
))
sensing.add_block("fulltouchingobjectmenu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#FULL TOUCHING OBJECT MENU",
))
sensing.add_block("touchingobjectmenusprites", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#TOUCHING OBJECT MENU SPRITES",
))
sensing.add_block("distancetomenu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#DISTANCE TO MENU",
))
sensing.add_block("sensing_keyoptions", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#KEY MENU",
))
sensing.add_block("sensing_scrolldirections", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#SCROLL DIRECTION MENU",
))
sensing.add_block("sensing_of_object_menu", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#OJBECT PROPERTY MENU",
))
sensing.add_block("sensing_fingeroptions", BlockInfo(
    block_type=BlockType.MENU,
    new_opcode="#FINGER INDEX MENU",
))
variables.add_block(OPCODE_VAR_VALUE.removeprefix("data_"), BlockInfo(
    block_type=BlockType.STRING_REPORTER,
    new_opcode="value of [VARIABLE]",
    can_have_monitor="True",
))
lists.add_block(OPCODE_LIST_VALUE.removeprefix("data_"), BlockInfo(
    block_type=BlockType.STRING_REPORTER,
    new_opcode="value of [LIST]",
    can_have_monitor="True",
))

custom_blocks = BlockInfoSet(
    name="Custom Blocks",
    opcode_prefix="procedures",
    alt_opcode_prefixes=["argument"],
    block_infos={
        "definition": BlockInfo(
            block_type=BlockType.HAT,
            new_opcode="define custom block",
        ),
        "definition_return": BlockInfo(
            block_type=BlockType.HAT,
            new_opcode="define custom block reporter",
        ),
        "prototype": BlockInfo( # only temporary
            block_type=BlockType.NOT_RELEVANT,
            new_opcode="#CUSTOM BLOCK PROTOTYPE",
        ),
        "call": BlockInfo(
            block_type=BlockType.DYNAMIC,
            new_opcode="call custom block",
        ),
        "return": BlockInfo(
            block_type=BlockType.ENDING_STATEMENT,
            new_opcode="return (VALUE)",
            inputs={
                "return": InputInfo(InputType.TEXT, new="VALUE"),
            },
        ),
        "set": BlockInfo(
            block_type=BlockType.STATEMENT,
            new_opcode="set (PARAM) to (VALUE)",
            inputs={
                "PARAM": InputInfo(InputType.ROUND, new="PARAM"),
                "VALUE": InputInfo(InputType.TEXT, new="VALUE"),
            },
        ),
        "reporter_string_number": BlockInfo(
            block_type=BlockType.STRING_REPORTER,
            new_opcode="value of text [ARGUMENT]",
            alt_opcode_prefix="argument",
        ),
        "reporter_boolean": BlockInfo(
            block_type=BlockType.BOOLEAN_REPORTER,
            new_opcode="value of boolean [ARGUMENT]",
            alt_opcode_prefix="argument",
        ),
    },
)





info_api = BlockInfoApi()
info_api.add_block_info_set(motion       )
info_api.add_block_info_set(looks        )
info_api.add_block_info_set(sounds       )
info_api.add_block_info_set(events       )
info_api.add_block_info_set(control      )
info_api.add_block_info_set(sensing      )
info_api.add_block_info_set(operators    )
info_api.add_block_info_set(variables    )
info_api.add_block_info_set(lists        )
info_api.add_block_info_set(custom_blocks)
