from pypenguin.opcode_info.data_imports import *

class ExtensionDropdownType(DropdownType):
    in_out_menue = DropdownTypeInfo(
        direct_values=["IN", "OUT"],
        rules=[],
        old_direct_values=["IN", "OUT"],
        fallback=None,
    )

class ExtensionInputType(InputType):
    pass

dumbExample = OpcodeInfoGroup(
    name="dumbExample",
    opcode_info=DualKeyDict({
        ("dumbExample_last_used_base", "dumbExample::last used base"): OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=True,
            monitor_id_behaviour=MonitorIdBehaviour.OPCFULL,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("dumbExample_last_two_inout_values", "dumbExample::last two [S1] and [S2] values"): OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict({
                ("S1", "S1"): DropdownInfo(type=ExtensionDropdownType.in_out_menue),
                ("S2", "S2"): DropdownInfo(type=ExtensionDropdownType.in_out_menue),
            }),
            can_have_monitor=True,
            monitor_id_behaviour=MonitorIdBehaviour.OPCFULL_PARAMS,
            has_shadow=False,
            has_variable_id=True,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("dumbExample_menu_in_out_menue", "dumbExample_menu_in_out_menue"): OpcodeInfo(
            opcode_type=OpcodeType.MENU,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=True,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
    }),
)

extension_fingerprint = ContentFingerprint(length=1231, hash=b'\xbf\xb6\xfb\x13@\xc6\x13\xdb\x0f\x81\xcbW\x9ea\x0f\x1dc\xbc\xf9\x07\x87Z\xf8\xcbQ\xdb\xc1}GV\xa3\xf2')