const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');
const Icons = { // Icons do not matter
    Mouse: null,
    Button: null,
    Text: null,
    Textarea: null,
    Box: null,
    ScrollingBox: null,
    Checkbox: null,
    Dropdown: null,
    Multiselect: null,
    Slider: null,
}

/**
 * Class
 * @constructor
 */
class jgAdvancedText {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'jgInterfaces',
            name: 'Interfaces',
            color1: '#ac96b5',
            color2: '#8e7a96',
            blocks: [
                {
                    opcode: 'createButton',
                    text: 'create button named: [NAME] with text: [TEXT]',
                    blockIconURI: Icons.Button,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Button'
                        },
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Click me'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'createTextInput',
                    text: 'create text input named: [NAME] with placeholder: [PLACEHOLDER] and default: [DEFAULT]',
                    blockIconURI: Icons.Text,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'TextInput'
                        },
                        PLACEHOLDER: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Type here...'
                        },
                        DEFAULT: {
                            type: ArgumentType.STRING,
                            defaultValue: ' '
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'createTextBox',
                    text: 'create textbox named: [NAME] with placeholder: [PLACEHOLDER] and default: [DEFAULT] being resizable? [RESIZE]',
                    blockIconURI: Icons.Textarea,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Textbox'
                        },
                        PLACEHOLDER: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Type here...'
                        },
                        DEFAULT: {
                            type: ArgumentType.STRING,
                            defaultValue: ' '
                        },
                        RESIZE: {
                            type: ArgumentType.BOOLEAN
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'createDropdown',
                    text: 'create dropdown menu named: [NAME] with label: [LABEL]',
                    blockIconURI: Icons.Dropdown,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Dropdown'
                        },
                        LABEL: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Click me'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'createCheckbox',
                    text: 'create checkbox named: [NAME] with label: [LABEL]',
                    blockIconURI: Icons.Checkbox,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Checkbox'
                        },
                        LABEL: {
                            type: ArgumentType.STRING,
                            defaultValue: ' '
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'createSlider',
                    text: 'create slider named: [NAME] minimum number: [MIN] maximum number: [MAX]',
                    blockIconURI: Icons.Slider,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Slider'
                        },
                        MIN: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        MAX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'createScrollingArea',
                    text: 'create scrolling box named: [NAME]',
                    blockIconURI: Icons.ScrollingBox,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Scroll area'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'createMultiselect',
                    text: 'create multiselect box named: [NAME]',
                    blockIconURI: Icons.Multiselect,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Multi-select'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'createGroup',
                    text: 'create group box named: [NAME]',
                    blockIconURI: Icons.Box,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Box'
                        }
                    },
                    blockType: BlockType.COMMAND
                },
            ]
        };
    }
}

module.exports = jgAdvancedText;
