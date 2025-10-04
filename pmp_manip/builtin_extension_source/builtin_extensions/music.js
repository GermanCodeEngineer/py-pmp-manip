const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const formatMessage = require('format-message');

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+PHRpdGxlPm11c2ljLWJsb2NrLWljb248L3RpdGxlPjxkZWZzPjxwYXRoIGQ9Ik0zMi4xOCAyNS44NzRDMzIuNjM2IDI4LjE1NyAzMC41MTIgMzAgMjcuNDMzIDMwYy0zLjA3IDAtNS45MjMtMS44NDMtNi4zNzItNC4xMjYtLjQ1OC0yLjI4NSAxLjY2NS00LjEzNiA0Ljc0My00LjEzNi42NDcgMCAxLjI4My4wODQgMS44OS4yMzQuMzM4LjA4Ni42MzcuMTguOTM4LjMwMi44Ny0uMDItLjEwNC0yLjI5NC0xLjgzNS0xMi4yMy0yLjEzNC0xMi4zMDIgMy4wNi0xLjg3IDguNzY4LTIuNzUyIDUuNzA4LS44ODUuMDc2IDQuODItMy42NSAzLjg0NC0zLjcyNC0uOTg3LTQuNjUtNy4xNTMuMjYzIDE0LjczOHptLTE2Ljk5OCA1Ljk5QzE1LjYzIDM0LjE0OCAxMy41MDcgMzYgMTAuNDQgMzZjLTMuMDcgMC01LjkyMi0xLjg1Mi02LjM4LTQuMTM2LS40NDgtMi4yODQgMS42NzQtNC4xMzUgNC43NS00LjEzNSAxLjAwMyAwIDEuOTc1LjE5NiAyLjg1NS41NDMuODIyLS4wNTUtLjE1LTIuMzc3LTEuODYyLTEyLjIyOC0yLjEzMy0xMi4zMDMgMy4wNi0xLjg3IDguNzY0LTIuNzUzIDUuNzA2LS44OTQuMDc2IDQuODItMy42NDggMy44MzQtMy43MjQtLjk4Ny00LjY1LTcuMTUyLjI2MiAxNC43Mzh6IiBpZD0iYSIvPjwvZGVmcz48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjx1c2UgZmlsbD0iI0ZGRiIgeGxpbms6aHJlZj0iI2EiLz48cGF0aCBzdHJva2Utb3BhY2l0eT0iLjEiIHN0cm9rZT0iIzAwMCIgZD0iTTI4LjQ1NiAyMS42NzVjLS4wMS0uMzEyLS4wODctLjgyNS0uMjU2LTEuNzAyLS4wOTYtLjQ5NS0uNjEyLTMuMDIyLS43NTMtMy43My0uMzk1LTEuOTgtLjc2LTMuOTItMS4xNDItNi4xMTMtLjczMi00LjIyMy0uNjkzLTYuMDUuMzQ0LTYuNTI3LjUtLjIzIDEuMDYtLjA4IDEuODQuMzUuNDE0LjIyNyAyLjE4MiAxLjM2NSAyLjA3IDEuMjk2IDEuOTk0IDEuMjQyIDMuNDY0IDEuNzc0IDQuOTMgMS41NDggMS41MjYtLjIzNyAyLjUwNC0uMDYgMi44NzYuNjE4LjM0OC42MzUuMDE1IDEuNDE2LS43MyAyLjE4LTEuNDcyIDEuNTE2LTMuOTc1IDIuNTE0LTUuODQ4IDIuMDIzLS44MjItLjIyLTEuMjM4LS40NjUtMi4zOC0xLjI2N2wtLjA5NS0uMDY2Yy4wNDcuNTkzLjI2NCAxLjc0LjcxNyAzLjgwMy4yOTQgMS4zMzYgMi4wOCA5LjE4NyAyLjYzNyAxMS42NzRsLjAwMi4wMTJjLjUyOCAyLjYzNy0xLjg3MyA0LjcyNC01LjIzNiA0LjcyNC0zLjI5IDAtNi4zNjMtMS45ODgtNi44NjItNC41MjgtLjUzLTIuNjQgMS44NzMtNC43MzQgNS4yMzMtNC43MzQuNjcyIDAgMS4zNDcuMDg1IDIuMDE0LjI1LjIyNy4wNTcuNDM2LjExOC42MzYuMTg3em0tMTYuOTk2IDUuOTljLS4wMS0uMzE4LS4wOS0uODM4LS4yNjYtMS43MzctLjA5LS40Ni0uNTk1LTIuOTM3LS43NTMtMy43MjctLjM5LTEuOTYtLjc1LTMuODktMS4xMy02LjA3LS43MzItNC4yMjMtLjY5Mi02LjA1LjM0NC02LjUyNi41MDItLjIzIDEuMDYtLjA4MiAxLjg0LjM1LjQxNS4yMjcgMi4xODIgMS4zNjQgMi4wNyAxLjI5NSAxLjk5MyAxLjI0MiAzLjQ2MiAxLjc3NCA0LjkyNiAxLjU0OCAxLjUyNS0uMjQgMi41MDQtLjA2NCAyLjg3Ni42MTQuMzQ4LjYzNS4wMTUgMS40MTUtLjcyOCAyLjE4LTEuNDc0IDEuNTE3LTMuOTc3IDIuNTEzLTUuODQ3IDIuMDE3LS44Mi0uMjItMS4yMzYtLjQ2NC0yLjM3OC0xLjI2N2wtLjA5NS0uMDY1Yy4wNDcuNTkzLjI2NCAxLjc0LjcxNyAzLjgwMi4yOTQgMS4zMzcgMi4wNzggOS4xOSAyLjYzNiAxMS42NzVsLjAwMy4wMTNjLjUxNyAyLjYzOC0xLjg4NCA0LjczMi01LjIzNCA0LjczMi0zLjI4NyAwLTYuMzYtMS45OTMtNi44Ny00LjU0LS41Mi0yLjY0IDEuODg0LTQuNzMgNS4yNC00LjczLjkwNSAwIDEuODAzLjE1IDIuNjUuNDM2eiIvPjwvZz48L3N2Zz4=';

