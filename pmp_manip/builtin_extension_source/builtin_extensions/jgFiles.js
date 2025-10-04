const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const noopSwitch = { isNoop: true };

/**
 * Class for File blocks
 * @constructor
 */
class JgFilesBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'jgFiles',
            name: 'Files (legacy)',
            color1: '#ffbb00',
            color2: '#ffaa00',
            // docsURI: 'https://docs.turbowarp.org/blocks',
            blocks: [
                {
                    opcode: 'isFileReaderSupported',
                    text: 'can files be used?',
                    disableMonitor: false,
                    blockType: BlockType.BOOLEAN
                },
                {
                    opcode: 'askUserForFileOfType',
                    text: 'ask user for a file of type [FILE_TYPE]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        FILE_TYPE: {
                            type: ArgumentType.STRING,
                            defaultValue: 'txt savefile'
                        }
                    },
                    switches: [
                        noopSwitch,
                        'askUserForFileOfTypeAsArrayBuffer',
                        'askUserForFileOfTypeAsDataUri',
                    ],
                    switchText: 'ask for file'
                },
                {
                    opcode: 'askUserForFileOfTypeAsArrayBuffer',
                    text: 'ask user for an array buffer file of type [FILE_TYPE]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        FILE_TYPE: {
                            type: ArgumentType.STRING,
                            defaultValue: 'txt savefile'
                        }
                    },
                    switches: [
                        'askUserForFileOfType',
                        noopSwitch,
                        'askUserForFileOfTypeAsDataUri',
                    ],
                    switchText: 'ask for array buffer'
                },
                {
                    opcode: 'askUserForFileOfTypeAsDataUri',
                    text: 'ask user for a data uri file of type [FILE_TYPE]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        FILE_TYPE: {
                            type: ArgumentType.STRING,
                            defaultValue: 'png'
                        }
                    },
                    switches: [
                        'askUserForFileOfType',
                        'askUserForFileOfTypeAsArrayBuffer',
                        noopSwitch,
                    ],
                    switchText: 'ask for data uri'
                },
                {
                    opcode: 'downloadFile',
                    text: 'download content [FILE_CONTENT] as file name [FILE_NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        FILE_CONTENT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Hello!'
                        },
                        FILE_NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'text.txt'
                        }
                    },
                    switches: [
                        noopSwitch,
                        'downloadFileDataUri',
                        'downloadFileBuffer',
                    ],
                    switchText: 'download file'
                },
                {
                    opcode: 'downloadFileDataUri',
                    text: 'download data uri [FILE_CONTENT] as file name [FILE_NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        FILE_CONTENT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'data:image/png;base64,'
                        },
                        FILE_NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'content.png'
                        }
                    },
                    switches: [
                        'downloadFile',
                        noopSwitch,
                        'downloadFileBuffer',
                    ],
                    switchText: 'download data uri'
                },
                {
                    opcode: 'downloadFileBuffer',
                    text: 'download array buffer [FILE_CONTENT] as file name [FILE_NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        FILE_CONTENT: {
                            type: ArgumentType.STRING,
                            defaultValue: '[]'
                        },
                        FILE_NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'data.bin'
                        }
                    },
                    switches: [
                        'downloadFile',
                        'downloadFileDataUri',
                        noopSwitch
                    ],
                    switchText: 'download array buffer'
                }
            ]
        };
    }
}

module.exports = JgFilesBlocks;
