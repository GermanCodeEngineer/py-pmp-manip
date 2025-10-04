const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const noopSwitch = { isNoop: true };

/**
 * Class for Runtime blocks
 * @constructor
 */
class JgRuntimeBlocks {
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
            id: 'jgRuntime',
            name: 'Runtime',
            color1: '#777777',
            color2: '#6a6a6a',
            blocks: [
                {
                    opcode: 'addSpriteUrl',
                    text: 'add sprite from [URL]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: `https://corsproxy.io/?${encodeURIComponent('https://penguinmod.com/Sprite1.pms')}`
                        }
                    },
                    switches: [
                        noopSwitch,
                        'addCostumeUrl',
                        'addCostumeUrlForceMime',
                        'addSoundUrl',
                        'loadProjectDataUrl',
                    ],
                    switchText: 'add sprite from url'
                },
                {
                    opcode: 'addCostumeUrl',
                    text: 'add costume [name] from [URL]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: `https://corsproxy.io/?${encodeURIComponent('https://penguinmod.com/navicon.png')}`
                        },
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: 'penguinmod'
                        }
                    },
                    switches: [
                        'addSpriteUrl',
                        noopSwitch,
                        'addCostumeUrlForceMime',
                        {
                            opcode: 'addSoundUrl',
                            remapArguments: {
                                name: 'NAME'
                            }
                        },
                        'loadProjectDataUrl',
                    ],
                    switchText: 'add costume from url'
                },
                {
                    opcode: 'addCostumeUrlForceMime',
                    text: 'add [costtype] costume [name] from [URL]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        costtype: {
                            type: ArgumentType.STRING,
                            menu: "costumeMimeType"
                        },
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: `https://corsproxy.io/?${encodeURIComponent('https://penguinmod.com/navicon.png')}`
                        },
                        name: {
                            type: ArgumentType.STRING,
                            defaultValue: 'penguinmod'
                        }
                    },
                    switches: [
                        'addSpriteUrl',
                        'addCostumeUrl',
                        noopSwitch,
                        {
                            opcode: 'addSoundUrl',
                            remapArguments: {
                                name: 'NAME'
                            }
                        },
                        'loadProjectDataUrl',
                    ],
                    switchText: 'add typed costume from url'
                },
                {
                    opcode: 'addSoundUrl',
                    text: 'add sound [NAME] from [URL]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: 'https://extensions.turbowarp.org/meow.mp3'
                        },
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Meow'
                        }
                    },
                    switches: [
                        'addSpriteUrl',
                        {
                            opcode: 'addCostumeUrl',
                            remapArguments: {
                                NAME: 'name'
                            }
                        },
                        {
                            opcode: 'addCostumeUrlForceMime',
                            remapArguments: {
                                NAME: 'name'
                            }
                        },
                        noopSwitch,
                        'loadProjectDataUrl',
                    ],
                    switchText: 'add sound from url'
                },
                {
                    opcode: 'loadProjectDataUrl',
                    text: 'load project from [URL]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: ''
                        }
                    },
                    switches: [
                        'addSpriteUrl',
                        'addCostumeUrl',
                        'addCostumeUrlForceMime',
                        'addSoundUrl',
                        noopSwitch
                    ],
                    switchText: 'load project from url'
                },
                {
                    opcode: 'getIndexOfCostume',
                    text: 'get costume index of [costume]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        costume: {
                            type: ArgumentType.STRING,
                            defaultValue: "costume1"
                        }
                    },
                    switches: [
                        noopSwitch,
                        {
                            opcode: 'getIndexOfSound',
                            remapArguments: {
                                costume: 'NAME'
                            }
                        },
                    ],
                    switchText: 'get costume index'
                },
                {
                    opcode: 'getIndexOfSound',
                    text: 'get sound index of [NAME]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "Pop"
                        }
                    },
                    switches: [
                        {
                            opcode: 'getIndexOfCostume',
                            remapArguments: {
                                NAME: 'costume'
                            }
                        },
                        noopSwitch
                    ],
                    switchText: 'get sound index of'
                },
                {
                    opcode: 'getProjectDataUrl',
                    text: 'get data url of project',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true
                },
                '---',
                {
                    opcode: 'setStageSize',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.setStageSize',
                        default: 'set stage width: [WIDTH] height: [HEIGHT]',
                        description: 'Sets the width and height of the stage.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        WIDTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 480
                        },
                        HEIGHT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 360
                        }
                    }
                },
                {
                    opcode: 'getStageWidth',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.getStageWidth',
                        default: 'stage width',
                        description: 'Block that returns the width of the stage.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        noopSwitch,
                        'getStageHeight',
                    ],
                    switchText: 'get stage width'
                },
                {
                    opcode: 'getStageHeight',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.getStageHeight',
                        default: 'stage height',
                        description: 'Block that returns the height of the stage.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        'getStageWidth',
                        noopSwitch
                    ],
                    switchText: 'get stage height'
                },
                '---',
                {
                    opcode: 'updateRuntimeConfig',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.updateRuntimeConfig',
                        default: 'set [OPTION] to [ENABLED]',
                        description: 'Block that enables or disables configuration on the runtime like high quality pen or turbo mode.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        OPTION: {
                            menu: 'runtimeConfig'
                        },
                        ENABLED: {
                            menu: 'onoff'
                        }
                    }
                },
                {
                    opcode: 'changeRenderingCapping',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.changeRenderingCapping',
                        default: 'change render setting [OPTION] to [CAPPED]',
                        description: 'Block that updates configuration on the renderer like resolution for certain content.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        OPTION: {
                            menu: 'renderConfigCappable'
                        },
                        CAPPED: {
                            menu: 'cappableSettings'
                        }
                    }
                },
                {
                    opcode: 'setRenderingNumber',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.setRenderingNumber',
                        default: 'set render setting [OPTION] to [NUM]',
                        description: 'Block that sets configuration on the renderer like resolution for certain content.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        OPTION: {
                            menu: 'renderConfigNumber'
                        },
                        NUM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'runtimeConfigEnabled',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.runtimeConfigEnabled',
                        default: '[OPTION] enabled?',
                        description: 'Block that returns whether a runtime option like Turbo Mode is enabled on the project or not.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        OPTION: {
                            menu: 'runtimeConfig'
                        }
                    }
                },
                {
                    opcode: 'turboModeEnabled',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.turboModeEnabled',
                        default: 'turbo mode enabled?',
                        description: 'Block that returns whether Turbo Mode is enabled on the project or not.'
                    }),
                    disableMonitor: false,
                    hideFromPalette: true,
                    blockType: BlockType.BOOLEAN
                },
                '---',
                {
                    opcode: 'setMaxClones',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.setMaxClones',
                        default: 'set max clones to [MAX]',
                        description: 'Block that enables or disables configuration on the runtime like high quality pen or turbo mode.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.COMMAND,
                    arguments: {
                        MAX: {
                            menu: 'cloneLimit',
                            defaultValue: 300
                        }
                    }
                },
                {
                    opcode: 'maxAmountOfClones',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.maxAmountOfClones',
                        default: 'max clone count',
                        description: 'Block that returns the maximum amount of clones that may exist.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        noopSwitch,
                        'amountOfClones',
                        'getIsClone'
                    ],
                    switchText: 'max clone count'
                },
                {
                    opcode: 'amountOfClones',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.amountOfClones',
                        default: 'clone count',
                        description: 'Block that returns the amount of clones that currently exist.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        'maxAmountOfClones',
                        noopSwitch,
                        'getIsClone'
                    ],
                    switchText: 'clone count'
                },
                {
                    opcode: 'getIsClone',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.getIsClone',
                        default: 'is clone?',
                        description: 'Block that returns whether the sprite is a clone or not.'
                    }),
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                    switches: [
                        'maxAmountOfClones',
                        'amountOfClones',
                        noopSwitch
                    ],
                    switchText: 'is clone?'
                },
                '---',
                {
                    opcode: 'setMaxFrameRate',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.setMaxFrameRate',
                        default: 'set max framerate to: [FRAMERATE]',
                        description: 'Sets the max allowed framerate.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        FRAMERATE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 30
                        }
                    },
                },
                {
                    opcode: 'getMaxFrameRate',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.getMaxFrameRate',
                        default: 'max framerate',
                        description: 'Block that returns the amount of FPS allowed.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        noopSwitch,
                        'getFrameRate',
                    ],
                    switchText: 'max framerate'
                },
                {
                    opcode: 'getFrameRate',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.getFrameRate',
                        default: 'framerate',
                        description: 'Block that returns the amount of FPS.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        'getMaxFrameRate',
                        noopSwitch
                    ],
                    switchText: 'framerate'
                },
                '---',
                {
                    opcode: 'setBackgroundColor',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.setBackgroundColor',
                        default: 'set stage background color to [COLOR]',
                        description: 'Sets the background color of the stage.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR
                        }
                    }
                },
                {
                    opcode: 'getBackgroundColor',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.getBackgroundColor',
                        default: 'stage background color',
                        description: 'Block that returns the stage background color in HEX.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER
                },
                "---",
                {
                    opcode: "pauseScript",
                    blockType: BlockType.COMMAND,
                    text: "pause this script using name: [NAME]",
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "my script",
                        },
                    },
                    switches: [
                        'pauseScript',
                        'unpauseScript',
                    ],
                    switchText: 'pause this script',
                },
                {
                    opcode: "unpauseScript",
                    blockType: BlockType.COMMAND,
                    text: "unpause script named: [NAME]",
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "my script",
                        },
                    },
                    switches: [
                        'pauseScript',
                        noopSwitch,
                    ],
                    switchText: 'unpause script named'
                },
                {
                    opcode: "isScriptPaused",
                    blockType: BlockType.BOOLEAN,
                    text: "is script named [NAME] paused?",
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "my script",
                        },
                    }
                },
                "---",
                {
                    opcode: 'variables_createVariable',
                    text: 'create variable named [NAME] for [SCOPE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "my variable" },
                        SCOPE: { type: ArgumentType.STRING, menu: "variableScope" }
                    },
                    switches: [
                        noopSwitch,
                        'variables_createCloudVariable',
                        'variables_createList'
                    ],
                    switchText: 'create variable'
                },
                {
                    opcode: 'variables_createCloudVariable',
                    text: 'create cloud variable named [NAME]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "cloud variable" },
                    },
                    switches: [
                        'variables_createVariable',
                        noopSwitch,
                        'variables_createList'
                    ],
                    switchText: 'create cloud variable'
                },
                {
                    opcode: 'variables_createList',
                    text: 'create list named [NAME] for [SCOPE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "list" },
                        SCOPE: { type: ArgumentType.STRING, menu: "variableScope" }
                    },
                    switches: [
                        'variables_createVariable',
                        'variables_createCloudVariable',
                        noopSwitch
                    ],
                    switchText: 'create list'
                },
                {
                    opcode: 'variables_getVariable',
                    text: 'get value of variable named [NAME] in [SCOPE]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "my variable" },
                        SCOPE: { type: ArgumentType.STRING, menu: "variableTypes" }
                    },
                    switches: [
                        noopSwitch,
                        {
                            opcode: 'variables_getList',
                            remapMenus: {
                                SCOPE: {
                                    'all sprites': 'for all sprites',
                                    'this sprite':  'in this sprite',
                                    'cloud':    'for all sprites',
                                }
                            }
                        },
                        'variables_existsVariable',
                        'variables_existsList'
                    ],
                    switchText: 'value of variable in scope'
                },
                {
                    opcode: 'variables_getList',
                    text: 'get array of list named [NAME] in [SCOPE]',
                    disableMonitor: true,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "list" },
                        SCOPE: { type: ArgumentType.STRING, menu: "variableScope" }
                    },
                    switches: [
                        'variables_getVariable',
                        noopSwitch,
                        'variables_existsVariable',
                        'variables_existsList'
                    ],
                    switchText: 'value of list in scope'
                },
                {
                    opcode: 'variables_existsVariable',
                    text: 'variable named [NAME] exists in [SCOPE]?',
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "my variable" },
                        SCOPE: { type: ArgumentType.STRING, menu: "variableTypes" }
                    },
                    switches: [
                        'variables_getVariable',
                        'variables_getList',
                        noopSwitch,
                        'variables_existsList'
                    ],
                    switchText: 'variable exists in scope'
                },
                {
                    opcode: 'variables_existsList',
                    text: 'list named [NAME] exists in [SCOPE]?',
                    disableMonitor: true,
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "list" },
                        SCOPE: { type: ArgumentType.STRING, menu: "variableScope" }
                    },
                    switches: [
                        'variables_getVariable',
                        'variables_getList',
                        'variables_existsVariable',
                        noopSwitch
                    ],
                    switchText: 'list exists in scope'

                },
                "---",
                {
                    opcode: 'getDataOption',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.getDataOption',
                        default: 'get binary data of [OPTION] named [NAME]',
                        description: 'Block that returns the binary data of a sprite, sound or costume.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        OPTION: {
                            type: ArgumentType.STRING,
                            menu: "objectType"
                        },
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "Sprite1"
                        }
                    },
                    switches: [
                        noopSwitch,
                        'getDataUriOption',
                    ],
                    switchText: 'get binary data of option'
                },
                {
                    opcode: 'getDataUriOption',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.getDataUriOption',
                        default: 'get data uri of [OPTION] named [NAME]',
                        description: 'Block that returns the data URI of a sprite, sound or costume.'
                    }),
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        OPTION: {
                            type: ArgumentType.STRING,
                            menu: "objectType"
                        },
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "Sprite1"
                        }
                    },
                    switches: [
                        'getDataOption',
                        noopSwitch
                    ],
                    switchText: 'get data uri of option'
                },
                "---",
                {
                    opcode: 'getAllSprites',
                    text: 'get all sprites',
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        noopSwitch,
                        'getAllCostumes',
                        'getAllSounds',
                        'getAllFonts',
                    ]
                },
                {
                    opcode: 'getAllCostumes',
                    text: 'get all costumes',
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        'getAllSprites',
                        noopSwitch,
                        'getAllSounds',
                        'getAllFonts',
                    ]
                },
                {
                    opcode: 'getAllSounds',
                    text: 'get all sounds',
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        'getAllSprites',
                        'getAllCostumes',
                        noopSwitch,
                        'getAllFonts',
                    ]
                },
                {
                    opcode: 'getAllFonts',
                    text: 'get all fonts',
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    switches: [
                        'getAllSprites',
                        'getAllCostumes',
                        'getAllSounds',
                        noopSwitch,
                    ]
                },
                "---",
                {
                    opcode: 'getAllVariables',
                    text: 'get all variables [ALLSCOPE]',
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ALLSCOPE: {
                            type: ArgumentType.STRING,
                            menu: "allVariableType"
                        }
                    },
                    switches: [
                        noopSwitch,
                        {
                            opcode: 'getAllLists',
                            remapMenus: {
                                ALLSCOPE: {
                                    'for all sprites': 'for all sprites',
                                    'in every sprite': 'in every sprite',
                                    'in this sprite':  'in this sprite',
                                    'in the cloud':    'for all sprites',
                                }
                            }
                        }
                    ],
                    switchText: 'get all variables'
                },
                {
                    opcode: 'getAllLists',
                    text: 'get all lists [ALLSCOPE]',
                    disableMonitor: false,
                    blockType: BlockType.REPORTER,
                    arguments: {
                        ALLSCOPE: {
                            type: ArgumentType.STRING,
                            menu: "allVariableScope"
                        }
                    },
                    switches: [
                        'getAllVariables',
                        noopSwitch,
                    ],
                    switchText: 'get all lists',
                },
                "---",
                {
                    blockType: BlockType.LABEL,
                    text: "Potentially Dangerous"
                },
                {
                    opcode: 'deleteCostume',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.deleteCostume',
                        default: 'delete costume at index [COSTUME]',
                        description: 'Deletes a costume at the specified index.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        COSTUME: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    switches: [
                        noopSwitch,
                        {
                            opcode: 'deleteSound',
                            remapArguments: {
                                COSTUME: 'SOUND'
                            }
                        },
                        {
                            opcode: 'deleteSprite',
                            remapArguments: {
                                COSTUME: 'NAME'
                            }
                        },
                    ],
                    switchText: 'delete costume at index'
                },
                {
                    opcode: 'deleteSound',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.deleteSound',
                        default: 'delete sound at index [SOUND]',
                        description: 'Deletes a sound at the specified index.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        SOUND: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    switches: [
                        {
                            opcode: 'deleteCostume',
                            remapArguments: {
                                SOUND: 'COSTUME'
                            }
                        },
                        noopSwitch,
                        {
                            opcode: 'deleteSprite',
                            remapArguments: {
                                SOUND: 'NAME'
                            }
                        },
                    ],
                    switchText: 'delete sound at index'
                },
                "---",
                {
                    opcode: 'variables_deleteVariable',
                    text: 'delete variable named [NAME] in [SCOPE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "my variable" },
                        SCOPE: { type: ArgumentType.STRING, menu: "variableTypes" }
                    },
                    switches: [
                        noopSwitch,
                        {
                            opcode: 'variables_deleteList',
                            remapMenus: {
                                SCOPE: {
                                    'all sprites': 'all sprites',
                                    'this sprite': 'this sprite',
                                    'cloud': 'all sprites'
                                }
                            }
                        }
                    ],
                    switchText: 'delete variable'
                },
                {
                    opcode: 'variables_deleteList',
                    text: 'delete list named [NAME] in [SCOPE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "list" },
                        SCOPE: { type: ArgumentType.STRING, menu: "variableScope" }
                    },
                    switches: [
                        'variables_deleteVariable',
                        noopSwitch
                    ],
                    switchText: 'delete list'
                },
                "---",
                {
                    opcode: 'deleteSprite',
                    text: formatMessage({
                        id: 'jgRuntime.blocks.deleteSprite',
                        default: 'delete sprite named [NAME]',
                        description: 'Deletes a sprite with the specified name.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "Sprite1"
                        }
                    },
                    switches: [
                        {
                            opcode: 'deleteCostume',
                            remapArguments: {
                                NAME: 'COSTUME'
                            }
                        },
                        {
                            opcode: 'deleteSound',
                            remapArguments: {
                                NAME: 'SOUND'
                            }
                        },
                        noopSwitch,
                    ],
                    switchText: 'delete sprite named'
                },
            ],
            menus: {
                objectType: {
                    acceptReporters: true,
                    items: [
                        "sprite", "costume", "sound"
                    ].map(item => ({ text: item, value: item }))
                },
                variableScope: {
                    acceptReporters: true,
                    items: [
                        "all sprites", "this sprite"
                    ].map(item => ({ text: item, value: item }))
                },
                allVariableScope: {
                    acceptReporters: true,
                    items: [
                        "for all sprites", "in every sprite", "in this sprite"
                    ].map(item => ({ text: item, value: item }))
                },
                allVariableType: {
                    acceptReporters: true,
                    items: [
                        "for all sprites", "in every sprite",
                        "in this sprite", "in the cloud"
                    ].map(item => ({ text: item, value: item }))
                },
                variableTypes: {
                    acceptReporters: true,
                    items: [
                        "all sprites", "this sprite", "cloud"
                    ].map(item => ({ text: item, value: item }))
                },
                cloneLimit: {
                    items: [
                        '100', '128', '300', '500',
                        '1000', '1024', '5000',
                        '10000', '16384', 'Infinity'
                    ],
                    isTypeable: true,
                    isNumeric: true
                },
                runtimeConfig: {
                    acceptReporters: true,
                    items: [
                        "turbo mode",
                        "high quality pen",
                        "offscreen sprites",
                        "remove miscellaneous limits",
                        "disable offscreen rendering",
                        "disable direction clamping",
                        "interpolation",
                        "warp timer"
                    ]
                },
                renderConfigCappable: {
                    acceptReporters: true,
                    items: ["animated text resolution"]
                },
                renderConfigNumber: {
                    acceptReporters: true,
                    items: ["animated text resolution"]
                },
                onoff: ["on", "off"],
                costumeMimeType: ["png", "bmp", "jpg", "jpeg", "jfif", "webp", "gif", "vector"],
                cappableSettings: ["uncapped", "capped", "fixed"]
            }
        };
    }
}

module.exports = JgRuntimeBlocks;
