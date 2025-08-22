from pmp_manip import get_default_config, init_config, FRProject, info_api

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="assets/second_repr_example.pmp")
frproject.add_all_extensions_to_info_api(info_api)

srproject = frproject.to_second(info_api)
print("The contents of the project are:")
print(srproject)
