const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const EasingMethods = {
    linear: null,
    sine: null,
    quad: null,
    cubic: null,
    quart: null,
    quint: null,
    expo: null,
    circ: null,
    back: null,
    elastic: null,
    bounce: null,
};

class Tween {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }
    getInfo() {
        return {
            id: "jgTween",
            name: "Tweening",
            blocks: [
                {
                    opcode: "tweenValue",
                    text: formatMessage({
                        id: 'jgTween.blocks.tweenValue',
                        default: '[MODE] ease [DIRECTION] [START] to [END] by [AMOUNT]%',
                        description: 'Block for easing a value with a certain mode and direction by a certain amount.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        MODE: {
                            type: ArgumentType.STRING,
                            menu: "modes"
                        },
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: "direction"
                        },
                        START: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        END: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        },
                        AMOUNT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 50
                        }
                    }
                },
                {
                    opcode: "tweenVariable",
                    text: "tween variable [VAR] to [VALUE] over [SEC] seconds using [MODE] ease [DIRECTION]",
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VAR: {
                            type: ArgumentType.STRING,
                            menu: "vars"
                        },
                        VALUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        },
                        SEC: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        MODE: {
                            type: ArgumentType.STRING,
                            menu: "modes"
                        },
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: "direction"
                        }
                    }
                },
                {
                    opcode: "tweenXY",
                    text: "tween to x: [X] y: [Y] over [SEC] seconds using [MODE] ease [DIRECTION]",
                    blockType: BlockType.COMMAND,
                    arguments: {
                        PROPERTY: {
                            type: ArgumentType.STRING,
                            menu: "properties"
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        },
                        SEC: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        MODE: {
                            type: ArgumentType.STRING,
                            menu: "modes"
                        },
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: "direction"
                        }
                    }
                },
                {
                    opcode: "tweenProperty",
                    text: "tween [PROPERTY] to [VALUE] over [SEC] seconds using [MODE] ease [DIRECTION]",
                    blockType: BlockType.COMMAND,
                    arguments: {
                        PROPERTY: {
                            type: ArgumentType.STRING,
                            menu: "properties"
                        },
                        VALUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        },
                        SEC: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        MODE: {
                            type: ArgumentType.STRING,
                            menu: "modes"
                        },
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: "direction"
                        }
                    }
                },
                "---",
                {
                    opcode: "tweenVariableCancel",
                    text: "cancel tween for variable [VAR]",
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VAR: {
                            type: ArgumentType.STRING,
                            menu: "vars"
                        }
                    }
                },
                {
                    opcode: "tweenPropertyCancel",
                    text: "cancel tween for [PROPERTY]",
                    blockType: BlockType.COMMAND,
                    arguments: {
                        PROPERTY: {
                            type: ArgumentType.STRING,
                            menu: "properties"
                        }
                    }
                },
                "---",
                {
                    opcode: "tweenC", blockType: BlockType.LOOP,
                    text: "[MODE] ease [DIRECTION] [CHANGE] [START] to [END] in [SEC] secs",
                    arguments: {
                        MODE: {
                            type: ArgumentType.STRING,
                            menu: "modes",
                        },
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: "direction",
                        },
                        CHANGE: {
                            type: ArgumentType.STRING,
                            fillIn: "tweenVal"
                        },
                        START: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0,
                        },
                        END: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100,
                        },
                        SEC: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1,
                        }, 
                    }
                },
                {
                    opcode: "tweenVal", blockType: BlockType.REPORTER,
                    text: "tween value", canDragDuplicate: true, hideFromPalette: true
                },
            ],
            menus: {
                modes: {
                    acceptReporters: true,
                    items: Object.keys(EasingMethods)
                },
                direction: {
                    acceptReporters: true,
                    items: ["in", "out", "in out"]
                },
                vars: {
                    acceptReporters: false, // for Scratch parity
                    items: "getVariables"
                },
                properties: {
                    acceptReporters: true,
                    items: ["x position", "y position", "direction", "size"]
                }
            }
        };
    }
}

module.exports = Tween;
