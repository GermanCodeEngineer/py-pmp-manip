from typing      import Any
from copy        import deepcopy
from dataclasses import dataclass

from utility     import GreprClass, PypenguinEnum, ThanksError
from utility     import AA_TYPE, AA_TYPES, AA_LIST_OF_TYPE, AA_MIN, AA_RANGE, AA_COORD_PAIR, AA_NOT_ONE_OF, SameNameTwiceError
from opcode_info import OpcodeInfoAPI

from core.asset          import FRCostume, FRSound, SRCostume, SRSound
from core.block          import FRBlock, TRBlock, SRScript, TRBlockReference
from core.block_mutation import SRCustomBlockMutation
from core.comment        import FRComment, SRFloatingComment, SRAttachedComment
from core.context        import PartialContext, FullContext
from core.dropdown       import SRDropdownValue, SRDropdownKind
from core.fr_to_tr_api   import FRtoTRAPI, ValidationAPI
from core.monitor        import SRMonitor
from core.vars_lists     import SRVariable, SRSpriteOnlyVariable, SRAllSpriteVariable, SRCloudVariable
from core.vars_lists     import SRList, SRSpriteOnlyList, SRAllSpriteList

@dataclass(repr=False)
class FRTarget(GreprClass):
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
    
    def __post_init__(self) -> None:
        if self.custom_vars != []: raise ThanksError()

    @classmethod
    def from_data(cls, data: dict[str, Any], info_api: OpcodeInfoAPI) -> "FRTarget":
        return cls(
            is_stage        = data["isStage"   ],
            name            = data["name"      ],
            variables       = {key: tuple(value) for key, value in data["variables"].items()},
            lists           = {key: tuple(value) for key, value in data["lists"    ].items()},
            broadcasts      = data["broadcasts"],
            custom_vars     = data["customVars"],
            blocks          = {
                block_id: (
                    tuple(block_data) if isinstance(block_data, list) else FRBlock.from_data(block_data, info_api=info_api)
                ) for block_id, block_data in data["blocks"].items()
            },
            comments        = {
                comment_id: FRComment.from_data(comment_data)
                for comment_id, comment_data in data["comments"].items()
            },
            current_costume = data["currentCostume"],
            costumes        = [
                FRCostume.from_data(costume_data) for costume_data in data["costumes"]
            ],
            sounds          = [
                FRSound.  from_data(sound_data  ) for sound_data   in data["sounds"  ]
            ],
            id              = data["id"        ],
            volume          = data["volume"    ],
            layer_order     = data["layerOrder"],
        )

    def proto_step(self, info_api: OpcodeInfoAPI
    ) -> tuple[
        list[SRScript], 
        list[SRFloatingComment], 
        list[SRCostume], 
        list[SRSound], 
        list[SRVariable], 
        list[SRList],
    ]:
        floating_comments = []
        attached_comments = {}
        for comment_id, comment in self.comments.items():
            new_comment = comment.step()
            if isinstance(new_comment, SRFloatingComment):
                floating_comments.append(new_comment)
            elif isinstance(new_comment, SRAttachedComment):
                attached_comments[comment_id] = new_comment

        blocks = deepcopy(self.blocks)
        for block_reference, block in blocks.items():
            if isinstance(block, tuple):
                blocks[block_reference] = FRBlock.from_tuple(block, parent_id=None, info_api=info_api)

        block_api = FRtoTRAPI(blocks=blocks, block_comments=attached_comments)
        new_blocks: dict["TRBlockReference", "TRBlock"] = {}
        for block_reference, block in blocks.items():
            new_block = block.step(
                block_api = block_api,
                info_api  = info_api,
                own_id    = block_reference,
            )
            new_blocks[TRBlockReference(id=block_reference)] = new_block

        for block_reference in block_api.scheduled_block_deletions:
            del new_blocks[TRBlockReference(id=block_reference)]
        
        # Get all top level block ids
        top_level_block_refs: list[TRBlockReference] = []
        [top_level_block_refs.append(block_reference) if block.is_top_level else None for block_reference, block in new_blocks.items()]
        
        from utility import grepr
        
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
            position, script_blocks = block.step(
                all_blocks    = new_blocks,
                info_api      = info_api,
            )
            new_scripts.append(SRScript(
                position = position,
                blocks   = script_blocks,
            ))
        
        new_variables, new_lists = self.step_variables_lists()
        return (
            new_scripts,
            floating_comments,
            [costume.step() for costume in self.costumes],
            [sound  .step() for sound   in self.sounds  ],
            new_variables,
            new_lists,
        )
    
    def step_variables_lists(self) -> tuple[list[SRVariable], list[SRList]]:
        new_variables = []
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
            new_variables.append(cls(name=name, current_value=current_value))
        
        new_lists = []
        for list_ in self.lists.values():
            name = list_[0]
            current_value = list_[1]
            if self.is_stage:
                cls = SRAllSpriteList
            else:
                cls = SRSpriteOnlyList
            new_lists.append(cls(name=name, current_value=current_value))
        
        return new_variables, new_lists

