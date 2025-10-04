const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for CloneTool blocks
 * @constructor
 */
class JgCloneToolBlocks {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'jgClones',
            name: 'Clone Communication',
            color1: '#FFAB19',
            color2: '#EC9C13',
            blocks: [
                {
                    blockType: BlockType.LABEL,
                    text: "Main Sprite Communication"
                },
                {
                    opcode: 'getCloneWithVariableSetTo',
                    text: formatMessage({
                        id: 'jgClones.blocks.getCloneWithVariableSetTo',
                        default: 'get [DATA] of clone with [VAR] set to [VALUE]',
                        description: 'Block that returns the value of the item picked within a clone with a variable set to a certain value.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        DATA: { type: ArgumentType.STRING, menu: 'spriteData' },
                        VAR: { type: ArgumentType.STRING, menu: 'spriteVariables' },
                        VALUE: { type: ArgumentType.STRING, defaultValue: '0' },
                    }
                },
                {
                    opcode: 'getCloneVariableWithVariableSetTo',
                    text: formatMessage({
                        id: 'jgClones.blocks.getCloneVariableWithVariableSetTo',
                        default: 'get [VAR1] of clone with [VAR2] set to [VALUE]',
                        description: 'Block that returns the value of the variable picked within a clone with a variable set to a certain value.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VAR1: { type: ArgumentType.STRING, menu: 'spriteVariables' },
                        VAR2: { type: ArgumentType.STRING, menu: 'spriteVariables' },
                        VALUE: { type: ArgumentType.STRING, defaultValue: '0' },
                    }
                },
                // {
                //     opcode: 'setValueOnCloneWithVariableSetTo',
                //     text: formatMessage({
                //         id: 'jgClones.blocks.setValueOnCloneWithVariableSetTo',
                //         default: 'set [DATA] to [VALUE1] on clone with [VAR] set to [VALUE2]',
                //         description: 'Block that sets the value of the item picked within a clone with a variable set to a certain value.'
                //     }),
                //     blockType: BlockType.COMMAND,
                //     arguments: {
                //         DATA: { type: ArgumentType.STRING, menu: 'spriteData' },
                //         VALUE1: { type: ArgumentType.STRING, defaultValue: '0' },
                //         VAR: { type: ArgumentType.STRING, menu: 'spriteVariables' },
                //         VALUE2: { type: ArgumentType.STRING, defaultValue: '0' },
                //     }
                // },
                {
                    opcode: 'setVariableOnCloneWithVariableSetTo',
                    text: formatMessage({
                        id: 'jgClones.blocks.setVariableOnCloneWithVariableSetTo',
                        default: 'set [VAR1] to [VALUE1] on clone with [VAR2] set to [VALUE2]',
                        description: 'Block that sets a variable within a clone with a variable set to a certain value.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VAR1: { type: ArgumentType.STRING, menu: 'spriteVariables' },
                        VALUE1: { type: ArgumentType.STRING, defaultValue: '0' },
                        VAR2: { type: ArgumentType.STRING, menu: 'spriteVariables' },
                        VALUE2: { type: ArgumentType.STRING, defaultValue: '0' },
                    }
                },
                "---",
                "---",
                {
                    blockType: BlockType.LABEL,
                    text: "Clone Communication"
                },
                {
                    opcode: 'getMainSpriteData',
                    text: formatMessage({
                        id: 'jgClones.blocks.getMainSpriteData',
                        default: 'get [DATA] of main sprite',
                        description: 'Block that returns the value of the item picked on the main sprite.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        DATA: { type: ArgumentType.STRING, menu: 'spriteData' }
                    }
                },
                {
                    opcode: 'getVariableOnMainSprite',
                    text: formatMessage({
                        id: 'jgClones.blocks.getVariableOnMainSprite',
                        default: 'get [VAR] of main sprite',
                        description: 'Block that returns the value of the variable picked on the main sprite.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        VAR: { type: ArgumentType.STRING, menu: 'spriteVariables' },
                    }
                },
                // {
                //     opcode: 'setValueOnMainSprite',
                //     text: formatMessage({
                //         id: 'jgClones.blocks.setValueOnMainSprite',
                //         default: 'set [DATA] to [VALUE] on main sprite',
                //         description: 'Block that sets the value of the item picked within the main sprite.'
                //     }),
                //     blockType: BlockType.COMMAND,
                //     arguments: {
                //         DATA: { type: ArgumentType.STRING, menu: 'spriteData' },
                //         VALUE: { type: ArgumentType.STRING, defaultValue: '0' }
                //     }
                // },
                {
                    opcode: 'setVariableOnMainSprite',
                    text: formatMessage({
                        id: 'jgClones.blocks.setVariableOnMainSprite',
                        default: 'set [VAR] to [VALUE] on main sprite',
                        description: 'Block that sets a variable within the main sprite.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VAR: { type: ArgumentType.STRING, menu: 'spriteVariables' },
                        VALUE: { type: ArgumentType.STRING, defaultValue: '0' }
                    }
                },
                "---",
                "---",
                {
                    blockType: BlockType.LABEL,
                    text: "Other"
                },
                {
                    opcode: 'getIsClone',
                    text: formatMessage({
                        id: 'jgClones.blocks.getIsClone',
                        default: 'is clone?',
                        description: 'Block that returns whether the current sprite is a clone or not.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'clonesInSprite',
                    text: formatMessage({
                        id: 'jgClones.blocks.clonesInSprite',
                        default: 'clone count of [SPRITE]',
                        description: 'Block that returns the amount of clones of this sprite that currently exist.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        SPRITE: { type: ArgumentType.STRING, menu: 'sprites' },
                    }
                }
            ],
            menus: {
                sprites: "getSpriteMenu",
                spriteVariables: "getSpriteVariablesMenu",
                spriteData: {
                    acceptReporters: true,
                    items: [
                        // motion
                        "x position",
                        "y position",
                        "direction",
                        "rotation style",
                        // looks (excluding effects)
                        "visible",
                        "costume number",
                        "costume name",
                        "size",
                        "x stretch",
                        "y stretch",
                        // sound
                        "volume",
                        // sensing
                        "draggable",
                        // music (doesnt seem to work)
                        // "tempo",

                        // effects
                        "color effect",
                        "fisheye effect",
                        "whirl effect",
                        "pixelate effect",
                        "mosaic effect",
                        "brightness effect",
                        "ghost effect",
                        "saturation effect",
                        "red effect",
                        "green effect",
                        "blue effect",
                        "opaque effect",
                    ].map(item => ({ text: item, value: item }))
                }
            }
        };
    }
}

module.exports = JgCloneToolBlocks;
