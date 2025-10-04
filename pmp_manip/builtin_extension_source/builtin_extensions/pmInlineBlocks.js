/**
 * Class of 2024
 * @constructor
 */
class pmInlineBlocks {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for deez nuts
     * this extension really only exists to seperate the block
     */
    getInfo() {
        return {
            id: 'pmInlineBlocks',
            name: 'Inline Blocks',
            color1: '#FFAB19',
            color2: '#EC9C13',
            color3: '#CF8B17',
            isDynamic: true,
            blocks: [
                {
                    opcode: "control_inline_stack_output",
                    ppm_final_opcode: true,
                    text: "inline block",
                    branchCount: 1,
                    blockType: Scratch.BlockType.REPORTER, // Technically unknown but behaves like REPORTER+SQUARE
                    blockShape: Scratch.BlockShape.SQUARE,
                    disableMonitor: true,
                },
            ],
        };
    }
}

module.exports = pmInlineBlocks;
