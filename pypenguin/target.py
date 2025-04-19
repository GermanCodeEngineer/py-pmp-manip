from typing import Any
import copy

from utility    import gprint, PypenguinClass
from block      import FRBlock, TRBlock, SRScript, TRBlockReference
from comment    import FRComment, SRFloatingComment, SRAttachedComment
from asset      import FRCostume, FRSound, SRCostume, SRSound
from config     import FRtoTRApi, SpecialCaseHandler
from block_info import BlockInfoApi
from vars_lists import SRVariable, SRSpriteOnlyVariable, SRAllSpriteVariable, SRCloudVariable
from vars_lists import SRList, SRSpriteOnlyList, SRAllSpriteList

class FRTarget(PypenguinClass):
    _grepr = True
    _grepr_fields = ["is_stage", "name", "variables", "lists", "broadcasts", "custom_vars", "blocks", "comments", "current_costume", "costumes", "sounds", "id", "volume", "layer_order"]
    
    is_stage: bool
    name: str
    variables: dict[str, tuple[str, Any]]
    lists: dict[str, tuple[str, Any]]
    broadcasts: dict[str, str]
    custom_vars: list | None
    blocks: dict[str, tuple | FRBlock]
    comments: dict[str, FRComment]
    current_costume: int
    costumes: list[FRCostume]
    sounds: list[FRSound] 
    id: str
    volume: int | float
    layer_order: int

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRTarget":
        self = cls()
        self.is_stage        = data["isStage"   ]
        self.name            = data["name"      ]
        self.variables       = {key: tuple(value) for key, value in data["variables"].items()}
        self.lists           = {key: tuple(value) for key, value in data["lists"    ].items()}
        self.broadcasts      = data["broadcasts"]
        self.custom_vars     = data["customVars"]
        if data["customVars"] != []:
            raise Exception("Wow! I have been trying to find out what 'customVars' is used for. Can you explain how you did that? Please contact me on GitHub.")
        self.blocks          = {
            block_id: (
                tuple(block_data) if isinstance(block_data, list) else FRBlock.from_data(block_data)
            ) for block_id, block_data in data["blocks"].items()
        }
        self.comments        = {
          comment_id: FRComment.from_data(comment_data)
          for comment_id, comment_data in data["comments"].items()
        }
        self.current_costume = data["currentCostume"]
        self.costumes        = [
          FRCostume.from_data(costume_data) for costume_data in data["costumes"]
        ]
        self.sounds          = [
          FRSound.  from_data(sound_data  ) for sound_data   in data["sounds"  ]
        ]
        self.id              = data["id"        ]
        self.volume          = data["volume"    ] # Yep. I like order.
        self.layer_order     = data["layerOrder"]
        return self

    def step(self, config: SpecialCaseHandler, info_api: BlockInfoApi
    ) -> tuple[list[SRScript], list[SRFloatingComment], list[SRCostume], list[SRSound], 
    list[SRVariable], list[SRList]]:
        floating_comments = []
        attached_comments = {}
        for comment_id, comment in self.comments.items():
            new_comment = comment.step()
            if isinstance(new_comment, SRFloatingComment):
                floating_comments.append(new_comment)
            elif isinstance(new_comment, SRAttachedComment):
                attached_comments[comment_id] = new_comment
        
        
        #gprint(floating_comments)
        #gprint(attached_comments)

        blocks = copy.deepcopy(self.blocks)
        for block_reference, block in blocks.items():
            if isinstance(block, tuple):
                blocks[block_reference] = FRBlock.from_tuple(block, parent_id=None)

        block_api = FRtoTRApi(blocks=blocks, block_comments=attached_comments)
        new_blocks: dict["TRBlockReference", "TRBlock"] = {}
        for block_reference, block in blocks.items():
            new_block = block.step(
                config    = config,
                block_api = block_api,
                info_api  = info_api,
                own_id    = block_reference,
            )
            new_blocks[TRBlockReference(id=block_reference)] = new_block

        for block_reference in block_api.scheduled_block_deletions:
            del new_blocks[TRBlockReference(id=block_reference)]
        
        #for block_reference, block in self.blocks.items():
        #    pass
        #    print("\n"*2)
        #    print(100*"=")
        #    gprint(block_reference, block)
        #    gprint(new_blocks.get(TRBlockReference(id=block_reference)))
        
        
        
        # Get all top level block ids
        top_level_block_refs: list[TRBlockReference] = []
        [top_level_block_refs.append(block_reference) if block.is_top_level else None for block_reference, block in new_blocks.items()]
        
        # Account for that one bug(not my fault), where a block is falsely independent
        #gprint(new_blocks)
        for block_reference, block in new_blocks.items():
            for input_value in block.inputs.values():
                for sub_reference in input_value.references:
                    sub_block = new_blocks[sub_reference]
                    if not sub_block.is_top_level:
                        continue
                    sub_block.is_top_level = False
                    sub_block.position     = None
                    top_level_block_refs.remove(sub_reference)

        new_scripts = []
        for top_level_block_ref in top_level_block_refs:
            block = new_blocks[top_level_block_ref]
            position, script_blocks = block.step(
                all_blocks    = new_blocks,
                own_reference = top_level_block_ref,
                info_api      = info_api,
            )
            new_scripts.append(SRScript(
                position = position,
                blocks   = script_blocks,
            ))
        #gprint(new_scripts)

        new_variables, new_lists = self.step_variables_lists()
        return (
             new_scripts,
             floating_comments,
             [costume.step() for costume in self.costumes],
             [sound  .step() for sound   in self.sounds  ],
             new_variables,
             new_lists,
        )
    
    def step_variables_lists(self) -> tuple[dict[str, SRVariable], dict[str, SRList]]:
        new_variables = {}
        for variable in self.variables.values():
            name = variable[0]
            current_value = variable[1]
            if self.is_stage:
                if (len(variable) == 3) and (variable[2] == True):
                    cls = SRCloudVariable
                else:
                    cls = SRAllSpriteVariable
            else:
                cls = SRSpriteOnlyVariable
            new_variables[name] = cls(current_value=current_value)
        
        new_lists = {}
        for list_ in self.lists.values():
            name = list_[0]
            current_value = list_[1]
            if self.is_stage:
                cls = SRAllSpriteList
            else:
                cls = SRSpriteOnlyList
            new_lists[name] = cls(current_value=current_value)
        
        return new_variables, new_lists
                
