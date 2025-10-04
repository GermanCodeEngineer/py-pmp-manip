const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');
const TargetType = require("../../extension-support/target-type");

//const blockIconURI = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAAFACAMAAAD6TlWYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAPUExURQAAAP+xNQDiGgCU/wAAAJEQGGoAAAAFdFJOU/////8A+7YOUwAAAAlwSFlzAAAOwwAADsMBx2+oZAAABA5JREFUeF7t0EtuW0EUA9F8vP81Z8JRAwzbLuk5COoMBb1LdP34EGJAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEHos4M+HZfbtDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0KPBfxfGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEZsBfh/z8z/r9SfnsywwIGRAyIGRAyICQASEDQp8OeMrfvk06vEzOXjPgIWevGfCQs9cMeMjZawY85Ow1Ax5y9poBDzl7zYCHnL2GA57y2dvlvW+TmcmARWYmAxaZmQxYZGYyYJGZyYBFZiYDFpmZDFhkZnp5wFPOvFze+TaZmQxYZGYyYJGZyYBFZiYDFpmZDFhkZjJgkZnJgEVmprcHPOXsl+V9j8lsZcAhs5UBh8xWBhwyWxlwyGxlwCGzlQGHzFYGHDJbPR7wlJlreddjMlsZcMhsZcAhs5UBh8xWBhwyWxlwyGxlwCGzlQGHzFbfHvCU2SrvekxmKwMOma0MOGS2MuCQ2cqAQ2YrAw6ZrQw4ZLYy4JDZyoBDZisDDpmtDDhktjLgkNnKgENmKwMOma0MOGS2MuCQ2erbA2bmWt71mMxWBhwyWxlwyGxlwCGzlQGHzFYGHDJbGXDIbGXAIbPV4wFz9svyrsdktjLgkNnKgENmKwMOma0MOGS2MuCQ2cqAQ2YrAw6Zrd4eMGdeLu97m8xMBiwyMxmwyMxkwCIzkwGLzEwGLDIzGbDIzGTAIjPTywPms7fLO98mM5MBi8xMBiwyMxmwyMxkwCIzkwGLzEwGLDIzGbDIzIQD5m/fJu99mZy9ZsBDzl4z4CFnrxnwkLPXDHjI2WsGPOTsNQMecvaaAQ85e+3TAfPzPysdruWzLzMgZEDIgJABIQNCBoQMCM2A+jsDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgMjHxx+IPExM0h8siAAAAABJRU5ErkJggg=="

/**
 * Class for Reflex blocks
 * @constructor
 */
class jwReflex {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'jwReflex',
            name: 'Reflex',
            //blockIconURI: blockIconURI,
            color1: '#000000', //tbd
            color2: '#ffffff', // tbd
            blocks: [
                {
                    opcode: 'createFlex',
                    text: formatMessage({
                        id: 'jwReflex.blocks.createFlex',
                        default: 'create flex',
                        description: 'Creates the flex. If there is already a flex, nothing happens. You can only remove a flex by reloading the project.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'updateFlex',
                    text: formatMessage({
                        id: 'jwReflex.blocks.updateFlex',
                        default: 'update flex',
                        description: 'Update position of sprite with flex data.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'setFlexXY',
                    text: formatMessage({
                        id: 'jwReflex.blocks.setFlexXY',
                        default: 'set flex pos [FX] [FY]',
                        description: 'Sets flex position'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        FX: {
                            type: ArgumentType.NUMBER,
                            default: 0
                        },
                        FY: {
                            type: ArgumentType.NUMBER,
                            default: 0
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getFlexX',
                    text: formatMessage({
                        id: 'jwReflex.blocks.getFlexX',
                        default: 'x flex position',
                        description: 'Gets the flex positon\'s x value'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getFlexY',
                    text: formatMessage({
                        id: 'jwReflex.blocks.getFlexY',
                        default: 'y flex position',
                        description: 'Gets the flex positon\'s y value'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'setOffsetXY',
                    text: formatMessage({
                        id: 'jwReflex.blocks.setOffsetXY',
                        default: 'set offset pos [OX] [OY]',
                        description: 'Sets offset position'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        OX: {
                            type: ArgumentType.NUMBER,
                            default: 0
                        },
                        OY: {
                            type: ArgumentType.NUMBER,
                            default: 0
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getOffsetX',
                    text: formatMessage({
                        id: 'jwReflex.blocks.getOffsetX',
                        default: 'x offset position',
                        description: 'Gets the offset positon\'s x value'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getOffsetY',
                    text: formatMessage({
                        id: 'jwReflex.blocks.getOffsetY',
                        default: 'y offset position',
                        description: 'Gets the offset positon\'s y value'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                }
            ]
        };
    }
}

module.exports = jwReflex;
