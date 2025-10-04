const formatMessage = require('format-message');
const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0MCA0MCI+PHN0eWxlPi5zdDJ7ZmlsbDpyZWR9LnN0M3tmaWxsOiNlMGUwZTB9LnN0NHtmaWxsOm5vbmU7c3Ryb2tlOiM2NjY7c3Ryb2tlLXdpZHRoOi41O3N0cm9rZS1taXRlcmxpbWl0OjEwfTwvc3R5bGU+PHBhdGggZD0iTTM1IDI4SDVhMSAxIDAgMCAxLTEtMVYxMmMwLS42LjQtMSAxLTFoMzBjLjUgMCAxIC40IDEgMXYxNWMwIC41LS41IDEtMSAxeiIgZmlsbD0iI2ZmZiIgaWQ9IkxheWVyXzYiLz48ZyBpZD0iTGF5ZXJfNCI+PHBhdGggY2xhc3M9InN0MiIgZD0iTTQgMjVoMzJ2Mi43SDR6TTEzIDI0aC0yLjJhMSAxIDAgMCAxLTEtMXYtOS43YzAtLjYuNC0xIDEtMUgxM2MuNiAwIDEgLjQgMSAxVjIzYzAgLjYtLjUgMS0xIDF6Ii8+PHBhdGggY2xhc3M9InN0MiIgZD0iTTYuMSAxOS4zdi0yLjJjMC0uNS40LTEgMS0xaDkuN2MuNSAwIDEgLjUgMSAxdjIuMmMwIC41LS41IDEtMSAxSDcuMWExIDEgMCAwIDEtMS0xeiIvPjxjaXJjbGUgY2xhc3M9InN0MiIgY3g9IjIyLjgiIGN5PSIxOC4yIiByPSIzLjQiLz48Y2lyY2xlIGNsYXNzPSJzdDIiIGN4PSIzMC42IiBjeT0iMTguMiIgcj0iMy40Ii8+PHBhdGggY2xhc3M9InN0MiIgZD0iTTQuMiAyN2gzMS45di43SDQuMnoiLz48L2c+PGcgaWQ9IkxheWVyXzUiPjxjaXJjbGUgY2xhc3M9InN0MyIgY3g9IjIyLjgiIGN5PSIxOC4yIiByPSIyLjMiLz48Y2lyY2xlIGNsYXNzPSJzdDMiIGN4PSIzMC42IiBjeT0iMTguMiIgcj0iMi4zIi8+PHBhdGggY2xhc3M9InN0MyIgZD0iTTEyLjUgMjIuOWgtMS4yYy0uMyAwLS41LS4yLS41LS41VjE0YzAtLjMuMi0uNS41LS41aDEuMmMuMyAwIC41LjIuNS41djguNGMwIC4zLS4yLjUtLjUuNXoiLz48cGF0aCBjbGFzcz0ic3QzIiBkPSJNNy4yIDE4Ljd2LTEuMmMwLS4zLjItLjUuNS0uNWg4LjRjLjMgMCAuNS4yLjUuNXYxLjJjMCAuMy0uMi41LS41LjVINy43Yy0uMyAwLS41LS4yLS41LS41ek00IDI2aDMydjJINHoiLz48L2c+PGcgaWQ9IkxheWVyXzMiPjxwYXRoIGNsYXNzPSJzdDQiIGQ9Ik0zNS4yIDI3LjlINC44YTEgMSAwIDAgMS0xLTFWMTIuMWMwLS42LjUtMSAxLTFoMzAuNWMuNSAwIDEgLjQgMSAxVjI3YTEgMSAwIDAgMS0xLjEuOXoiLz48cGF0aCBjbGFzcz0ic3Q0IiBkPSJNMzUuMiAyNy45SDQuOGExIDEgMCAwIDEtMS0xVjEyLjFjMC0uNi41LTEgMS0xaDMwLjVjLjUgMCAxIC40IDEgMVYyN2ExIDEgMCAwIDEtMS4xLjl6Ii8+PC9nPjwvc3ZnPg==';

/**
 * An id for the space key on a keyboard.
 */
const KEY_ID_SPACE = 'SPACE';

/**
 * An id for the left arrow key on a keyboard.
 */
const KEY_ID_LEFT = 'LEFT';

/**
 * An id for the right arrow key on a keyboard.
 */
const KEY_ID_RIGHT = 'RIGHT';

/**
 * An id for the up arrow key on a keyboard.
 */
const KEY_ID_UP = 'UP';

/**
 * An id for the down arrow key on a keyboard.
 */
const KEY_ID_DOWN = 'DOWN';

/**
 * Class for the makey makey blocks in Scratch 3.0
 * @constructor
 */
