// Created by TheShovel
// https://github.com/TheShovel

// Thanks LilyMakesThings for the awesome banner!

const ArgumentType = require("../../extension-support/argument-type");
const BlockType = require("../../extension-support/block-type");

// Icons do not matter
const ColorIcon = null;
const BorderIcon = null;
const extensionIcon = null;
const miscIcon = null;
const TransparentIcon = null;
const GradientIcon = null;
const PictureIcon = null;
const ResetIcon = null;

class MonitorStyles {
    constructor(runtime) {
        this.runtime = runtime;
    }
    getInfo() {
        return {
            id: "shovelcss",
            name: "Custom Styles",
            menuIconURI: extensionIcon,
            color1: "#0072d6",
            color2: "#0064bc",
            color3: "#01539b",
            blocks: [
                {
                    blockIconURI: ColorIcon,
                    opcode: "changecss",
                    blockType: BlockType.COMMAND,
                    text: "set [COLORABLE] to [COLOR]",
                    arguments: {
                        COLORABLE: {
                            type: ArgumentType.STRING,
                            menu: "COLORABLE_MENU",
                        },
                        COLOR: {
                            type: ArgumentType.COLOR,
                            defaultValue: "#ff0000",
                        },
                    },
                },
                {
                    blockIconURI: GradientIcon,
                    opcode: "gradientAngle",
                    blockType: BlockType.REPORTER,
                    text: "make a gradient with [COLOR1] and [COLOR2] at angle [ANGLE]",
                    arguments: {
                        COLOR1: {
                            type: ArgumentType.COLOR,
                            defaultValue: "#ff0000",
                        },
                        COLOR2: {
                            type: ArgumentType.COLOR,
                            defaultValue: "#6ed02d",
                        },
                        ANGLE: {
                            type: ArgumentType.ANGLE,
                            defaultValue: "90",
                        },
                    },
                },
                {
                    blockIconURI: TransparentIcon,
                    disableMonitor: true,
                    opcode: "transparentinput",
                    blockType: BlockType.REPORTER,
                    text: "transparent",
                },
                {
                    blockIconURI: PictureIcon,
                    disableMonitor: true,
                    opcode: "pictureinput",
                    blockType: BlockType.REPORTER,
                    text: "image [URL]",
                    arguments: {
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: "https://extensions.turbowarp.org/dango.png",
                        },
                    },
                },
                "---",
                {
                    blockIconURI: PictureIcon,
                    disableMonitor: true,
                    opcode: "setAskURI",
                    blockType: BlockType.COMMAND,
                    text: "set ask prompt button image to [URL]",
                    arguments: {
                        URL: {
                            type: ArgumentType.STRING,
                            defaultValue: "https://extensions.turbowarp.org/dango.png",
                        },
                    },
                },
                "---",
                {
                    blockIconURI: BorderIcon,
                    opcode: "setbordersize",
                    blockType: BlockType.COMMAND,
                    text: "set border width of [BORDER] to [SIZE]",
                    arguments: {
                        BORDER: {
                            type: ArgumentType.STRING,
                            menu: "BORDER_WIDTH_MENU",
                        },
                        SIZE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "2",
                        },
                    },
                },
                {
                    blockIconURI: BorderIcon,
                    opcode: "setborderradius",
                    blockType: BlockType.COMMAND,
                    text: "set roundness of [CORNER] to [SIZE]",
                    arguments: {
                        SIZE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "4",
                        },
                        CORNER: {
                            type: ArgumentType.STRING,
                            menu: "BORDER_ROUNDNESS_MENU",
                        },
                    },
                },
                "---",
                {
                    blockIconURI: ResetIcon,
                    opcode: "clearCSS",
                    blockType: BlockType.COMMAND,
                    text: "reset styles",
                },
                "---",
                {
                    blockIconURI: miscIcon,
                    opcode: "allowscrollrule",
                    blockType: BlockType.COMMAND,
                    text: "set list scrolling to [SCROLLRULE]",
                    arguments: {
                        SCROLLRULE: {
                            type: ArgumentType.STRING,
                            menu: "SCROLL_MENU",
                        },
                    },
                },
                {
                    blockIconURI: miscIcon,
                    opcode: "getValue",
                    blockType: BlockType.REPORTER,
                    text: "get [ITEM]",
                    arguments: {
                        ITEM: {
                            type: ArgumentType.STRING,
                            menu: "VALUEGET_LIST",
                        },
                    },
                },
                "---",
                {
                    blockIconURI: miscIcon,
                    opcode: "setvarpos",
                    blockType: BlockType.COMMAND,
                    text: "set position of variable [NAME] to x: [X] y: [Y]",
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "my variable",
                        },
                    },
                },
                {
                    blockIconURI: miscIcon,
                    opcode: "setlistpos",
                    blockType: BlockType.COMMAND,
                    text: "set position of list [NAME] to x: [X] y: [Y]",
                    arguments: {
                        X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        Y: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0",
                        },
                        NAME: {
                            type: ArgumentType.STRING,
                            defaultValue: "my variable",
                        },
                    },
                },
            ],
            // Accepting reporters because there can't be errors in case the value is not correct
            menus: {
                COLORABLE_MENU: {
                    acceptReporters: true,
                    items: [
                        "monitor text",
                        "monitor background",
                        "monitor border",
                        "variable value background",
                        "variable value text",
                        "list header background",
                        "list footer background",
                        "list value background",
                        "list value text",
                        "ask prompt background",
                        "ask prompt button background",
                        "ask prompt input background",
                        "ask prompt question text",
                        "ask prompt input text",
                        "ask prompt input border",
                    ],
                },
                BORDER_WIDTH_MENU: {
                    acceptReporters: true,
                    items: [
                        "monitor background",
                        "ask prompt background",
                        "ask prompt input",
                    ],
                },
                BORDER_ROUNDNESS_MENU: {
                    acceptReporters: true,
                    items: [
                        "monitor background",
                        "variable value",
                        "list value",
                        "ask prompt background",
                        "ask prompt button",
                        "ask prompt input",
                    ],
                },
                SCROLL_MENU: {
                    acceptReporters: true,
                    items: ["enabled", "disabled"],
                },
                VALUEGET_LIST: {
                    acceptReporters: true,
                    items: [
                        "monitor text",
                        "monitor background",
                        "monitor border color",
                        "variable value background",
                        "variable value text",
                        "list header background",
                        "list footer background",
                        "list value background",
                        "list value text",
                        "ask prompt background",
                        "ask prompt button background",
                        "ask prompt input background",
                        "ask prompt input text",
                        "ask prompt input border",
                        "monitor background border width",
                        "ask prompt background border width",
                        "ask prompt input border width",
                        "monitor background roundness",
                        "variable value roundness",
                        "list value roundness",
                        "ask prompt background roundness",
                        "ask prompt button roundness",
                        "ask prompt input roundness",
                        "ask prompt button image",
                        "list scroll rule",
                    ],
                },
            },
        };
    }
}

module.exports = MonitorStyles;
