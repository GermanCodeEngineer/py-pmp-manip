from __future__ import annotations
from copy       import copy, deepcopy
from io         import BytesIO
from json       import loads
from typing     import Any
from uuid       import UUID

from pmp_manip.important_consts import SHA256_SEC_TARGET_NAME
from pmp_manip.opcode_info.api  import OpcodeInfoAPI, DropdownValueKind
from pmp_manip.project_api      import SCRATCH_API, PENGUINMOD_API, fetch_projects
from pmp_manip.utility          import (
    grepr_dataclass, field, enforce_argument_types, 
    read_all_files_of_zip, create_zip_file, string_to_sha256, gdumps,
    KeyReprDict, AbstractTreePath, HasGreprValidate, ValidateAttribute,
    MANIP_SameValueTwiceError, MANIP_SpriteLayerStackError, MANIP_UnexpectedSubprocessError
)

from pmp_manip.core.context       import PartialContext
from pmp_manip.core.extension     import SRCustomExtension, SRBuiltinExtension
from pmp_manip.core.meta          import FRMeta
from pmp_manip.core.monitor       import FRMonitor, SRMonitor
from pmp_manip.core.enums         import SRTTSLanguage, SRVideoState, TargetPlatform
from pmp_manip.core.target        import FRTarget, FRStage, FRSprite, SRTarget, SRStage, SRSprite
from pmp_manip.core.vars_lists    import SRVariable, SRList


