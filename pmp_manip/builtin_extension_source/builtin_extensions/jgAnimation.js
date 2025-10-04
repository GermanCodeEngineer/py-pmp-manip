const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const EasingMethods = {
    linear: null,
    sine: null,
    quad: null,
    cubic: null,
    quart: null,
    quint: null,
    expo: null,
    circ: null,
    back: null,
    elastic: null,
    bounce: null,
    snap: null,
    snapcenter: null,
    snapend: null,
};

class AnimationExtension {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    getInfo() {
        return {
            id: "jgAnimation",
            name: "Animation",
            isDynamic: true,
            blocks: [
                { opcode: 'createAnimation', text: 'New Animation', blockType: BlockType.BUTTON, },
                { opcode: 'deleteAnimation', text: 'Delete an Animation', blockType: BlockType.BUTTON, },
                {
                    opcode: 'getAnimation', text: '[ANIMATION]', blockType: BlockType.REPORTER,
                    arguments: {
                        ANIMATION: { menu: 'animations', defaultValue: '{animationId}', type: ArgumentType.STRING, }
                    },
                },
                { text: "Animations", blockType: BlockType.LABEL, },
                {
                    opcode: "playAnimation",
                    blockType: BlockType.COMMAND,
                    text: "play [ANIM] [OFFSET] and [FORWARDS] after last keyframe",
                    arguments: {
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                        OFFSET: {
                            type: ArgumentType.STRING,
                            menu: 'offsetMenu',
                        },
                        FORWARDS: {
                            type: ArgumentType.STRING,
                            menu: 'forwardsMenu',
                        },
                    },
                },
                {
                    opcode: "pauseAnimation",
                    blockType: BlockType.COMMAND,
                    text: "pause [ANIM]",
                    arguments: {
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "unpauseAnimation",
                    blockType: BlockType.COMMAND,
                    text: "unpause [ANIM]",
                    arguments: {
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "stopAnimation",
                    blockType: BlockType.COMMAND,
                    text: "stop [ANIM]",
                    arguments: {
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                { text: "Keyframes", blockType: BlockType.LABEL, },
                {
                    opcode: "addStateKeyframe",
                    blockType: BlockType.COMMAND,
                    text: "add current state with [EASING] [DIRECTION] as keyframe with duration [LENGTH] in animation [ANIM]",
                    arguments: {
                        EASING: {
                            type: ArgumentType.STRING,
                            menu: 'easingMode',
                        },
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: 'easingDir',
                        },
                        LENGTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1,
                        },
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "addJSONKeyframe",
                    blockType: BlockType.COMMAND,
                    text: "add keyframe JSON [JSON] as keyframe in animation [ANIM]",
                    arguments: {
                        JSON: {
                            type: ArgumentType.STRING,
                            defaultValue: '{}',
                        },
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "setStateKeyframe",
                    blockType: BlockType.COMMAND,
                    text: "set keyframe [IDX] in animation [ANIM] to current state with [EASING] [DIRECTION] and duration [LENGTH] ",
                    arguments: {
                        IDX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '1',
                        },
                        EASING: {
                            type: ArgumentType.STRING,
                            menu: 'easingMode',
                        },
                        DIRECTION: {
                            type: ArgumentType.STRING,
                            menu: 'easingDir',
                        },
                        LENGTH: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1,
                        },
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "setJSONKeyframe",
                    blockType: BlockType.COMMAND,
                    text: "set keyframe [IDX] in animation [ANIM] to JSON [JSON]",
                    arguments: {
                        IDX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '1',
                        },
                        JSON: {
                            type: ArgumentType.STRING,
                            defaultValue: '{}',
                        },
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "deleteKeyframe",
                    blockType: BlockType.COMMAND,
                    text: "delete keyframe [IDX] from [ANIM]",
                    arguments: {
                        IDX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '1',
                        },
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "deleteAllKeyframes",
                    blockType: BlockType.COMMAND,
                    text: "delete all keyframes [ANIM]",
                    arguments: {
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "getKeyframe",
                    blockType: BlockType.REPORTER,
                    text: "get keyframe [IDX] from [ANIM]",
                    arguments: {
                        IDX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '1',
                        },
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "getKeyframeCount",
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    text: "amount of keyframes in [ANIM]",
                    arguments: {
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "isPausedAnimation",
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    hideFromPalette: true,
                    text: "is [ANIM] paused?",
                    arguments: {
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "isPropertyAnimation",
                    blockType: BlockType.BOOLEAN,
                    disableMonitor: true,
                    text: "is [ANIM] [ANIMPROP]?",
                    arguments: {
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                        ANIMPROP: {
                            type: ArgumentType.STRING,
                            menu: 'animationDataProperty',
                        },
                    },
                },
                { text: "Operations", blockType: BlockType.LABEL, },
                {
                    opcode: "goToKeyframe",
                    blockType: BlockType.COMMAND,
                    text: "go to keyframe [IDX] in [ANIM]",
                    arguments: {
                        IDX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '1',
                        },
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
                {
                    opcode: "snapToKeyframe",
                    blockType: BlockType.COMMAND,
                    text: "snap to keyframe [IDX] in [ANIM]",
                    arguments: {
                        IDX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '1',
                        },
                        ANIM: {
                            type: ArgumentType.STRING,
                            menu: 'animations',
                        },
                    },
                },
            ],
            menus: {
                animations: '_animationsMenu',
                easingMode: {
                    acceptReporters: true,
                    items: Object.keys(EasingMethods),
                },
                easingDir: {
                    acceptReporters: true,
                    items: ["in", "out", "in out"],
                },
                animationDataProperty: {
                    acceptReporters: false,
                    items: ["playing", "paused"],
                },
                offsetMenu: {
                    acceptReporters: false,
                    items: [
                        { text: "relative to current state", value: "relative" },
                        { text: "snapped to first keyframe", value: "snapped" }
                    ],
                },
                forwardsMenu: {
                    acceptReporters: false,
                    items: [
                        { text: "stay", value: "stay" },
                        { text: "reset to original state", value: "reset" },
                    ],
                },
            }
        };
    }
}

module.exports = AnimationExtension;