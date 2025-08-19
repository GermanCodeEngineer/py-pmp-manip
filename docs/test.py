from pmp_manip import get_default_config, init_config, info_api, FRProject, SRProject, SRSprite, SRScript, SRBlock, SRBlockAndDropdownInputValue, SRDropdownValue
from pmp_manip.opcode_info.api import DropdownValueKind

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="assets/small_example.pmp")
print(frproject)
srproject = frproject.to_second(info_api)
print("The contents of the project are:")
print(srproject)

frproject = srproject.to_first(info_api)
print(frproject)

"""srproject = SRProject.create_empty()
main_sprite = SRSprite.create_empty(name="my sprite")
script = SRScript(
    position=(0,0),
    blocks=[
        SRBlock(
            opcode="stop script [TARGET]",
            inputs={},
            dropdowns={
                "TARGET": SRDropdownValue(
                    kind=DropdownValueKind.STANDARD,
                    value="this script",
                ),
            },
        )
    ],
)
main_sprite.scripts.append(script)
srproject.sprites.append(main_sprite)
srproject.sprite_layer_stack.append(main_sprite.uuid)

print(srproject)
srproject.validate(info_api)"""


