const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const formatMessage = require('format-message');

/**
 * Icon png to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/png;base64,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';

/**
 * Icon png to be displayed in the blocks category menu, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const menuIconURI = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABGdBTUEAALGPC/xhBQAAA9dJREFUWAnNmE2IFEcUgF/9dE/v7LoaM9kkK4JBRA0EFBIPRm85hBAvEXHXwyo5eFE87GFcReMkObgJiQnkkJzEg9n8HIJixKNe1IMKihgiCbviwV11V3d0d3pmuqsqr5ppcEnb3TNVggVFVVe9eu+r97qqq4tASqp8/fsboQgmU0TMugi571K29bPy9ovPU8Sf16HbpQj3EkYFBcJcr5Am2nZfs94AIWVfqMQeHNwhICUBZ4ypUIA/X2sbIm2AW8AJK0lkEP6TJpfqwXgg4QxmF/fB7Gtvxk1G5ZKHU1CqTgPJoSUXYJYeohSUJu+qrqdVUGh2/pVX4VFffx77WaqBZkrkEFj271+qWH0sXcU3FBzyQe/Mg7B//LbKMTRTxNiDbsMHHjTJlyM7HEJIBHXs2KXFj+oTNSdoQOCYLS5jD9IwBMm5H8NplwwPb/QV4yEIcycaAza9IuA76B38fuz1OF5RXUkmHCdu6rg0BpSMgV/sAe7DdzGFrvvdi0D3mSZjQA0wt7REQsY+iWF0XbfFzyal8SLRxuteD+Du4h4Z/flbqaBHibAQtZmQtcZaAZSMwtTylaR/4vaw1ju5YhWG10pwwAqghmp2FeHO2+t11WqyM80W0m7vAOhsM1kD7CGz8L57Jsq6bitZC/GcWgLf1H6KuHT92cTDAFy/BgXMXm0OCpgV50Bo9kK3BqiBboabQMMU/WoL5im4jToeq/AIgXsiRx5KKCjcwPEsiAv/BQMu9EwyDHXd/3kqCOSzDk6t5/YglQKKeJwq+PNRmJI8kwSTaj1HZy5AhSHqnXkIvU9mMUwEw4Q5wTM57LUtkg8QPw/cdcBJ+PhvKJ0Gj80nGq6JXrg6/XFiX97GXIBpyqTieKpKViOl+WEhWXMaUavvvdIZ8Giy5+Lh3bwKm/t+Be3JazMfxc1tldY26rastiHcsQevTG9pw0znovkAcRWHzSDKnZtaOJLSfMFLB5RqtRBS4LbCurqLCy0YPkU3C0IIPEimMqR2ei7ZX2+KQdRi/WahNT/GmfOD4Vyzhx/66pcjp85dUvcmp6J8+txldXh07PPskdkS+V6EbD0vTOKlB0x9B/O6BS8ULly9PgE6x4kDPR/XX5pyYKj8xcCucsUmkNUQE0JvKKm2VioVK5HRE7UKOHbi6B94RzP+93jtpC0vWgXUF0hr3ipuw8uadwd3jXxoA9IK4Pah8t6BneV9GgjD28Svw1mlxFobgFbeFTz13cKbth93fDryp2CEq0a4hTA+aAPQ/ESJFDdvXLzzzrqNjlTqOP6uDeFf0uhvJ0ZP2QD8D6ZzU6u8YIbBAAAAAElFTkSuQmCC';

/**
 * Enum for pushed and pulled menu options.
 * @readonly
 * @enum {string}
 */
const PushPullValues = {
    PUSHED: 'pushed',
    PULLED: 'pulled'
};

/**
 * Enum for motion gesture menu options.
 * @readonly
 * @enum {string}
 */
const GestureValues = {
    SHAKEN: 'shaken',
    STARTED_FALLING: 'started falling',
    TURNED_FACE_UP: 'turned face up',
    TURNED_FACE_DOWN: 'turned face down'
};

/**
 * Enum for tilt axis menu options.
 * @readonly
 * @enum {string}
 */
const TiltAxisValues = {
    FRONT: 'front',
    BACK: 'back',
    LEFT: 'left',
    RIGHT: 'right',
    ANY: 'any'
};

