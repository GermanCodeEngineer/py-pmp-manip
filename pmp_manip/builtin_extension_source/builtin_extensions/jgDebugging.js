const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const noopSwitch = { isNoop: true };

/**
 * Class for Debugging blocks
 * @constructor
 */
class jgDebuggingBlocks {
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
            id: 'jgDebugging',
            name: 'Debugging',
            color1: '#878787',
            color2: '#757575',
            blocks: [
                {
                    opcode: 'openDebugger',
                    text: 'open debugger',
                    blockType: BlockType.COMMAND,
                    switches: [ noopSwitch, 'closeDebugger' ]
                },
                {
                    opcode: 'closeDebugger',
                    text: 'close debugger',
                    blockType: BlockType.COMMAND,
                    switches: [ 'openDebugger', noopSwitch ]
                },
                '---',
                {
                    opcode: 'log',
                    text: 'log [INFO]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        INFO: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello!"
                        }
                    },
                    switches: [ noopSwitch, 'warn', 'error' ],
                    switchText: 'log'
                },
                {
                    opcode: 'warn',
                    text: 'warn [INFO]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        INFO: {
                            type: ArgumentType.STRING,
                            defaultValue: "Warning"
                        }
                    },
                    switches: [ 'log', noopSwitch, 'error' ],
                    switchText: 'warn'
                },
                {
                    opcode: 'error',
                    text: 'error [INFO]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        INFO: {
                            type: ArgumentType.STRING,
                            defaultValue: "Error"
                        }
                    },
                    switches: [ 'log', 'warn', noopSwitch ],
                    switchText: 'error'
                },
                '---',
                {
                    opcode: 'breakpoint',
                    blockType: BlockType.COMMAND,
                }
            ]
        };
    }
}

module.exports = jgDebuggingBlocks;
