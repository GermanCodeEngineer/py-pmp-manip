from pypenguin.opcode_info.data_imports import *

pm_json = OpcodeInfoGroup(name="pm_json", opcode_info=DualKeyDict({
    ("jgJSON_json_validate", "is json (JSON) valid?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("json", "JSON"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_getValueFromJSON", "get (KEY) from (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("VALUE", "KEY"): InputInfo(InputType.TEXT),
            ("JSON", "JSON"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_getTreeValueFromJSON", "get path (PATH) from (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("VALUE", "PATH"): InputInfo(InputType.TEXT),
            ("JSON", "JSON"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_setValueToKeyInJSON", "set (KEY) to (VALUE) in (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("KEY", "KEY"): InputInfo(InputType.TEXT),
            ("VALUE", "VALUE"): InputInfo(InputType.TEXT),
            ("JSON", "JSON"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_delete", "in json (JSON) delete key (KEY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("key", "KEY"): InputInfo(InputType.TEXT),
            ("json", "JSON"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_values", "get all values from json (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("json", "JSON"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_keys", "get all keys from json (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("json", "JSON"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_has", "json (JSON) has key (KEY) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("json", "JSON"): InputInfo(InputType.TEXT),
            ("key", "KEY"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_combine", "combine json (JSON1) and json (JSON2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("one", "JSON1"): InputInfo(InputType.TEXT),
            ("two", "JSON2"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_validate", "is array (ARRAY) valid?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_split", "create an array from text (TEXT) with delimeter (DELIMETER)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(InputType.TEXT),
            ("delimeter", "DELIMETER"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_join", "create text from array (ARRAY) with delimeter (DELIMETER)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("delimeter", "DELIMETER"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_push", "in array (ARRAY) add (ITEM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("item", "ITEM"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_concatLayer1", "add items from array (SOURCEARRAY) to array (TARGETARRAY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array2", "SOURCEARRAY"): InputInfo(InputType.TEXT),
            ("array1", "TARGETARRAY"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_concatLayer2", "add items from array (SOURCEARRAY1) and array (SOURCEARRAY2) to array (TARGETARRAY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array2", "SOURCEARRAY1"): InputInfo(InputType.TEXT),
            ("array3", "SOURCEARRAY2"): InputInfo(InputType.TEXT),
            ("array1", "TARGETARRAY"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_delete", "in array (ARRAY) delete (INDEX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("index", "INDEX"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_reverse", "reverse array (ARRAY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_insert", "in array (ARRAY) insert (VALUE) at (INDEX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("value", "VALUE"): InputInfo(InputType.TEXT),
            ("index", "INDEX"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_set", "in array (ARRAY) set (INDEX) to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("index", "INDEX"): InputInfo(InputType.NUMBER),
            ("value", "VALUE"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_get", "in array (ARRAY) get (INDEX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("index", "INDEX"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_indexofNostart", "in array (ARRAY) get index of (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("value", "VALUE"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_indexof", "in array (ARRAY) from (START) get index of (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("number", "START"): InputInfo(InputType.NUMBER),
            ("value", "VALUE"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_length", "length of array (ARRAY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_contains", "array (ARRAY) contains (VALUE) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("value", "VALUE"): InputInfo(InputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_flat", "flatten nested array (ARRAY) by (LAYERS) layers"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("layer", "LAYERS"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_getrange", "in array (ARRAY) get all items from (START) to (STOP)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
            ("index1", "START"): InputInfo(InputType.NUMBER),
            ("index2", "STOP"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_isempty", "is array (ARRAY) empty?"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(InputType.TEXT),
        }),
    ),

}))