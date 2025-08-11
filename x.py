from pmp_manip import FRProject
from pmp_manip.opcode_info.data import info_api
from pmp_manip.config import get_default_config, init_config

# Init the required configuration
cfg = get_default_config()
init_config(cfg)

# Import and add the music extension
info_api.add_builtin_extension("music")

frproject = FRProject.from_file(file_path = "assets/from_online/ONLINE 2D MAINCRAFT.pmp")
srproject = frproject.to_second(info_api)

