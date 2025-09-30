from pmp_manip import *

init_config(get_default_config())

f = FRProject.from_file("assets/from_online/Drive Mad Recreation (WIP).pmp")
print(f)

print(f.extensions)
print(dict(f.extension_urls))
info_api.generate_and_add_extension("griffpatch", 'https://extensions.turbowarp.org/box2d.js')

s = f.to_second(info_api)
print(s)