/**
 * Enum for axis menu options.
 * @readonly
 * @enum {string}
 */
const AxisValues = {
    X: 'x',
    Y: 'y',
    Z: 'z'
};

/**
 * Scratch 3.0 blocks to interact with a GDX-FOR peripheral.
 */
class Scratch3GdxForBlocks {

    /**
     * @return {string} - the name of this extension.
     */
    static get EXTENSION_NAME () {
        return 'Force and Acceleration';
    }

    /**
     * @return {string} - the ID of this extension.
     */
    static get EXTENSION_ID () {
        return 'gdxfor';
    }

    get AXIS_MENU () {
        return [
            {
                text: 'x',
                value: AxisValues.X
            },
            {
                text: 'y',
                value: AxisValues.Y
            },
            {
                text: 'z',
                value: AxisValues.Z
            }
        ];
    }

    get TILT_MENU () {
        return [
            {
                text: formatMessage({
                    id: 'gdxfor.tiltDirectionMenu.front',
                    default: 'front',
                    description: 'label for front element in tilt direction picker for gdxfor extension'
                }),
                value: TiltAxisValues.FRONT
            },
            {
                text: formatMessage({
                    id: 'gdxfor.tiltDirectionMenu.back',
                    default: 'back',
                    description: 'label for back element in tilt direction picker for gdxfor extension'
                }),
                value: TiltAxisValues.BACK
            },
            {
                text: formatMessage({
                    id: 'gdxfor.tiltDirectionMenu.left',
                    default: 'left',
                    description: 'label for left element in tilt direction picker for gdxfor extension'
                }),
                value: TiltAxisValues.LEFT
            },
            {
                text: formatMessage({
                    id: 'gdxfor.tiltDirectionMenu.right',
                    default: 'right',
                    description: 'label for right element in tilt direction picker for gdxfor extension'
                }),
                value: TiltAxisValues.RIGHT
            }
        ];
    }

    get TILT_MENU_ANY () {
        return [
            ...this.TILT_MENU,
            {
                text: formatMessage({
                    id: 'gdxfor.tiltDirectionMenu.any',
                    default: 'any',
                    description: 'label for any direction element in tilt direction picker for gdxfor extension'
                }),
                value: TiltAxisValues.ANY
            }
        ];
    }

    get PUSH_PULL_MENU () {
        return [
            {
                text: formatMessage({
                    id: 'gdxfor.pushed',
                    default: 'pushed',
                    description: 'the force sensor was pushed inward'
                }),
                value: PushPullValues.PUSHED
            },
            {
                text: formatMessage({
                    id: 'gdxfor.pulled',
                    default: 'pulled',
                    description: 'the force sensor was pulled outward'
                }),
                value: PushPullValues.PULLED
            }
        ];
    }

    get GESTURE_MENU () {
        return [
            {
                text: formatMessage({
                    id: 'gdxfor.shaken',
                    default: 'shaken',
                    description: 'the sensor was shaken'
                }),
                value: GestureValues.SHAKEN
            },
            {
                text: formatMessage({
                    id: 'gdxfor.startedFalling',
                    default: 'started falling',
                    description: 'the sensor started free falling'
                }),
                value: GestureValues.STARTED_FALLING
            },
            {
                text: formatMessage({
                    id: 'gdxfor.turnedFaceUp',
                    default: 'turned face up',
                    description: 'the sensor was turned to face up'
                }),
                value: GestureValues.TURNED_FACE_UP
            },
            {
                text: formatMessage({
                    id: 'gdxfor.turnedFaceDown',
                    default: 'turned face down',
                    description: 'the sensor was turned to face down'
                }),
                value: GestureValues.TURNED_FACE_DOWN
            }
        ];
    }

