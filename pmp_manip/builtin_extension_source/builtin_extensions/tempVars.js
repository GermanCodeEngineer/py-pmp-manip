const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class
 * @constructor
 */
class tempVars {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'tempVars',
            name: 'Temporary Variables',
            color1: '#0069c2',
            color2: '#0060B4',
            color3: '#0060B4',
            blocks: [
                {
                    opcode: 'setVariable',
                    text: 'set [name] to [value]',
                    arguments: {
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Variable'
                        },
                        value: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Value'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'changeVariable',
                    text: 'change [name] by [value]',
                    arguments: {
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Variable'
                        },
                        value: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '1'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'getVariable',
                    text: 'get [name]',
                    arguments: {
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Variable'
                        }
                    },
                    allowDropAnywhere: true,
                    blockType: BlockType.REPORTER
                },
                '---',
                {
                    opcode: 'deleteVariable',
                    text: 'delete [name]',
                    arguments: {
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Variable'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'deleteAllVariables',
                    text: 'delete all variables',
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'variableExists',
                    text: 'variable [name] exists?',
                    arguments: {
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Variable'
                        }
                    },
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'allVariables',
                    text: 'current variables',
                    arguments: {
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Variable'
                        }
                    },
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                '---',
                {
                    opcode: 'forEachTempVar',
                    text: 'for each [NAME] in [REPEAT]',
                    branchCount: 1,
                    blockType: BlockType.LOOP,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Variable'
                        },
                        REPEAT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 10
                        }
                    }
                }
            ]
        };
    }
}

module.exports = tempVars;
