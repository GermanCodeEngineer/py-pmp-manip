const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

function generateJoin(amount) {
    const joinWords = [
        'apple',
        'banana',
        'pear',
        'orange',
        'mango',
        'strawberry',
        'pineapple',
        'grape',
        'kiwi'
    ];

    const argumentTextArray = [];
    const argumentss = {};

    for (let i = 0; i < amount; i++) {
        argumentTextArray.push(`[STRING${i + 1}]`);
        argumentss[`STRING${i + 1}`] = {
            type: ArgumentType.STRING,
            defaultValue: joinWords[i] + ((i === (amount - 1)) ? '' : ' ')
        };
    }

    const opcode = `join${amount}`;
    const defaultText = `join ${argumentTextArray.join(' ')}`;

    return {
        opcode: opcode,
        text: Scratch.translate({ id: opcode, default: defaultText }),
        blockType: BlockType.REPORTER,
        disableMonitor: true,
        arguments: argumentss
    };
}

function generateSeveralJoins(amount) {
    const joins = [];
    for (let i = 3; i < amount; i++) {
        joins.push(generateJoin(i+1));
    }
    return joins.map((e, index) => {
        const switches = [];
        for (let i = 3; i < amount; i++) {
            if (i == index+3) {
                switches.push({ isNoop: true });
                continue;
            }
            switches.push(`join${i+1}`);
        }
        e["switchText"] = `join x${index+4}`;
        e["switches"]   = switches;
        return e;
    });
}

/**
 * Class of 2023
 * @constructor
 */
