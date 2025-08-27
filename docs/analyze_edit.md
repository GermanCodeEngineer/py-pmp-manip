# Analyzing and Editing Projects in `pmp_manip`

## Searching a Project for specific data

### Primitive Attempt
Let us try find e.g. all blocks.
```python
from pmp_manip import get_default_config, init_config, info_api, FRProject

cfg = get_default_config()
init_config(cfg)

# Load or Create a Project
frproject = FRProject.from_file("assets/from_online/my 1st platformer.pmp")
# Convert it into the good format
srproject = frproject.to_second(info_api)

all_blocks = []

# Group Stage and Sprites, as they all have blocks
targets = [srproject.stage] + srproject.sprites
for target in targets:
    # Scan every script in it
    for script in target.scripts:
        # Scan every block in that script
        for block in script.blocks:
            all_blocks.append(block)

            # Oh, but blocks can contain blocks
            for input in block.inputs.values():
                # because SRInputValue itself does not guarantee attribute existance:
                input_block = getattr(input, "block", None)
                input_blocks = getattr(input, "blocks", [])
                if input_block is not None:
                    all_blocks.append(input_block)
                all_blocks.extend(input_blocks)

                # Oh, but these blocks can contain blocks too...
```
It is seemingly harder then we thought. It is technically possible to do this manually, **but `pmp_manip` provides better alternatives.**

### `TreeVisitor`
A `TreeVisitor` object automates the (filtered) iteration of a whole `SRProject` or parts of it.
There are two ways to create a `TreeVisitor` object.

### `TreeVisitor.new_include_all_except(excluded: Iterable[type[SECOND_REPR_T]]) -> TreeVisitor[SECOND_REPR_T]`
`new_include_all_except` creates a `TreeVisitor` which includes all second representation objects except for the specified types.


### `TreeVisitor.new_include_only(included: Iterable[type[INCLUDED_T]]) -> TreeVisitor[INCLUDED_T]`
`new_include_only` creates a `TreeVisitor` which only includes second representation objects of the specified types.

### `TreeVisitor.visit_tree(obj: SECOND_REPR_T) -> dict[AbstractTreePath, INCLUDED_T]`
Run the alredy configured `TreeVisitor` recursively on an Abstract Second Representation Tree.
Returns a map from node path (from tree root to value) to node value.

### Example using `TreeVisitor`
Let us try it:
```python
from pmp_manip import (
    get_default_config, init_config, info_api, FRProject,
    TreeVisitor,
)

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file("assets/from_online/my 1st platformer.pmp")
srproject = frproject.to_second(info_api)

# Create our TreeVisitor with configuration. Let us allow everything for now:
visitor = TreeVisitor.new_include_all_except(excluded=[])

# Run the TreeVisitor
path_to_node_map = visitor.visit_tree(srproject)
# Get only nodes and discard paths (just for this example)
all_nodes = list(path_to_node_map.values())

print(f"Found {len(path_to_node_map)} element(s)")
# Let us see what types of nodes we get
for i, item in enumerate(all_nodes[:10]):
    print(f"Sample node type: {type(item).__name__}")
```
Output:
```
Found 516 element(s)
Sample node type: SRStage
Sample node type: SRScript
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRScriptInputValue
Sample node type: SRBlock
Sample node type: SRBlockAndBoolInputValue
Sample node type: SRScriptInputValue
Sample node type: SRVectorCostume
Sample node type: SRSound
```
We got over 500 nodes of varying types like `SRStage`, `SRBlock` or `SRSound`.
But we are only looking for blocks. For that we need to configure our `TreeVisitor` differently:

```python
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
```
Output:
```
Found 180 element(s)
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRBlock
Sample node type: SRBlock
Example Node:
SRBlock(
    opcode="change [EFFECT] sprite effect by (AMOUNT)",
    inputs={
        "AMOUNT": SRBlockAndTextInputValue(block=None, immediate="25"),
    },
    dropdowns={
        "EFFECT": SRDropdownValue(kind=DropdownValueKind.STANDARD, value="ghost"),
    },
    comment=None,
    mutation=None,
)
```
We reached our goal! You know now how to find all node of a/multiple types in a project.
You can run a `TreeVisitor` on parts of a project too e.g. only the stage, a single script etc.

### Searching for more complex Block and Script Patterns
What if you are not looking for all blocks but only some blocks e.g. with a certain `opcode`?
Or what if you are looking for certain multi-block structures?
`pmp_manip` provides `Pattern` search system for blocks, scripts and related objects.

### Patterns
Subclasses Table

### Const

### Custom Functionlike Handler
What to take what to call

### `match_handler`
ignore result for now


## Editing a Project

### `MatchResult`





## Saving a Project to a file

### `FRProject.to_file(self, file_path: str) -> None`

You can save a project to a .sb3 or .pmp file using `FRProject.to_file`:

```python
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
```
Output:
```
Project was saved to a file successfully :)
```

You can now upload `"path/to/my_modified_project.pmp"` to the PenguinMod Editor and inspect it.

---

### References
* For a **documentation overview** and **all pages** of the tutorial, see [docs/index.md](index.md)
* Next Page: **Handling Extensions**, see [docs/handling_extensions.md](handling_extensions.md)

