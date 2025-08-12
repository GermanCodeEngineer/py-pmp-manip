Core functionality of the `pmp_manip` project needs information about block opcodes to work with those blocks.
**Custom** and **Builtin** extensions allow the creation of custom blocks, which `pmp_manip` does not know how to handle by default.

For example:
```py
from pmp_manip import FRProject
from pmp_manip.opcode_info.data import info_api
from pmp_manip.config import get_default_config, init_config

# Init the required configuration
cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="path/to/my_music_project.py")
srproject = frproject.to_second(info_api)
print("Project was converted successfully :)")
```
will raise
```bash
>>> python my_script.py
pmp_manip.utility.errors.MANIP_UnknownOpcodeError: Could not find OpcodeInfo by old opcode 'music_playDrumForBeats'. Have you possibly forgotten to add an extension?
```
because that project uses Scratch's music extension and `info_api`(the api managing info about block opcodes) does not know about the music extension by default. You need to explicitly add it:

```py
from pmp_manip import FRProject
from pmp_manip.opcode_info.api import BuiltinExtensionRef
from pmp_manip.opcode_info.data import info_api
from pmp_manip.config import get_default_config, init_config

# Init the required configuration
cfg = get_default_config()
init_config(cfg)

# Import and add the music extension
info_api.add_extension(BuiltinExtensionRef.music)

frproject = FRProject.from_file(file_path="path/to/my_music_project.py")
srproject = frproject.to_second(info_api)
print("Project was converted successfully :)")
```
Now it works. But what if you want to use a custom extension or do not want to add all extensions manually?
For Custom Extensions, the required info py file has to be generated first.
Let's a basic setup;

```py
from pmp_manip import FRProject
from pmp_manip.opcode_info.api import BuiltinExtensionRef
from pmp_manip.opcode_info.data import info_api
from pmp_manip.config import get_default_config, init_config

cfg = get_default_config()
init_config(cfg)

# Load the project
frproject = FRProject.from_file(file_path="path/to/my_music_project.py")
# Then add all extensions required for that project automatically
frproject.add_all_extensions_to_info_api(info_api)
# Then use it how you want...
srproject = frproject.to_second(info_api)
print("Project was converted successfully :)")
```
`add_all_extensions_to_info_api` is available for both `FRProject` and `SRProject` instances
It runs the extension info generator under the hood

