# Variables & Lists
OPCODE_VAR_VALUE      = "data_variable"
OPCODE_LIST_VALUE     = "data_listcontents"
NEW_OPCODE_VAR_VALUE  = "value of [VARIABLE]"
NEW_OPCODE_LIST_VALUE = "value of [LIST]"
OPCODE_VAR_VALUE_NUM  = 12
OPCODE_LIST_VALUE_NUM = 13

# Custom Block Definitions
OPCODE_CB_DEF         = "procedures_definition"
OPCODE_CB_DEF_RET     = "procedures_definition_return"
ANY_OPCODE_CB_DEF     =  {OPCODE_CB_DEF, OPCODE_CB_DEF_RET}

OPCODE_CB_PROTOTYPE   = "procedures_prototype"

OPCODE_CB_ARG_TEXT    = "argument_reporter_string_number"
OPCODE_CB_ARG_BOOL    = "argument_reporter_boolean"
ANY_OPCODE_CB_ARG     = {OPCODE_CB_ARG_TEXT, OPCODE_CB_ARG_BOOL}

NEW_OPCODE_CB_DEF     = "define custom block"
NEW_OPCODE_CB_DEF_REP = "define custom block reporter"
ANY_NEW_OPCODE_CB_DEF = {NEW_OPCODE_CB_DEF, NEW_OPCODE_CB_DEF_REP}

# Custom Block Calls
OPCODE_CB_CALL        = "procedures_call"
NEW_OPCODE_CB_CALL    = "call custom block"