@dataclass(repr=False)          
class FRStage(FRTarget):
    _grepr_fields = FRTarget._grepr_fields + ["tempo", "video_transparency", "video_state", "text_to_speech_language"]
    
    tempo: int
    video_transparency: int | float
    video_state: str
    text_to_speech_language: str | None

    @classmethod
    def from_data(cls, data: dict[str, Any], info_api: OpcodeInfoAPI) -> "FRTarget":
        return cls(
            is_stage                = data["isStage"   ],
            name                    = data["name"      ],
            variables               = {key: tuple(value) for key, value in data["variables"].items()},
            lists                   = {key: tuple(value) for key, value in data["lists"    ].items()},
            broadcasts              = data["broadcasts"],
            custom_vars             = data["customVars"],
            blocks                  = {
                block_id: (
                    tuple(block_data) if isinstance(block_data, list) else FRBlock.from_data(block_data, info_api=info_api)
                ) for block_id, block_data in data["blocks"].items()
            },
            comments                = {
                comment_id: FRComment.from_data(comment_data)
                for comment_id, comment_data in data["comments"].items()
            },
            current_costume         = data["currentCostume"],
            costumes                = [
                FRCostume.from_data(costume_data) for costume_data in data["costumes"]
            ],
            sounds                  = [
                FRSound.  from_data(sound_data  ) for sound_data   in data["sounds"  ]
            ],
            id                      = data["id"                  ],
            volume                  = data["volume"              ],
            layer_order             = data["layerOrder"          ],

            tempo                   = data["tempo"               ],
            video_transparency      = data["videoTransparency"   ],
            video_state             = data["videoState"          ],
            text_to_speech_language = data["textToSpeechLanguage"],
        )
    
    def step(self, info_api: OpcodeInfoAPI
    ) -> tuple["SRStage", list[SRAllSpriteVariable],  list[SRAllSpriteList]]:
        (
            scripts,
            comments,
            costumes,
            sounds,
            all_sprite_variables,
            all_sprite_lists,
        ) = super().proto_step(info_api)
        return (SRStage(
            scripts       = scripts,
            comments      = comments,
            costume_index = self.current_costume,
            costumes      = costumes,
            sounds        = sounds,
            volume        = self.volume,
        ), all_sprite_variables, all_sprite_lists)

