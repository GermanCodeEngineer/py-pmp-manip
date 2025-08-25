from pmp_manip import (
    get_default_config, init_config, info_api, FRProject, AbstractTreePath,
    SRScript, SRBlock,
)
from pmp_manip.core.tools import TreeVisitor, get_path_in_tree, path_exists_in_tree

cfg = get_default_config()
init_config(cfg)

# Load or Create a Project
frproject = FRProject.from_file("assets/from_online/my 1st platformer.pmp")
srproject = frproject.to_second(info_api)

#path = AbstractTreePath().add_attribute("sprites").add_index_or_key(7).add_attribute("scripts").add_index_or_key(0).add_attribute("blocks").add_index_or_key(3).add_attribute("inputs")
#.sprites[7].scripts[0].blocks[3].inputs
#print(get_path_in_tree(srproject, path))

def handle_key_pressed(key_pressed_path: AbstractTreePath, key_pressed_node: SRBlock):
    # example for this path: AbstractTreePath(.sprites[0].scripts[1].blocks[1].inputs['BODY'].blocks[0].inputs['CONDITION'].block)
    # 3 levels: this block < input value < all inputs < parent block(possible if block)
    parent_path = key_pressed_path.go_up(3)
    parent_node = get_path_in_tree(srproject, parent_path)
    # Condition 1: If Block is parent
    if not isinstance(parent_node, SRBlock): return
    if parent_node.opcode != "if <CONDITION> then {THEN}": return
    if_path = parent_path
    
    # example for this path: AbstractTreePath(.sprites[0].scripts[1].blocks[1].inputs['BODY'].blocks[0])
    # 4 levels: if block < all blocks in input < input value < all inputs < parent block(possible forever block)
    parent_path = if_path.go_up(4)
    parent_node = get_path_in_tree(srproject, parent_path, default=None) # default=None to prevent error
    # Condition 2: Forever Block is parent
    if not isinstance(parent_node, SRBlock): return
    if parent_node.opcode != "forever {BODY}": return
    forever_path = parent_path
    forever_node = parent_node
    
    # example for this path: AbstractTreePath(.sprites[0].scripts[1].blocks[1])
    # 2 levels: forever block < all blocks in script < script
    parent_path = forever_path.go_up(2)
    parent_node = get_path_in_tree(srproject, parent_path, default=None)
    # Condition 3: Forever Block is in script directly
    if not isinstance(parent_node, SRScript): return
    script_path = parent_path
    script_node = parent_node

    # Condition 4: Script has 2 blocks, green flag and forever block
    if len(script_node.blocks) != 2: return
    if not script_node.blocks[0].opcode == "when green flag clicked": return
    if script_node.blocks[1] is not forever_node: return

    print(script_node)
    print(script_path)

iterator_gen = TreeVisitor.new_include_only(included=[SRBlock])
path_to_node_map = iterator_gen.visit_tree(srproject)
for path, node in path_to_node_map.items():
    if isinstance(node, SRBlock):
        print(path, repr(node.opcode))
        if node.opcode == "key ([KEY]) pressed?":
            handle_key_pressed(path, node)
            break

    else: raise ValueError()

