const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const TargetType = require('../../extension-support/target-type');
const formatMessage = require('format-message');

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU+cGVuLWljb248L3RpdGxlPjxnIHN0cm9rZT0iIzU3NUU3NSIgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik04Ljc1MyAzNC42MDJsLTQuMjUgMS43OCAxLjc4My00LjIzN2MxLjIxOC0yLjg5MiAyLjkwNy01LjQyMyA1LjAzLTcuNTM4TDMxLjA2NiA0LjkzYy44NDYtLjg0MiAyLjY1LS40MSA0LjAzMi45NjcgMS4zOCAxLjM3NSAxLjgxNiAzLjE3My45NyA0LjAxNUwxNi4zMTggMjkuNTljLTIuMTIzIDIuMTE2LTQuNjY0IDMuOC03LjU2NSA1LjAxMiIgZmlsbD0iI0ZGRiIvPjxwYXRoIGQ9Ik0yOS40MSA2LjExcy00LjQ1LTIuMzc4LTguMjAyIDUuNzcyYy0xLjczNCAzLjc2Ni00LjM1IDEuNTQ2LTQuMzUgMS41NDYiLz48cGF0aCBkPSJNMzYuNDIgOC44MjVjMCAuNDYzLS4xNC44NzMtLjQzMiAxLjE2NGwtOS4zMzUgOS4zYy4yODItLjI5LjQxLS42NjguNDEtMS4xMiAwLS44NzQtLjUwNy0xLjk2My0xLjQwNi0yLjg2OC0xLjM2Mi0xLjM1OC0zLjE0Ny0xLjgtNC4wMDItLjk5TDMwLjk5IDUuMDFjLjg0NC0uODQgMi42NS0uNDEgNC4wMzUuOTYuODk4LjkwNCAxLjM5NiAxLjk4MiAxLjM5NiAyLjg1NU0xMC41MTUgMzMuNzc0Yy0uNTczLjMwMi0xLjE1Ny41Ny0xLjc2NC44M0w0LjUgMzYuMzgybDEuNzg2LTQuMjM1Yy4yNTgtLjYwNC41My0xLjE4Ni44MzMtMS43NTcuNjkuMTgzIDEuNDQ4LjYyNSAyLjEwOCAxLjI4Mi42Ni42NTggMS4xMDIgMS40MTIgMS4yODcgMi4xMDIiIGZpbGw9IiM0Qzk3RkYiLz48cGF0aCBkPSJNMzYuNDk4IDguNzQ4YzAgLjQ2NC0uMTQuODc0LS40MzMgMS4xNjVsLTE5Ljc0MiAxOS42OGMtMi4xMyAyLjExLTQuNjczIDMuNzkzLTcuNTcyIDUuMDFMNC41IDM2LjM4bC45NzQtMi4zMTYgMS45MjUtLjgwOGMyLjg5OC0xLjIxOCA1LjQ0LTIuOSA3LjU3LTUuMDFsMTkuNzQzLTE5LjY4Yy4yOTItLjI5Mi40MzItLjcwMi40MzItMS4xNjUgMC0uNjQ2LS4yNy0xLjQtLjc4LTIuMTIyLjI1LjE3Mi41LjM3Ny43MzcuNjE0Ljg5OC45MDUgMS4zOTYgMS45ODMgMS4zOTYgMi44NTYiIGZpbGw9IiM1NzVFNzUiIG9wYWNpdHk9Ii4xNSIvPjxwYXRoIGQ9Ik0xOC40NSAxMi44M2MwIC41LS40MDQuOTA1LS45MDQuOTA1cy0uOTA1LS40MDUtLjkwNS0uOTA0YzAtLjUuNDA3LS45MDMuOTA2LS45MDMuNSAwIC45MDQuNDA0LjkwNC45MDR6IiBmaWxsPSIjNTc1RTc1Ii8+PC9nPjwvc3ZnPg==';

// aka nothing because every image is way too big just like your mother
const DefaultDrawImage = 'data:image/png;base64,'; 

/**
 * Enum for pen color parameter values.
 * @readonly
 * @enum {string}
 */
const ColorParam = {
    COLOR: 'color',
    SATURATION: 'saturation',
    BRIGHTNESS: 'brightness',
    TRANSPARENCY: 'transparency'
};

/**
 * Enum for layer parameter values.
 * @readonly
 * @enum {string}
 */
const LayerParam = {
    FRONT: 'front',
    BACK: 'back'
};

const ItalicsParam = {
    ON: 'on',
    OFF: 'off'
};


/**
 * @typedef {object} PenState - the pen state associated with a particular target.
 * @property {Boolean} penDown - tracks whether the pen should draw for this target.
 * @property {number} color - the current color (hue) of the pen.
 * @property {PenAttributes} penAttributes - cached pen attributes for the renderer. This is the authoritative value for
 *   diameter but not for pen color.
 */

