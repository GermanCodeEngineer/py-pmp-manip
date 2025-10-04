const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const formatMessage = require('format-message');

/**
 * The LEGO Wireless Protocol documentation used to create this extension can be found at:
 * https://lego.github.io/lego-ble-wireless-protocol-docs/index.html
 */

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const iconURI = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAMAAAC5zwKfAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAACpQTFRF////fIel5ufolZ62/2YavsPS+YZOkJmy9/j53+Hk6+zs6N/b6dfO////tDhMHAAAAA50Uk5T/////////////////wBFwNzIAAAA6ElEQVR42uzX2w6DIBAEUGDVtlr//3dLaLwgiwUd2z7MJPJg5EQWiGhGcAxBggQJEiT436CIfqXJPTn3MKNYYMSDFpoAmp24OaYgvwKnFgL2zvVTCwHrMoMi+nUQLFthaNCCa0iwclLkDgYVsQp0mzxuqXgK1MRzoCLWgkPXNN2wI/q6Kvt7u/cX0HtejN8x2sXpnpb8J8D3b0Keuhh3X975M+i0xNVbg3s1TIasgK21bQyGO+s2PykaGMYbge8KrNrssvkOWDXkErB8UuBHETjoYLkKBA8ZfuDkbwVBggQJEiR4MC8BBgDTtMZLx2nFCQAAAABJRU5ErkJggg==';

/**
 * Ids for each color sensor value used by the extension.
 * @readonly
 * @enum {string}
 */
const BoostColor = {
    ANY: 'any',
    NONE: 'none',
    RED: 'red',
    BLUE: 'blue',
    GREEN: 'green',
    YELLOW: 'yellow',
    WHITE: 'white',
    BLACK: 'black'
};

/**
 * Enum for motor specification.
 * @readonly
 * @enum {string}
 */
const BoostMotorLabel = {
    A: 'A',
    B: 'B',
    C: 'C',
    D: 'D',
    AB: 'AB',
    ALL: 'ABCD'
};

/**
 * Enum for motor direction specification.
 * @readonly
 * @enum {string}
 */
const BoostMotorDirection = {
    FORWARD: 'this way',
    BACKWARD: 'that way',
    REVERSE: 'reverse'
};

/**
 * Enum for tilt sensor direction.
 * @readonly
 * @enum {string}
 */
const BoostTiltDirection = {
    UP: 'up',
    DOWN: 'down',
    LEFT: 'left',
    RIGHT: 'right',
    ANY: 'any'
};

/**
 * Scratch 3.0 blocks to interact with a LEGO Boost peripheral.
 */
class Scratch3BoostBlocks {

    /**
     * @return {string} - the ID of this extension.
     */
    static get EXTENSION_ID () {
        return 'boost';
    }

    /**
     * @return {number} - the tilt sensor counts as "tilted" if its tilt angle meets or exceeds this threshold.
     */
    static get TILT_THRESHOLD () {
        return 15;
    }

