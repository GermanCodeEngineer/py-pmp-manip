from pypenguin.opcode_info.data_imports import *

class ExtensionDropdownType(DropdownType):
    base_menu = DropdownTypeInfo(
        direct_values=["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"],
        rules=[],
        old_direct_values=["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"],
        fallback=None,
    )

class ExtensionInputType(InputType):
    base_menu = (
        InputMode.BLOCK_AND_DROPDOWN,
        None,
        ExtensionDropdownType.base_menu,
        0,
    )

gen_truefantombase = OpcodeInfoGroup(
    name="gen_truefantombase",
    opcode_info=DualKeyDict({
        ("is_base_block", "is_base_block"): OpcodeInfo(
            opcode_type=OpcodeType.BOOLEAN_REPORTER,
            inputs=DualKeyDict({
                ("A", "A"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
                ("B", "B"): InputInfo(
                    type=ExtensionInputType.base_menu,
                    menu=MenuInfo(opcode="base_menu", inner="base_menu"),
                ),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            has_shadow=False,
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("base_block", "base_block"): OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict({
                ("A", "A"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
                ("B", "B"): InputInfo(
                    type=ExtensionInputType.base_menu,
                    menu=MenuInfo(opcode="base_menu", inner="base_menu"),
                ),
                ("C", "C"): InputInfo(
                    type=ExtensionInputType.base_menu,
                    menu=MenuInfo(opcode="base_menu", inner="base_menu"),
                ),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            has_shadow=False,
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
    }),
)