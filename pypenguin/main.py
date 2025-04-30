from core.project import FRProject
from opcode_info.groups import info_api

#file_path = "../assets/from_online/my 1st platformer.pmp"
#file_path = "../assets/from_online/color.pmp"
#file_path = "../assets/input_modes.pmp"
#file_path = "../assets/monitors.pmp"
file_path = "../assets/from_online/dumb example.pmp"

project = FRProject.from_pmp_file(file_path, info_api=info_api)

from opcode_info import InputMode
from core.block import SRScript, SRBlock, SRInputValue, InputMode
from core.block_mutation import SRCustomBlockMutation, SRCustomBlockArgumentMutation
from core.custom_block import SRCustomBlockOptype, SRCustomBlockOpcode, SRCustomBlockArgument, SRCustomBlockArgumentType
from core.dropdown import SRDropdownValue, SRDropdownKind

new_project = project.step(info_api=info_api)
s1 = SRScript(position=(0,0), blocks=[
    SRBlock(
        opcode="define custom block reporter",
        inputs={},
        dropdowns={},
        comment=None,
        mutation=SRCustomBlockMutation(
            custom_opcode=SRCustomBlockOpcode(segments=(
                "hi", SRCustomBlockArgument(type=SRCustomBlockArgumentType.BOOLEAN, name="u"),
            )),
            no_screen_refresh=True,
            optype=SRCustomBlockOptype.BOOLEAN_REPORTER,
            color1="#000000",
            color2="#000000",
            color3="#000000",
        ),
    ),
])
new_project.sprites[0].scripts.append(s1)

print(new_project)
new_project.validate(info_api=info_api)
