import json
from enum import Enum

from utility               import read_file_of_zip, ThanksError, PypenguinClass
from target                import FRTarget, FRStage, FRSprite, SRTarget, SRStage, SRSprite
from monitor               import FRMonitor, SRMonitor
from meta                  import FRMeta
from config                import SpecialCaseHandler
from block_info            import BlockInfoApi, DropdownType
from vars_lists            import SRAllSpriteVariable, SRAllSpriteList
from extension             import SRExtension, SRCustomExtension, SRBuiltinExtension

from utility import gprint

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

    @classmethod
    def from_pmp_file(cls, file_path: str) -> "FRProject":
        self = cls()
        project_data = json.loads(read_file_of_zip(file_path, "project.json"))
        with open("extracted.json", "w") as file:
            json.dump(project_data, file, indent=4)
        
        self.targets = [
            FRStage.from_data(target_data) if i==0 else FRSprite.from_data(target_data)
            for i, target_data in enumerate(project_data["targets"])
        ]
        self.monitors = [
            FRMonitor.from_data(monitor_data) 
            for monitor_data in project_data["monitors"]
        ]
        if project_data["extensionData"] != {}: raise ThanksError()
        self.extension_data = project_data["extensionData"]
        self.extensions     = project_data["extensions"   ]
        self.extension_urls = project_data.get("extensionURLs", {})
        self.meta           = FRMeta.from_data(project_data["meta"])
        return self
        
    def step(self, config: SpecialCaseHandler, info_api: BlockInfoApi):
        #TODO: Scratch to PenguinMod Conversion
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
            new_tts_language = DropdownType.TEXT_TO_SPEECH_LANGUAGE.translate_old_to_new_value(
                old_value = old_stage.text_to_speech_language,
            ).value # eg. "en" -> "English (en)"
        
        new_extensions = []
        for extension_id in self.extensions:
            if extension_id in self.extension_urls:
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

["on", "on flipped", "off"]
class SRVideoState(Enum):
    ON         = 0
    ON_FLIPPED = 1
    OFF        = 2

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
    
    @staticmethod
    def from_string(value: str) -> "SRVideoState":
        if   value == "on"        : return SRVideoState.ON
        elif value == "on flipped": return SRVideoState.ON_FLIPPED
        elif value == "off"       : return SRVideoState.OFF
        else: raise ValueError(f"Invalid video state: {value}")

class SRProject(PypenguinClass):
    _grepr = True
    _grepr_fields = ["stage", "sprites", "all_sprite_variables", "all_sprite_lists", "tempo", "video_transparency", "video_state", "text_to_speech_language", "global_monitors", "extension_data", "extensions", "extension_urls"]
    
    stage: SRStage
    sprites: list[SRSprite]
    all_sprite_variables: list[SRAllSpriteVariable]
    all_sprite_lists    : list[SRAllSpriteList]
    tempo: int
    video_transparency: int | float
    video_state: SRVideoState
    text_to_speech_language: str | None
    global_monitors: list[SRMonitor]
    extensions: list[SRExtension]

    def __init__(self,
        stage: SRStage,
        sprites: list[SRSprite],
        all_sprite_variables: list[SRAllSpriteVariable],
        all_sprite_lists    : list[SRAllSpriteList],
        tempo: int,
        video_transparency: int | float,
        video_state: SRVideoState,
        text_to_speech_language: str | None,
        global_monitors: list[SRMonitor],
        extensions: list[SRExtension],
    ):
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

file_path = "../assets/from_online/my 1st platformer.pmp"
#file_path = "../assets/from_online/dumb example.pmp"
#file_path = "../assets/from_online/color.pmp"
#file_path = "../assets/input_modes.pmp"
#file_path = "../assets/monitors.pmp"

project = FRProject.from_pmp_file(file_path)
gprint(project)
from config import config
from block_info import info_api
#gprint(config)
new_project = project.step(config=config, info_api=info_api)
gprint(new_project)
