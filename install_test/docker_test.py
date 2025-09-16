from pmp_manip import SRProject
SRProject.create_empty()

from pmp_manip import (
    get_default_config, init_config,
    info_api,
)

cfg = get_default_config()
init_config(cfg)

info_api.generate_and_add_extension("pmSensingExpansion", extension_source=None)

print("Package imported successfully!")
