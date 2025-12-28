const BlockType = require('../../extension-support/block-type')
const BlockShape = require('../../extension-support/block-shape')
const ArgumentType = require('../../extension-support/argument-type')
const TargetType = require('../../extension-support/target-type')

const Vector = {
    Type: class {}, // not needed
    Block: {
        blockType: BlockType.REPORTER,
        blockShape: BlockShape.LEAF,
        forceOutputType: "Vector",
        disableMonitor: true
    },
    Argument: {
        shape: BlockShape.LEAF,
        check: ["Vector"]
    }
}

class Extension {
    getInfo() {
        return {
            id: "jwVector",
            name: "Vector",
            color1: "#6babff",
            menuIconURI: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMCAyMCIgeG1sbnM6Yng9Imh0dHBzOi8vYm94eS1zdmcuY29tIj4KICA8ZWxsaXBzZSBzdHlsZT0ic3Ryb2tlLXdpZHRoOiAycHg7IHBhaW50LW9yZGVyOiBzdHJva2U7IGZpbGw6IHJnYigxMDcsIDE3MSwgMjU1KTsgc3Ryb2tlOiByZ2IoNjksIDEyNiwgMjA0KTsiIGN4PSIxMCIgY3k9IjEwIiByeD0iOSIgcnk9IjkiPjwvZWxsaXBzZT4KICA8cGF0aCBkPSJNIDQuMzUyIDEzLjc2NiBDIDQuMzUyIDE0LjgwNSA1LjE5NCAxNS42NDggNi4yMzUgMTUuNjQ4IEwgMTAgMTUuNjQ4IEMgMTEuMDM5IDE1LjY0OCAxMS44ODIgMTQuODA1IDExLjg4MiAxMy43NjYgTCAxMS44ODIgMTAgQyAxMS44ODIgOC45NTkgMTEuMDM5IDguMTE4IDEwIDguMTE4IEwgNi4yMzUgOC4xMTggQyA1LjE5NCA4LjExOCA0LjM1MiA4Ljk1OSA0LjM1MiAxMCBMIDQuMzUyIDEzLjc2NiBNIDguMTE3IDEzLjc2NiBDIDYuNjY4IDEzLjc2NiA1Ljc2MiAxMi4xOTUgNi40ODcgMTAuOTQyIEMgNi44MjIgMTAuMzU4IDcuNDQzIDEwIDguMTE3IDEwIEMgOS41NjcgMTAgMTAuNDcyIDExLjU2OSA5Ljc0NyAxMi44MjQgQyA5LjQxMSAxMy40MDYgOC43ODkgMTMuNzY2IDguMTE3IDEzLjc2NiBNIDcuMTc2IDkuMDU5IEwgOS4wNTggOS4wNTkgTCA5LjA1OCA1LjI5NCBDIDkuMDU4IDQuNTY5IDguMjczIDQuMTE2IDcuNjQ3IDQuNDc5IEMgNy4zNTUgNC42NDYgNy4xNzYgNC45NTcgNy4xNzYgNS4yOTQgTCA3LjE3NiA5LjA1OSBaIE0gMTAuOTQxIDEwLjk0MiBMIDEwLjk0MSAxMi44MjQgTCAxNC43MDYgMTIuODI0IEMgMTUuNDMxIDEyLjgyNCAxNS44ODMgMTIuMDM5IDE1LjUyMSAxMS40MTIgQyAxNS4zNTIgMTEuMTIxIDE1LjA0MSAxMC45NDIgMTQuNzA2IDEwLjk0MiBMIDEwLjk0MSAxMC45NDIgWiIgc3R5bGU9ImZpbGw6IHJnYigyNTUsIDI1NSwgMjU1KTsiPjwvcGF0aD4KPC9zdmc+",
            blocks: [
                {
                    opcode: 'newVector',
                    text: 'new vector x: [X] y: [Y]',
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'newVectorFromMagnitude',
                    text: 'new vector magnitude: [X] angle: [Y]',
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        Y: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 0
                        }
                    },
                    ...Vector.Block
                },
                "---",
                {
                    opcode: 'vectorX',
                    text: '[VECTOR] x',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VECTOR: Vector.Argument
                    }
                },
                {
                    opcode: 'vectorY',
                    text: '[VECTOR] y',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VECTOR: Vector.Argument
                    }
                },
                "---",
                {
                    opcode: 'add',
                    text: '[X] + [Y]',
                    arguments: {
                        X: Vector.Argument,
                        Y: Vector.Argument
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'subtract',
                    text: '[X] - [Y]',
                    arguments: {
                        X: Vector.Argument,
                        Y: Vector.Argument
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'multiplyA',
                    text: '[X] * [Y]',
                    arguments: {
                        X: Vector.Argument,
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'multiplyB',
                    text: '[X] * [Y]',
                    arguments: {
                        X: Vector.Argument,
                        Y: Vector.Argument
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'divideA',
                    text: '[X] / [Y]',
                    arguments: {
                        X: Vector.Argument,
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'divideB',
                    text: '[X] / [Y]',
                    arguments: {
                        X: Vector.Argument,
                        Y: Vector.Argument
                    },
                    ...Vector.Block
                },
                "---",
                {
                    opcode: 'magnitude',
                    text: 'magnitude of [VECTOR]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VECTOR: Vector.Argument
                    }
                },
                {
                    opcode: 'angle',
                    text: 'angle of [VECTOR]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VECTOR: Vector.Argument
                    }
                },
                {
                    opcode: 'normalize',
                    text: 'normalize [VECTOR]',
                    arguments: {
                        VECTOR: Vector.Argument
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'absolute',
                    text: 'absolute [VECTOR]',
                    arguments: {
                        VECTOR: Vector.Argument
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'rotate',
                    text: 'rotate [VECTOR] by [ANGLE]',
                    arguments: {
                        VECTOR: Vector.Argument,
                        ANGLE: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 90
                        }
                    },
                    ...Vector.Block
                },
                {
                    opcode: 'round',
                    text: '[ROUNDING] of [VECTOR]',
                    arguments: {
                        ROUNDING: {
                            menu: 'roundingFunctions',
                        },
                        VECTOR: Vector.Argument
                    },
                    ...Vector.Block
                },
                "---",
                {
                    opcode: 'getPos',
                    text: 'position',
                    extensions: ["colours_motion"],
                    filter: [TargetType.SPRITE],
                    ...Vector.Block
                },
                {
                    opcode: 'setPos',
                    text: 'set position to [VECTOR]',
                    arguments: {
                        VECTOR: Vector.Argument
                    },
                    extensions: ["colours_motion"],
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'getStretch',
                    text: 'stretch',
                    extensions: ["colours_looks"],
                    filter: [TargetType.SPRITE],
                    ...Vector.Block
                },
                {
                    opcode: 'setStretch',
                    text: 'set stretch to [VECTOR]',
                    arguments: {
                        VECTOR: Vector.Argument
                    },
                    extensions: ["colours_looks"],
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'getMouse',
                    text: 'mouse position',
                    extensions: ["colours_sensing"],
                    ...Vector.Block
                },
            ],
            menus: {
                roundingFunctions: {
                    acceptReporters: false,
                    items: [
                        {
                            text: 'round',
                            value: 'round'
                        },
                        {
                            text: 'ceil', // might as well go full in on the inconsistencies since we are already doing "round of"
                            value: 'ceil'
                        },
                        {
                            text: 'floor',
                            value: 'floor'
                        }
                    ]
                },
            }
        };
    }
}

module.exports = Extension
