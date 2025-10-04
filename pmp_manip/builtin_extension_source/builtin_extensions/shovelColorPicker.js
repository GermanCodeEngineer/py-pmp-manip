// Created by TheShovel
// https://github.com/TheShovel
//
// 99% of the code here was not created by a PenguinMod developer!
// Look above for proper crediting :)

const ArgumentType = require("../../extension-support/argument-type");
const BlockType = require("../../extension-support/block-type");

class ColorPicker {
    constructor(runtime) {
        this.runtime = runtime;
    }

    getInfo() {
        return {
            id: "shovelColorPicker",
            name: "ColorPicker",
            color1: "#ff7db5",
            color2: "#e0649a",
            color3: "#c14d7f",
            blocks: [
                {
                    opcode: "showPicker",
                    blockType: BlockType.COMMAND,
                    text: "show color picker",
                },
                {
                    opcode: "setPos",
                    blockType: BlockType.COMMAND,
                    text: "set picker position to x: [X] y: [Y]",
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0,
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0,
                        },
                    },
                },
                {
                    opcode: "setColor",
                    blockType: BlockType.COMMAND,
                    text: "set picker color to [COLOR]",
                    arguments: {
                        COLOR: {
                            type: ArgumentType.COLOR,
                            defaultValue: "#855CD6",
                        },
                    },
                },
                {
                    opcode: "getColor",
                    blockType: BlockType.REPORTER,
                    text: "color [TYPE] value",
                    arguments: {
                        TYPE: {
                            type: ArgumentType.STRING,
                            menu: "RGBMenu",
                        },
                    },
                },
                {
                    opcode: "getPos",
                    blockType: BlockType.REPORTER,
                    text: "picker [COORD] position",
                    arguments: {
                        COORD: {
                            type: ArgumentType.STRING,
                            menu: "POSMenu",
                        },
                    },
                },
                {
                    opcode: "whenChanged",
                    blockType: BlockType.EVENT,
                    isEdgeActivated: false,
                    text: "when color changed",
                },
            ],
            menus: {
                RGBMenu: {
                    acceptReporters: true,
                    items: ["hex", "red", "green", "blue"],
                },
                POSMenu: {
                    acceptReporters: true,
                    items: ["X", "Y"],
                },
            },
        };
    }
}

module.exports = ColorPicker;