import typing

from block import FLComplexBlock

class FLTarget:
    _grepr = True
    _grepr_fields = ["is_stage", "name", "variables", "lists", "broadcasts", "custom_vars", "blocks", "comments", "current_costume", "costumes", "sounds", "id", "volume", "layer_order"]
    
    is_stage: bool
    name: str
    variables: typing.Dict[str, typing.Tuple[str, typing.Any]]
    lists: typing.Dict[str, typing.Tuple[str, typing.Any]]
    broadcasts: typing.Dict[str, str]
    custom_vars: typing.List | None
    blocks: typing.Dict[str, FLComplexBlock]
    #comments: 
    current_costume: int
    #costumes: 
    #sounds: 
    id: str
    volume: int | float
    layer_order: int

    @staticmethod
    def from_data(data):
        return FLTarget(data)

    def __init__(self, data):
        self.is_stage        = data["isStage"       ]
        self.name            = data["name"          ]
        self.variables       = {key: tuple(value) for key, value in data["variables"].items()}
        self.lists           = {key: tuple(value) for key, value in data["lists"    ].items()}
        self.broadcasts      = data["broadcasts"    ]
        self.custom_vars     = data["customVars"    ]
        self.blocks          = [
            FL
        ]
        self.comments        = data["comments"      ]
        self.current_costume = data["currentCostume"]
        self.costumes        = data["costumes"      ]
        self.sounds          = data["sounds"        ]
        self.id              = data["id"            ]
        self.volume          = data["volume"        ] # Yep. I like order.
        self.layer_order     = data["layerOrder"    ]

class FLStage(FLTarget):
    _grepr_fields = FLTarget._grepr_fields + ["tempo", "video_transparency", "video_state", "text_to_speech_language"]


    @staticmethod
    def from_data(data):
        return FLStage(data)

    def __init__(self, data):
        super().__init__(data)
        self.tempo                   = data["tempo"               ]
        self.video_transparency      = data["videoTransparency"   ]
        self.video_state             = data["videoState"          ]
        self.text_to_speech_language = data["textToSpeechLanguage"]

class FLSprite(FLTarget):
    _grepr_fields = FLTarget._grepr_fields + ["visible", "x", "y", "size", "direction", "draggable", "rotation_style"]

    visible: bool
    x: int | float
    y: int | float
    size: int | float
    direction: int | float
    draggable: bool
    rotation_style: str

    @staticmethod
    def from_data(data):
        return FLSprite(data)
    
    def __init__(self, data):
        super().__init__(data)
        self.visible        = data["visible"      ]
        self.x              = data["x"            ]
        self.y              = data["y"            ]
        self.size           = data["size"         ]
        self.direction      = data["direction"    ]
        self.draggable      = data["draggable"    ]
        self.rotation_style = data["rotationStyle"]



