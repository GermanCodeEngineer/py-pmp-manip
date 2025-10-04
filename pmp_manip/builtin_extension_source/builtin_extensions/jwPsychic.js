const BlockType = require('../../extension-support/block-type')
const ArgumentType = require('../../extension-support/argument-type')
const TargetType = require('../../extension-support/target-type')

let Vector = {
    Type: class {},
    Block: {},
    Argument: {}
}

let jwArray = {
    Type: class {},
    Block: {},
    Argument: {}
}

let Target = {
    Type: class {},
    Block: {},
    Argument: {}
}

class Extension {
    getInfo() {
        return {
            id: "jwPsychic",
            name: "Psychic",
            color1: "#b16bed",
            menuIconURI: "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMCAyMCIgeG1sbnM6Yng9Imh0dHBzOi8vYm94eS1zdmcuY29tIiB3aWR0aD0iMjBweCIgaGVpZ2h0PSIyMHB4Ij48ZGVmcz48Yng6ZXhwb3J0PjxieDpmaWxlIGZvcm1hdD0ic3ZnIi8+PC9ieDpleHBvcnQ+PC9kZWZzPjxlbGxpcHNlIHN0eWxlPSJzdHJva2Utd2lkdGg6IDJweDsgcGFpbnQtb3JkZXI6IHN0cm9rZTsgZmlsbDogcmdiKDE3NywgMTA3LCAyMzcpOyBzdHJva2U6IHJnYigxNTksIDk2LCAyMTMpOyIgY3g9IjEwIiBjeT0iMTAiIHJ4PSI5IiByeT0iOSIvPjxyZWN0IHg9IjQuNjM0IiB5PSIxMC4yMjgiIHdpZHRoPSI0Ljc3IiBoZWlnaHQ9IjQuNzciIHN0eWxlPSJmaWxsOiByZ2IoMjU1LCAyNTUsIDI1NSk7Ii8+PHJlY3QgeD0iMTAuNTk2IiB5PSIxMC4yMjgiIHdpZHRoPSI0Ljc3IiBoZWlnaHQ9IjQuNzciIHN0eWxlPSJmaWxsOiByZ2IoMjU1LCAyNTUsIDI1NSk7Ii8+PHJlY3QgeD0iNy42MTUiIHdpZHRoPSI0Ljc3IiBoZWlnaHQ9IjQuNzciIHN0eWxlPSJmaWxsOiByZ2IoMjU1LCAyNTUsIDI1NSk7IiB5PSI0LjI2NyIvPjwvc3ZnPg==",
            blocks: [
                {
                    opcode: 'tick',
                    text: 'tick',
                    blockType: BlockType.COMMAND
                },
                "---",
                {
                    opcode: 'boundaries',
                    text: 'set boundaries [OPTION]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        OPTION: {
                            type: ArgumentType.STRING,
                            menu: 'boundariesOption'
                        }
                    }
                },
                {
                    opcode: 'setGravity',
                    text: 'set gravity to [VECTOR]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VECTOR: Vector.Argument
                    }
                },
                {
                    opcode: 'getGravity',
                    text: 'gravity',
                    ...Vector.Block
                },
                "---",
                {
                    opcode: 'enablePhysics',
                    text: 'enable physics as [OPTION]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        OPTION: {
                            type: ArgumentType.STRING,
                            menu: 'enablePhysicsOption'
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'disablePhysics',
                    text: 'disable physics',
                    blockType: BlockType.COMMAND,
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'setPos',
                    text: 'set position to [VECTOR]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VECTOR: Vector.Argument
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getPos',
                    text: 'position',
                    filter: [TargetType.SPRITE],
                    ...Vector.Block
                },
                {
                    opcode: 'setVel',
                    text: 'set velocity to [VECTOR]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VECTOR: Vector.Argument
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getVel',
                    text: 'velocity',
                    filter: [TargetType.SPRITE],
                    ...Vector.Block
                },
                {
                    opcode: 'setRot',
                    text: 'set rotation to [ANGLE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ANGLE: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 90
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getRot',
                    text: 'rotation',
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'setAngVel',
                    text: 'set angular velocity to [ANGLE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ANGLE: {
                            type: ArgumentType.ANGLE,
                            defaultValue: 0
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getAngVel',
                    text: 'angular velocity',
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'getMass',
                    text: 'mass',
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'setDensity',
                    text: 'set density to [NUMBER]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NUMBER: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.001
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getDensity',
                    text: 'density',
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'setStatic',
                    text: 'set fixed to [BOOLEAN]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        BOOLEAN: {
                            type: ArgumentType.BOOLEAN
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getStatic',
                    text: 'fixed',
                    blockType: BlockType.BOOLEAN,
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'setRotatable',
                    text: 'set rotatable to [BOOLEAN]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        BOOLEAN: {
                            type: ArgumentType.BOOLEAN
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getRotatable',
                    text: 'rotatable',
                    blockType: BlockType.BOOLEAN,
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'setFric',
                    text: 'set friction to [NUMBER]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NUMBER: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.1
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getFric',
                    text: 'friction',
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'setAirFric',
                    text: 'set air resistance to [NUMBER]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NUMBER: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.01
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getAirFric',
                    text: 'air resistance',
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'setRest',
                    text: 'set restitution to [NUMBER]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        NUMBER: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {
                    opcode: 'getRest',
                    text: 'restitution',
                    blockType: BlockType.REPORTER,
                    filter: [TargetType.SPRITE]
                },
                "---",
                {
                    opcode: 'getCollides',
                    text: 'targets colliding with [OPTION]',
                    arguments: {
                        OPTION: {
                            type: ArgumentType.STRING,
                            menu: 'touchingOption'
                        }
                    },
                    filter: [TargetType.SPRITE],
                    ...jwArray.Block
                }
            ],
            menus: {
                enablePhysicsOption: [
                    'precise',
                    'box',
                    'circle'
                ],
                boundariesOption: [
                    'all',
                    'floor',
                    'none'
                ],
                touchingOption: [
                    'body',
                    'feet',
                    'head'
                ]
            }
        };
    }
}

module.exports = Extension