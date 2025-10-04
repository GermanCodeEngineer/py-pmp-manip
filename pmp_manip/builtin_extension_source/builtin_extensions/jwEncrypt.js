const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for Proto blocks
 * @constructor
 */
class jwEncrypt {
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
            autoLoad: true,
            id: 'jwEncrypt',
            name: 'Encrypt',
            // blockIconURI: blockIconURI,
            color1: '#ffdc7a',
            color2: '#ffd45e',
            blocks: [
                {
                    opcode: 'encrypt',
                    text: formatMessage({
                        id: 'jwEncrypt.blocks.encrypt',
                        default: 'encrypt [MENU] [VALUE]',
                        description: 'Encrypt a string'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "string"
                        },
                        MENU: {
                            type: ArgumentType.STRING,
                            defaultValue: 'base64',
                            menu: 'encrypt'
                        }
                    }
                }
            ],
            menus: {
                encrypt: [
                    'base64'
                ]
            }
        };
    }
}

module.exports = jwEncrypt;
