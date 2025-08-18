from typing      import Any
from copy        import copy, deepcopy
from dataclasses import field
from abc         import abstractmethod, ABC
from uuid        import uuid4, UUID

from pmp_manip.important_consts import SHA256_SEC_TARGET_NAME, SHA256_SEC_BROADCAST_MSG
from pmp_manip.opcode_info.api  import OpcodeInfoAPI, DropdownValueKind
from pmp_manip.utility          import (
    string_to_sha256, grepr_dataclass, MANIP_ThanksError,
    AA_TYPE, AA_TYPES, AA_LIST_OF_TYPE, AA_LIST_OF_TYPES, AA_MIN_LEN, AA_MIN, AA_RANGE, AA_COORD_PAIR, AA_NOT_ONE_OF, 
    MANIP_SameValueTwiceError, MANIP_ConversionError,
)

from pmp_manip.core.asset           import FRCostume, FRSound, SRVectorCostume, SRBitmapCostume, SRSound
from pmp_manip.core.block_interface import SecondToInterIF, InterToFirstIF, FirstToInterIF, ValidationIF
from pmp_manip.core.block_mutation  import SRCustomBlockMutation
from pmp_manip.core.block           import FRBlock, IRBlock, SRScript
from pmp_manip.core.comment         import FRComment, SRComment
from pmp_manip.core.context         import PartialContext, CompleteContext
from pmp_manip.core.enums           import SRSpriteRotationStyle
from pmp_manip.core.monitor         import FRMonitor, SRMonitor
from pmp_manip.core.vars_lists      import SRVariable, SRVariable, SRVariable, SRCloudVariable
from pmp_manip.core.vars_lists      import SRList, SRList, SRList


