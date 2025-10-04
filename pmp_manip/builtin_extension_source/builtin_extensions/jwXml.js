const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

class Extension {
    getInfo() {
        return {
            id: "jwXml",
            name: "XML",
            color1: "#ffbb3d",
            color2: "#cc9837",
            blocks: [
                {
                    opcode: 'createNewXML',
                    text: "generate xml [ROOT] with:",
                    arguments: {
                        ROOT: {
                            type: ArgumentType.STRING,
                            defaultValue: "root"
                        }
                    },
                    blockType: BlockType.CONDITIONAL
                },
                {
                    opcode: 'addText',
                    text: "add text [TEXT]",
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo"
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'addChild',
                    text: "add child [CHILD]",
                    arguments: {
                        CHILD: {}
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'addAttribute',
                    text: "add attribute [ATT] as [TEXT]",
                    arguments: {
                        ATT: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo"
                        },
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "bar"
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'generated',
                    text: "xml generated",
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'clear',
                    text: "clear (ADVANCED)",
                    blockType: BlockType.COMMAND
                },
                "---",
                {
                    opcode: 'getChild',
                    text: "get child [NUM] from [XML]",
                    arguments: {
                        NUM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getNamed',
                    text: "get element [STR] from [XML]",
                    arguments: {
                        STR: {
                            type: ArgumentType.STRING,
                            defaultValue: "element"
                        }
                    },
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getAttr',
                    text: "get attribute [ATT] from [XML]",
                    arguments: {
                        ATT: {
                            type: ArgumentType.STRING,
                            defaultValue: "attribute"
                        }
                    },
                    blockType: BlockType.REPORTER
                }
            ]
        };
    }
}

module.exports = Extension