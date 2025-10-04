const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const formatMessage = require('format-message');

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const iconURI = 'data:image/png;base64,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';

/**
 * Enum for motor specification.
 * @readonly
 * @enum {string}
 */
const WeDo2MotorLabel = {
    DEFAULT: 'motor',
    A: 'motor A',
    B: 'motor B',
    ALL: 'all motors'
};

/**
 * Enum for motor direction specification.
 * @readonly
 * @enum {string}
 */
const WeDo2MotorDirection = {
    FORWARD: 'this way',
    BACKWARD: 'that way',
    REVERSE: 'reverse'
};

/**
 * Enum for tilt sensor direction.
 * @readonly
 * @enum {string}
 */
const WeDo2TiltDirection = {
    UP: 'up',
    DOWN: 'down',
    LEFT: 'left',
    RIGHT: 'right',
    ANY: 'any'
};

/**
 * Scratch 3.0 blocks to interact with a LEGO WeDo 2.0 peripheral.
 */
class Scratch3WeDo2Blocks {

    /**
     * @return {string} - the ID of this extension.
     */
    static get EXTENSION_ID () {
        return 'wedo2';
    }

    /**
     * @return {number} - the tilt sensor counts as "tilted" if its tilt angle meets or exceeds this threshold.
     */
    static get TILT_THRESHOLD () {
        return 15;
    }

