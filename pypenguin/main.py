from core import *
from opcode_info.groups import info_api
from opcode_info import InputMode
from utility import ValidationConfig

#file_path = "../assets/from_online/my 1st platformer.pmp"
#file_path = "../assets/from_online/color.pmp"
#file_path = "../assets/input_modes.pmp"
#file_path = "../assets/monitors.pmp"
file_path = "../assets/from_online/dumb example.pmp"

project = FRProject.from_pmp_file(file_path, info_api=info_api)

new_project = project.step(info_api=info_api)

print(new_project)
new_project.validate(info_api=info_api, config=ValidationConfig())

