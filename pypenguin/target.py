import typing

from block   import FLBlock, FLCustomBlockMutation
from comment import FLComment, SLFloatingComment, SLAttachedComment
from asset   import FLCostume, FLSound

class FLTarget:
    _grepr = True
    _grepr_fields = ["is_stage", "name", "variables", "lists", "broadcasts", "custom_vars", "blocks", "comments", "current_costume", "costumes", "sounds", "id", "volume", "layer_order"]
    
    is_stage: bool
    name: str
    variables: typing.Dict[str, typing.Tuple[str, typing.Any]]
    lists: typing.Dict[str, typing.Tuple[str, typing.Any]]
    broadcasts: typing.Dict[str, str]
    custom_vars: typing.List | None
    blocks: typing.Dict[str, tuple | FLBlock]
    comments: typing.Dict[str, FLComment]
    current_costume: int
    costumes: typing.List[FLCostume]
    sounds: typing.List[FLSound] 
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
                tuple(block_data) if isinstance(block_data, list) else FLBlock.from_data(block_data)
            ) for block_id, block_data in data["blocks"].items()
        }
        self.comments        = {
          comment_id: FLComment.from_data(comment_data)
          for comment_id, comment_data in data["comments"].items()
        }
        self.current_costume = data["currentCostume"]
        self.costumes        = [
          FLCostume.from_data(costume_data) for costume_data in data["costumes"]
        ]
        self.sounds          = [
          FLSound.  from_data(sound_data  ) for sound_data   in data["sounds"  ]
        ]
        self.id              = data["id"        ]
        self.volume          = data["volume"    ] # Yep. I like order.
        self.layer_order     = data["layerOrder"]
        return self

    def get_cb_mutation(self, proccode: str):
        for block in self.blocks.values():
            if not isinstance(block, FLBlock): continue
            if not isinstance(block.mutation, FLCustomBlockMutation): continue
            if block.mutation.proccode == proccode:
                return block.mutation
        raise ValueError(f"Mutation of proccode {repr(proccode)} not found.")
        
    def step(self):
        floating_comments = []
        attached_comments = {}
        for comment_id, comment in self.comments.items():
            new_comment = comment.step()
            if isinstance(new_comment, SLFloatingComment):
                floating_comments.append(new_comment)
            elif isinstance(new_comment, SLAttachedComment):
                attached_comments[comment_id] = new_comment

        for block_id, block in self.blocks.items():
            old_block = block
            if isinstance(block, tuple):
                block = FLBlock.from_tuple(block, parent_id=None)
            from utility import gprint
            gprint(block_id, old_block)
            gprint("====>", block)
            #new_block = block.step(
            #    get_comment=(lambda comment_id: attached_comments[comment_id]),
            #    get_cb_mutation=self.get_cb_mutation,
            #)

class FLStage(FLTarget):
    _grepr_fields = FLTarget._grepr_fields + ["tempo", "video_transparency", "video_state", "text_to_speech_language"]
    
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

class FLSprite(FLTarget):
    _grepr_fields = FLTarget._grepr_fields + ["visible", "x", "y", "size", "direction", "draggable", "rotation_style"]

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


