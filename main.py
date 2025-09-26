from pmp_manip import *
#from pmp_manip.opcode_info.doc_api import *


#create_mkdocs_project(site_name="abx")
init_config(get_default_config())

f = FRProject.from_file("assets/expandable_blocks.pmp")
#print(f)
s = f.to_second(info_api)
print(s)

