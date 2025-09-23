from pmp_manip import *
#from pmp_manip.opcode_info.doc_api import *


#create_mkdocs_project(site_name="abx")
init_config(get_default_config())
f = FRProject.from_file("assets/e.pmp")
print(f)

#info_api.generate_and_add_extension("pen", None)

s = f.to_second(info_api)
print(s)

script = SRScript(
    position=(0,0),
    blocks=[
        SRBlock(
            opcode="&lists::filter [LIST] by (INDEX) (ITEM) <KEEP>",
            inputs={
                "INDEX": SRBlockAndTextInputValue(
                    block=None,
                    immediate=""
                ),
                "ITEM": SRBlockAndTextInputValue(
                    block=None,
                    immediate=""
                ),
                "KEEP": SRBlockAndTextInputValue(
                    block=None,
                    immediate=""
                )
            },
            dropdowns={
                "LIST": SRDropdownValue(DropdownValueKind.LIST, "x")
            },
        )
    ],
)
SRBlock(
                    opcode="&special::{{POLYGON MENU}}"
                )
s.sprites[0].scripts.append(script)
#print(s.sprites[0].scripts[0])
s.validate(info_api)