    /**
     * Construct a set of WeDo 2.0 blocks.
     * @param {Runtime} runtime - the Scratch 3.0 runtime.
     */
    constructor (runtime) {
        /**
         * The Scratch 3.0 runtime.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: Scratch3WeDo2Blocks.EXTENSION_ID,
            name: 'WeDo 2.0',
            blockIconURI: iconURI,
            showStatusButton: true,
            blocks: [
                {
                    opcode: 'motorOnFor',
                    text: formatMessage({
                        id: 'wedo2.motorOnFor',
                        default: 'turn [MOTOR_ID] on for [DURATION] seconds',
                        description: 'turn a motor on for some time'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: WeDo2MotorLabel.DEFAULT
                        },
                        DURATION: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    }
                },
                {
                    opcode: 'motorOn',
                    text: formatMessage({
                        id: 'wedo2.motorOn',
                        default: 'turn [MOTOR_ID] on',
                        description: 'turn a motor on indefinitely'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: WeDo2MotorLabel.DEFAULT
                        }
                    }
                },
                {
                    opcode: 'motorOff',
                    text: formatMessage({
                        id: 'wedo2.motorOff',
                        default: 'turn [MOTOR_ID] off',
                        description: 'turn a motor off'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: WeDo2MotorLabel.DEFAULT
                        }
                    }
                },
                {
                    opcode: 'startMotorPower',
                    text: formatMessage({
                        id: 'wedo2.startMotorPower',
                        default: 'set [MOTOR_ID] power to [POWER]',
                        description: 'set the motor\'s power and turn it on'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: WeDo2MotorLabel.DEFAULT
                        },
                        POWER: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        }
                    }
                },
                {
                    opcode: 'setMotorDirection',
                    text: formatMessage({
                        id: 'wedo2.setMotorDirection',
                        default: 'set [MOTOR_ID] direction to [MOTOR_DIRECTION]',
                        description: 'set the motor\'s turn direction'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: WeDo2MotorLabel.DEFAULT
                        },
                        MOTOR_DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_DIRECTION',
                            defaultValue: WeDo2MotorDirection.FORWARD
                        }
                    }
                },
                {
                    opcode: 'setLightHue',
                    text: formatMessage({
                        id: 'wedo2.setLightHue',
                        default: 'set light color to [HUE]',
                        description: 'set the LED color'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        HUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 50
                        }
                    }
                },
                {
                    opcode: 'playNoteFor',
                    text: formatMessage({
                        id: 'wedo2.playNoteFor',
                        default: 'play note [NOTE] for [DURATION] seconds',
                        description: 'play a certain note for some time'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NOTE: {
                            type: ArgumentType.NUMBER, // TODO: ArgumentType.MIDI_NOTE?
                            defaultValue: 60
                        },
                        DURATION: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.5
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'whenDistance',
                    text: formatMessage({
                        id: 'wedo2.whenDistance',
                        default: 'when distance [OP] [REFERENCE]',
                        description: 'check for when distance is < or > than reference'
                    }),
                    blockType: BlockType.HAT,
                    arguments: {
                        OP: {
                            type: ArgumentType.STRING,
                            menu: 'OP',
                            defaultValue: '<'
                        },
                        REFERENCE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 50
                        }
                    }
                },
                {
                    opcode: 'whenTilted',
                    text: formatMessage({
                        id: 'wedo2.whenTilted',
                        default: 'when tilted [TILT_DIRECTION_ANY]',
                        description: 'check when tilted in a certain direction'
                    }),
                    func: 'isTilted',
                    blockType: BlockType.HAT,
                    arguments: {
                        TILT_DIRECTION_ANY: {
                            type: ArgumentType.STRING,
                            menu: 'TILT_DIRECTION_ANY',
                            defaultValue: WeDo2TiltDirection.ANY
                        }
                    }
                },
                {
                    opcode: 'getDistance',
                    text: formatMessage({
                        id: 'wedo2.getDistance',
                        default: 'distance',
                        description: 'the value returned by the distance sensor'
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'isTilted',
                    text: formatMessage({
                        id: 'wedo2.isTilted',
                        default: 'tilted [TILT_DIRECTION_ANY]?',
                        description: 'whether the tilt sensor is tilted'
                    }),
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        TILT_DIRECTION_ANY: {
                            type: ArgumentType.STRING,
                            menu: 'TILT_DIRECTION_ANY',
                            defaultValue: WeDo2TiltDirection.ANY
                        }
                    }
                },
                {
                    opcode: 'getTiltAngle',
                    text: formatMessage({
                        id: 'wedo2.getTiltAngle',
                        default: 'tilt angle [TILT_DIRECTION]',
                        description: 'the angle returned by the tilt sensor'
                    }),
                    blockType: BlockType.REPORTER,
                    arguments: {
                        TILT_DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: 'TILT_DIRECTION',
                            defaultValue: WeDo2TiltDirection.UP
                        }
                    }
                }
            ],
            menus: {
                MOTOR_ID: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'wedo2.motorId.default',
                                default: 'motor',
                                description: 'label for motor element in motor menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2MotorLabel.DEFAULT
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.motorId.a',
                                default: 'motor A',
                                description: 'label for motor A element in motor menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2MotorLabel.A
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.motorId.b',
                                default: 'motor B',
                                description: 'label for motor B element in motor menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2MotorLabel.B
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.motorId.all',
                                default: 'all motors',
                                description: 'label for all motors element in motor menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2MotorLabel.ALL
                        }
                    ]
                },
                MOTOR_DIRECTION: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'wedo2.motorDirection.forward',
                                default: 'this way',
                                description:
                                    'label for forward element in motor direction menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2MotorDirection.FORWARD
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.motorDirection.backward',
                                default: 'that way',
                                description:
                                    'label for backward element in motor direction menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2MotorDirection.BACKWARD
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.motorDirection.reverse',
                                default: 'reverse',
                                description:
                                    'label for reverse element in motor direction menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2MotorDirection.REVERSE
                        }
                    ]
                },
                TILT_DIRECTION: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.up',
                                default: 'up',
                                description: 'label for up element in tilt direction menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2TiltDirection.UP
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.down',
                                default: 'down',
                                description: 'label for down element in tilt direction menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2TiltDirection.DOWN
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.left',
                                default: 'left',
                                description: 'label for left element in tilt direction menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2TiltDirection.LEFT
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.right',
                                default: 'right',
                                description: 'label for right element in tilt direction menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2TiltDirection.RIGHT
                        }
                    ]
                },
                TILT_DIRECTION_ANY: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.up',
                                default: 'up'
                            }),
                            value: WeDo2TiltDirection.UP
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.down',
                                default: 'down'
                            }),
                            value: WeDo2TiltDirection.DOWN
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.left',
                                default: 'left'
                            }),
                            value: WeDo2TiltDirection.LEFT
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.right',
                                default: 'right'
                            }),
                            value: WeDo2TiltDirection.RIGHT
                        },
                        {
                            text: formatMessage({
                                id: 'wedo2.tiltDirection.any',
                                default: 'any',
                                description: 'label for any element in tilt direction menu for LEGO WeDo 2 extension'
                            }),
                            value: WeDo2TiltDirection.ANY
                        }
                    ]
                },
                OP: {
                    acceptReporters: true,
                    items: ['<', '>']
                }
            }
        };
    }
}

module.exports = Scratch3WeDo2Blocks;