@grepr_dataclass()
class FRProject(HasGreprValidate): 
    """
    The first representation (FR) of the project data tree. Its data is equivalent to the data stored in a .pmp file
    """

    targets: list[FRTarget]
    monitors: list[FRMonitor]
    extension_data: dict # I could not find out what it would be used for, seems to be always {}
    extensions: list[str]
    extension_urls: dict[str, str]
    meta: FRMeta
    asset_files: dict[str, bytes] 
    # using KeyReprDict here to only show file names and not their gigantic byte values in repr

    @classmethod
    def from_data(cls, 
        data: dict, 
        asset_files: dict[str, bytes], 
    ) -> FRProject:
        """
        Deserializes json_data into a FRProject
        
        Args:
            data: the json_data
            asset_files: the contents of the costume and sound files
        
        Returns:
            the FRProject
        """
        return cls(
            targets = [
                (FRStage if i==0 else FRSprite).from_data(target_data)
                for i, target_data in enumerate(data["targets"])
            ],
            monitors = [
                FRMonitor.from_data(monitor_data) 
                for monitor_data in data["monitors"]
            ],
            extension_data = deepcopy(data.get("extensionData", {})),
            extensions     = copy(data.get("extensions", [])),
            extension_urls = KeyReprDict(data.get("extensionURLs", {})),
            meta           = FRMeta.from_data(data["meta"]) if "meta" in data else FRMeta.new_scratch_meta(),
            asset_files    = copy(asset_files),
        )
    
    def to_data(self) -> tuple[dict[str, Any], dict[str, bytes]]:
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
            "extensionURLs": dict(self.extension_urls),
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

    @enforce_argument_types
    @classmethod
    def from_file(cls, file_source: str | BytesIO) -> FRProject:
        """
        Reads project data from a project file(.sb3 or .pmp) and creates a FRProject from it.

        Args:
            file_source: file path to or bytes of the .sb3 or .pmp file
        """
        contents = read_all_files_of_zip(file_source)
        project_data = loads(contents["project.json"].decode())
        del contents["project.json"]

        if not(isinstance(file_source, str) and file_source.endswith(".pmp")):
            project_data = cls._data_sb3_to_pmp(project_data)
        return cls.from_data(project_data, asset_files=KeyReprDict(contents))

    @enforce_argument_types
    @classmethod
    def fetch_by_id(cls, project_id: str, platform: TargetPlatform = TargetPlatform.PENGUINMOD) -> FRProject:
        """
        Fetch a project from the PenguinMod or Scratch API by it's ID using a Node.js subprocess.

        Args:
            project_id: the ID of the project (e.g. "0131435715")
            platform: the platform the project is on (determines api url)
        
        Raises:
            GU_FailedFileWriteError(unlikely): if the temporary directory could not be created
            MANIP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
            MANIP_SubprocessTimeoutError: if the Node.js subprocess took too long
            MANIP_UnexpectedSubprocessError: if the project could not be fetched or some error occurs during the subprocess call
        """
        projects, error = cls.fetch_by_ids(project_ids=[project_id], platform=platform)
        if error is not None:
            raise error
        return projects[project_id]

    @enforce_argument_types
    @classmethod
    def fetch_by_ids(cls, project_ids: list[str], platform: TargetPlatform = TargetPlatform.PENGUINMOD
        ) -> tuple[dict[str, FRProject], MANIP_UnexpectedSubprocessError | None]:
        """
        Fetch multiple projects in parallel from the PenguinMod or Scratch API by their IDs using a Node.js subprocess.

        Args:
            project_ids: the IDs of the projects (e.g. ["0131435715", "9876543210"])
            platform: the platform the projects are on (determines api url)
        
        Returns:
            Dictionary mapping IDs to sucessfully fetched projects and an optional error if some projects failed to fetch.
            
        Raises:
            GU_FailedFileWriteError(unlikely): if the temporary directory could not be created
            MANIP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
            MANIP_SubprocessTimeoutError: if the Node.js subprocess took too long
            MANIP_UnexpectedSubprocessError: if some error occurs during the subprocess call
        """
        match platform:
            case TargetPlatform.SCRATCH:
                api_url = SCRATCH_API
            case TargetPlatform.PENGUINMOD:
                api_url = PENGUINMOD_API
        
        results, error = fetch_projects(
            project_ids=project_ids, api_url=api_url, 
            timeout_base=30, timeout_per_project=10,
        )
        projects = {project_id: cls.from_file(file_source=results[project_id]) if project_id in results else None for project_id in project_ids}
        return (projects, error)
    
    @enforce_argument_types
    def to_file(self, file_path: str) -> None:
        """
        Writes the project data to a project file(.sb3 or .pmp)

        Args:
            file_path: file path to the .sb3 or .pmp file
        
        Returns:
            the FRProject
        """
        project_data, asset_files = self.to_data()
        contents = asset_files
        contents["project.json"] = gdumps(project_data).encode()
        create_zip_file(file_path, contents)

    def __post_init__(self) -> None:
        """
        Ensure my assumption about extension_data was correct
        
        Returns:
            None
        """
        # TODO #if self.extension_data != {}: raise MANIP_ThanksError() # also uncomment test

    @enforce_argument_types
    def add_all_extensions_to_info_api(self, info_api: OpcodeInfoAPI) -> None:
        """
        For every extension of the project generate and import the required opcode info py file and add it to the OpcodeInfoAPI.
        If cached versions exist and they are up to date, they will be kept and not replaced.
        **[WARNING] Does not copy info_api, but modifies it**
        
        Raises:
            MANIP_UnknownBuiltinExtensionError: if one tries to add an unknown or not yet implemented builtin extension
            MANIP_ExtensionModuleNotFoundError: If the extension's python module does not exist
            MANIP_UnexpectedExtensionModuleImportError: If the extension's python module can not be loaded e.g. because it is malformed
            MANIP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
            MANIP_ExtensionFetchError: if the extension code could not be fetched for some reason
            MANIP_DirectExtensionInfoExtractionError: if the extension info could not be extracted through direct execution
            MANIP_SafeExtensionInfoExtractionError: if the extension info could not be extracted through safe analysis
            MANIP_ExtensionInfoConvertionError: if the extracted extension info could not be converted into the format of this project
            MANIP_ThanksError(unlikely): if a block argument uses the mysterious Scratch.ArgumentType.SEPERATOR
            GU_FailedFileWriteError(unlikely): if the generated extension info file or cache file or their directory could not be written/created
    
        Warnings:
            MANIP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed in the getInfo method of the extension code in safe analysis
            MANIP_UnexpectedNotPossibleFeatureWarning: if an impossible to implement feature is used (eg. ternary expr) in the getInfo method of the extension code in safe analysis
        """
        for extension_id in self.extensions:
            info_api.generate_and_add_extension(
                extension_id=extension_id,
                extension_source=self.extension_urls.get(extension_id, None),
            )
    
    @enforce_argument_types
    def to_second(self, info_api: OpcodeInfoAPI) -> SRProject:
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
                new_stage, global_variables, global_lists = old_stage.to_second(
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
            global_variables        = global_variables,
            global_lists            = global_lists,
            global_monitors         = global_monitors,
            extensions              = new_extensions,
            tempo                   = old_stage.tempo,
            video_transparency      = old_stage.video_transparency,
            video_state             = SRVideoState.from_code(old_stage.video_state),
            text_to_speech_language = new_tts_language,
        )


