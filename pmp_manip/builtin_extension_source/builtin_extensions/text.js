const formatMessage = require('format-message');
const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj48cGF0aCBkPSJNMjcuODM0IDlhMyAzIDAgMDEyLjU0NiAxLjQxMmwuMDk3LjE2Ny4wNTQuMTEuMDUyLjExMi4wNDguMTEyIDYuMjIyIDE2YTMuMDAxIDMuMDAxIDAgMDEtMi4yNyA0LjA0MWwtLjE4LjAyNS0uMTE1LjAxMS0uMTE2LjAwNy0uMTE1LjAwM2gtMS44NTVhMyAzIDAgMDEtMi41NDUtMS40MTJsLS4wOTYtLjE2Ny0uMTA3LS4yMjItLjA0OC0uMTExTDI4Ljk4MyAyOGgtNC45M2wtLjQyMiAxLjA4N2EzLjAwMyAzLjAwMyAwIDAxLTIuNDEgMS44ODlsLS4xOTMuMDE4LS4xOTQuMDA2LTEuOTQtLjAwMi0uMDk2LjAwMkg3YTMgMyAwIDAxLTIuODctMy44NzJsLjA3Mi0uMjA5IDYuMTgzLTE2YTMuMDAxIDMuMDAxIDAgMDEyLjYwNC0xLjkxM0wxMy4xODQgOWwzLjkuMDAxLjA5OS0uMDAxIDMuOTI0LjAwMi4wOTUtLjAwMiAzLjkwNS4wMDIuMDk1LS4wMDJoMi42MzJ6IiBmaWxsLW9wYWNpdHk9Ii4xNSIgZmlsbD0iIzAwMCIvPjxwYXRoIGQ9Ik0yNS42NjMgMjFsLjgxNi0yLjA5OS44MTYgMi4wOTloLTEuNjMyem0xMC4yNTggNi4yNzVsLTYuMjIzLTE2LS4wNzUtLjE2OC0uMDg1LS4xNDVjLS4zODctLjYxMS0xLjAxOS0uOTYyLTEuNzAzLS45NjJoLTIuNjMzbC0uMDk2LjAwMi0uMDYyLS4wMDFMMjEuMjAyIDEwbC0uMDk2LjAwMi0uMDYyLS4wMDFMMTcuMTgzIDEwbC0uMDg2LjAwMkwxMy4xODQgMTBsLS4xNjUuMDA3YTIuMDAzIDIuMDAzIDAgMDAtMS43MDIgMS4yNzJsLTYuMTgyIDE2LS4wNTkuMTc1QTIgMiAwIDAwNyAzMGgxMS43OThsLjA4OC0uMDAyIDEuOTQ5LjAwMi4xNjMtLjAwNy4xNjEtLjAxOWEyIDIgMCAwMDEuNTM5LTEuMjQ5bC42Ny0xLjcyNWg2LjI5OWwuNjcyIDEuNzI2LjA3NC4xNjcuMDg2LjE0NWMuMzg3LjYxMSAxLjAxOC45NjIgMS43MDMuOTYyaDEuODU1bC4xNzQtLjAwOS4xNjQtLjAyNGMuOTc2LS4xODcgMS42NjItMS4wMDMgMS42NjItMS45NjcgMC0uMjQ4LS4wNDYtLjQ5NC0uMTM2LS43MjV6IiBmaWxsLW9wYWNpdHk9Ii4yNSIgZmlsbD0iIzAwMCIvPjxwYXRoIGQ9Ik0xMy4xODMgMTFoMy44MThhMSAxIDAgMDEuOTQxIDEuMzM4bC01Ljc0MiAxNmExIDEgMCAwMS0uOTQuNjYySDdhMSAxIDAgMDEtLjkzMy0xLjM2bDYuMTgzLTE2YTEgMSAwIDAxLjkzMy0uNjR6IiBmaWxsPSIjNEM5N0ZGIi8+PHBhdGggZD0iTTE3LjE4MyAxMUgyMWExIDEgMCAwMS45NDIgMS4zMzhsLTUuNzQyIDE2YTEgMSAwIDAxLS45NDEuNjYyaC00LjI2YTEgMSAwIDAxLS45MzItMS4zNmw2LjE4My0xNmExIDEgMCAwMS45MzMtLjY0eiIgZmlsbD0iI0NGNjNDRiIvPjxwYXRoIGQ9Ik0yMS4yMDIgMTFIMjVhMSAxIDAgMDEuOTMzIDEuMzYxbC02LjIwMyAxNmExIDEgMCAwMS0uOTMyLjYzOUgxNWExIDEgMCAwMS0uOTMzLTEuMzYxbDYuMjAzLTE2YTEgMSAwIDAxLjkzMi0uNjM5eiIgZmlsbD0iI0ZGQkYwMCIvPjxwYXRoIGQ9Ik0yNy44MzQgMTFhMSAxIDAgMDEuOTMyLjYzOGw2LjIyMiAxNkExIDEgMCAwMTM0LjA1NiAyOWgtMS44NTRhMSAxIDAgMDEtLjkzMi0uNjM4TDMwLjM1MSAyNmgtNy42NjZsLS45MTkgMi4zNjJhMSAxIDAgMDEtLjkzMi42MzhIMTguOThhMSAxIDAgMDEtLjkzMi0xLjM2Mmw2LjIyMi0xNmExIDEgMCAwMS45MzItLjYzOHptLTEuMzE2IDUuMTQzTDI0LjI0IDIyaDQuNTU2bC0yLjI3OC01Ljg1N3oiIGZpbGw9IiNGRkYiLz48L2c+PC9zdmc+';
const menuIconURI = blockIconURI;
const DefaultText = 'Welcome to my project!';
const DefaultAnimateText = 'Here we go!';
const SANS_SERIF_ID = 'Sans Serif';
const SERIF_ID = 'Serif';
const HANDWRITING_ID = 'Handwriting';
const MARKER_ID = 'Marker';
const CURLY_ID = 'Curly';
const PIXEL_ID = 'Pixel';