/**
 * Icon svg to be displayed in the category menu, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const menuIconURI = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTE2LjA5IDEyLjkzN2MuMjI4IDEuMTQxLS44MzMgMi4wNjMtMi4zNzMgMi4wNjMtMS41MzUgMC0yLjk2Mi0uOTIyLTMuMTg2LTIuMDYzLS4yMy0xLjE0Mi44MzMtMi4wNjggMi4zNzItMi4wNjguMzIzIDAgLjY0MS4wNDIuOTQ1LjExN2EzLjUgMy41IDAgMCAxIC40NjguMTUxYy40MzUtLjAxLS4wNTItMS4xNDctLjkxNy02LjExNC0xLjA2Ny02LjE1MiAxLjUzLS45MzUgNC4zODQtMS4zNzcgMi44NTQtLjQ0Mi4wMzggMi40MS0xLjgyNSAxLjkyMi0xLjg2Mi0uNDkzLTIuMzI1LTMuNTc3LjEzMiA3LjM3ek03LjQ2IDguNTYzYy0xLjg2Mi0uNDkzLTIuMzI1LTMuNTc2LjEzIDcuMzdDNy44MTYgMTcuMDczIDYuNzU0IDE4IDUuMjIgMThjLTEuNTM1IDAtMi45NjEtLjkyNi0zLjE5LTIuMDY4LS4yMjQtMS4xNDIuODM3LTIuMDY3IDIuMzc1LTIuMDY3LjUwMSAwIC45ODcuMDk4IDEuNDI3LjI3Mi40MTItLjAyOC0uMDc0LTEuMTg5LS45My02LjExNEMzLjgzNCAxLjg3IDYuNDMgNy4wODcgOS4yODIgNi42NDZjMi44NTQtLjQ0Ny4wMzggMi40MS0xLjgyMyAxLjkxN3oiIGZpbGw9IiM1NzVFNzUiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjwvc3ZnPg==';

/**
 * Class for the music-related blocks in Scratch 3.0
 * @param {Runtime} runtime - the runtime instantiating this block package.
 * @constructor
 */
