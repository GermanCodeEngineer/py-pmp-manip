from pmp_manip import get_default_config, init_config, FRProject, info_api
from PIL import Image, ImageFile

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="assets/asset_formats.pmp")

srproject = frproject.to_second(info_api)
print("The contents of the project are:")
print(srproject)
x = srproject.sprites[0].costumes[1].content
print(type(x), isinstance(x, Image.Image))
