const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for PostLit blocks
 * @constructor
 */
class jwPostLit {
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
            id: 'jwPostLit',
            name: 'postLit',
            //blockIconURI: blockIconURI,
            color2: '#14f789',
            color1: '#0fd173',
            blocks: [
                {
                    opcode: 'categorySignIn',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.categorySignIn',
                        default: 'Sign In',
                        description: 'Sign in to postLit.'
                    }),
                    blockType: BlockType.LABEL
                },
                {
                    opcode: 'signIn',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.signIn',
                        default: 'sign in [USER] [PASS]',
                        description: 'Sign in to postLit.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        USER: {
                            type: ArgumentType.STRING,
                            defaultValue: "username"
                        },
                        PASS: {
                            type: ArgumentType.STRING,
                            defaultValue: "password"
                        }
                    }
                },
                {
                    opcode: 'currentUsername',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.currentUsername',
                        default: 'username',
                        description: 'Username for your postLit account.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'currentToken',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.currentToken',
                        default: 'token',
                        description: 'Token for your postLit account.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'isSignedIn',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.isSignedIn',
                        default: 'signed in?',
                        description: 'Checks if you are currently signed into a postLit account.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.BOOLEAN
                },
                "---",
                {
                    opcode: 'categoryPosts',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.categoryPosts',
                        default: 'Posts',
                        description: 'Blocks to create and get data from posts'
                    }),
                    blockType: BlockType.LABEL
                },
                {
                    opcode: 'createPost',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.createPost',
                        default: 'create post [STRING]',
                        description: 'Create a post.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        STRING: {
                            type: ArgumentType.STRING,
                            defaultValue: "post"
                        }
                    }
                },
                {
                    opcode: 'getLatestPost',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.getLatestPost',
                        default: 'latest post id',
                        description: 'Gets the ID of the latest post made with the create post block.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER
                },
                "---",
                {
                    opcode: 'getPost',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.getPost',
                        default: 'get post [ID] [WANTS]',
                        description: 'Gets some data from a post.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ID: {
                            type: ArgumentType.STRING,
                            defaultValue: 'id'
                        },
                        WANTS: {
                            type: ArgumentType.STRING,
                            defaultValue: 'json',
                            menu: 'getPostWants'
                        },
                    }
                },
                {
                    opcode: 'likePost',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.likePost',
                        default: 'like post [ID]',
                        description: 'Like a post.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ID: {
                            type: ArgumentType.STRING,
                            defaultValue: 'id'
                        },
                    }
                },
                {
                    opcode: 'unlikePost',
                    text: formatMessage({
                        id: 'jwPostLit.blocks.unlikePost',
                        default: 'unlike post [ID]',
                        description: 'Unlike a post.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ID: {
                            type: ArgumentType.STRING,
                            defaultValue: 'id'
                        },
                    }
                }
            ],
            menus: {
                getPostWants: [
                    'json',
                    'author',
                    'content',
                    'time',
                    'comments',
                    'likes',
                    'likers',
                    'reposts'
                ]
            }
        };
    }
}

module.exports = jwPostLit;
