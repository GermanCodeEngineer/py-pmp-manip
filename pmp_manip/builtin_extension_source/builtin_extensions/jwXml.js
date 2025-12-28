const BlockType = require('../../extension-support/block-type')
const BlockShape = require('../../extension-support/block-shape')
const ArgumentType = require('../../extension-support/argument-type')

let XML = {
    Type: class {}, // not needed
    Block: {
        blockType: BlockType.REPORTER,
        blockShape: BlockShape.INDENTED,
        forceOutputType: "jwXML",
        disableMonitor: true
    },
    Argument: {
        shape: BlockShape.INDENTED,
        check: ["jwXML"],
        exemptFromNormalization: true
    },
    fxp: undefined, // not needed
}

let jwArray = {
    Type: class {},
    Block: {},
    Argument: {}
}

class Extension {
    getInfo() {
        return {
            id: "jwXML",
            name: "XML",
            color1: "#8dd941",
            menuIconURI: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMCAyMCI+CiAgPGVsbGlwc2Ugc3R5bGU9InN0cm9rZTogcmdiKDExMiwgMTczLCA1Mik7IGZpbGw6IHJnYigxNDEsIDIxNywgNjUpOyIgY3g9IjEwIiBjeT0iMTAiIHJ4PSI5LjUiIHJ5PSI5LjUiPjwvZWxsaXBzZT4KICA8cGF0aCBkPSJNIDguMjg3IDYuMjE0IEwgNC41IDEzLjc4NiBNIDEyLjA3MyA2LjIxNCBMIDE1Ljg2IDEwIEwgMTIuMDczIDEzLjc4NiIgc3Ryb2tlPSIjZmZmIiBmaWxsPSJub25lIiBzdHlsZT0ic3Ryb2tlLWxpbmVjYXA6IHJvdW5kOyBzdHJva2UtbGluZWpvaW46IHJvdW5kOyBzdHJva2Utd2lkdGg6IDJweDsiPjwvcGF0aD4KPC9zdmc+",
            blocks: [
                {
                    opcode: "newNode",
                    text: "new node [NAME]",
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "name"
                        }
                    },
                    ...XML.Block
                },
                {
                    opcode: "parse",
                    text: "parse [INPUT] as node",
                    arguments: {
                        INPUT: {
                            type: ArgumentType.STRING,
                            defaultValue: '<name />',
                            exemptFromNormalization: true
                        }
                    },
                    ...XML.Block
                },
                {
                    opcode: "parseMultiple",
                    text: "parse [INPUT] as nodes",
                    arguments: {
                        INPUT: {
                            type: ArgumentType.STRING,
                            defaultValue: '<one /><two />',
                            exemptFromNormalization: true
                        }
                    },
                    ...jwArray.Block
                },
                "---",
                {
                    opcode: "getName",
                    text: "name of [NODE]",
                    blockType: BlockType.REPORTER,
                    arguments: {
                        NODE: XML.Argument
                    }
                },
                {
                    opcode: "setName",
                    text: "set name of [NODE] to [NAME]",
                    arguments: {
                        NODE: XML.Argument,
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "name"
                        }
                    },
                    ...XML.Block
                },
                "---",
                {
                    opcode: "appendChild",
                    text: "append [CHILD] to [NODE]",
                    arguments: {
                        CHILD: {
                            type: ArgumentType.STRING,
                            defaultValue: 'text / node',
                            exemptFromNormalization: true
                        },
                        NODE: XML.Argument
                    },
                    ...XML.Block
                },
                {
                    opcode: "removeChildren",
                    text: "remove children of [NODE]",
                    arguments: {
                        NODE: XML.Argument
                    },
                    ...XML.Block
                },

                {
                    opcode: "getChildren",
                    text: "children of [NODE]",
                    arguments: {
                        NODE: XML.Argument
                    },
                    ...jwArray.Block
                },
                {
                    opcode: "setChildren",
                    text: "set children of [NODE] to [CHILDREN]",
                    arguments: {
                        NODE: XML.Argument,
                        CHILDREN: jwArray.Argument
                    },
                    ...XML.Block
                },
                "---",
                {
                    opcode: "getAttribute",
                    text: "attribute [ATTRIBUTE] of [NODE]",
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ATTRIBUTE: {
                            type: ArgumentType.STRING,
                            defaultValue: "name"
                        },
                        NODE: XML.Argument
                    },
                },
                {
                    opcode: "setAttribute",
                    text: "set attribute [ATTRIBUTE] of [NODE] to [VALUE]",
                    arguments: {
                        ATTRIBUTE: {
                            type: ArgumentType.STRING,
                            defaultValue: "name"
                        },
                        NODE: XML.Argument,
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "value"
                        },
                    },
                    ...XML.Block
                },
                {
                    opcode: "removeAttribute",
                    text: "remove attribute [ATTRIBUTE] of [NODE]",
                    arguments: {
                        ATTRIBUTE: {
                            type: ArgumentType.STRING,
                            defaultValue: "name"
                        },
                        NODE: XML.Argument
                    },
                    ...XML.Block
                },
                {
                    opcode: "removeAttributes",
                    text: "remove all attributes of [NODE]",
                    arguments: {
                        NODE: XML.Argument
                    },
                    ...XML.Block
                },
                {
                    opcode: "hasAttribute",
                    text: "[NODE] has attribute [ATTRIBUTE]",
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        NODE: XML.Argument,
                        ATTRIBUTE: {
                            type: ArgumentType.STRING,
                            defaultValue: "name"
                        }
                    }
                },
                {
                    opcode: "getAttributes",
                    text: "attributes of [NODE]",
                    arguments: {
                        NODE: XML.Argument
                    },
                    ...jwArray.Block
                },
                "---",
                {
                    opcode: "toString",
                    text: "stringify [NODE] [FORMAT]",
                    blockType: BlockType.REPORTER,
                    arguments: {
                        NODE: XML.Argument,
                        FORMAT: {
                            menu: "stringifyFormat",
                            defaultValue: "compact"
                        }
                    }
                },
                "---",
                {
                    opcode: "validName",
                    text: "is [NAME] valid name",
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "name"
                        }
                    }
                },
                {
                    opcode: "toStringSafe",
                    text: "make [TEXT] XML safe",
                    blockType: BlockType.REPORTER,
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: '<unsafe>'
                        }
                    }
                },
                {
                    opcode: "filterArray",
                    text: "elements named [NAME] in [INPUT]",
                    blockType: BlockType.REPORTER,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "name"
                        },
                        INPUT: jwArray.Argument
                    },
                    ...jwArray.Block,
                }
            ],
            menus: {
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