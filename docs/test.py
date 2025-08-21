from pmp_manip import get_default_config, init_config, SRProject, info_api

cfg = get_default_config()
init_config(cfg)

# Load or Create a Project
srproject = SRProject.create_empty()

# Assuming you have alredy modified the project to your wishes
# Convert the project into first representation to make it exportable.
frproject = srproject.to_first(info_api)

# Export the project
frproject.to_file("path/to/my_modified_project.pmp")
print("Project was saved to a file successfully :)")
