// Created by TheShovel
// https://github.com/TheShovel
//
// 99% of the code here was not created by a PenguinMod developer!
// Look above for proper crediting :)

const ArgumentType = require("../../extension-support/argument-type");
const BlockType = require("../../extension-support/block-type");

class lzcompress {
    getInfo() {
        return {
            id: "shovellzcompresss",
            name: "LZ Compress",
            blocks: [
                {
                    opcode: "compress",
                    blockType: BlockType.REPORTER,
                    text: "compress [TEXT] to [TYPE]",
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello world!",
                        },
                        TYPE: {
                            type: ArgumentType.STRING,
                            menu: "COMPRESSIONTYPES",
                        },
                    },
                },
                {
                    opcode: "decompress",
                    blockType: BlockType.REPORTER,
                    text: "decompress [TEXT] from [TYPE]",
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "҅〶惶@✰Ӏ葀",
                        },
                        TYPE: {
                            type: ArgumentType.STRING,
                            menu: "COMPRESSIONTYPES",
                        },
                    },
                },
            ],
            menus: {
                COMPRESSIONTYPES: {
                    acceptReporters: true,
                    items: [
                        "Raw",
                        "Base64",
                        "EncodedURIComponent",
                        "ArrayBuffer",
                        "UTF16",
                    ],
                },
            },
        };
    }
}

module.exports = lzcompress;