from pmp_manip import get_default_config, init_config, info_api, FRProject, SRProject, SRSprite, SRScript, SRBlock, SRBlockAndDropdownInputValue, SRDropdownValue
from pmp_manip.opcode_info.api import DropdownValueKind

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="assets/second_repr_example.pmp")
frproject.add_all_extensions_to_info_api(info_api)
print(frproject)
srproject = frproject.to_second(info_api)
print("The contents of the project are:")
print(srproject)




