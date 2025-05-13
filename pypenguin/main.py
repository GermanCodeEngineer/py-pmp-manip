import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pypenguin.core import *
from pypenguin.opcode_info.groups import info_api
from pypenguin.opcode_info import InputMode
from pypenguin.utility import ValidationConfig

#file_path = "../assets/from_online/my 1st platformer.pmp"
#file_path = "../assets/input_modes.pmp"
file_path = "../assets/monitors.pmp"
#file_path = "../assets/dumb example.pmp"
#file_path = "../assets/testing_blocks.pmp"
#file_path = "../assets/scratch_project.sb3"

project = FRProject.from_pmp_file(file_path, info_api=info_api)
from json import loads

#with open("extracted.json", "r") as file:
#    from pprint import pprint
#    pprint(loads(file.read()))
#print(project)


new_project = project.step(info_api=info_api)
print(new_project)
new_project.validate(info_api=info_api, config=ValidationConfig())
