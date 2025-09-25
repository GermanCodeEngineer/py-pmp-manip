from pmp_manip import *
#from pmp_manip.opcode_info.doc_api import *


#create_mkdocs_project(site_name="abx")
init_config(get_default_config())


f = FRProject.from_file("in.pmp")
print(f)

"""
s = f.to_second(info_api)
print(s)
s.validate(info_api)
script = s.sprites[0].scripts[-1]
if_block = script.blocks[0]
if_block.mutation.branches = 3
if_block.mutation.ends_inn_else = True
for i in range(1, 3+1):
    if_block.inputs[f"THEN{i}"] = SRScriptInputValue(blocks=[])
for i in range(1, 3+1):
    if_block.inputs[f"CONDITION{i}"] = SRBlockAndBoolInputValue(block=None, immediate=True)
print(if_block)
"""
s = SRProject.create_empty()
sprite = SRSprite.create_empty(name="my_Sprite")
script = SRScript(
    position=(0,0),
    blocks=[
        SRBlock(
            opcode="&control::if <CONDITION> then {THEN}",
            inputs={
                "CONDITION": SRBlockAndBoolInputValue(
                    block=None,
                    immediate=True,
                ),
                "THEN": SRScriptInputValue(
                    blocks=[],
                ),
            },
        ),
    ],
)
sprite.scripts.append(script)
s.sprites.append(sprite)
s.sprite_layer_stack.append(sprite.uuid)

s.validate(info_api)

f = s.to_first(info_api)
f.to_file("out.pmp")
