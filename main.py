from pmp_manip import *
from pmp_manip.utility import write_file_text
from pmp_manip.opcode_info.doc_api import *


#create_mkdocs_project(site_name="abx")
init_config(get_default_config())

doc_string = generate_opcode_doc(info_api, "&control::if <CONDITION> then {THEN} else {ELSE}")
write_file_text("generated.md", doc_string)

