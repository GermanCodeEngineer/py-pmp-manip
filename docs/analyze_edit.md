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
There is a **corresponding pattern class for every script or block related class.** 
Pattern classes have the **same attributes as their second representation equivalents.**
### `Pattern`
Basis for a Pattern selecting Second Representation Scripts, Blocks etc.
Every subclass corresponds to a specific SR class and matches against its attributes.
#### `Pattern.access_point_id`
* **type**: `str` or `None`
* **description in SR**: An optional identifier for the match location in the Second Representation tree. If provided, the matched object is stored and accessible on success under this access point ID.
* **default value**: `None`
---

### `ScriptPattern`
Pattern for selecting [`SRScript`](second_repr.md#srscript) instances with certain data.
#### `ScriptPattern.position`
* **type**: `Const[tuple[int | float, int | float]]` or `Callable[[tuple[int | float, int | float]], SuccessfulMatchResult|None]` or `tuple[int | float, int | float]` or `None`
* **description in SR**: Stores the position of the script in the "Code" tab. Unlimited, but usually in the range of hundreds and thousands.
* **default value**: `None`
#### `ScriptPattern.blocks`
* **type**: `Const[list[SRBlock]]` or `Callable[[list[SRBlock]], SuccessfulMatchResult|None]` or `list[BlockHandler]`,<br> where `BlockHandler` means `Const[SRBlock]` or `Callable[[SRBlock], SuccessfulMatchResult|None]` or `BlockPattern`
* **description in SR**: Stores the script's sequence of blocks from top to bottom.
* **default value**: `[]`
---

### `BlockPattern`
Pattern for selecting [`SRBlock`](second_repr.md#srblock) instances with certain data.
#### `BlockPattern.opcode`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: The unique identifier for it's kind of block.
* **default value**: `None`
#### `BlockPattern.inputs`
* **type**: `Const[dict[str, SRInputValue]]` or `Callable[[dict[str, SRInputValue]], SuccessfulMatchResult|None]` or `dict[str, InputHandler]`,<br>where `InputHandler` means `Const[SRInputValue]` or `Callable[[SRInputValue], SuccessfulMatchResult|None]` or `InputPattern`
* **description in SR**: The arguments fields of the block and their values. Includes text, number fields, round dropdowns one can insert blocks into and all others except for square dropdowns.
* **default value**: `{}`
#### `BlockPattern.dropdowns`
* **type**: `Const[dict[str, SRDropdownValue]]` or `Callable[[dict[str, SRDropdownValue]], SuccessfulMatchResult|None]` or `dict[str, DropdownHandler]`,<br>where `DropdownHandler` means `Const[SRDropdownValue]` or `Callable[[SRDropdownValue], SuccessfulMatchResult|None]` or `DropdownPattern`
* **description in SR**: The argument fields of the block and their values. Only includes square dropdowns, not round dropdowns one can insert blocks into.
* **default value**: `{}`
#### `BlockPattern.comment`
* **type**: `Const[SRComment | None]` or `Callable[[SRComment | None], SuccessfulMatchResult|None]` or `None`
* **description in SR**: The optional attached comment of the block.
* **default value**: `None`
#### `BlockPattern.mutation`
* **type**: `Const[SRMutation]` or `CBArgumentMutationPattern` or `CBMutationPattern` or `CBCallMutationPattern` or `None`
* **description in SR**: The optional mutation of the block for some opcodes(kinds of blocks). Most blocks do not need one.
* **default value**: `None`
---

### `InputPattern`
Pattern for selecting [`SRInputValue`](second_repr.md#srinputvalue) instances (or subclasses) with certain data.
#### `InputPattern.blocks`
* **type**: `Const[list[SRBlock]]` or `Callable[[list[SRBlock]], SuccessfulMatchResult|None]` or `list[BlockHandler]`,<br> where `BlockHandler` means `Const[SRBlock]` or `Callable[[SRBlock], SuccessfulMatchResult|None]` or `BlockPattern`
* **description in SR**: Stores the subscript's sequence of blocks from top to bottom (e.g. the "then" section of the "if" block).
* **default value**: `[]`
#### `InputPattern.block`
* **type**: `Const[SRBlock | None]` or `Callable[[SRBlock | None], SuccessfulMatchResult|None]` or `BlockPattern` or `None`
* **description in SR**: Stores the optional block inserted into the argument text field, round dropdown menu etc.
* **default value**: `None`
#### `InputPattern.immediate`
* **type**: `Const[str | bool | None]` or `Callable[[str | bool | None], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the "immediate" value of the input value i.e. if the default value if no block is dragged into the input.
* **default value**: `None`
#### `InputPattern.dropdown`
* **type**: `Const[SRDropdownValue | None]` or `Callable[[SRDropdownValue | None], SuccessfulMatchResult|None]` or `DropdownPattern` or `None`
* **description in SR**: Stores the round dropdown menu of the input value.
* **default value**: `None`
---

### `DropdownPattern`
Pattern for selecting [`SRDropdownValue`](second_repr.md#srdropdownvalue) instances with certain data.
#### `DropdownPattern.kind`
* **type**: `Const[DropdownValueKind]` or `Callable[[DropdownValueKind], SuccessfulMatchResult|None]` or `None`
* **description in SR**: Stores the kind of thing the dropdown value refers to (e.g. `VARIABLE`, `SPRITE`, `OBJECT` or `STANDARD`).
* **default value**: `None`
#### `DropdownPattern.value`
* **type**: `Const[str | (int)]` or `Callable[[str | (int)], SuccessfulMatchResult|None]` or `None`
* **description in SR**: Stores the actual value of the dropdown value.
* **default value**: `None`
---

### `CBArgumentMutationPattern`
Pattern for selecting [`SRCustomBlockArgumentMutation`](second_repr.md#srcustomblockargumentmutation) instances with certain data.
#### `CBArgumentMutationPattern.argument_name`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the name of the custom block argument which the argument reporter block is for.
* **default value**: `None`
#### `CBArgumentMutationPattern.main_color`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the main color of the "define" block the argument reporter block is for.
* **default value**: `None`
#### `CBArgumentMutationPattern.prototype_color`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the main color of the inner block of the "define" block the argument reporter block is for.
* **default value**: `None`
#### `CBArgumentMutationPattern.outline_color`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the outline color of the inner block of the "define" block the argument reporter block is for.
* **default value**: `None`
---

### `CBMutationPattern`
Pattern for selecting [`SRCustomBlockMutation`](second_repr.md#srcustomblockmutation) instances with certain data.
#### `CBMutationPattern.custom_opcode`
* **type**: `Const[SRCustomBlockOpcode]` or `Callable[[SRCustomBlockOpcode], SuccessfulMatchResult|None]` or `CBOpcodePattern` or `None`
* **description in SR**: Stores the name and argument field names and kinds of the custom block.
* **default value**: `None`
#### `CBMutationPattern.no_screen_refresh`
* **type**: `Const[bool]` or `Callable[[bool], SuccessfulMatchResult|None]` or `None`
* **description in SR**: Wether the "Run without screen refresh" box was ticked when creating the custom block.
* **default value**: `None`
#### `CBMutationPattern.optype`
* **type**: `Const[SRCustomBlockOptype]` or `Callable[[SRCustomBlockOptype], SuccessfulMatchResult|None]` or `None`
* **description in SR**: What shape of block the custom block is (e.g. square statement, boolean, reporter).
* **default value**: `None`
#### `CBMutationPattern.main_color`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the main color of the "define" block.
* **default value**: `None`
#### `CBMutationPattern.prototype_color`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the main color of the inner block of the "define" block.
* **default value**: `None`
#### `CBMutationPattern.outline_color`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the outline color of the inner block of the "define" block the argument reporter block is for.
* **default value**: `None`
---

### `CBCallMutationPattern`
Pattern for selecting [`SRCustomBlockCallMutation`](second_repr.md#srcustomblockcallmutation) instances with certain data.
#### `CBCallMutationPattern.custom_opcode`
* **type**: `Const[SRCustomBlockOpcode]` or `Callable[[SRCustomBlockOpcode], SuccessfulMatchResult|None]` or `CBOpcodePattern` or `None`
* **description in SR**: Stores the labels and argument field names and kinds of the custom block, this block will call, to reference it.
* **default value**: `None`
---

### `CBOpcodePattern`
Pattern for selecting [`SRCustomBlockOpcode`](second_repr.md#srcustomblockopcode) instances with certain data.
#### `CBOpcodePattern.segments`
* **type**: `Const[tuple[str | SRCustomBlockArgument]]` or `Callable[[tuple[str | SRCustomBlockArgument]], SuccessfulMatchResult|None]` or `tuple[CBArgumentHandler]` or `None`<br> where `CBArgumentHandler` means `Const[str | SRCustomBlockArgument]` or `Callable[[str | SRCustomBlockArgument], SuccessfulMatchResult|None]` or `CBArgumentPattern`
* **description in SR**: Stores the labels and argument field names and kinds of the custom block. A `str` item represents a label, a `SRCustomBlockArgument` represents an argument of the custom block.
* **default value**: `None`
---

### `CBArgumentPattern`
Pattern for selecting [`SRCustomBlockArgument`](second_repr.md#srcustomblockargument) instances with certain data.
#### `CBArgumentPattern.name`
* **type**: `Const[str]` or `Callable[[str], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the name of the argument.
* **default value**: `None`
#### `CBArgumentPattern.type`
* **type**: `Const[SRCustomBlockArgumentType]` or `Callable[[SRCustomBlockArgumentType], SuccessfulMatchResult|None]` or `None`
* **description in SR**: the kind of the argument (string or number vs. boolean).
* **default value**: `None`

Notes:
* see SR Class link for details on attributes etc.
---

### `Const`
Requires an exact constant value at it's location in a pattern or similar. 
#### `Const.value`
* **type**: `Any`
* **description**: the exact constant value required for a successful match.

### `match_handler`
ignore result for now

### Terminology
* "**Handler**" means either a subclass of [`Pattern`](#pattern), a [custom function](#custom-functionlike-handler).

### Custom Functionlike Handler
* A custom callable (e.g. `def` or `lambda` function).
* Takes one argument of the specified type.
* Should returns a `SuccessfulMatchResult` if it consideres with the given value a match otherwise `None`.
* \# TODO: nested match calls

### `SuccessfulMatchResult`

## Use

## Editing a Project






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
* Next Page: **Exporting Projects**, see [docs/export.pmp](export.md)

