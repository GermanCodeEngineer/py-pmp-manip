from core.project import FRProject

#file_path = "../assets/from_online/my 1st platformer.pmp"
#file_path = "../assets/from_online/color.pmp"
#file_path = "../assets/input_modes.pmp"
#file_path = "../assets/monitors.pmp"
file_path = "../assets/from_online/dumb example.pmp"

project = FRProject.from_pmp_file(file_path)

from opcode_info.groups import info_api
from opcode_info import InputMode
from core.block import SRScript, SRBlock, SRInputValue

new_project = project.step(info_api=info_api)
s1 = SRScript(position=(0,0), blocks=[
    SRBlock(
        opcode="define custom block ",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=None,
    ),
])
new_project.sprites[0].scripts.append(s1)

print(new_project)
new_project.validate(info_api=info_api)
