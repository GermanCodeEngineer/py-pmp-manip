from pmp_manip import FRProject
from pmp_manip.opcode_info.api import BuiltinExtensionRef
from pmp_manip.opcode_info.data import info_api
from pmp_manip.config import get_default_config, init_config

cfg = get_default_config()
init_config(cfg)

# Load the project
frproject = FRProject.from_file(file_path="assets/music_example.pmp")
# Then add all extensions required for that project automatically
frproject.add_all_extensions_to_info_api(info_api)
# Then use it how you want...
srproject = frproject.to_second(info_api)
print("Project was converted successfully :)")
