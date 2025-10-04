const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

class JgScriptsBlocks {
  /**
   * Class for Script blocks
   * @constructor
   */
  constructor(runtime) {
    /**
     * The runtime instantiating this block package.
     * @type {Runtime}
     */
    this.runtime = runtime;
  }
  /**
   * @returns {object} metadata for this extension and its blocks.
  */
  getInfo() {
    return {
      id: "jgScripts",
      name: "Scripts",
      color1: "#8c8c8c",
      color2: "#7a7a7a",
      blocks: [
        {
          opcode: "createScript",
          blockType: BlockType.COMMAND,
          text: "create script named [NAME]",
          arguments: {
            NAME: { type: ArgumentType.STRING, defaultValue: "Script1" }
          },
        },
        {
          opcode: "deleteScript",
          blockType: BlockType.COMMAND,
          text: "delete script named [NAME]",
          arguments: {
            NAME: { type: ArgumentType.STRING, defaultValue: "Script1" }
          },
        },
        {
          opcode: "deleteAll",
          blockType: BlockType.COMMAND,
          text: "delete all scripts"
        },
        {
          opcode: "allScripts",
          blockType: BlockType.REPORTER,
          text: "all scripts"
        },
        {
          opcode: "scriptExists",
          blockType: BlockType.BOOLEAN,
          text: "script named [NAME] exists?",
          arguments: {
            NAME: { type: ArgumentType.STRING, defaultValue: "Script1" }
          },
        },
        "---",
        {
          opcode: "addBlocksTo",
          blockType: BlockType.COMMAND,
          text: ["add blocks", "to script [NAME]"],
          branchCount: 1,
          arguments: {
            NAME: { type: ArgumentType.STRING, defaultValue: "Script1" }
          },
        },
        {
          opcode: "JGreturn",
          text: "return [THING]",
          blockType: BlockType.COMMAND,
          isTerminal: true,
          arguments: {
            THING: { type: ArgumentType.STRING, defaultValue: "1" }
          },
        },
        "---",
        {
          opcode: "scriptData",
          text: "script data",
          blockType: BlockType.REPORTER,
          allowDropAnywhere: true,
          disableMonitor: true
        },
        "---",
        {
          opcode: "runBlocks",
          text: "run script [NAME] in [SPRITE]",
          blockType: BlockType.CONDITIONAL,
          branchCount: -1,
          arguments: {
            NAME: { type: ArgumentType.STRING, defaultValue: "Script1" },
            SPRITE: { type: ArgumentType.STRING, menu: "TARGETS" }
          },
        },
        {
          opcode: "runBlocksData",
          text: "run script [NAME] in [SPRITE] with data [DATA]",
          blockType: BlockType.CONDITIONAL,
          branchCount: -1,
          arguments: {
            NAME: { type: ArgumentType.STRING, defaultValue: "Script1" },
            SPRITE: { type: ArgumentType.STRING, menu: "TARGETS" },
            DATA: { type: ArgumentType.STRING, defaultValue: "data" }
          },
        },
        "---",
        {
          opcode: "reportBlocks",
          text: "run script [NAME] in [SPRITE]",
          blockType: BlockType.REPORTER,
          allowDropAnywhere: true,
          arguments: {
            NAME: { type: ArgumentType.STRING, defaultValue: "Script1" },
            SPRITE: { type: ArgumentType.STRING, menu: "TARGETS" }
          },
        },
        {
          opcode: "reportBlocksData",
          text: "run script [NAME] in [SPRITE] with data [DATA]",
          blockType: BlockType.REPORTER,
          allowDropAnywhere: true,
          arguments: {
            NAME: { type: ArgumentType.STRING, defaultValue: "Script1" },
            SPRITE: { type: ArgumentType.STRING, menu: "TARGETS" },
            DATA: { type: ArgumentType.STRING, defaultValue: "data" }
          },
        }
      ],
      menus: {
        TARGETS: { acceptReporters: true, items: "getTargets" }
      },
    };
  }
}

module.exports = JgScriptsBlocks;
