"""Generate a simple step-driven processor emulator PenguinMod project.

The generated project contains one sprite ("CPU") and implements a tiny register
machine with hardcoded instructions in lists. Execution is single-step only.
"""
from __future__ import annotations

from pathlib import Path

from lxml import etree

from pmp_manip import (
    get_default_config,
    init_config,
    info_api,
    SRProject,
    SRSprite,
    SRVectorCostume,
    SRVariable,
    SRList,
)
from pmp_manip.core.block import (
    SRBlock,
    SRScript,
    SRBlockAndTextInputValue,
    SRBlockAndDropdownInputValue,
    SRBlockAndBoolInputValue,
    SRScriptInputValue,
)
from pmp_manip.core.block_mutation import (
    SRCustomBlockMutation,
    SRCustomBlockCallMutation,
    SRCustomBlockArgumentMutation,
)
from pmp_manip.core.custom_block import (
    SRCustomBlockOpcode,
    SRCustomBlockArgument,
    SRCustomBlockArgumentType,
    SRCustomBlockOptype,
)
from pmp_manip.core.dropdown import SRDropdownValue
from pmp_manip.opcode_info.api.dropdown import DropdownValueKind
from pmp_manip.utility import AbstractTreePath


CB_MAIN = "#FF6680"
CB_PROTO = "#e65c73"
CB_OUTLINE = "#cc5266"


def txt(value: str, block: SRBlock | None = None) -> SRBlockAndTextInputValue:
    """Create a text/number input wrapper."""
    return SRBlockAndTextInputValue(block=block, immediate=value)


def bool_in(block: SRBlock | None, immediate: bool = False) -> SRBlockAndBoolInputValue:
    """Create a boolean input wrapper."""
    return SRBlockAndBoolInputValue(block=block, immediate=immediate)


def dd(kind: DropdownValueKind, value: str | int) -> SRDropdownValue:
    """Create a dropdown value."""
    return SRDropdownValue(kind=kind, value=value)


def block(
    opcode: str,
    *,
    inputs: dict[str, object] | None = None,
    dropdowns: dict[str, SRDropdownValue] | None = None,
    mutation: object | None = None,
) -> SRBlock:
    """Create an SRBlock with defaults to reduce boilerplate."""
    return SRBlock(
        opcode=opcode,
        inputs={} if inputs is None else inputs,
        dropdowns={} if dropdowns is None else dropdowns,
        comment=None,
        mutation=mutation,
    )


def var_ref(name: str) -> SRBlock:
    """Reporter block for a variable value."""
    return block(
        "&variables::value of [VARIABLE]",
        dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, name)},
    )


def list_item_ref(list_name: str, index_block: SRBlock) -> SRBlock:
    """Reporter block for item (INDEX) of list."""
    return block(
        "&lists::item (INDEX) of [LIST]",
        inputs={"INDEX": txt("1", index_block)},
        dropdowns={"LIST": dd(DropdownValueKind.LIST, list_name)},
    )


def equals(a: SRBlock, b: SRBlock | None = None, imm_b: str = "") -> SRBlock:
    """Boolean equality operator."""
    return block(
        "&operators::(OPERAND1) = (OPERAND2)",
        inputs={
            "OPERAND1": txt("", a),
            "OPERAND2": txt(imm_b, b),
        },
    )


def math_bin(opcode: str, left: SRBlock, right: SRBlock) -> SRBlock:
    """Create a binary arithmetic reporter."""
    return block(
        opcode,
        inputs={
            "OPERAND1": txt("0", left),
            "OPERAND2": txt("0", right),
        },
    )


def set_var(name: str, value_block: SRBlock | None = None, imm: str = "0") -> SRBlock:
    """Set variable block."""
    return block(
        "&variables::set [VARIABLE] to (VALUE)",
        inputs={"VALUE": txt(imm, value_block)},
        dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, name)},
    )


def change_var(name: str, value_block: SRBlock | None = None, imm: str = "1") -> SRBlock:
    """Change variable block."""
    return block(
        "&variables::change [VARIABLE] by (VALUE)",
        inputs={"VALUE": txt(imm, value_block)},
        dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, name)},
    )


def call_custom(custom_opcode: SRCustomBlockOpcode, inputs: dict[str, object]) -> SRBlock:
    """Call a custom block with the provided mutation and inputs."""
    return block(
        "&customblocks::call custom block",
        inputs=inputs,
        mutation=SRCustomBlockCallMutation(custom_opcode=custom_opcode),
    )


