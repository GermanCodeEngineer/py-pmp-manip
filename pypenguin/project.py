import typing
import json

from utility   import read_file_of_zip, ThanksError
from target    import FLStage, FLSprite
from monitor   import FLMonitor
from meta      import FLMeta

from utility import gprint

class FLProject: 
    """The first "level"(FL) of the project data tree. Its data is equivalent to the data stored in a .pmp file."""
    _grepr = True
    _grepr_fields = ["targets", "monitors", "extension_data", "extensions", "extension_urls", "meta"]

    targets: typing.List[FLStage | FLSprite]
    monitors: typing.List[FLMonitor]
    extension_data: typing.Dict[typing.Any, typing.Any] # I couldn't find out what it would be used for
    extensions: typing.List[str]
    extension_urls: typing.Dict[str, str] | None
    meta: FLMeta

    @classmethod
    def from_pmp_file(cls, file_path: str):
        self = cls()
        project_data = json.loads(read_file_of_zip(file_path, "project.json"))
        with open("extracted.json", "w") as file:
            json.dump(project_data, file)
        
        self.targets = [
            FLStage.from_data(target_data) if i==0 else FLSprite.from_data(target_data)
            for i, target_data in enumerate(project_data["targets"])
        ]
        self.monitors = [
            FLMonitor.from_data(monitor_data) 
            for monitor_data in project_data["monitors"]
        ]
        if project_data["extensionData"] != {}: raise ThanksError()
        self.extension_data = project_data["extensionData"]
        self.extensions     = project_data["extensions"   ]
        self.extension_urls = project_data.get("extensionURLs", None)
        self.meta           = FLMeta.from_data(project_data["meta"])
        return self
        
    def step(self):
        #TODO: Scratch to PenguinMod Conversion
        for target in self.targets:
            target.step()
        

#file_path = "../assets/from_online/my 1st platformer.pmp"
file_path = "../assets/from_online/dumb example.pmp"

project = FLProject.from_pmp_file(file_path)

gprint(project)
project.step()