/* PenguinMod Fonts */
const PLAYFUL_ID = 'Playful';
const BUBBLY_ID = 'Bubbly';
const BITSANDBYTES_ID = 'Bits and Bytes';
const TECHNOLOGICAL_ID = 'Technological';
const ARCADE_ID = 'Arcade';
const ARCHIVO_ID = 'Archivo';
const ARCHIVOBLACK_ID = 'Archivo Black';
const SCRATCH_ID = 'Scratch';

const RANDOM_ID = 'Random';

class Scratch3TextBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    get FONT_IDS () {
        return [SANS_SERIF_ID, SERIF_ID, HANDWRITING_ID, MARKER_ID, CURLY_ID, PIXEL_ID, PLAYFUL_ID, BUBBLY_ID, ARCADE_ID, BITSANDBYTES_ID, TECHNOLOGICAL_ID, SCRATCH_ID, ARCHIVO_ID, ARCHIVOBLACK_ID];
    }

    getInfo () {
        return {
            id: 'text',
            name: 'Animated Text',
            blockIconURI: blockIconURI,
            menuIconURI: menuIconURI,
            color1: '#9966ff',
            color2: '#8a5ce6',
            color3: '#7a52cc',
            blocks: [{
                opcode: 'setText',
                text: formatMessage({
                    id: 'text.setText',
                    "default": 'show text [TEXT]',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    TEXT: {
                        type: ArgumentType.STRING,
                        defaultValue: DefaultText
                    }
                }
            }, {
                opcode: 'animateText',
                text: formatMessage({
                    id: 'text.animateText',
                    "default": '[ANIMATE] text [TEXT]',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    ANIMATE: {
                        type: ArgumentType.STRING,
                        menu: 'ANIMATE',
                        defaultValue: 'rainbow'
                    },
                    TEXT: {
                        type: ArgumentType.STRING,
                        defaultValue: DefaultAnimateText
                    }
                }
            }, {
                opcode: 'clearText',
                text: formatMessage({
                    id: 'text.clearText',
                    "default": 'show sprite',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {}
            }, '---', {
                opcode: 'setFont',
                text: formatMessage({
                    id: 'text.setFont',
                    "default": 'set font to [FONT]',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    FONT: {
                        type: ArgumentType.STRING,
                        menu: 'FONT',
                        defaultValue: 'Pixel'
                    }
                }
            }, {
                opcode: 'setColor',
                text: formatMessage({
                    id: 'text.setColor',
                    "default": 'set text color to [COLOR]',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    COLOR: {
                        type: ArgumentType.COLOR
                    }
                }
            }, {
                opcode: 'setWidth',
                text: formatMessage({
                    id: 'text.setWidth',
                    "default": 'set width to [WIDTH] aligned [ALIGN]',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    WIDTH: {
                        type: ArgumentType.NUMBER,
                        defaultValue: 200
                    },
                    ALIGN: {
                        type: ArgumentType.STRING,
                        defaultValue: 'left',
                        menu: 'ALIGN'
                    }
                }
            }, {
                opcode: 'rainbow',
                text: formatMessage({
                    id: 'text.rainbow',
                    default: 'rainbow for [SECS] seconds',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    SECS: {
                        type: ArgumentType.NUMBER,
                        defaultValue: 1
                    }
                }
            },
            '---',
            {
                opcode: 'addLine',
                text: formatMessage({
                    id: 'text.addLine',
                    default: 'add line [TEXT]',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    TEXT: {
                        type: ArgumentType.STRING,
                        defaultValue: 'more lines!'
                    }
                }
            },
            '---',
            {
                opcode: 'setOutlineWidth',
                text: formatMessage({
                    id: 'text.setOutlineWidth',
                    default: 'set outline width to [WIDTH]',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    WIDTH: {
                        type: ArgumentType.NUMBER,
                        defaultValue: 1
                    }
                }
            }, {
                opcode: 'setOutlineColor',
                text: formatMessage({
                    id: 'text.setOutlineColor',
                    default: 'set outline color to [COLOR]',
                    description: ''
                }),
                blockType: BlockType.COMMAND,
                arguments: {
                    COLOR: {
                        type: ArgumentType.COLOR
                    }
                }
            }, 
            '---',
            {
                opcode: 'getVisible',
                text: 'is text visible?',
                blockType: BlockType.BOOLEAN
            }, {
                opcode: 'getWidth',
                text: 'get width of the text',
                blockType: BlockType.REPORTER
            }, {
                opcode: 'getHeight',
                text: 'get height of the text',
                blockType: BlockType.REPORTER
            },
            {
                opcode: "getDisplayedText",
                blockType: BlockType.REPORTER,
                text: ("displayed text")
            },
            {
                opcode: "getRender",
                blockType: BlockType.REPORTER,
                text: ("get data uri of last rendered text")
            },

            // TODO: Give these blocks actual functionality.
            //       Most of them can be done easily.

            // TURBOWARP BLOCKS (added for compatibility reasons)
            // TURBOWARP BLOCKS (added for compatibility reasons)
            // TURBOWARP BLOCKS (added for compatibility reasons)
            // TURBOWARP BLOCKS (added for compatibility reasons)
            // TURBOWARP BLOCKS (added for compatibility reasons)
            // TURBOWARP BLOCKS (added for compatibility reasons)

            // TODO: Give these blocks actual functionality.
            //       Most of them can be done easily.

            {
                opcode: "setAlignment",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) align text to [ALIGN]"),
                hideFromPalette: true,
                arguments: {
                    ALIGN: {
                        type: ArgumentType.STRING,
                        menu: "twAlign"
                    }
                }
            },
            {
                // why is the other block called "setWidth" :(
                opcode: "setWidthValue",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) set width to [WIDTH]"),
                hideFromPalette: true,
                arguments: {
                    WIDTH: {
                        type: ArgumentType.NUMBER,
                        defaultValue: 200
                    }
                }
            },
            {
                opcode: "resetWidth",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) reset text width"),
                hideFromPalette: true
            },
            "---",
            {
                opcode: "getLines",
                blockType: BlockType.REPORTER,
                text: ("(NOT USABLE YET) # of lines"),
                hideFromPalette: true,
                disableMonitor: true
            },
            "---",
            {
                opcode: "startAnimate",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) start [ANIMATE] animation"),
                hideFromPalette: true,
                arguments: {
                    ANIMATE: {
                        type: ArgumentType.STRING,
                        menu: "twAnimate",
                        defaultValue: "rainbow"
                    }
                }
            },
            {
                opcode: "animateUntilDone",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) animate [ANIMATE] until done"),
                hideFromPalette: true,
                arguments: {
                    ANIMATE: {
                        type: ArgumentType.STRING,
                        menu: "twAnimate",
                        defaultValue: "rainbow"
                    }
                }
            },
            {
                opcode: "isAnimating",
                blockType: BlockType.BOOLEAN,
                text: ("(NOT USABLE YET) is animating?"),
                hideFromPalette: true,
                disableMonitor: true
            },
            "---",
            {
                opcode: "setAnimateDuration",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) set [ANIMATE] duration to [NUM] seconds"),
                hideFromPalette: true,
                arguments: {
                    ANIMATE: {
                        type: ArgumentType.STRING,
                        menu: "twAnimateDuration",
                        defaultValue: "rainbow"
                    },
                    NUM: {
                        type: ArgumentType.NUMBER,
                        defaultValue: 3
                    }
                }
            },
            {
                opcode: "resetAnimateDuration",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) reset [ANIMATE] duration"),
                hideFromPalette: true,
                arguments: {
                    ANIMATE: {
                        type: ArgumentType.STRING,
                        menu: "twAnimateDuration",
                        defaultValue: "rainbow"
                    }
                }
            },
            {
                opcode: "getAnimateDuration",
                blockType: BlockType.REPORTER,
                text: ("(NOT USABLE YET) [ANIMATE] duration"),
                hideFromPalette: true,
                arguments: {
                    ANIMATE: {
                        type: ArgumentType.STRING,
                        menu: "twAnimateDuration",
                        defaultValue: "rainbow"
                    }
                }
            },
            "---",
            {
                opcode: "setTypeDelay",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) set typing delay to [NUM] seconds"),
                hideFromPalette: true,
                arguments: {
                    NUM: {
                        type: ArgumentType.NUMBER,
                        defaultValue: 0.1
                    }
                }
            },
            {
                opcode: "resetTypeDelay",
                blockType: BlockType.COMMAND,
                text: ("(NOT USABLE YET) reset typing delay"),
                hideFromPalette: true
            },
            {
                opcode: "getTypeDelay",
                blockType: BlockType.REPORTER,
                text: ("(NOT USABLE YET) typing delay"),
                hideFromPalette: true,
                disableMonitor: true
            },
            "---",
            {
                opcode: "textActive",
                blockType: BlockType.BOOLEAN,
                text: ("(TURBOWARP BLOCK) is showing text?"),
                hideFromPalette: true,
                disableMonitor: true
            },
            {
                opcode: "getTextAttribute",
                blockType: BlockType.REPORTER,
                text: "(NOT USABLE YET) text [ATTRIBUTE]",
                arguments: {
                    ATTRIBUTE: {
                        type: ArgumentType.STRING,
                        menu: "twAnimate"
                    }
                },
                disableMonitor: true,
                hideFromPalette: true
            }
        
            ],
            menus: {
                FONT: {
                    items: [{
                        text: 'Sans Serif',
                        value: SANS_SERIF_ID
                    }, {
                        text: 'Serif',
                        value: SERIF_ID
                    }, {
                        text: 'Handwriting',
                        value: HANDWRITING_ID
                    }, {
                        text: 'Marker',
                        value: MARKER_ID
                    }, {
                        text: 'Curly',
                        value: CURLY_ID
                    }, {
                        text: 'Pixel',
                        value: PIXEL_ID
                    }, {
                        text: 'Playful',
                        value: PLAYFUL_ID
                    }, {
                        text: 'Bubbly',
                        value: BUBBLY_ID
                    }, {
                        text: 'Arcade',
                        value: ARCADE_ID
                    }, {
                        text: 'Bits and Bytes',
                        value: BITSANDBYTES_ID
                    }, {
                        text: 'Technological',
                        value: TECHNOLOGICAL_ID
                    }, {
                        text: 'Scratch',
                        value: SCRATCH_ID
                    }, {
                        text: 'Archivo',
                        value: ARCHIVO_ID
                    }, {
                        text: 'Archivo Black',
                        value: ARCHIVOBLACK_ID
                    },
                    {
                        text: 'random font',
                        value: RANDOM_ID
                    }],
                    isTypeable: true
                },
                ALIGN: {
                    items: [{
                        text: 'left',
                        value: 'left'
                    }, {
                        text: 'center',
                        value: 'center'
                    }, {
                        text: 'right',
                        value: 'right'
                    }]
                },
                ANIMATE: {
                    items: [{
                        text: 'type',
                        value: 'type'
                    }, {
                        text: 'rainbow',
                        value: 'rainbow'
                    }, {
                        text: 'zoom',
                        value: 'zoom'
                    }]
                },
                // TurboWarp menus (acceptReporters: true)
                twAnimate: {
                    acceptReporters: true,
                    items: [
                        {
                            text: ("type"),
                            value: "type"
                        },
                        {
                            text: ("rainbow"),
                            value: "rainbow"
                        },
                        {
                            text: ("zoom"),
                            value: "zoom"
                        }
                    ]
                },
                twAnimateDuration: {
                    acceptReporters: true,
                    items: [
                        {
                            text: ("rainbow"),
                            value: "rainbow"
                        },
                        {
                            text: ("zoom"),
                            value: "zoom"
                        }
                    ]
                },
                twAlign: {
                    acceptReporters: true,
                    items: [
                        {
                            text: ("left"),
                            value: "left"
                        },
                        {
                            text: ("center"),
                            value: "center"
                        },
                        {
                            text: ("right"),
                            value: "right"
                        }
                    ]
                }
            }
        };
    }
}

module.exports = Scratch3TextBlocks;
