from typing import Any

from utility import gprint
from block   import FRBlock, FRCustomBlockMutation
from comment import FRComment, SRFloatingComment, SRAttachedComment
from asset   import FRCostume, FRSound

class FRTarget:
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
    def from_data(cls, data):
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

    def get_cb_mutation(self, proccode: str):
        for block in self.blocks.values():
            if not isinstance(block, FRBlock): continue
            if not isinstance(block.mutation, FRCustomBlockMutation): continue
            if block.mutation.proccode == proccode:
                return block.mutation
        raise ValueError(f"Mutation of proccode {repr(proccode)} not found.")
        
    def step(self):
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

        for block_id, block in self.blocks.items():
            if isinstance(block, tuple):
                block = FRBlock.from_tuple(block, parent_id=None)
                
            new_block = block.step(
                get_comment=(lambda comment_id: attached_comments[comment_id]),
                get_cb_mutation=self.get_cb_mutation,
            )
            gprint(block_id, block)
            gprint("====>", new_block)

class FRStage(FRTarget):
    _grepr_fields = FRTarget._grepr_fields + ["tempo", "video_transparency", "video_state", "text_to_speech_language"]
    
    tempo: int
    video_transparency: int | float
    video_state: str
    text_to_speech_language: str
    
    @classmethod
    def from_data(cls, data):
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
    def from_data(cls, data):
        self = super().from_data(data)
        self.visible        = data["visible"      ]
        self.x              = data["x"            ]
        self.y              = data["y"            ]
        self.size           = data["size"         ]
        self.direction      = data["direction"    ]
        self.draggable      = data["draggable"    ]
        self.rotation_style = data["rotationStyle"]
        return self

