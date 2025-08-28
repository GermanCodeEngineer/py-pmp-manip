from pmp_manip import (
    get_default_config, init_config, info_api, FRProject, SRScript,
    ScriptPattern, BlockPattern, InputPattern, PatternConst,
    TreeVisitor, AbstractTreePath, match_handler,
)

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file("assets/from_online/my 1st platformer.pmp")
srproject = frproject.to_second(info_api)

# Use our pattern from above
pattern = ScriptPattern(
    blocks=[
        BlockPattern(opcode=PatternConst(value="when green flag clicked")),
        BlockPattern(
            opcode=PatternConst(value="forever {BODY}"),
            inputs={
                "BODY": InputPattern(
                    blocks=[
                        BlockPattern(
                            opcode=PatternConst(value="if <CONDITION> then {THEN}"),
                        ),
                    ],
                ),
            },
        ),
    ],
)

visitor = TreeVisitor.new_include_only(included=[SRScript])
# Run the TreeVisitor only on the first sprite(=> no scripts from stage or other sprite will even be considered)
player_sprite = srproject.sprites[0]
path_to_node_map = visitor.visit_tree(player_sprite)
# Find all matches
matches: list[tuple[AbstractTreePath, SRScript]] = []
for path, node in path_to_node_map.items():
    match_result = match_handler(handler=pattern, value=node)
    if match_result is not None:
        matches.append((path, node))

# Print first match fully
first_match_path, first_match_node = matches[0]
print("A match found at", first_match_path)
print("Matching Script:")
print(first_match_node)

# Only print block inside "CONDITION" input of other matches for brevity
for match_path, match_node in matches[1:]:
    forever_block = match_node.blocks[1]
    # "BODY" must be a SRScriptInputValue => must have .blocks
    if_block = forever_block.inputs["BODY"].blocks[0]
    # "CONDITION" must be SRBlockAndBoolInputValue => must have .block, but could be none since not checked by pattern
    condition_block = if_block.inputs["CONDITION"].block

    print() # Seperator
    print("A match found at", match_path)
    print("Condition block:")
    print(condition_block)
