const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class of 2023
 * @constructor
 */
class pmSensingExpansion {
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
            id: 'pmSensingExpansion',
            name: 'Sensing Expansion',
            color1: "#5CB1D6",
            color2: "#47A8D1",
            color3: "#2E8EB8",
            isDynamic: true,
            blocks: [
                {
                    opcode: 'batteryPercentage',
                    text: 'battery percentage',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true
                },
                {
                    opcode: 'batteryCharging',
                    text: 'is device charging?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true
                },
                {
                    opcode: 'vibrateDevice',
                    text: 'vibrate',
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'browserLanguage',
                    text: 'preferred language',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true
                },
                {
                    opcode: 'urlOptions',
                    text: 'url [OPTIONS]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        OPTIONS: {
                            type: ArgumentType.STRING,
                            menu: "urlSections"
                        }
                    }
                },
                {
                    opcode: 'urlOptionsOf',
                    text: '[OPTIONS] of url [URL]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        OPTIONS: {
                            type: ArgumentType.STRING,
                            menu: "urlSections"
                        },
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: "https://home.penguinmod.com:3000/some/random/page?param=10#20"
                        }
                    }
                },
                {
                    opcode: 'setUsername',
                    text: 'set username to [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "Penguin"
                        }
                    }
                },
                {
                    opcode: 'setUrlEnd',
                    text: 'set url path to [PATH]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        PATH: {
                            type: ArgumentType.STRING,
                            defaultValue: "?parameter=10#you-can-change-these-without-refreshing"
                        }
                    }
                },
                {
                    opcode: 'queryParamOfUrl',
                    text: 'query parameter [PARAM] of url [URL]',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        PARAM: {
                            type: ArgumentType.STRING,
                            defaultValue: "param"
                        },
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: "https://penguinmod.com/?param=10"
                        }
                    }
                },
                {
                    opcode: 'packaged',
                    text: 'project packaged?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true
                },
                {
                    opcode: 'spriteName',
                    text: 'sprite name',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true
                },
                {
                    opcode: 'framed',
                    text: 'project in iframe?',
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true
                },
                {
                    opcode: 'currentMillisecond',
                    text: 'current millisecond',
                    blockType: BlockType.REPORTER,
                    disableMonitor: false
                },
                {
                    opcode: 'deltaTime',
                    text: 'delta time',
                    blockType: BlockType.REPORTER,
                    disableMonitor: false
                },
                {
                    opcode: 'pickColor',
                    text: 'grab color at x: [X] y: [Y]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'maxSpriteLayers',
                    text: 'max sprite layers',
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'averageLoudness',
                    text: 'average loudness',
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'scrollingDistance',
                    text: 'scrolling distance',
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'setScrollingDistance',
                    text: 'set scrolling distance to [AMOUNT]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        AMOUNT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'changeScrollingDistanceBy',
                    text: 'change scrolling distance by [AMOUNT]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        AMOUNT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        }
                    }
                },
                {
                    opcode: 'currentKeyPressed',
                    text: 'current key pressed',
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getLastKeyPressed',
                    text: Scratch.translate({
                        id: 'tw.blocks.lastKeyPressed',
                        default: 'last key pressed',
                        description: 'Block that returns the last key that was pressed'
                    }),
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'getButtonIsDown',
                    text: Scratch.translate({
                        id: 'tw.blocks.buttonIsDown',
                        default: '[MOUSE_BUTTON] mouse button down?',
                        description: 'Block that returns whether a specific mouse button is down'
                    }),
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        MOUSE_BUTTON: {
                            type: ArgumentType.NUMBER,
                            menu: 'mouseButton',
                            defaultValue: '0'
                        }
                    }
                },
                {
                    opcode: 'changed',
                    blockType: BlockType.BOOLEAN,
                    text: '[ONE] changed?',
                    arguments: {
                        ONE: {
                            type: null,
                            // Will be interpreted like the input of the "switch" block, no text just an optional block
                        },
                    },
                },
                {
                    opcode: 'sensing_thing_has_number',
                    ppm_final_opcode: true,
                    blockType: BlockType.BOOLEAN,
                    text: '[TEXT1] has number?',
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: "abc 10 def",
                        },
                    },
                },
                {
                    opcode: 'sensing_isUpperCase',
                    ppm_final_opcode: true,
                    blockType: BlockType.BOOLEAN,
                    text: 'is character [text] uppercase?',
                    arguments: {
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: "abc 10 def",
                        },
                    },
                },
                {
                    opcode: 'sensing_regextest',
                    ppm_final_opcode: true,
                    blockType: BlockType.BOOLEAN,
                    text: 'test regex [reg] [regrule] with text [text]',
                    arguments: {
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo bar",
                        },
                        reg: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                        },
                        regrule: {
                            type: ArgumentType.STRING,
                            defaultValue: "g",
                        },
                    },
                },
                {
                    opcode: 'amountOfTimeKeyHasBeenHeld',
                    text: 'seconds since holding [KEY]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            menu: "key",
                        },
                    },
                },
                {
                    opcode: 'sensing_getspritewithattrib',
                    ppm_final_opcode: true,
                    blockType: BlockType.REPORTER,
                    text: 'get sprite with [var] set to [val]',
                    arguments: {
                        var: {
                            type: ArgumentType.STRING,
                            defaultValue: "my variable",
                        },
                        val: {
                            type: ArgumentType.STRING,
                            defaultValue: "0",
                        },
                    },
                },
                {
                    opcode: 'sensing_getoperatingsystem',
                    ppm_final_opcode: true,
                    blockType: BlockType.REPORTER,
                    text: 'operating system',
                },
                {
                    opcode: 'sensing_getbrowser',
                    ppm_final_opcode: true,
                    blockType: BlockType.REPORTER,
                    text: 'browser',
                },
                {
                    opcode: 'sensing_geturl',
                    ppm_final_opcode: true,
                    blockType: BlockType.REPORTER,
                    text: 'url',
                },
            ],
            menus: {
                key: {
                    items: [
                        "space", "up arrow", "down arrow", "right arrow", "left arrow", 
                        "enter", "any", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
                        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", 
                        "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                        "-", ",", ".", "`", "=", "[", "]", "\\", ";", "'", "/", "!", "@", 
                        "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "{", "}", "|", 
                        ":", '"', "?", "<", ">", "~", "backspace", "delete", "shift", 
                        "caps lock", "scroll lock", "control", "escape", "insert", 
                        "home", "end", "page up", "page down",
                    ],
                    acceptReporters: true,
                },
                mouseButton: {
                    items: [
                        {
                            text: Scratch.translate({
                                id: 'tw.blocks.mouseButton.primary',
                                default: '(0) primary',
                                description: 'Dropdown item to select primary (usually left) mouse button'
                            }),
                            value: '0'
                        },
                        {
                            text: Scratch.translate({
                                id: 'tw.blocks.mouseButton.middle',
                                default: '(1) middle',
                                description: 'Dropdown item to select middle mouse button'
                            }),
                            value: '1'
                        },
                        {
                            text: Scratch.translate({
                                id: 'tw.blocks.mouseButton.secondary',
                                default: '(2) secondary',
                                description: 'Dropdown item to select secondary (usually right) mouse button'
                            }),
                            value: '2'
                        },
                    ],
                    acceptReporters: true
                },
                urlSections: {
                    acceptReporters: true,
                    items: [
                        "protocol",
                        "host",
                        "hostname",
                        "port",
                        "pathname",
                        "search",
                        "hash",
                        "origin",
                        "subdomain",
                        "path"
                    ].map(item => ({ text: item, value: item }))
                }
            }
        };
    }
}

module.exports = pmSensingExpansion;
