// Most of the blocks here are from More Motion by NexusKitten:
// https://scratch.mit.edu/users/NamelessCat/
// https://github.com/NexusKitten

const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');



/**
 * Class of idk
 * @constructor
 */
class pmMotionExpansion {
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
            id: 'pmMotionExpansion',
            name: 'Motion Expansion',
            color1: '#4C97FF',
            color2: '#4280D7',
            color3: '#3373CC',
            isDynamic: true,
            blocks: [
                {
                    opcode: "rotationStyle",
                    blockType: BlockType.REPORTER,
                    text: "rotation style",
                    disableMonitor: true,
                },
                {
                    opcode: "fence",
                    blockType: BlockType.COMMAND,
                    text: "manually fence",
                },
                {
                    opcode: "steptowards",
                    blockType: BlockType.COMMAND,
                    text: "move [STEPS] steps towards x: [X] y: [Y]",
                    arguments: {
                        STEPS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "10",
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                    },
                    switches: [
                        { isNoop: true },
                        "tweentowards"
                    ],
                    switchText: "move steps towards xy"
                },
                {
                    opcode: "tweentowards",
                    blockType: BlockType.COMMAND,
                    text: "move [PERCENT]% of the way to x: [X] y: [Y]",
                    arguments: {
                        PERCENT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "10",
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                    },
                    switches: [
                        "steptowards",
                        { isNoop: true },
                    ],
                    switchText: "move _% of the way to xy"
                },
                {
                    opcode: "touchingxy",
                    blockType: BlockType.BOOLEAN,
                    text: "touching x: [X] y: [Y]?",
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                    },
                    switches: [
                        { isNoop: true },
                        "touchingrect"
                    ],
                    switchText: "touching xy"
                },
                {
                    opcode: "touchingrect",
                    blockType: BlockType.BOOLEAN,
                    text: "touching rectangle x1: [X1] y1: [Y1] x2: [X2] y2: [Y2]?",
                    arguments: {
                        X1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "-100",
                        },
                        Y1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "-100",
                        },
                        X2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "100",
                        },
                        Y2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "100",
                        },
                    },
                    switches: [
                        "touchingxy",
                        { isNoop: true },
                    ],
                    switchText: "touching rectangle"
                },
                {
                    opcode: "setHome",
                    blockType: BlockType.COMMAND,
                    text: "set my home",
                    switches: [
                        { isNoop: true },
                        "gotoHome"
                    ]
                },
                {
                    opcode: "gotoHome",
                    blockType: BlockType.COMMAND,
                    text: "go to home",
                    switches: [
                        "setHome",
                        { isNoop: true }
                    ]
                },
                {
                    opcode: "motion_turnrightaroundxy",
                    ppm_final_opcode: true,
                    blockType: BlockType.COMMAND,
                    text: "turn clockwise [DEGREES] around x: [X] y: [Y]", // Icons do not matter
                    arguments: {
                        DEGREES: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "15",
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                    },
                },
                {
                    opcode: "motion_turnleftaroundxy",
                    ppm_final_opcode: true,
                    blockType: BlockType.COMMAND,
                    text: "turn counterclockwise [DEGREES] around x: [X] y: [Y]", // Icons do not matter
                    arguments: {
                        DEGREES: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "15",
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                    },
                },
                {
                    opcode: "motion_ifonxybounce",
                    ppm_final_opcode: true,
                    blockType: BlockType.COMMAND,
                    text: "if touching x: [X] y: [Y], bounce", // Icons do not matter
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                    },
                },
            ]
        };
    }
}

module.exports = pmMotionExpansion;
