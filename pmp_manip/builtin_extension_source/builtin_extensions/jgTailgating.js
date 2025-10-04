const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

class TailgatingExtension {
  constructor(runtime) {
    /**
     * The runtime instantiating this block package.
     * @type {Runtime}
     */
    this.runtime = runtime;
  }

  getInfo() {
    return {
      id: "jgTailgating",
      name: "Tailgating",
      blocks: [
        {
          opcode: "startTrackingSprite",
          blockType: BlockType.COMMAND,
          text: "start tracking [SPRITE] as [NAME]",
          arguments: {
            SPRITE: {
              type: ArgumentType.STRING,
              menu: "spriteMenu",
            },
            NAME: {
              type: ArgumentType.STRING,
              defaultValue: "leader",
            }
          },
        },
        {
          opcode: "stopTrackingSprite",
          blockType: BlockType.COMMAND,
          text: "stop tracking [NAME]",
          arguments: {
            NAME: {
              type: ArgumentType.STRING,
              defaultValue: "leader",
            }
          },
        },
        '---',
        {
          opcode: "followSprite",
          blockType: BlockType.COMMAND,
          text: "follow [INDEX] positions behind [NAME]",
          arguments: {
            INDEX: {
              type: ArgumentType.NUMBER,
              defaultValue: 20,
            },
            NAME: {
              type: ArgumentType.STRING,
              defaultValue: "leader",
            }
          },
        },
        {
          opcode: "savePositionsBehindSprite",
          blockType: BlockType.COMMAND,
          text: "set max saved positions behind [NAME] to [MAX]",
          arguments: {
            MAX: {
              type: ArgumentType.NUMBER,
              defaultValue: 20,
            },
            NAME: {
              type: ArgumentType.STRING,
              defaultValue: "leader",
            }
          },
        },
        {
          opcode: "getSpriteFollowPos",
          blockType: BlockType.REPORTER,
          disableMonitor: true,
          text: "get position [INDEX] behind [NAME]",
          arguments: {
            INDEX: {
              type: ArgumentType.NUMBER,
              defaultValue: 20,
            },
            NAME: {
              type: ArgumentType.STRING,
              defaultValue: "leader",
            }
          },
        },
      ],
      menus: {
        spriteMenu: '_getSpriteMenu'
      },
    };
  }
}

module.exports = TailgatingExtension;