class FRStage(FRTarget):
    _grepr_fields = FRTarget._grepr_fields + ["tempo", "video_transparency", "video_state", "text_to_speech_language"]
    
    tempo: int
    video_transparency: int | float
    video_state: str
    text_to_speech_language: str | None
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRStage":
        self = super().from_data(data)
        assert self.is_stage
        self.tempo                   = data["tempo"               ]
        self.video_transparency      = data["videoTransparency"   ]
        self.video_state             = data["videoState"          ]
        self.text_to_speech_language = data["textToSpeechLanguage"]
        return self
    
    def step(self, config: SpecialCaseHandler, info_api: BlockInfoApi
    ) -> tuple["SRStage", dict[str, SRAllSpriteVariable],  dict[str, SRAllSpriteList]]:
         (
             scripts,
             comments,
             costumes,
             sounds,
             all_sprite_variables,
             all_sprite_lists,
         ) = super().step(
             config   = config,
             info_api = info_api,
         )
         return (SRStage(
             name          = self.name,
             scripts       = scripts,
             comments      = comments,
             costume_index = self.current_costume,
             costumes      = costumes,
             sounds        = sounds,
             volume        = self.volume,
         ), all_sprite_variables, all_sprite_lists)

class FRSprite(FRTarget):
    _grepr_fields = FRTarget._grepr_fields + ["visible", "x", "y", "size", "direction", "draggable", "rotation_style"]

    visible: bool
    x: int | float
    y: int | float
    size: int | float
    direction: int | float
    draggable: bool
    rotation_style: str

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRSprite":
        self = super().from_data(data)
        assert not self.is_stage
        self.visible        = data["visible"      ]
        self.x              = data["x"            ]
        self.y              = data["y"            ]
        self.size           = data["size"         ]
        self.direction      = data["direction"    ]
        self.draggable      = data["draggable"    ]
        self.rotation_style = data["rotationStyle"]
        return self

    def step(self, config: SpecialCaseHandler, info_api: BlockInfoApi
    ) -> tuple["SRSprite", None, None]:
         (
             scripts,
             comments,
             costumes,
             sounds,
             sprite_only_variables,
             sprite_only_lists,
         ) = super().step(
             config   = config,
             info_api = info_api,
         )
         return (SRSprite(
             name                  = self.name,
             scripts               = scripts,
             comments              = comments,
             costume_index         = self.current_costume,
             costumes              = costumes,
             sounds                = sounds,
             volume                = self.volume,
             sprite_only_variables = sprite_only_variables,
             sprite_only_lists     = sprite_only_lists,
             layer_order           = self.layer_order,
             is_visible            = self.visible,
             position              = (self.x, self.y),
             size                  = self.size,
             direction             = self.direction,
             is_draggable          = self.draggable,
             rotation_style        = self.rotation_style
             
         ), None, None)
    


