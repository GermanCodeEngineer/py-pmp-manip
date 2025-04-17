from typing import Any
import copy

from utility    import gprint, PypenguinClass
from block      import FRBlock, TRBlock, SRScript, TRBlockReference
from comment    import FRComment, SRFloatingComment, SRAttachedComment
from asset      import FRCostume, FRSound
from config     import FRtoTRApi, SpecialCaseHandler
from block_info import BlockInfoApi

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

    def step(self, config: SpecialCaseHandler, info_api: BlockInfoApi):
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
        
        for block_reference, block in self.blocks.items():
            pass
            print("\n"*2)
            print(100*"=")
            gprint(block_reference, block)
            gprint(new_blocks.get(TRBlockReference(id=block_reference)))
        
        # Get all top level block ids
        top_level_block_refs: list[TRBlockReference] = []
        [top_level_block_refs.append(block_reference) if block.is_top_level else None for block_reference, block in new_blocks.items()]
        
        # Account for that one bug(not my fault), where a block is falsely independent
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
            position, script_blocks = block.nest_recursively(
                all_blocks    = new_blocks,
                own_reference = top_level_block_ref,
            )
            new_scripts.append(SRScript(
                position = position,
                blocks   = script_blocks,
            ))

        new_costumes = [costume.step() for costume in self.costumes]
        new_sounds   = [sound  .step() for sound   in self.sounds  ]

class FRStage(FRTarget):
    _grepr_fields = FRTarget._grepr_fields + ["tempo", "video_transparency", "video_state", "text_to_speech_language"]
    
    tempo: int
    video_transparency: int | float
    video_state: str
    text_to_speech_language: str
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRStage":
        self = super().from_data(data)
        self.tempo                   = data["tempo"               ]
        self.video_transparency      = data["videoTransparency"   ]
        self.video_state             = data["videoState"          ]
        self.text_to_speech_language = data["textToSpeechLanguage"]
        return self

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
        self.visible        = data["visible"      ]
        self.x              = data["x"            ]
        self.y              = data["y"            ]
        self.size           = data["size"         ]
        self.direction      = data["direction"    ]
        self.draggable      = data["draggable"    ]
        self.rotation_style = data["rotationStyle"]
        return self

