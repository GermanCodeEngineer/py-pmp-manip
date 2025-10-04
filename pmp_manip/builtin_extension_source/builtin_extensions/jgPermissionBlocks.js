const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for Permission blocks
 * @constructor
 */
class JgPermissionBlocks {
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
            id: 'JgPermissionBlocks',
            name: 'Permissions',
            color1: '#00C4FF',
            color2: '#0093FF',
            blocks: [
                {
                    blockType: BlockType.LABEL,
                    text: "This extension is deprecated."
                },
                // tw says deleting menu elements is unsafe
                // blocks below this are hidden
                { hideFromPalette: true, opcode: 'requestPermission', text: 'request [PERMISSION] permission', disableMonitor: false, blockType: BlockType.BOOLEAN, arguments: { PERMISSION: { type: ArgumentType.STRING, menu: 'permissions', defaultValue: "javascript" } } },
                { hideFromPalette: true, opcode: 'requestPermission2', text: 'request [PERMISSION] permission', disableMonitor: false, blockType: BlockType.BOOLEAN, arguments: { PERMISSION: { type: ArgumentType.STRING, menu: 'permissions2' } } },
                { hideFromPalette: true, opcode: 'requestAllPermission', text: 'request all permissions', disableMonitor: false, blockType: BlockType.BOOLEAN },
                { hideFromPalette: true, opcode: 'requestSitePermission', text: 'request permission to show [URL]', disableMonitor: false, blockType: BlockType.BOOLEAN, arguments: { URL: { type: ArgumentType.STRING, defaultValue: "https://www.example.com" } } },
            ],
            menus: {
                // tw says deleting menu elements is unsafe
                // menus below this are hidden
                permissions: "fetchPermissionsList",
                permissions2: "fetchPermissionsList2"
            }
        };
    }
}

module.exports = JgPermissionBlocks;
