from pmp_manip import *
#from pmp_manip.opcode_info.doc_api import *


#create_mkdocs_project(site_name="abx")
init_config(get_default_config())
f = FRProject.from_file("assets/e.pmp")
print(f)

#info_api.generate_and_add_extension("pen", None)

s = f.to_second(info_api)
print(s)
s.validate(info_api)
