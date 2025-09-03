from pmp_manip import init_config, get_default_config, FRProject, info_api
from pmp_manip.utility import write_file_text
init_config(get_default_config())

from pmp_manip.ext_info_gen.manager import generate_extension_info_py_file

generate_extension_info_py_file("https://extensions.penguinmod.com/extensions/derpygamer2142/gpusb3.js", "gpusb3", False)

