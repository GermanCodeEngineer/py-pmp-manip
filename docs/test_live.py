from pmp_manip import (
    get_default_config, init_config, info_api, FRProject,
)
from pmp_manip.core.tools import TreeVisitor, get_path_in_tree, path_exists_in_tree

cfg = get_default_config()
init_config(cfg)

# Load or Create a Project
frproject = FRProject.from_file("assets/from_online/my 1st platformer.pmp")
# Convert it into the good format
srproject = frproject.to_second(info_api)

# Create our TreeVisitor with configuration. Let us allow everything for now:
visitor = TreeVisitor.new_include_all_except(excluded=[]) # 

# Run the TreeVisitor
path_to_node_map = visitor.visit_tree(srproject)
print(path_to_node_map)


