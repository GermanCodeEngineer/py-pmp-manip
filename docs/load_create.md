# Loading and Creating Projects in `pmp_manip`

## Loading a Project from a file

### `FRProject.from_file(cls, file_path: str) -> FRProject`

You can load a project from a .sb3 or .pmp file using `FRProject.from_file`:

```python
from pmp_manip import get_default_config, init_config, FRProject

# Init the required configuration
cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="path/to/my_project.pmp")
print("Project was loaded from a file successfully :)")
```
Output:
```
Project was loaded from a file successfully :)
```

`frproject` is now an `FRProject` (First Representation Project) instance.


---

## Comparing FRProject and SRProject

| attribute   | First Representatation (`FRProject`)         | Second Representation (`SRProject`)                      |
|-------------|----------------------------------------------|----------------------------------------------------------|
| structure   | similar to `.sb3` or `.pmp` files; JSON tree | Object Oriented; Tree of Custom Dataclasses              |
| efficiency  | inefficient; hard to understand and modify   | efficient; easy to understand and modify                 |
| ex/import   | Yes through `.from_file` and `.to_file`      | No, Must be converted from and to `FRProject`            |
| recommended | Nooooooooooooooooooooooooooooooo             | Yes, even has a `.validate` method to check for mistakes |


Recommendation:
Always use `SRProject` for analysis and modifications, and only use `FRProject` to import from/export to files.


---

## Converting from FRProject to SRProject

### `FRProject.to_second(self, info_api: OpcodeInfoAPI) -> SRProject`

Converts First Representation --> Second Representation

Requires info_api (it and projects with extensions will be discussed later)


Example:

```python
from pmp_manip import get_default_config, init_config, FRProject, info_api

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="path/to/my_project.pmp")
print("Project was loaded from a file successfully :)")

# Use to_second to covert from First to Second Representation
srproject = frproject.to_second(info_api)
print("Project was converted into Second Representation successfully :)")
```

Output:
```
Project was loaded from a file successfully :)
Project was converted into Second Representation successfully :)
```

srproject is now an SRProject instance - much easier to work with for edits.


---

## Creating an empty Project

### `SRProject.create_empty(cls) -> SRProject`

Creates a project with:
* No sprites
* No variables
* Default settings
* Everything in Second Representation.

Example:

```python
from pmp_manip import get_default_config, init_config, SRProject

cfg = get_default_config()
init_config(cfg)

srproject = SRProject.create_empty()
print("Empty project was created successfully :)")
```

Output:
```
Empty project was created successfully :)
```

You now have a blank project to work with.
(How to understand and modify projects will be covered in the next page.)


---

### References
* For a **documentation overview** and **all pages** of the tutorial, see [docs/index.md](index.md)
* Next Page: **Working with Second Representation**, see [docs/second_repr.md](second_repr.md)
