const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const blockIconURI = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAAFACAMAAAD6TlWYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAPUExURQAAAP+xNQDiGgCU/wAAAJEQGGoAAAAFdFJOU/////8A+7YOUwAAAAlwSFlzAAAOwwAADsMBx2+oZAAABA5JREFUeF7t0EtuW0EUA9F8vP81Z8JRAwzbLuk5COoMBb1LdP34EGJAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEHos4M+HZfbtDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0KPBfxfGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEZsBfh/z8z/r9SfnsywwIGRAyIGRAyICQASEDQp8OeMrfvk06vEzOXjPgIWevGfCQs9cMeMjZawY85Ow1Ax5y9poBDzl7zYCHnL2GA57y2dvlvW+TmcmARWYmAxaZmQxYZGYyYJGZyYBFZiYDFpmZDFhkZnp5wFPOvFze+TaZmQxYZGYyYJGZyYBFZiYDFpmZDFhkZjJgkZnJgEVmprcHPOXsl+V9j8lsZcAhs5UBh8xWBhwyWxlwyGxlwCGzlQGHzFYGHDJbPR7wlJlreddjMlsZcMhsZcAhs5UBh8xWBhwyWxlwyGxlwCGzlQGHzFbfHvCU2SrvekxmKwMOma0MOGS2MuCQ2cqAQ2YrAw6ZrQw4ZLYy4JDZyoBDZisDDpmtDDhktjLgkNnKgENmKwMOma0MOGS2MuCQ2erbA2bmWt71mMxWBhwyWxlwyGxlwCGzlQGHzFYGHDJbGXDIbGXAIbPV4wFz9svyrsdktjLgkNnKgENmKwMOma0MOGS2MuCQ2cqAQ2YrAw6Zrd4eMGdeLu97m8xMBiwyMxmwyMxkwCIzkwGLzEwGLDIzGbDIzGTAIjPTywPms7fLO98mM5MBi8xMBiwyMxmwyMxkwCIzkwGLzEwGLDIzGbDIzIQD5m/fJu99mZy9ZsBDzl4z4CFnrxnwkLPXDHjI2WsGPOTsNQMecvaaAQ85e+3TAfPzPysdruWzLzMgZEDIgJABIQNCBoQMCM2A+jsDQgaEDAgZEDIgZEDIgJABIQNCBoQMCBkQMiBkQMiAkAEhA0IGhAwIGRAyIGRAyICQASEDQgaEDAgZEDIgZEDIgMjHxx+IPExM0h8siAAAAABJRU5ErkJggg=="

/**
 * Class for Unite blocks
 * @constructor
 */
