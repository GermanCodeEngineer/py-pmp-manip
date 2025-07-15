from pypenguin.opcode_info.data_imports import *

class ExtensionDropdownType(DropdownType):
    pass

class ExtensionInputType(InputType):
    pass

pmControlsExpansion = OpcodeInfoGroup(
    name="pmControlsExpansion",
    opcode_info=DualKeyDict({
        ("pmControlsExpansion_ifElseIf", "pmControlsExpansion::if <CONDITION1> then {SUBSTACK} else if <CONDITION2> then {SUBSTACK2}"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("CONDITION1", "CONDITION1"): InputInfo(type=BuiltinInputType.BOOLEAN, menu=None),
                ("CONDITION2", "CONDITION2"): InputInfo(type=BuiltinInputType.BOOLEAN, menu=None),
                ("SUBSTACK", "SUBSTACK"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
                ("SUBSTACK2", "SUBSTACK2"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("pmControlsExpansion_ifElseIfElse", "pmControlsExpansion::if <CONDITION1> then {SUBSTACK} else if <CONDITION2> then {SUBSTACK2} else {SUBSTACK3}"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("CONDITION1", "CONDITION1"): InputInfo(type=BuiltinInputType.BOOLEAN, menu=None),
                ("CONDITION2", "CONDITION2"): InputInfo(type=BuiltinInputType.BOOLEAN, menu=None),
                ("SUBSTACK", "SUBSTACK"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
                ("SUBSTACK2", "SUBSTACK2"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
                ("SUBSTACK3", "SUBSTACK3"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("pmControlsExpansion_asNewBroadCast", "pmControlsExpansion::new thread {SUBSTACK}"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("SUBSTACK", "SUBSTACK"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("pmControlsExpansion_restartFromTheTop", "pmControlsExpansion::restart from the top"): OpcodeInfo(
            opcode_type=OpcodeType.ENDING_STATEMENT,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("pmControlsExpansion_asNewBroadCastArgs", "pmControlsExpansion::new thread with data (DATA) {SUBSTACK}"): OpcodeInfo(
            opcode_type=OpcodeType.STATEMENT,
            inputs=DualKeyDict({
                ("DATA", "DATA"): InputInfo(type=BuiltinInputType.TEXT, menu=None),
                ("SUBSTACK", "SUBSTACK"): InputInfo(type=BuiltinInputType.SCRIPT, menu=None),
            }),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
        ("pmControlsExpansion_asNewBroadCastArgBlock", "pmControlsExpansion::thread data"): OpcodeInfo(
            opcode_type=OpcodeType.STRING_REPORTER,
            inputs=DualKeyDict(),
            dropdowns=DualKeyDict(),
            can_have_monitor=False,
            monitor_id_behaviour=None,
            has_shadow=False,
            has_variable_id=False,
            special_cases={},
            old_mutation_cls=None,
            new_mutation_cls=None,
        ),
    }),
)

extension_fingerprint = ContentFingerprint(length=13907, hash=b'b\x0f\xd6\xcaMP{\xe4\x8d\xbd52\xd9\x90>\x15`\xf1H4\xf6I&\tc\xb5\x7fM\xea|-\x91')