class SRTarget(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "scripts", "comments", "costume_index", "costumes", "sounds", "volume"]

    name: str
    scripts: list[SRScript]
    comments: list[SRFloatingComment]
    costume_index: int
    costumes: list[SRCostume]
    sounds: list[SRSound]
    volume: int | float
    
    def __init__(self, 
        name: str,
        scripts: list[SRScript],
        comments: list[SRFloatingComment],
        costume_index: int,
        costumes: list[SRCostume],
        sounds: list[SRSound],
        volume: int | float,
    ):
        self.name          = name
        self.scripts       = scripts
        self.comments      = comments
        self.costume_index = costume_index
        self.costumes      = costumes
        self.sounds        = sounds
        self.volume        = volume

class SRStage(SRTarget):
    pass # The stage has no additional properties
     
class SRSprite(SRTarget):
    _grepr_fields = SRTarget._grepr_fields + ["sprite_only_variables", "sprite_only_lists", "layer_order", "is_visible", "position", "size", "direction", "is_draggable", "rotation_style"]
    
    sprite_only_variables: dict[str, SRSpriteOnlyVariable]
    sprite_only_lists    : dict[str, SRSpriteOnlyList]
    layer_order: int
    is_visible: bool
    position: tuple[int | float, int | float]
    size: int | float
    direction: int | float
    is_draggable: bool
    rotation_style: str # TODO: make enum
    
    def __init__(self, 
        name: str,
        scripts: list[SRScript],
        comments: list[SRFloatingComment],
        costume_index: int,
        costumes: list[SRCostume],
        sounds: list[SRSound],
        volume: int | float,
        sprite_only_variables: dict[str, SRSpriteOnlyVariable],
        sprite_only_lists    : dict[str, SRSpriteOnlyList],
        layer_order: int,
        is_visible: bool,
        position: tuple[int | float, int | float],
        size: int | float,
        direction: int | float,
        is_draggable: bool,
        rotation_style: str,
    ):
        super().__init__(
            name          = name,
            scripts       = scripts,
            comments      = comments,
            costume_index = costume_index,
            costumes      = costumes,
            sounds        = sounds,
            volume        = volume,
        )
        self.sprite_only_variables = sprite_only_variables
        self.sprite_only_lists     = sprite_only_lists
        self.layer_order           = layer_order
        self.position              = position
        self.size                  = size
        self.direction             = direction
        self.is_draggable          = is_draggable
        self.rotation_style        = rotation_style

