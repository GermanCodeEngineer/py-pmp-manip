const ArgumentType = require("../../extension-support/argument-type");
const BlockType = require("../../extension-support/block-type");

class sharkpoolPrinting {
    constructor(runtime) {
        this.runtime = runtime;
    }
    getInfo() {
        return {
            id: "sharkpoolPrinting",
            name: "Printing",
            blocks: [
                {
                    opcode: "isPrintingSupported",
                    blockType: BlockType.BOOLEAN,
                    text: "is printing supported?",
                    // actually seems like browsers havent deprecated this even though it causes crashes in certain browsers
                    hideFromPalette: true,
                    disableMonitor: true,
                },
                {
                    opcode: "printElements",
                    blockType: BlockType.COMMAND,
                    text: "print elements and wait",
                },
                '---',
                {
                    opcode: "addElementText",
                    blockType: BlockType.COMMAND,
                    text: "add text [TXT]",
                    arguments: {
                        TXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello world!"
                        }
                    },
                },
                {
                    opcode: "addElementScreenshot",
                    blockType: BlockType.COMMAND,
                    text: "add stage screenshot",
                },
                {
                    opcode: "addElementImg",
                    blockType: BlockType.COMMAND,
                    text: "add image [IMG]",
                    arguments: {
                        IMG: {
                            type: ArgumentType.STRING,
                            defaultValue: "https://penguinmod.com/favicon.png"
                        }
                    },
                },
                {
                    opcode: "addElementHtml",
                    blockType: BlockType.COMMAND,
                    text: "add html [HTML]",
                    arguments: {
                        HTML: {
                            type: ArgumentType.STRING,
                            defaultValue: "<h1>Header text</h1><p>Paragraph here</p>"
                        }
                    },
                },
                {
                    opcode: "removeElements",
                    blockType: BlockType.COMMAND,
                    text: "remove all elements",
                },
                { blockType: BlockType.LABEL, text: "Formatting" },
                {
                    opcode: "txtFont",
                    blockType: BlockType.COMMAND,
                    text: "set font to [FONT] size [SZ]",
                    arguments: {
                        FONT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Arial"
                        },
                        SZ: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 12
                        },
                    },
                },
                {
                    opcode: "txtColor",
                    blockType: BlockType.COMMAND,
                    text: "set text color [COLOR]",
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR
                        },
                    },
                },
                {
                    opcode: "txtAlign",
                    blockType: BlockType.COMMAND,
                    text: "align text [ALIGN]",
                    arguments: {
                        ALIGN: {
                            type: ArgumentType.STRING,
                            menu: "ALIGNMENTS"
                        },
                    },
                },
                {
                    opcode: "txtSpacing",
                    blockType: BlockType.COMMAND,
                    text: "set text spacing letter [LET] line [LIN]",
                    arguments: {
                        LET: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        LIN: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1.2
                        },
                    },
                },
                "---",
                {
                    opcode: "imgSize",
                    blockType: BlockType.COMMAND,
                    text: "set image width [W] height [H]",
                    arguments: {
                        W: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 200
                        },
                        H: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 200
                        },
                    },
                },
                {
                    opcode: "imgPos",
                    blockType: BlockType.COMMAND,
                    text: "set image position to x [x] y [y]",
                    arguments: {
                        x: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        },
                        y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                    },
                },
                {
                    opcode: "imgRot",
                    blockType: BlockType.COMMAND,
                    text: "set image rotation to [rot]",
                    arguments: {
                        rot: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 90
                        },
                    },
                },
                { blockType: BlockType.LABEL, text: "Background" },
                {
                    opcode: "setBGColor",
                    blockType: BlockType.COMMAND,
                    text: "set background color [COLOR]",
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR
                        },
                    },
                },
                {
                    opcode: "setBGImage",
                    blockType: BlockType.COMMAND,
                    text: "set background image [IMG]",
                    arguments: {
                        IMG: {
                            type: ArgumentType.STRING,
                            defaultValue: "https://penguinmod.com/test.png"
                        }
                    },
                },
                {
                    opcode: "setBGRepeat",
                    blockType: BlockType.COMMAND,
                    text: "set background to [BGMODE]",
                    arguments: {
                        BGMODE: {
                            type: ArgumentType.STRING,
                            menu: "BGMODE"
                        },
                    },
                },
                {
                    opcode: "resetBackground",
                    blockType: BlockType.COMMAND,
                    text: "remove background",
                },
                { blockType: BlockType.LABEL, text: "Miscellaneous" },
                {
                    opcode: "elementCount",
                    blockType: BlockType.REPORTER,
                    text: "elements in print"
                },
                {
                    opcode: "lastHTML",
                    blockType: BlockType.REPORTER,
                    text: "last printed html"
                },
            ],
            menus: {
                ALIGNMENTS: {
                    acceptReporters: true,
                    items: ["left", "right", "center"]
                },
                BGMODE: {
                    acceptReporters: true,
                    items: ["repeat", "not repeat", "fill", "stretch"]
                },
            }
        };
    }
}

module.exports = sharkpoolPrinting;
