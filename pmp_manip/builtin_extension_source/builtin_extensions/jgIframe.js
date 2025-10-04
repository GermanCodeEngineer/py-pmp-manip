const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const EffectOptions = {
    acceptReporters: true,
    items: [
        { text: "color", value: "color" },
        { text: "grayscale", value: "grayscale" },
        { text: "brightness", value: "brightness" },
        { text: "contrast", value: "contrast" },
        { text: "ghost", value: "ghost" },
        { text: "blur", value: "blur" },
        { text: "invert", value: "invert" },
        { text: "saturate", value: "saturate" },
        { text: "sepia", value: "sepia" }
    ]
};

/**
 * Class for IFRAME blocks
 * @constructor
 */
class JgIframeBlocks {
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
            id: 'jgIframe',
            name: 'IFrame',
            color1: '#F36518',
            color2: '#E64D18',
            blocks: [
                {
                    opcode: 'createIframeElement',
                    text: formatMessage({
                        id: 'jgIframe.blocks.createIframeElement',
                        default: 'set new iframe',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'deleteIframeElement',
                    text: formatMessage({
                        id: 'jgIframe.blocks.deleteIframeElement',
                        default: 'delete iframe',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'iframeElementExists',
                    text: formatMessage({
                        id: 'jgIframe.blocks.iframeElementExists',
                        default: 'iframe exists?',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                },
                "---",
                "---",
                {
                    opcode: 'whenIframeIsLoaded',
                    text: formatMessage({
                        id: 'jgIframe.blocks.whenIframeIsLoaded',
                        default: 'when iframe loads site',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.HAT
                },
                {
                    opcode: 'setIframeUrl',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframeUrl',
                        default: 'set iframe url to [URL]',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: "https://www.example.com"
                        }
                    }
                },
                {
                    opcode: 'setIframePosLeft',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframePosLeft',
                        default: 'set iframe x to [X]',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'setIframePosTop',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframePosTop',
                        default: 'set iframe y to [Y]',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'setIframeSizeWidth',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframeSizeWidth',
                        default: 'set iframe width to [WIDTH]',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        WIDTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 480
                        }
                    }
                },
                {
                    opcode: 'setIframeSizeHeight',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframeSizeHeight',
                        default: 'set iframe height to [HEIGHT]',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        HEIGHT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 360
                        }
                    }
                },
                {
                    opcode: 'setIframeRotation',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframeRotation',
                        default: 'point iframe in direction [ROTATE]',
                        description: ''
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ROTATE: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 90
                        }
                    }
                },
                {
                    opcode: 'setIframeBackgroundColor',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframeBackgroundColor',
                        default: 'set iframe background color to [COLOR]',
                        description: ''
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    }
                },
                {
                    opcode: 'setIframeBackgroundOpacity',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframeBackgroundOpacity',
                        default: 'set iframe background transparency to [GHOST]%',
                        description: ''
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        GHOST: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        }
                    }
                },
                {
                    opcode: 'setIframeClickable',
                    text: formatMessage({
                        id: 'jgIframe.blocks.setIframeClickable',
                        default: 'toggle iframe to be [USABLE]',
                        description: ''
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        USABLE: {
                            type: ArgumentType.STRING,
                            menu: 'iframeClickable'
                        }
                    }
                },
                {
                    opcode: 'showIframeElement',
                    text: formatMessage({
                        id: 'jgIframe.blocks.showIframeElement',
                        default: 'show iframe',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'hideIframeElement',
                    text: formatMessage({
                        id: 'jgIframe.blocks.hideIframeElement',
                        default: 'hide iframe',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'getIframeLeft',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeLeft',
                        default: 'iframe x',
                        description: ''
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getIframeTop',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeTop',
                        default: 'iframe y',
                        description: ''
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getIframeWidth',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeWidth',
                        default: 'iframe width',
                        description: ''
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getIframeHeight',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeHeight',
                        default: 'iframe height',
                        description: ''
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getIframeRotation',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeRotation',
                        default: 'iframe rotation',
                        description: ''
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getIframeBackgroundColor',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeBackgroundColor',
                        default: 'iframe background color',
                        description: ''
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getIframeBackgroundOpacity',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeBackgroundOpacity',
                        default: 'iframe background transparency',
                        description: ''
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getIframeTargetUrl',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeTargetUrl',
                        default: 'iframe target url',
                        description: ''
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'iframeElementIsHidden',
                    text: formatMessage({
                        id: 'jgIframe.blocks.iframeElementIsHidden',
                        default: 'iframe is hidden?',
                        description: 'im too lazy to write these anymore tbh'
                    }),
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                },
                {
                    opcode: 'getIframeClickable',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeClickable',
                        default: 'iframe is interactable?',
                        description: ''
                    }),
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                },
                "---",
                "---",
                // effects YAYYAYAWOOHOOO YEEAAAAAAAAA
                {
                    opcode: 'iframeElementSetEffect',
                    text: formatMessage({
                        id: 'jgIframe.blocks.iframeElementSetEffect',
                        default: 'set [EFFECT] effect on iframe to [AMOUNT]',
                        description: 'YAYYAYAWOOHOOO YEEAAAAAAAAAYAYYAYAWOOHOOO YEEAAAAAAAAA'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        EFFECT: {
                            type: ArgumentType.STRING,
                            menu: 'effects',
                            defaultValue: "color"
                        },
                        AMOUNT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'iframeElementChangeEffect',
                    text: formatMessage({
                        id: 'jgIframe.blocks.iframeElementChangeEffect',
                        default: 'change [EFFECT] effect on iframe by [AMOUNT]',
                        description: 'YAYYAYAWOOHOOO YEEAAAAAAAAAYAYYAYAWOOHOOO YEEAAAAAAAAA'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        EFFECT: {
                            type: ArgumentType.STRING,
                            menu: 'effects',
                            defaultValue: "color"
                        },
                        AMOUNT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 25
                        }
                    }
                },
                {
                    opcode: 'iframeElementClearEffects',
                    text: formatMessage({
                        id: 'jgIframe.blocks.iframeElementClearEffects',
                        default: 'clear iframe effects',
                        description: 'YAYYAYAWOOHOOO YEEAAAAAAAAAYAYYAYAWOOHOOO YEEAAAAAAAAA'
                    }),
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'getIframeEffectAmount',
                    text: formatMessage({
                        id: 'jgIframe.blocks.getIframeEffectAmount',
                        default: 'iframe [EFFECT]',
                        description: 'YAYYAYAWOOHOOO YEEAAAAAAAAAYAYYAYAWOOHOOO YEEAAAAAAAAA'
                    }),
                    blockType: BlockType.REPORTER,
                    arguments: {
                        EFFECT: {
                            type: ArgumentType.STRING,
                            menu: 'effects',
                            defaultValue: "color"
                        }
                    }
                },
                "---"
            ],
            menus: {
                effects: EffectOptions,
                iframeClickable: {
                    acceptReporters: true,
                    items: [
                        'interactable',
                        'non-interactable'
                    ]
                }
            }
        };
    }
}

module.exports = JgIframeBlocks;
