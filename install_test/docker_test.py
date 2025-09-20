# Test Importing and Project Creation
from pmp_manip import SRProject
SRProject.create_empty()

# Test Building an extension
from pmp_manip import (
    get_default_config, init_config,
    info_api,
)

cfg = get_default_config()
init_config(cfg)

extension = "pmSensingExpansion"
info_api.generate_and_add_extension(extension, extension_source=None)
found = False
for opcode in info_api.opcode_info.keys_key1():
    if opcode.startswith(f"{extension}_"):
        found = True
assert found, "Did not add extension successfully"

print("Package imported successfully!")
