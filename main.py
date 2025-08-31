from pmp_manip import init_config, get_default_config, FRProject, info_api
from pmp_manip.utility import write_file_text
init_config(get_default_config())


a = FRProject.from_file("assets/from_online/ONLINE 2D MAINCRAFT.pmp")
b = a.to_second(info_api)
write_file_text("project.lua", str(a))

