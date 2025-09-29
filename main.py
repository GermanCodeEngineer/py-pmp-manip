from pmp_manip import init_config, get_default_config, info_api, generate_opcode_doc


init_config(get_default_config())

# Just input everything you know and you will likely find it:
doc_string = generate_opcode_doc(info_api, new_opcode="&sensing::touching clone of")