class jwUnite {
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
            id: 'jwUnite',
            name: 'Unite',
            blockIconURI: blockIconURI,
            color1: '#7ddcff',
            color2: '#4a98ff',
            blocks: [
                {
                    opcode: 'always',
                    text: formatMessage({
                        id: 'jwUnite.blocks.always',
                        default: 'always',
                        description: 'Runs the code every tick'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.EVENT
                },
                {
                    opcode: 'whenanything',
                    text: formatMessage({
                        id: 'jwUnite.blocks.whenanything',
                        default: 'when [ANYTHING]',
                        description: 'Runs blocks when set boolean is true'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.HAT,
                    arguments: {
                        ANYTHING: {
                            type: ArgumentType.BOOLEAN,
                        }
                    }
                },
                "---",
                {
                    opcode: 'getspritewithattrib',
                    text: formatMessage({
                        id: 'jwUnite.blocks.getspritewithattrib',
                        default: 'get sprite with [var] set to [val]',
                        description: 'Reports the first sprite with a variable set to a value'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        var: {
                            type: ArgumentType.STRING,
                            defaultValue: "my variable"
                        },
                        val: {
                            type: ArgumentType.STRING,
                            defaultValue: "0"
                        }
                    }
                },
                "---",
                {
                    opcode: 'backToGreenFlag',
                    text: formatMessage({
                        id: 'jwUnite.blocks.backToGreenFlag',
                        default: 'run [FLAG]',
                        description: 'Acts like a click on the flag has been done.'
                    }),
                    terminal: true,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        FLAG: {
                            type: ArgumentType.IMAGE,
                            dataURI: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAACJ0lEQVRIid2Uy09TQRSHv2kv1VR5hhQQqwlYGtqCmtbHokhDTNQtEVz4B/gfmBCDXoyGmLj3kbBwY2LY6MpHWJDUoBukKsTKQ6I2paWGBipCo73jBii30BpI78ZfMpkzMznznTOPAwZLbFgt/ZWY011k9gzysSdZLICStdJXkPRjSns41hcH2Y7EjmAVmESKFyjyCaPqr50AzBtWbeAsEKDE0oy7w4rnfAXNbWU0nlY40CQwmX0kY73UBr4QGw5vu5vndg31Zy6wv3OGhecZfQbrajk3Rp2zXRdCqe0Irg5o8k8w+uwWR9VLmE13eaeNgarRqtoQ4jKKdpUy+wLy+3Hg2vaAQlIsbk51ZUjNJ/n8egBv5CBan2Bf5TL1nlkafGkWYz8YeVy94bIjwHpOpTY/vs7Nc1WAHQCNr5sXTLsA/EOaNBagabph8QEyYzAA3QkZkYGeUOAVyTlWUt/I/M5gLa/GpDjYXFryuumPaCsgMWsl+ilEfLoOSQTBClBBuW2GExcXsVi9hQFSF8RWQGT8MNCLwzXAYHc2nNabbQzdu4/TH6ThpBMhbDmef1iKhRgf8iHFo/wAeEpIfUgoZ/bD9SAB1Us42MPUiJOaxhBVh5YwKYKfib3MhZtYXS5B0sl79VUhQH4Nq6vADbzqHaJTbUQn3QjKECKOlG8Iqblh7apUsFayX661gjLgH/zPgPm1PlFMQPaSHa4HTIcnSFW8LSbAcP0F3uGqEimnx6MAAAAASUVORK5CYII=',
                            alt: 'Blue Flag'
                        }
                    }
                },
                "---",
                {
                    opcode: 'trueBoolean',
                    text: formatMessage({
                        id: 'jwUnite.blocks.trueBoolean',
                        default: 'true',
                        description: 'Returns true'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                },
                {
                    opcode: 'falseBoolean',
                    text: formatMessage({
                        id: 'jwUnite.blocks.falseBoolean',
                        default: 'false',
                        description: 'Returns false'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                },
                {
                    opcode: 'randomBoolean',
                    text: formatMessage({
                        id: 'jwUnite.blocks.randomBoolean',
                        default: 'random',
                        description: 'Returns true or false'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                },
                "---",
                {
                    opcode: 'mobile',
                    text: formatMessage({
                        id: 'jwUnite.blocks.mobile',
                        default: 'mobile?',
                        description: 'Returns true if the project is running on a mobile device'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                },
                "---",
                {
                    opcode: 'thing_is_text',
                    text: formatMessage({
                        id: 'jwUnite.blocks.thing_is_text',
                        default: '[TEXT1] is text?',
                        description: 'Checks if something is text!'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.thing_is_text_whatToCheck',
                                default: 'world',
                                description: 'What to check.'
                            })
                        }
                    }
                },
                {
                    opcode: 'thing_is_number',
                    text: formatMessage({
                        id: 'jwUnite.blocks.thing_is_number',
                        default: '[TEXT1] is number?',
                        description: 'Checks if something is a number!'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.thing_is_number_whatToCheck',
                                default: '10',
                                description: 'What to check.'
                            })
                        }
                    }
                },
                {
                    opcode: 'if_return_else_return',
                    text: formatMessage({
                        id: 'jwUnite.blocks.if_return_else_return',
                        default: 'if [boolean] is true [TEXT1] is false [TEXT2]',
                        description: 'Returns a value based on wether or not the boolean is true or false'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        boolean: {
                            type: ArgumentType.BOOLEAN
                        },
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.if_return_else_return_ifValue',
                                default: 'foo',
                                description: 'What to return if the boolean is true.'
                            })
                        },
                        TEXT2: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.if_return_else_return_elseValue',
                                default: 'bar',
                                description: 'What to return if the boolean is false.'
                            })
                        }
                    }
                },
                {
                    opcode: 'indexOfTextInText',
                    text: formatMessage({
                        id: 'jwUnite.blocks.indexOfTextInText',
                        default: 'index of [TEXT1] in [TEXT2]',
                        description: 'Finds the position of some text in another piece of text.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.indexof_textToFind',
                                default: 'world',
                                description: 'The text to look for.'
                            })
                        },
                        TEXT2: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.indexof_textToSearch',
                                default: 'Hello world!',
                                description: 'The text to search in.'
                            })
                        }
                    }
                },
                {
                    opcode: 'regextest',
                    text: formatMessage({
                        id: 'jwUnite.blocks.regextest',
                        default: 'test [text] with regex [reg]',
                        description: 'tests a string to see if its valid for this regex'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.regextest_text',
                                default: 'foo bar',
                                description: 'the text to test'
                            })
                        },
                        reg: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.regextest_regex',
                                default: '/foo/g',
                                description: 'the regex to test the text with'
                            })
                        }
                    }
                },
                {
                    opcode: 'regexmatch',
                    text: formatMessage({
                        id: 'jwUnite.blocks.regexmatch',
                        default: 'match [text] with regex [reg]',
                        description: 'gets all regex matxhes on a string'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.regexmatch_text',
                                default: 'foo bar',
                                description: 'the text to test'
                            })
                        },
                        reg: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.regexmatch_regex',
                                default: '/foo/g',
                                description: 'the regex to test the text with'
                            })
                        }
                    }
                },
                {
                    opcode: 'replaceAll',
                    text: formatMessage({
                        id: 'jwUnite.blocks.replaceAll',
                        default: 'in [text] replace all [term] with [res]',
                        description: 'replaces all of somthing with something in a string'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        text: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.replaceAll_text',
                                default: 'foo bar',
                                description: 'the text to test'
                            })
                        },
                        term: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.replaceAll_replacy',
                                default: 'foo',
                                description: 'what text to replace'
                            })
                        },
                        res: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.replaceAll_replacer',
                                default: 'bar',
                                description: 'the text to replace with'
                            })
                        }
                    }
                },
                {
                    opcode: 'getLettersFromIndexToIndexInText',
                    text: formatMessage({
                        id: 'jwUnite.blocks.getLettersFromIndexToIndexInText',
                        default: 'letters from [INDEX1] to [INDEX2] in [TEXT]',
                        description: 'Gets a part of text using the indexes specified.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        INDEX1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        },
                        INDEX2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 3
                        },
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.getLettersFromIndexToIndexInText_text',
                                default: 'Hello!',
                                description: 'The text to get a substring from.'
                            })
                        }
                    }
                },
                {
                    opcode: 'readLineInMultilineText',
                    text: formatMessage({
                        id: 'jwUnite.blocks.readLineInMultilineText',
                        default: 'read line [LINE] in [TEXT]',
                        description: 'Reads a certain line in text with multiple lines.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        LINE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: formatMessage({
                                id: 'jwUnite.readLineInMultilineText_text',
                                default: 'Text with multiple lines here',
                                description: 'The text to read lines from.'
                            })
                        }
                    }
                },
                {
                    opcode: 'newLine',
                    text: formatMessage({
                        id: 'jwUnite.blocks.newLine',
                        default: 'newline',
                        description: 'Represents a new line character.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
                {
                    opcode: 'stringify',
                    text: formatMessage({
                        id: 'jwUnite.blocks.stringify',
                        default: '[ONE] as string',
                        description: 'Represents a new line character.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo"
                        }
                }},
                {
                    opcode: 'lerpFunc',
                    text: formatMessage({
                        id: 'jwUnite.blocks.lerpFunc',
                        default: 'interpolate [ONE] to [TWO] by [AMOUNT]',
                        description: 'Linearly interpolates the first number to the second by the amount.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        TWO: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 3
                        },
                        AMOUNT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.5
                        }
                    }
                },
                {
                    opcode: 'advMath',
                    text: formatMessage({
                        id: 'jwUnite.blocks.advMath',
                        default: '[ONE] [OPTION] [TWO]',
                        description: 'Operators advanced math function but with 2 variables'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ONE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        },
                        OPTION: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "^",
                            menu: 'advMath'
                        },
                        TWO: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 2
                        }
                    }
                },
                {
                    opcode: 'constrainnumber',
                    text: formatMessage({
                        id: 'jwUnite.blocks.constrainnumber',
                        default: 'constrain [inp] min [min] max [max]',
                        description: 'Constrains a number to a specified minimum and maximum'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        inp: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 50
                        },
                        min: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1,
                        },
                        max: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        }
                    }
                },
                "---",
                {
                    opcode: 'setReplacer',
                    text: formatMessage({
                        id: 'jwUnite.blocks.setReplacer',
                        default: 'replacer [REPLACER] to [VALUE]',
                        description: 'Sets a replacer to a value'
                    }),
                    arguments: {
                        REPLACER: {
                            type: ArgumentType.STRING,
                            defaultValue: "foo",
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "bar"
                        },
                    },
                    disableMonitor: true,
                    blockType: BlockType.COMMAND,
                },
                {
                    opcode: 'replaceWithReplacers',
                    text: formatMessage({
                        id: 'jwUnite.blocks.replaceWithReplacers',
                        default: 'replace [STRING] with replacers',
                        description: 'Replaces all replacer names with their respective value'
                    }),
                    
                    arguments: {
                        STRING: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello {foo}!"
                        },
                    },
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                },
            ],
            menus: {
                advMath: [
                    '^',
                    'root',
                    'log'
                ]/*
                sprites: {
                    items: 'getAllSprites',
                    acceptReporters: true
                }
                */
            }
        };
    }
}

module.exports = jwUnite;
