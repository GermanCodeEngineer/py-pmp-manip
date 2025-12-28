const BlockType = require('../../extension-support/block-type')
const BlockShape = require('../../extension-support/block-shape')
const ArgumentType = require('../../extension-support/argument-type')

const Lambda = {
    Type: class {}, // not needed
    Block: {
        blockType: BlockType.REPORTER,
        blockShape: BlockShape.SQUARE,
        forceOutputType: "Lambda",
        disableMonitor: true
    },
    Argument: {
        shape: BlockShape.SQUARE,
        check: ["Lambda"]
    }
}

class Extension {
    get rawLambdaAvailable() {
        return vm.runtime.ext_SPjavascriptV2?.isEditorUnsandboxed
    }

    getInfo() {
        return {
            id: "jwLambda",
            name: "Lambda",
            color1: "#c71a4b",
            menuIconURI: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMCAyMCI+CiAgPGVsbGlwc2Ugc3R5bGU9ImZpbGw6IHJnYigxOTksIDI2LCA3NSk7IHN0cm9rZTogcmdiKDE1OSwgMjAsIDYwKTsiIGN4PSIxMCIgY3k9IjEwIiByeT0iOS41IiByeD0iOS41Ij48L2VsbGlwc2U+CiAgPHBhdGggZD0iTSA3LjIzNyA1LjI2NCBDIDEwLjM5NSA1LjI2NCAxMC4zOTUgMTQuNzM2IDEzLjU1MSAxNC43MzYgTSAxMC4wNzkgOS4wNTMgTCA2LjQ0OSAxNC43MzYiIHN0eWxlPSJmaWxsOiBub25lOyBzdHJva2U6IHJnYigyNTUsIDI1NSwgMjU1KTsgc3Ryb2tlLWxpbmVjYXA6IHJvdW5kOyBzdHJva2Utd2lkdGg6IDJweDsiPjwvcGF0aD4KPC9zdmc+",
            blocks: [
                {
                    opcode: 'arg',
                    text: 'argument',
                    blockType: BlockType.REPORTER,
                    hideFromPalette: true,
                    allowDropAnywhere: true,
                    canDragDuplicate: true
                },
                {
                    opcode: 'newLambda',
                    text: 'new lambda [ARG]',
                    hideFromPalette: true,
                    arguments: {
                        ARG: {
                            fillIn: 'arg'
                        }
                    },
                    branches: [{}],
                    ...Lambda.Block
                },
                {
                    blockType: BlockType.XML,
                    xml: `
                    <block type="jwLambda_newLambda">
                        <value name="ARG">
                            <shadow type="jwLambda_arg" />
                        </value>
                        <value name="SUBSTACK">
                            <block type="procedures_return">
                                <value name="return">
                                    <shadow type="text">
                                        <field name="TEXT">1</field>
                                    </shadow>
                                </value>
                            </block>
                        </value>
                    </block>
                    `
                },
                {
                    opcode: 'rawLambdaInput',
                    text: '[FIELD]',
                    hideFromPalette: true,
                    blockType: BlockType.REPORTER,
                    blockShape: BlockShape.SQUARE,
                    arguments: {
                        FIELD: {
                            type: ArgumentType.CUSTOM, id: "SPjavascriptV2-codeEditor",
                            defaultValue: "function* (arg, thread, target, runtime, stage) {\n  return 1;\n}"
                        }
                    }
                },
                {
                    opcode: 'rawLambda',
                    text: 'new lambda [RAW]',
                    hideFromPalette: true/*!this.rawLambdaAvailable || !(typeof ScratchBlocks === "object")*/,
                    arguments: {
                        RAW: {
                            fillIn: "rawLambdaInput"
                        }
                    },
                    ...Lambda.Block
                },
                "---",
                {
                    opcode: 'execute',
                    text: 'execute [LAMBDA] with [ARG]',
                    arguments: {
                        LAMBDA: Lambda.Argument,
                        ARG: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                            exemptFromNormalization: true
                        }
                    }
                },
                {
                    opcode: 'executeR',
                    text: 'execute [LAMBDA] with [ARG]',
                    blockType: BlockType.REPORTER,
                    allowDropAnywhere: true,
                    arguments: {
                        LAMBDA: Lambda.Argument,
                        ARG: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                            exemptFromNormalization: true
                        }
                    }
                },
                "---",
                {
                    opcode: 'this',
                    text: 'this lambda',
                    ...Lambda.Block
                },
                {
                    opcode: 'timesExecuted',
                    text: 'times [LAMBDA] executed',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        LAMBDA: Lambda.Argument
                    }
                }
            ]
        };
    }
}

module.exports = Extension