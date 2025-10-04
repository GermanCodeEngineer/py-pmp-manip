// Simplified remake of an icon by True-Fantom
const icon = 'data:image/svg+xml,' + encodeURIComponent(`
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0,0,200,200">
      <circle r="100" cx="100" cy="100" fill="#9966ff"/>
      <path d="M122,61v-4a12,12 0,0,0 -12,-12h-4m-17,0h-16m-17,0h-4a12,12 0,0,0 -12,12v4m0,17v16m0,17v4a12,12 0,0,0 12,12h4" stroke="#ffffff" stroke-width="11" stroke-linecap="round" fill="none"/>
      <g fill="#ffffff" stroke="#9966ff" stroke-width="7.5">
        <circle r="32" cx="118" cy="102"/>
        <circle r="32" cx="96" cy="137"/>
        <circle r="32" cx="140" cy="137"/>
      </g>
    </svg>`);

class Extension {
    getInfo() {
        return {
            id: 'xeltallivclipblend',
            name: 'Clipping and Blending',
            color1: '#9966FF',
            color2: '#855CD6',
            color3: '#774DCB',
            menuIconURI: icon,
            blocks: [
                {
                    opcode: 'setClipbox',
                    blockType: Scratch.BlockType.COMMAND,
                    text: 'set clipping box x1:[X1] y1:[Y1] x2:[X2] y2:[Y2]',
                    arguments: {
                        X1: {
                            type: Scratch.ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        Y1: {
                            type: Scratch.ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
                        X2: {
                            type: Scratch.ArgumentType.NUMBER,
                            defaultValue: '100'
                        },
                        Y2: {
                            type: Scratch.ArgumentType.NUMBER,
                            defaultValue: '100'
                        }
                    },
                    filter: [Scratch.TargetType.SPRITE]
                },
                {
                    opcode: 'clearClipbox',
                    blockType: Scratch.BlockType.COMMAND,
                    text: 'clear clipping box',
                    filter: [Scratch.TargetType.SPRITE]
                },
                {
                    opcode: 'getClipbox',
                    blockType: Scratch.BlockType.REPORTER,
                    text: 'clipping box [PROP]',
                    arguments: {
                        PROP: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'width',
                            menu: 'props'
                        }
                    },
                    filter: [Scratch.TargetType.SPRITE]
                },
                '---',
                {
                    opcode: 'setBlend',
                    blockType: Scratch.BlockType.COMMAND,
                    text: 'use [BLENDMODE] blending ',
                    arguments: {
                        BLENDMODE: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'default',
                            menu: 'blends'
                        }
                    },
                    filter: [Scratch.TargetType.SPRITE]
                },
                {
                    opcode: 'getBlend',
                    blockType: Scratch.BlockType.REPORTER,
                    text: 'blending',
                    filter: [Scratch.TargetType.SPRITE],
                    disableMonitor: true
                },
                '---',
                {
                    opcode: 'setAdditiveBlend',
                    blockType: Scratch.BlockType.COMMAND,
                    text: 'turn additive blending [STATE]',
                    arguments: {
                        STATE: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'on',
                            menu: 'states'
                        }
                    },
                    filter: [Scratch.TargetType.SPRITE],
                    hideFromPalette: true
                },
                {
                    opcode: 'getAdditiveBlend',
                    blockType: Scratch.BlockType.BOOLEAN,
                    text: 'is additive blending on?',
                    filter: [Scratch.TargetType.SPRITE],
                    hideFromPalette: true
                },
            ],
            menus: {
                states: {
                    acceptReporters: true,
                    items: ['on', 'off']
                },
                blends: {
                    acceptReporters: true,
                    items: ['default', 'additive', 'subtract', 'multiply', 'invert']
                },
                props: {
                    acceptReporters: true,
                    items: ['width', 'height', 'min x', 'min y', 'max x', 'max y']
                },
            }
        };
    }
}

module.exports = Extension