    /**
     * Construct a set of GDX-FOR blocks.
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
            id: Scratch3GdxForBlocks.EXTENSION_ID,
            name: Scratch3GdxForBlocks.EXTENSION_NAME,
            blockIconURI: blockIconURI,
            menuIconURI: menuIconURI,
            showStatusButton: true,
            blocks: [
                {
                    opcode: 'whenGesture',
                    text: formatMessage({
                        id: 'gdxfor.whenGesture',
                        default: 'when [GESTURE]',
                        description: 'when the sensor detects a gesture'
                    }),
                    blockType: BlockType.HAT,
                    arguments: {
                        GESTURE: {
                            type: ArgumentType.STRING,
                            menu: 'gestureOptions',
                            defaultValue: GestureValues.SHAKEN
                        }
                    }
                },
                {
                    opcode: 'whenForcePushedOrPulled',
                    text: formatMessage({
                        id: 'gdxfor.whenForcePushedOrPulled',
                        default: 'when force sensor [PUSH_PULL]',
                        description: 'when the force sensor is pushed or pulled'
                    }),
                    blockType: BlockType.HAT,
                    arguments: {
                        PUSH_PULL: {
                            type: ArgumentType.STRING,
                            menu: 'pushPullOptions',
                            defaultValue: PushPullValues.PUSHED
                        }
                    }
                },
                {
                    opcode: 'getForce',
                    text: formatMessage({
                        id: 'gdxfor.getForce',
                        default: 'force',
                        description: 'gets force'
                    }),
                    blockType: BlockType.REPORTER
                },
                '---',
                {
                    opcode: 'whenTilted',
                    text: formatMessage({
                        id: 'gdxfor.whenTilted',
                        default: 'when tilted [TILT]',
                        description: 'when the sensor detects tilt'
                    }),
                    blockType: BlockType.HAT,
                    arguments: {
                        TILT: {
                            type: ArgumentType.STRING,
                            menu: 'tiltAnyOptions',
                            defaultValue: TiltAxisValues.ANY
                        }
                    }
                },
                {
                    opcode: 'isTilted',
                    text: formatMessage({
                        id: 'gdxfor.isTilted',
                        default: 'tilted [TILT]?',
                        description: 'is the device tilted?'
                    }),
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        TILT: {
                            type: ArgumentType.STRING,
                            menu: 'tiltAnyOptions',
                            defaultValue: TiltAxisValues.ANY
                        }
                    }
                },
                {
                    opcode: 'getTilt',
                    text: formatMessage({
                        id: 'gdxfor.getTilt',
                        default: 'tilt angle [TILT]',
                        description: 'gets tilt'
                    }),
                    blockType: BlockType.REPORTER,
                    arguments: {
                        TILT: {
                            type: ArgumentType.STRING,
                            menu: 'tiltOptions',
                            defaultValue: TiltAxisValues.FRONT
                        }
                    }
                },
                '---',
                {
                    opcode: 'isFreeFalling',
                    text: formatMessage({
                        id: 'gdxfor.isFreeFalling',
                        default: 'falling?',
                        description: 'is the device in free fall?'
                    }),
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'getSpinSpeed',
                    text: formatMessage({
                        id: 'gdxfor.getSpin',
                        default: 'spin speed [DIRECTION]',
                        description: 'gets spin speed'
                    }),
                    blockType: BlockType.REPORTER,
                    arguments: {
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: 'axisOptions',
                            defaultValue: AxisValues.Z
                        }
                    }
                },
                {
                    opcode: 'getAcceleration',
                    text: formatMessage({
                        id: 'gdxfor.getAcceleration',
                        default: 'acceleration [DIRECTION]',
                        description: 'gets acceleration'
                    }),
                    blockType: BlockType.REPORTER,
                    arguments: {
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: 'axisOptions',
                            defaultValue: AxisValues.X
                        }
                    }
                }
            ],
            menus: {
                pushPullOptions: {
                    acceptReporters: true,
                    items: this.PUSH_PULL_MENU
                },
                gestureOptions: {
                    acceptReporters: true,
                    items: this.GESTURE_MENU
                },
                axisOptions: {
                    acceptReporters: true,
                    items: this.AXIS_MENU
                },
                tiltOptions: {
                    acceptReporters: true,
                    items: this.TILT_MENU
                },
                tiltAnyOptions: {
                    acceptReporters: true,
                    items: this.TILT_MENU_ANY
                }
            }
        };
    }
}

module.exports = Scratch3GdxForBlocks;
