const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

//const blockIconURI = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAAFACAMAAAD6TlWYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAPUExURQAAAP+xNQDiGgCU/wAAAJEQGGoAAAAFdFJOU/////8A+7YOUwAAAAlwSFlzAAAOwwAADsMBx2+oZAAABA5JREFUeF7t0EtuW0EUA9F8vP81Z8JRAwzbLuk5COoMBb1LdP34EGJAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEHos4M+HZfbtDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0KPBfxfGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEZsBfh/z8z/r9SfnsywwIGRAyIGRAyICQASEDQp8OeMrfvk06vEzOXjPgIWevGfCQs9cMeMjZawY85Ow1Ax5y9poBDzl7zYCHnL2GA57y2dvlvW+TmcmARWYmAxaZmQxYZGYyYJGZyYBFZiYDFpmZDFhkZnp5wFPOvFze+TaZmQxYZGYyYJGZyYBFZiYDFpmZDFhkZjJgkZnJgEVmprcHPOXsl+V9j8lsZcAhs5UBh8xWBhwyWxlwyGxlwCGzlQGHzFYGHDJbPR7wlJlreddjMlsZcMhsZcAhs5UBh8xWBhwyWxlwyGxlwCGzlQGHzFbfHvCU2SrvekxmKwMOma0MOGS2MuCQ2cqAQ2YrAw6ZrQw4ZLYy4JDZyoBDZisDDpmtDDhktjLgkNnKgENmKwMOma0MOGS2MuCQ2erbA2bmWt71mMxWBhwyWxlwyGxlwCGzlQGHzFYGHDJbGXDIbGXAIbPV4wFz9svyrsdktjLgkNnKgENmKwMOma0MOGS2MuCQ2cqAQ2YrAw6Zrd4eMGdeLu97m8xMBiwyMxmwyMxkwCIzkwGLzEwGLDIzGbDIzGTAIjPTywPms7fLO98mM5MBi8xMBiwyMxmwyMxkwCIzkwGLzEwGLDIzGbDIzIQD5m/fJu99mZy9ZsBDzl4z4CFnrxnwkLPXDHjI2WsGPOTsNQMecvaaAQ85e+3TAfPzPysdruWzLzMgZEDIgJABIQNCBoQMCM2A+jsDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgMjHxx+IPExM0h8siAAAAABJRU5ErkJggg=="

/**
 * Class for Blocky2 blocks
 * @constructor
 */
class Blockly2Math {
    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'blockly2math',
            name: 'Math',
            //blockIconURI: blockIconURI,
            color1: '#5b67a5',
            color2: '#444d7c',
            blocks: [
                {
                    opcode: 'Number',
                    text: formatMessage({
                        id: 'blockly2math.blocks.Number',
                        default: '[NUMBER]',
                        description: 'Define a number'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        NUMBER: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        }
                    }
                },
                {
                    opcode: 'Operation',
                    text: formatMessage({
                        id: 'blockly2math.blocks.Operation',
                        default: '[ONE][OP][TWO]',
                        description: 'Perform a basic math operation'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        OP: {
                            type: ArgumentType.STRING,
                            defaultValue: "+",
                            menu: "Operation"
                        },
                        TWO: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    }
                },
                {
                    opcode: 'AdvancedOperation',
                    text: formatMessage({
                        id: 'blockly2math.blocks.AdvancedOperation',
                        default: '[OP][ONE]',
                        description: 'Perform a advanced math operation'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        OP: {
                            type: ArgumentType.STRING,
                            defaultValue: "square root",
                            menu: "AdvancedOperation"
                        },
                    }
                },
                {
                    opcode: 'Function',
                    text: formatMessage({
                        id: 'blockly2math.blocks.Function',
                        default: '[OP][ONE]',
                        description: 'Perform a math function'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        OP: {
                            type: ArgumentType.STRING,
                            defaultValue: "sin",
                            menu: "Function"
                        },
                    }
                },
                {
                    opcode: 'Constant',
                    text: formatMessage({
                        id: 'blockly2math.blocks.Constant',
                        default: '[CONST]',
                        description: 'Retrieve a constant'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        CONST: {
                            type: ArgumentType.STRING,
                            defaultValue: "π",
                            menu: "Constant"
                        },
                    }
                },
                {
                    opcode: 'IsOption',
                    text: formatMessage({
                        id: 'blockly2math.blocks.IsOption',
                        default: '[ONE] is [OPTION]?',
                        description: 'Check if number match condition'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        ONE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        OPTION: {
                            type: ArgumentType.STRING,
                            defaultValue: "even",
                            menu: "IsOption"
                        },
                    }
                },
                {
                    opcode: 'IsOption2',
                    text: formatMessage({
                        id: 'blockly2math.blocks.IsOption2',
                        default: '[ONE] is [OPTION] [TWO]?',
                        description: 'Check if numbers match condition'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        ONE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        TWO: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        OPTION: {
                            type: ArgumentType.STRING,
                            defaultValue: "even",
                            menu: "IsOption2"
                        },
                    }
                },
            ],
            menus: {
                Operation: [
                    "+",
                    "-",
                    "×",
                    "÷",
                    "^"
                ],
                AdvancedOperation: [
                    "square root",
                    "absolute",
                    "-",
                    "ln",
                    "log10",
                    "e^",
                    "10^"
                ],
                Function: [
                    "sin",
                    "cos",
                    "tan",
                    "asin",
                    "acos",
                    "atan"
                ],
                Constant: [
                    "π",
                    "e",
                    "φ",
                    "sqrt(2)",
                    "sqrt(½)",
                    "∞"
                ],
                IsOption: [
                    "even",
                    "odd",
                    "prime",
                    "whole",
                    "positive",
                    "negative",
                ],
                IsOption2: [
                    "divisible by"
                ]
            }
        };
    }
}

module.exports = Blockly2Math;