def cb_arg_text(argument_name: str) -> SRBlock:
    """Reporter for a custom block text/number argument."""
    return block(
        "&customblocks::custom block text arg [ARGUMENT]",
        mutation=SRCustomBlockArgumentMutation(
            argument_name=argument_name,
            main_color=CB_MAIN,
            prototype_color=CB_PROTO,
            outline_color=CB_OUTLINE,
        ),
    )


def create_processor_project() -> SRProject:
    """Construct the SRProject for the processor emulator."""
    cfg = get_default_config()
    init_config(cfg)

    project = SRProject.create_empty()
    cpu = SRSprite.create_empty(name="CPU")

    cpu.costumes = [
        SRVectorCostume(
            name="cpu",
            file_extension="svg",
            rotation_center=(60, 40),
            content=etree.fromstring(
                (
                    "<svg xmlns='http://www.w3.org/2000/svg' width='120' height='80' viewBox='0 0 120 80'>"
                    "<rect x='6' y='6' width='108' height='68' rx='8' fill='#1f2937' stroke='#60a5fa' stroke-width='4'/>"
                    "<text x='60' y='48' text-anchor='middle' fill='#e5e7eb' font-size='24' font-family='monospace'>CPU</text>"
                    "</svg>"
                ).encode("utf-8")
            ),
        )
    ]

    variable_names = [
        "pc",
        "halted",
        "step_requested",
        "branch_taken",
        "cmp_flag",
        "opcode_handled",
        "last_opcode",
        "status_text",
        "instr_a",
        "instr_b",
        "instr_c",
        "r0",
        "r1",
        "r2",
        "r3",
    ]
    cpu.local_variables = [SRVariable(name=name, current_value=0) for name in variable_names]
    for name in ("last_opcode", "status_text"):
        for var in cpu.local_variables:
            if var.name == name:
                var.current_value = ""

    cpu.local_lists = [
        SRList(name="prog_op", current_value=[]),
        SRList(name="prog_a", current_value=[]),
        SRList(name="prog_b", current_value=[]),
        SRList(name="prog_c", current_value=[]),
    ]

    set_reg_opcode = SRCustomBlockOpcode(
        segments=(
            "set reg",
            SRCustomBlockArgument(name="idx", type=SRCustomBlockArgumentType.STRING_NUMBER),
            "to",
            SRCustomBlockArgument(name="value", type=SRCustomBlockArgumentType.STRING_NUMBER),
        )
    )
    get_reg_opcode = SRCustomBlockOpcode(
        segments=(
            "get reg",
            SRCustomBlockArgument(name="idx", type=SRCustomBlockArgumentType.STRING_NUMBER),
        )
    )
    exec_step_opcode = SRCustomBlockOpcode(segments=("execute one step",))

    define_set_reg = block(
        "&customblocks::define custom block",
        mutation=SRCustomBlockMutation(
            custom_opcode=set_reg_opcode,
            no_screen_refresh=True,
            optype=SRCustomBlockOptype.STATEMENT,
            main_color=CB_MAIN,
            prototype_color=CB_PROTO,
            outline_color=CB_OUTLINE,
        ),
    )

    def idx_arg_for_set() -> SRBlock:
        return cb_arg_text("idx")

    def value_arg_for_set() -> SRBlock:
        return cb_arg_text("value")

    cpu.scripts.append(
        SRScript(
            position=(24, 48),
            blocks=[
                define_set_reg,
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(idx_arg_for_set(), imm_b="0"), immediate=False),
                        "THEN": SRScriptInputValue(blocks=[set_var("r0", value_arg_for_set())]),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(idx_arg_for_set(), imm_b="1"), immediate=False),
                        "THEN": SRScriptInputValue(blocks=[set_var("r1", value_arg_for_set())]),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(idx_arg_for_set(), imm_b="2"), immediate=False),
                        "THEN": SRScriptInputValue(blocks=[set_var("r2", value_arg_for_set())]),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(idx_arg_for_set(), imm_b="3"), immediate=False),
                        "THEN": SRScriptInputValue(blocks=[set_var("r3", value_arg_for_set())]),
                    },
                ),
            ],
        )
    )

    define_get_reg = block(
        "&customblocks::define custom block reporter",
        mutation=SRCustomBlockMutation(
            custom_opcode=get_reg_opcode,
            no_screen_refresh=True,
            optype=SRCustomBlockOptype.NUMBER_REPORTER,
            main_color=CB_MAIN,
            prototype_color=CB_PROTO,
            outline_color=CB_OUTLINE,
        ),
    )
    def idx_arg_for_get() -> SRBlock:
        return cb_arg_text("idx")

    cpu.scripts.append(
        SRScript(
            position=(24, 368),
            blocks=[
                define_get_reg,
                block(
                    "&control::if <CONDITION> then {THEN} else {ELSE}",
                    inputs={
                        "CONDITION": bool_in(equals(idx_arg_for_get(), imm_b="0"), immediate=False),
                        "THEN": SRScriptInputValue(blocks=[block("&customblocks::return (VALUE)", inputs={"VALUE": txt("", var_ref("r0"))})]),
                        "ELSE": SRScriptInputValue(
                            blocks=[
                                block(
                                    "&control::if <CONDITION> then {THEN} else {ELSE}",
                                    inputs={
                                        "CONDITION": bool_in(equals(idx_arg_for_get(), imm_b="1"), immediate=False),
                                        "THEN": SRScriptInputValue(blocks=[block("&customblocks::return (VALUE)", inputs={"VALUE": txt("", var_ref("r1"))})]),
                                        "ELSE": SRScriptInputValue(
                                            blocks=[
                                                block(
                                                    "&control::if <CONDITION> then {THEN} else {ELSE}",
                                                    inputs={
                                                        "CONDITION": bool_in(equals(idx_arg_for_get(), imm_b="2"), immediate=False),
                                                        "THEN": SRScriptInputValue(blocks=[block("&customblocks::return (VALUE)", inputs={"VALUE": txt("", var_ref("r2"))})]),
                                                        "ELSE": SRScriptInputValue(
                                                            blocks=[block("&customblocks::return (VALUE)", inputs={"VALUE": txt("", var_ref("r3"))})]
                                                        ),
                                                    },
                                                )
                                            ]
                                        ),
                                    },
                                )
                            ]
                        ),
                    },
                ),
            ],
        )
    )

    define_exec_one_step = block(
        "&customblocks::define custom block",
        mutation=SRCustomBlockMutation(
            custom_opcode=exec_step_opcode,
            no_screen_refresh=True,
            optype=SRCustomBlockOptype.STATEMENT,
            main_color=CB_MAIN,
            prototype_color=CB_PROTO,
            outline_color=CB_OUTLINE,
        ),
    )

    def instr_a_ref() -> SRBlock:
        return var_ref("instr_a")

    def instr_b_ref() -> SRBlock:
        return var_ref("instr_b")

    def instr_c_ref() -> SRBlock:
        return var_ref("instr_c")

    def call_get_reg_from(name: str) -> SRBlock:
        return call_custom(get_reg_opcode, {"idx": txt("0", var_ref(name))})

    loadi_then = SRScriptInputValue(
        blocks=[
            call_custom(set_reg_opcode, {"idx": txt("0", instr_a_ref()), "value": txt("0", instr_b_ref())}),
        ]
    )
    mov_then = SRScriptInputValue(
        blocks=[
            call_custom(set_reg_opcode, {"idx": txt("0", instr_a_ref()), "value": txt("0", call_get_reg_from("instr_b"))}),
        ]
    )
    add_then = SRScriptInputValue(
        blocks=[
            call_custom(
                set_reg_opcode,
                {
                    "idx": txt("0", instr_a_ref()),
                    "value": txt(
                        "0",
                        math_bin(
                            "&operators::(OPERAND1) + (OPERAND2)",
                            call_get_reg_from("instr_b"),
                            call_get_reg_from("instr_c"),
                        ),
                    ),
                },
            ),
        ]
    )
    sub_then = SRScriptInputValue(
        blocks=[
            call_custom(
                set_reg_opcode,
                {
                    "idx": txt("0", instr_a_ref()),
                    "value": txt(
                        "0",
                        math_bin(
                            "&operators::(OPERAND1) - (OPERAND2)",
                            call_get_reg_from("instr_b"),
                            call_get_reg_from("instr_c"),
                        ),
                    ),
                },
            ),
        ]
    )
    cmp_then = SRScriptInputValue(
        blocks=[
            block(
                "&control::if <CONDITION> then {THEN} else {ELSE}",
                inputs={
                    "CONDITION": bool_in(
                        equals(call_get_reg_from("instr_a"), call_get_reg_from("instr_b")),
                        immediate=False,
                    ),
                    "THEN": SRScriptInputValue(blocks=[set_var("cmp_flag", imm="1")]),
                    "ELSE": SRScriptInputValue(blocks=[set_var("cmp_flag", imm="0")]),
                },
            )
        ]
    )
    jmp_then = SRScriptInputValue(
        blocks=[
            set_var("pc", instr_a_ref()),
            set_var("branch_taken", imm="1"),
        ]
    )
    jz_then = SRScriptInputValue(
        blocks=[
            block(
                "&control::if <CONDITION> then {THEN}",
                inputs={
                    "CONDITION": bool_in(equals(var_ref("cmp_flag"), imm_b="1"), immediate=False),
                    "THEN": SRScriptInputValue(
                        blocks=[
                            set_var("pc", instr_a_ref()),
                            set_var("branch_taken", imm="1"),
                        ]
                    ),
                },
            )
        ]
    )
    halt_then = SRScriptInputValue(blocks=[set_var("halted", imm="1")])
    mul_then = SRScriptInputValue(
        blocks=[
            call_custom(
                set_reg_opcode,
                {
                    "idx": txt("0", instr_a_ref()),
                    "value": txt(
                        "0",
                        math_bin(
                            "&operators::(OPERAND1) * (OPERAND2)",
                            call_get_reg_from("instr_b"),
                            call_get_reg_from("instr_c"),
                        ),
                    ),
                },
            ),
        ]
    )
    mod_then = SRScriptInputValue(
        blocks=[
            call_custom(
                set_reg_opcode,
                {
                    "idx": txt("0", instr_a_ref()),
                    "value": txt(
                        "0",
                        math_bin(
                            "&operators::(OPERAND1) mod (OPERAND2)",
                            call_get_reg_from("instr_b"),
                            call_get_reg_from("instr_c"),
                        ),
                    ),
                },
            ),
        ]
    )
    addi_then = SRScriptInputValue(
        blocks=[
            call_custom(
                set_reg_opcode,
                {
                    "idx": txt("0", instr_a_ref()),
                    "value": txt(
                        "0",
                        math_bin(
                            "&operators::(OPERAND1) + (OPERAND2)",
                            call_get_reg_from("instr_b"),
                            instr_c_ref(),
                        ),
                    ),
                },
            ),
        ]
    )
    jnz_then = SRScriptInputValue(
        blocks=[
            block(
                "&control::if <CONDITION> then {THEN}",
                inputs={
                    "CONDITION": bool_in(equals(var_ref("cmp_flag"), imm_b="0"), immediate=False),
                    "THEN": SRScriptInputValue(
                        blocks=[
                            set_var("pc", instr_a_ref()),
                            set_var("branch_taken", imm="1"),
                        ]
                    ),
                },
            )
        ]
    )

    def with_handled(sub: SRScriptInputValue) -> SRScriptInputValue:
        return SRScriptInputValue(blocks=[*sub.blocks, set_var("opcode_handled", imm="1")])

    cpu.scripts.append(
        SRScript(
            position=(24, 732),
            blocks=[
                define_exec_one_step,
                set_var("branch_taken", imm="0"),
                set_var("opcode_handled", imm="0"),
                set_var("last_opcode", list_item_ref("prog_op", var_ref("pc"))),
                set_var("instr_a", list_item_ref("prog_a", var_ref("pc"))),
                set_var("instr_b", list_item_ref("prog_b", var_ref("pc"))),
                set_var("instr_c", list_item_ref("prog_c", var_ref("pc"))),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="LOADI"), immediate=False),
                        "THEN": with_handled(loadi_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="MOV"), immediate=False),
                        "THEN": with_handled(mov_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="ADD"), immediate=False),
                        "THEN": with_handled(add_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="SUB"), immediate=False),
                        "THEN": with_handled(sub_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="MUL"), immediate=False),
                        "THEN": with_handled(mul_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="MOD"), immediate=False),
                        "THEN": with_handled(mod_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="ADDI"), immediate=False),
                        "THEN": with_handled(addi_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="CMP"), immediate=False),
                        "THEN": with_handled(cmp_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="JMP"), immediate=False),
                        "THEN": with_handled(jmp_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="JZ"), immediate=False),
                        "THEN": with_handled(jz_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="JNZ"), immediate=False),
                        "THEN": with_handled(jnz_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("last_opcode"), imm_b="HALT"), immediate=False),
                        "THEN": with_handled(halt_then),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(equals(var_ref("opcode_handled"), imm_b="0"), immediate=False),
                        "THEN": SRScriptInputValue(
                            blocks=[
                                set_var("last_opcode", imm="ERR_UNKNOWN"),
                                set_var("halted", imm="1"),
                            ]
                        ),
                    },
                ),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(
                            block(
                                "&operators::<OPERAND1> and <OPERAND2>",
                                inputs={
                                    "OPERAND1": bool_in(equals(var_ref("branch_taken"), imm_b="0"), immediate=False),
                                    "OPERAND2": bool_in(equals(var_ref("halted"), imm_b="0"), immediate=False),
                                },
                            ),
                            immediate=False,
                        ),
                        "THEN": SRScriptInputValue(blocks=[change_var("pc", imm="1")]),
                    },
                ),
            ],
        )
    )

    init_blocks = [
        set_var("pc", imm="1"),
        set_var("halted", imm="0"),
        set_var("step_requested", imm="0"),
        set_var("branch_taken", imm="0"),
        set_var("cmp_flag", imm="0"),
        set_var("opcode_handled", imm="0"),
        set_var("last_opcode", imm=""),
        set_var("status_text", imm=""),
        set_var("instr_a", imm="0"),
        set_var("instr_b", imm="0"),
        set_var("instr_c", imm="0"),
        set_var("r0", imm="0"),
        set_var("r1", imm="0"),
        set_var("r2", imm="0"),
        set_var("r3", imm="0"),
        block("&lists::delete all of [LIST]", dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_op")}),
        block("&lists::delete all of [LIST]", dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_a")}),
        block("&lists::delete all of [LIST]", dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_b")}),
        block("&lists::delete all of [LIST]", dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_c")}),
        block("&variables::show variable [VARIABLE]", dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, "pc")}),
        block("&variables::show variable [VARIABLE]", dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, "halted")}),
        block("&variables::show variable [VARIABLE]", dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, "last_opcode")}),
        block("&variables::show variable [VARIABLE]", dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, "r0")}),
        block("&variables::show variable [VARIABLE]", dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, "r1")}),
        block("&variables::show variable [VARIABLE]", dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, "r2")}),
        block("&variables::show variable [VARIABLE]", dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, "r3")}),
        block("&variables::show variable [VARIABLE]", dropdowns={"VARIABLE": dd(DropdownValueKind.VARIABLE, "status_text")}),
        block("&lists::show list [LIST]", dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_op")}),
    ]

    program = [
        ("LOADI", "0", "9", "0"),
        ("LOADI", "1", "4", "0"),
        ("ADD", "2", "0", "1"),
        ("MOD", "3", "2", "1"),
        ("ADDI", "3", "3", "5"),
        ("CMP", "3", "0", "0"),
        ("JNZ", "9", "0", "0"),
        ("LOADI", "2", "0", "0"),
        ("MUL", "2", "1", "3"),
        ("HALT", "0", "0", "0"),
    ]
    for op, a, b, c in program:
        init_blocks.extend(
            [
                block(
                    "&lists::add (ITEM) to [LIST]",
                    inputs={"ITEM": txt(op)},
                    dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_op")},
                ),
                block(
                    "&lists::add (ITEM) to [LIST]",
                    inputs={"ITEM": txt(a)},
                    dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_a")},
                ),
                block(
                    "&lists::add (ITEM) to [LIST]",
                    inputs={"ITEM": txt(b)},
                    dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_b")},
                ),
                block(
                    "&lists::add (ITEM) to [LIST]",
                    inputs={"ITEM": txt(c)},
                    dropdowns={"LIST": dd(DropdownValueKind.LIST, "prog_c")},
                ),
            ]
        )

    cpu.scripts.append(
        SRScript(
            position=(560, 48),
            blocks=[block("&events::when green flag clicked"), *init_blocks],
        )
    )

    cpu.scripts.append(
        SRScript(
            position=(560, 450),
            blocks=[
                block(
                    "&events::when [KEY] key pressed",
                    dropdowns={"KEY": dd(DropdownValueKind.STANDARD, "space")},
                ),
                set_var("step_requested", imm="1"),
            ],
        )
    )

    cpu.scripts.append(
        SRScript(
            position=(560, 620),
            blocks=[
                block("&events::always"),
                block(
                    "&control::if <CONDITION> then {THEN}",
                    inputs={
                        "CONDITION": bool_in(
                            block(
                                "&operators::<OPERAND1> and <OPERAND2>",
                                inputs={
                                    "OPERAND1": bool_in(equals(var_ref("step_requested"), imm_b="1"), immediate=False),
                                    "OPERAND2": bool_in(equals(var_ref("halted"), imm_b="0"), immediate=False),
                                },
                            ),
                            immediate=False,
                        ),
                        "THEN": SRScriptInputValue(
                            blocks=[
                                call_custom(exec_step_opcode, {}),
                                set_var("step_requested", imm="0"),
                            ]
                        ),
                    },
                ),
            ],
        )
    )

    status_join = block(
        "&operators::join (STRING1) (STRING2)",
        inputs={
            "STRING1": txt(
                "pc=",
                block(
                    "&operators::join (STRING1) (STRING2)",
                    inputs={
                        "STRING1": txt("pc="),
                        "STRING2": txt("", var_ref("pc")),
                    },
                ),
            ),
            "STRING2": txt(
                "",
                block(
                    "&operators::join (STRING1) (STRING2)",
                    inputs={
                        "STRING1": txt(
                            "",
                            block(
                                "&operators::join (STRING1) (STRING2)",
                                inputs={
                                    "STRING1": txt(
                                        "",
                                        block(
                                            "&operators::join (STRING1) (STRING2)",
                                            inputs={
                                                "STRING1": txt(" halt="),
                                                "STRING2": txt("", var_ref("halted")),
                                            },
                                        ),
                                    ),
                                    "STRING2": txt(
                                        "",
                                        block(
                                            "&operators::join (STRING1) (STRING2)",
                                            inputs={
                                                "STRING1": txt(" r0="),
                                                "STRING2": txt("", var_ref("r0")),
                                            },
                                        ),
                                    ),
                                },
                            ),
                        ),
                        "STRING2": txt(
                            "",
                            block(
                                "&operators::join (STRING1) (STRING2)",
                                inputs={
                                    "STRING1": txt(
                                        "",
                                        block(
                                            "&operators::join (STRING1) (STRING2)",
                                            inputs={
                                                "STRING1": txt(" r1="),
                                                "STRING2": txt("", var_ref("r1")),
                                            },
                                        ),
                                    ),
                                    "STRING2": txt(
                                        "",
                                        block(
                                            "&operators::join (STRING1) (STRING2)",
                                            inputs={
                                                "STRING1": txt(
                                                    "",
                                                    block(
                                                        "&operators::join (STRING1) (STRING2)",
                                                        inputs={
                                                            "STRING1": txt(" r2="),
                                                            "STRING2": txt("", var_ref("r2")),
                                                        },
                                                    ),
                                                ),
                                                "STRING2": txt(
                                                    "",
                                                    block(
                                                        "&operators::join (STRING1) (STRING2)",
                                                        inputs={
                                                            "STRING1": txt(" r3="),
                                                            "STRING2": txt("", var_ref("r3")),
                                                        },
                                                    ),
                                                ),
                                            },
                                        ),
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
        },
    )

    cpu.scripts.append(
        SRScript(
            position=(560, 800),
            blocks=[
                block("&events::always"),
                set_var("status_text", status_join),
                block("&looks::say (MESSAGE)", inputs={"MESSAGE": txt("", var_ref("status_text"))}),
            ],
        )
    )

    project.sprites.append(cpu)
    project.sprite_layer_stack = [cpu.uuid]
    return project


def create_and_write_processor_emulator(output: str | Path = "processor_emulator.pmp") -> Path:
    """Create, validate and export the processor emulator project."""
    out = Path(output)
    project = create_processor_project()
    project.validate(AbstractTreePath(), info_api)
    fr = project.to_first(info_api)
    fr.to_file(str(out))
    return out


if __name__ == "__main__":
    out_path = create_and_write_processor_emulator("processor_emulator.pmp")
    print(f"Wrote project: {out_path.resolve()}")