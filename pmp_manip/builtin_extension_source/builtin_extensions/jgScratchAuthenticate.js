const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const Icon = null; // Icons do not matter

/**
 * Class for Scratch Authentication blocks
 * @constructor
 */
class JgScratchAuthenticateBlocks {
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
            id: 'jgScratchAuthenticate',
            name: 'Scratch Auth',
            color1: '#FFA01C',
            color2: '#ff8C00',
            blockIconURI: Icon,
            // TODO: docs doesnt exist, make some docs
            // docsURI: 'https://docs.penguinmod.com/extensions/scratch-auth',
            blocks: [
                // LEGACY BLOCK
                {
                    opcode: 'authenticate',
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.blocks.authenticate',
                        default: 'get scratch username and set sign in location name to [NAME]',
                        description: "Block that returns the user's name on Scratch."
                    }),
                    disableMonitor: true,
                    hideFromPalette: true,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "PenguinMod" }
                    },
                    blockType: BlockType.REPORTER
                },
                // NEW BLOCKS
                {
                    opcode: 'showPrompt',
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.blocks.showPrompt',
                        default: 'show login message as [NAME]',
                        description: "Block that shows the Log in menu from Scratch Authentication."
                    }),
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            menu: 'loginLocation'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'getPromptStatus',
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.blocks.promptStatus',
                        default: 'login prompt [STATUS]?',
                        description: "The status of the login prompt for Scratch Authentication."
                    }),
                    arguments: {
                        STATUS: {
                            type: ArgumentType.STRING,
                            menu: "promptStatus"
                        }
                    },
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'privateCode',
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.blocks.privateCode',
                        default: 'authentication code',
                        description: "The login code when Scratch Authentication closes the login prompt."
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'serverRedirectLocation',
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.blocks.serverRedirectLocation',
                        default: 'redirect location',
                        description: "The redirect location when Scratch Authentication closes the login prompt."
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                '---',
                {
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.labels.loginInfo1',
                        default: 'The blocks below invalidate',
                        description: "Label to denote that blocks invalidate the Scratch Auth private code below this label"
                    }),
                    blockType: BlockType.LABEL
                },
                {
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.labels.loginInfo2',
                        default: 'the authentication code from above.',
                        description: "Label to denote that blocks invalidate the Scratch Auth private code below this label"
                    }),
                    blockType: BlockType.LABEL
                },
                {
                    opcode: 'validLogin',
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.blocks.validLogin',
                        default: 'login is valid?',
                        description: "Whether or not the authentication was valid."
                    }),
                    disableMonitor: true,
                    // this doesnt seem to be important,
                    // login should always be valid when checking on client-side
                    hideFromPalette: true,
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'scratchUsername',
                    text: formatMessage({
                        id: 'jgScratchAuthenticate.blocks.scratchUsername',
                        default: 'scratch username',
                        description: "The username that was logged in."
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
            ],
            menus: {
                loginLocation: {
                    items: '_getLoginLocations',
                    isTypeable: true,
                },
                promptStatus: [
                    { text: 'in progress', value: 'inProgress' },
                    { text: 'blocked', value: 'blocked' },
                    { text: 'complete', value: 'completed' },
                    { text: 'closed by the user', value: 'userClosed' },
                ]
            }
        };
    }
}

module.exports = JgScratchAuthenticateBlocks;
