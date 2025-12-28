const BlockType = require('../../extension-support/block-type')
const BlockShape = require('../../extension-support/block-shape')
const ArgumentType = require('../../extension-support/argument-type')

class Extension {
    getInfo() {
        return {
            id: "jwScope",
            name: "Scope",
            color1: "#4f85f3",
            menuIconURI: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMCAyMCI+CiAgPGVsbGlwc2Ugc3R5bGU9InN0cm9rZS1saW5lam9pbjogcm91bmQ7IHBhaW50LW9yZGVyOiBmaWxsOyBzdHJva2U6IHJnYig3MSwgMTE5LCAyMTkpOyBmaWxsOiByZ2IoNzksIDEzMywgMjQzKTsiIGN4PSIxMCIgY3k9IjEwIiByeD0iOS41IiByeT0iOS41Ij48L2VsbGlwc2U+CiAgPHJlY3Qgc3R5bGU9InBhaW50LW9yZGVyOiBzdHJva2U7IGZpbGw6IG5vbmU7IHN0cm9rZTogcmdiKDI1NSwgMjU1LCAyNTUpOyBzdHJva2UtbGluZWpvaW46IHJvdW5kOyBzdHJva2Utd2lkdGg6IDJweDsiIHg9IjUiIHk9IjUiIHdpZHRoPSIxMCIgaGVpZ2h0PSIxMCIgcng9IjMiIHJ5PSIzIj48L3JlY3Q+Cjwvc3ZnPg==",
            docsURI: 'https://docs.penguinmod.com/extensions/jwScope/',
            blocks: [
                {
                    opcode: "set",
                    blockType: BlockType.COMMAND,
                    text: "set [NAME] to [VALUE]",
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "var",
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "apple",
                            exemptFromNormalization: true
                        }
                    },
                },
                {
                    opcode: "change",
                    blockType: BlockType.COMMAND,
                    text: "change [NAME] by [VALUE]",
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "var",
                        },
                        VALUE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        }
                    },
                },
                {
                    opcode: "get",
                    blockType: BlockType.REPORTER,
                    text: "get [NAME]",
                    allowDropAnywhere: true,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "var"
                        }
                    },
                },
                "---",
                {
                    opcode: "create",
                    blockType: BlockType.COMMAND,
                    text: "init [NAME]",
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "var",
                        }
                    },
                },
                {
                    opcode: "delete",
                    blockType: BlockType.COMMAND,
                    text: "remove [NAME]",
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "var",
                        }
                    },
                },
                "---",
                {
                    opcode: "reset",
                    blockType: BlockType.COMMAND,
                    text: "reset scope"
                },
                "---",
                {
                    opcode: "current",
                    text: "current scope",
                    hideFromPalette: !vm.runtime.ext_jwArray,
                    blockType: BlockType.REPORTER,
                    blockShape: BlockShape.SQUARE,
                    ...(vm.jwArray ? vm.jwArray.Block : {})
                },
                {
                    opcode: "all",
                    text: "all scopes",
                    hideFromPalette: !vm.runtime.ext_jwArray,
                    blockType: BlockType.REPORTER,
                    blockShape: BlockShape.SQUARE,
                    ...(vm.jwArray ? vm.jwArray.Block : {})
                }
            ]
        };
    }
}

module.exports = Extension