class Scratch3MusicBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }
    
    /**
     * Create data for a menu in scratch-blocks format, consisting of an array of objects with text and
     * value properties. The text is a translated string, and the value is one-indexed.
     * @param  {object[]} info - An array of info objects each having a name property.
     * @return {array} - An array of objects with text and value properties.
     * @private
     */
    _buildMenu (info) {
        return info.map((entry, index) => {
            const obj = {};
            obj.text = entry.name;
            obj.value = String(index + 1);
            return obj;
        });
    }

    /**
     * An array of info about each drum.
     * @type {object[]}
     * @param {string} name - the translatable name to display in the drums menu.
     * @param {string} fileName - the name of the audio file containing the drum sound.
     */
    get DRUM_INFO () {
        return [
            {
                name: formatMessage({
                    id: 'music.drumSnare',
                    default: '(1) Snare Drum',
                    description: 'Sound of snare drum as used in a standard drum kit'
                }),
                fileName: '1-snare'
            },
            {
                name: formatMessage({
                    id: 'music.drumBass',
                    default: '(2) Bass Drum',
                    description: 'Sound of bass drum as used in a standard drum kit'
                }),
                fileName: '2-bass-drum'
            },
            {
                name: formatMessage({
                    id: 'music.drumSideStick',
                    default: '(3) Side Stick',
                    description: 'Sound of a drum stick hitting the side of a drum (usually the snare)'
                }),
                fileName: '3-side-stick'
            },
            {
                name: formatMessage({
                    id: 'music.drumCrashCymbal',
                    default: '(4) Crash Cymbal',
                    description: 'Sound of a drum stick hitting a crash cymbal'
                }),
                fileName: '4-crash-cymbal'
            },
            {
                name: formatMessage({
                    id: 'music.drumOpenHiHat',
                    default: '(5) Open Hi-Hat',
                    description: 'Sound of a drum stick hitting a hi-hat while open'
                }),
                fileName: '5-open-hi-hat'
            },
            {
                name: formatMessage({
                    id: 'music.drumClosedHiHat',
                    default: '(6) Closed Hi-Hat',
                    description: 'Sound of a drum stick hitting a hi-hat while closed'
                }),
                fileName: '6-closed-hi-hat'
            },
            {
                name: formatMessage({
                    id: 'music.drumTambourine',
                    default: '(7) Tambourine',
                    description: 'Sound of a tambourine being struck'
                }),
                fileName: '7-tambourine'
            },
            {
                name: formatMessage({
                    id: 'music.drumHandClap',
                    default: '(8) Hand Clap',
                    description: 'Sound of two hands clapping together'
                }),
                fileName: '8-hand-clap'
            },
            {
                name: formatMessage({
                    id: 'music.drumClaves',
                    default: '(9) Claves',
                    description: 'Sound of claves being struck together'
                }),
                fileName: '9-claves'
            },
            {
                name: formatMessage({
                    id: 'music.drumWoodBlock',
                    default: '(10) Wood Block',
                    description: 'Sound of a wood block being struck'
                }),
                fileName: '10-wood-block'
            },
            {
                name: formatMessage({
                    id: 'music.drumCowbell',
                    default: '(11) Cowbell',
                    description: 'Sound of a cowbell being struck'
                }),
                fileName: '11-cowbell'
            },
            {
                name: formatMessage({
                    id: 'music.drumTriangle',
                    default: '(12) Triangle',
                    description: 'Sound of a triangle (instrument) being struck'
                }),
                fileName: '12-triangle'
            },
            {
                name: formatMessage({
                    id: 'music.drumBongo',
                    default: '(13) Bongo',
                    description: 'Sound of a bongo being struck'
                }),
                fileName: '13-bongo'
            },
            {
                name: formatMessage({
                    id: 'music.drumConga',
                    default: '(14) Conga',
                    description: 'Sound of a conga being struck'
                }),
                fileName: '14-conga'
            },
            {
                name: formatMessage({
                    id: 'music.drumCabasa',
                    default: '(15) Cabasa',
                    description: 'Sound of a cabasa being shaken'
                }),
                fileName: '15-cabasa'
            },
            {
                name: formatMessage({
                    id: 'music.drumGuiro',
                    default: '(16) Guiro',
                    description: 'Sound of a guiro being played'
                }),
                fileName: '16-guiro'
            },
            {
                name: formatMessage({
                    id: 'music.drumVibraslap',
                    default: '(17) Vibraslap',
                    description: 'Sound of a Vibraslap being played'
                }),
                fileName: '17-vibraslap'
            },
            {
                name: formatMessage({
                    id: 'music.drumCuica',
                    default: '(18) Cuica',
                    description: 'Sound of a cuica being played'
                }),
                fileName: '18-cuica'
            }
        ];
    }

    /**
     * An array of info about each instrument.
     * @type {object[]}
     * @param {string} name - the translatable name to display in the instruments menu.
     * @param {string} dirName - the name of the directory containing audio samples for this instrument.
     * @param {number} [releaseTime] - an optional duration for the release portion of each note.
     * @param {number[]} samples - an array of numbers representing the MIDI note number for each
     *                           sampled sound used to play this instrument.
     */
    get INSTRUMENT_INFO () {
        return [
            {
                name: formatMessage({
                    id: 'music.instrumentPiano',
                    default: '(1) Piano',
                    description: 'Sound of a piano'
                }),
                dirName: '1-piano',
                releaseTime: 0.5,
                samples: [24, 36, 48, 60, 72, 84, 96, 108]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentElectricPiano',
                    default: '(2) Electric Piano',
                    description: 'Sound of an electric piano'
                }),
                dirName: '2-electric-piano',
                releaseTime: 0.5,
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentOrgan',
                    default: '(3) Organ',
                    description: 'Sound of an organ'
                }),
                dirName: '3-organ',
                releaseTime: 0.5,
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentGuitar',
                    default: '(4) Guitar',
                    description: 'Sound of an accoustic guitar'
                }),
                dirName: '4-guitar',
                releaseTime: 0.5,
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentElectricGuitar',
                    default: '(5) Electric Guitar',
                    description: 'Sound of an electric guitar'
                }),
                dirName: '5-electric-guitar',
                releaseTime: 0.5,
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentBass',
                    default: '(6) Bass',
                    description: 'Sound of an accoustic upright bass'
                }),
                dirName: '6-bass',
                releaseTime: 0.25,
                samples: [36, 48]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentPizzicato',
                    default: '(7) Pizzicato',
                    description: 'Sound of a string instrument (e.g. violin) being plucked'
                }),
                dirName: '7-pizzicato',
                releaseTime: 0.25,
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentCello',
                    default: '(8) Cello',
                    description: 'Sound of a cello being played with a bow'
                }),
                dirName: '8-cello',
                releaseTime: 0.1,
                samples: [36, 48, 60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentTrombone',
                    default: '(9) Trombone',
                    description: 'Sound of a trombone being played'
                }),
                dirName: '9-trombone',
                samples: [36, 48, 60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentClarinet',
                    default: '(10) Clarinet',
                    description: 'Sound of a clarinet being played'
                }),
                dirName: '10-clarinet',
                samples: [48, 60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentSaxophone',
                    default: '(11) Saxophone',
                    description: 'Sound of a saxophone being played'
                }),
                dirName: '11-saxophone',
                samples: [36, 60, 84]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentFlute',
                    default: '(12) Flute',
                    description: 'Sound of a flute being played'
                }),
                dirName: '12-flute',
                samples: [60, 72]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentWoodenFlute',
                    default: '(13) Wooden Flute',
                    description: 'Sound of a wooden flute being played'
                }),
                dirName: '13-wooden-flute',
                samples: [60, 72]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentBassoon',
                    default: '(14) Bassoon',
                    description: 'Sound of a bassoon being played'
                }),
                dirName: '14-bassoon',
                samples: [36, 48, 60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentChoir',
                    default: '(15) Choir',
                    description: 'Sound of a choir singing'
                }),
                dirName: '15-choir',
                releaseTime: 0.25,
                samples: [48, 60, 72]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentVibraphone',
                    default: '(16) Vibraphone',
                    description: 'Sound of a vibraphone being struck'
                }),
                dirName: '16-vibraphone',
                releaseTime: 0.5,
                samples: [60, 72]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentMusicBox',
                    default: '(17) Music Box',
                    description: 'Sound of a music box playing'
                }),
                dirName: '17-music-box',
                releaseTime: 0.25,
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentSteelDrum',
                    default: '(18) Steel Drum',
                    description: 'Sound of a steel drum being struck'
                }),
                dirName: '18-steel-drum',
                releaseTime: 0.5,
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentMarimba',
                    default: '(19) Marimba',
                    description: 'Sound of a marimba being struck'
                }),
                dirName: '19-marimba',
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentSynthLead',
                    default: '(20) Synth Lead',
                    description: 'Sound of a "lead" synthesizer being played'
                }),
                dirName: '20-synth-lead',
                releaseTime: 0.1,
                samples: [60]
            },
            {
                name: formatMessage({
                    id: 'music.instrumentSynthPad',
                    default: '(21) Synth Pad',
                    description: 'Sound of a "pad" synthesizer being played'
                }),
                dirName: '21-synth-pad',
                releaseTime: 0.25,
                samples: [60]
            }
        ];
    }

    /**
     * An array that is a mapping from MIDI instrument numbers to Scratch instrument numbers.
     * @type {number[]}
     */
    get MIDI_INSTRUMENTS () {
        return [
            // Acoustic Grand, Bright Acoustic, Electric Grand, Honky-Tonk
            1, 1, 1, 1,
            // Electric Piano 1, Electric Piano 2, Harpsichord, Clavinet
            2, 2, 4, 4,
            // Celesta, Glockenspiel, Music Box, Vibraphone
            17, 17, 17, 16,
            // Marimba, Xylophone, Tubular Bells, Dulcimer
            19, 16, 17, 17,
            // Drawbar Organ, Percussive Organ, Rock Organ, Church Organ
            3, 3, 3, 3,
            // Reed Organ, Accordion, Harmonica, Tango Accordion
            3, 3, 3, 3,
            // Nylon String Guitar, Steel String Guitar, Electric Jazz Guitar, Electric Clean Guitar
            4, 4, 5, 5,
            // Electric Muted Guitar, Overdriven Guitar,Distortion Guitar, Guitar Harmonics
            5, 5, 5, 5,
            // Acoustic Bass, Electric Bass (finger), Electric Bass (pick), Fretless Bass
            6, 6, 6, 6,
            // Slap Bass 1, Slap Bass 2, Synth Bass 1, Synth Bass 2
            6, 6, 6, 6,
            // Violin, Viola, Cello, Contrabass
            8, 8, 8, 8,
            // Tremolo Strings, Pizzicato Strings, Orchestral Strings, Timpani
            8, 7, 8, 19,
            // String Ensemble 1, String Ensemble 2, SynthStrings 1, SynthStrings 2
            8, 8, 8, 8,
            // Choir Aahs, Voice Oohs, Synth Voice, Orchestra Hit
            15, 15, 15, 19,
            // Trumpet, Trombone, Tuba, Muted Trumpet
            9, 9, 9, 9,
            // French Horn, Brass Section, SynthBrass 1, SynthBrass 2
            9, 9, 9, 9,
            // Soprano Sax, Alto Sax, Tenor Sax, Baritone Sax
            11, 11, 11, 11,
            // Oboe, English Horn, Bassoon, Clarinet
            14, 14, 14, 10,
            // Piccolo, Flute, Recorder, Pan Flute
            12, 12, 13, 13,
            // Blown Bottle, Shakuhachi, Whistle, Ocarina
            13, 13, 12, 12,
            // Lead 1 (square), Lead 2 (sawtooth), Lead 3 (calliope), Lead 4 (chiff)
            20, 20, 20, 20,
            // Lead 5 (charang), Lead 6 (voice), Lead 7 (fifths), Lead 8 (bass+lead)
            20, 20, 20, 20,
            // Pad 1 (new age), Pad 2 (warm), Pad 3 (polysynth), Pad 4 (choir)
            21, 21, 21, 21,
            // Pad 5 (bowed), Pad 6 (metallic), Pad 7 (halo), Pad 8 (sweep)
            21, 21, 21, 21,
            // FX 1 (rain), FX 2 (soundtrack), FX 3 (crystal), FX 4 (atmosphere)
            21, 21, 21, 21,
            // FX 5 (brightness), FX 6 (goblins), FX 7 (echoes), FX 8 (sci-fi)
            21, 21, 21, 21,
            // Sitar, Banjo, Shamisen, Koto
            4, 4, 4, 4,
            // Kalimba, Bagpipe, Fiddle, Shanai
            17, 14, 8, 10,
            // Tinkle Bell, Agogo, Steel Drums, Woodblock
            17, 17, 18, 19,
            // Taiko Drum, Melodic Tom, Synth Drum, Reverse Cymbal
            1, 1, 1, 1,
            // Guitar Fret Noise, Breath Noise, Seashore, Bird Tweet
            21, 21, 21, 21,
            // Telephone Ring, Helicopter, Applause, Gunshot
            21, 21, 21, 21
        ];
    }

    /**
     * An array that is a mapping from MIDI drum numbers in range (35..81) to Scratch drum numbers.
     * It's in the format [drumNum, pitch, decay].
     * The pitch and decay properties are not currently being used.
     * @type {Array[]}
     */
    get MIDI_DRUMS () {
        return [
            [1, -4], // "BassDrum" in 2.0, "Bass Drum" in 3.0 (which was "Tom" in 2.0)
            [1, 0], // Same as just above
            [2, 0],
            [0, 0],
            [7, 0],
            [0, 2],
            [1, -6, 4],
            [5, 0],
            [1, -3, 3.2],
            [5, 0], // "HiHatPedal" in 2.0, "Closed Hi-Hat" in 3.0
            [1, 0, 3],
            [4, -8],
            [1, 4, 3],
            [1, 7, 2.7],
            [3, -8],
            [1, 10, 2.7],
            [4, -2],
            [3, -11],
            [4, 2],
            [6, 0],
            [3, 0, 3.5],
            [10, 0],
            [3, -8, 3.5],
            [16, -6],
            [4, 2],
            [12, 2],
            [12, 0],
            [13, 0, 0.2],
            [13, 0, 2],
            [13, -5, 2],
            [12, 12],
            [12, 5],
            [10, 19],
            [10, 12],
            [14, 0],
            [14, 0], // "Maracas" in 2.0, "Cabasa" in 3.0 (TODO: pitch up?)
            [17, 12],
            [17, 5],
            [15, 0], // "GuiroShort" in 2.0, "Guiro" in 3.0 (which was "GuiroLong" in 2.0) (TODO: decay?)
            [15, 0],
            [8, 0],
            [9, 0],
            [9, -4],
            [17, -5],
            [17, 0],
            [11, -6, 1],
            [11, -6, 3]
        ];
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'music',
            name: formatMessage({
                id: 'music.categoryName',
                default: 'Music',
                description: 'Label for the Music extension category'
            }),
            menuIconURI: menuIconURI,
            blockIconURI: blockIconURI,
            blocks: [
                {
                    opcode: 'playDrumForBeats',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'music.playDrumForBeats',
                        default: 'play drum [DRUM] for [BEATS] beats',
                        description: 'play drum sample for a number of beats'
                    }),
                    arguments: {
                        DRUM: {
                            type: ArgumentType.NUMBER,
                            menu: 'DRUM',
                            defaultValue: 1
                        },
                        BEATS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.25
                        }
                    }
                },
                {
                    opcode: 'midiPlayDrumForBeats',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'music.midiPlayDrumForBeats',
                        default: 'play drum [DRUM] for [BEATS] beats',
                        description: 'play drum sample for a number of beats according to a mapping of MIDI codes'
                    }),
                    arguments: {
                        DRUM: {
                            type: ArgumentType.NUMBER,
                            menu: 'DRUM',
                            defaultValue: 1
                        },
                        BEATS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.25
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'restForBeats',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'music.restForBeats',
                        default: 'rest for [BEATS] beats',
                        description: 'rest (play no sound) for a number of beats'
                    }),
                    arguments: {
                        BEATS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.25
                        }
                    }
                },
                {
                    opcode: 'playNoteForBeats',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'music.playNoteForBeats',
                        default: 'play note [NOTE] for [BEATS] beats',
                        description: 'play a note for a number of beats'
                    }),
                    arguments: {
                        NOTE: {
                            type: ArgumentType.NOTE,
                            defaultValue: 60
                        },
                        BEATS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 0.25
                        }
                    }
                },
                {
                    opcode: 'setInstrument',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'music.setInstrument',
                        default: 'set instrument to [INSTRUMENT]',
                        description: 'set the instrument (e.g. piano, guitar, trombone) for notes played'
                    }),
                    arguments: {
                        INSTRUMENT: {
                            type: ArgumentType.NUMBER,
                            menu: 'INSTRUMENT',
                            defaultValue: 1
                        }
                    }
                },
                {
                    opcode: 'midiSetInstrument',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'music.midiSetInstrument',
                        default: 'set instrument to [INSTRUMENT]',
                        description: 'set the instrument for notes played according to a mapping of MIDI codes'
                    }),
                    arguments: {
                        INSTRUMENT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    },
                    hideFromPalette: true
                },
                {
                    opcode: 'setTempo',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'music.setTempo',
                        default: 'set tempo to [TEMPO]',
                        description: 'set tempo (speed) for notes, drums, and rests played'
                    }),
                    arguments: {
                        TEMPO: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 60
                        }
                    }
                },
                {
                    opcode: 'changeTempo',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'music.changeTempo',
                        default: 'change tempo by [TEMPO]',
                        description: 'change tempo (speed) for notes, drums, and rests played'
                    }),
                    arguments: {
                        TEMPO: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 20
                        }
                    }
                },
                {
                    opcode: 'getTempo',
                    text: formatMessage({
                        id: 'music.getTempo',
                        default: 'tempo',
                        description: 'get the current tempo (speed) for notes, drums, and rests played'
                    }),
                    blockType: BlockType.REPORTER
                }
            ],
            menus: {
                DRUM: {
                    acceptReporters: true,
                    items: this._buildMenu(this.DRUM_INFO)
                },
                INSTRUMENT: {
                    acceptReporters: true,
                    items: this._buildMenu(this.INSTRUMENT_INFO)
                }
            }
        };
    }
}

module.exports = Scratch3MusicBlocks;