class Scratch3MakeyMakeyBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /*
    * Localized short-form names of the space bar and arrow keys, for use in the
    * displayed menu items of the "when keys pressed in order" block.
    * @type {object}
    */
    get KEY_TEXT_SHORT () {
        return {
            [KEY_ID_SPACE]: formatMessage({
                id: 'makeymakey.spaceKey',
                default: 'space',
                description: 'The space key on a computer keyboard.'
            }),
            [KEY_ID_LEFT]: formatMessage({
                id: 'makeymakey.leftArrowShort',
                default: 'left',
                description: 'Short name for the left arrow key on a computer keyboard.'
            }),
            [KEY_ID_UP]: formatMessage({
                id: 'makeymakey.upArrowShort',
                default: 'up',
                description: 'Short name for the up arrow key on a computer keyboard.'
            }),
            [KEY_ID_RIGHT]: formatMessage({
                id: 'makeymakey.rightArrowShort',
                default: 'right',
                description: 'Short name for the right arrow key on a computer keyboard.'
            }),
            [KEY_ID_DOWN]: formatMessage({
                id: 'makeymakey.downArrowShort',
                default: 'down',
                description: 'Short name for the down arrow key on a computer keyboard.'
            })
        };
    }

    /*
     * An array of strings of KEY_IDs representing the default set of
     * key sequences for use by the "when keys pressed in order" block.
     * @type {array}
     */
    get DEFAULT_SEQUENCES () {
        return [
            `${KEY_ID_LEFT} ${KEY_ID_UP} ${KEY_ID_RIGHT}`,
            `${KEY_ID_RIGHT} ${KEY_ID_UP} ${KEY_ID_LEFT}`,
            `${KEY_ID_LEFT} ${KEY_ID_RIGHT}`,
            `${KEY_ID_RIGHT} ${KEY_ID_LEFT}`,
            `${KEY_ID_UP} ${KEY_ID_DOWN}`,
            `${KEY_ID_DOWN} ${KEY_ID_UP}`,
            `${KEY_ID_UP} ${KEY_ID_RIGHT} ${KEY_ID_DOWN} ${KEY_ID_LEFT}`,
            `${KEY_ID_UP} ${KEY_ID_LEFT} ${KEY_ID_DOWN} ${KEY_ID_RIGHT}`,
            `${KEY_ID_UP} ${KEY_ID_UP} ${KEY_ID_DOWN} ${KEY_ID_DOWN} ` +
                `${KEY_ID_LEFT} ${KEY_ID_RIGHT} ${KEY_ID_LEFT} ${KEY_ID_RIGHT}`
        ];
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'makeymakey',
            name: 'Makey Makey',
            blockIconURI: blockIconURI,
            blocks: [
                {
                    opcode: 'whenMakeyKeyPressed',
                    text: formatMessage({
                        id: 'makeymakey.whenKeyPressed',
                        default: 'when [KEY] key pressed',
                        description: 'when a keyboard key is pressed'
                    }),
                    blockType: BlockType.HAT,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            menu: 'KEY',
                            defaultValue: KEY_ID_SPACE
                        }
                    }
                },
                {
                    opcode: 'whenCodePressed',
                    text: formatMessage({
                        id: 'makeymakey.whenKeysPressedInOrder',
                        default: 'when [SEQUENCE] pressed in order',
                        description: 'when a sequence of keyboard keys is pressed in a specific order'
                    }),
                    blockType: BlockType.HAT,
                    arguments: {
                        SEQUENCE: {
                            type: ArgumentType.STRING,
                            menu: 'SEQUENCE',
                            defaultValue: this.DEFAULT_SEQUENCES[0]
                        }
                    }
                },
                "---",
                {
                    opcode: 'isMakeyKeyPressed',
                    text: formatMessage({
                        id: 'makeymakey.isKeyPressed',
                        default: 'is [KEY] key pressed',
                        description: 'is a keyboard key is pressed'
                    }),
                    blockType: BlockType.BOOLEAN,
                    arguments: {
                        KEY: {
                            type: ArgumentType.STRING,
                            menu: 'KEY',
                            defaultValue: KEY_ID_SPACE
                        }
                    }
                }
            ],
            menus: {
                KEY: {
                    acceptReporters: true,
                    items: [
                        {
                            text: formatMessage({
                                id: 'makeymakey.spaceKey',
                                default: 'space',
                                description: 'The space key on a computer keyboard.'
                            }),
                            value: KEY_ID_SPACE
                        },
                        {
                            text: formatMessage({
                                id: 'makeymakey.upArrow',
                                default: 'up arrow',
                                description: 'The up arrow key on a computer keyboard.'
                            }),
                            value: KEY_ID_UP
                        },
                        {
                            text: formatMessage({
                                id: 'makeymakey.downArrow',
                                default: 'down arrow',
                                description: 'The down arrow key on a computer keyboard.'
                            }),
                            value: KEY_ID_DOWN
                        },
                        {
                            text: formatMessage({
                                id: 'makeymakey.rightArrow',
                                default: 'right arrow',
                                description: 'The right arrow key on a computer keyboard.'
                            }),
                            value: KEY_ID_RIGHT
                        },
                        {
                            text: formatMessage({
                                id: 'makeymakey.leftArrow',
                                default: 'left arrow',
                                description: 'The left arrow key on a computer keyboard.'
                            }),
                            value: KEY_ID_LEFT
                        },
                        {text: 'w', value: 'w'},
                        {text: 'a', value: 'a'},
                        {text: 's', value: 's'},
                        {text: 'd', value: 'd'},
                        {text: 'f', value: 'f'},
                        {text: 'g', value: 'g'}
                    ]
                },
                SEQUENCE: {
                    acceptReporters: true,
                    items: this.buildSequenceMenu(this.DEFAULT_SEQUENCES)
                }
            }
        };
    }

    /*
     * Build the menu of key sequences.
     * @param {array} sequencesArray an array of strings of KEY_IDs.
     * @returns {array} an array of objects with text and value properties.
     */
    buildSequenceMenu (sequencesArray) {
        return sequencesArray.map(
            str => this.getMenuItemForSequenceString(str)
        );
    }

    /*
     * Create a menu item for a sequence string.
     * @param {string} sequenceString a string of KEY_IDs.
     * @return {object} an object with text and value properties.
     */
    getMenuItemForSequenceString (sequenceString) {
        let sequenceArray = sequenceString.split(' ');
        sequenceArray = sequenceArray.map(str => this.KEY_TEXT_SHORT[str]);
        return {
            text: sequenceArray.join(' '),
            value: sequenceString
        };
    }
}
module.exports = Scratch3MakeyMakeyBlocks;
