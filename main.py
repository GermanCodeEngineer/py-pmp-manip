from pmp_manip import (
    get_default_config, init_config,
    info_api,
)
from pmp_manip.opcode_info.api.main import BUILTIN_EXTENSIONS

cfg = get_default_config()
init_config(cfg)

info_api.generate_and_add_extension("pen", extension_source=None)
"""
for builtin_ext_id in BUILTIN_EXTENSIONS.keys():
    try:
        info_api.generate_and_add_extension(builtin_ext_id, extension_source=None)
    except Exception as error:
        print("failed", builtin_ext_id, str(error).splitlines()[:1])
        raise
    else:
        print("succeeded", builtin_ext_id)
"""

