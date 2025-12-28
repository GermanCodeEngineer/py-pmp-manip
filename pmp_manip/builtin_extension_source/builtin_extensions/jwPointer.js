const BlockType = require('../../extension-support/block-type')
const ArgumentType = require('../../extension-support/argument-type')

let jwPointer = {
    Type: class {}, // not neededs
    Block: {
        blockType: BlockType.REPORTER,
        forceOutputType: "jwPointer",
        disableMonitor: true
    },
    Argument: {
        check: ["jwPointer"]
    },

    pointers: []
}

class Extension {
    getInfo() {
        return {
            id: "jwPointer",
            name: "Pointers",
            blocks: [
                {
                    opcode: 'create',
                    text: 'create pointer [VALUE]',
                    arguments: {
                        VALUE: {
                            type: ArgumentType.STRING,
                            exemptFromNormalization: true
                        }
                    },
                    ...jwPointer.Block
                },
            ]
        };
    }
}

module.exports = Extension