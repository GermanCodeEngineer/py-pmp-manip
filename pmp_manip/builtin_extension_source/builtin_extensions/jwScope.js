const BlockType = require('../../extension-support/block-type')
const ArgumentType = require('../../extension-support/argument-type')

class Extension {
    constructor() {
    }

    getInfo() {
        return {
            id: "jwScope",
            name: "Scope",
            color1: "#4f85f3",
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
                    opcode: "get",
                    blockType: BlockType.REPORTER,
                    text: "get [NAME]",
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
                }
            ]
        };
    }
}

module.exports = Extension