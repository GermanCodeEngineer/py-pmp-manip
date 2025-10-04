/* eslint-disable space-infix-ops */
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

// eslint-disable-next-line no-undef
const pathToMedia = 'static/blocks-media'; // ScratchBlocks.mainWorkspace.options.pathToMedia
const defaultState = 'default';

class PenguinModCamera {
    constructor(runtime) {
        this.runtime = runtime;
    }

    getInfo() {
        return {
            id: 'pmCamera',
            name: 'Camera',
            color1: '#0586FF',
            blocks: [
                {
                    opcode: 'moveSteps',
                    blockType: BlockType.COMMAND,
                    text: 'move camera [STEPS] steps',
                    arguments: {
                        STEPS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        }
                    }
                },
                {
                    opcode: 'turnRight',
                    blockType: BlockType.COMMAND,
                    text: 'turn camera [DIRECTION] [DEGREES] degrees',
                    arguments: {
                        DIRECTION: {
                            type: ArgumentType.IMAGE,
                            dataURI: `${pathToMedia}/rotate-right.svg`
                        },
                        DEGREES: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '15'
                        }
                    }
                },
                {
                    opcode: 'turnLeft',
                    blockType: BlockType.COMMAND,
                    text: 'turn camera [DIRECTION] [DEGREES] degrees',
                    arguments: {
                        DIRECTION: {
                            type: ArgumentType.IMAGE,
                            dataURI: `${pathToMedia}/rotate-left.svg`
                        },
                        DEGREES: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '15'
                        }
                    }
                },
                {
                    opcode: 'bindTarget',
                    blockType: BlockType.COMMAND,
                    text: 'bind [TARGET] to camera [SCREEN]',
                    arguments: {
                        TARGET: {
                            type: ArgumentType.STRING,
                            menu: 'BINDABLE_TARGETS'
                        },
                        SCREEN: {
                            type: ArgumentType.STRING,
                            defaultValue: defaultState
                        }
                    }
                },
                {
                    opcode: 'unbindTarget',
                    blockType: BlockType.COMMAND,
                    text: 'unbind [TARGET] from the camera',
                    arguments: {
                        TARGET: {
                            type: ArgumentType.STRING,
                            menu: 'BINDABLE_TARGETS'
                        }
                    }
                },
                {
                    opcode: 'setCurrentCamera',
                    blockType: BlockType.COMMAND,
                    text: 'set current camera to [SCREEN]',
                    arguments: {
                        SCREEN: {
                            type: ArgumentType.STRING,
                            defaultValue: defaultState
                        }
                    }
                },
                {
                    opcode: 'setRenderImediat',
                    blockType: BlockType.COMMAND,
                    text: 'set render mode to [RENDER_MODE]',
                    arguments: {
                        RENDER_MODE: {
                            type: ArgumentType.STRING,
                            menu: 'RENDER_MODES'
                        }
                    }
                },
                {
                    opcode: 'manualRender',
                    blockType: BlockType.COMMAND,
                    text: 'render camera'
                },
                '---',
                {
                    opcode: 'gotoXY',
                    blockType: BlockType.COMMAND,
                    text: 'set camera x: [X] y: [Y]',
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        }
                    }
                },
                {
                    opcode: 'setSize',
                    blockType: BlockType.COMMAND,
                    text: 'set camera zoom to [ZOOM]%',
                    arguments: {
                        ZOOM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '100'
                        }
                    }
                },
                {
                    opcode: 'changeSize',
                    blockType: BlockType.COMMAND,
                    text: 'change camera zoom by [ZOOM]%',
                    arguments: {
                        ZOOM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        }
                    }
                },
                '---',
                {
                    opcode: 'pointTowards',
                    blockType: BlockType.COMMAND,
                    text: 'point camera in direction [DIRECTION]',
                    arguments: {
                        DIRECTION: {
                            type: ArgumentType.ANGLE,
                            defaultValue: '90'
                        }
                    }
                },
                {
                    opcode: 'pointTowardsPoint',
                    blockType: BlockType.COMMAND,
                    text: 'point camera towards x: [X] y: [Y]',
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        }
                    }
                },
                '---',
                {
                    opcode: 'changeXpos',
                    blockType: BlockType.COMMAND,
                    text: 'change camera x by [X]',
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        }
                    }
                },
                {
                    opcode: 'setXpos',
                    blockType: BlockType.COMMAND,
                    text: 'set camera x to [X]',
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        }
                    }
                },
                {
                    opcode: 'changeYpos',
                    blockType: BlockType.COMMAND,
                    text: 'change camera y by [Y]',
                    arguments: {
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '10'
                        }
                    }
                },
                {
                    opcode: 'setYpos',
                    blockType: BlockType.COMMAND,
                    text: 'set camera y to [Y]',
                    arguments: {
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        }
                    }
                },
                '---',
                {
                    opcode: 'xPosition',
                    blockType: BlockType.REPORTER,
                    text: 'camera x'
                },
                {
                    opcode: 'yPosition',
                    blockType: BlockType.REPORTER,
                    text: 'camera y'
                },
                {
                    opcode: 'direction',
                    blockType: BlockType.REPORTER,
                    text: 'camera direction'
                },
                {
                    // theres also a property named "size" so this one is special
                    opcode: 'getSize',
                    blockType: BlockType.REPORTER,
                    text: 'camera zoom'
                },
                {
                    opcode: 'getCurrentCamera',
                    blockType: BlockType.REPORTER,
                    text: 'current camera'
                }
            ],
            menus: {
                BINDABLE_TARGETS: {
                    items: 'getBindableTargets',
                    acceptReports: true
                },
                RENDER_MODES: {
                    items: [
                        'immediate',
                        'manual'
                    ]
                }
            }
        };
    }
}

module.exports = PenguinModCamera;