@grepr_dataclass(eq=True) # eq must be True for order to work, is overwritten
class SRProject:
    """
    The second representation (SR) of a Scratch/PenguinMod Project
    """
    
    stage: SRStage = field(call_subvalidate=True)
    sprites: list[SRSprite]
    sprite_layer_stack: list[UUID]
    global_variables: list[SRVariable]
    global_lists: list[SRList]
    global_monitors: list[SRMonitor]
    extensions: list[SRBuiltinExtension | SRCustomExtension]
    tempo: int
    video_transparency: int | float # There seems to be no limit
    video_state: SRVideoState
    text_to_speech_language: SRTTSLanguage | None

    @classmethod
    def create_empty(cls) -> SRProject:
        """
        Create an empty SRProject with no sprites, variables etc. and the default settings
        
        Returns:
            the empty SRProject
        """
        return cls(
            stage=SRStage.create_empty(),
            sprites=[],
            sprite_layer_stack=[],
            global_variables=[],
            global_lists=[],
            global_monitors=[],
            extensions=[],
            tempo=60,
            video_transparency=50,
            video_state=SRVideoState.ON,
            text_to_speech_language=None,
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
            self.stage                   != other.stage or
            self.sprites                 != other.sprites or
            self.global_variables        != other.global_variables or
            self.global_lists            != other.global_lists or
            self.global_monitors         != other.global_monitors or
            self.extensions              != other.extensions or
            self.tempo                   != other.tempo or
            self.video_transparency      != other.video_transparency or
            self.video_state             != other.video_state or
            self.text_to_speech_language != other.text_to_speech_language
        ):
            return False

        if len(self.sprite_layer_stack) != len(other.sprite_layer_stack):
            return False

        self_uuid_to_sprite  = {sprite.uuid: sprite for sprite in self .sprites}
        other_uuid_to_sprite = {sprite.uuid: sprite for sprite in other.sprites}

        for self_uuid, other_uuid in zip(self.sprite_layer_stack, other.sprite_layer_stack):
            if self_uuid_to_sprite.get(self_uuid) != other_uuid_to_sprite.get(other_uuid):
                return False

        return True

    @enforce_argument_types
    def post_validate(self, path: AbstractTreePath, info_api: OpcodeInfoAPI) -> None:
        """
        Ensure an instance is valid, raise GU_ValidationError if not
        
        Args:
            info_api: the opcode info api used to fetch information about opcodes
        
        Raises:
            GU_ValidationError: if the instance is invalid
            MANIP_SameValueTwiceError(GU_ValidationError): if two sprites or extensions have the same name
        """
        ValidateAttribute.VA_EXACT_LEN(self, path, "sprite_layer_stack", 
            len(self.sprites), condition=f"In this case the project has {len(self.sprites)} sprites(s)"
        )
        ValidateAttribute.VA_RANGE(self, path, "tempo", 20, 500)

        self._validate_sprites(path, info_api)
        
        for i, variable in enumerate(self.global_variables):
            variable.validate(path.add_attribute("global_variables").add_index_or_key(i))
        for i, list_ in enumerate(self.global_lists):
            list_.validate(path.add_attribute("global_lists").add_index_or_key(i))
        
        self._validate_var_names(path)
        self._validate_list_names(path)
        
        for i, monitor in enumerate(self.global_monitors):
            monitor.validate(path.add_attribute("global_monitors").add_index_or_key(i), info_api)
        
        for i, extension in enumerate(self.extensions):
            extension.validate(path.add_attribute("extensions").add_index_or_key(i))
        
        defined_extensions = {}
        for i, extension in enumerate(self.extensions):
            current_path = path.add_attribute("extensions").add_index_or_key(i)
            if extension.id in defined_extensions:
                other_path = defined_extensions[extension.id]
                raise MANIP_SameValueTwiceError(other_path, current_path, "Two extensions must not have the same id")
            defined_extensions[extension.id] = current_path
        
        # 1. Ensure no same sprite name
        # 2. Validate Dropdown Values
        defined_sprites      = {}
        local_variables = {None: []}
        local_lists     = {None: []}
        for i, sprite in enumerate(self.sprites):
            current_path = path.add_attribute("sprites").add_index_or_key(i)
            if sprite.name in defined_sprites:
                other_path = defined_sprites[sprite.name]
                raise MANIP_SameValueTwiceError(other_path, current_path, "Two sprites must not have the same name")
            defined_sprites[sprite.name] = current_path
            local_variables[sprite.name] = [
                (DropdownValueKind.VARIABLE, variable.name) for variable in sprite.local_variables]
            local_lists    [sprite.name] = [
                (DropdownValueKind.LIST    , list_   .name) for list_    in sprite.local_lists]
        
        global_variables = [(DropdownValueKind.VARIABLE, variable.name) for variable in self.global_variables]
        global_lists     = [(DropdownValueKind.LIST    , list_   .name) for list_    in self.global_lists    ]
        backdrops            = [(DropdownValueKind.BACKDROP, backdrop.name) for backdrop in self.stage.costumes      ]
        for i, target in enumerate([self.stage]+self.sprites):
            if i == 0:
                target_key = None
                current_path = path.add_attribute("stage")
            else:
                target_key = target.name
                current_path = path.add_attribute("sprites").add_index_or_key(i-1)
            partial_context = PartialContext(
                scope_variables  = global_variables + local_variables[target_key],
                scope_lists      = global_lists     + local_lists    [target_key],
                global_variables = global_variables,
                local_variables  = local_variables,
                local_lists      = local_lists,
                other_sprites    = [
                    (DropdownValueKind.SPRITE, sprite_name) for sprite_name in defined_sprites.keys()],
                backdrops        = backdrops,
            )
            target.validate_scripts(
                path     = current_path, 
                info_api = info_api, 
                context  = partial_context,
            )
            if i == 0: 
                global_context = partial_context
            else:
                target: SRSprite
                target.validate_monitor_dropdown_values(
                    path     = current_path, 
                    info_api = info_api, 
                    context  = partial_context,
                )
        
        for i, monitor in enumerate(self.global_monitors):
            monitor.validate_dropdown_values(
                path     = path.add_attribute("global_monitors").add_index_or_key(i), 
                info_api = info_api, 
                context  = global_context,
            )

    def _validate_sprites(self, path: AbstractTreePath, info_api: OpcodeInfoAPI) -> None:
        """
        Ensure the sprites of a SRProject are valid, raise GU_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            None
        
        Raises:
            MANIP_SameValueTwiceError(GU_ValidationError): if two sprites have the same UUID **OR** if the same UUID is included twice in sprite_layer_stack 
            MANIP_SpriteLayerStackError(GU_ValidationError): if the sprite_layer_stack contains a UUID which belongs to no sprite 
        """
        sprite_uuid_paths: dict[UUID, list] = {}
        for i, sprite in enumerate(self.sprites):
            current_path = path.add_index_or_key("sprites").add_index_or_key(i)
            sprite.validate(current_path, info_api)
            if sprite.uuid in sprite_uuid_paths:
                other_path = sprite_uuid_paths[sprite.uuid]
                raise MANIP_SameValueTwiceError(other_path, current_path, "Two sprites must npt have the same UUID")
            sprite_uuid_paths[sprite.uuid] = current_path
        

        stack_uuid_paths: dict[UUID, list] = {}
        for i, uuid in enumerate(self.sprite_layer_stack):
            current_path = path.add_attribute("sprite_layer_stack").add_index_or_key(i)
            if uuid in stack_uuid_paths:
                other_path = stack_uuid_paths[uuid]
                raise MANIP_SameValueTwiceError(other_path, current_path, "The same UUID must npt be included twice")
            if uuid not in sprite_uuid_paths:
                raise MANIP_SpriteLayerStackError(current_path, "Must be the UUID of an existing sprite")
            stack_uuid_paths[uuid] = current_path
        # same length and uniqueness is assured and every UUID must have a partner sprite
        # => no sprite can possibly be missing a partner UUID
        
    def _validate_var_names(self, path: AbstractTreePath) -> None:
        """
        Ensures no variables with the same name exist

        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_SameValueTwiceError(GU_ValidationError): if the project contains vars with the same name
        """
        defined_variables = {}
        for i, variable in enumerate(self.global_variables):
            current_path = path.add_attribute("global_variables").add_index_or_key(i)
            if variable.name in defined_variables:
                other_path = defined_variables[variable.name]
                raise MANIP_SameValueTwiceError(other_path, current_path, "Two variables must not have the same name")
            defined_variables[variable.name] = current_path
        
        for i, sprite in enumerate(self.sprites):
            for j, variable in enumerate(sprite.local_variables):
                current_path = path.add_attribute("sprites").add_index_or_key(i).add_attribute("local_variables").add_index_or_key(j)
                if variable.name in defined_variables:
                    other_path = defined_variables[variable.name]
                    raise MANIP_SameValueTwiceError(other_path, current_path, "Two variables must not have the same name")
                defined_variables[variable.name] = current_path
        
    def _validate_list_names(self, path: AbstractTreePath) -> None:
        """
        Ensures no lists with the same name exist

        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_SameValueTwiceError(GU_ValidationError): if the project contains lists with the same name
        """
        defined_lists = {}
        for i, list_ in enumerate(self.global_lists):
            current_path = path.add_attribute("global_lists").add_index_or_key(i)
            if list_.name in defined_lists:
                other_path = defined_lists[list_.name]
                raise MANIP_SameValueTwiceError(other_path, current_path, "Two lists must not have the same name")
            defined_lists[list_.name] = current_path
        
        for i, sprite in enumerate(self.sprites):
            for j, list_ in enumerate(sprite.local_lists):
                current_path = path.add_attribute("sprites").add_index_or_key(i).add_attribute("local_lists").add_index_or_key(j)
                if list_.name in defined_lists:
                    other_path = defined_lists[list_.name]
                    raise MANIP_SameValueTwiceError(other_path, current_path, "Two lists must not have the same name")
                defined_lists[list_.name] = current_path
    
    @enforce_argument_types
    def add_all_extensions_to_info_api(self, info_api: OpcodeInfoAPI) -> None:
        """
        For every extension of the project generate and import the required opcode info py file and add it to the OpcodeInfoAPI.
        If cached versions exist and they are up to date, they will be kept and not replaced.
        [WARNING] Does not copy info_api, but modifies it
        
        Raises:
            MANIP_UnknownBuiltinExtensionError: if one tries to add an unknown or not yet implemented builtin extension
            MANIP_ExtensionModuleNotFoundError: If the extension's python module does not exist
            MANIP_UnexpectedExtensionModuleImportError: If the extension's python module can not be loaded e.g. because it is malformed
            MANIP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
            MANIP_ExtensionFetchError: if the extension code could not be fetched for some reason
            MANIP_DirectExtensionInfoExtractionError: if the extension info could not be extracted through direct execution
            MANIP_SafeExtensionInfoExtractionError: if the extension info could not be extracted through safe analysis
            MANIP_ExtensionInfoConvertionError: if the extracted extension info could not be converted into the format of this project
            MANIP_ThanksError(unlikely): if a block argument uses the mysterious Scratch.ArgumentType.SEPERATOR
            GU_FailedFileWriteError(unlikely): if the generated extension info file or cache file or their directory could not be written/created
    
        Warnings:
            MANIP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed in the getInfo method of the extension code in safe analysis
            MANIP_UnexpectedNotPossibleFeatureWarning: if an impossible to implement feature is used (eg. ternary expr) in the getInfo method of the extension code in safe analysis
        """
        for extension in self.extensions:
            if   isinstance(extension, SRBuiltinExtension):
                info_api.generate_and_add_extension(
                    extension_id=extension.id,
                    extension_source=None,
                )
            elif isinstance(extension, SRCustomExtension):
                info_api.generate_and_add_extension(
                    extension_id=extension.id,
                    extension_source=extension.url,
                )
    
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
    
    @enforce_argument_types
    def to_first(self, info_api: OpcodeInfoAPI, target_platform: TargetPlatform = TargetPlatform.PENGUINMOD) -> FRProject:
        """
        Converts a SRProject into a FRProject
        
        Args:
            info_api: the opcode info api used to fetch information about opcodes
        
        Returns:
            the FRProject
        """

        old_targets  = []
        old_monitors = []
        asset_files  = {}
        tts_language = None if self.text_to_speech_language is None else self.text_to_speech_language.to_code()
        old_stage, old_global_monitors, stage_asset_files = self.stage.to_first(
            info_api                = info_api,
            global_vars             = self.global_variables,
            global_lists            = self.global_lists,
            global_monitors         = self.global_monitors,
            broadcast_messages      = self._find_broadcast_messages(),
            tempo                   = self.tempo,
            video_transparency      = self.video_transparency,
            video_state             = self.video_state.to_code(),
            text_to_speech_language = tts_language,
        )
        old_targets.append(old_stage)
        old_monitors.extend(old_global_monitors)
        asset_files.update(stage_asset_files)
        
        for new_sprite in self.sprites:
            old_sprite, old_local_monitors, sprite_asset_files = new_sprite.to_first(
                info_api     = info_api,
                global_vars  = self.global_variables,
                global_lists = self.global_lists,
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
            extension_urls = KeyReprDict(extension_urls),
            meta           = meta,
            asset_files    = KeyReprDict(asset_files),
        )


__all__ = ["FRProject", "SRProject"]

