from pmp_manip.core.block import get_input_cls_for_input_mode
from pmp_manip.utility    import (
    enforce_argument_types, get_closest_matches,
    MANIP_UnknownOpcodeError,
)


from pmp_manip.important_consts import (
    OPCODE_STOP_SCRIPT, OPCODE_POLYGON, OPCODE_CB_CALL,
    OPCODE_EXPANDABLE_IF, OPCODE_EXPANDABLE_MATH,
)
from pmp_manip.opcode_info.api import (
    OpcodeInfoAPI, OpcodeInfo, OpcodeType,
    BuiltinInputType, InputType, BuiltinDropdownType, DropdownType,
    DropdownValueRule,
)


TAB = 4 * " "


def _repo_link(file: str, section: str) -> str:
    """
    Get a link to a section in a md file in the project's github.
    """
    return f"https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/{file}#{section}"

def _inputsrcls_link(input_type: InputType) -> str:
    """
    Get a link to the class of an input in the project documentation.
    """
    input_cls = get_input_cls_for_input_mode(input_type.mode).__name__
    return f"[`{input_cls}`]({_repo_link("docs/second_repr.md", section=input_cls)})"

def _generate_possible_values_string(dropdown_type: DropdownType) -> str:
    """
    Generate a string of values possible for a type of dropdown.
    """
    if DropdownValueRule.EXTENSION_UNPREDICTABLE in dropdown_type.type_info.rules:
        return "Unpredictable. Calculated by extension at runtime in PM-Editor."
    else:
        possible_values = dropdown_type.guess_possible_new_dropdown_values(include_rules=True)
        return (
            "No guessed possible values" if possible_values == [] else
            "".join([f"\n{TAB}{TAB}* `SRDropdownValue{value!r}`" for value in possible_values])
        )

def _generate_inputs_section(old_opcode: str, opcode_namespace: str, opcode_info: OpcodeInfo) -> str:
    """
    Generate inputs section of documentation about a block in Markdown(md) format.
    
    Args:
        old_opcode: the old opcode i.e. kind of block
        opcode_namespace: category/extension of the opcode
        opcode_info: information about that opcode from the OpcodeInfoAPI
    """
    inputs_descr = "### Inputs\n"
    # Iterate directly without api call, special cases are handled manually
    for new_input_id, input_info in opcode_info.inputs.items_key2():
        input_type: InputType = input_info.type
        input_descr = (
            TAB+f"* type: **{input_type.name}**"+
            ("\n" if isinstance(input_type, BuiltinInputType)
            else f" from {opcode_namespace} extension\n")+
            TAB+f"* SR-Class: {_inputsrcls_link(input_type)}\n"
        )
        if input_info.menu is not None:
            input_descr += (
                TAB+"* possible values for `.dropdown`:"+
                _generate_possible_values_string(input_type.corresponding_dropdown_type)+"\n"
            )
        inputs_descr += f"* `{new_input_id}`\n{input_descr}"
    if   old_opcode == OPCODE_CB_CALL:
        inputs_descr += (
            "Depends on the inputs of the custom block to call.\n"+
            "* all inputs\n"+
            TAB+"* type: **TEXT** or **BOOLEAN**\n"+
            TAB+f"* SR-Class: {_inputsrcls_link(BuiltinInputType.TEXT)}\n"
        )
    elif old_opcode == OPCODE_POLYGON:
        inputs_descr += (
            "Depends on how many coordinate pairs the parent block expects. "+
            "format of keys: `X1`...`Xn`, `Y1`...`Yn`\n"+
            "* `X1`...`Xn`\n"+
            # SPECIAL_NUMBER is essentially the same, the user does not care
            TAB+"* type: **NUMBER**\n"+ 
            TAB+f"* SR-Class: {_inputsrcls_link(BuiltinInputType.NUMBER)}\n"
            "* `Y1`...`Yn`\n"+
            TAB+"* type: **NUMBER**\n"+ 
            TAB+f"* SR-Class: {_inputsrcls_link(BuiltinInputType.NUMBER)}\n"
        )
    elif old_opcode == OPCODE_EXPANDABLE_IF:
        inputs_descr += (
            "Depends on how many branches the block has. "+
            "format of keys: `CONDITION1`...`CONDITIONn`, `THEN1`...`THENn`, `ELSE` if it has an else branch\n"+
            "* `CONDITION1`...`CONDITIONn`\n"+
            TAB+"* type: **BOOLEAN**\n"+ 
            TAB+f"* SR-Class: {_inputsrcls_link(BuiltinInputType.BOOLEAN)}\n"
            "* `THEN1`...`THENn`\n"+
            TAB+"* type: **SCRIPT**\n"+ 
            TAB+f"* SR-Class: {_inputsrcls_link(BuiltinInputType.SCRIPT)}\n"
            "* (`ELSE`)\n"+
            TAB+"* type: **SCRIPT**\n"+ 
            TAB+f"* SR-Class: {_inputsrcls_link(BuiltinInputType.SCRIPT)}\n"
        )
    elif old_opcode == OPCODE_EXPANDABLE_MATH:
        inputs_descr += (
            "Depends on how many operations the block does. "+
            "format of keys: `OPERAND1`...`OPERANDn`\n"+
            "* `OPERAND1`...`OPERANDn`\n"+
            TAB+"* type: **NUMBER**\n"+ 
            TAB+f"* SR-Class: {_inputsrcls_link(BuiltinInputType.NUMBER)}\n"
        )
    if inputs_descr.count("\n") == 1:
        inputs_descr = "### Inputs: /\n"
    return inputs_descr

