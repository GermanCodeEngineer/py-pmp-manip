from copy   import copy, deepcopy
from json   import loads
from typing import Any
from uuid   import UUID

from pypenguin.important_consts import SHA256_SEC_TARGET_NAME
from pypenguin.opcode_info.api  import OpcodeInfoAPI, DropdownValueKind
from pypenguin.utility          import (
    grepr_dataclass, read_all_files_of_zip, create_zip_file, string_to_sha256, gdumps, ValidationConfig, KeyReprDict,
    AA_TYPE, AA_NONE_OR_TYPE, AA_TYPES, AA_LIST_OF_TYPE, AA_RANGE, AA_EXACT_LEN,
    ThanksError, SameValueTwiceError, SpriteLayerStackError,
)

from pypenguin.core.context       import PartialContext
from pypenguin.core.extension     import SRExtension, SRCustomExtension, SRBuiltinExtension
from pypenguin.core.meta          import FRMeta
from pypenguin.core.monitor       import FRMonitor, SRMonitor
from pypenguin.core.enums         import SRTTSLanguage, SRVideoState, TargetPlatform
from pypenguin.core.target        import FRTarget, FRStage, FRSprite, SRTarget, SRStage, SRSprite
from pypenguin.core.vars_lists    import SRVariable, SRList


