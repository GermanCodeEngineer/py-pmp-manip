/* eslint-disable no-multi-spaces */
/* eslint-disable no-invalid-this */
/* eslint-disable no-undef */
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const DefaultDrawImage = 'https://studio.penguinmod.com/favicon.ico'; 
const canvasPropInfos = [
    ['compositing method', 'globalCompositeOperation', [
        ['source over', 'source-over'],
        ['source in', 'source-in'],
        ['source out', 'source-out'],
        ['source atop', 'source-atop'],
        ['destination over', 'destination-over'],
        ['destination in', 'destination-in'],
        ['destination out', 'destination-out'],
        ['destination atop', 'destination-atop'],
        ['lighter', 'lighter'],
        ['copy', 'copy'],
        ['xor', 'xor'],
        ['multiply', 'multiply'],
        ['screen', 'screen'],
        ['overlay', 'overlay'],
        ['darken', 'darken'],
        ['lighten', 'lighten'],
        ['color dodge', 'color-dodge'],
        ['color burn', 'color-burn'],
        ['hard light', 'hard-light'],
        ['soft light', 'soft-light'],
        ['difference', 'difference'],
        ['exclusion', 'exclusion'],
        ['hue', 'hue'],
        ['saturation', 'saturation'],
        ['color', 'color'],
        ['luminosity', 'luminosity']
    ], 'source-over'],
    ['CSS filter', 'filter', ArgumentType.STRING, 'none'],
    ['font', 'font', ArgumentType.STRING, ''],
    ['font kerning method', 'fontKerning', [
        ['browser defined', 'auto'],
        ['font defined', 'normal'],
        ['none', 'none']
    ], 'normal'],
    ['font stretch', 'fontStretch', [
        ['ultra condensed', 'ultra-condensed'],
        ['extra condensed', 'extra-condensed'],
        ['condensed', 'condensed'],
        ['normal', 'normal'],
        ['semi expanded', 'semi-expanded'],
        ['expanded', 'expanded'],
        ['extra expanded', 'extra-expanded'],
        ['ultra expanded', 'ultra-expanded']
    ], 'normal'],
    ['font case sizing', 'fontVariantCaps', [
        ['normal', 'normal'],
        ['uni-case', 'unicase'],
        ['titling-case', 'titling-caps'],
        ['smaller uppercase', 'small-caps'],
        ['smaller cased characters', 'all-small-caps'],
        ['petite uppercase', 'petite-caps'],
        ['petite cased characters', 'all-petite-caps']
    ], 'normal'],
    ['transparency', 'globalAlpha', ArgumentType.NUMBER, '0'],
    ['image smoothing', 'imageSmoothingEnabled', ArgumentType.BOOLEAN, ''],
    ['image smoothing quality', 'imageSmoothingQuality', [
        ['low', 'low'],
        ['medium', 'medium'],
        ['high', 'high']
    ], 'low'],
    ['letter spacing', 'letterSpacing', ArgumentType.NUMBER, '0'],
    ['line cap shape', 'lineCap', [
        ['sharp', 'butt'],
        ['round', 'round'],
        ['square', 'square']
    ], 'butt'],
    ['line dash offset', 'lineDashOffset', ArgumentType.NUMBER, '0'],
    ['line join shape', 'lineJoin', [
        ['round', 'round'],
        ['beveled', 'bevel'],
        ['sharp', 'miter']
    ], 'miter'],
    ['line size', 'lineWidth', ArgumentType.NUMBER, '1'],
    ['sharp line join limit', 'miterLimit', ArgumentType.NUMBER, '10'],
    ['shadow blur', 'shadowBlur', ArgumentType.NUMBER, '0'],
    ['shadow color', 'shadowColor', ArgumentType.COLOR, null],
    ['shadow X offset', 'shadowOffsetX', ArgumentType.NUMBER, '0'],
    ['shadow Y offset', 'shadowOffsetY', ArgumentType.NUMBER, '0'],
    ['line color', 'strokeStyle', ArgumentType.COLOR, null],
    ['text horizontal alignment', 'textAlign', [
        ['start', 'start'],
        ['left', 'left'],
        ['center', 'center'],
        ['right', 'right'],
        ['end', 'end']
    ], 'start'],
    ['text vertical alignment', 'textBaseline', [
        ['top', 'top'],
        ['hanging', 'hanging'],
        ['middle', 'middle'],
        ['alphabetic', 'alphabetic'],
        ['ideographic', 'ideographic'],
        ['bottom', 'bottom']
    ], 'alphabetic'],
    ['text rendering optimisation', 'textRendering', [
        ['auto', 'auto'],
        ['render speed', 'optimizeSpeed'],
        ['legibility', 'optimizeLegibility'],
        ['geometric precision', 'geometricPrecision']
    ], 'auto'],
    ['word spacing', 'wordSpacing', ArgumentType.NUMBER, '0']
];

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
        this.propList = [];
        for (const item of canvasPropInfos) {
            this.propList.push(item.slice(0, 2));
        }
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'newCanvas',
            name: 'html canvas',
            color1: '#0069c2',
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
                            menu: 'canvas'
                        }
                    },
                    text: '[canvas]'
                },
                {
                    blockType: BlockType.LABEL,
                    text: "stylizing"
                },
                {
                    opcode: 'setSize',
                    text: 'set width: [width] height: [height] of [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
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
                    opcode: 'setProperty',
                    text: 'set [prop] of [canvas] to ',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        prop: {
                            type: ArgumentType.STRING,
                            menu: 'canvasProps'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'getProperty',
                    text: 'get [prop] of [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        prop: {
                            type: ArgumentType.STRING,
                            menu: 'canvasProps'
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'dash',
                    blockType: BlockType.COMMAND,
                    text: 'set line dash to [dashing] in [canvas]',
                    arguments: {
                        dashing: {
                            type: ArgumentType.STRING,
                            defaultValue: '[10, 10]'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    blockType: BlockType.LABEL,
                    text: "direct drawing"
                },
                {
                    opcode: 'clearCanvas',
                    text: 'clear canvas [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
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
                            menu: 'canvas'
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
                    opcode: 'drawText',
                    text: 'draw text [text] at [x] [y] onto [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: 'photos printed'
                        },
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'drawTextWithCap',
                    text: 'draw text [text] at [x] [y] with size cap [cap] onto [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: 'photos printed'
                        },
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        cap: {
                            type: ArgumentType.NUMBER,
                            defauleValue: '10'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'outlineText',
                    text: 'draw text outline for [text] at [x] [y] onto [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: 'photos printed'
                        },
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'outlineTextWithCap',
                    text: 'draw text outline for [text] at [x] [y] with size cap [cap] onto [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: 'photos printed'
                        },
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        cap: {
                            type: ArgumentType.NUMBER,
                            defauleValue: '10'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'drawRect',
                    text: 'draw rectangle at x: [x] y: [y] with width: [width] height: [height] on [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
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
                    opcode: 'outlineRect',
                    text: 'draw rectangle outline at x: [x] y: [y] with width: [width] height: [height] on [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
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
                    opcode: 'preloadUriImage',
                    blockType: BlockType.COMMAND,
                    text: 'preload image [URI] as [NAME]',
                    arguments: {
                        URI: {
                            type: ArgumentType.STRING,
                            exemptFromNormalization: true,
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
                    opcode: 'getWidthOfPreloaded',
                    blockType: BlockType.REPORTER,
                    text: 'get width of [name]',
                    arguments: {
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: "preloaded image"
                        }
                    }
                },
                {
                    opcode: 'getHeightOfPreloaded',
                    blockType: BlockType.REPORTER,
                    text: 'get height of [name]',
                    arguments: {
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: "preloaded image"
                        }
                    }
                },
                {
                    opcode: 'drawUriImage',
                    blockType: BlockType.COMMAND,
                    text: 'draw image [URI] at x:[X] y:[Y] onto canvas [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        URI: {
                            type: ArgumentType.STRING,
                            exemptFromNormalization: true,
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
                    text: 'draw image [URI] at x:[X] y:[Y] width:[WIDTH] height:[HEIGHT] pointed at: [ROTATE] onto canvas [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        URI: {
                            type: ArgumentType.STRING,
                            exemptFromNormalization: true,
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
                    text: 'draw image [URI] at x:[X] y:[Y] width:[WIDTH] height:[HEIGHT] cropping from x:[CROPX] y:[CROPY] width:[CROPW] height:[CROPH] pointed at: [ROTATE] onto canvas [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        },
                        URI: {
                            type: ArgumentType.STRING,
                            exemptFromNormalization: true,
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
                {
                    blockType: BlockType.LABEL,
                    text: "path drawing"
                },
                {
                    opcode: 'beginPath',
                    blockType: BlockType.COMMAND,
                    text: 'begin path drawing on [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'moveTo',
                    blockType: BlockType.COMMAND,
                    text: 'move pen to x:[x] y:[y] on [canvas]',
                    arguments: {
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'lineTo',
                    blockType: BlockType.COMMAND,
                    text: 'add line going to x:[x] y:[y] on [canvas]',
                    arguments: {
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'arcTo',
                    blockType: BlockType.COMMAND,
                    text: 'add arc going to x:[x] y:[y] on [canvas] with control points [controlPoints] and radius [radius]',
                    arguments: {
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        controlPoints: {
                            type: ArgumentType.POLYGON,
                            nodes: 2
                        },
                        radius: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                "---",
                {
                    opcode: 'addRect',
                    blockType: BlockType.COMMAND,
                    text: 'add a rectangle at x:[x] y:[y] with width:[width] height:[height] to [canvas]',
                    arguments: {
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
                            defaultValue: 10
                        },
                        height: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 10
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'addEllipse',
                    blockType: BlockType.COMMAND,
                    text: 'add a ellipse at x:[x] y:[y] with width:[width] height:[height] pointed towards [dir] to [canvas]',
                    arguments: {
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
                            defaultValue: 10
                        },
                        height: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 10
                        },
                        dir: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 90
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'addEllipseStartStop',
                    blockType: BlockType.COMMAND,
                    text: 'add a ellipse with starting rotation [start] and ending rotation [end] at x:[x] y:[y] with width:[width] height:[height] pointed towards [dir] to [canvas]',
                    arguments: {
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
                            defaultValue: 10
                        },
                        height: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 10
                        },
                        start: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        end: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '360'
                        },
                        dir: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 90
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                "---",
                {
                    opcode: 'closePath',
                    blockType: BlockType.COMMAND,
                    text: 'attempt to close any open path in [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'stroke',
                    blockType: BlockType.COMMAND,
                    text: 'draw outline for current path in [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'fill',
                    blockType: BlockType.COMMAND,
                    text: 'draw fill for current path in [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    blockType: BlockType.LABEL,
                    text: "transforms"
                },
                {
                    opcode: 'saveTransform',
                    blockType: BlockType.COMMAND,
                    text: 'save [canvas]\'s transform',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'restoreTransform',
                    blockType: BlockType.COMMAND,
                    text: 'reset to [canvas]\'s saved transform',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                "---",
                {
                    opcode: 'turnRotationLeft',
                    blockType: BlockType.COMMAND,
                    text: 'turn left [degrees] in [canvas]',
                    arguments: {
                        degrees: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '90'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'turnRotationRight',
                    blockType: BlockType.COMMAND,
                    text: 'turn right [degrees] in [canvas]',
                    arguments: {
                        degrees: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '90'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'setRotation',
                    blockType: BlockType.COMMAND,
                    text: 'set rotation to [degrees] in [canvas]',
                    arguments: {
                        degrees: {
                            type: ArgumentType.ANGLE,
                            defaultValue: '90'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                "---",
                {
                    opcode: 'setTranslateXY',
                    blockType: BlockType.COMMAND,
                    text: 'set translation X: [x] Y: [y] on [canvas]',
                    arguments: {
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'changeTranslateXY',
                    blockType: BlockType.COMMAND,
                    text: 'change translation X: [x] Y: [y] on [canvas]',
                    arguments: {
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                "---",
                {
                    opcode: 'changeTranslateX',
                    blockType: BlockType.COMMAND,
                    text: 'change X translation by [amount] on [canvas]',
                    arguments: {
                        amount: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'setTranslateX',
                    blockType: BlockType.COMMAND,
                    text: 'set X scaler to [amount] on [canvas]',
                    arguments: {
                        amount: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'changeTranslateY',
                    blockType: BlockType.COMMAND,
                    text: 'change Y translation by [amount] on [canvas]',
                    arguments: {
                        amount: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'setTranslateY',
                    blockType: BlockType.COMMAND,
                    text: 'set Y translation by [amount] on [canvas]',
                    arguments: {
                        amount: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                "---",
                {
                    opcode: 'changeScaleXY',
                    blockType: BlockType.COMMAND,
                    text: 'change XY scaler by [percent]% on [canvas]',
                    arguments: {
                        percent: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'setScaleXY',
                    blockType: BlockType.COMMAND,
                    text: 'set XY scaler to [percent]% on [canvas]',
                    arguments: {
                        percent: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'changeScaleX',
                    blockType: BlockType.COMMAND,
                    text: 'change X scaler by [percent]% on [canvas]',
                    arguments: {
                        percent: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'setScaleX',
                    blockType: BlockType.COMMAND,
                    text: 'set X scaler to [percent]% on [canvas]',
                    arguments: {
                        percent: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'changeScaleY',
                    blockType: BlockType.COMMAND,
                    text: 'change Y scaler by [percent]% on [canvas]',
                    arguments: {
                        percent: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'setScaleY',
                    blockType: BlockType.COMMAND,
                    text: 'set Y scaler to [percent]% on [canvas]',
                    arguments: {
                        percent: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '50'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                "---",
                {
                    opcode: 'resetTransform',
                    blockType: BlockType.COMMAND,
                    text: 'clear transform in [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'loadTransform',
                    blockType: BlockType.COMMAND,
                    text: 'set new transform [transform] on [canvas]',
                    arguments: {
                        transform: {
                            type: ArgumentType.STRING,
                            defaultValue: '[1, 0, 0, 1, 0, 0]'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'getTransform',
                    blockType: BlockType.REPORTER,
                    text: 'get current transform in [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    blockType: BlockType.LABEL,
                    text: "utilizing"
                },
                {
                    opcode: 'putOntoSprite',
                    blockType: BlockType.COMMAND,
                    text: 'set this sprites costume to [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'getDataURI',
                    blockType: BlockType.REPORTER,
                    text: 'get data URL of [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'getWidthOfCanvas',
                    blockType: BlockType.REPORTER,
                    text: 'get width of [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'getHeightOfCanvas',
                    blockType: BlockType.REPORTER,
                    text: 'get height of [canvas]',
                    arguments: {
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                },
                {
                    opcode: 'getDrawnWidthOfText',
                    blockType: BlockType.REPORTER,
                    text: 'get [dimension] of text [text] when drawn to [canvas]',
                    arguments: {
                        dimension: {
                            type: ArgumentType.STRING,
                            menu: 'textDimension'
                        },
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: 'bogos binted'
                        },
                        canvas: {
                            type: ArgumentType.STRING,
                            menu: 'canvas'
                        }
                    }
                }
            ],
            menus: {
                textDimension: {
                    items: [
                        'width',
                        'height',
                        ['bounding box left', 'actualBoundingBoxLeft'],
                        ['bounding box right', 'actualBoundingBoxRight'],
                        ['bounding box ascent', 'actualBoundingBoxAscent'],
                        ['bounding box descent', 'actualBoundingBoxDescent'],
                        ['font bounding box ascent', 'fontBoundingBoxAscent'],
                        ['font bounding box descent', 'fontBoundingBoxDescent']
                        // maby add the other ones but the em ones be hella spotty
                    ]
                },
                canvas: {
                    variableType: 'canvas'
                },
                canvasProps: {
                    items: this.propList
                }
            }
        };
    }

}

module.exports = canvas;