const SANS_SERIF_ID = 'Sans Serif';
const SERIF_ID = 'Serif';
const HANDWRITING_ID = 'Handwriting';
const MARKER_ID = 'Marker';
const CURLY_ID = 'Curly';
const PIXEL_ID = 'Pixel';

/* PenguinMod Fonts */
const PLAYFUL_ID = 'Playful';
const BUBBLY_ID = 'Bubbly';
const BITSANDBYTES_ID = 'Bits and Bytes';
const TECHNOLOGICAL_ID = 'Technological';
const ARCADE_ID = 'Arcade';
const ARCHIVO_ID = 'Archivo';
const ARCHIVOBLACK_ID = 'Archivo Black';
const SCRATCH_ID = 'Scratch';

const RANDOM_ID = 'Random';

/**
 * Host for the Pen-related blocks in Scratch 3.0
 * @param {Runtime} runtime - the runtime instantiating this block package.
 * @constructor
 */
class Scratch3PenBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * The default pen state, to be used when a target has no existing pen state.
     * @type {PenState}
     */
    static get DEFAULT_PEN_STATE () {
        return {
            penDown: false,
            color: 66.66,
            saturation: 100,
            brightness: 100,
            transparency: 0,
            _shade: 50, // Used only for legacy `change shade by` blocks
            penAttributes: {
                color4f: [0, 0, 1, 1],
                diameter: 1
            }
        };
    }

    /**
     * Initialize color parameters menu with localized strings
     * @returns {array} of the localized text and values for each menu element
     * @private
     */
    _initColorParam () {
        return [
            {
                text: formatMessage({
                    id: 'pen.colorMenu.color',
                    default: 'color',
                    description: 'label for color element in color picker for pen extension'
                }),
                value: ColorParam.COLOR
            },
            {
                text: formatMessage({
                    id: 'pen.colorMenu.saturation',
                    default: 'saturation',
                    description: 'label for saturation element in color picker for pen extension'
                }),
                value: ColorParam.SATURATION
            },
            {
                text: formatMessage({
                    id: 'pen.colorMenu.brightness',
                    default: 'brightness',
                    description: 'label for brightness element in color picker for pen extension'
                }),
                value: ColorParam.BRIGHTNESS
            },
            {
                text: formatMessage({
                    id: 'pen.colorMenu.transparency',
                    default: 'transparency',
                    description: 'label for transparency element in color picker for pen extension'
                }),
                value: ColorParam.TRANSPARENCY

            }
        ];
    }

    getLayerParam () {
        return [
            {
                text: formatMessage({
                    id: 'pen.layerMenu.front',
                    default: 'front',
                    description: 'label for front'
                }),
                value: LayerParam.FRONT
            },
            {
                text: formatMessage({
                    id: 'pen.layerMenu.back',
                    default: 'back',
                    description: 'label for back'
                }),
                value: LayerParam.BACK
            }
        ];
    }
    
    getItalicsToggleParam () {
        return [
            {
                text: formatMessage({
                    id: 'pen.italicsToggle.on',
                    default: 'on',
                    description: 'label for on'
                }),
                value: ItalicsParam.ON
            },
            {
                text: formatMessage({
                    id: 'pen.italicsToggle.off',
                    default: 'off',
                    description: 'label for off'
                }),
                value: ItalicsParam.OFF
            }
        ];
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'pen',
            name: formatMessage({
                id: 'pen.categoryName',
                default: 'Pen',
                description: 'Label for the pen extension category'
            }),
            blockIconURI: blockIconURI,
            blocks: [
                {
                    blockType: BlockType.LABEL,
                    text: formatMessage({
                        id: 'pm.pen.stageSelected',
                        default: 'Stage selected: less pen blocks',
                        description: 'Label that appears in the Pen category when the stage is selected'
                    }),
                    filter: [TargetType.STAGE]
                },
                {
                    opcode: 'clear',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.clear',
                        default: 'erase all',
                        description: 'erase all pen trails and stamps'
                    })
                },
                {
                    opcode: 'stamp',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.stamp',
                        default: 'stamp',
                        description: 'render current costume on the background'
                    }),
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'penDown',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.penDown',
                        default: 'pen down',
                        description: 'start leaving a trail when the sprite moves'
                    }),
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'penUp',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.penUp',
                        default: 'pen up',
                        description: 'stop leaving a trail behind the sprite'
                    }),
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'setPenColorToColor',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setColor',
                        default: 'set pen color to [COLOR]',
                        description: 'set the pen color to a particular (RGB) value'
                    }),
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'changePenColorParamBy',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.changeColorParam',
                        default: 'change pen [COLOR_PARAM] by [VALUE]',
                        description: 'change the state of a pen color parameter'
                    }),
                    arguments: {
                        COLOR_PARAM: {
                            type: ArgumentType.STRING,
                            menu: 'colorParam',
                            defaultValue: ColorParam.COLOR
                        },
                        VALUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 10
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'setPenColorParamTo',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setColorParam',
                        default: 'set pen [COLOR_PARAM] to [VALUE]',
                        description: 'set the state for a pen color parameter e.g. saturation'
                    }),
                    arguments: {
                        COLOR_PARAM: {
                            type: ArgumentType.STRING,
                            menu: 'colorParam',
                            defaultValue: ColorParam.COLOR
                        },
                        VALUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 50
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'changePenSizeBy',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.changeSize',
                        default: 'change pen size by [SIZE]',
                        description: 'change the diameter of the trail left by a sprite'
                    }),
                    arguments: {
                        SIZE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'setPenSizeTo',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setSize',
                        default: 'set pen size to [SIZE]',
                        description: 'set the diameter of a trail left by a sprite'
                    }),
                    arguments: {
                        SIZE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'drawRect',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.drawRect',
                        default: 'use [COLOR] to draw a square on x:[X] y:[Y] width:[WIDTH] height:[HEIGHT]',
                        description: 'draw a square'
                    }),
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        WIDTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 10
                        },
                        HEIGHT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 10
                        }
                    }
                },
                {
                    opcode: 'drawArrayComplexShape',
                    blockType: BlockType.COMMAND,
                    text: 'draw polygon from points [SHAPE] with fill [COLOR]',
                    arguments: {
                        SHAPE: {
                            type: ArgumentType.STRING,
                            defaultValue: '[-20, 20, 20, 20, 0, -20]'
                        },
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    },
                    hideFromPalette: false
                },
                "---",
                {
                    opcode: 'preloadUriImage',
                    blockType: BlockType.COMMAND,
                    text: 'preload image [URI] as [NAME]',
                    arguments: {
                        URI: {
                            type: ArgumentType.STRING,
                            defaultValue: DefaultDrawImage
                        },
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "preloaded image"
                        }
                    }
                },
                {
                    opcode: 'unloadUriImage',
                    blockType: BlockType.COMMAND,
                    text: 'unload image [NAME]',
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "preloaded image"
                        }
                    }
                },
                {
                    opcode: 'drawUriImage',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.drawUriImage',
                        default: 'draw image [URI] at x:[X] y:[Y]',
                        description: 'draw image'
                    }),
                    arguments: {
                        URI: {
                            type: ArgumentType.STRING,
                            defaultValue: DefaultDrawImage
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'drawUriImageWHR',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.drawUriImageWHR',
                        default: 'draw image [URI] at x:[X] y:[Y] width:[WIDTH] height:[HEIGHT] pointed at: [ROTATE]',
                        description: 'draw image width height rotation'
                    }),
                    arguments: {
                        URI: {
                            type: ArgumentType.STRING,
                            defaultValue: DefaultDrawImage
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        WIDTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 64
                        },
                        HEIGHT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 64
                        },
                        ROTATE: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 90
                        }
                    }
                },
                {
                    opcode: 'drawUriImageWHCX1Y1X2Y2R',
                    blockType: BlockType.COMMAND,
                    text: 'draw image [URI] at x:[X] y:[Y] width:[WIDTH] height:[HEIGHT] cropping from x:[CROPX] y:[CROPY] width:[CROPW] height:[CROPH] pointed at: [ROTATE]',
                    arguments: {
                        URI: {
                            type: ArgumentType.STRING,
                            defaultValue: DefaultDrawImage
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        WIDTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 64
                        },
                        HEIGHT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 64
                        },
                        CROPX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        CROPY: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        CROPW: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        },
                        CROPH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        },
                        ROTATE: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 90
                        }
                    }
                },
                "---",
                {
                    opcode: 'printText',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.printText',
                        default: 'print [TEXT] on x:[X] y:[Y]',
                        description: 'print text'
                    }),
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Foobars are yummy'
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'setPrintFont',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setPrintFont',
                        default: 'set print font to [FONT]',
                        description: 'set print font'
                    }),
                    arguments: {
                        FONT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Arial',
                            menu: 'FONT'
                        }
                    }
                },
                {
                    opcode: 'setPrintFontSize',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setPrintFontSize',
                        default: 'set print font size to [SIZE]',
                        description: 'set print font size'
                    }),
                    arguments: {
                        SIZE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 24
                        }
                    }
                },
                {
                    opcode: 'setPrintFontColor',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setPrintFontColor',
                        default: 'set print font color to [COLOR]',
                        description: 'set print font color'
                    }),
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    }
                },
                {
                    opcode: 'setPrintFontStrokeColor',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setPrintFontStrokeColor',
                        default: 'set print stroke color to [COLOR]',
                        description: 'set print stroke color'
                    }),
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    }
                },
                {
                    opcode: 'setPrintFontStrokeWidth',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setPrintFontStrokeWidth',
                        default: 'set print stroke width to [WIDTH]',
                        description: 'set print stroke width'
                    }),
                    arguments: {
                        WIDTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'setPrintFontWeight',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setPrintFontWeight',
                        default: 'set print font weight to [WEIGHT]',
                        description: 'set print font weight'
                    }),
                    arguments: {
                        WEIGHT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 700
                        }
                    }
                },
                {
                    opcode: 'setPrintFontItalics',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setPrintFontItalics',
                        default: 'turn print font italics [OPTION]',
                        description: 'toggle print font italics'
                    }),
                    arguments: {
                        OPTION: {
                            type: ArgumentType.STRING,
                            menu: 'italicsToggleParam',
                            defaultValue: ItalicsParam.ON
                        }
                    }
                },
                /* Legacy blocks, should not be shown in flyout */
                {
                    opcode: 'drawComplexShape',
                    blockType: BlockType.COMMAND,
                    text: 'draw triangle [SHAPE] with fill [COLOR]',
                    arguments: {
                        SHAPE: {
                            type: ArgumentType.POLYGON,
                            nodes: 3
                        },
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'draw4SidedComplexShape',
                    blockType: BlockType.COMMAND,
                    text: 'draw quadrilateral [SHAPE] with fill [COLOR]',
                    arguments: {
                        SHAPE: {
                            type: ArgumentType.POLYGON,
                            nodes: 4
                        },
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'setPenShadeToNumber',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setShade',
                        default: 'LEGACY - set pen shade to [SHADE]',
                        description: 'legacy pen blocks - set pen shade'
                    }),
                    arguments: {
                        SHADE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'changePenShadeBy',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.changeShade',
                        default: 'LEGACY - change pen shade by [SHADE]',
                        description: 'legacy pen blocks - change pen shade'
                    }),
                    arguments: {
                        SHADE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'setPenHueToNumber',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.setHue',
                        default: 'LEGACY - set pen color to [HUE]',
                        description: 'legacy pen blocks - set pen color to number'
                    }),
                    arguments: {
                        HUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'changePenHueBy',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'pen.changeHue',
                        default: 'LEGACY - change pen color by [HUE]',
                        description: 'legacy pen blocks - change pen color'
                    }),
                    arguments: {
                        HUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'goPenLayer',
                    blockType: BlockType.COMMAND,
                    hideFromPalette: true,
                    text: formatMessage({
                        id: 'pen.GoPenLayer',
                        default: 'go to [OPTION] layer',
                        description: 'go to front layer(pen)'
                    }),
                    arguments: {
                        OPTION: {
                            type: ArgumentType.STRING,
                            menu: 'layerParam',
                            defaultValue: LayerParam.FRONT
                        }
                    }
                }
            ],
            menus: {
                colorParam: {
                    acceptReporters: true,
                    items: this._initColorParam()
                },
                layerParam: {
                    acceptReporters: false,
                    items: this.getLayerParam()
                },
                italicsToggleParam: {
                    acceptReporters: false,
                    items: this.getItalicsToggleParam()
                },
                FONT: {
                    items: [{
                        text: 'Sans Serif',
                        value: SANS_SERIF_ID
                    }, {
                        text: 'Serif',
                        value: SERIF_ID
                    }, {
                        text: 'Handwriting',
                        value: HANDWRITING_ID
                    }, {
                        text: 'Marker',
                        value: MARKER_ID
                    }, {
                        text: 'Curly',
                        value: CURLY_ID
                    }, {
                        text: 'Pixel',
                        value: PIXEL_ID
                    }, {
                        text: 'Playful',
                        value: PLAYFUL_ID
                    }, {
                        text: 'Bubbly',
                        value: BUBBLY_ID
                    }, {
                        text: 'Arcade',
                        value: ARCADE_ID
                    }, {
                        text: 'Bits and Bytes',
                        value: BITSANDBYTES_ID
                    }, {
                        text: 'Technological',
                        value: TECHNOLOGICAL_ID
                    }, {
                        text: 'Scratch',
                        value: SCRATCH_ID
                    }, {
                        text: 'Archivo',
                        value: ARCHIVO_ID
                    }, {
                        text: 'Archivo Black',
                        value: ARCHIVOBLACK_ID
                    },
                    {
                        text: 'random font',
                        value: RANDOM_ID
                    }],
                    isTypeable: true
                }
            }
        };
    }
}

module.exports = Scratch3PenBlocks;
