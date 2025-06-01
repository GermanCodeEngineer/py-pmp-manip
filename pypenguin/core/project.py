from json        import loads
from uuid        import UUID

from pypenguin.utility     import (
    read_all_files_of_zip, string_to_sha256, ThanksError, grepr_dataclass, ValidationConfig, 
    AA_TYPE, AA_NONE_OR_TYPE, AA_TYPES, AA_LIST_OF_TYPE, AA_RANGE, AA_EXACT_LEN,
    SameValueTwiceError, SpriteLayerStackError,
)
from pypenguin.opcode_info import OpcodeInfoAPI, DropdownValueKind

from pypenguin.core.context       import PartialContext
from pypenguin.core.extension     import SRExtension, SRCustomExtension, SRBuiltinExtension
from pypenguin.core.meta          import FRMeta
from pypenguin.core.monitor       import FRMonitor, SRMonitor
from pypenguin.core.enums         import SRTTSLanguage, SRVideoState
from pypenguin.core.target        import FRTarget, FRStage, FRSprite, SRStage, SRSprite
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
    asset_files: dict[str, bytes]

    @classmethod
    def from_data(cls, 
        data: dict, 
        asset_files: dict[str, bytes], 
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
                (FRStage if i==0 else FRSprite).from_data(target_data, info_api=info_api)
                for i, target_data in enumerate(data["targets"])
            ],
            monitors = [
                FRMonitor.from_data(monitor_data) 
                for monitor_data in data["monitors"]
            ],
            extension_data = data.get("extensionData", {}),
            extensions     = data["extensions"   ],
            extension_urls = data.get("extensionURLs", {}),
            meta           = FRMeta.from_data(data["meta"]),
            asset_files    = asset_files,
        )
    
    @classmethod
    def _data_sb3_to_pmp(cls, project_data: dict) -> dict: # TODO: add test
        """
        *[Internal Method]* Adapt sb3 project data to the pmp project data format

        Args:
            project_data: the project data in sb3 format
        
        Returns:
            the project data in pmp format
        """
        for i, sprite_data in enumerate(project_data["targets"]):
            sprite_name = "_stage_" if i == 0 else sprite_data["name"]
            sprite_data["id"] = string_to_sha256(primary=sprite_name)
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
        del contents["project.json"]
        if   file_path.endswith(".sb3"):
            project_data = FRProject._data_sb3_to_pmp(project_data)
        return FRProject.from_data(project_data, asset_files=contents, info_api=info_api)

    def __post_init__(self) -> None:
        """
        Ensure my assumption about extension_data was correct
        
        Returns:
            None
        """
        if self.extension_data != {}: raise ThanksError()

    def step(self, info_api: OpcodeInfoAPI):
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
                new_stage, all_sprite_variables, all_sprite_lists = old_stage.step(
                    asset_files=self.asset_files, 
                    info_api=info_api,
                )
            else:
                target: FRSprite
                new_sprite, _, _ = target.step(
                    asset_files=self.asset_files, 
                    info_api=info_api,
                )
                new_sprite: SRSprite
                new_sprites.append(new_sprite)
                sprite_layer_stack_dict[target.layer_order] = new_sprite.uuid
        
        global_monitors = []
        sprite_names = [sprite.name for sprite in new_sprites]
        for monitor in self.monitors:
            monitor_sprite_name, new_monitor = monitor.step(info_api=info_api, sprite_names=sprite_names)
            if new_monitor is None: 
                continue
            if monitor_sprite_name is None:
                global_monitors.append(new_monitor)
            else:
                sprite_index = sprite_names.index(monitor_sprite_name)
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

    def __eq__(self, other) -> bool: # TODO: test
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

        if self.sprites != other.sprites:
            return False

        if len(self.sprite_layer_stack) != len(other.sprite_layer_stack):
            return False

        self_uuid_to_sprite  = {sprite.uuid: sprite for sprite in self.sprites}
        other_uuid_to_sprite = {sprite.uuid: sprite for sprite in other.sprites}

        for self_uuid, other_uuid in zip(self.sprite_layer_stack, other.sprite_layer_stack):
            if self_uuid_to_sprite.get(self_uuid) != other_uuid_to_sprite.get(other_uuid):
                return False

        return (
            self.stage == other.stage and
            self.all_sprite_variables == other.all_sprite_variables and
            self.all_sprite_lists == other.all_sprite_lists and
            self.tempo == other.tempo and
            self.video_transparency == other.video_transparency and
            self.text_to_speech_language == other.text_to_speech_language and
            self.global_monitors == other.global_monitors and
            self.extensions == other.extensions
        ) # TODO: optimize (move this up for performance)

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
        *[Internal Method]* Ensure the sprites of a SRProject are valid, raise ValidationError if not
        
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
                other_path = stack_uuid_paths[sprite.uuid]
                raise SameValueTwiceError(other_path, current_path, "The same UUID mustn't be included twice")
            if uuid not in sprite_uuid_paths:
                raise SpriteLayerStackError(current_path, "Must be the UUID of an existing sprite")
            stack_uuid_paths[uuid] = current_path
        # same length and uniqueness is assured and every UUID must have a partner sprite
        # => no sprite can possibly be missing a partner UUID
        
            

    def _validate_var_names(self, path: list, config: ValidationConfig) -> None:
        """
        *[Internal Method]* Ensures no variables with the same name exist

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
        *[Internal Method]* Ensures no lists with the same name exist

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


__all__ = ["FRProject", "SRProject"]

