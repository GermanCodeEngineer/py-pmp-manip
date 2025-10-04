const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

/**
 * Class for AudioGroups & AudioSources
 * @constructor
 */
class AudioExtension {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'jgExtendedAudio',
            name: 'Sound Systems',
            color1: '#E256A1',
            color2: '#D33388',
            isDynamic: true,
            blocks: [
                { opcode: 'createAudioGroup', text: 'New Audio Group', blockType: BlockType.BUTTON, },
                { opcode: 'deleteAudioGroup', text: 'Remove an Audio Group', blockType: BlockType.BUTTON, },
                {
                    opcode: 'audioGroupGet', text: '[AUDIOGROUP]', blockType: BlockType.REPORTER,
                    arguments: {
                        AUDIOGROUP: { menu: 'audioGroup', defaultValue: '{audioGroupId}', type: ArgumentType.STRING, }
                    },
                },
                { text: "Operations", blockType: BlockType.LABEL, },
                {
                    opcode: 'audioGroupSetVolumeSpeedPitchPan', text: 'set [AUDIOGROUP] [VSPP] to [VALUE]%', blockType: BlockType.COMMAND,
                    arguments: {
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                        VSPP: { type: ArgumentType.STRING, menu: 'vspp', defaultValue: "" },
                        VALUE: { type: ArgumentType.NUMBER, defaultValue: 100 },
                    },
                },
                {
                    opcode: 'audioGroupGetModifications', text: '[AUDIOGROUP] [OPTION]', blockType: BlockType.REPORTER, disableMonitor: true,
                    arguments: {
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                        OPTION: { type: ArgumentType.STRING, menu: 'audioGroupOptions', defaultValue: "" },
                    },
                },
                "---",
                {
                    opcode: 'audioSourceCreate', text: '[CREATEOPTION] audio source named [NAME] in [AUDIOGROUP]', blockType: BlockType.COMMAND,
                    arguments: {
                        CREATEOPTION: { type: ArgumentType.STRING, menu: 'createOptions', defaultValue: "" },
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                    },
                },
                {
                    opcode: 'audioSourceDuplicate', text: 'duplicate audio source from [NAME] to [COPY] in [AUDIOGROUP]', blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        COPY: { type: ArgumentType.STRING, defaultValue: "AudioSource2" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                    },
                },
                {
                    opcode: 'audioSourceReverse', text: 'reverse audio source used in [NAME] in [AUDIOGROUP]', blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        COPY: { type: ArgumentType.STRING, defaultValue: "AudioSource2" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                    },
                },
                {
                    opcode: 'audioSourceDeleteAll', text: '[DELETEOPTION] all audio sources in [AUDIOGROUP]', blockType: BlockType.COMMAND,
                    arguments: {
                        DELETEOPTION: { type: ArgumentType.STRING, menu: 'deleteOptions', defaultValue: "" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                    },
                },
                "---",
                {
                    opcode: 'audioSourceSetScratch', text: 'set audio source [NAME] in [AUDIOGROUP] to use [SOUND]', blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                        SOUND: { type: ArgumentType.STRING, menu: 'sounds', defaultValue: "" },
                    },
                },
                {
                    opcode: 'audioSourceSetUrl', text: 'set audio source [NAME] in [AUDIOGROUP] to use [URL]', blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                        URL: { type: ArgumentType.STRING, defaultValue: "https://extensions.turbowarp.org/meow.mp3" },
                    },
                },
                {
                    opcode: 'audioSourcePlayerOption', text: '[PLAYEROPTION] audio source [NAME] in [AUDIOGROUP]', blockType: BlockType.COMMAND,
                    arguments: {
                        PLAYEROPTION: { type: ArgumentType.STRING, menu: 'playerOptions', defaultValue: "" },
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                    },
                },
                "---",
                {
                    opcode: 'audioSourceSetLoop', text: 'set audio source [NAME] in [AUDIOGROUP] to [LOOP]', blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                        LOOP: { type: ArgumentType.STRING, menu: 'loop', defaultValue: "loop" },
                    },
                },
                {
                    opcode: 'audioSourceSetTime2', text: 'set audio source [NAME] [TIMEPOS] position in [AUDIOGROUP] to [TIME] seconds', blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        TIMEPOS: { type: ArgumentType.STRING, menu: 'timePosition' },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                        TIME: { type: ArgumentType.NUMBER, defaultValue: 0.3 },
                    },
                },
                {
                    opcode: 'audioSourceSetVolumeSpeedPitchPan', text: 'set audio source [NAME] [VSPP] in [AUDIOGROUP] to [VALUE]%', blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        VSPP: { type: ArgumentType.STRING, menu: 'vspp', defaultValue: "" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                        VALUE: { type: ArgumentType.NUMBER, defaultValue: 100 },
                    },
                },
                "---",
                {
                    opcode: 'audioSourceGetModificationsBoolean', text: 'audio source [NAME] [OPTION] in [AUDIOGROUP]', blockType: BlockType.BOOLEAN, disableMonitor: true,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        OPTION: { type: ArgumentType.STRING, menu: 'audioSourceOptionsBooleans', defaultValue: "" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                    },
                },
                {
                    opcode: 'audioSourceGetModificationsNormal', text: 'audio source [NAME] [OPTION] in [AUDIOGROUP]', blockType: BlockType.REPORTER, disableMonitor: true,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        OPTION: { type: ArgumentType.STRING, menu: 'audioSourceOptions', defaultValue: "" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                    },
                },
                // deleted blocks
                {
                    opcode: 'audioSourceSetTime', text: 'set audio source [NAME] start position in [AUDIOGROUP] to [TIME] seconds', blockType: BlockType.COMMAND,
                    arguments: {
                        NAME: { type: ArgumentType.STRING, defaultValue: "AudioSource1" },
                        AUDIOGROUP: { type: ArgumentType.STRING, menu: 'audioGroup', defaultValue: "" },
                        TIME: { type: ArgumentType.NUMBER, defaultValue: 0.3 },
                    },
                    hideFromPalette: true,
                },
            ],
            menus: {
                audioGroup: 'fetchAudioGroupMenu',
                sounds: 'fetchScratchSoundMenu',
                // specific menus
                vspp: {
                    acceptReporters: true,
                    items: [
                        { text: "volume", value: "volume" },
                        { text: "speed", value: "speed" },
                        { text: "detune", value: "pitch" },
                        { text: "pan", value: "pan" },
                    ]
                },
                playerOptions: {
                    acceptReporters: true,
                    items: [
                        { text: "play", value: "play" },
                        { text: "pause", value: "pause" },
                        { text: "stop", value: "stop" },
                    ]
                },
                loop: {
                    acceptReporters: true,
                    items: [
                        { text: "loop", value: "loop" },
                        { text: "not loop", value: "not loop" },
                    ]
                },
                timePosition: {
                    acceptReporters: true,
                    items: [
                        { text: "time", value: "time" },
                        { text: "start", value: "start" },
                        { text: "end", value: "end" },
                        { text: "start loop", value: "start loop" },
                        { text: "end loop", value: "end loop" },
                    ]
                },
                deleteOptions: {
                    acceptReporters: true,
                    items: [
                        { text: "delete", value: "delete" },
                        { text: "play", value: "play" },
                        { text: "pause", value: "pause" },
                        { text: "stop", value: "stop" },
                    ]
                },
                createOptions: {
                    acceptReporters: true,
                    items: [
                        { text: "create", value: "create" },
                        { text: "delete", value: "delete" },
                    ]
                },
                // audio group stuff
                audioGroupOptions: {
                    acceptReporters: true,
                    items: [
                        { text: "volume", value: "volume" },
                        { text: "speed", value: "speed" },
                        { text: "detune", value: "pitch" },
                        { text: "pan", value: "pan" },
                    ]
                },
                // audio source stuff
                audioSourceOptionsBooleans: {
                    acceptReporters: true,
                    items: [
                        { text: "playing", value: "playing" },
                        { text: "paused", value: "paused" },
                        { text: "looping", value: "looping" },
                    ]
                },
                audioSourceOptions: {
                    acceptReporters: true,
                    items: [
                        { text: "volume", value: "volume" },
                        { text: "speed", value: "speed" },
                        { text: "detune", value: "pitch" },
                        { text: "pan", value: "pan" },
                        { text: "time position", value: "time position" },
                        { text: "output volume", value: "output volume" },
                        { text: "start position", value: "start position" },
                        { text: "end position", value: "end position" },
                        { text: "start loop position", value: "start loop position" },
                        { text: "end loop position", value: "end loop position" },
                        { text: "sound length", value: "sound length" },
                        { text: "origin sound", value: "origin sound" },

                        // see https://stackoverflow.com/a/54567527 as to why this is not a menu option
                        // { text: "dominant frequency", value: "dominant frequency" },
                    ]
                }
            }
        };
    }
}

module.exports = AudioExtension;
