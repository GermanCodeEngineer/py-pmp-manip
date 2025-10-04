const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for Timers blocks
 * @constructor
 */
class JgTimersBlocks {
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
            id: 'jgTimers',
            name: 'Multiple Timers',
            color1: '#0093FE',
            color2: '#1177FC',
            blocks: [
                {
                    opcode: 'createTimer',
                    text: 'create timer named [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
                {
                    opcode: 'deleteTimer',
                    text: 'delete timer named [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
                {
                    opcode: 'deleteAllTimer',
                    text: 'delete all timers',
                    blockType: BlockType.COMMAND
                },

                { text: "Values", blockType: BlockType.LABEL, },

                {
                    opcode: 'getTimer',
                    text: 'get timer named [NAME]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: false,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
                {
                    opcode: 'getTimerData',
                    text: 'get [DATA] of timer named [NAME]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: false,
                    arguments: {
                        DATA: { type: ArgumentType.STRING, menu: "timerData" },
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
                {
                    opcode: 'existsTimer',
                    text: 'timer named [NAME] exists?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: false,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },

                {
                    opcode: 'getAllTimer',
                    text: 'get all timers',
                    blockType: BlockType.REPORTER,
                    disableMonitor: false
                },

                { text: "Operations", blockType: BlockType.LABEL, },

                {
                    opcode: 'startTimer',
                    text: 'start timer [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
                {
                    opcode: 'pauseTimer',
                    text: 'pause timer [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
                {
                    opcode: 'stopTimer',
                    text: 'stop timer [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
                {
                    opcode: 'resetTimer',
                    text: 'reset timer [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
                {
                    opcode: 'addTimer',
                    text: 'add [SECONDS] seconds to timer [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        SECONDS: { type: ArgumentType.NUMBER, defaultValue: 5 },
                        NAME: { type: ArgumentType.STRING, defaultValue: "timer" }
                    }
                },
            ],
            menus: {
                timerData: {
                    acceptReporters: true,
                    items: [
                        "milliseconds",
                        "minutes",
                        "hours",
                        // haha funny options
                        "days",
                        "weeks",
                        "years"
                    ].map(item => ({ text: item, value: item }))
                }
            }
        };
    }
}

module.exports = JgTimersBlocks;
