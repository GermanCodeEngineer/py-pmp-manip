const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for blocks
 * @constructor
 */
class JgDooDooBlocks {
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
            id: 'jgDooDoo',
            name: 'doo doo',
            color1: '#59C059',
            color2: '#46B946',
            color3: '#389438',
            blocks: [
                {
                    opcode: 'returnSelectedCharacter',
                    text: '[CHAR]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        CHAR: { type: ArgumentType.STRING, menu: "funny" }
                    }
                },
                {
                    text: 'ip addresses are fake',
                    blockType: BlockType.LABEL,
                },
                {
                    text: '(sorry not sorry)',
                    blockType: BlockType.LABEL,
                },
                {
                    opcode: 'fullNameIp',
                    text: 'ip address of [NAME]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "gloobert dooben" }
                    }
                },
                {
                    opcode: 'randomStartupIp',
                    text: 'ip address',
                    blockType: BlockType.REPORTER,
                    disableMonitor: false
                },
                {
                    opcode: 'chicago',
                    text: 'chicago',
                    blockType: BlockType.REPORTER,
                    disableMonitor: false
                },
                '---',
                {
                    opcode: 'doodoo',
                    text: 'go to x: 17 y: 36',
                    blockType: BlockType.COMMAND,
                    disableMonitor: false
                },
                {
                    opcode: 'visualReportbad',
                    text: 'give me admin on PenguinMod',
                    blockType: BlockType.COMMAND
                },
                '---',
                {
                    opcode: 'launchroblox',
                    text: 'launch roblox',
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'launchrobloxgame',
                    text: 'open roblox game id: [ID]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ID: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 11219669059
                        }
                    }
                },
            ],
            menus: {
                funny: "getAllCharacters"
            }
        };
    }
}

module.exports = JgDooDooBlocks;