    /**
     * Construct a set of Boost blocks.
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
            id: Scratch3BoostBlocks.EXTENSION_ID,
            name: 'BOOST',
            blockIconURI: iconURI,
            showStatusButton: true,
            blocks: [
                {
                    opcode: 'motorOnFor',
                    text: formatMessage({
                        id: 'boost.motorOnFor',
                        default: 'turn motor [MOTOR_ID] for [DURATION] seconds',
                        description: 'turn a motor on for some time'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: BoostMotorLabel.A
                        },
                        DURATION: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    }
                },
                {
                    opcode: 'motorOnForRotation',
                    text: formatMessage({
                        id: 'boost.motorOnForRotation',
                        default: 'turn motor [MOTOR_ID] for [ROTATION] rotations',
                        description: 'turn a motor on for rotation'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: BoostMotorLabel.A
                        },
                        ROTATION: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    }
                },
                {
                    opcode: 'motorOn',
                    text: formatMessage({
                        id: 'boost.motorOn',
                        default: 'turn motor [MOTOR_ID] on',
                        description: 'turn a motor on indefinitely'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: BoostMotorLabel.A
                        }
                    }
                },
                {
                    opcode: 'motorOff',
                    text: formatMessage({
                        id: 'boost.motorOff',
                        default: 'turn motor [MOTOR_ID] off',
                        description: 'turn a motor off'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: BoostMotorLabel.A
                        }
                    }
                },
                {
                    opcode: 'setMotorPower',
                    text: formatMessage({
                        id: 'boost.setMotorPower',
                        default: 'set motor [MOTOR_ID] speed to [POWER] %',
                        description: 'set the motor\'s speed without turning it on'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: BoostMotorLabel.ALL
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
                        id: 'boost.setMotorDirection',
                        default: 'set motor [MOTOR_ID] direction [MOTOR_DIRECTION]',
                        description: 'set the motor\'s turn direction without turning it on'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MOTOR_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_ID',
                            defaultValue: BoostMotorLabel.A
                        },
                        MOTOR_DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_DIRECTION',
                            defaultValue: BoostMotorDirection.FORWARD
                        }
                    }
                },
                {
                    opcode: 'getMotorPosition',
                    text: formatMessage({
                        id: 'boost.getMotorPosition',
                        default: 'motor [MOTOR_REPORTER_ID] position',
                        description: 'the position returned by the motor'
                    }),
                    blockType: BlockType.REPORTER,
                    arguments: {
                        MOTOR_REPORTER_ID: {
                            type: ArgumentType.STRING,
                            menu: 'MOTOR_REPORTER_ID',
                            defaultValue: BoostMotorLabel.A
                        }
                    }
                },
                {
                    opcode: 'whenColor',
                    text: formatMessage({
                        id: 'boost.whenColor',
                        default: 'when [COLOR] brick seen',
                        description: 'check for when color'
                    }),
                    blockType: BlockType.HAT,
                    arguments: {
                        COLOR: {
                            type: ArgumentType.STRING,
                            menu: 'COLOR',
                            defaultValue: BoostColor.ANY
                        }
                    }
                },
                {
                    opcode: 'seeingColor',
                    text: formatMessage({
                        id: 'boost.seeingColor',
                        default: 'seeing [COLOR] brick?',
                        description: 'is the color sensor seeing a certain color?'
                    }),
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        COLOR: {
                            type: ArgumentType.STRING,
                            menu: 'COLOR',
                            defaultValue: BoostColor.ANY
                        }
                    }
                },
                {
                    opcode: 'whenTilted',
                    text: formatMessage({
                        id: 'boost.whenTilted',
                        default: 'when tilted [TILT_DIRECTION_ANY]',
                        description: 'check when tilted in a certain direction'
                    }),
                    func: 'isTilted',
                    blockType: BlockType.HAT,
                    arguments: {
                        TILT_DIRECTION_ANY: {
                            type: ArgumentType.STRING,
                            menu: 'TILT_DIRECTION_ANY',
                            defaultValue: BoostTiltDirection.ANY
                        }
                    }
                },
                {
                    opcode: 'getTiltAngle',
                    text: formatMessage({
                        id: 'boost.getTiltAngle',
                        default: 'tilt angle [TILT_DIRECTION]',
                        description: 'the angle returned by the tilt sensor'
                    }),
                    blockType: BlockType.REPORTER,
                    arguments: {
                        TILT_DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: 'TILT_DIRECTION',
                            defaultValue: BoostTiltDirection.UP
                        }
                    }
                },
                {
                    opcode: 'setLightHue',
                    text: formatMessage({
                        id: 'boost.setLightHue',
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
                }
            ],
            menus: {
                MOTOR_ID: {
                    acceptReporters: true,
                    items: [
                        {
                            text: 'A',
                            value: BoostMotorLabel.A
                        },
                        {
                            text: 'B',
                            value: BoostMotorLabel.B
                        },
                        {
                            text: 'C',
                            value: BoostMotorLabel.C
                        },
                        {
                            text: 'D',
                            value: BoostMotorLabel.D
                        },
                        {
                            text: 'AB',
                            value: BoostMotorLabel.AB
                        },
                        {
                            text: 'ABCD',
                            value: BoostMotorLabel.ALL
                        }
                    ]
                },
                MOTOR_REPORTER_ID: {
                    acceptReporters: true,
                    items: [
                        {
                            text: 'A',
                            value: BoostMotorLabel.A
                        },
                        {
                            text: 'B',
                            value: BoostMotorLabel.B
                        },
                        {
                            text: 'C',
                            value: BoostMotorLabel.C
                        },
                        {
                            text: 'D',
                            value: BoostMotorLabel.D
                        }
                    ]
                },
                MOTOR_DIRECTION: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'boost.motorDirection.forward',
                                default: 'this way',
                                description:
                                    'label for forward element in motor direction menu for LEGO Boost extension'
                            }),
                            value: BoostMotorDirection.FORWARD
                        },
                        {
                            text: formatMessage({
                                id: 'boost.motorDirection.backward',
                                default: 'that way',
                                description:
                                    'label for backward element in motor direction menu for LEGO Boost extension'
                            }),
                            value: BoostMotorDirection.BACKWARD
                        },
                        {
                            text: formatMessage({
                                id: 'boost.motorDirection.reverse',
                                default: 'reverse',
                                description:
                                    'label for reverse element in motor direction menu for LEGO Boost extension'
                            }),
                            value: BoostMotorDirection.REVERSE
                        }
                    ]
                },
                TILT_DIRECTION: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.up',
                                default: 'up',
                                description: 'label for up element in tilt direction menu for LEGO Boost extension'
                            }),
                            value: BoostTiltDirection.UP
                        },
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.down',
                                default: 'down',
                                description: 'label for down element in tilt direction menu for LEGO Boost extension'
                            }),
                            value: BoostTiltDirection.DOWN
                        },
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.left',
                                default: 'left',
                                description: 'label for left element in tilt direction menu for LEGO Boost extension'
                            }),
                            value: BoostTiltDirection.LEFT
                        },
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.right',
                                default: 'right',
                                description: 'label for right element in tilt direction menu for LEGO Boost extension'
                            }),
                            value: BoostTiltDirection.RIGHT
                        }
                    ]
                },
                TILT_DIRECTION_ANY: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.up',
                                default: 'up'
                            }),
                            value: BoostTiltDirection.UP
                        },
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.down',
                                default: 'down'
                            }),
                            value: BoostTiltDirection.DOWN
                        },
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.left',
                                default: 'left'
                            }),
                            value: BoostTiltDirection.LEFT
                        },
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.right',
                                default: 'right'
                            }),
                            value: BoostTiltDirection.RIGHT
                        },
                        {
                            text: formatMessage({
                                id: 'boost.tiltDirection.any',
                                default: 'any',
                                description: 'label for any element in tilt direction menu for LEGO Boost extension'
                            }),
                            value: BoostTiltDirection.ANY
                        }
                    ]
                },
                COLOR: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'boost.color.red',
                                default: 'red',
                                description: 'the color red'
                            }),
                            value: BoostColor.RED
                        },
                        {
                            text: formatMessage({
                                id: 'boost.color.blue',
                                default: 'blue',
                                description: 'the color blue'
                            }),
                            value: BoostColor.BLUE
                        },
                        {
                            text: formatMessage({
                                id: 'boost.color.green',
                                default: 'green',
                                description: 'the color green'
                            }),
                            value: BoostColor.GREEN
                        },
                        {
                            text: formatMessage({
                                id: 'boost.color.yellow',
                                default: 'yellow',
                                description: 'the color yellow'
                            }),
                            value: BoostColor.YELLOW
                        },
                        {
                            text: formatMessage({
                                id: 'boost.color.white',
                                default: 'white',
                                desription: 'the color white'
                            }),
                            value: BoostColor.WHITE
                        },
                        {
                            text: formatMessage({
                                id: 'boost.color.black',
                                default: 'black',
                                description: 'the color black'
                            }),
                            value: BoostColor.BLACK
                        },
                        {
                            text: formatMessage({
                                id: 'boost.color.any',
                                default: 'any color',
                                description: 'any color'
                            }),
                            value: BoostColor.ANY
                        }
                    ]
                }
            }
        };
    }
}

module.exports = Scratch3BoostBlocks;
