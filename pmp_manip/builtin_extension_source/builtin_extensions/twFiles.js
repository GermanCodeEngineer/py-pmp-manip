const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const MODE_MODAL = 'modal';
const MODE_IMMEDIATELY_SHOW_SELECTOR = 'selector';

const AS_TEXT = 'text';
const AS_BUFFER = 'buffer';
const AS_DATA_URL = 'url';

class Files {
    getInfo() {
        return {
            id: 'twFiles',
            name: 'Files',
            color1: '#fcb103',
            color2: '#db9a37',
            color3: '#db8937',
            blocks: [
                {
                    opcode: 'showPicker',
                    blockType: BlockType.REPORTER,
                    text: 'open a file',
                    disableMonitor: true,
                    hideFromPalette: true
                },
                {
                    opcode: 'showPickerExtensions',
                    blockType: BlockType.REPORTER,
                    text: 'open a [extension] file',
                    arguments: {
                        extension: {
                            type: ArgumentType.STRING,
                            defaultValue: '.txt'
                        }
                    },
                    hideFromPalette: true
                },

                {
                    opcode: 'showPickerAs',
                    blockType: BlockType.REPORTER,
                    text: 'open a file as [as]',
                    arguments: {
                        as: {
                            type: ArgumentType.STRING,
                            menu: 'encoding'
                        }
                    }
                },
                {
                    opcode: 'showPickerExtensionsAs',
                    blockType: BlockType.REPORTER,
                    text: 'open a [extension] file as [as]',
                    arguments: {
                        extension: {
                            type: ArgumentType.STRING,
                            defaultValue: '.txt'
                        },
                        as: {
                            type: ArgumentType.STRING,
                            menu: 'encoding'
                        }
                    }
                },

                '---',

                {
                    opcode: 'download',
                    blockType: BlockType.COMMAND,
                    text: 'download [encoding] [text] as [file]',
                    arguments: {
                        encoding: {
                            type: ArgumentType.STRING,
                            menu: 'encoding'
                        },
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Hello, world!'
                        },
                        file: {
                            type: ArgumentType.STRING,
                            defaultValue: 'save.txt'
                        }
                    }
                },
                {
                    opcode: 'setOpenMode',
                    blockType: BlockType.COMMAND,
                    text: 'set open file selector mode to [mode]',
                    arguments: {
                        mode: {
                            type: ArgumentType.STRING,
                            defaultValue: MODE_MODAL,
                            menu: 'automaticallyOpen'
                        }
                    }
                },
                '---',
                {
                    opcode: 'getFileName',
                    blockType: BlockType.REPORTER,
                    text: 'last opened file name',
                    disableMonitor: true
                }
            ],
            menus: {
                encoding: {
                    acceptReporters: true,
                    items: [
                        {
                            text: 'text',
                            value: AS_TEXT
                        },
                        {
                            text: 'data: URL',
                            value: AS_DATA_URL
                        },
                        {
                            text: 'array buffer',
                            value: AS_BUFFER
                        }
                    ]
                },
                automaticallyOpen: {
                    acceptReporters: true,
                    items: [
                        {
                            text: 'show modal',
                            value: MODE_MODAL
                        },
                        {
                            text: 'open selector immediately',
                            value: MODE_IMMEDIATELY_SHOW_SELECTOR
                        }
                    ]
                }
            }
        };
    }
}

module.exports = Files;
