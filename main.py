from pmp_manip import (
    get_default_config, init_config, FRProject,
    info_api,
)
from pmp_manip.opcode_info.api import ExtensionRef
from pmp_manip.utility import write_file_text

cfg = get_default_config()
init_config(cfg)

#info_api.generate_and_add_extension(extension_id="music", extension_source=None) 
info_api._add_extension_by_ref(ExtensionRef(
    id="scratch_pen",
    module_dir="pmp_manip/opcode_info/data/",
))
print(info_api)

frproject = FRProject.from_file(file_path="assets/pen_polygon_example.pmp")
write_file_text("fr.lua", repr(frproject))
srproject = frproject.to_second(info_api)
#print("Project was converted successfully :)")
