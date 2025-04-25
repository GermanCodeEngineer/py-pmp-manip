import json

from utility               import read_file_of_zip, ThanksError, PypenguinClass, PypenguinEnum
from utility               import AA_TYPE, AA_TYPES, AA_LIST_OF_TYPE, AA_RANGE, SameNameTwiceError
from target                import FRTarget, FRStage, FRSprite, SRStage, SRSprite
from monitor               import FRMonitor, SRMonitor
from meta                  import FRMeta
from config                import SpecialCaseHandler
from block_info            import OpcodeInfoApi
from vars_lists            import SRAllSpriteVariable, SRAllSpriteList
from extension             import SRExtension, SRCustomExtension, SRBuiltinExtension
from tts                   import TextToSpeechLanguage
from context               import PartialContext
from dropdown              import SRDropdownValue, SRDropdownKind

class FRProject(PypenguinClass): 
    """The first representation (FR) of the project data tree. Its data is equivalent to the data stored in a .pmp file."""
    _grepr = True
    _grepr_fields = ["targets", "monitors", "extension_data", "extensions", "extension_urls", "meta"]

    targets: list[FRTarget]
    monitors: list[FRMonitor]
    extension_data: dict # I couldn't find out what it would be used for, seems to be always {}
    extensions: list[str]
    extension_urls: dict[str, str]
    meta: FRMeta

    def __init__(self, 
        targets: list[FRTarget],
        monitors: list[FRMonitor],
        extension_data: dict,
        extensions: list[str],
        extension_urls: dict[str, str],
        meta: FRMeta,
    ):
        self.targets        = targets
        self.monitors       = monitors
        self.extension_data = extension_data
        if self.extension_data != {}: raise ThanksError()
        self.extensions     = extensions
        self.extension_urls = extension_urls
        self.meta           = meta

    @classmethod
    def from_data(cls, project_data: dict):
        with open("extracted.json", "w") as file:
            json.dump(project_data, file, indent=4)
        
        return cls(
            targets = [
                FRStage.from_data(target_data) if i==0 else FRSprite.from_data(target_data)
                for i, target_data in enumerate(project_data["targets"])
            ],
            monitors = [
                FRMonitor.from_data(monitor_data) 
                for monitor_data in project_data["monitors"]
            ],
            extension_data = project_data["extensionData"],
            extensions     = project_data["extensions"   ],
            extension_urls = project_data.get("extensionURLs", {}),
            meta           = FRMeta.from_data(project_data["meta"]),
        )

    @classmethod
    def from_pmp_file(cls, file_path: str) -> "FRProject":
        assert file_path.endswith(".pmp")
        project_data = json.loads(read_file_of_zip(file_path, "project.json"))
        return cls.from_data(project_data)
    
    @classmethod
    def from_sb3_file(cls, file_path: str):
        # TODO: 
        # - test this method + test sprite id 
        # - test custom block type of sb3's defaulting to "statement"
        assert file_path.endswith(".sb3")
        project_data = json.loads(read_file_of_zip(file_path, "project.json"))
        for i, sprite_data in enumerate(project_data["targets"]):
            sprite_data["customVars"] = []
            #if i == 0:
            #    token = stringToToken("_stage_")
            #else:
            #    token = stringToToken(sprite_data["name"])
            #sprite_data["id"        ] = token
    
            #for block_data in sprite_data["blocks"].values():
            #    if isinstance(block_data, list): continue # skip list blocks
            #    if block_data["opcode"] == "procedures_prototype":
            #        block_data["mutation"]["optype"] = json.dumps("statement") # Scratch custom blocks are always "instruction" blocks
        
        project_data["extensionData"] = {}
    
        #project_data["meta"] = {
        #    "semver": "3.0.0",
        #    "vm"    : "0.2.0",
        #    "agent" : "",
        #    "platform": {
        #        "name"   : "PenguinMod",
        #        "url"    : "https://penguinmod.com/",
        #        "version": "stable",
        #    },
        #}
        return cls.from_data(project_data)

    def step(self, config: SpecialCaseHandler, info_api: OpcodeInfoApi):
        new_sprites: list[SRSprite] = []
        for target in self.targets:
            if  target.is_stage:
                old_stage: FRStage = target
                (
                    new_stage, all_sprite_variables, all_sprite_lists,
                ) = target.step(config=config, info_api=info_api)
                new_stage: SRStage
            else:
                new_sprite, _, _ = target.step(config=config, info_api=info_api)
                new_sprite: SRSprite
                new_sprites.append(new_sprite)
        
        global_monitors = []
        sprite_names = [sprite.name for sprite in new_sprites]
        for monitor in self.monitors:
            monitor_sprite_name, new_monitor = monitor.step(info_api=info_api, sprite_names=sprite_names)
            if new_monitor is not None:
                if monitor_sprite_name is None:
                    global_monitors.append(new_monitor)
                else:
                    sprite_index = sprite_names.index(monitor_sprite_name)
                    new_sprites[sprite_index].local_monitors.append(new_monitor)
       
        if old_stage.text_to_speech_language is None:
            new_tts_language = None
        else:
            new_tts_language = TextToSpeechLanguage.from_string(old_stage.text_to_speech_language)
        
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
            all_sprite_variables    = all_sprite_variables,
            all_sprite_lists        = all_sprite_lists,
            tempo                   = old_stage.tempo,
            video_transparency      = old_stage.video_transparency,
            video_state             = SRVideoState.from_string(old_stage.video_state),
            text_to_speech_language = new_tts_language,
            global_monitors         = global_monitors,
            extensions              = new_extensions,
        )


