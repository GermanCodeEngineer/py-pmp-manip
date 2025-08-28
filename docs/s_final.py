from pmp_manip import (
    get_default_config, init_config, info_api, FRProject,
    SRScript, SRBlock,
    ScriptPattern, BlockPattern, InputPattern, PatternConst, match_handler,
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

pattern = ScriptPattern(
    blocks=[
        BlockPattern(opcode=PatternConst("when green flag clicked")),
        BlockPattern(
            opcode=PatternConst("forever {BODY}"),
            inputs={
                "BODY": InputPattern(
                    blocks=[
                        BlockPattern(
                            opcode=PatternConst("if <CONDITION> then {THEN}"),
                            inputs={
                                "CONDITION": lambda x: True
                            },
                            access_point_id="if_block"
                        ),
                    ],
                ),
            },
            access_point_id="forever_block",
        ),
    ],
    access_point_id="root",
)
print(pattern)


visitor = TreeVisitor.new_include_only(included=[SRScript])
path_to_node_map = visitor.visit_tree(srproject)
for path, node in path_to_node_map.items():
    match_result = match_handler(handler=pattern, value=node)
    if match_result is not None:
        print(100*"=")
        print(path)
        print(node)
        print(match_result)
        break
        