def _generate_block_shape_section(old_opcode: str, opcode_type: OpcodeType) -> str:
    """
    Generate block shape section of documentation about a block in Markdown(md) format.
    
    Args:
        old_opcode: the old opcode i.e. kind of block
        opcode_type: information about the block shape
    """
    if   old_opcode == OPCODE_STOP_SCRIPT:
        block_shape_descr = "* Flexible. Can be **ENDING_STATEMENT or STATEMENT** depending on the menu dropdown.\n"
    elif old_opcode == OPCODE_CB_CALL:
        block_shape_descr = "* Flexible. Can be **STATEMENT, ENDING_STATEMENT, STRING_REPORTER, NUMBER_REPORTER, BOOLEAN_REPORTER** matches the shape of the custom block to call.\n"
    else:
        block_shape_descr = ""
    
    return (
        "### Block Shape\n"+
        f"* [**{opcode_type.name}**]({_repo_link('docs/block_shape.md', section=opcode_type.name)})\n"+
        block_shape_descr
    )

@enforce_argument_types
def generate_opcode_doc(info_api: OpcodeInfoAPI, new_opcode: str) -> str:
    """
    Generate documentation about a block opcode in Markdown(md) format including shape, inputs, dropdowns, mutation and monitor.
    
    Args:
        info_api: the opcode info api used to fetch information about opcodes
        new_opcode: the new opcode i.e. kind of block
    
    Raises:
        MANIP_UnknownOpcodeError: if an undefined new opcode is passed
    """
    opcode_info = info_api.get_info_by_new_safe(new_opcode)
    if opcode_info is None:
        closest_matches = get_closest_matches(new_opcode, info_api.all_new, n=10)
        msg = (
            f"Unknown new opcode {new_opcode!r}. Did you forget to add an extension? "
            f"The closest matches are: \n  - "+"\n  - ".join([repr(m) for m in closest_matches])
        )
        raise MANIP_UnknownOpcodeError(msg)
    old_opcode = info_api.get_old_by_new(new_opcode)
    opcode_namespace, opcode_text = new_opcode.removeprefix("&").split("::")

    dropdowns_descr = "### Dropdowns\n"
    for new_dropdown_id, dropdown_info in opcode_info.get_new_dropdown_ids_infos().items():
        dropdown_type: DropdownType = dropdown_info.type
        if dropdown_type is BuiltinDropdownType.EDITOR_BUTTON:
            continue
        dropdown_descr = (
            TAB+f"* type: **{dropdown_type.name}**"+
            ("\n" if isinstance(dropdown_type, BuiltinDropdownType)
            else f" from {opcode_namespace} extension\n")+
            TAB+"* possible values: "+
            _generate_possible_values_string(dropdown_type)
        )
        dropdowns_descr += f"* `{new_dropdown_id}`\n{dropdown_descr}\n"
    if dropdowns_descr.count("\n") == 1:
        dropdowns_descr = "### Dropdowns: /\n"

    if opcode_info.new_mutation_cls:
        mutation_cls = opcode_info.new_mutation_cls.__name__
        mutation_descr = (
            "### Mutation\n"+
            f"An instance of [`{mutation_cls}`]({_repo_link('docs/second_repr.md', section=mutation_cls)}).\n"
        )
    else:
        mutation_descr = "### Mutation: /\n"
    
    if opcode_info.can_have_monitor:
        monitor_descr = (
            "### Monitor\n"+
            f"[Monitors]({_repo_link('docs/second_repr.md', section='SRMonitor')}) with this opcode can exist.\n"
        )
    else:
        monitor_descr = "### Monitor: /\n"

    return (
        f"## Documentation for opcode `{opcode_text}`({opcode_namespace})\n"+
        _generate_block_shape_section(old_opcode, opcode_info.opcode_type)+
        _generate_inputs_section(old_opcode, opcode_namespace, opcode_info)+
        dropdowns_descr+
        mutation_descr+
        monitor_descr
    )


__all__ = ["generate_opcode_doc"]

