const BlockType = require("../../extension-support/block-type");
const BlockShape = require("../../extension-support/block-shape");
const ArgumentType = require("../../extension-support/argument-type");

let isScratchBlocksReady = typeof ScratchBlocks === "object";

// we cant have nice things
const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

class SPjavascriptV2 {
  constructor(runtime) {
    this.runtime = runtime;
  }
  getInfo() {
    return {
      id: "SPjavascriptV2",
      name: "JavaScript V2",
      color1: "#f7df1e",
      blockText: "#323330",
      blocks: [
        {
          opcode: "toggleSandbox",
          text: this.isEditorUnsandboxed ? "Run Sandboxed" : "Run Unsandboxed",
          blockType: BlockType.BUTTON,
        },
        {
          opcode: "codeInput",
          text: "[CODE]",
          blockType: BlockType.REPORTER,
          blockShape: BlockShape.SQUARE,
          hideFromPalette: true,
          arguments: {
            CODE: {
              type: ArgumentType.CUSTOM, id: "SPjavascriptV2-codeEditor",
              defaultValue: "needsInit-1@#4%^7*(0"
            }
          },
        },
        {
          opcode: "argumentReport",
          text: "data",
          blockType: BlockType.REPORTER,
          hideFromPalette: true,
          canDragDuplicate: true,
          disableMonitor: true,
        },
        {
          opcode: "returnData",
          blockType: BlockType.COMMAND,
          isTerminal: true,
          hideFromPalette: true,
          text: "return [DATA]",
          arguments: {
            DATA: { type: ArgumentType.STRING }
          },
        },
        /* shown if ScratchBlocks is not availiable */
        {
          opcode: "jsCommand",
          text: "run [CODE]",
          blockType: BlockType.COMMAND,
          hideFromPalette: isScratchBlocksReady && !isSafari,
          arguments: {
            CODE: { type: ArgumentType.STRING, defaultValue: `alert("Hello!")` }
          }
        },
        {
          opcode: "jsReporter",
          text: "run [CODE]",
          blockType: BlockType.REPORTER,
          disableMonitor: true,
          allowDropAnywhere: true,
          hideFromPalette: isScratchBlocksReady && !isSafari,
          arguments: {
            CODE: {
              type: ArgumentType.STRING,
              defaultValue: "Math.random()"
            }
          }
        },
        {
          opcode: "jsBoolean",
          text: "run [CODE]",
          blockType: BlockType.BOOLEAN,
          disableMonitor: true,
          hideFromPalette: isScratchBlocksReady && !isSafari,
          arguments: {
            CODE: {
              type: ArgumentType.STRING,
              defaultValue: "Math.round(Math.random()) === 1"
            }
          }
        },
        /* shown if ScratchBlocks is availiable */
        {
          opcode: "jsCommandBinded",
          text: "run [CODE] with data [ARGS]",
          blockType: BlockType.COMMAND,
          hideFromPalette: isSafari || !isScratchBlocksReady,
          arguments: {
            CODE: { fillIn: "codeInput" },
            ARGS: {
              type: ArgumentType.STRING,
              defaultValue: `{ "FOO": "bar" }`,
              exemptFromNormalization: true
            }
          }
        },
        {
          opcode: "jsReporterBinded",
          text: "run [CODE] with data [ARGS]",
          blockType: BlockType.REPORTER,
          disableMonitor: true,
          allowDropAnywhere: true,
          hideFromPalette: isSafari || !isScratchBlocksReady,
          arguments: {
            CODE: { fillIn: "codeInput" },
            ARGS: {
              type: ArgumentType.STRING,
              defaultValue: `{ "STRING": "output: " }`,
              exemptFromNormalization: true
            }
          }
        },
        {
          opcode: "jsBooleanBinded",
          text: "run [CODE] with data [ARGS]",
          blockType: BlockType.BOOLEAN,
          disableMonitor: true,
          hideFromPalette: isSafari || !isScratchBlocksReady,
          arguments: {
            CODE: { fillIn: "codeInput" },
            ARGS: {
              type: ArgumentType.STRING,
              defaultValue: `{ "THRESHOLD": 0.5 }`,
              exemptFromNormalization: true
            }
          }
        },
        ...(isScratchBlocksReady ? ["---"] : []),
        {
          opcode: "defineGlobalFunc",
          text: "create global function named [NAME] with code [CODE]",
          blockType: BlockType.COMMAND,
          hideFromPalette: (isSafari || !isScratchBlocksReady) && !this.isEditorUnsandboxed,
          arguments: {
            NAME: {
              type: ArgumentType.STRING, defaultValue: "myFunction"
            },
            CODE: { fillIn: "codeInput" }
          }
        },
        {
          opcode: "defineScratchCode",
          text: "create local function named [NAME] with code [CODE]",
          blockType: BlockType.CONDITIONAL,
          hideFromPalette: true,
          arguments: {
            NAME: { type: ArgumentType.STRING },
            CODE: { fillIn: "argumentReport" }
          }
        },
        {
          opcode: "deleteGlobalFunc",
          text: "delete global function [NAME]",
          blockType: BlockType.COMMAND,
          hideFromPalette: !isScratchBlocksReady && !this.isEditorUnsandboxed,
          arguments: {
            NAME: {
              type: ArgumentType.STRING, defaultValue: "myFunction"
            }
          }
        },
        {
          opcode: "packagerInfo",
          text: "Sandbox in Packager Notice",
          blockType: BlockType.BUTTON,
          hideFromPalette: !this.isEditorUnsandboxed
        }
      ]
    };
  }
}

module.exports = SPjavascriptV2;
