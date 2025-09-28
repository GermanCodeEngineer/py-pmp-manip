from pmp_manip import *
from pmp_manip.utility import write_file_text
from pmp_manip.opcode_info.doc_api import *


#create_mkdocs_project(site_name="abx")
init_config(get_default_config())

info_api.generate_and_add_extension("pen")

#doc_string = generate_opcode_doc(info_api, "&pen::change pen ([COLOR_PARAM]) by (VALUE)")
#doc_string = generate_opcode_doc(info_api, "&pen::set print font to [FONT]")
#doc_string = generate_opcode_doc(info_api, "&sensing::mouse x")

#doc_string = generate_opcode_doc(info_api, "&control::if <CONDITION> then {THEN} else {ELSE}")

#doc_string = generate_opcode_doc(info_api, "&customblocks::call custom block")
#doc_string = generate_opcode_doc(info_api, "&special::{{POLYGON MENU}}")
#doc_string = generate_opcode_doc(info_api, "&control::{{EXPANDABLE IF-THEN-ELSE CHAIN}}")
doc_string = generate_opcode_doc(info_api, "&motion::glide to (X) (Y)")
write_file_text("generated.md", doc_string)

