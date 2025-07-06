import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pypenguin.core import *
from pypenguin.opcode_info.data import info_api
from pypenguin.utility import ValidationConfig

file_path = "../assets/from_online/my 1st platformer.pmp"
#file_path = "../assets/input_modes.pmp"
#file_path = "../assets/monitors.pmp"
#file_path = "../assets/dumb example.pmp"
#file_path = "../assets/testing_blocks.pmp"
#file_path = "../assets/scratch_project.sb3"
#file_path = "../assets/asset_formats.pmp"
#file_path = "../assets/many_dropdowns.pmp"

project = FRProject.from_file(file_path, info_api=info_api)
print(project)

new_project = project.to_second(info_api)
del project
new_project.validate(config=ValidationConfig(), info_api=info_api)

old_project = new_project.to_first(info_api, target_platform=TargetPlatform.PENGUINMOD)

#old_project.extensions.append("truefantombase")
#old_project.extension_urls["truefantombase"] = "https://extensions.turbowarp.org/true-fantom/base.js"
old_project.to_file("../assets/from_online/changed_plaformer.sb3")




