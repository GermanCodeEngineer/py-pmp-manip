const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for storage blocks
 * @constructor
 */
class JgStorageBlocks {
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
            id: 'jgStorage',
            name: 'Storage',
            color1: '#76A8FE',
            color2: '#538EFC',
            docsURI: 'https://docs.penguinmod.com/extensions/storage',
            blocks: [
                {
                    blockType: BlockType.LABEL,
                    text: "Local Storage"
                },
                {
                    opcode: 'getValue',
                    text: 'get [KEY]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        },
                    }
                },
                {
                    opcode: 'setValue',
                    text: 'set [KEY] to [VALUE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "value"
                        },
                    }
                },
                {
                    opcode: 'deleteValue',
                    text: 'delete [KEY]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        }
                    }
                },
                {
                    opcode: 'getKeys',
                    text: 'get all stored names',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                {
                    blockType: BlockType.LABEL,
                    text: "Local Uploaded Project Storage"
                },
                {
                    opcode: 'getProjectValue',
                    text: 'get uploaded project [KEY]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        },
                    }
                },
                {
                    opcode: 'setProjectValue',
                    text: 'set uploaded project [KEY] to [VALUE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "value"
                        },
                    }
                },
                {
                    opcode: 'deleteProjectValue',
                    text: 'delete uploaded project [KEY]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        }
                    }
                },
                {
                    opcode: 'getProjectKeys',
                    text: 'get all stored names in this uploaded project',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                {
                    blockType: BlockType.LABEL,
                    text: "Local Project Storage"
                },
                {
                    opcode: 'getUniqueValue',
                    text: 'get local project [KEY]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        },
                    }
                },
                {
                    opcode: 'setUniqueValue',
                    text: 'set local project [KEY] to [VALUE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "value"
                        },
                    }
                },
                {
                    opcode: 'deleteUniqueValue',
                    text: 'delete local project [KEY]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        }
                    }
                },
                {
                    opcode: 'getUniqueKeys',
                    text: 'get all stored names in this local project',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                {
                    blockType: BlockType.LABEL,
                    text: "Server Storage"
                },
                {
                    opcode: 'isGlobalServer',
                    text: 'is using global server?',
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'useCertainServer',
                    text: 'set server to [SERVER] server',
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        SERVER: {
                            type: ArgumentType.STRING,
                            menu: "serverType"
                        },
                    }
                },
                {
                    opcode: 'waitingForConnection',
                    text: 'waiting for server to respond?',
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'connectionFailed',
                    text: 'server failed to respond?',
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'serverErrorOutput',
                    text: 'server error',
                    disableMonitor: false,
                    blockType: BlockType.REPORTER
                },
                "---",
                {
                    opcode: 'getServerValue',
                    text: 'get server [KEY]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        },
                    }
                },
                {
                    opcode: 'setServerValue',
                    text: 'set server [KEY] to [VALUE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "value"
                        },
                    }
                },
                {
                    opcode: 'deleteServerValue',
                    text: 'delete server [KEY]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            defaultValue: "key"
                        }
                    }
                }
            ],
            menus: {
                serverType: {
                    acceptReporters: true,
                    items: [
                        "project",
                        "global"
                    ].map(item => ({ text: item, value: item }))
                }
            }
        };
    }
}

module.exports = JgStorageBlocks;
