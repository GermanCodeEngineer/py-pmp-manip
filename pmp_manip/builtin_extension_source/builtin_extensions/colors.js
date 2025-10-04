const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for TurboWarp blocks
 * @constructor
 */
class colorBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    deafultHsv = '{"h": 360, "s": 1, "v": 1}';
    deafultRgb = '{"r": 255, "g": 0, "b": 0}';
    deafultHex = '#ff0000';
    deafultDecimal = '16711680';

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'colors',
            name: 'Colors',
            color1: '#ff4c4c',
            color2: '#e64444',
            blocks: [
                {
                    opcode: 'colorPicker',
                    text: '[OUTPUT] of [COLOR]',
                    disableMonitor: true,
                    arguments: {
                        OUTPUT: {
                            type: ArgumentType.STRING,
                            menu: "outputColorType"
                        },
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'defaultBlack',
                    text: 'black',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'defaultWhite',
                    text: 'white',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                {
                    blockType: BlockType.LABEL,
                    text: 'RGB'
                },
                {
                    opcode: 'rgbToDecimal',
                    text: 'rgb [color] to decimal',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultRgb
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'rgbToHex',
                    text: 'rgb [color] to hex',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultRgb
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'rgbToHsv',
                    text: 'rgb [color] to hsv',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultRgb
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    blockType: BlockType.LABEL,
                    text: 'Hex'
                },
                {
                    opcode: 'hexToDecimal',
                    text: 'hex [color] to decimal',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultHex
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'hexToRgb',
                    text: 'hex [color] to rgb',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultHex
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'hexToHsv',
                    text: 'hex [color] to hsv',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultHex
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    blockType: BlockType.LABEL,
                    text: 'Decimal'
                },
                {
                    opcode: 'decimalToHex',
                    text: 'decimal [color] to hex',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultDecimal
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'decimalToRgb',
                    text: 'decimal [color] to rgb',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultDecimal
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'decimalToHsv',
                    text: 'decimal [color] to hsv',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultDecimal
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    blockType: BlockType.LABEL,
                    text: 'HSV'
                },
                {
                    opcode: 'hsvToHex',
                    text: 'hsv [color] to hex',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultHsv
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'hsvToRgb',
                    text: 'hsv [color] to rgb',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultHsv
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'hsvToDecimal',
                    text: 'hsv [color] to decimal',
                    arguments: {
                        color: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultHsv
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                "---",
                {
                    blockType: BlockType.LABEL,
                    text: 'Other'
                },
                {
                    opcode: 'csbMaker',
                    text: 'color: [h] saturation: [s] brightness: [v] transparency: [a]',
                    arguments: {
                        h: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        s: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        v: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        a: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'hsvMaker',
                    text: 'h: [h] s: [s] v: [v] a: [a]',
                    arguments: {
                        h: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        s: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        v: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        a: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'rgbMaker',
                    text: 'r: [r] g: [g] b: [b] a: [a]',
                    arguments: {
                        r: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        g: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        b: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        a: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'mixColors',
                    text: 'mix [color1] [color2] by [percent]',
                    arguments: {
                        color1: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultRgb
                        },
                        color2: {
                            type: ArgumentType.STRING,
                            defaultValue: this.deafultRgb
                        },
                        percent: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0.5'
                        }
                    },
                    blockType: BlockType.REPORTER
                }
            ],
            menus: {
                outputColorType: {
                    items: [
                        { text: 'decimal', value: "decimal" },
                        { text: 'rgb', value: "rgb" },
                        { text: 'hsv', value: "hsv" },
                        { text: 'hex', value: "hex" }
                    ],
                    acceptReporters: true
                }
            }
        };
    }
}

module.exports = colorBlocks;
