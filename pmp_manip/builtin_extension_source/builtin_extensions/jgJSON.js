/* eslint-disable no-undef */
const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const noopSwitch = { isNoop: true };

/**
 * Class for JSON blocks
 * @constructor
 */
class JgJSONBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'jgJSON',
            name: 'JSON',
            color1: '#0FBD8C',
            color2: '#0EAF82',
            blocks: [
                {
                    opcode: 'json_validate',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        json: {
                            type: ArgumentType.STRING,
                            defaultValue: "{}"
                        }
                    },
                    text: 'is json [json] valid?',
                    switches: [
                        noopSwitch,
                        {
                            opcode: 'json_array_validate',
                            remapArguments: {
                                json: 'array'
                            }
                        }
                    ],
                    switchText: 'is json valid?',
                },
                "---",
                {
                    opcode: 'getValueFromJSON',
                    text: formatMessage({
                        id: 'jgJSON.blocks.getValueFromJSON',
                        default: 'get [VALUE] from [JSON]',
                        description: 'Gets a value from a JSON object.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.getValueFromJSON_value',
                                default: 'key',
                                description: 'The name of the item you want to get from the JSON.'
                            })
                        },
                        JSON: {
                            type: ArgumentType.STRING,
                            defaultValue: '{"key": "value"}'
                        }
                    },
                    switches: [
                        noopSwitch,
                        'getTreeValueFromJSON',
                        {
                            opcode: 'setValueToKeyInJSON',
                            remapArguments: {
                                VALUE: 'KEY'
                            }
                        },
                        {
                            opcode: 'json_delete',
                            remapArguments: {
                                VALUE: 'key',
                                JSON: 'json'
                            }
                        },
                    ],
                    switchText: 'get key from json'
                },
                {
                    opcode: 'getTreeValueFromJSON',
                    text: 'get path [VALUE] from [JSON]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: 'first/second'
                        },
                        JSON: {
                            type: ArgumentType.STRING,
                            defaultValue: '{"first": {"second": 2, "third": 3}}'
                        }
                    },
                    switches: [
                        'getValueFromJSON',
                        noopSwitch,
                        {
                            opcode: 'setValueToKeyInJSON',
                            remapArguments: {
                                VALUE: 'KEY'
                            }
                        },
                        {
                            opcode: 'json_delete',
                            remapArguments: {
                                VALUE: 'key',
                                JSON: 'json'
                            }
                        },
                    ],
                    switchText: 'get path from json'
                },
                {
                    opcode: 'setValueToKeyInJSON',
                    text: formatMessage({
                        id: 'jgJSON.blocks.setValueToKeyInJSON',
                        default: 'set [KEY] to [VALUE] in [JSON]',
                        description: 'Returns the JSON with the key set to the value.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_value',
                                default: 'value',
                                description: 'The value of the key you are setting.'
                            })
                        },
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_key',
                                default: 'key',
                                description: 'The key you are setting in the JSON.'
                            })
                        },
                        JSON: {
                            type: ArgumentType.STRING,
                            defaultValue: "{}"
                        }
                    },
                    switches: [
                        {
                            opcode: 'getValueFromJSON',
                            remapArguments: {
                                KEY: 'VALUE'
                            }
                        },
                        {
                            opcode: 'getTreeValueFromJSON',
                            remapArguments: {
                                KEY: 'VALUE'
                            }
                        },
                        noopSwitch,
                        {
                            opcode: 'json_delete',
                            remapArguments: {
                                KEY: 'key',
                                JSON: 'json'
                            }
                        }
                    ],
                    switchText: 'set key to value in json'
                },
                {
                    opcode: 'json_delete',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        json: {
                            type: ArgumentType.STRING,
                            defaultValue: "{}"
                        },
                        key: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_key',
                                default: 'key',
                                description: 'The key you are setting in the JSON.'
                            })
                        }
                    },
                    text: 'in json [json] delete key [key]',
                    switches: [
                        {
                            opcode: 'getValueFromJSON',
                            remapArguments: {
                                key: 'VALUE',
                                json: 'JSON'
                            }
                        },
                        {
                            opcode: 'getTreeValueFromJSON',
                            remapArguments: {
                                key: 'VALUE',
                                json: 'JSON'
                            }
                        },
                        {
                            opcode: 'setValueToKeyInJSON',
                            remapArguments: {
                                key: 'KEY',
                                json: 'JSON'
                            }
                        },
                        noopSwitch,
                    ],
                    switchText: 'in json delete key'
                },
                {
                    opcode: 'json_values',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        json: {
                            type: ArgumentType.STRING,
                            defaultValue: "{}"
                        }
                    },
                    text: 'get all values from json [json]',
                    switches: [
                        noopSwitch,
                        'json_keys',
                    ],
                    switchText: 'get all values from json',
                },
                {
                    opcode: 'json_keys',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        json: {
                            type: ArgumentType.STRING,
                            defaultValue: "{}"
                        }
                    },
                    text: 'get all keys from json [json]',
                    switches: [
                        'json_values',
                        noopSwitch,
                    ],
                    switchText: 'get all keys from json',
                },
                {
                    opcode: 'json_has',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        json: {
                            type: ArgumentType.STRING,
                            defaultValue: "{}"
                        },
                        key: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_key',
                                default: 'key',
                                description: 'The key you are setting in the JSON.'
                            })
                        }
                    },
                    text: 'json [json] has key [key]?'
                },
                {
                    opcode: 'json_combine',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        one: {
                            type: ArgumentType.STRING,
                            defaultValue: "{}"
                        },
                        two: {
                            type: ArgumentType.STRING,
                            defaultValue: "{}"
                        }
                    },
                    text: 'combine json [one] and json [two]'
                },
                {
                    blockType: BlockType.LABEL,
                    text: "Arrays"
                },
                {
                    opcode: 'json_array_validate',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[]"
                        }
                    },
                    text: 'is array [array] valid?',
                    switches: [
                        {
                            opcode: 'json_validate',
                            remapArguments: {
                                array: 'json'
                            }
                        },
                        noopSwitch,
                    ],
                    switchText: 'is array valid?',
                },
                {
                    opcode: 'json_array_split',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: "A, B, C"
                        },
                        delimeter: {
                            type: ArgumentType.STRING,
                            defaultValue: ', '
                        }
                    },
                    text: 'create an array from text [text] with delimeter [delimeter]',
                    switches: [
                        noopSwitch,
                        {
                            opcode: 'json_array_join',
                            remapArguments: {
                                text: 'array'
                            }
                        }
                    ],
                    switchText: 'create array from text'
                },
                {
                    opcode: 'json_array_join',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        delimeter: {
                            type: ArgumentType.STRING,
                            defaultValue: ', '
                        }
                    },
                    text: 'create text from array [array] with delimeter [delimeter]',
                    switches: [
                        {
                            opcode: 'json_array_split',
                            remapArguments: {
                                array: 'text'
                            }
                        },
                        noopSwitch,
                    ],
                    switchText: 'create text from array'
                },
                "---",
                {
                    opcode: 'json_array_push',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        item: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_value',
                                default: 'value',
                                description: 'The value of the key you are setting.'
                            })
                        }
                    },
                    text: 'in array [array] add [item]',
                    switches: [
                        noopSwitch,
                        'json_array_delete',
                        'json_array_insert',
                        'json_array_set',
                    ],
                    switchText: 'in array add item',
                },
                "---",
                {
                    opcode: 'json_array_concatLayer1',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array1: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        array2: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"D\", \"E\", \"F\"]"
                        }
                    },
                    text: 'add items from array [array2] to array [array1]',
                    switches: [
                        noopSwitch,
                        'json_array_concatLayer2'
                    ],
                    switchText: 'add items from array to array',
                },
                {
                    opcode: 'json_array_concatLayer2',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array1: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        array2: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"D\", \"E\", \"F\"]"
                        },
                        array3: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"G\", \"H\", \"I\"]"
                        }
                    },
                    text: 'add items from array [array2] and array [array3] to array [array1]',
                    switches: [
                        'json_array_concatLayer1',
                        noopSwitch,
                    ],
                    switchText: 'add items from array and array to array',
                },
                "---",
                {
                    opcode: 'json_array_delete',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        index: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        }
                    },
                    text: 'in array [array] delete [index]',
                    switches: [
                        'json_array_push',
                        noopSwitch,
                        'json_array_insert',
                        'json_array_set',
                    ],
                    switchText: 'in array delete index',
                },
                {
                    opcode: 'json_array_reverse',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        }
                    },
                    text: 'reverse array [array]'
                },
                {
                    opcode: 'json_array_insert',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        index: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        },
                        value: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_value',
                                default: 'value',
                                description: 'The value of the key you are setting.'
                            })
                        }
                    },
                    text: 'in array [array] insert [value] at [index]',
                    switches: [
                        'json_array_push',
                        'json_array_delete',
                        noopSwitch,
                        'json_array_set',
                    ],
                    switchText: 'in array insert value at index',
                },
                {
                    opcode: 'json_array_set',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        index: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        },
                        value: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_value',
                                default: 'value',
                                description: 'The value of the key you are setting.'
                            })
                        }
                    },
                    text: 'in array [array] set [index] to [value]',
                    switches: [
                        'json_array_push',
                        'json_array_delete',
                        'json_array_insert',
                        noopSwitch,
                    ],
                    switchText: 'in array set index to value',
                },
                "---",
                {
                    opcode: 'json_array_get',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        index: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        }
                    },
                    text: 'in array [array] get [index]',
                    switches: [
                        noopSwitch,
                        'json_array_indexofNostart',
                        {
                            opcode: 'json_array_indexof',
                            remapArguments: {
                                index: 'number',
                            },
                        },
                        {
                            opcode: 'json_array_getrange',
                            remapArguments: {
                                index: 'index1'
                            }
                        }
                    ],
                    switchText: 'in array get index',
                },
                {
                    opcode: 'json_array_indexofNostart',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        value: {
                            type: ArgumentType.STRING,
                            defaultValue: "value"
                        }
                    },
                    text: 'in array [array] get index of [value]',
                    switches: [
                        'json_array_get',
                        noopSwitch,
                        'json_array_indexof',
                        'json_array_getrange',
                    ],
                    switchText: 'in arrray get index of value',
                },
                {
                    opcode: 'json_array_indexof',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        number: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        },
                        value: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_value',
                                default: 'value',
                                description: 'The value of the key you are setting.'
                            })
                        }
                    },
                    text: 'in array [array] from [number] get index of [value]',
                    switches: [
                        {
                            opcode: 'json_array_get',
                            remapArguments: {
                                number: 'index'
                            }
                        },
                        'json_array_indexofNostart',
                        noopSwitch,
                        {
                            opcode: 'json_array_getrange',
                            remapArguments: {
                                number: 'index1'
                            }
                        }
                    ],
                    switchText: 'in array from index get index of value',
                },
                {
                    opcode: 'json_array_length',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        }
                    },
                    text: 'length of array [array]'
                },
                {
                    opcode: 'json_array_contains',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        value: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jgJSON.setValueToKeyInJSON_value',
                                default: 'value',
                                description: 'The value of the key you are setting.'
                            })
                        }
                    },
                    text: 'array [array] contains [value]?'
                },
                "---",
                {
                    opcode: 'json_array_flat',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[[\"A\", \"B\"], [\"C\", \"D\"]]"
                        },
                        layer: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    text: 'flatten nested array [array] by [layer] layers'
                },
                "---",
                {
                    opcode: 'json_array_getrange',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        },
                        index1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        },
                        index2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        }
                    },
                    text: 'in array [array] get all items from [index1] to [index2]',
                    switches: [
                        {
                            opcode: 'json_array_get',
                            remapArguments: {
                                index1: 'index'
                            }
                        },
                        'json_array_indexofNostart',
                        {
                            opcode: 'json_array_get',
                            remapArguments: {
                                index1: 'number'
                            }
                        },
                        noopSwitch
                    ],
                    switchText: 'in array get items from index to index',
                },
                "---",
                {
                    opcode: 'json_array_isempty',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        }
                    },
                    text: 'is array [array] empty?'
                },
                "---",
                {
                    opcode: 'json_array_listtoarray',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        list: {
                            type: ArgumentType.STRING,
                            defaultValue: 'select a list',
                            menu: 'lists'
                        }
                    },
                    hideFromPalette: true,
                    text: 'get contents of list [list] as array'
                },
                {
                    opcode: 'json_array_tolist',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        list: {
                            type: ArgumentType.STRING,
                            defaultValue: 'select a list',
                            menu: 'lists'
                        },
                        array: {
                            type: ArgumentType.STRING,
                            defaultValue: "[\"A\", \"B\", \"C\"]"
                        }
                    },
                    hideFromPalette: true,
                    text: 'set contents of list [list] to contents of array [array]'
                }
            ],
            menus: {
                lists: 'getAllLists'
            }
        };
    }
}

module.exports = JgJSONBlocks;
