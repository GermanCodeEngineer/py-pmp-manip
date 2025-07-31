from pmp_manip.core import *
from pmp_manip.opcode_info.data import info_api
from pmp_manip.opcode_info.data.scratch_music import scratch_music
#from pmp_manip.opcode_info.data.gen_dumbExample import dumbExample
from pmp_manip.config import *


file_path = "assets/from_online/ONLINE 2D MAINCRAFT.pmp"
#file_path = "assets/cb_args.pmp"

cfg = get_default_config()
init_config(cfg)

info_api.add_group(scratch_music)

project = FRProject.from_file(file_path)
#print(project)
with open("log_first.lua", "w") as file:
    file.write(FRProject.__repr__(project))

new_project = project.to_second(info_api)
del project
new_project.validate(info_api=info_api)
print(new_project)

old_project = new_project.to_first(info_api, target_platform=TargetPlatform.PENGUINMOD)

#old_project.extensions.append("truefantombase")
#old_project.extension_urls["truefantombase"] = "https://extensions.turbowarp.org/true-fantom/base.js"
#old_project.to_file("assets/from_online/changed_plaformer.sb3")




