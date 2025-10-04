const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');



/**
 * Class for 3d Physics blocks
 */
class Fr3DBlocks {
    /**
     * metadata for this extension and its blocks.
     * @returns {object}
     */
    getInfo() {
        return {
            id: 'fr3d',
            name: '3D Physics',
            color1: '#D066FE',
            color2: '#8000BC',
            blocks: [
                {
                    opcode: 'step',
                    text: 'step simulation',
                    blockType: BlockType.COMMAND,
                },
                {
                    opcode: 'addp',
                    text: 'enable physics for [NAME1]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME1: { type: ArgumentType.STRING, defaultValue: "Object1" }
                    }
                },
                {
                    opcode: 'rmp',
                    text: 'disable physics for [NAME1]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME1: { type: ArgumentType.STRING, defaultValue: "Object1" }
                    }
                }
            ]
        };
    }
}

module.exports = Fr3DBlocks;
