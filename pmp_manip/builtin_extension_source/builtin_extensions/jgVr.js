const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');


/**
 * Class of 2025
 * @constructor
 */
class jgVr {
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
            id: 'jgVr',
            name: 'Virtual Reality',
            color1: '#3888cf',
            color2: '#2f72ad',
            blocks: [
                // CORE
                {
                    opcode: 'isSupported',
                    text: 'is vr supported?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true
                },
                {
                    opcode: 'createSession',
                    text: 'create vr session',
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'closeSession',
                    text: 'close vr session',
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'isOpened',
                    text: 'is vr open?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true
                },
                '---', // SCREEN SPLITTING SETTINGS
                {
                    opcode: 'enableDisableSplitting',
                    text: 'turn auto-splitting [ONOFF]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ONOFF: {
                            type: ArgumentType.STRING,
                            menu: 'onoff'
                        }
                    }
                },
                {
                    opcode: 'splittingOffset',
                    text: 'set auto-split offset to [PX] pixels',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        PX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 40
                        }
                    }
                },
                {
                    opcode: 'placement169',
                    text: '[SIDE] x placement',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        SIDE: {
                            type: ArgumentType.STRING,
                            menu: 'side'
                        }
                    }
                },
                '---', // HEADSET POSITION
                {
                    opcode: 'headsetPosition',
                    text: 'headset position [VECTOR3]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        VECTOR3: {
                            type: ArgumentType.STRING,
                            menu: 'vector3'
                        }
                    }
                },
                {
                    opcode: 'headsetRotation',
                    text: 'headset rotation [VECTOR3]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        VECTOR3: {
                            type: ArgumentType.STRING,
                            menu: 'vector3'
                        }
                    }
                },
                '---', // CONTROLLER INPUT
                {
                    opcode: 'controllerPosition',
                    text: 'controller #[COUNT] position [VECTOR3]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        COUNT: {
                            type: ArgumentType.NUMBER,
                            menu: 'count'
                        },
                        VECTOR3: {
                            type: ArgumentType.STRING,
                            menu: 'vector3'
                        }
                    }
                },
                {
                    opcode: 'controllerRotation',
                    text: 'controller #[COUNT] rotation [VECTOR3]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        COUNT: {
                            type: ArgumentType.NUMBER,
                            menu: 'count'
                        },
                        VECTOR3: {
                            type: ArgumentType.STRING,
                            menu: 'vector3'
                        }
                    }
                },
            ],
            menus: {
                vector3: {
                    acceptReporters: true,
                    items: [
                        "x",
                        "y",
                        "z",
                    ].map(item => ({ text: item, value: item }))
                },
                count: {
                    acceptReporters: true,
                    items: [
                        "1",
                        "2",
                    ].map(item => ({ text: item, value: item }))
                },
                side: {
                    acceptReporters: false,
                    items: [
                        "left",
                        "right",
                    ].map(item => ({ text: item, value: item }))
                },
                onoff: {
                    acceptReporters: false,
                    items: [
                        "on",
                        "off",
                    ].map(item => ({ text: item, value: item }))
                },
            }
        };
    }
}

module.exports = jgVr;