@dataclass(repr=False)
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
    def from_data(cls, data: dict[str, Any], info_api: OpcodeInfoAPI) -> "FRTarget": # TODO: remove repeated code
        return cls(
            is_stage        = data["isStage"   ],
            name            = data["name"      ],
            variables       = {key: tuple(value) for key, value in data["variables"].items()},
            lists           = {key: tuple(value) for key, value in data["lists"    ].items()},
            broadcasts      = data["broadcasts"],
            custom_vars     = data["customVars"],
            blocks          = {
                block_id: (
                    tuple(block_data) if isinstance(block_data, list) else FRBlock.from_data(block_data, info_api=info_api)
                ) for block_id, block_data in data["blocks"].items()
            },
            comments        = {
                comment_id: FRComment.from_data(comment_data)
                for comment_id, comment_data in data["comments"].items()
            },
            current_costume = data["currentCostume"],
            costumes        = [
                FRCostume.from_data(costume_data) for costume_data in data["costumes"]
            ],
            sounds          = [
                FRSound.  from_data(sound_data  ) for sound_data   in data["sounds"  ]
            ],
            id              = data["id"           ],
            volume          = data["volume"       ],
            layer_order     = data["layerOrder"   ],

            visible         = data["visible"      ],
            x               = data["x"            ],
            y               = data["y"            ],
            size            = data["size"         ],
            direction       = data["direction"    ],
            draggable       = data["draggable"    ],
            rotation_style  = data["rotationStyle"],
        )

    def step(self, info_api: OpcodeInfoAPI
    ) -> tuple["SRSprite", None, None]:
        (
            scripts,
            comments,
            costumes,
            sounds,
            sprite_only_variables,
            sprite_only_lists,
        ) = super().proto_step(info_api)
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
            local_monitors        = [], # will be filled later
            layer_order           = self.layer_order,
            is_visible            = self.visible,
            position              = (self.x, self.y),
            size                  = self.size,
            direction             = self.direction,
            is_draggable          = self.draggable,
            rotation_style        = SRSpriteRotationStyle.from_string(self.rotation_style),
        ), None, None)
    
@dataclass(repr=False)
class SRTarget(GreprClass):
    _grepr = True
    _grepr_fields = ["scripts", "comments", "costume_index", "costumes", "sounds", "volume"]

    scripts: list[SRScript]
    comments: list[SRFloatingComment]
    costume_index: int
    costumes: list[SRCostume]
    sounds: list[SRSound]
    volume: int | float

    def validate(self, path: list, info_api: OpcodeInfoAPI) -> None:
        AA_LIST_OF_TYPE(self, path, "scripts", SRScript)
        AA_LIST_OF_TYPE(self, path, "comments", SRFloatingComment)
        AA_LIST_OF_TYPE(self, path, "costumes", SRCostume)
        AA_TYPE(self, path, "costume_index", int)
        AA_RANGE(self, path, "costume_index", min=0, max=len(self.costumes)-1, condition=f"In this case the sprite has {len(self.costumes)} costume(s)")
        AA_LIST_OF_TYPE(self, path, "sounds", SRSound)
        AA_TYPES(self, path, "volume", (int, float))
        AA_RANGE(self, path, "volume", min=0, max=100)
        
        for i, comment in enumerate(self.comments):
            comment.validate(path+["comments", i])

        defined_costumes = {}
        for i, costume in enumerate(self.costumes):
            current_path = path+["costumes", i]
            costume.validate(path)
            if costume.name in defined_costumes:
                other_path = defined_costumes[costume.name]
                raise SameNameTwiceError(other_path, current_path, "Two costumes mustn't have the same name")
            defined_costumes[costume.name] = current_path
        
        defined_sounds = {}
        for i, sound in enumerate(self.sounds):
            current_path = path+["sounds", i]
            sound.validate(path)
            if sound.name in defined_sounds:
                other_path = defined_sounds[sound.name]
                raise SameNameTwiceError(other_path, current_path, "Two sounds mustn't have the same name")
            defined_sounds[sound.name] = current_path
        # TODO: complete this
    
    def get_full_context(self, partial_context: PartialContext) -> FullContext:
        return FullContext.from_partial(
            pc       = partial_context,
            costumes = [SRDropdownValue(SRDropdownKind.COSTUME, costume.name) for costume in self.costumes],
            sounds   = [SRDropdownValue(SRDropdownKind.SOUND  , sound  .name) for sound   in self.sounds  ],
            is_stage = isinstance(self, SRStage),
        )
    
    def validate_scripts(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        context: PartialContext,
    ) -> None:
        context = self.get_full_context(partial_context=context)
        validation_api = ValidationAPI(scripts=self.scripts)
        cb_optypes = {}
        for i, script in enumerate(self.scripts):
            script.validate(
                path           = path+["scripts", i],
                info_api       = info_api,
                validation_api = validation_api,
                context        = context,
            )
            for j, block in enumerate(script.blocks):
                current_path = path+["scripts", i, "blocks", j]
                if isinstance(block.mutation, SRCustomBlockMutation):
                    custom_opcode = block.mutation.custom_opcode
                    if custom_opcode in cb_optypes:
                        other_path = cb_optypes[custom_opcode]
                        raise SameNameTwiceError(other_path, current_path, "Two custom blocks mustn't have the same name(see .mutation.custom_opcode.proccode)")
                    cb_optypes[custom_opcode] = block.mutation.optype
        