@grepr_dataclass(grepr_fields=["is_stage", "name", "variables", "lists", "broadcasts", "custom_vars", "blocks", "comments", "current_costume", "costumes", "sounds", "id", "volume", "layer_order"])
class FRTarget(ABC):
    """
    The first representation (FR) of a target. A target can be either a sprite or the stage
    """
    
    is_stage: bool
    name: str
    variables: dict[str, tuple[str, (int|float|str|bool)] | tuple[str, (int|float|str|bool), bool]]
    lists: dict[str, tuple[str, list[int|float|str|bool]]]
    broadcasts: dict[str, str]
    custom_vars: list
    blocks: dict[str, tuple | FRBlock]
    comments: dict[str, FRComment]
    current_costume: int
    costumes: list[FRCostume]
    sounds: list[FRSound] 
    volume: int | float
    layer_order: int
    id: str
    
    @classmethod
    @abstractmethod
    def from_data(cls, data: dict[str, Any]) -> "FRTarget":
        """
        Deserializes json_data into a FRTarget
        
        Args:
            data: the json_data
        
        Returns:
            the FRTarget
        """

    @staticmethod
    def _from_data_common(data: dict[str, Any]) -> dict[str, Any]:
        """
        Prepare common fields for FRTarget and its subclasses

        Args:
            data: the json_data

        Returns:
            a dict containing the prepared values for common fields
        """
        return dict(
            is_stage=data["isStage"],
            name=data["name"],
            variables={key: tuple(value) for key, value in data["variables"].items()},
            lists={key: tuple(value) for key, value in data["lists"].items()},
            broadcasts=copy(data["broadcasts"]),
            custom_vars=deepcopy(data.get("customVars", [])),
            blocks={
                block_id: (
                    tuple(block_data)
                    if isinstance(block_data, list)
                    else FRBlock.from_data(block_data)
                )
                for block_id, block_data in data["blocks"].items()
            },
            comments={
                comment_id: FRComment.from_data(comment_data)
                for comment_id, comment_data in data["comments"].items()
            },
            current_costume=data["currentCostume"],
            costumes=[FRCostume.from_data(costume_data) for costume_data in data["costumes"]],
            sounds=[FRSound.from_data(sound_data) for sound_data in data["sounds"]],
            volume=data["volume"],
            layer_order=data["layerOrder"],
        )

    def __post_init__(self) -> None:
        """
        Ensure my assumption about custom_vars was correct
        
        Returns:
            None
        """
        if self.custom_vars != []: raise MANIP_ThanksError()

    @abstractmethod
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRTarget into json data
        
        Returns:
            the json data
        """

    def _to_data_common(self) -> dict[str, Any]:
        """
        Prepare common fields for FRTarget and its subclasses

        Returns:
            a dict containing the prepared values for common fields
        """
        return {
            "isStage": self.is_stage,
            "name": self.name,
            "variables": {key: list(value) for key, value in self.variables.items()},
            "lists": {key: list(value) for key, value in self.lists.items()},
            "broadcasts": copy(self.broadcasts),
            "customVars": deepcopy(self.custom_vars),
            "blocks": {
                block_id: (
                    list(block)
                    if isinstance(block, tuple)
                    else block.to_data()
                )
                for block_id, block in self.blocks.items()
            },
            "comments": {
                comment_id: comment.to_data()
                for comment_id, comment in self.comments.items()
            },
            "currentCostume": self.current_costume,
            "costumes": [costume.to_data() for costume in self.costumes],
            "sounds": [sound.to_data() for sound in self.sounds],
            "volume": self.volume,
            "layerOrder": self.layer_order,
            "id": self.id,
        }

    @abstractmethod
    def to_second(self, 
        asset_files: dict[str, bytes],
        info_api: OpcodeInfoAPI,
    ) -> tuple["SRTarget", list[SRVariable] | None,  list[SRList] | None]:
        """
        Converts a FRTarget into a SRTarget
        
        Args:
            asset_files: the asset files, which store the contents of costumes and sounds
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the SRTarget, a list of the global variables or None, a list of the global lists or None
        """

    def _to_second_common(self, asset_files: dict[str, bytes], info_api: OpcodeInfoAPI) -> tuple[
        list[SRScript], 
        list[SRComment], 
        list[SRVectorCostume | SRBitmapCostume], 
        list[SRSound], 
        list[SRVariable], 
        list[SRList],
    ]:
        """
        Convert common fields into second representation

        Args:
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            lists of scripts, floating comments, costumes, sounds, variables and lists
        """
        floating_comments = []
        attached_comments = {}
        for comment_id, comment in self.comments.items():
            is_attached, new_comment = comment.to_second()
            if is_attached:
                attached_comments[comment_id] = new_comment
            else:
                floating_comments.append(new_comment)

        blocks = deepcopy(self.blocks)
        for block_id, block in blocks.items():
            if isinstance(block, tuple):
                blocks[block_id] = FRBlock.from_tuple(block, parent_id=None)

        fti_if = FirstToInterIF(blocks=blocks, block_comments=attached_comments)
        new_blocks: dict["str", "IRBlock"] = {}
        for block_id, block in blocks.items():
            new_block = block.to_inter(
                fti_if   = fti_if,
                info_api = info_api,
                own_id   = block_id,
            )
            new_blocks[block_id] = new_block

        for block_id in fti_if.scheduled_block_deletions:
            del new_blocks[block_id]
        
        # Get all top level block ids
        top_level_block_ids: list[str] = []
        [
            top_level_block_ids.append(block_id) 
            if block.is_top_level else None for block_id, block in new_blocks.items()
        ]
        
        # Account for that one bug(not my fault), where a block is falsely independent
        for block_id, block in new_blocks.items():
            for input_value in block.inputs.values():
                for sub_reference in input_value.references:
                    sub_block = new_blocks[sub_reference]
                    if not sub_block.is_top_level:
                        continue
                    sub_block.is_top_level = False
                    sub_block.position     = None
                    top_level_block_ids.remove(sub_reference)

        new_scripts = []
        for top_level_block_id in top_level_block_ids:
            block = new_blocks[top_level_block_id]
            position, script_blocks = block.to_second(
                all_blocks    = new_blocks,
                info_api      = info_api,
            )
            new_scripts.append(SRScript(
                position = position,
                blocks   = script_blocks,
            ))
        
        new_variables, new_lists = self._to_second_variables_lists()
        return (
            new_scripts,
            floating_comments,
            [costume.to_second(asset_files) for costume in self.costumes],
            [sound  .to_second(asset_files) for sound   in self.sounds  ],
            new_variables,
            new_lists,
        )
    
    def _to_second_variables_lists(self) -> tuple[list[SRVariable], list[SRList]]:
        """
        Converts the variables and lists of a FRProject into second representation and returns them
        
        Returns:
            list of variables and list of lists in second representation
        """
        new_variables = []
        for variable in self.variables.values():
            if    len(variable) == 2:
                new_variables.append(
                    SRVariable(name=variable[0], current_value=variable[1])
                )
            elif (len(variable) == 3) and (variable[2] is True) and self.is_stage:
                new_variables.append(
                    SRCloudVariable(name=variable[0], current_value=variable[1])
                )
            else:
                raise MANIP_ConversionError(f"Invalid variable data {variable}")
        
        new_lists = []
        for list_ in self.lists.values():
            if len(list_) == 2:
                new_lists.append(
                    SRList(name=list_[0], current_value=copy(list_[1]))
                )
            else:
                raise MANIP_ConversionError(f"Invalid list data {list_}")
        
        return new_variables, new_lists

@grepr_dataclass(grepr_fields=["tempo", "video_transparency", "video_state", "text_to_speech_language"])
class FRStage(FRTarget):
    """
    The first representation (FR) of the stage
    """
    
    tempo: int
    video_transparency: int | float
    video_state: str
    text_to_speech_language: str | None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRStage":
        """
        Deserializes json_data into a FRStage
        
        Args:
            data: the json_data
        
        Returns:
            the FRStage
        """
        common_fields = cls._from_data_common(data)
        if "id" in data:
            id = data["id"]
        else:
            id = string_to_sha256("_stage_", secondary=SHA256_SEC_TARGET_NAME)
        return cls(
            **common_fields,
            id=id,
            tempo=data["tempo"],
            video_transparency=data["videoTransparency"],
            video_state=data["videoState"],
            text_to_speech_language=data["textToSpeechLanguage"],
        )
    
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRStage into json data
        
        Returns:
            the json data
        """
        data = self._to_data_common()
        data |= {
            "tempo"               : self.tempo,
            "videoTransparency"   : self.video_transparency,
            "videoState"          : self.video_state,
            "textToSpeechLanguage": self.text_to_speech_language,
        }
        return data
    
    def to_second(self, 
        asset_files: dict[str, bytes],
        info_api: OpcodeInfoAPI,
    ) -> tuple["SRStage", list[SRVariable],  list[SRList]]:
        """
        Converts a FRStage into a SRStage
        
        Args:
            asset_files: the asset files, which store the contents of costumes and sounds
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the SRStage, a list of the global variables, a list of the global lists
        """
        (
            scripts,
            comments,
            costumes,
            sounds,
            global_variables,
            global_lists,
        ) = super()._to_second_common(asset_files, info_api)
        new_stage = SRStage(
            scripts       = scripts,
            comments      = comments,
            costumes      = costumes,
            sounds        = sounds,
            costume_index = self.current_costume,
            volume        = self.volume,
        )
        return (new_stage, global_variables, global_lists)

