const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');
const formatMessage = require('format-message');

/**
 * Class for Pathfinding blocks
 * @constructor
 */
class JgPathfindingBlocks {
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
            id: 'jgPathfinding',
            name: 'Pathfinding',
            color1: '#5386E2',
            color2: '#4169B1',
            blocks: [
                {
                    opcode: 'createBlockadeAt',
                    text: formatMessage({
                        id: 'jgPathfinding.blocks.createBlockadeAt',
                        default: 'create blockade at x1: [X1] y1: [Y1] x2: [X2] y2: [Y2]',
                        description: "Block that creates a blockade in the pathfinding area."
                    }),
                    arguments: {
                        X1: { type: ArgumentType.NUMBER, defaultValue: -70 },
                        Y1: { type: ArgumentType.NUMBER, defaultValue: 20 },
                        X2: { type: ArgumentType.NUMBER, defaultValue: 70 },
                        Y2: { type: ArgumentType.NUMBER, defaultValue: -20 },
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'clearBlockades',
                    text: formatMessage({
                        id: 'jgPathfinding.blocks.clearBlockades',
                        default: 'clear blockades',
                        description: "Block that removes all blockades in the pathfinding area."
                    }),
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'setPatherXY',
                    text: formatMessage({
                        id: 'jgPathfinding.blocks.setPatherXY',
                        default: 'set pather starting x: [X] y: [Y]',
                        description: "Block that sets the starting position for the pather."
                    }),
                    arguments: {
                        X: { type: ArgumentType.NUMBER, defaultValue: 0 },
                        Y: { type: ArgumentType.NUMBER, defaultValue: 120 },
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'setWidthHeight',
                    text: formatMessage({
                        id: 'jgPathfinding.blocks.setWidthHeight',
                        default: 'set pather width: [WIDTH] height: [HEIGHT]',
                        description: "Block that sets the width and height of the path follower. This allows sprites to avoid clipping inside walls on the way to the destination."
                    }),
                    arguments: {
                        WIDTH: { type: ArgumentType.NUMBER, defaultValue: 55 },
                        HEIGHT: { type: ArgumentType.NUMBER, defaultValue: 95 },
                    },
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'pathToSpot',
                    text: formatMessage({
                        id: 'jgPathfinding.blocks.pathToSpot',
                        default: 'find path to x: [X] y: [Y] around blockades',
                        description: "Block that finds a path around blockades in the pathfinding area to get to a location."
                    }),
                    arguments: {
                        X: { type: ArgumentType.NUMBER, defaultValue: 60 },
                        Y: { type: ArgumentType.NUMBER, defaultValue: -60 },
                    },
                    blockType: BlockType.COMMAND
                },
                '---',
                {
                    opcode: 'setListToPath',
                    text: formatMessage({
                        id: 'jgPathfinding.blocks.setListToPath',
                        default: 'set [LIST] to current path',
                        description: "Block that sets a list to the current path."
                    }),
                    arguments: {
                        LIST: { type: ArgumentType.LIST },
                    },
                    hideFromPalette: true,
                    blockType: BlockType.COMMAND
                },
                {
                    opcode: 'getPathAs',
                    text: formatMessage({
                        id: 'jgPathfinding.blocks.getPathAs',
                        default: 'current path as [TYPE]',
                        description: "Block that returns the current path in a certain way."
                    }),
                    arguments: {
                        TYPE: { type: ArgumentType.STRING, menu: "pathReturnType" },
                    },
                    disableMonitor: true,
                    blockType: BlockType.REPORTER
                },
            ],
            menus: {
                // lists: "menuLists",
                pathReturnType: {
                    acceptReporters: true,
                    items: [
                        "json arrays",
                        "json array with objects",
                        "json object",
                        "comma seperated list",
                    ].map(item => ({ text: item, value: item }))
                }
            }
        };
    }
}

module.exports = JgPathfindingBlocks;