@grepr_dataclass(grepr_fields=["targets", "monitors", "extension_data", "extensions", "extension_urls", "meta", "asset_files"])
class FRProject: 
    """
    The first representation (FR) of the project data tree. Its data is equivalent to the data stored in a .pmp file
    """

    targets: list[FRTarget]
    monitors: list[FRMonitor]
    extension_data: dict # I couldn't find out what it would be used for, seems to be always {}
    extensions: list[str]
    extension_urls: dict[str, str]
    meta: FRMeta
    asset_files: KeyReprDict[str, bytes] 
    # using KeyReprDict here to only show file names and not their gigantic byte values in repr

    @classmethod
    def from_data(cls, 
        data: dict, 
        asset_files: KeyReprDict[str, bytes], 
        info_api: OpcodeInfoAPI,
    ) -> "FRProject":
        """
        Deserializes raw data into a FRProject
        
        Args:
            data: the raw data
            asset_files: the contents of the costume and sound files
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the FRProject
        """
        return cls(
            targets = [
                (FRStage if i==0 else FRSprite).from_data(target_data, info_api)
                for i, target_data in enumerate(data["targets"])
            ],
            monitors = [
                FRMonitor.from_data(monitor_data) 
                for monitor_data in data["monitors"]
            ],
            extension_data = deepcopy(data.get("extensionData", {})),
            extensions     = copy(data["extensions"]),
            extension_urls = copy(data.get("extensionURLs", {})),
            meta           = FRMeta.from_data(data["meta"]),
            asset_files    = copy(asset_files),
        )
    
    def to_data(self) -> tuple[dict[str, Any], KeyReprDict[str, bytes]]:
        """
        Serializes a FRProject into json data
        
        Returns:
            the json data and the asset files
        """
        data = {
            "targets"      : [target.to_data() for target in self.targets],
            "monitors"     : [monitor.to_data() for monitor in self.monitors],
            "extensionData": deepcopy(self.extension_data),
            "extensions"   : copy(self.extensions),
            "extensionURLs": copy(self.extension_urls),
            "meta"         : self.meta.to_data(),
        }
        return (data, copy(self.asset_files))

    @staticmethod
    def _data_sb3_to_pmp(project_data: dict) -> dict:
        """
        Adapt sb3 project data to the pmp project data format

        Args:
            project_data: the project data in sb3 format
        
        Returns:
            the project data in pmp format
        """
        for i, sprite_data in enumerate(project_data["targets"]):
            sprite_name = "_stage_" if i == 0 else sprite_data["name"]
            sprite_data["id"] = string_to_sha256(sprite_name, secondary=SHA256_SEC_TARGET_NAME)
        return project_data

    @classmethod
    def from_file(cls, file_path: str, info_api: OpcodeInfoAPI) -> "FRProject":
        """
        Reads project data from a project file(.sb3 or .pmp) and creates a FRProject from it

        Args:
            file_path: file path to the .sb3 or .pmp file
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the FRProject
        """
        assert file_path.endswith(".sb3") or file_path.endswith(".pmp")
        contents = read_all_files_of_zip(file_path)
        project_data = loads(contents["project.json"].decode("utf-8"))
        print(FRProject.__repr__(project_data|{"extensionURLs": ...}))
        input()
        del contents["project.json"]
        if   file_path.endswith(".sb3"):
            project_data = FRProject._data_sb3_to_pmp(project_data)
        return FRProject.from_data(project_data, asset_files=KeyReprDict(contents), info_api=info_api)

    def __post_init__(self) -> None:
        """
        Ensure my assumption about extension_data was correct
        
        Returns:
            None
        """
        if self.extension_data != {}: raise ThanksError()

    def to_file(self, file_path: str) -> None:
        """
        Writes the project data to a project file(.sb3 or .pmp)

        Args:
            file_path: file path to the .sb3 or .pmp file
        
        Returns:
            the FRProject
        """
        assert file_path.endswith(".sb3") or file_path.endswith(".pmp")
        project_data, asset_files = self.to_data()
        contents = asset_files
        contents["project.json"] = gdumps(project_data).encode("utf-8")
        create_zip_file(file_path, contents)

    def to_second(self, info_api: OpcodeInfoAPI) -> "SRProject":
        """
        Converts a FRProject into a SRProject
        
        Args:
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the SRProject
        """
        old_stage: FRStage
        new_stage: SRStage
        new_sprites: list[SRSprite] = []
        sprite_layer_stack_dict = {}
        for target in self.targets:
            if  target.is_stage:
                old_stage: FRStage = target
                new_stage, all_sprite_variables, all_sprite_lists = old_stage.to_second(
                    asset_files=self.asset_files, 
                    info_api=info_api,
                )
            else:
                target: FRSprite
                new_sprite, _, _ = target.to_second(
                    asset_files=self.asset_files, 
                    info_api=info_api,
                )
                new_sprite: SRSprite
                new_sprites.append(new_sprite)
                sprite_layer_stack_dict[target.layer_order] = new_sprite.uuid
        
        global_monitors = []
        sprite_names = [sprite.name for sprite in new_sprites]
        for monitor in self.monitors:
            new_monitor = monitor.to_second(info_api, sprite_names)
            if new_monitor is None: 
                continue
            if monitor.sprite_name is None:
                global_monitors.append(new_monitor)
            else:
                sprite_index = sprite_names.index(monitor.sprite_name)
                new_sprites[sprite_index].local_monitors.append(new_monitor)
       
        if old_stage.text_to_speech_language is None:
            new_tts_language = None
        else:
            new_tts_language = SRTTSLanguage.from_code(old_stage.text_to_speech_language)
        
        new_extensions = []
        for extension_id in self.extensions:
            if extension_id in self.extension_urls.keys():
                new_extensions.append(SRCustomExtension(
                    id  = extension_id,
                    url = self.extension_urls[extension_id],
                ))
            else:
                new_extensions.append(SRBuiltinExtension(
                    id  = extension_id,
                ))
        
        return SRProject(
            stage                   = new_stage,
            sprites                 = new_sprites,
            sprite_layer_stack      = [pair[1] for pair in sorted(sprite_layer_stack_dict.items())],
            all_sprite_variables    = all_sprite_variables,
            all_sprite_lists        = all_sprite_lists,
            tempo                   = old_stage.tempo,
            video_transparency      = old_stage.video_transparency,
            video_state             = SRVideoState.from_code(old_stage.video_state),
            text_to_speech_language = new_tts_language,
            global_monitors         = global_monitors,
            extensions              = new_extensions,
        )


