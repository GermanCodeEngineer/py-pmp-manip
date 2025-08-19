from pmp_manip.opcode_info.data_imports import *

ext_pm_json = OpcodeInfoGroup(name="pm_json", opcode_info=DualKeyDict({
    ("jgJSON_json_validate", "is json (JSON) valid?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("json", "JSON"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_getValueFromJSON", "get (KEY) from (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("VALUE", "KEY"): InputInfo(BuiltinInputType.TEXT),
            ("JSON", "JSON"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_getTreeValueFromJSON", "get path (PATH) from (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("VALUE", "PATH"): InputInfo(BuiltinInputType.TEXT),
            ("JSON", "JSON"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_setValueToKeyInJSON", "set (KEY) to (VALUE) in (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("KEY", "KEY"): InputInfo(BuiltinInputType.TEXT),
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
            ("JSON", "JSON"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_delete", "in json (JSON) delete key (KEY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("key", "KEY"): InputInfo(BuiltinInputType.TEXT),
            ("json", "JSON"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_values", "get all values from json (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("json", "JSON"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_keys", "get all keys from json (JSON)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("json", "JSON"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_has", "json (JSON) has key (KEY) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("json", "JSON"): InputInfo(BuiltinInputType.TEXT),
            ("key", "KEY"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_combine", "combine json (JSON1) and json (JSON2)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("one", "JSON1"): InputInfo(BuiltinInputType.TEXT),
            ("two", "JSON2"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_validate", "is array (ARRAY) valid?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_split", "create an array from text (TEXT) with delimeter (DELIMETER)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("text", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("delimeter", "DELIMETER"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_join", "create text from array (ARRAY) with delimeter (DELIMETER)"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("delimeter", "DELIMETER"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_push", "in array (ARRAY) add (ITEM)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("item", "ITEM"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_concatLayer1", "add items from array (SOURCEARRAY) to array (TARGETARRAY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array2", "SOURCEARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("array1", "TARGETARRAY"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_concatLayer2", "add items from array (SOURCEARRAY1) and array (SOURCEARRAY2) to array (TARGETARRAY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array2", "SOURCEARRAY1"): InputInfo(BuiltinInputType.TEXT),
            ("array3", "SOURCEARRAY2"): InputInfo(BuiltinInputType.TEXT),
            ("array1", "TARGETARRAY"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_delete", "in array (ARRAY) delete (INDEX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("index", "INDEX"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_reverse", "reverse array (ARRAY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_insert", "in array (ARRAY) insert (VALUE) at (INDEX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("value", "VALUE"): InputInfo(BuiltinInputType.TEXT),
            ("index", "INDEX"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_set", "in array (ARRAY) set (INDEX) to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("index", "INDEX"): InputInfo(BuiltinInputType.NUMBER),
            ("value", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_get", "in array (ARRAY) get (INDEX)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("index", "INDEX"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_indexofNostart", "in array (ARRAY) get index of (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("value", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_indexof", "in array (ARRAY) from (START) get index of (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("number", "START"): InputInfo(BuiltinInputType.NUMBER),
            ("value", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_length", "length of array (ARRAY)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_contains", "array (ARRAY) contains (VALUE) ?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("value", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("jgJSON_json_array_flat", "flatten nested array (ARRAY) by (LAYERS) layers"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("layer", "LAYERS"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_getrange", "in array (ARRAY) get all items from (START) to (STOP)"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
            ("index1", "START"): InputInfo(BuiltinInputType.NUMBER),
            ("index2", "STOP"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("jgJSON_json_array_isempty", "is array (ARRAY) empty?"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("array", "ARRAY"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

}))