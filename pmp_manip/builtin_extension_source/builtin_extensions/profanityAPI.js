// Created by TheShovel
// https://github.com/TheShovel
//
// 99% of the code here was not created by a PenguinMod developer!
// Look above for proper crediting :)

const ArgumentType = require("../../extension-support/argument-type");
const BlockType = require("../../extension-support/block-type");

class profanityAPI {
    getInfo() {
        return {
            id: "profanityAPI",
            name: "Censorship",
            blocks: [
                {
                    opcode: "checkProfanity",
                    blockType: BlockType.REPORTER,
                    disableMonitor: false,
                    text: "remove profanity from [TEXT]",
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "Hello, I love pizza!",
                        },
                    },
                },
            ],
        };
    }
}

module.exports = profanityAPI;