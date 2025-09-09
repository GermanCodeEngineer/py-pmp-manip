from pmp_manip import (
    get_default_config, init_config,
    info_api,
)
from pmp_manip.opcode_info.api.main import BUILTIN_EXT_TO_PATH

cfg = get_default_config()
init_config(cfg)

#info_api.generate_and_add_extension("pmMotionExpansion", extension_source=None)
#"""
for builtin_ext_id in BUILTIN_EXT_TO_PATH.keys():
    try:
        info_api.generate_and_add_extension(builtin_ext_id, extension_source=None, is_strict=True)
    except Exception as error:
        print("failed", builtin_ext_id, str(error).splitlines()[0])
        raise
    else:
        print("succeeded", builtin_ext_id)
#"""

