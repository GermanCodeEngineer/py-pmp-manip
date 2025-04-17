import json

from utility               import read_file_of_zip, ThanksError
from target                import FRStage, FRSprite
from monitor               import FRMonitor
from meta                  import FRMeta
from config                import SpecialCaseHandler
from block_info            import BlockInfoApi
#from block_opcodes         import *

from utility import gprint, PypenguinClass

class FRProject(PypenguinClass): 
    """The first representation (FR) of the project data tree. Its data is equivalent to the data stored in a .pmp file."""
    _grepr = True
    _grepr_fields = ["targets", "monitors", "extension_data", "extensions", "extension_urls", "meta"]

    targets: list[FRStage | FRSprite]
    monitors: list[FRMonitor]
    extension_data: dict # I couldn't find out what it would be used for, seems to be always {}
    extensions: list[str]
    extension_urls: dict[str, str] | None
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
        self.extension_urls = project_data.get("extensionURLs", None)
        self.meta           = FRMeta.from_data(project_data["meta"])
        return self
        
    def step(self, config: SpecialCaseHandler, info_api: BlockInfoApi):
        #TODO: Scratch to PenguinMod Conversion
        for target in self.targets:
            target.step(config=config, info_api=info_api)
        
#file_path = "../assets/from_online/my 1st platformer.pmp"
file_path = "../assets/from_online/dumb example.pmp"
#file_path = "../assets/from_online/color.pmp"

project = FRProject.from_pmp_file(file_path)
gprint(project)
from config import config
from block_info import info_api
#gprint(config)
project.step(config=config, info_api=info_api)

