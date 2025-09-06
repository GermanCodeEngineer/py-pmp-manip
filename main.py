from pmp_manip import (
    get_default_config, init_config, FRProject, SRBlockAndTextInputValue,
    info_api,
)
from pmp_manip.opcode_info.api import ExtensionRef
from pmp_manip.utility import write_file_text

cfg = get_default_config()
init_config(cfg)

info_api.generate_and_add_extension("lmsTempVars2", extension_source=None)
#print(info_api)

"""
frproject = FRProject.from_file(file_path="assets/pen_polygon_example.pmp")
write_file_text("fr.lua", repr(frproject))
srproject = frproject.to_second(info_api)
write_file_text("sr.lua", repr(srproject))

srproject.sprites[0].scripts[0].blocks[0].inputs["SHAPE"].block.inputs["Y3"] = SRBlockAndTextInputValue(block=None, immediate="93.39")
srproject.validate(info_api)

new_frproject = srproject.to_first(info_api)
write_file_text("nfr.lua", repr(new_frproject))
#print("Project was converted successfully :)")
"""