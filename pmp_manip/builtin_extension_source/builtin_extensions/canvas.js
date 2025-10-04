const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class
 * @constructor
 */
class canvas {
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
            id: 'canvas',
            name: 'html canvas',
            color1: '#0069c2',
            color2: '#0060B4',
            color3: '#0060B4',
            isDynamic: true,
            blocks: [
                {
                    opcode: 'createNewCanvas',
                    blockType: BlockType.BUTTON,
                    text: 'create new canvas'
                },
                {
                    opcode: 'canvasGetter',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: '{canvasId}'
                        }
                    },
                    text: '[canvas]'
                },
                {
                    blockType: BlockType.LABEL,
                    text: "config"
                },
                {
                    opcode: 'setGlobalCompositeOperation',
                    text: 'set composite operation of [canvas] to [CompositeOperation]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        },
                        CompositeOperation: {
                            type: ArgumentType.STRING,
                            menu: 'CompositeOperation',
                            defaultValue: ""
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'setSize',
                    text: 'set width: [width] height: [height] of [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        },
                        width: {
                            type: ArgumentType.NUMBER,
                            defaultValue: this.runtime.stageWidth
                        },
                        height: {
                            type: ArgumentType.NUMBER,
                            defaultValue: this.runtime.stageHeight
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'setTransparency',
                    text: 'set transparency of [canvas] to [transparency]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        },
                        transparency: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'setFill',
                    text: 'set fill color of [canvas] to [color]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        },
                        color: {
                            type: ArgumentType.COLOR
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'setBorderColor',
                    text: 'set border color of [canvas] to [color]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        },
                        color: {
                            type: ArgumentType.COLOR
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    blockType: BlockType.LABEL,
                    text: "drawing"
                },
                {
                    opcode: 'clearCanvas',
                    text: 'clear canvas [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'clearAria',
                    text: 'clear area at x: [x] y: [y] with width: [width] height: [height] on [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        },
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        width: {
                            type: ArgumentType.NUMBER,
                            defaultValue: this.runtime.stageWidth
                        },
                        height: {
                            type: ArgumentType.NUMBER,
                            defaultValue: this.runtime.stageHeight
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                '---',
                {
                    opcode: 'drawRect',
                    text: 'draw rectangle at x: [x] y: [y] with width: [width] height: [height] on [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        },
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        width: {
                            type: ArgumentType.NUMBER,
                            defaultValue: this.runtime.stageWidth
                        },
                        height: {
                            type: ArgumentType.NUMBER,
                            defaultValue: this.runtime.stageHeight
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'drawImage',
                    text: 'draw image [src] at x: [x] y: [y] on [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas',
                            defaultValue: ""
                        },
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        src: {
                            type: ArgumentType.STRING,
                            defaultValue: 'https://studio.penguinmod.com/favicon.ico'
                        }
                    },
                    blockType: BlockType.COMMAND
                }
            ],
            menus: {
                canvas: 'getCanvasMenuItems',
                CompositeOperation: {
                    items: [
                        {
                            "text": "source-over",
                            "value": "source-over"
                        },
                        {
                            "text": "source-in",
                            "value": "source-in"
                        },
                        {
                            "text": "source-out",
                            "value": "source-out"
                        },
                        {
                            "text": "source-atop",
                            "value": "source-atop"
                        },
                        {
                            "text": "destination-over",
                            "value": "destination-over"
                        },
                        {
                            "text": "destination-in",
                            "value": "destination-in"
                        },
                        {
                            "text": "destination-out",
                            "value": "destination-out"
                        },
                        {
                            "text": "destination-atop",
                            "value": "destination-atop"
                        },
                        {
                            "text": "lighter",
                            "value": "lighter"
                        },
                        {
                            "text": "copy",
                            "value": "copy"
                        },
                        {
                            "text": "xor",
                            "value": "xor"
                        },
                        {
                            "text": "multiply",
                            "value": "multiply"
                        },
                        {
                            "text": "screen",
                            "value": "screen"
                        },
                        {
                            "text": "overlay",
                            "value": "overlay"
                        },
                        {
                            "text": "darken",
                            "value": "darken"
                        },
                        {
                            "text": "lighten",
                            "value": "lighten"
                        },
                        {
                            "text": "color-dodge",
                            "value": "color-dodge"
                        },
                        {
                            "text": "color-burn",
                            "value": "color-burn"
                        },
                        {
                            "text": "hard-light",
                            "value": "hard-light"
                        },
                        {
                            "text": "soft-light",
                            "value": "soft-light"
                        },
                        {
                            "text": "difference",
                            "value": "difference"
                        },
                        {
                            "text": "exclusion",
                            "value": "exclusion"
                        },
                        {
                            "text": "hue",
                            "value": "hue"
                        },
                        {
                            "text": "saturation",
                            "value": "saturation"
                        },
                        {
                            "text": "color",
                            "value": "color"
                        },
                        {
                            "text": "luminosity",
                            "value": "luminosity"
                        }
                    ]
                }
            }
        };
    }
}

module.exports = canvas;