@grepr_dataclass(grepr_fields=["stage", "sprites", "sprite_layer_stack", "all_sprite_variables", "all_sprite_lists", "tempo", "video_transparency", "video_state", "text_to_speech_language", "global_monitors", "extensions"], eq=False)
class SRProject:
    """
    The second representation (SR) of a Scratch/PenguinMod Project
    """
    
    stage: SRStage
    sprites: list[SRSprite]
    sprite_layer_stack: list[UUID]
    all_sprite_variables: list[SRVariable]
    all_sprite_lists: list[SRList]
    tempo: int
    video_transparency: int | float # There seems to be no limit
    video_state: SRVideoState
    text_to_speech_language: SRTTSLanguage | None
    global_monitors: list[SRMonitor]
    extensions: list[SRExtension]

    @classmethod
    def create_empty(cls) -> "SRProject":
        """
        Create an empty SRProject with no sprites, variables etc. and the default settings
        
        Returns:
            the empty SRProject
        """
        return cls(
            stage=SRStage.create_empty(),
            sprites=[],
            sprite_layer_stack=[],
            all_sprite_variables=[],
            all_sprite_lists=[],
            tempo=60,
            video_transparency=50,
            video_state=SRVideoState.ON,
            text_to_speech_language=None,
            global_monitors=[],
            extensions=[],
        )

    def __eq__(self, other) -> bool:
        """
        Checks whether a SRProject is equal to another.
        Requires same sprites and sprite layer stack order.
        Ignores mismatched UUIDs, which would otherwise make equality impossible.

        Args:
            other: the object to compare to

        Returns:
            bool: wether self is equal to other
        """
        if not isinstance(other, SRProject):
            return NotImplemented
        
        if (
            self.stage != other.stage or
            self.sprites != other.sprites or
            self.all_sprite_variables != other.all_sprite_variables or
            self.all_sprite_lists != other.all_sprite_lists or
            self.tempo != other.tempo or
            self.video_transparency != other.video_transparency or
            self.text_to_speech_language != other.text_to_speech_language or
            self.global_monitors != other.global_monitors or
            self.extensions != other.extensions
        ):
            return False

        if len(self.sprite_layer_stack) != len(other.sprite_layer_stack):
            return False

        self_uuid_to_sprite  = {sprite.uuid: sprite for sprite in self.sprites}
        other_uuid_to_sprite = {sprite.uuid: sprite for sprite in other.sprites}

        for self_uuid, other_uuid in zip(self.sprite_layer_stack, other.sprite_layer_stack):
            if self_uuid_to_sprite.get(self_uuid) != other_uuid_to_sprite.get(other_uuid):
                return False

        return True

    def validate(self, config: ValidationConfig, info_api: OpcodeInfoAPI) -> None:
        """
        Ensure a SRProject is valid, raise ValidationError if not
        
        Args:
            config: Configuration for Validation Behaviour
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRProject is invalid
            SameValueTwiceError(ValidationError): if two sprites have the same name
        """
        path = []
        AA_TYPE(self, path, "stage", SRStage)
        AA_LIST_OF_TYPE(self, path, "sprites", SRSprite)
        AA_LIST_OF_TYPE(self, path, "sprite_layer_stack", UUID)
        AA_EXACT_LEN(self, path, "sprite_layer_stack", 
            length=len(self.sprites), condition=f"In this case the project has {len(self.sprites)} sprites(s)"
        )
        AA_LIST_OF_TYPE(self, path, "all_sprite_variables", SRVariable)
        AA_LIST_OF_TYPE(self, path, "all_sprite_lists", SRList)
        AA_TYPE(self, path, "tempo", int)
        AA_RANGE(self, path, "tempo", min=20, max=500)
        AA_TYPES(self, path, "video_transparency", (int, float))
        AA_TYPE(self, path, "video_state", SRVideoState)
        AA_NONE_OR_TYPE(self, path, "text_to_speech_language", SRTTSLanguage)
        AA_LIST_OF_TYPE(self, path, "global_monitors", SRMonitor)
        AA_LIST_OF_TYPE(self, path, "extensions", SRExtension)
        
        self.stage.validate(path+["stage"], config, info_api)

        self._validate_sprites(path, config, info_api)
        
        for i, variable in enumerate(self.all_sprite_variables):
            variable.validate(path+["all_sprite_variables", i], config)
        for i, list_ in enumerate(self.all_sprite_lists):
            list_.validate(path+["all_sprite_lists", i], config)
        
        self._validate_var_names(path, config)
        self._validate_list_names(path, config)
        
        for i, monitor in enumerate(self.global_monitors):
            monitor.validate(path+["global_monitors", i], config, info_api)
        
        for i, extension in enumerate(self.extensions):
            extension.validate(path+["extensions", i], config)
        
        # 1. Ensure no same sprite name
        # 2. Validate Dropdown Values
        defined_sprites      = {}
        sprite_only_variables = {None: []}
        sprite_only_lists     = {None: []}
        for i, sprite in enumerate(self.sprites):
            current_path = path+["sprites", i]
            if sprite.name in defined_sprites:
                other_path = defined_sprites[sprite.name]
                raise SameValueTwiceError(other_path, current_path, "Two sprites mustn't have the same name")
            defined_sprites[sprite.name] = current_path
            sprite_only_variables[sprite.name] = [
                (DropdownValueKind.VARIABLE, variable.name) for variable in sprite.sprite_only_variables]
            sprite_only_lists    [sprite.name] = [
                (DropdownValueKind.LIST    , list_   .name) for list_    in sprite.sprite_only_lists]
        
        all_sprite_variables = [(DropdownValueKind.VARIABLE, variable.name) for variable in self.all_sprite_variables]
        all_sprite_lists     = [(DropdownValueKind.LIST    , list_   .name) for list_    in self.all_sprite_lists    ]
        backdrops            = [(DropdownValueKind.BACKDROP, backdrop.name) for backdrop in self.stage.costumes      ]
        for i, target in enumerate([self.stage]+self.sprites):
            if i == 0:
                target_key = None
                current_path = path+["stage"]
            else:
                target_key = target.name
                current_path = path+["sprites", i-1]
            partial_context = PartialContext(
                scope_variables       = all_sprite_variables + sprite_only_variables[target_key],
                scope_lists           = all_sprite_lists     + sprite_only_lists    [target_key],
                all_sprite_variables  = all_sprite_variables,
                sprite_only_variables = sprite_only_variables,
                sprite_only_lists     = sprite_only_lists,
                other_sprites         = [
                    (DropdownValueKind.SPRITE, sprite_name) for sprite_name in defined_sprites.keys()],
                backdrops             = backdrops,
            )
            target.validate_scripts(
                path     = current_path, 
                config   = config,
                info_api = info_api, 
                context  = partial_context,
            )
            if i == 0: 
                global_context = partial_context
            else:
                target: SRSprite
                target.validate_monitor_dropdown_values(
                    path     = current_path, 
                    config   = config,
                    info_api = info_api, 
                    context  = partial_context,
                )
        
        for i, monitor in enumerate(self.global_monitors):
            monitor.validate_dropdown_values(
                path     = path+["global_monitors", i], 
                config   = config,
                info_api = info_api, 
                context  = global_context,
            )

    def _validate_sprites(self, path: list, config: ValidationConfig, info_api: OpcodeInfoAPI) -> None:
        """
        Ensure the sprites of a SRProject are valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        
        Raises:
            SameValueTwiceError(ValidationError): if two sprites have the same UUID **OR** if the same UUID is included twice in sprite_layer_stack 
            SpriteLayerStackError(ValidationError): if the sprite_layer_stack contains a UUID which belongs to no sprite 
        """
        sprite_uuid_paths: dict[UUID, list] = {}
        for i, sprite in enumerate(self.sprites):
            current_path = path+["sprites", i]
            sprite.validate(current_path, config, info_api)
            if sprite.uuid in sprite_uuid_paths:
                other_path = sprite_uuid_paths[sprite.uuid]
                raise SameValueTwiceError(other_path, current_path, "Two sprites mustn't have the same UUID")
            sprite_uuid_paths[sprite.uuid] = current_path
        

        stack_uuid_paths: dict[UUID, list] = {}
        for i, uuid in enumerate(self.sprite_layer_stack):
            current_path = path+["sprite_layer_stack", i]
            if uuid in stack_uuid_paths:
                other_path = stack_uuid_paths[uuid]
                raise SameValueTwiceError(other_path, current_path, "The same UUID mustn't be included twice")
            if uuid not in sprite_uuid_paths:
                raise SpriteLayerStackError(current_path, "Must be the UUID of an existing sprite")
            stack_uuid_paths[uuid] = current_path
        # same length and uniqueness is assured and every UUID must have a partner sprite
        # => no sprite can possibly be missing a partner UUID
        
    def _validate_var_names(self, path: list, config: ValidationConfig) -> None:
        """
        Ensures no variables with the same name exist

        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            SameValueTwiceError(ValidationError): if the project contains vars with the same name
        """
        defined_variables = {}
        for i, variable in enumerate(self.all_sprite_variables):
            current_path = path+["all_sprite_variables", i]
            if variable.name in defined_variables:
                other_path = defined_variables[variable.name]
                raise SameValueTwiceError(other_path, current_path, "Two variables mustn't have the same name")
            defined_variables[variable.name] = current_path
        
        for i, sprite in enumerate(self.sprites):
            for j, variable in enumerate(sprite.sprite_only_variables):
                current_path = path+["sprites", i, "sprite_only_variables", j]
                if variable.name in defined_variables:
                    other_path = defined_variables[variable.name]
                    raise SameValueTwiceError(other_path, current_path, "Two variables mustn't have the same name")
                defined_variables[variable.name] = current_path
        
    def _validate_list_names(self, path: list, config: ValidationConfig) -> None:
        """
        Ensures no lists with the same name exist

        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            SameValueTwiceError(ValidationError): if the project contains lists with the same name
        """
        defined_lists = {}
        for i, list_ in enumerate(self.all_sprite_lists):
            current_path = path+["all_sprite_lists", i]
            if list_.name in defined_lists:
                other_path = defined_lists[list_.name]
                raise SameValueTwiceError(other_path, current_path, "Two lists mustn't have the same name")
            defined_lists[list_.name] = current_path
        
        for i, sprite in enumerate(self.sprites):
            for j, list_ in enumerate(sprite.sprite_only_lists):
                current_path = path+["sprites", i, "sprite_only_lists", j]
                if list_.name in defined_lists:
                    other_path = defined_lists[list_.name]
                    raise SameValueTwiceError(other_path, current_path, "Two lists mustn't have the same name")
                defined_lists[list_.name] = current_path
    
    def _find_broadcast_messages(self) -> list[str]:
        """
        Finds the used broadcast messages in all sprites and the stage
        
        Returns:
            the used broadcast messages
        """
        broadcast_messages = []
        for target in ([self.stage] + self.sprites):
            target: SRTarget
            for script in target.scripts:
                for block in script.blocks:
                    broadcast_messages.extend(block.find_broadcast_messages())
        return broadcast_messages
    
    
    def to_first(self, info_api: OpcodeInfoAPI, target_platform: TargetPlatform) -> FRProject:
        """
        Converts a SRProject into a FRProject
        
        Args:
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the FRProject
        """

        old_targets  = []
        old_monitors = []
        asset_files  = KeyReprDict()
        tts_language = None if self.text_to_speech_language is None else self.text_to_speech_language.to_code()
        old_stage, old_global_monitors, stage_asset_files = self.stage.to_first(
            info_api                = info_api,
            global_vars             = self.all_sprite_variables,
            global_lists            = self.all_sprite_lists,
            global_monitors         = self.global_monitors,
            broadcast_messages      = self._find_broadcast_messages(),
            tempo                   = self.tempo,
            video_transparency      = self.video_transparency,
            video_state             = self.video_state.to_code(),
            text_to_speech_language = tts_language, # TODO: rename text_to_speech to tts
        )
        old_targets.append(old_stage)
        old_monitors.extend(old_global_monitors)
        asset_files.update(stage_asset_files)
        
        for new_sprite in self.sprites:
            old_sprite, old_local_monitors, sprite_asset_files = new_sprite.to_first(
                info_api     = info_api,
                global_vars  = self.all_sprite_variables,
                global_lists = self.all_sprite_lists,
                layer_order  = self.sprite_layer_stack.index(new_sprite.uuid) + 1,
            )
            old_targets.append(old_sprite)
            old_monitors.extend(old_local_monitors)
            asset_files.update(sprite_asset_files)

        extensions     = []
        extension_urls = {}
        for extension in self.extensions:
            extensions.append(extension.id)
            if isinstance(extension, SRCustomExtension):
                extension_urls[extension.id] = extension.url

        match target_platform:
            case TargetPlatform.SCRATCH:
                meta = FRMeta.new_scratch_meta()
            case TargetPlatform.PENGUINMOD:
                meta = FRMeta.new_penguinmod_meta()

        return FRProject(
            targets        = old_targets,
            monitors       = old_monitors,
            extension_data = {},
            extensions     = extensions,
            extension_urls = extension_urls,
            meta           = meta,
            asset_files    = asset_files,
        )


__all__ = ["FRProject", "SRProject"]

