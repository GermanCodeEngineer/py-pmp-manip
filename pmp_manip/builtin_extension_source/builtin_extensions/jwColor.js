const BlockType = require('../../extension-support/block-type')
const ArgumentType = require('../../extension-support/argument-type')

const Color = {
    Type: class {}, // Not needed
    Block: {
        blockType: BlockType.REPORTER,
        forceOutputType: "Color",
        disableMonitor: true
    },
    Argument: {
        type: ArgumentType.COLOR,
        defaultValue: "#ff7aab"
    }
}

class Extension {
    getInfo() {
        return {
            id: "jwColor",
            name: "Color",
            color1: "#f04a87",
            menuIconURI: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMCAyMCI+CiAgPGVsbGlwc2Ugc3R5bGU9ImZpbGw6IHJnYigyNDAsIDc0LCAxMzUpOyBzdHJva2U6IHJnYigyMTYsIDY2LCAxMjIpOyBzdHJva2Utd2lkdGg6IDJweDsgcGFpbnQtb3JkZXI6IHN0cm9rZTsiIGN4PSIxMCIgY3k9IjEwIiByeD0iOSIgcnk9IjkiPjwvZWxsaXBzZT4KICA8cGF0aCB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGQ9Ik0gMTIuMTYyIDExLjAxNSBDIDExLjM1OCAxMS44MTkgMTAuNzY1IDEyLjIzMyAxMC4yOTkgMTIuMzkxIEMgMTAuMTYyIDExLjk2OCA5LjkyOSAxMS41NzYgOS42MDEgMTEuMjQ4IEMgOS4yNjIgMTAuOTIgOC44NzEgMTAuNjg3IDguNDQ3IDEwLjUzOCBDIDguNjE3IDEwLjA3MyA5LjAzIDkuNDggOS44MjMgOC42ODcgQyAxMS43MjggNi43NzEgMTUuMTE1IDQuNDMyIDE1Ljc2MSA1LjA3OCBDIDE2LjQwNyA1LjcyMyAxNC4wNjggOS4xMSAxMi4xNjIgMTEuMDE1IFogTSA4LjY1IDE0LjUzOSBDIDguMzM1IDE0Ljg0NCA3LjkyOSAxNSA3LjUyMiAxNS4wMiBMIDcuNTIyIDE1LjAzIEwgNy40MjEgMTUuMDMgQyA0LjY5OCAxNS4xMjggMy41MDkgMTIuMDQ2IDQuNDQ0IDEyLjM2OSBDIDUuNjczIDEyLjc5MiA2LjE3MiAxMi4xODMgNi4xOTEgMTIuMTYzIEMgNi44NzIgMTEuNTE2IDcuOTY5IDExLjUxNiA4LjY1IDEyLjE2MyBDIDkuMzMxIDEyLjgyMSA5LjMzMSAxMy44OTIgOC42NSAxNC41MzkgWiIgaWQ9ImJ1cnNoLWljb24iIHN0eWxlPSJmaWxsOiByZ2IoMjU1LCAyNTUsIDI1NSk7Ij48L3BhdGg+Cjwvc3ZnPg==",
            blocks: [
                {
                    opcode: 'newColor',
                    text: 'new color [COLOR]',
                    arguments: {
                        COLOR: Color.Argument
                    },
                    ...Color.Block
                },
                {
                    opcode: 'fromRGB',
                    text: 'from RGB [R] [G] [B]',
                    arguments: {
                        R: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 255
                        },
                        G: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 122
                        },
                        B: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 171
                        }
                    },
                    ...Color.Block
                },
                {
                    opcode: 'fromHSV',
                    text: 'from HSV [H] [S] [V]',
                    arguments: {
                        H: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 338
                        },
                        S: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.52
                        },
                        V: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    ...Color.Block
                },
                {
                    opcode: 'fromHex',
                    text: 'from hex [HEX]',
                    arguments: {
                        HEX: {
                            type: ArgumentType.STRING,
                            defaultValue: "ff7aab"
                        }
                    },
                    ...Color.Block
                },
                "---",
                {
                    opcode: 'add',
                    text: '[A] + [B]',
                    arguments: {
                        A: Color.Argument,
                        B: Color.Argument
                    },
                    ...Color.Block
                },
                {
                    opcode: 'sub',
                    text: '[A] - [B]',
                    arguments: {
                        A: Color.Argument,
                        B: Color.Argument
                    },
                    ...Color.Block
                },
                {
                    opcode: 'mul',
                    text: '[A] * [B]',
                    arguments: {
                        A: Color.Argument,
                        B: Color.Argument
                    },
                    ...Color.Block
                },
                {
                    opcode: 'interpolate',
                    text: 'interpolate [A] to [B] by [I] using [OPTION]',
                    arguments: {
                        A: Color.Argument,
                        B: Color.Argument,
                        I: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.5
                        },
                        OPTION: {
                            menu: "interpolateOption"
                        }
                    },
                    ...Color.Block
                },
                "---",
                {
                    opcode: 'get',
                    text: 'get [OPTION] [COLOR]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        COLOR: Color.Argument,
                        OPTION: {
                            menu: "propOption"
                        }
                    }
                },
                {
                    opcode: 'set',
                    text: 'set [OPTION] [COLOR] to [VALUE]',
                    arguments: {
                        COLOR: Color.Argument,
                        VALUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        OPTION: {
                            menu: "propOption"
                        }
                    },
                    ...Color.Block
                },
                "---",
                {
                    opcode: 'toDecimal',
                    text: '[COLOR] to decimal',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        COLOR: Color.Argument
                    }
                },
                {
                    opcode: 'toHex',
                    text: '[COLOR] to hexadecimal',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        COLOR: Color.Argument
                    }
                }
            ],
            menus: {
                interpolateOption: {
                    acceptReporters: true,
                    items: [
                        'RGB',
                        'HSV'
                    ]
                },
                propOption: {
                    acceptReporters: true,
                    items: [
                        'red',
                        'green',
                        'blue',
                        'hue',
                        'saturation',
                        'value'
                    ]
                }
            }
        };
    }
}

module.exports = Extension