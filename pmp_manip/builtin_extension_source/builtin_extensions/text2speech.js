const formatMessage = require('format-message');
const languageNames = require('scratch-translate-extension-languages');
const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');

/**
 * Icon svg to be displayed in the blocks category menu, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const menuIconURI = 'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMjBweCIgaGVpZ2h0PSIyMHB4IiB2aWV3Qm94PSIwIDAgMjAgMjAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDUyLjIgKDY3MTQ1KSAtIGh0dHA6Ly93d3cuYm9oZW1pYW5jb2RpbmcuY29tL3NrZXRjaCAtLT4KICAgIDx0aXRsZT5FeHRlbnNpb25zL1NvZnR3YXJlL1RleHQtdG8tU3BlZWNoLU1lbnU8L3RpdGxlPgogICAgPGRlc2M+Q3JlYXRlZCB3aXRoIFNrZXRjaC48L2Rlc2M+CiAgICA8ZyBpZD0iRXh0ZW5zaW9ucy9Tb2Z0d2FyZS9UZXh0LXRvLVNwZWVjaC1NZW51IiBzdHJva2U9Im5vbmUiIHN0cm9rZS13aWR0aD0iMSIgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4KICAgICAgICA8ZyBpZD0idGV4dDJzcGVlY2giIHRyYW5zZm9ybT0idHJhbnNsYXRlKDIuMDAwMDAwLCAyLjAwMDAwMCkiIGZpbGwtcnVsZT0ibm9uemVybyI+CiAgICAgICAgICAgIDxwYXRoIGQ9Ik01Ljc1LDguODM0NjcxNzMgQzUuNzUsOC4zMjY5NjM0NCA1LjAwMzAwNzI3LDguMDQyMjEzNzEgNC41NTYyODAxMiw4LjQ0NDE0OTk5IEwzLjIwNjI4MDEyLDkuNTI1MzU3MDIgQzIuNjk2NzMzNzgsOS45MzM0NDk2OCAyLjAzNzQ4Njc1LDEwLjE2NTg3ODggMS4zNSwxMC4xNjU4Nzg4IEwxLjE1LDEwLjE2NTg3ODggQzAuNjMyNTk2MTY1LDEwLjE2NTg3ODggMC4yNSwxMC41MTA2MDAyIDAuMjUsMTAuOTUyMDM1NSBMMC4yNSwxMy4wNjkzOTkzIEMwLjI1LDEzLjUxMDgzNDYgMC42MzI1OTYxNjUsMTMuODU1NTU2IDEuMTUsMTMuODU1NTU2IEwxLjM1LDEzLjg1NTU1NiBDMi4wNzg3Nzg0MSwxMy44NTU1NTYgMi43MjY4NjE2MSwxNC4wNjY3NjM2IDMuMjU5ODYwNDksMTQuNDk5IEw0LjU1OTIwMTQ3LDE1LjU3OTY2MDggQzUuMDEzMDkyNzYsMTUuOTU0NTM5NiA1Ljc1LDE1LjY3MzYzNDQgNS43NSwxNS4xNDE3MTI4IEw1Ljc1LDguODM0NjcxNzMgWiIgaWQ9InNwZWFrZXIiIHN0cm9rZS1vcGFjaXR5PSIwLjE1IiBzdHJva2U9IiMwMDAwMDAiIHN0cm9rZS13aWR0aD0iMC41IiBmaWxsPSIjNEQ0RDREIj48L3BhdGg+CiAgICAgICAgICAgIDxwYXRoIGQ9Ik0xMC43MDQ4MzEzLDggQzkuNzkwNjc0NjgsOS4xMzExNDg0NyA4LjMwNjYxODQsOS43MTQyODU3MSA3LjgzMzMzMzMzLDkuNzE0Mjg1NzEgQzcuODMzMzMzMzMsOS43MTQyODU3MSA3LjUsOS43MTQyODU3MSA3LjUsOS4zODA5NTIzOCBDNy41LDkuMDg1MjI2ODQgOC4wNjIyMDE2OCw4LjkwMTk0MTY0IDguMTg5MDYwNjcsNy41Njc1NDA1OCBDNi44ODk5Njk5MSw2LjkwNjc5MDA1IDYsNS41NTczMjY4MyA2LDQgQzYsMS43OTA4NjEgNy43OTA4NjEsNC4wNTgxMjI1MWUtMTYgMTAsMCBMMTIsMCBDMTQuMjA5MTM5LC00LjA1ODEyMjUxZS0xNiAxNiwxLjc5MDg2MSAxNiw0IEMxNiw2LjIwOTEzOSAxNC4yMDkxMzksOCAxMiw4IEwxMC43MDQ4MzEzLDggWiIgaWQ9InNwZWVjaCIgZmlsbD0iIzBFQkQ4QyI+PC9wYXRoPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+';

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iNDBweCIgaGVpZ2h0PSI0MHB4IiB2aWV3Qm94PSIwIDAgNDAgNDAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDUyLjIgKDY3MTQ1KSAtIGh0dHA6Ly93d3cuYm9oZW1pYW5jb2RpbmcuY29tL3NrZXRjaCAtLT4KICAgIDx0aXRsZT5FeHRlbnNpb25zL1NvZnR3YXJlL1RleHQtdG8tU3BlZWNoLUJsb2NrPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkV4dGVuc2lvbnMvU29mdHdhcmUvVGV4dC10by1TcGVlY2gtQmxvY2siIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1vcGFjaXR5PSIwLjE1Ij4KICAgICAgICA8ZyBpZD0idGV4dDJzcGVlY2giIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQuMDAwMDAwLCA0LjAwMDAwMCkiIGZpbGwtcnVsZT0ibm9uemVybyIgc3Ryb2tlPSIjMDAwMDAwIj4KICAgICAgICAgICAgPHBhdGggZD0iTTExLjUsMTcuNjY5MzQzNSBDMTEuNSwxNi42NTM5MjY5IDEwLjAwNjAxNDUsMTYuMDg0NDI3NCA5LjExMjU2MDI0LDE2Ljg4ODMgTDYuNDEyNTYwMjQsMTkuMDUwNzE0IEM1LjM5MzQ2NzU1LDE5Ljg2Njg5OTQgNC4wNzQ5NzM1MSwyMC4zMzE3NTc1IDIuNywyMC4zMzE3NTc1IEwyLjMsMjAuMzMxNzU3NSBDMS4yNjUxOTIzMywyMC4zMzE3NTc1IDAuNSwyMS4wMjEyMDAzIDAuNSwyMS45MDQwNzEgTDAuNSwyNi4xMzg3OTg2IEMwLjUsMjcuMDIxNjY5MyAxLjI2NTE5MjMzLDI3LjcxMTExMiAyLjMsMjcuNzExMTEyIEwyLjcsMjcuNzExMTEyIEM0LjE1NzU1NjgyLDI3LjcxMTExMiA1LjQ1MzcyMzIyLDI4LjEzMzUyNzEgNi41MTk3MjA5OCwyOC45OTggTDkuMTE4NDAyOTMsMzEuMTU5MzIxNiBDMTAuMDI2MTg1NSwzMS45MDkwNzkzIDExLjUsMzEuMzQ3MjY4OSAxMS41LDMwLjI4MzQyNTUgTDExLjUsMTcuNjY5MzQzNSBaIiBpZD0ic3BlYWtlciIgZmlsbD0iIzRENEQ0RCI+PC9wYXRoPgogICAgICAgICAgICA8cGF0aCBkPSJNMjEuNjQzNjA2NiwxNi41IEMxOS45NzcwMDk5LDE4LjQzNzAyMzQgMTcuMTA1MDI3NSwxOS45Mjg1NzE0IDE1LjY2NjY2NjcsMTkuOTI4NTcxNCBDMTUuNTEyNjM5NywxOS45Mjg1NzE0IDE1LjMxNjYyOTIsMTkuODk1OTAzIDE1LjEwOTcyNjUsMTkuNzkyNDUxNyBDMTQuNzM3NjAzOSwxOS42MDYzOTA0IDE0LjUsMTkuMjQ5OTg0NiAxNC41LDE4Ljc2MTkwNDggQzE0LjUsMTguNjU2ODA0MSAxNC41MTcwNTU1LDE4LjU1NDUwNzYgMTQuNTQ5NDQ2NywxOC40NTQwODQ0IEMxNC42MjU3NTQ1LDE4LjIxNzUwNjMgMTUuMTczNTcyMSwxNy40Njc1MzEgMTUuMjc3MjA3MSwxNy4yODA5ODgxIEMxNS41NDYzNTI2LDE2Ljc5NjUyNjEgMTUuNzM5MDI1LDE2LjIwNjM1NjEgMTUuODQzMjg5MSwxNS40MTYwMDM0IEMxMy4xODk3MDA1LDEzLjkyNjgzNjkgMTEuNSwxMS4xMTM5NjY4IDExLjUsOCBDMTEuNSwzLjMwNTU3OTYzIDE1LjMwNTU3OTYsLTAuNSAyMCwtMC41IEwyNCwtMC41IEMyOC42OTQ0MjA0LC0wLjUgMzIuNSwzLjMwNTU3OTYzIDMyLjUsOCBDMzIuNSwxMi42OTQ0MjA0IDI4LjY5NDQyMDQsMTYuNSAyNCwxNi41IEwyMS42NDM2MDY2LDE2LjUgWiIgaWQ9InNwZWVjaCIgZmlsbD0iI0ZGRkZGRiI+PC9wYXRoPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+';

/**
 * An id for one of the voices.
 */
