from pmp_manip import (
    get_default_config, init_config, info_api, FRProject, SRScript,
    ScriptPattern, BlockPattern, InputPattern, PatternConst,
    TreeVisitor, AbstractTreePath, SuccessfulMatchResult, match_handler,
)

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file("assets/from_online/my 1st platformer.pmp")
srproject = frproject.to_second(info_api)

def allow_opcode(opcode: str) -> SuccessfulMatchResult | None:
    # Do whatever you want...
    # Here I am using the custom handler to allow multiple values at a certain location
    allowed = opcode in [
        "if <CONDITION> then {THEN}",
        "if <CONDITION> then {THEN} else {ELSE}",
        "switch (CONDITION) {CASES}",
        "switch (CONDITION) {CASES} default {DEFAULT}",
    ]
    # We can return an empty result, as we do not care about access points (discussed later)
    return SuccessfulMatchResult() if allowed else None

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
                            # Provide the function instead of a Const
                            opcode=allow_opcode,
                        ),
                    ],
                ),
            },
        ),
    ],
)

visitor = TreeVisitor.new_include_only(included=[SRScript])
# Run the TreeVisitor on the whole project
path_to_node_map = visitor.visit_tree(srproject)
# Find all matches
matches: list[tuple[AbstractTreePath, SRScript]] = []
for path, node in path_to_node_map.items():
    match_result = match_handler(handler=pattern, value=node)
    if match_result is not None:
        matches.append((path, node))

# Print some matches for brevity
for index, path_and_node in enumerate(matches):
    match_path, match_node = path_and_node
    forever_block = match_node.blocks[1]
    # "BODY" must be a SRScriptInputValue => must have .blocks
    if_block_or_similar = forever_block.inputs["BODY"].blocks[0]
    # Print the first and different ones:
    if (index == 0) or (if_block_or_similar.opcode != "if <CONDITION> then {THEN}"):
        print("An interesting match found at", match_path)
        print("Matching Script:")
        print(match_node)