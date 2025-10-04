const BlockType = require('../../extension-support/block-type')
const BlockShape = require('../../extension-support/block-shape')
const ArgumentType = require('../../extension-support/argument-type')

const jwDate = {
    Type: class {}, // Not needed
    Block: {
        blockType: BlockType.REPORTER,
        blockShape: BlockShape.TICKET,
        forceOutputType: "jwDate",
        disableMonitor: true
    },
    Argument: {
        shape: BlockShape.TICKET,
        check: ["jwDate"]
    }
}

class Extension {
    getInfo() {
        return {
            id: "jwDate",
            name: "Dates",
            color1: "#ff788a",
            blocks: [
                {
                    opcode: 'now',
                    text: 'now',
                    ...jwDate.Block
                },
                {
                    opcode: 'epoch',
                    text: 'unix epoch',
                    ...jwDate.Block
                },
                {
                    opcode: 'parse',
                    text: 'parse [INPUT]',
                    arguments: {
                        INPUT: {
                            type: ArgumentType.String,
                            defaultValue: "1/1/1970 01:23",
                            exemptFromNormalization: true
                        }
                    },
                    ...jwDate.Block
                }
            ],
            menus: {}
        }
    }
}

module.exports = Extension