const ALTO_ID = 'ALTO';

/**
 * An id for one of the voices.
 */
const TENOR_ID = 'TENOR';

/**
 * An id for one of the voices.
 */
const SQUEAK_ID = 'SQUEAK';

/**
 * An id for one of the voices.
 */
const GIANT_ID = 'GIANT';

/**
 * An id for one of the voices.
 */
const KITTEN_ID = 'KITTEN';

/**
 * An id for one of the voices.
 */
const GOOGLE_ID = 'GOOGLE';

/**
 * Language ids. The value for each language id is a valid Scratch locale.
 */
const ARABIC_ID = 'ar';
const CHINESE_ID = 'zh-cn';
const DANISH_ID = 'da';
const DUTCH_ID = 'nl';
const ENGLISH_ID = 'en';
const FRENCH_ID = 'fr';
const GERMAN_ID = 'de';
const HINDI_ID = 'hi';
const ICELANDIC_ID = 'is';
const ITALIAN_ID = 'it';
const JAPANESE_ID = 'ja';
const KOREAN_ID = 'ko';
const NORWEGIAN_ID = 'nb';
const POLISH_ID = 'pl';
const PORTUGUESE_BR_ID = 'pt-br';
const PORTUGUESE_ID = 'pt';
const ROMANIAN_ID = 'ro';
const RUSSIAN_ID = 'ru';
const SPANISH_ID = 'es';
const SPANISH_419_ID = 'es-419';
const SWEDISH_ID = 'sv';
const TURKISH_ID = 'tr';
const WELSH_ID = 'cy';