class pmOperatorsExpansion {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'pmOperatorsExpansion',
            name: 'Operators Expansion',
            color1: '#59C059',
            color2: '#46B946',
            color3: '#389438',
            isDynamic: true,
            blocks: [
                ...generateSeveralJoins(9),
                {
                    opcode: 'partOfRatio',
                    text: '[PART] part of ratio [RATIO]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        PART: {
                            type: ArgumentType.STRING,
                            menu: "part"
                        },
                        RATIO: {
                            type: ArgumentType.STRING,
                            defaultValue: "1:2"
                        }
                    },
                    switches: [
                        { isNoop: true },
                        'simplifyRatio'
                    ],
                    switchText: 'part of ratio'
                },
                {
                    opcode: 'simplifyRatio',
                    text: 'simplify ratio [RATIO]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        RATIO: {
                            type: ArgumentType.STRING,
                            defaultValue: "1:2"
                        }
                    },
                    switches: [
                        'partOfRatio',
                        { isNoop: true }
                    ],
                    switchText: 'simplify ratio'
                },
                {
                    opcode: 'pi',
                    text: 'π',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    switches: [
                        { isNoop: true },
                        'euler',
                        'infinity'
                    ]
                },
                {
                    opcode: 'euler',
                    text: 'e',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    switches: [
                        'pi',
                        { isNoop: true },
                        'infinity'
                    ]
                },
                {
                    opcode: 'infinity',
                    text: '∞',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    switches: [
                        'pi',
                        'euler',
                        { isNoop: true }
                    ]
                },
                {
                    opcode: 'truncateNumber',
                    text: 'truncate number [NUM]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        NUM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "2.5"
                        }
                    }
                },
                {
                    opcode: 'isNumberMultipleOf',
                    text: 'is [NUM] multiple of [MULTIPLE]?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    arguments: {
                        NUM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "20"
                        },
                        MULTIPLE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "10"
                        }
                    },
                    switches: [
                        { isNoop: true },
                        'isInteger',
                        'isPrime',
                        'isEven'
                    ],
                    switchText: 'is multiple of?'
                },
                {
                    opcode: 'isInteger',
                    text: 'is [NUM] an integer?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    arguments: {
                        NUM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0.5"
                        }
                    },
                    switches: [
                        'isNumberMultipleOf',
                        { isNoop: true },
                        'isPrime',
                        'isEven'
                    ],
                    switchText: 'is integer?'
                },
                {
                    opcode: 'isPrime',
                    text: 'is [NUM] a prime number?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    arguments: {
                        NUM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "13"
                        }
                    },
                    switches: [
                        'isNumberMultipleOf',
                        'isInteger',
                        { isNoop: true },
                        'isEven'
                    ],
                    switchText: 'is prime?'
                },
                {
                    opcode: 'isEven',
                    text: 'is [NUM] even?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    arguments: {
                        NUM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "4"
                        }
                    },
                    switches: [
                        'isNumberMultipleOf',
                        'isInteger',
                        'isPrime',
                        { isNoop: true }
                    ],
                    switchText: 'is even?'
                },
                {
                    opcode: 'reverseChars',
                    text: 'reverse [TEXT]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello!"
                        }
                    },
                    switches: [
                        { isNoop: true },
                        'shuffleChars'
                    ],
                    switchText: 'reverse text'
                },
                {
                    opcode: 'shuffleChars',
                    text: 'shuffle [TEXT]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello!"
                        }
                    },
                    switches: [
                        'reverseChars',
                        { isNoop: true },
                    ],
                    switchText: 'shuffle text'
                },
                {
                    opcode: 'exactlyEqual',
                    text: '[ONE] exactly equals [TWO]?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    arguments: {
                        ONE: {
                            type: ArgumentType.STRING,
                            defaultValue: "a"
                        },
                        TWO: {
                            type: ArgumentType.STRING,
                            defaultValue: "b"
                        }
                    },

                },
                {
                    opcode: 'betweenNumbers',
                    text: 'is [NUM] between [MIN] and [MAX]?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    arguments: {
                        NUM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 5
                        },
                        MIN: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        MAX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 10
                        }
                    }
                },
                {
                    opcode: 'evaluateMath',
                    text: 'answer to [EQUATION]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        EQUATION: {
                            type: ArgumentType.STRING,
                            defaultValue: "5 * 2"
                        }
                    }
                },
                {
                    opcode: 'setReplacer',
                    text: 'set replacer [REPLACER] to [TEXT]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        REPLACER: {
                            type: ArgumentType.STRING,
                            defaultValue: "${replacer}"
                        },
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "world"
                        }
                    },
                    switches: [
                        { isNoop: true },
                        'resetReplacers'
                    ],
                    switchText: 'set replacer'
                },
                {
                    opcode: 'resetReplacers',
                    text: 'reset replacers',
                    blockType: BlockType.COMMAND,
                    switches: [
                        'setReplacer',
                        { isNoop: true }
                    ],
                    switchText: 'reset replacers'
                },
                {
                    opcode: 'applyReplacers',
                    text: 'apply replacers to [TEXT]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello ${replacer}!"
                        }
                    }
                },
                {
                    opcode: 'textAfter',
                    text: 'text after [TEXT] in [BASE]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello"
                        },
                        BASE: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello world!"
                        }
                    },
                    switches: [
                        { isNoop: true },
                        'textBefore'
                    ],
                    switchText: 'text after'
                },
                {
                    opcode: 'textBefore',
                    text: 'text before [TEXT] in [BASE]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "world"
                        },
                        BASE: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello world!"
                        }
                    },
                    switches: [
                        'textAfter',
                        { isNoop: true }
                    ],
                    switchText: 'text before'
                },
                {
                    opcode: 'shiftLeft',
                    text: '[num1] << [num2]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        num1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        },
                        num2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "5"
                        }
                    },
                    switches: [
                        { isNoop: true },
                        'shiftRight',
                        'binnaryAnd',
                        'binnaryOr',
                        'binnaryXor',
                        'binnaryNot',
                    ],
                    switchText: 'lshift'
                },
                {
                    opcode: 'shiftRight',
                    text: '[num1] >> [num2]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        num1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "32"
                        },
                        num2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "5"
                        }
                    },
                    switches: [
                        'shiftLeft',
                        { isNoop: true },
                        'binnaryAnd',
                        'binnaryOr',
                        'binnaryXor',
                        'binnaryNot',
                    ],
                    switchText: 'rshift'
                },
                {
                    opcode: 'binnaryAnd',
                    text: '[num1] & [num2]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        num1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "32"
                        },
                        num2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "5"
                        }
                    },
                    switches: [
                        'shiftLeft',
                        'shiftRight',
                        { isNoop: true },
                        'binnaryOr',
                        'binnaryXor',
                        'binnaryNot',
                    ],
                    switchText: 'and'
                },
                {
                    opcode: 'binnaryOr',
                    text: '[num1] | [num2]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        num1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "7"
                        },
                        num2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "8"
                        }
                    },
                    switches: [
                        'shiftLeft',
                        'shiftRight',
                        'binnaryAnd',
                        { isNoop: true },
                        'binnaryXor',
                        'binnaryNot',
                    ],
                    switchText: 'or'
                },
                {
                    opcode: 'binnaryXor',
                    text: '[num1] ^ [num2]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        num1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "7"
                        },
                        num2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "2"
                        }
                    },
                    switches: [
                        'shiftLeft',
                        'shiftRight',
                        'binnaryAnd',
                        'binnaryOr',
                        { isNoop: true },
                        'binnaryNot',
                    ],
                    switchText: 'xor'
                },
                {
                    opcode: 'binnaryNot',
                    text: '~ [num1]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        num1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "2"
                        }
                    },
                    switches: [
                        'shiftLeft',
                        'shiftRight',
                        'binnaryAnd',
                        'binnaryOr',
                        'binnaryXor',
                        { isNoop: true }
                    ],
                    switchText: 'not'
                },
                {
                    opcode: 'speedToPitch',
                    text: 'speed [SPEED] to pitch',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        SPEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "2"
                        },
                    },
                    switches: [
                        { isNoop: true },
                        {
                            opcode: 'pitchToSpeed',
                            remapArguments: {
                                SPEED: 'PITCH'
                            }
                        }
                    ],
                    switchText: 'speed to pitch'
                },
                {
                    opcode: 'pitchToSpeed',
                    text: 'pitch [PITCH] to speed',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        PITCH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "120"
                        },
                    },
                    switches: [
                        {
                            opcode: 'speedToPitch',
                            remapArguments: {
                                PITCH: 'SPEED'
                            }
                        },
                        { isNoop: true },
                    ],
                    switchText: 'pitch to speed'
                },
                {
                    opcode: 'orIfFalsey',
                    text: '[ONE] or else [TWO]',
                    blockType: BlockType.REPORTER,
                    allowDropAnywhere: true,
                    disableMonitor: true,
                    arguments: {
                        ONE: {
                            type: ArgumentType.STRING,
                            defaultValue: "a"
                        },
                        TWO: {
                            type: ArgumentType.STRING,
                            defaultValue: "b"
                        }
                    }
                },
                {
                    opcode: 'ifIsTruthy',
                    text: 'if [ONE] is true then [TWO]',
                    blockType: BlockType.REPORTER,
                    allowDropAnywhere: true,
                    disableMonitor: true,
                    arguments: {
                        ONE: {
                            type: ArgumentType.BOOLEAN
                        },
                        TWO: {
                            type: ArgumentType.STRING,
                            defaultValue: "perfect!"
                        }
                    }
                },
                {
                    opcode: 'atan2',
                    text: 'atan2 of x [X] y [Y]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "45"
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "90"
                        },
                    }
                },
                {
                    opcode: 'operator_nand',
                    ppm_final_opcode: true,
                    text: '[OPERAND1] nand [OPERAND2]',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        OPERAND1: {type: ArgumentType.BOOLEAN},
                        OPERAND2: {type: ArgumentType.BOOLEAN},
                    }
                },
                {
                    opcode: 'operator_nor',
                    ppm_final_opcode: true,
                    text: '[OPERAND1] nor [OPERAND2]',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        OPERAND1: {type: ArgumentType.BOOLEAN},
                        OPERAND2: {type: ArgumentType.BOOLEAN},
                    }
                },
                {
                    opcode: 'operator_xor',
                    ppm_final_opcode: true,
                    text: '[OPERAND1] xor [OPERAND2]',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        OPERAND1: {type: ArgumentType.BOOLEAN},
                        OPERAND2: {type: ArgumentType.BOOLEAN},
                    }
                },
                {
                    opcode: 'operator_xnor',
                    ppm_final_opcode: true,
                    text: '[OPERAND1] xnor [OPERAND2]',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        OPERAND1: {type: ArgumentType.BOOLEAN},
                        OPERAND2: {type: ArgumentType.BOOLEAN},
                    }
                },
                {
                    opcode: 'operator_randomBoolean',
                    ppm_final_opcode: true,
                    text: 'random',
                    blockType: BlockType.BOOLEAN,
                },
                {
                    opcode: 'operator_countAppearTimes',
                    ppm_final_opcode: true,
                    text: 'amount of times [TEXT1] appears in [TEXT2]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: "a",
                        },
                        TEXT2: {
                            type: ArgumentType.STRING,
                            defaultValue: "abc abc abc",
                        },
                    },
                },
                {
                    opcode: 'operator_readLineInMultilineText',
                    ppm_final_opcode: true,
                    text: 'read line [LINE] in [TEXT]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        LINE: {
                            type: ArgumentType.STRING,
                            defaultValue: "1",
                        },
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Text with multiple lines here",
                        },
                    },
                },
                {
                    opcode: 'operator_textIncludesLetterFrom',
                    ppm_final_opcode: true,
                    text: '[TEXT1] includes a letter from [TEXT2] ?',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: "abcdef",
                        },
                        TEXT2: {
                            type: ArgumentType.STRING,
                            defaultValue: "fgh",
                        },
                    },
                },
                {
                    opcode: 'operator_character_to_code',
                    ppm_final_opcode: true,
                    text: 'character [ONE] to id',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.STRING,
                            defaultValue: "a",
                        },
                    },
                },
                {
                    opcode: 'operator_character_to_code',
                    ppm_final_opcode: true,
                    text: 'character [ONE] to id',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.STRING,
                            defaultValue: "a",
                        },
                    },
                },
                {
                    opcode: 'operator_code_to_character',
                    ppm_final_opcode: true,
                    text: 'id [ONE] to character',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.STRING,
                            defaultValue: "97",
                        },
                    },
                },
            ],
            menus: {
                part: {
                    acceptReporters: true,
                    items: [
                        "first",
                        "last"
                    ].map(item => ({ text: item, value: item }))
                }
            }
        };
    }
}

module.exports = pmOperatorsExpansion;
