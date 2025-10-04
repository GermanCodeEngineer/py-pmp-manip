const BlockType = require('../../extension-support/block-type');

/**
 * Class for Extension blocks
 * @constructor
 */
class Extension {
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
            id: 'jgChristmas',
            name: 'Christmas',
            color1: '#ff0000',
            color2: '#00ff00',
            blockIconURI: null, // Icons do not matter
            blocks: [
                {
                    opcode: 'snow',
                    text: 'snow',
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'clearSnow',
                    text: 'clear snow',
                    blockType: BlockType.COMMAND
                },
                // {
                //     opcode: 'addPresent',
                //     text: 'add present',
                //     blockType: BlockType.COMMAND
                // },
                // {
                //     opcode: 'removePresents',
                //     text: 'remove all presents',
                //     blockType: BlockType.COMMAND
                // },
                {
                    opcode: 'addLight',
                    text: 'add light',
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'removeLights',
                    text: 'remove all lights',
                    blockType: BlockType.COMMAND
                },
            ]
        };
    }
}

module.exports = Extension;
