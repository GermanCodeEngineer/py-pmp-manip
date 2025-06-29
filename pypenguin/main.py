import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pypenguin.core import *
from pypenguin.opcode_info.data import info_api
from pypenguin.utility import ValidationConfig

#file_path = "../assets/from_online/my 1st platformer.pmp"
#file_path = "../assets/input_modes.pmp"
#file_path = "../assets/monitors.pmp"
#file_path = "../assets/dumb example.pmp"
file_path = "../assets/testing_blocks.pmp"
#file_path = "../assets/scratch_project.sb3"
#file_path = "../assets/asset_formats.pmp"

project = FRProject.from_file(file_path, info_api=info_api)


project.asset_files = ...
print(project)

#new_project = project.to_second(info_api=info_api)
#print(new_project)
#new_project.validate(info_api=info_api, config=ValidationConfig())


