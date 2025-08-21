# Editing and Exporting Projects in `pmp_manip`

## Editing a Project
### Example 1
### Example 2
### Example 3

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

