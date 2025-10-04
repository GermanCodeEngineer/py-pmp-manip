const BlockType = require('../../extension-support/block-type');

/**
 * Class for blocks
 * @constructor
 */
class JgBestExtensionBlocks {
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
            id: 'jgBestExtension',
            name: 'the great',
            color1: '#ff0000',
            color2: '#00ff00',
            color3: '#0000ff',
            blocks: [
                {
                    opcode: 'ohioBlock',
                    text: 'absolutely delectable!',
                    blockType: BlockType.COMMAND,
                    disableMonitor: false
                }
            ]
        };
    }
}

module.exports = JgBestExtensionBlocks;
