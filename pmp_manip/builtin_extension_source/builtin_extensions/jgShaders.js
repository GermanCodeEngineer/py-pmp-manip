const BlockType = require('../../extension-support/block-type');

/**
 * Class for Shaders blocks
 * @constructor
 */
class jgShadersBlocks {
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
            id: 'jgShaders',
            name: 'Shaders',
            blocks: [
                {
                    opcode: 'enableShader',
                    text: 'enable [SHADER]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        SHADER: {
                            menu: "shaders"
                        }
                    }
                },
                {
                    opcode: 'disableShader',
                    text: 'disable [SHADER]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        SHADER: {
                            menu: "shaders"
                        }
                    }
                },
            ],
            menus: {
                shaders: {
                    items: [
                        'bloom'
                    ]
                },
            }
        };
    }
}

module.exports = jgShadersBlocks;
