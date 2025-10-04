const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class
 * oh yea you cant access util in the runner anymore
 * im not adding it because im done with implementing eval in PM since it was done like 3 times
 * @constructor
 */
class jgJavascript {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
        this.runningEditorUnsandboxed = false;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'jgJavascript',
            name: 'JavaScript',
            isDynamic: true,
            // color1: '#EFC900', look like doo doo
            blocks: [
                {
                    opcode: 'unsandbox',
                    text: 'Run Unsandboxed',
                    blockType: BlockType.BUTTON,
                    hideFromPalette: this.runningEditorUnsandboxed
                },
                {
                    opcode: 'sandbox',
                    text: 'Run Sandboxed',
                    blockType: BlockType.BUTTON,
                    hideFromPalette: !this.runningEditorUnsandboxed
                },
                {
                    opcode: 'javascriptHat',
                    text: 'when javascript [CODE] == true',
                    blockType: BlockType.HAT,
                    hideFromPalette: !this.runningEditorUnsandboxed, // this block seems to cause strange behavior because of how sandboxed eval is done
                    arguments: {
                        CODE: {
                            type: ArgumentType.STRING,
                            defaultValue: "Math.round(Math.random()) === 1"
                        }
                    }
                },
                {
                    opcode: 'javascriptStack',
                    text: 'javascript [CODE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        CODE: {
                            type: ArgumentType.STRING,
                            defaultValue: "alert('Hello!')"
                        }
                    }
                },
                {
                    opcode: 'javascriptString',
                    text: 'javascript [CODE]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        CODE: {
                            type: ArgumentType.STRING,
                            defaultValue: "Math.random()"
                        }
                    }
                },
                {
                    opcode: 'javascriptBool',
                    text: 'javascript [CODE]',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    arguments: {
                        CODE: {
                            type: ArgumentType.STRING,
                            defaultValue: "Math.round(Math.random()) === 1"
                        }
                    }
                },
                {
                    blockType: BlockType.LABEL,
                    text: 'You can run unsandboxed',
                    hideFromPalette: !this.runningEditorUnsandboxed
                },
                {
                    blockType: BlockType.LABEL,
                    text: 'when packaging the project.',
                    hideFromPalette: !this.runningEditorUnsandboxed
                },
                {
                    blockType: BlockType.LABEL,
                    text: '⠀',
                    hideFromPalette: !this.runningEditorUnsandboxed
                },
                {
                    blockType: BlockType.LABEL,
                    text: 'Player Options >',
                    hideFromPalette: !this.runningEditorUnsandboxed
                },
                {
                    blockType: BlockType.LABEL,
                    text: 'Remove sandbox on the JavaScript Ext.',
                    hideFromPalette: !this.runningEditorUnsandboxed
                },
            ]
        };
    }
}

module.exports = jgJavascript;
