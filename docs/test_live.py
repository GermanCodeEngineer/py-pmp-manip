from pmp_manip import (
    get_default_config, init_config, info_api, FRProject,
    SRBlock,
    TreeVisitor,
)

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file("assets/from_online/my 1st platformer.pmp")
srproject = frproject.to_second(info_api)

# Let us allow only blocks(SRBlock) this time:
visitor = TreeVisitor.new_include_only(included=[SRBlock])

path_to_node_map = visitor.visit_tree(srproject)
# Get only nodes and discard paths (just for this example)
all_nodes = list(path_to_node_map.values())

print(f"Found {len(path_to_node_map)} element(s)")
for i, item in enumerate(all_nodes[:10]):
    print(f"Sample node type: {type(item).__name__}")
# Print the last one as an example
print("Example Node:")
print(all_nodes[-1])
