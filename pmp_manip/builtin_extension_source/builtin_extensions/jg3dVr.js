const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');
const Icon = null; // Icons do not matter
const IconController = null;

/**
 * Class for 3D VR blocks
 */
class Jg3DVrBlocks {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         */
        this.runtime = runtime;
    }
    /**
     * Metadata for this extension and its blocks.
     * @returns {object}
     */
    getInfo() {
        return {
            id: 'jg3dVr',
            name: '3D VR',
            color1: '#B100FE',
            color2: '#8000BC',
            blockIconURI: Icon,
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
                '---',
                {
                    opcode: 'attachObject',
                    text: 'attach camera to object named [OBJECT]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        OBJECT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Object1"
                        }
                    }
                },
                {
                    opcode: 'detachObject',
                    text: 'detach camera from object',
                    blockType: BlockType.COMMAND
                },
                '---',
                {
                    opcode: 'getControllerPosition',
                    text: 'controller #[INDEX] position [VECTOR3]',
                    blockType: BlockType.REPORTER,
                    blockIconURI: IconController,
                    disableMonitor: true,
                    arguments: {
                        INDEX: {
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
                    opcode: 'getControllerRotation',
                    text: 'controller #[INDEX] rotation [VECTOR3]',
                    blockType: BlockType.REPORTER,
                    blockIconURI: IconController,
                    disableMonitor: true,
                    arguments: {
                        INDEX: {
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
                    opcode: 'getControllerSide',
                    text: 'side of controller #[INDEX]',
                    blockType: BlockType.REPORTER,
                    blockIconURI: IconController,
                    disableMonitor: true,
                    arguments: {
                        INDEX: {
                            type: ArgumentType.NUMBER,
                            menu: 'count'
                        }
                    }
                },
                '---',
                {
                    opcode: 'getControllerStick',
                    text: 'joystick axis [XY] of controller #[INDEX]',
                    blockType: BlockType.REPORTER,
                    blockIconURI: IconController,
                    disableMonitor: true,
                    arguments: {
                        XY: {
                            type: ArgumentType.STRING,
                            menu: 'vector2'
                        },
                        INDEX: {
                            type: ArgumentType.NUMBER,
                            menu: 'count'
                        }
                    }
                },
                {
                    opcode: 'getControllerTrig',
                    text: 'analog value of [TRIGGER] trigger on controller #[INDEX]',
                    blockType: BlockType.REPORTER,
                    blockIconURI: IconController,
                    disableMonitor: true,
                    arguments: {
                        TRIGGER: {
                            type: ArgumentType.STRING,
                            menu: 'trig'
                        },
                        INDEX: {
                            type: ArgumentType.NUMBER,
                            menu: 'count'
                        }
                    }
                },
                {
                    opcode: 'getControllerButton',
                    text: 'button [BUTTON] on controller #[INDEX] pressed?',
                    blockType: BlockType.BOOLEAN,
                    blockIconURI: IconController,
                    disableMonitor: true,
                    arguments: {
                        BUTTON: {
                            type: ArgumentType.STRING,
                            menu: 'butt'
                        },
                        INDEX: {
                            type: ArgumentType.NUMBER,
                            menu: 'count'
                        }
                    }
                },
                {
                    opcode: 'getControllerTouching',
                    text: '[BUTTON] on controller #[INDEX] touched?',
                    blockType: BlockType.BOOLEAN,
                    blockIconURI: IconController,
                    disableMonitor: true,
                    arguments: {
                        BUTTON: {
                            type: ArgumentType.STRING,
                            menu: 'buttAll'
                        },
                        INDEX: {
                            type: ArgumentType.NUMBER,
                            menu: 'count'
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
                vector2: {
                    acceptReporters: true,
                    items: [
                        "x",
                        "y",
                    ].map(item => ({ text: item, value: item }))
                },
                butt: {
                    acceptReporters: true,
                    items: [
                        "a",
                        "b",
                        "x",
                        "y",
                        "joystick",
                    ].map(item => ({ text: item, value: item }))
                },
                trig: {
                    acceptReporters: true,
                    items: [
                        "back",
                        "side",
                    ].map(item => ({ text: item, value: item }))
                },
                buttAll: {
                    acceptReporters: true,
                    items: [
                        "a button",
                        "b button",
                        "x button",
                        "y button",
                        "joystick",
                        "back trigger",
                        "side trigger",
                    ].map(item => ({ text: item, value: item }))
                },
                count: {
                    acceptReporters: true,
                    items: [
                        "1",
                        "2",
                    ].map(item => ({ text: item, value: item }))
                },
            }
        };
    }
}

module.exports = Jg3DVrBlocks;
