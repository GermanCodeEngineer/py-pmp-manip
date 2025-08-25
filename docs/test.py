from pmp_manip import get_default_config, init_config, FRProject, info_api
from pmp_manip.core.tools import TreeIteratorGenerator
from pmp_manip.utility import AbstractTreePath

cfg = get_default_config()
init_config(cfg)

# Load or Create a Project
frproject = FRProject.from_file("assets/from_online/my 1st platformer.pmp")
srproject = frproject.to_second(info_api)
#print(srproject)
#print(100*"=")

iterator_gen = TreeIteratorGenerator.new_include_all_except(excluded=())
pairs = iterator_gen.iterate_tree(srproject)
print(type(pairs), type(pairs[0]), type(pairs[0][0]), type(pairs[0][1]))

