# Variables & Lists
OPCODE_VAR_VALUE               = "data_variable"
OPCODE_LIST_VALUE              = "data_listcontents"
NEW_OPCODE_VAR_VALUE           = "value of [VARIABLE]"
NEW_OPCODE_LIST_VALUE          = "value of [LIST]"
ANY_OPCODE_IMMEDIATE_BLOCK     = {OPCODE_VAR_VALUE, OPCODE_LIST_VALUE}
ANY_NEW_OPCODE_IMMEDIATE_BLOCK = {NEW_OPCODE_VAR_VALUE, NEW_OPCODE_LIST_VALUE}

OPCODE_NUM_VAR_VALUE           = 12
OPCODE_NUM_LIST_VALUE          = 13
ANY_OPCODE_NUM_IMMEDIATE_BLOCK = {OPCODE_NUM_VAR_VALUE, OPCODE_NUM_LIST_VALUE}
ANY_TEXT_INPUT_NUM             = {4, 5, 6, 7, 8, 9, 10, 11}

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

# Other Special Blocks
OPCODE_STOP_SCRIPT    = "control_stop"