class SRVideoState(PypenguinEnum):
    @staticmethod
    def from_string(value: str) -> "SRVideoState":
        if   value == "on"        : return SRVideoState.ON
        elif value == "on flipped": return SRVideoState.ON_FLIPPED
        elif value == "off"       : return SRVideoState.OFF
        else: raise ValueError(f"Invalid video state: {value}")

    ON         = 0
    ON_FLIPPED = 1
    OFF        = 2

class SRProject(PypenguinClass):
    _grepr = True
    _grepr_fields = ["stage", "sprites", "all_sprite_variables", "all_sprite_lists", "tempo", "video_transparency", "video_state", "text_to_speech_language", "global_monitors", "extensions"]
    
    stage: SRStage
    sprites: list[SRSprite]
    all_sprite_variables: list[SRAllSpriteVariable]
    all_sprite_lists: list[SRAllSpriteList]
    tempo: int
    video_transparency: int | float
    video_state: SRVideoState
    text_to_speech_language: TextToSpeechLanguage | None
    global_monitors: list[SRMonitor]
    extensions: list[SRExtension]

    def __init__(self,
        stage: SRStage,
        sprites: list[SRSprite],
        all_sprite_variables: list[SRAllSpriteVariable],
        all_sprite_lists: list[SRAllSpriteList],
        tempo: int,
        video_transparency: int | float,
        video_state: SRVideoState,
        text_to_speech_language: TextToSpeechLanguage | None,
        global_monitors: list[SRMonitor],
        extensions: list[SRExtension],
    ):
        """
        Initialize the SR (Second Representation) of a Scratch/PenguinMod Project.
        """
        self.stage                   = stage
        self.sprites                 = sprites
        self.all_sprite_variables    = all_sprite_variables
        self.all_sprite_lists        = all_sprite_lists
        self.tempo                   = tempo
        self.video_transparency      = video_transparency
        self.video_state             = video_state
        self.text_to_speech_language = text_to_speech_language
        self.global_monitors         = global_monitors
        self.extensions              = extensions

    def validate_var_names(self, path: list) -> None:
        """
        Ensures no variables with the same name exist.
        """
        defined_variables = {}
        for i, variable in enumerate(self.all_sprite_variables):
            current_path = path+["all_sprite_variables", i]
            if variable.name in defined_variables:
                other_path = defined_variables[variable.name]
                raise SameNameTwiceError(other_path, current_path, "Two variables mustn't have the same name")
            defined_variables[variable.name] = current_path
        
        for i, sprite in enumerate(self.sprites):
            for j, variable in enumerate(sprite.sprite_only_variables):
                current_path = path+["sprites", i, "sprite_only_variables", j]
                if variable.name in defined_variables:
                    other_path = defined_variables[variable.name]
                    raise SameNameTwiceError(other_path, current_path, "Two variables mustn't have the same name")
                defined_variables[variable.name] = current_path
        
    def validate_list_names(self, path: list) -> None:
        """
        Ensures no lists with the same name exist.
        """
        defined_lists = {}
        for i, list_ in enumerate(self.all_sprite_lists):
            current_path = path+["all_sprite_lists", i]
            if list_.name in defined_lists:
                other_path = defined_lists[list_.name]
                raise SameNameTwiceError(other_path, current_path, "Two lists mustn't have the same name")
            defined_lists[list_.name] = current_path
        
        for i, sprite in enumerate(self.sprites):
            for j, list_ in enumerate(sprite.sprite_only_lists):
                current_path = path+["sprites", i, "sprite_only_lists", j]
                if list_.name in defined_lists:
                    other_path = defined_lists[list_.name]
                    raise SameNameTwiceError(other_path, current_path, "Two lists mustn't have the same name")
                defined_lists[list_.name] = current_path

    def validate(self, info_api: OpcodeInfoApi) -> None:
        """
        Checks wether a SRProject is valid and raises a subclass of ValidationError if not.
        """
        path = []
        AA_TYPE(self, path, "stage", SRStage)
        AA_LIST_OF_TYPE(self, path, "sprites", SRSprite)
        AA_LIST_OF_TYPE(self, path, "all_sprite_variables", SRAllSpriteVariable)
        AA_LIST_OF_TYPE(self, path, "all_sprite_lists", SRAllSpriteList)
        AA_TYPE(self, path, "tempo", int)
        AA_RANGE(self, path, "tempo", min=20, max=500)
        AA_TYPES(self, path, "video_transparency", (int, float)) # TODO: research min/max
        AA_TYPE(self, path, "video_state", SRVideoState)
        AA_TYPES(self, path, "text_to_speech_language", (TextToSpeechLanguage, type(None)))
        AA_LIST_OF_TYPE(self, path, "global_monitors", SRMonitor)
        AA_LIST_OF_TYPE(self, path, "extensions", SRExtension)
        
        # TODO: complete this
        self.stage.validate(path+["stage"], info_api)
        for i, sprite in enumerate(self.sprites):
            sprite.validate(path+["sprites", i], info_api)
        
        for i, variable in enumerate(self.all_sprite_variables):
            variable.validate(path+["all_sprite_variables", i])
        for i, list_ in enumerate(self.all_sprite_lists):
            list_.validate(path+["all_sprite_lists", i])
        
        self.validate_var_names(path)
        self.validate_list_names(path)
        
        for i, monitor in enumerate(self.global_monitors):
            monitor.validate(path+["global_monitors", i], info_api)
        
        for i, extension in enumerate(self.extensions):
            extension.validate(path+["extensions", i])
        
        # 1. Ensure no same sprite name
        # 2. Validate Dropdown Values
        defined_sprites      = {}
        sprite_only_variables = {None: []}
        sprite_only_lists     = {None: []}
        for i, sprite in enumerate(self.sprites):
            current_path = path+["sprites", i]
            if sprite.name in defined_sprites:
                other_path = defined_sprites[sprite.name]
                raise SameNameTwiceError(other_path, current_path, "Two sprites mustn't have the same name")
            defined_sprites[sprite.name] = current_path
            sprite_only_variables[sprite.name] = [
                SRDropdownValue(SRDropdownKind.VARIABLE, variable.name) for variable in sprite.sprite_only_variables]
            sprite_only_lists    [sprite.name] = [
                SRDropdownValue(SRDropdownKind.LIST    , list_   .name) for list_    in sprite.sprite_only_lists]
        
        all_sprite_variables = [SRDropdownValue(SRDropdownKind.VARIABLE, variable.name) for variable in self.all_sprite_variables]
        all_sprite_lists     = [SRDropdownValue(SRDropdownKind.LIST    , list_   .name) for list_    in self.all_sprite_lists    ]
        backdrops            = [SRDropdownValue(SRDropdownKind.BACKDROP, backdrop.name) for backdrop in self.stage.costumes      ]
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
                    SRDropdownValue(SRDropdownKind.SPRITE, sprite_name) for sprite_name in defined_sprites.keys()],
                backdrops             = backdrops,
            )
            target.validate_scripts(
                path     = current_path, 
                info_api = info_api, 
                context  = partial_context,
            )
            if i == 0: global_context = partial_context
        
        for i, monitor in enumerate(self.global_monitors):
            monitor.validate_dropdowns_values(
                path     = path+["global_monitors", i], 
                info_api = info_api, 
                context  = global_context,
            )
        # TODO: ensure no double used names anywhere


#file_path = "../assets/from_online/my 1st platformer.pmp"
file_path = "../assets/from_online/dumb example.pmp"
#file_path = "../assets/from_online/color.pmp"
#file_path = "../assets/input_modes.pmp"
#file_path = "../assets/monitors.pmp"

project = FRProject.from_pmp_file(file_path)

from config import config
from block_info import info_api

new_project = project.step(config=config, info_api=info_api)
print(new_project)

new_project.validate(info_api=info_api)

