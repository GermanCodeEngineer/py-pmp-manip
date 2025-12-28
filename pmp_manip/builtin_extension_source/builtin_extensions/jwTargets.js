const BlockType = require('../../extension-support/block-type')
const BlockShape = require('../../extension-support/block-shape')
const ArgumentType = require('../../extension-support/argument-type')

const Target = {
    Type: class {}, // not needed
    Block: {
        blockType: BlockType.REPORTER,
        blockShape: BlockShape.OCTAGONAL,
        forceOutputType: "Target",
        disableMonitor: true
    },
    Argument: {
        check: ["Target"],
        shape: BlockShape.OCTAGONAL
    }
}

let jwArray = {
    Type: class {},
    Block: {},
    Argument: {}
}

class Extension {
    getInfo() {
        return {
            id: "jwTargets",
            name: "Targets",
            color1: "#4254f5",
            menuIconURI: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMCAyMCIgeG1sbnM6Yng9Imh0dHBzOi8vYm94eS1zdmcuY29tIj4KICA8Y2lyY2xlIHN0eWxlPSJzdHJva2Utd2lkdGg6IDJweDsgcGFpbnQtb3JkZXI6IHN0cm9rZTsgZmlsbDogcmdiKDY2LCA4NCwgMjQ1KTsgc3Ryb2tlOiByZ2IoNDAsIDU1LCAxOTkpOyIgY3g9IjEwIiBjeT0iMTAiIHI9IjkiPjwvY2lyY2xlPgogIDxwYXRoIGQ9Ik0gMTAgMy4yMjIgQyA0Ljc4MyAzLjIyMiAxLjUyMyA4Ljg3IDQuMTMgMTMuMzg5IEMgNS4zNCAxNS40ODUgNy41OCAxNi43NzggMTAgMTYuNzc4IEMgMTUuMjE4IDE2Ljc3OCAxOC40OCAxMS4xMyAxNS44NjkgNi42MTEgQyAxNC42NjEgNC41MTUgMTIuNDIyIDMuMjIyIDEwIDMuMjIyIE0gMTAgNS40ODEgQyAxMy40NzkgNS40ODEgMTUuNjUzIDkuMjQ4IDEzLjkxMyAxMi4yNTkgQyAxMy4xMDYgMTMuNjU4IDExLjYxNiAxNC41MTkgMTAgMTQuNTE5IEMgNi41MjIgMTQuNTE5IDQuMzUgMTAuNzUyIDYuMDg3IDcuNzQxIEMgNi44OTUgNi4zNDIgOC4zODUgNS40ODEgMTAgNS40ODEgTSAxMCA3Ljc0MSBDIDguMjYyIDcuNzQxIDcuMTczIDkuNjIyIDguMDQ0IDExLjEzIEMgOC40NDggMTEuODI4IDkuMTkzIDEyLjI1OSAxMCAxMi4yNTkgQyAxMS43NCAxMi4yNTkgMTIuODI3IDEwLjM3OCAxMS45NTYgOC44NyBDIDExLjU1MyA4LjE3MiAxMC44MDggNy43NDEgMTAgNy43NDEiIGZpbGw9IiNmZmYiIHN0eWxlPSIiPjwvcGF0aD4KPC9zdmc+",
            blocks: [
                {
                    opcode: 'this',
                    text: 'this target',
                    hideFromPalette: true,
                    ...Target.Block
                },
                {
                    opcode: 'stage',
                    text: 'stage target',
                    hideFromPalette: true,
                    ...Target.Block
                },
                {
                    opcode: 'fromName',
                    text: '[SPRITE] target',
                    arguments: {
                        SPRITE: {
                            menu: "sprite"
                        }
                    },
                    ...Target.Block
                },
                {
                    opcode: 'cloneOrigin',
                    text: 'origin of [TARGET]',
                    arguments: {
                        TARGET: Target.Argument
                    },
                    ...Target.Block
                },
                '---',
                {
                    opcode: 'get',
                    text: '[TARGET] [MENU]',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        TARGET: Target.Argument,
                        MENU: {
                            menu: "targetProperty",
                            defaultValue: "name"
                        }
                    }
                },
                {
                    opcode: 'set',
                    text: 'set [TARGET] [MENU] to [VALUE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        TARGET: Target.Argument,
                        MENU: {
                            menu: "targetPropertySet",
                            defaultValue: "x"
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            exemptFromNormalization: true
                        }
                    }
                },
                '---',
                {
                    opcode: 'isClone',
                    text: 'is [TARGET] a clone',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        TARGET: Target.Argument
                    }
                },
                {
                    opcode: 'isTouching',
                    text: 'is [A] touching [B]',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        A: Target.Argument,
                        B: Target.Argument
                    }
                },
                {
                    opcode: 'isTouchingObject',
                    text: 'is [A] touching [B]',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        A: Target.Argument,
                        B: {
                            menu: "touchingObject"
                        },
                    }
                },
                '---',
                {
                    opcode: 'getVar',
                    text: 'var [NAME] of [TARGET]',
                    blockType: BlockType.REPORTER,
                    allowDropAnywhere: true,
                    arguments: {
                        TARGET: Target.Argument,
                        NAME: {
                            type: ArgumentType.STRING
                        }
                    }
                },
                {
                    opcode: 'setVar',
                    text: 'set var [NAME] of [TARGET] to [VALUE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        TARGET: Target.Argument,
                        NAME: {
                            type: ArgumentType.STRING
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            exemptFromNormalization: true
                        }
                    }
                },
                '---',
                {
                    opcode: 'clone',
                    text: 'create clone of [TARGET]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        TARGET: Target.Argument
                    }
                },
                {
                    opcode: 'cloneR',
                    text: 'create clone of [TARGET]',
                    arguments: {
                        TARGET: Target.Argument
                    },
                    ...Target.Block
                },
                {
                    opcode: 'deleteClone',
                    text: 'delete clone [TARGET]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        TARGET: Target.Argument
                    }
                },
                '---',
                {
                    opcode: 'all',
                    text: 'all targets',
                    ...jwArray.Block
                },
                {
                    opcode: 'touching',
                    text: 'targets touching [TARGET]',
                    arguments: {
                        TARGET: Target.Argument
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'clones',
                    text: 'clones of [TARGET]',
                    arguments: {
                        TARGET: Target.Argument
                    },
                    ...jwArray.Block
                },
                {
                    opcode: 'arrayHasTarget',
                    text: '[ARRAY] has clone of [TARGET]',
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        ARRAY: jwArray.Argument,
                        TARGET: Target.Argument
                    }
                },
                /*'---',
                {
                    opcode: 'whenStart',
                    text: 'when I start as a clone of [TARGET]',
                    blockType: BlockType.EVENT,
                    isEdgeActivated: false,
                    arguments: {
                        TARGET: Target.Argument
                    }
                },*/
                '---',
                {
                    blockType: BlockType.XML,
                    xml: `<block type="control_run_as_sprite" />`
                }
            ],
            menus: {
                sprite: {
                    acceptReporters: true,
                    items: 'getSpriteMenu'
                },
                targetProperty: {
                    acceptReporters: true,
                    items: [
                        "name",
                        "id",
                        "x",
                        "y",
                        "direction",
                        "size",
                        "stretch x",
                        "stretch y",
                        "costume #",
                        "costume name",
                        "visible",
                        "layer",
                        "volume"
                    ]
                },
                targetPropertySet: {
                    acceptReporters: true,
                    items: [
                        "x",
                        "y",
                        "direction",
                        "size",
                        "stretch x",
                        "stretch y",
                        "costume #",
                        "costume name",
                        "visible",
                        "layer",
                        "volume"
                    ]
                },
                touchingObject: [
                    { text: "mouse-pointer", value: "_mouse_" },
                    { text: "edge", value: "_edge_" }
                ]
            }
        };
    }
}

module.exports = Extension