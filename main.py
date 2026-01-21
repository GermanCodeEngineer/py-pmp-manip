from pmp_manip import *
init_config(get_default_config())
empty = SRProject.create_empty()
empty.sprites.append(SRSprite.create_empty(name="hi"))
print(empty)


print(CBCallMutationPattern())
SRExpandableJoinMutation(input_count=2)
