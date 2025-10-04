// Created by TheShovel
// https://github.com/TheShovel
//
// Extra modifications: (their names will be listed nearby their changes for convenience)
//      SharkPool
//      https://github.com/SharkPool-SP
//
// 99% of the code here was not created by a PenguinMod developer!
// Look above for proper crediting :)

const ArgumentType = require("../../extension-support/argument-type");
const BlockType = require("../../extension-support/block-type");

class CanvasEffects {
    constructor(runtime) {
        this.runtime = runtime;
    }

    getInfo() {
        return {
            id: "theshovelcanvaseffects",
            name: "Canvas Effects",
            blocks: [
                {
                    opcode: "seteffect",
                    blockType: BlockType.COMMAND,
                    text: "set canvas [EFFECT] to [NUMBER]",
                    arguments: {
                        EFFECT: {
                            type: ArgumentType.STRING,
                            menu: "EFFECTMENU",
                        },
                        NUMBER: {
                            type: ArgumentType.NUMBER,
                        },
                    },
                },
                {
                    opcode: "changeEffect",
                    blockType: BlockType.COMMAND,
                    text: "change canvas [EFFECT] by [NUMBER]",
                    arguments: {
                        EFFECT: {
                            type: ArgumentType.STRING,
                            menu: "EFFECTMENU",
                        },
                        NUMBER: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 5,
                        },
                    },
                },
                {
                    opcode: "geteffect",
                    blockType: BlockType.REPORTER,
                    text: "get canvas [EFFECT]",
                    arguments: {
                        EFFECT: {
                            type: ArgumentType.STRING,
                            menu: "EFFECTGETMENU",
                        },
                    },
                },
                {
                    opcode: "setBorder",
                    blockType: BlockType.COMMAND,
                    text: "add [BORDER] border to canvas with color [COLOR1] and backup [COLOR2] and thickness [THICK]",
                    arguments: {
                        BORDER: {
                            type: ArgumentType.STRING,
                            menu: "BORDERTYPES",
                        },
                        THICK: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 5,
                        },
                        COLOR1: {
                            type: ArgumentType.COLOR,
                            defaultValue: "#ff0000",
                        },
                        COLOR2: {
                            type: ArgumentType.COLOR,
                            defaultValue: "#0000ff",
                        },
                    },
                },
                {
                    opcode: "setImage",
                    blockType: BlockType.COMMAND,
                    text: "set canvas image to [IMAGE] scaled [AMT]%",
                    hideFromPalette: true, // only appears when stage BG is transparent
                    arguments: {
                        IMAGE: {
                            type: ArgumentType.STRING,
                            defaultValue: "https://extensions.turbowarp.org/dango.png",
                        },
                        AMT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100,
                        },
                    },
                },
                {
                    opcode: "cleareffects",
                    blockType: BlockType.COMMAND,
                    text: "clear canvas effects",
                },
                {
                    opcode: "renderscale",
                    blockType: BlockType.COMMAND,
                    text: "set canvas render size to width:[X] height:[Y]",
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100,
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100,
                        },
                    },
                },
                {
                    opcode: "setrendermode",
                    blockType: BlockType.COMMAND,
                    text: "set canvas resize rendering mode [EFFECT]",
                    arguments: {
                        EFFECT: {
                            type: ArgumentType.STRING,
                            menu: "RENDERMODE",
                        },
                    },
                },
            ],
            menus: {
                EFFECTMENU: {
                    acceptReporters: true,
                    items: [
                        "blur",
                        "contrast",
                        "saturation",
                        "color shift",
                        "brightness",
                        "invert",
                        "sepia",
                        "transparency",
                        "scale",
                        "skew X",
                        "skew Y",
                        "offset X",
                        "offset Y",
                        "rotation",
                        "border radius",
                    ],
                },
                RENDERMODE: {
                    acceptReporters: true,
                    items: ["pixelated", "default"],
                },
                EFFECTGETMENU: {
                    acceptReporters: true,
                    // this contains 'resize rendering mode', EFFECTMENU does not
                    items: [
                        "blur",
                        "contrast",
                        "saturation",
                        "color shift",
                        "brightness",
                        "invert",
                        "resize rendering mode",
                        "sepia",
                        "transparency",
                        "scale",
                        "skew X",
                        "skew Y",
                        "offset X",
                        "offset Y",
                        "rotation",
                        "border radius",
                    ],
                },
                BORDERTYPES: {
                    acceptReporters: true,
                    items: [
                        "dotted",
                        "dashed",
                        "solid",
                        "double",
                        "groove",
                        "ridge",
                        "inset",
                        "outset",
                        "none",
                    ],
                },
            },
        };
    }
}

module.exports = CanvasEffects;
