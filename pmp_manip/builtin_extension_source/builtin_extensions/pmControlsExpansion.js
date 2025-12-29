const BlockType = require('../../extension-support/block-type');
const BlockShape = require('../../extension-support/block-shape');
const ArgumentType = require('../../extension-support/argument-type');
const ArgumentAlignment = require('../../extension-support/argument-alignment');
const AsyncIcon = null; // Icons do not matter

const pathToMedia = 'static/blocks-media'; // ScratchBlocks.mainWorkspace.options.pathToMedia

/**
 * Class of idk
 * @constructor
 */
class pmControlsExpansion {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for extension category NOT blocks
     * this extension only contains blocks defined elsewhere,
     * since we just want to seperate them rather than create
     * slow versions of them
     */
    getInfo() {
        return {
            id: 'pmControlsExpansion',
            name: 'Controls Expansion',
            color1: '#FFAB19',
            color2: '#EC9C13',
            color3: '#CF8B17',
            isDynamic: true,
            blocks: [
                {
                    opcode: "control_repeatForSeconds",
                    ppm_final_opcode: true,
                    text: "repeat for [TIMES] seconds",
                    branchCount: 1,
                    blockType: BlockType.CONDITIONAL,
                    arguments: {
                        TIMES: { type: ArgumentType.NUMBER, defaultValue: 1 },
                    },
                },
                {
                    opcode: "control_inline_stack_output",
                    ppm_final_opcode: true,
                    text: "inline block",
                    branchCount: 1,
                    blockType: BlockType.REPORTER, // Technically unknown but behaves like REPORTER+SQUARE
                    blockShape: BlockShape.SQUARE,
                    disableMonitor: true,
                },
                {
                    opcode: "control_waittick",
                    ppm_final_opcode: true,
                    text: "wait until next tick",
                    blockType: BlockType.COMMAND,
                },
                {
                    opcode: 'asNewBroadcast',
                    text: [
                        'new thread',
                        '[ICON]'
                    ],
                    branchCount: 1,
                    blockType: BlockType.CONDITIONAL,
                    alignments: [
                        null, // text
                        null, // SUBSTACK
                        ArgumentAlignment.RIGHT // ICON
                    ],
                    arguments: {
                        ICON: {
                            type: ArgumentType.IMAGE,
                            dataURI: AsyncIcon
                        }
                    }
                },
                {
                    opcode: 'restartFromTheTop',
                    text: 'restart from the top [ICON]',
                    blockType: BlockType.COMMAND,
                    isTerminal: true,
                    arguments: {
                        ICON: {
                            type: ArgumentType.IMAGE,
                            dataURI: `${pathToMedia}/repeat.svg`
                        }
                    }
                },
                {
                    opcode: 'asNewBroadcastArgs',
                    text: [
                        'new thread with data [DATA]',
                        '[ICON]'
                    ],
                    branchCount: 1,
                    blockType: BlockType.CONDITIONAL,
                    alignments: [
                        null, // text
                        null, // SUBSTACK
                        ArgumentAlignment.RIGHT // ICON
                    ],
                    arguments: {
                        DATA: {
                            type: ArgumentType.STRING,
                            defaultValue: "abc",
                            exemptFromNormalization: true
                        },
                        ICON: {
                            type: ArgumentType.IMAGE,
                            dataURI: AsyncIcon
                        }
                    }
                },
                {
                    opcode: 'asNewBroadcastArgBlock',
                    text: 'thread data',
                    blockType: BlockType.REPORTER,
                    allowDropAnywhere: true,
                    disableMonitor: true
                },
                {
                    opcode: "control_get_counter",
                    ppm_final_opcode: true,
                    text: "counter",
                    blockType: BlockType.REPORTER,
                },
                {
                    opcode: "control_incr_counter",
                    ppm_final_opcode: true,
                    text: "increment counter",
                    blockType: BlockType.COMMAND,
                },
                {
                    opcode: "control_decr_counter",
                    ppm_final_opcode: true,
                    text: "decrement counter",
                    blockType: BlockType.COMMAND,
                },
                {
                    opcode: "control_set_counter",
                    ppm_final_opcode: true,
                    text: "set counter to [VALUE]",
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VALUE: { type: ArgumentType.NUMBER, defaultValue: 10 },
                    },
                },
                {
                    opcode: "control_clear_counter",
                    ppm_final_opcode: true,
                    text: "clear counter",
                    blockType: BlockType.COMMAND,
                },
                /*{ // would create conflicts with builtin categories
                    opcode: 'control_if',
                    ppm_final_opcode: true,
                    text: [
                        'if [CONDITION] then',
                    ],
                    branchCount: 1,
                    blockType: BlockType.CONDITIONAL,
                    arguments: {
                        CONDITION: { type: ArgumentType.BOOLEAN }
                    }
                },
                {
                    opcode: 'control_if_else',
                    ppm_final_opcode: true,
                    text: [
                        'if [CONDITION] then',
                        'else'
                    ],
                    branchCount: 2,
                    blockType: BlockType.CONDITIONAL,
                    arguments: {
                        CONDITION: { type: ArgumentType.BOOLEAN }
                    }
                },*/
                {
                    opcode: 'ifElseIf',
                    text: [
                        'if [CONDITION1] then',
                        'else if [CONDITION2] then'
                    ],
                    branchCount: 2,
                    blockType: BlockType.CONDITIONAL,
                    arguments: {
                        CONDITION1: { type: ArgumentType.BOOLEAN },
                        CONDITION2: { type: ArgumentType.BOOLEAN }
                    }
                },
                {
                    opcode: 'ifElseIfElse',
                    text: [
                        'if [CONDITION1] then',
                        'else if [CONDITION2] then',
                        'else'
                    ],
                    branchCount: 3,
                    blockType: BlockType.CONDITIONAL,
                    arguments: {
                        CONDITION1: { type: ArgumentType.BOOLEAN },
                        CONDITION2: { type: ArgumentType.BOOLEAN }
                    }
                },
            ]
        };
    }
}

module.exports = pmControlsExpansion;