@grepr_dataclass(grepr_fields=["visible", "x", "y", "size", "direction", "draggable", "rotation_style"],)
class FRSprite(FRTarget):
    """
    The first representation (FR) of a sprite
    """

    visible: bool
    x: int | float
    y: int | float
    size: int | float
    direction: int | float
    draggable: bool
    rotation_style: str

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRSprite":
        """
        Deserializes json_data into a FRSprite
        
        Args:
            data: the json_data
        
        Returns:
            the FRSprite
        """
        common_fields = cls._from_data_common(data)
        if "id" in data:
            id = data["id"]
        else:
            id = string_to_sha256(data["name"], secondary=SHA256_SEC_TARGET_NAME)
        return cls(
            **common_fields,
            id=id,
            visible=data["visible"],
            x=data["x"],
            y=data["y"],
            size=data["size"],
            direction=data["direction"],
            draggable=data["draggable"],
            rotation_style=data["rotationStyle"],
        )

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRSprite into json data
        
        Returns:
            the json data
        """
        data = self._to_data_common()
        data |= {
            "visible"      : self.visible,
            "x"            : self.x,
            "y"            : self.y,
            "size"         : self.size,
            "direction"    : self.direction,
            "draggable"    : self.draggable,
            "rotationStyle": self.rotation_style,
        }
        return data
    
    def to_second(self, 
        asset_files: dict[str, bytes],
        info_api: OpcodeInfoAPI,
    ) -> tuple["SRSprite", None, None]:
        """
        Converts a FRSprite into a SRSprite
        
        Args:
            asset_files: the asset files, which store the contents of costumes and sounds
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the SRSprite, None, None
        """
        (
            scripts,
            comments,
            costumes,
            sounds,
            local_variables,
            local_lists,
        ) = super()._to_second_common(asset_files, info_api)
        new_sprite = SRSprite(
            name            = self.name,
            scripts         = scripts,
            comments        = comments,
            costumes        = costumes,
            sounds          = sounds,
            costume_index   = self.current_costume,
            volume          = self.volume,
            local_variables = local_variables,
            local_lists     = local_lists,
            local_monitors  = [], # will be filled later
            is_visible      = self.visible,
            position        = (self.x, self.y),
            size            = self.size,
            direction       = self.direction,
            is_draggable    = self.draggable,
            rotation_style  = SRSpriteRotationStyle.from_code(self.rotation_style),
        )
        return (new_sprite, None, None)


@grepr_dataclass(
    grepr_fields=["scripts", "comments", "costumes", "sounds", "costume_index", "volume"], 
    init=False, forbid_init_only_subcls=True, suggested_subcls_names=["SRStage", "SRSprite"],
)
class SRTarget:
    """
    The second representation (SR) of a target, which is much more user friendly. A target can be either a sprite or the stage
    """
    scripts: list[SRScript]
    comments: list[SRComment]
    costumes: list[SRVectorCostume | SRBitmapCostume]
    sounds: list[SRSound]
    costume_index: int
    volume: int | float

    def validate(self, path: list, info_api: OpcodeInfoAPI) -> None:
        """
        Ensure a SRTarget is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRTarget is invalid
            MANIP_SameValueTwiceError(MANIP_ValidationError): if two costumes or two sounds have the same name
        """
        AA_LIST_OF_TYPE(self, path, "scripts", SRScript)
        AA_LIST_OF_TYPE(self, path, "comments", SRComment)
        AA_LIST_OF_TYPES(self, path, "costumes", (SRVectorCostume, SRBitmapCostume))
        AA_MIN_LEN(self, path, "costumes", min_len=1)
        AA_LIST_OF_TYPE(self, path, "sounds", SRSound)
        AA_TYPE(self, path, "costume_index", int)
        AA_RANGE(self, path, "costume_index", 
            min=0, max=len(self.costumes)-1, condition=f"In this case the sprite has {len(self.costumes)} costume(s)",
        )
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
                raise MANIP_SameValueTwiceError(other_path, current_path, "Two costumes must not have the same name")
            defined_costumes[costume.name] = current_path
        
        defined_sounds = {}
        for i, sound in enumerate(self.sounds):
            current_path = path+["sounds", i]
            sound.validate(path)
            if sound.name in defined_sounds:
                other_path = defined_sounds[sound.name]
                raise MANIP_SameValueTwiceError(other_path, current_path, "Two sounds must not have the same name")
            defined_sounds[sound.name] = current_path
    
    def validate_scripts(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        context: PartialContext,
    ) -> None:
        """
        Ensure the scripts of a SRTarget are valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            context: Context about parts of the project. Used to validate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the scripts of the SRTarget are invalid
            MANIP_SameValueTwiceError(MANIP_ValidationError): if two custom blocks have the same custom_opcode.
        """
        context = self._get_complete_context(partial_context=context)
        validation_if = ValidationIF(scripts=self.scripts)
        cb_custom_opcodes = {}
        for i, script in enumerate(self.scripts):
            script.validate(
                path           = path+["scripts", i],
                info_api       = info_api,
                validation_if = validation_if,
                context        = context,
            )
            for j, block in enumerate(script.blocks):
                current_path = path+["scripts", i, "blocks", j]
                if isinstance(block.mutation, SRCustomBlockMutation):
                    custom_opcode = block.mutation.custom_opcode
                    if custom_opcode in cb_custom_opcodes:
                        other_path = cb_custom_opcodes[custom_opcode]
                        raise MANIP_SameValueTwiceError(
                            other_path, current_path, "Two custom blocks must not have the same custom_opcode(see .mutation.custom_opcode)",
                        )
                    cb_custom_opcodes[custom_opcode] = current_path

    def _get_complete_context(self, partial_context: PartialContext) -> CompleteContext:
        """
        Gets the complete context for a SRTarget from the given partial context (project context)

        Args:
            partial_context: the partial context (project context)
        
        Returns:
            the complete context
        """
        return CompleteContext.from_partial(
            pc       = partial_context,
            costumes = [(DropdownValueKind.COSTUME, costume.name) for costume in self.costumes],
            sounds   = [(DropdownValueKind.SOUND  , sound  .name) for sound   in self.sounds  ],
            is_stage = isinstance(self, SRStage),
        )
    
    def _to_first_common(self,
        info_api: OpcodeInfoAPI,
        global_vars: list[SRVariable],
        global_lists: list[SRList],
        global_monitors: list[SRMonitor]|None,
    ) -> tuple[
        dict[str, FRBlock], dict[str, FRComment],
        list[FRCostume], list[FRSound],
        dict[str, tuple[str, str]|tuple[str, str, bool]],
        dict[str, tuple[str, str]],
        list[FRMonitor],
        dict[str, bytes],
    ]:
        """
        Convert common fields into first representation

        Args:
            info_api: the opcode info api used to fetch information about opcodes
            global_vars: a list of global variables
            global_lists: a list of global lists
            global_monitors: the non-local monitors (only needed for a SRStage)
        
        Returns:
            the blocks, comments, costumes, sounds, variables, lists and monitors in first representation
            and the file contents of the target assets
        """
        if   isinstance(self, SRStage):
            sprite_name   = None
            new_variables = global_vars
            new_lists     = global_lists
            local_vars    = []
            local_lists   = []
            new_monitors  = global_monitors
        elif isinstance(self, SRSprite):
            sprite_name   = self.name
            new_variables = self.local_variables
            new_lists     = self.local_lists
            local_vars    = self.local_variables
            local_lists   = self.local_lists
            new_monitors  = self.local_monitors
        
        sti_if = SecondToInterIF(scripts=self.scripts)
        for script in self.scripts:
            top_level_id = script.to_inter(sti_if, info_api)
        
        itf_if = InterToFirstIF(
            blocks=sti_if.produced_blocks,
            global_vars=[variable.name for variable in global_vars],
            global_lists=[list_.name for list_ in global_lists],
            local_vars=[variable.name for variable in local_vars],
            local_lists=[list_.name for list_ in local_lists],
            sprite_name=sprite_name,
            _next_block_id_num=sti_if._next_block_id_num, # to avoid reusing the same ids
        )
        
        id_to_parent_id = {}
        for block_id, block in sti_if.produced_blocks.items():
            block_ids = block.get_references()
            for block_id in block_ids:
                id_to_parent_id[block_id] = block_id
        
        for block_id, block in sti_if.produced_blocks.items():
            old_block = block.to_first(
                itf_if, info_api,
                parent_id=id_to_parent_id.get(block_id, None),
                # blocks not included must be independent because they are never referenced
                own_id=block_id,
            )
            itf_if.schedule_block_addition(block_id, old_block)
        
        [itf_if.add_comment(comment.to_first(block_id=None), floating=True) for comment in self.comments]
        
        asset_files = {}
        old_costumes = []
        for costume in self.costumes:
            old_costume, file_bytes = costume.to_first()
            old_costumes.append(old_costume)
            asset_files[old_costume.md5ext] = file_bytes
        old_sounds = []
        for sound in self.sounds:
            old_sound, file_bytes = sound.to_first()
            old_sounds.append(old_sound)
            asset_files[old_sound.md5ext] = file_bytes

        old_variables = {
            itf_if.get_variable_sha256(variable.name): variable.to_tuple()
            for variable in new_variables
        }
        old_lists = {
            itf_if.get_list_sha256(list_.name): list_.to_tuple()
            for list_ in new_lists
        }
        old_monitors = [monitor.to_first(itf_if, info_api) for monitor in new_monitors]

        return (
            itf_if.added_blocks, itf_if.added_comments,
            old_costumes, old_sounds,
            old_variables, old_lists,
            old_monitors,
            asset_files,
        )        
        

@grepr_dataclass(grepr_fields=[], init=True)
class SRStage(SRTarget):
    """
    The second representation (SR) of the stage, which is much more user friendly
    """

    @classmethod
    def create_empty(cls) -> "SRTarget":
        """
        Create an empty SRTarget with no scripts, costumes etc. and the default settings
        
        Returns:
            the empty SRTarget
        """
        return cls(
            scripts=[],
            comments=[],
            costumes=[SRVectorCostume.create_empty()],
            sounds=[],
            costume_index=0,
            volume=100,
        )

    def to_first(self, 
        info_api: OpcodeInfoAPI,
        global_vars: list[SRVariable],
        global_lists: list[SRList],
        global_monitors: list[SRMonitor],
        broadcast_messages: list[str],
        tempo: int,
        video_transparency: int | float,
        video_state: str,
        text_to_speech_language: str | None,
    ) -> tuple[FRStage, list[FRMonitor], dict[str, bytes]]:
        """
        Converts a SRStage into a FRStage
        
        Args:
            info_api: the opcode info api used to fetch information about opcodes
            global_vars: a list of global variables
            global_lists: a list of global lists
            global_monitors: the non-local monitors
            broadcast_messages: the broadcast messages used in the project
            tempo: the music extension tempo
            video_transparency: the video extensions transparency
            video_state: the state of the video extension
            text_to_speech_language: the tts language of the tts extension
        
        Returns:
            the FRStage, a list of global monitors and the resulting asset files
        """

        (
            old_blocks, old_comments,
            old_costumes, old_sounds,
            old_variables, old_lists,
            old_global_monitors,
            asset_files,
        ) = super()._to_first_common(
            info_api,
            global_vars, global_lists,
            global_monitors,
        )
        old_broadcasts = {
            string_to_sha256(broadcast_name, secondary=SHA256_SEC_BROADCAST_MSG): broadcast_name
            for broadcast_name in broadcast_messages
        }
        old_stage = FRStage(
            is_stage                = True,
            name                    = "Stage",
            variables               = old_variables,
            lists                   = old_lists,
            broadcasts              = old_broadcasts,
            custom_vars             = [], # Seems to have no purpose
            blocks                  = old_blocks,
            comments                = old_comments,
            costumes                = old_costumes,
            sounds                  = old_sounds,
            current_costume         = self.costume_index,
            volume                  = self.volume,
            layer_order             = 0, # stage is always on the bottom
            id                      = string_to_sha256("_stage_", secondary=SHA256_SEC_TARGET_NAME),

            tempo                   = tempo,
            video_transparency      = video_transparency,
            video_state             = video_state,
            text_to_speech_language = text_to_speech_language,
        )
        return (old_stage, old_global_monitors, asset_files)

@grepr_dataclass(grepr_fields=["name", "local_variables", "local_lists", "local_monitors", "is_visible", "position", "size", "direction", "is_draggable", " rotation_style", "uuid"])
class SRSprite(SRTarget):
    """
    The second representation (SR) of a sprite, which is much more user friendly
    """
    
    name: str
    local_variables: list[SRVariable]
    local_lists: list[SRList]
    local_monitors: list[SRMonitor] # TODO: disambig local vs. local
    is_visible: bool
    position: tuple[int | float, int | float]
    size: int | float
    direction: int | float
    is_draggable: bool
    rotation_style: "SRSpriteRotationStyle"
    uuid: UUID = field(default_factory=uuid4, init=False, compare=False)
    
    @classmethod
    def create_empty(cls, name: str) -> "SRSprite":
        """
        Create an empty SRSprite with no scripts, costumes, variables, local monitors etc. and the default settings
        
        Returns:
            the empty SRSprite
        """
        return cls(
            scripts=[],
            comments=[],
            costumes=[SRVectorCostume.create_empty()],
            sounds=[],
            costume_index=0,
            volume=100,
            
            name=name,
            local_variables=[],
            local_lists=[],
            local_monitors=[],
            is_visible=True,
            position=(0, 0),
            size=100,
            direction=90,
            is_draggable=False,
            rotation_style=SRSpriteRotationStyle.ALL_AROUND,
        )

    def __setattr__(self, name, value):
        if name == "uuid" and hasattr(self, "uuid"):
            raise AttributeError('Cannot modify "uuid" after creation')
        super().__setattr__(name, value)
    
    def validate(self, path: list, info_api: OpcodeInfoAPI) -> None:
        """
        Ensure a SRSprite is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRSprite is invalid
        """
        super().validate(path, info_api)
        
        AA_TYPE(self, path, "name", str)
        AA_NOT_ONE_OF(self, path, "name", ["_myself_", "_stage_", "_mouse_", "_edge_"])
        AA_LIST_OF_TYPE(self, path, "local_variables", SRVariable)
        AA_LIST_OF_TYPE(self, path, "local_lists", SRList)
        AA_LIST_OF_TYPE(self, path, "local_monitors", SRMonitor)
        AA_TYPE(self, path, "is_visible", bool)
        AA_COORD_PAIR(self, path, "position")
        AA_TYPES(self, path, "size", (int, float))
        AA_MIN(self, path, "size", min=0)
        AA_TYPES(self, path, "direction", (int, float))
        AA_RANGE(self, path, "direction", min=-180, max=180)
        AA_TYPE(self, path, "is_draggable", bool)
        AA_TYPE(self, path, "rotation_style", SRSpriteRotationStyle)
        AA_TYPE(self, path, "uuid", UUID)
        
        
        for i, variable in enumerate(self.local_variables):
            variable.validate(path+["local_variables", i])
        for i, list_ in enumerate(self.local_lists):
            list_.validate(path+["local_lists", i])
        
        for i, monitor in enumerate(self.local_monitors):
            monitor.validate(path+["local_monitors", i], info_api)
    
    def validate_monitor_dropdown_values(self, 
        path: list, 
        info_api: OpcodeInfoAPI,
        context: PartialContext | CompleteContext,
    ) -> None:
        """
        Ensure the dropdown values of the monitors of a SRSprite are valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
            context: Context about parts of the project. Used to validate dropdowns
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the monitor dropdown values of the SRSprite are invalid
        """
        context = self._get_complete_context(partial_context=context)
        for i, monitor in enumerate(self.local_monitors):
            monitor.validate_dropdown_values(
                path     = path+["local_monitors", i], 
                info_api = info_api, 
                context  = context,
            )

    def to_first(self, 
        info_api: OpcodeInfoAPI,
        global_vars: list[SRVariable],
        global_lists: list[SRList],
        layer_order: int,
    ) -> tuple[FRSprite, list[FRMonitor], dict[str, bytes]]:
        """
        Converts a SRSprite into a FRSprite
        
        Args:
            info_api: the opcode info api used to fetch information about opcodes
            global_vars: a list of global variables
            global_lists: a list of global lists
            layer_order: the relative layer the sprite is on
        
        Returns:
            the FRSprite and the resulting asset files
        """

        (
            old_blocks, old_comments,
            old_costumes, old_sounds,
            old_variables, old_lists,
            old_monitors,
            asset_files,
        ) = super()._to_first_common(
            info_api,
            global_vars, global_lists,
            global_monitors=None,
        )
        old_stage = FRSprite(
            is_stage                = False,
            name                    = self.name,
            variables               = old_variables,
            lists                   = old_lists,
            broadcasts              = {}, # Seems to always be empty
            custom_vars             = [], # Seems to have no purpose
            blocks                  = old_blocks,
            comments                = old_comments,
            costumes                = old_costumes,
            sounds                  = old_sounds,
            current_costume         = self.costume_index,
            volume                  = self.volume,
            layer_order             = layer_order,
            id                      = string_to_sha256(self.name, secondary=SHA256_SEC_TARGET_NAME),

            visible                 = self.is_visible,
            x                       = self.position[0],
            y                       = self.position[1],
            size                    = self.size,
            direction               = self.direction,
            draggable               = self.is_draggable,
            rotation_style          = self.rotation_style.to_code(),
        )
        return (old_stage, old_monitors, asset_files)


__all__ = ["FRTarget", "FRStage", "FRSprite", "SRTarget", "SRStage", "SRSprite"]

