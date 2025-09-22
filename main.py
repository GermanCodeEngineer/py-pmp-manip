from pmp_manip import (
    get_default_config, init_config,
    info_api,
)
from pmp_manip.opcode_info.api.main import BUILTIN_EXTENSIONS

cfg = get_default_config()
init_config(cfg)

#info_api.generate_and_add_extension("pmSensingExpansion", extension_source=None)#
"""
for builtin_ext_id in BUILTIN_EXTENSIONS:
    if builtin_ext_id != "pmInlineBlocks":
        continue
    try:
        info_api.generate_and_add_extension(builtin_ext_id, extension_source=None)
    except Exception as error:
        print("failed", builtin_ext_id, str(error).splitlines()[:1])
        raise
    else:
        print("succeeded", builtin_ext_id)
#"""

from pmp_manip import FRProject
f = FRProject.from_file("assets/extension_sources.pmp")
print(f)
print(dict(f.extension_urls))

