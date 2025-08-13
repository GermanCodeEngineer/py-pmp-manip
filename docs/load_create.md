# Loading and Creating Projects in `pmp_manip`

## Loading a Project from a file

### `FRProject.from_file(cls, file_path: str) -> FRProject`
You can load a project from `.sb3` or `.pmp` file using `FRProject.from_file`:

```python
from pmp_manip import get_default_config, init_config, FRProject

# Init the required configuration
cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="path/to/my_project.pmp")
print("Project was loaded from a file successfully :)")
```
`frproject` is now an `FRProject`(First Representation Project) instance:
```
Project was loaded from a file successfully :)
```

Let's compare `FRProject` and `SRProject`

| attribute   | First Representatation (`FRProject`)         | Second Representation (`SRProject`)                      |
|-------------|----------------------------------------------|----------------------------------------------------------|
| structure   | similar to `.sb3` or `.pmp` files; JSON tree | Object Oriented; Tree of Custom Dataclasses              |
| efficiency  | inefficient; hard to understand and modify   | efficient; easy to understand and modify                 |
| ex/import   | Yes through `.from_file` and `.to_file`      | No, Must be converted from and to `FRProject`            |
| recommended | Nooooooooooooooooooooooooooooooo             | Yes, even has a `.validate` method to check for mistakes |

It is recommended to always use `SRProject` for analyzation, modification etc. and only use `FRProject` to import from and export to files. To transform a `FRProject` into a `SRProject` we use `FRProject.to_second` 
### `FRProject.to_second(self, info_api: OpcodeInfoAPI) -> SRProject`
* converts **First** to **Second** Representation
* `info_api` and extensions will be discussed later in detail





### References
* For a **documentation overview** and **all pages** of the tutorial, see [docs/index.md](index.md)
* Next Page: **Handling Extension**, see [docs/handling_extensions.md](handling_extensions.md)
