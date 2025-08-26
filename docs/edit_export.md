# Editing and Exporting Projects in `pmp_manip`

## Searching a Project

### Primitive Attempt
Let us try find all blocks.
```python
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
Run the `TreeVisitor` recursively on an Abstract Second Representation Tree.
Returns a map from node path (from tree root to value) to node value.



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
* Next Page: **Handling Extensions**, see [docs/handling_extensions.md](handling_extensions.md)

