const formatMessage = require('format-message');
const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for Structs
 * @constructor
 */

class jwStructs {
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
            id: 'jwStructs',
            name: 'Structs',
            color1: '#7ddcff',
            color2: '#4a98ff',
            blocks: [
                {
                    opcode: 'createClass',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.createClass',
                        default: 'Create class [NAME]',
                        description: 'Create a class'
                    }),
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'MyClass'
                        }
                    }
                },
                {
                    opcode: 'createClassProperty',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.createClassProperty',
                        default: 'Create class property [NAME] with value [VALUE] in class [CLASS]',
                        description: 'Create a class property'
                    }),
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myProperty'
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myValue'
                        },
                        CLASS: {
                            type: ArgumentType.STRING,
                            defaultValue: 'MyClass'
                        }
                    }
                },
                "---",
                {
                    opcode: 'newObject',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.newObject',
                        default: 'Create object [NAME] from class [CLASS]',
                        description: 'Create a new object'
                    }),
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myObject'
                        },
                        CLASS: {
                            type: ArgumentType.STRING,
                            defaultValue: 'MyClass'
                        }
                    }
                },
                {
                    opcode: 'setObjectProperty',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.setObjectProperty',
                        default: 'Set property [PROPERTY] of object [OBJECT] to [VALUE]',
                        description: 'Set a property of an object'
                    }),
                    arguments: {
                        PROPERTY: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myProperty'
                        },
                        OBJECT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myObject'
                        },
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myValue'
                        }
                    }
                },
                {
                    opcode: 'returnObjectProperty',
                    blockType: BlockType.REPORTER,
                    text: formatMessage({
                        id: 'jwStructs.returnObjectProperty',
                        default: 'Property [PROPERTY] of object [OBJECT]',
                        description: 'Return a property of an object'
                    }),
                    arguments: {
                        PROPERTY: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myProperty'
                        },
                        OBJECT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myObject'
                        }
                    }
                },
                "---",
                {
                    opcode: 'createClassMethod',
                    blockType: BlockType.HAT,
                    text: formatMessage({
                        id: 'jwStructs.createClassMethod',
                        default: 'When method [NAME] is called in class [CLASS]',
                        description: 'Create a class method'
                    }),
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myMethod'
                        },
                        CLASS: {
                            type: ArgumentType.STRING,
                            defaultValue: 'MyClass'
                        }
                    }
                },
                {
                    opcode: 'callObjectMethod',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.callObjectMethod',
                        default: 'Call method [NAME] of object [OBJECT]',
                        description: 'Call a method of an object'
                    }),
                    arguments: {
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myMethod'
                        },
                        OBJECT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myObject'
                        }
                    }
                },
                "---",
                {
                    opcode: 'deleteClasses',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.deleteClasses',
                        default: 'Delete all classes',
                        description: 'Delete all classes'
                    })
                },
                {
                    opcode: 'deleteObjects',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.deleteObjects',
                        default: 'Delete all objects',
                        description: 'Delete all objects'
                    })
                },
                {
                    opcode: 'deleteClass',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.deleteClass',
                        default: 'Delete class [CLASS]',
                        description: 'Delete a class'
                    }),
                    arguments: {
                        CLASS: {
                            type: ArgumentType.STRING,
                            defaultValue: 'MyClass'
                        }
                    }
                },
                {
                    opcode: 'deleteObject',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'jwStructs.deleteObject',
                        default: 'Delete object [OBJECT]',
                        description: 'Delete an object'
                    }),
                    arguments: {
                        OBJECT: {
                            type: ArgumentType.STRING,
                            defaultValue: 'myObject'
                        }
                    }
                }
            ]
        };
    }
}

module.exports = jwStructs;