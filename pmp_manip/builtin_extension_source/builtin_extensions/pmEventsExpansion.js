const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class of idk
 * @constructor
 */
class pmEventsExpansion {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for extension
     */
    getInfo() {
        return {
            id: 'pmEventsExpansion',
            name: 'Events Expansion',
            color1: '#FFBF00',
            color2: '#E6AC00',
            color3: '#CC9900',
            isDynamic: true,
            blocks: [
                {
                    opcode: 'everyOtherFrame',
                    text: 'every other frame',
                    blockType: BlockType.EVENT,
                    isEdgeActivated: false,
                    switches: [
                        { isNoop: true },
                        'neverr'
                    ]
                },
                {
                    opcode: 'neverr',
                    text: 'never',
                    blockType: BlockType.EVENT,
                    isEdgeActivated: false,
                    switches: [
                        'everyOtherFrame',
                        { isNoop: true },
                    ]
                },
                {
                    opcode: 'whenSpriteClicked',
                    text: 'when [SPRITE] clicked',
                    blockType: BlockType.EVENT,
                    isEdgeActivated: false,
                    arguments: {
                        SPRITE: {
                            type: ArgumentType.STRING,
                            menu: "spriteName"
                        }
                    }
                },
                {
                    opcode: 'sendWithData',
                    text: 'broadcast [BROADCAST] with data [DATA]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        },
                        DATA: {
                            type: ArgumentType.STRING,
                            defaultValue: "abc"
                        }
                    }
                },
                {
                    opcode: 'receivedData',
                    text: 'when I receive [BROADCAST] with data',
                    blockType: BlockType.EVENT,
                    isEdgeActivated: false,
                    hideFromPalette: true,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            menu: "broadcastMenu"
                        }
                    }
                },
                {
                    opcode: 'isBroadcastReceived',
                    text: 'is message [BROADCAST] received?',
                    blockType: BlockType.BOOLEAN,
                    hideFromPalette: true,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        }
                    }
                },
                {
                    opcode: 'recievedDataReporter',
                    text: 'recieved data',
                    blockType: BlockType.REPORTER,
                    allowDropAnywhere: true,
                    disableMonitor: true
                },
                {
                    opcode: 'broadcastToSprite',
                    text: 'broadcast [BROADCAST] to [SPRITE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        },
                        SPRITE: {
                            type: ArgumentType.STRING,
                            menu: "spriteName"
                        }
                    }
                },
                {
                    opcode: 'broadcastFunction',
                    text: 'broadcast [BROADCAST] and wait',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    allowDropAnywhere: true,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        }
                    },
                    switches: [
                        { isNoop: true },
                        'broadcastFunctionArgs',
                        'broadcastThreadCount'
                    ],
                    switchText: 'broadcast and wait'
                },
                {
                    opcode: 'returnFromBroadcastFunc',
                    text: 'return [VALUE]',
                    blockType: BlockType.COMMAND,
                    isTerminal: true,
                    disableMonitor: true,
                    arguments: {
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "1"
                        }
                    }
                },
                {
                    opcode: 'broadcastThreadCount',
                    text: 'broadcast [BROADCAST] and get # of blocks started',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        }
                    },
                    switches: [
                        'broadcastFunction',
                        'broadcastFunctionArgs',
                        { isNoop: true },
                    ],
                    switchText: 'broadcast and get blocks started'
                },
                {
                    opcode: 'broadcastFunctionArgs',
                    text: 'broadcast [BROADCAST] with data [ARGS] and wait',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    allowDropAnywhere: true,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        },
                        ARGS: {
                            type: ArgumentType.STRING,
                            defaultValue: "abc"
                        }
                    },
                    switches: [
                        'broadcastFunction',
                        { isNoop: true },
                        'broadcastThreadCount'
                    ],
                    switchText: 'broadcast with data'
                },
            ],
            menus: {
                spriteName: "_spriteName",
                broadcastMenu: "_broadcastMenu"
            }
        };
    }
}

module.exports = pmEventsExpansion;
