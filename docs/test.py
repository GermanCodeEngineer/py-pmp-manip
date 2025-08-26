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

visitor = TreeVisitor.new_include_only(included=[SRBlock])
path_to_node_map = visitor.visit_tree(srproject)
for path, node in path_to_node_map.items():
    

from pmp_manip.core.patterns import *
pattern = ScriptPattern(
    blocks=[
        BlockPattern(opcode=Const("when green flag clicked")),
        BlockPattern(
            opcode=Const("forever {BODY}"),
            inputs={
                "BODY": InputPattern(
                    blocks=[
                        BlockPattern(
                            opcode=Const("if <CONDITION> then {THEN}"),
                            inputs={
                                "CONDITION": InputPattern(
                                    block=BlockPattern(opcode=Const("key ([KEY]) pressed?")),
                                ),
                            },
                        ),
                    ],
                ),
            },
        ),
    ],
)
value = srproject.sprites[0].scripts[1]
print(pattern)
print(value)
matches = match_handler(pattern, value)
print(matches)