class SRStage(SRTarget):
    pass # The stage has no additional properties

@dataclass(repr=False)
class SRSprite(SRTarget):
    _grepr_fields = ["name"] + SRTarget._grepr_fields + ["sprite_only_variables", "sprite_only_lists", "local_monitors", "layer_order", "is_visible", "position", "size", "direction", "is_draggable", "rotation_style"]
    
    name: str
    sprite_only_variables: list[SRSpriteOnlyVariable]
    sprite_only_lists: list[SRSpriteOnlyList]
    local_monitors: list[SRMonitor]
    layer_order: int
    is_visible: bool
    position: tuple[int | float, int | float]
    size: int | float
    direction: int | float
    is_draggable: bool
    rotation_style: "SRSpriteRotationStyle"
    
    def validate(self, path: list, info_api: OpcodeInfoAPI) -> None:
        super().validate(path, info_api)
        
        AA_TYPE(self, path, "name", str)
        AA_NOT_ONE_OF(self, path, "name", ["_myself_", "_stage_", "_mouse_", "_edge_"])
        AA_LIST_OF_TYPE(self, path, "sprite_only_variables", SRSpriteOnlyVariable)
        AA_LIST_OF_TYPE(self, path, "sprite_only_lists", SRSpriteOnlyList)
        AA_LIST_OF_TYPE(self, path, "local_monitors", SRMonitor)
        AA_TYPE(self, path, "layer_order", int)
        AA_MIN(self, path, "layer_order", min=1) # TODO: reform and check
        AA_TYPE(self, path, "is_visible", bool)
        AA_COORD_PAIR(self, path, "position")
        AA_TYPES(self, path, "size", (int, float))
        AA_MIN(self, path, "size", min=0)
        AA_TYPES(self, path, "direction", (int, float))
        AA_RANGE(self, path, "direction", min=-180, max=180)
        AA_TYPE(self, path, "is_draggable", bool)
        AA_TYPE(self, path, "rotation_style", SRSpriteRotationStyle)
        
        
        for i, variable in enumerate(self.sprite_only_variables):
            variable.validate(path+["sprite_only_variables", i])
        for i, list_ in enumerate(self.sprite_only_lists):
            list_.validate(path+["sprite_only_lists", i])
        
        for i, monitor in enumerate(self.local_monitors):
            monitor.validate(path+["local_monitors", i], info_api)
    
    def validate_monitors(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        context: PartialContext,
    ) -> None:
        context = self.get_full_context(partial_context=context)
        for i, monitor in enumerate(self.local_monitors):
            monitor.validate_dropdowns_values(
                path     = path+["global_monitors", i], 
                info_api = info_api, 
                context  = context,
            )
        

class SRSpriteRotationStyle(PypenguinEnum):
    @staticmethod
    def from_string(string: str):
        match string:
            case "all around"  : return SRSpriteRotationStyle.ALL_AROUND
            case "left-right"  : return SRSpriteRotationStyle.LEFT_RIGHT
            case "don't rotate": return SRSpriteRotationStyle.DONT_ROTATE
            case _: raise ValueError()

    ALL_AROUND  = 0
    LEFT_RIGHT  = 1
    DONT_ROTATE = 2

