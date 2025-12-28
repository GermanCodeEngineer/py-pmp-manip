const BlockType = require('../../extension-support/block-type');
const BlockShape = require('../../extension-support/block-shape');
const ArgumentType = require('../../extension-support/argument-type');

const jwArray = {
    Type: class {}, // not needed
    Block: {
        blockType: BlockType.REPORTER,
        blockShape: BlockShape.SQUARE,
        forceOutputType: "Array",
        disableMonitor: true
    },
    Argument: {
        shape: BlockShape.SQUARE,
        check: ["Array"]
    }
}

class Extension {
    getInfo() {
        return {
            id: "jwArray",
            name: "Arrays",
            color1: "#ff513d",
            menuIconURI: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMCAyMCIgeG1sbnM6Yng9Imh0dHBzOi8vYm94eS1zdmcuY29tIj4KICA8Y2lyY2xlIHN0eWxlPSJzdHJva2Utd2lkdGg6IDJweDsgcGFpbnQtb3JkZXI6IHN0cm9rZTsgZmlsbDogcmdiKDI1NSwgODEsIDYxKTsgc3Ryb2tlOiByZ2IoMjA1LCA1OSwgNDQpOyIgY3g9IjEwIiBjeT0iMTAiIHI9IjkiPjwvY2lyY2xlPgogIDxwYXRoIGQ9Ik0gOC4wNzMgNC4yMiBMIDYuMTQ3IDQuMjIgQyA1LjA4MyA0LjIyIDQuMjIgNS4wODMgNC4yMiA2LjE0NyBMIDQuMjIgMTMuODUzIEMgNC4yMiAxNC45MTkgNS4wODMgMTUuNzggNi4xNDcgMTUuNzggTCA4LjA3MyAxNS43OCBMIDguMDczIDEzLjg1MyBMIDYuMTQ3IDEzLjg1MyBMIDYuMTQ3IDYuMTQ3IEwgOC4wNzMgNi4xNDcgTCA4LjA3MyA0LjIyIFogTSAxMS45MjcgMTMuODUzIEwgMTMuODUzIDEzLjg1MyBMIDEzLjg1MyA2LjE0NyBMIDExLjkyNyA2LjE0NyBMIDExLjkyNyA0LjIyIEwgMTMuODUzIDQuMjIgQyAxNC45MTcgNC4yMiAxNS43OCA1LjA4MyAxNS43OCA2LjE0NyBMIDE1Ljc4IDEzLjg1MyBDIDE1Ljc4IDE0LjkxOSAxNC45MTcgMTUuNzggMTMuODUzIDE1Ljc4IEwgMTEuOTI3IDE1Ljc4IEwgMTEuOTI3IDEzLjg1MyBaIiBmaWxsPSIjZmZmIiBzdHlsZT0iIj48L3BhdGg+Cjwvc3ZnPg==",
            blocks: [
                {
                    opcode: 'blank',
                    text: 'blank array',
                    ...jwArray.Block
                },
                {
                    opcode: 'blankLength',
                    text: 'blank array of length [LENGTH]',
                    arguments: {
                        LENGTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'fromList',
                    text: 'array from list [LIST]',
                    arguments: {
                        LIST: {
                            menu: "list"
                        }
                    },
                    hideFromPalette: true, //doesn't work for some reason
                    ...jwArray.Block
                },
                {
                    opcode: 'parse',
                    text: 'parse [INPUT] as array',
                    arguments: {
                        INPUT: {
                            type: ArgumentType.STRING,
                            defaultValue: '["a", "b", "c"]',
                            exemptFromNormalization: true,
                            compilerInfo: {
                                jwArrayUnmodified: true
                            }
                        }
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'split',
                    text: 'split [STRING] by [DIVIDER]',
                    arguments: {
                        STRING: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo"
                        },
                        DIVIDER: {
                            type: ArgumentType.STRING
                        }
                    },
                    ...jwArray.Block
                },
                "---",
                {
                    opcode: 'builder',
                    text: 'array builder [SHADOW]',
                    branches: [{}],
                    arguments: {
                        SHADOW: {
                            fillIn: 'builderCurrent'
                        }
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'builderCurrent',
                    text: 'current array',
                    hideFromPalette: true,
                    canDragDuplicate: true,
                    ...jwArray.Block
                },
                {
                    opcode: 'builderAppend',
                    text: 'append [VALUE] to builder',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                            exemptFromNormalization: true,
                            compilerInfo: {
                                jwArrayUnmodified: true
                            }
                        }
                    }
                },
                {
                    opcode: 'builderSet',
                    text: 'set builder to [ARRAY]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ARRAY: jwArray.Argument
                    }
                },
                "---",
                {
                    opcode: 'get',
                    text: 'get [INDEX] in [ARRAY]',
                    blockType: BlockType.REPORTER,
                    allowDropAnywhere: true,
                    arguments: {
                        ARRAY: jwArray.Argument,
                        INDEX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    }
                },
                {
                    opcode: 'items',
                    text: 'items [X] to [Y] in [ARRAY]',
                    arguments: {
                        ARRAY: jwArray.Argument,
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 3
                        }
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'index',
                    text: 'index of [VALUE] in [ARRAY]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ARRAY: jwArray.Argument,
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                            exemptFromNormalization: true,
                            compilerInfo: {
                                jwArrayUnmodified: true
                            }
                        }
                    }
                },
                {
                    opcode: 'has',
                    text: '[ARRAY] has [VALUE]',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        ARRAY: jwArray.Argument,
                        VALUE: {
                            type: ArgumentType.STRING,
                            exemptFromNormalization: true,
                            compilerInfo: {
                                jwArrayUnmodified: true
                            }
                        }
                    }
                },
                {
                    opcode: 'length',
                    text: 'length of [ARRAY]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ARRAY: jwArray.Argument
                    }
                },
                "---",
                {
                    opcode: 'set',
                    text: 'set [INDEX] in [ARRAY] to [VALUE]',
                    arguments: {
                        ARRAY: jwArray.Argument,
                        INDEX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                            exemptFromNormalization: true,
                            compilerInfo: {
                                jwArrayUnmodified: true
                            }
                        }
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'append',
                    text: 'append [VALUE] to [ARRAY]',
                    arguments: {
                        ARRAY: jwArray.Argument,
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                            exemptFromNormalization: true,
                            compilerInfo: {
                                jwArrayUnmodified: true
                            }
                        }
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'concat',
                    text: 'merge [ONE] with [TWO]',
                    arguments: {
                        ONE: jwArray.Argument,
                        TWO: jwArray.Argument
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'fill',
                    text: 'fill [ARRAY] with [VALUE]',
                    arguments: {
                        ARRAY: jwArray.Argument,
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                            exemptFromNormalization: true,
                            compilerInfo: {
                                jwArrayUnmodified: true
                            }
                        }
                    },
                    ...jwArray.Block
                },
                "---",
                {
                    opcode: 'reverse',
                    text: 'reverse [ARRAY]',
                    arguments: {
                        ARRAY: jwArray.Argument
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'splice',
                    text: 'splice [ARRAY] at [INDEX] with [ITEMS] items',
                    arguments: {
                        ARRAY: jwArray.Argument,
                        INDEX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        ITEMS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'repeat',
                    text: 'repeat [ARRAY] [TIMES] times',
                    arguments: {
                        ARRAY: jwArray.Argument,
                        TIMES: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        }
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'flat',
                    text: 'flat [ARRAY] with depth [DEPTH]',
                    arguments: {
                        ARRAY: jwArray.Argument,
                        DEPTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    ...jwArray.Block
                },
                "---",
                {
                    opcode: 'toString',
                    text: 'stringify [ARRAY] [FORMAT]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ARRAY: jwArray.Argument,
                        FORMAT: {
                            menu: "stringifyFormat",
                            defaultValue: "compact"
                        }
                    }
                },
                {
                    opcode: 'join',
                    text: 'join [ARRAY] with [DIVIDER]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ARRAY: jwArray.Argument,
                        DIVIDER: {
                            type: ArgumentType.STRING,
                            defaultValue: ""
                        }
                    }
                },
                {
                    opcode: 'sum',
                    text: 'sum of [ARRAY]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ARRAY: jwArray.Argument
                    }
                },
                "---",
                {
                    opcode: 'forEachI',
                    text: 'index',
                    blockType: BlockType.REPORTER,
                    hideFromPalette: true,
                    canDragDuplicate: true
                },
                {
                    opcode: 'forEachV',
                    text: 'value',
                    blockType: BlockType.REPORTER,
                    hideFromPalette: true,
                    allowDropAnywhere: true,
                    canDragDuplicate: true
                },
                {
                    opcode: 'forEach',
                    text: 'for [I] [V] of [ARRAY]',
                    blockType: BlockType.LOOP,
                    arguments: {
                        ARRAY: jwArray.Argument,
                        I: {
                            fillIn: 'forEachI'
                        },
                        V: {
                            fillIn: 'forEachV'
                        }
                    }
                },
                {
                    opcode: 'basicSort',
                    text: 'sort [ARRAY] [I] [V] > [VALUE]',
                    arguments: {
                        ARRAY: jwArray.Argument,
                        I: {
                            fillIn: 'forEachI'
                        },
                        V: {
                            fillIn: 'forEachV'
                        },
                        VALUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    ...jwArray.Block
                }
            ],
            menus: {
                list: {
                    acceptReporters: false,
                    items: "getLists",
                },
                stringifyFormat: {
                    acceptReporters: false,
                    items: [
                        "compact",
                        "pretty"
                    ]
                }
            }
        };
    }
}

module.exports = Extension