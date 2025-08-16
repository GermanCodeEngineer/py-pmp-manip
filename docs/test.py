from pmp_manip import get_default_config, init_config, FRProject, info_api

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="assets/small_example.pmp")

srproject = frproject.to_second(info_api)
print("The contents of the project are:")
print(srproject)
