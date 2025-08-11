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

frproject = FRProject.from_file(file_path="path/to/my_project.py")
srproject = frproject.to_second(info_api)
```
will raise
```bash
>>> python my_script.py
pmp_manip.utility.errors.MANIP_UnknownOpcodeError: Could not find OpcodeInfo by old opcode 'music_playDrumForBeats'. Have you possibly forgotten to add an extension?
```
because the that project uses Scratch's music extension and `info_api`(the api managing info about block opcodes) does not know about the music extension by default. You need to add it manually:


Those builtin extensions
For this reason the extension opcode info generator submodule exists.