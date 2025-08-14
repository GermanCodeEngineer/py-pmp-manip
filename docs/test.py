from pmp_manip import get_default_config, init_config, FRProject, info_api

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="assets/small_example.pmp")
print("Project was loaded from a file successfully :)")

# Use to_second to covert from First to Second Representation
srproject = frproject.to_second(info_api)
print("Project was converted into Second Representation successfully :)")
print("The contents of the project are:")
print(srproject)

