const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');
/**
 * Class for perlin noise extension.
 * @constructor
 */

// noise generation code from p5.js

class iygPerlin {
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
            id: 'iygPerlin',
            name: 'Perlin Noise',
            color1: '#525252',
            color2: '#636363',
            blocks: [
                // Hidden
                {
                    opcode: 'GetNoise',
                    blockType: BlockType.REPORTER,
                    text: formatMessage({
                        id: 'iygPerlin.GetNoise',
                        default: 'Get perlin noise with seed [SEED] and octave [OCTAVE] at x [X], y [Y], and z [Z]',
                        description: 'Get seeded perlin noise at a specified x and y and z.'
                    }),
                    arguments: {
                        SEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        },
                        OCTAVE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 4
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Z: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    },
                    hideFromPalette: true
                },
                // Hidden
                {
                    opcode: 'GetRandomNoise',
                    blockType: BlockType.REPORTER,
                    text: formatMessage({
                        id: 'iygPerlin.GetRandomNoise',
                        default: 'Get noise with seed [SEED] at x [X], y [Y], and z [Z]',
                        description: 'Get seeded noise with a specified seed at a specified x and y and z.'
                    }),
                    arguments: {
                        SEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Z: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    },
                    hideFromPalette: true
                },
                // Hidden
                {
                    opcode: 'GeneratePerlinNoise',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'iygPerlin.GeneratePerlinNoise',
                        default: 'Pre-generate perlin noise with seed [SEED] and octave [OCTAVE]',
                        description: 'Pre-generate seeded perlin noise.'
                    }),
                    arguments: {
                        SEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        },
                        OCTAVE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 4
                        }
                    },
                    hideFromPalette: true
                },
                // Hidden
                {
                    opcode: 'GenerateRandomNoise',
                    blockType: BlockType.COMMAND,
                    hideFromPalette: true,
                    text: formatMessage({
                        id: 'iygPerlin.GenerateRandomNoise',
                        default: 'not needed [SEED] [SIZE]',
                        description: 'Pre-generate seeded noise.'
                    }),
                    arguments: {
                        SEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        },
                        SIZE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 50
                        }
                    },
                },
                // Hidden
                {
                    opcode: 'getSimplexNoise',
                    blockType: BlockType.REPORTER,
                    hideFromPalette: true,
                    text: formatMessage({
                        id: 'iygPerlin.getSimplexNoise',
                        default: 'Get simplex noise with seed [SEED] at x [X], y [Y], and z [Z]',
                        description: 'Get simplex noise with a specified seed at a specified x and y and z.'
                    }),
                    arguments: {
                        SEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Z: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },

                // End of hidden stuff

                {
                    opcode: 'GetNoiseV2',
                    blockType: BlockType.REPORTER,
                    text: formatMessage({
                        id: 'iygPerlin.GetNoiseV2',
                        default: 'Get perlin noise with seed [SEED] and octave [OCTAVE] at x [X], y [Y], and z [Z]',
                        description: 'Get seeded perlin noise at a specified x and y and z.'
                    }),
                    arguments: {
                        SEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        },
                        OCTAVE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 4
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Z: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    },
                },
                {
                    opcode: 'GetRandomNoiseV2',
                    blockType: BlockType.REPORTER,
                    text: formatMessage({
                        id: 'iygPerlin.GetRandomNoiseV2',
                        default: 'Get random noise with seed [SEED] at x [X], y [Y], and z [Z]',
                        description: 'Get seeded random noise with a specified seed at a specified x and y and z.'
                    }),
                    arguments: {
                        SEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        },
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        },
                        Z: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0
                        }
                    }
                },
                {
                    opcode: 'GeneratePerlinNoiseV2',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'iygPerlin.GeneratePerlinNoiseV2',
                        default: 'Pre-generate perlin noise with seed [SEED] and octave [OCTAVE]',
                        description: 'Pre-generate seeded perlin noise.'
                    }),
                    arguments: {
                        SEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 123
                        },
                        OCTAVE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 4
                        }
                    }
                },
            ]
        };
    }
}

module.exports = iygPerlin;