/**
 * Class for the text2speech blocks.
 * @constructor
 */
class Scratch3Text2SpeechBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * An object with info for each voice.
     */
    get VOICE_INFO () {
        return {
            [ALTO_ID]: {
                name: formatMessage({
                    id: 'text2speech.alto',
                    default: 'alto',
                    description: 'Name for a voice with ambiguous gender.'
                }),
                gender: 'female',
                playbackRate: 1
            },
            [TENOR_ID]: {
                name: formatMessage({
                    id: 'text2speech.tenor',
                    default: 'tenor',
                    description: 'Name for a voice with ambiguous gender.'
                }),
                gender: 'male',
                playbackRate: 1
            },
            [SQUEAK_ID]: {
                name: formatMessage({
                    id: 'text2speech.squeak',
                    default: 'squeak',
                    description: 'Name for a funny voice with a high pitch.'
                }),
                gender: 'female',
                playbackRate: 1.19 // +3 semitones
            },
            [GIANT_ID]: {
                name: formatMessage({
                    id: 'text2speech.giant',
                    default: 'giant',
                    description: 'Name for a funny voice with a low pitch.'
                }),
                gender: 'male',
                playbackRate: 0.84 // -3 semitones
            },
            [KITTEN_ID]: {
                name: formatMessage({
                    id: 'text2speech.kitten',
                    default: 'kitten',
                    description: 'A baby cat.'
                }),
                gender: 'female',
                playbackRate: 1.41 // +6 semitones
            },
            [GOOGLE_ID]: {
                name: formatMessage({
                    id: 'text2speech.google',
                    default: 'google',
                    description: 'Name for a voice with ambiguous gender.'
                }),
                special: 'google',
                gender: 'mixed',
                playbackRate: 1
            },
        };
    }

    /**
     * An object with information for each language.
     *
     * A note on the different sets of locales referred to in this extension:
     *
     * SCRATCH LOCALE
     *      Set by the editor, and used to store the language state in the project.
     *      Listed in l10n: https://github.com/LLK/scratch-l10n/blob/master/src/supported-locales.js
     * SUPPORTED LOCALE
     *      A Scratch locale that has a corresponding extension locale.
     * EXTENSION LOCALE
     *      A locale corresponding to one of the available spoken languages
     *      in the extension. There can be multiple supported locales for a single
     *      extension locale. For example, for both written versions of chinese,
     *      zh-cn and zh-tw, we use a single spoken language (Mandarin). So there
     *      are two supported locales, with a single extension locale.
     * SPEECH SYNTH LOCALE
     *      A different locale code system, used by our speech synthesis service.
     *      Each extension locale has a speech synth locale.
     * PENGUINMOD SYNTH LOCALE
     *      A different locale code system, used by PenguinMod's speech synthesis service.
     *      Each extension locale has a PenguinMod synth locale, and some may be the same as another locale.
     */
    get LANGUAGE_INFO () {
        return {
            [ARABIC_ID]: {
                name: 'Arabic',
                locales: ['ar'],
                speechSynthLocale: 'arb',
                penguinmodSynthLocale: 'ar',
                singleGender: true
            },
            [CHINESE_ID]: {
                name: 'Chinese (Mandarin)',
                locales: ['zh-cn', 'zh-tw'],
                speechSynthLocale: 'cmn-CN',
                penguinmodSynthLocale: 'zh-cn',
                singleGender: true
            },
            [DANISH_ID]: {
                name: 'Danish',
                locales: ['da'],
                speechSynthLocale: 'da-DK',
                penguinmodSynthLocale: 'da',
            },
            [DUTCH_ID]: {
                name: 'Dutch',
                locales: ['nl'],
                speechSynthLocale: 'nl-NL',
                penguinmodSynthLocale: 'nl',
            },
            [ENGLISH_ID]: {
                name: 'English',
                locales: ['en'],
                speechSynthLocale: 'en-US',
                penguinmodSynthLocale: 'en',
            },
            [FRENCH_ID]: {
                name: 'French',
                locales: ['fr'],
                speechSynthLocale: 'fr-FR',
                penguinmodSynthLocale: 'fr',
            },
            [GERMAN_ID]: {
                name: 'German',
                locales: ['de'],
                speechSynthLocale: 'de-DE',
                penguinmodSynthLocale: 'de',
            },
            [HINDI_ID]: {
                name: 'Hindi',
                locales: ['hi'],
                speechSynthLocale: 'hi-IN',
                penguinmodSynthLocale: 'hi',
                singleGender: true
            },
            [ICELANDIC_ID]: {
                name: 'Icelandic',
                locales: ['is'],
                speechSynthLocale: 'is-IS',
                penguinmodSynthLocale: 'is',
            },
            [ITALIAN_ID]: {
                name: 'Italian',
                locales: ['it'],
                speechSynthLocale: 'it-IT',
                penguinmodSynthLocale: 'it',
            },
            [JAPANESE_ID]: {
                name: 'Japanese',
                locales: ['ja', 'ja-hira'],
                speechSynthLocale: 'ja-JP',
                penguinmodSynthLocale: 'ja',
            },
            [KOREAN_ID]: {
                name: 'Korean',
                locales: ['ko'],
                speechSynthLocale: 'ko-KR',
                penguinmodSynthLocale: 'ko',
                singleGender: true
            },
            [NORWEGIAN_ID]: {
                name: 'Norwegian',
                locales: ['nb', 'nn'],
                speechSynthLocale: 'nb-NO',
                penguinmodSynthLocale: 'no',
                singleGender: true
            },
            [POLISH_ID]: {
                name: 'Polish',
                locales: ['pl'],
                speechSynthLocale: 'pl-PL',
                penguinmodSynthLocale: 'pl',
            },
            [PORTUGUESE_BR_ID]: {
                name: 'Portuguese (Brazilian)',
                locales: ['pt-br'],
                speechSynthLocale: 'pt-BR',
                penguinmodSynthLocale: 'pt-br',
            },
            [PORTUGUESE_ID]: {
                name: 'Portuguese (European)',
                locales: ['pt'],
                speechSynthLocale: 'pt-PT',
                penguinmodSynthLocale: 'pt',
            },
            [ROMANIAN_ID]: {
                name: 'Romanian',
                locales: ['ro'],
                speechSynthLocale: 'ro-RO',
                penguinmodSynthLocale: 'ro',
                singleGender: true
            },
            [RUSSIAN_ID]: {
                name: 'Russian',
                locales: ['ru'],
                speechSynthLocale: 'ru-RU',
                penguinmodSynthLocale: 'ru',
            },
            [SPANISH_ID]: {
                name: 'Spanish (European)',
                locales: ['es'],
                speechSynthLocale: 'es-ES',
                penguinmodSynthLocale: 'es-es',
            },
            [SPANISH_419_ID]: {
                name: 'Spanish (Latin American)',
                locales: ['es-419'],
                speechSynthLocale: 'es-US',
                penguinmodSynthLocale: 'es-us',
            },
            [SWEDISH_ID]: {
                name: 'Swedish',
                locales: ['sv'],
                speechSynthLocale: 'sv-SE',
                penguinmodSynthLocale: 'sv',
                singleGender: true
            },
            [TURKISH_ID]: {
                name: 'Turkish',
                locales: ['tr'],
                speechSynthLocale: 'tr-TR',
                penguinmodSynthLocale: 'tr',
                singleGender: true
            },
            [WELSH_ID]: {
                name: 'Welsh',
                locales: ['cy'],
                speechSynthLocale: 'cy-GB',
                penguinmodSynthLocale: 'cy',
                singleGender: true
            }
        };
    }

    /**
     * An array of IDs that are the voices that will only work on PenguinMod's API.
     */
    get PENGUINMOD_VOICES () {
        return [
            GOOGLE_ID
        ];
    }
    /**
     * Key-value pairs for turning a voice ID into the parameter for the PenguinMod API.
     */
    get PENGUINMOD_VOICE_MAP () {
        return {
            [GOOGLE_ID]: 'google'
        };
    }
    /**
     * Key-value pairs for getting a nice volume setting for a specific PenguinMod voice.
     * The volumes are a percentage number like 100 for 100% volume.
     */
    get PENGUINMOD_VOICE_VOLUMES () {
        return {
            [GOOGLE_ID]: 100
        };
    }

    /**
     * The default state, to be used when a target has no existing state.
     * @type {Text2SpeechState}
     */
    static get DEFAULT_TEXT2SPEECH_STATE () {
        return {
            voiceId: ALTO_ID
        };
    }

    /**
     * A default language to use for speech synthesis.
     * @type {string}
     */
    get DEFAULT_LANGUAGE () {
        return ENGLISH_ID;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        // Only localize the default input to the "speak" block if we are in a
        // supported language.
        const defaultTextToSpeak = formatMessage({
            id: 'text2speech.defaultTextToSpeak',
            default: 'hello',
            description: 'hello: the default text to speak'
        });

        return {
            id: 'text2speech',
            name: formatMessage({
                id: 'text2speech.categoryName',
                default: 'Text to Speech',
                description: 'Name of the Text to Speech extension.'
            }),
            blockIconURI: blockIconURI,
            menuIconURI: menuIconURI,
            blocks: [
                {
                    opcode: 'speakAndWait',
                    text: formatMessage({
                        id: 'text2speech.speakAndWaitBlock',
                        default: 'speak [WORDS]',
                        description: 'Speak some words.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        WORDS: {
                            type: ArgumentType.STRING,
                            defaultValue: defaultTextToSpeak
                        }
                    }
                },
                {
                    opcode: 'setVoice',
                    text: formatMessage({
                        id: 'text2speech.setVoiceBlock',
                        default: 'set voice to [VOICE]',
                        description: 'Set the voice for speech synthesis.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        VOICE: {
                            type: ArgumentType.STRING,
                            menu: 'voices',
                            defaultValue: ALTO_ID
                        }
                    }
                },
                {
                    opcode: 'setLanguage',
                    text: formatMessage({
                        id: 'text2speech.setLanguageBlock',
                        default: 'set language to [LANGUAGE]',
                        description: 'Set the language for speech synthesis.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        LANGUAGE: {
                            type: ArgumentType.STRING,
                            menu: 'languages',
                            defaultValue: "English",
                        }
                    }
                },
                {
                    opcode: 'setSpeed',
                    text: formatMessage({
                        id: 'text2speech.setSpeedBlock',
                        default: 'set reading speed to [SPEED]%',
                        description: 'Set the reading speed and pitch for speech synthesis.'
                    }),
                    blockType: BlockType.COMMAND,
                    arguments: {
                        SPEED: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 100
                        }
                    }
                }
            ],
            menus: {
                voices: {
                    acceptReporters: true,
                    items: this.getVoiceMenu()
                },
                languages: {
                    acceptReporters: true,
                    items: this.getLanguageMenu()
                }
            }
        };
    }

    /**
     * Get the menu of voices for the "set voice" block.
     * @return {array} the text and value for each menu item.
     */
    getVoiceMenu () {
        return Object.keys(this.VOICE_INFO).map(voiceId => ({
            text: this.VOICE_INFO[voiceId].name,
            value: voiceId
        }));
    }

    /**
     * Get the localized menu of languages for the "set language" block.
     * For each language:
     *   if there is a custom translated spoken language name, use that;
     *   otherwise use the translation in the languageNames menuMap;
     *   otherwise fall back to the untranslated name in LANGUAGE_INFO.
     * @return {array} the text and value for each menu item.
     */
    getLanguageMenu () {
        const editorLanguage = "en"; // generated extension info is always in English.
        // Get the array of localized language names
        const localizedNameMap = {};
        let nameArray = languageNames.menuMap[editorLanguage];
        if (nameArray) {
            // Also get any localized names of spoken languages
            let spokenNameArray = [];
            if (languageNames.spokenLanguages) {
                spokenNameArray = languageNames.spokenLanguages[editorLanguage];
                nameArray = nameArray.concat(spokenNameArray);
            }
            // Create a map of language code to localized name
            // The localized spoken language names have been concatenated onto
            // the end of the name array, so the result of the forEach below is
            // when there is both a written language name (e.g. 'Chinese
            // (simplified)') and a spoken language name (e.g. 'Chinese
            // (Mandarin)', we always use the spoken version.
            nameArray.forEach(lang => {
                localizedNameMap[lang.code] = lang.name;
            });
        }

        return Object.keys(this.LANGUAGE_INFO).map(key => {
            let name = this.LANGUAGE_INFO[key].name;
            const localizedName = localizedNameMap[key];
            if (localizedName) {
                name = localizedName;
            }
            // Uppercase the first character of the name
            name = name.charAt(0).toUpperCase() + name.slice(1);
            return {
                text: name,
                value: key
            };
        });
    }
}
module.exports = Scratch3Text2SpeechBlocks;
