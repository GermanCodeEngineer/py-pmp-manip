const BlockType = require("../../extension-support/block-type");
const ArgumentType = require("../../extension-support/argument-type");

const joinWords = [
  "apple", "banana", "pear",
  "orange", "mango", "strawberry",
  "pineapple", "grape", "kiwi"
];

function generateJoin(amount) {
  const argumentTextArray = [];
  const argumentss = {};
  for (let i = 0; i < amount; i++) {
    argumentTextArray.push(`[STRING${i + 1}]`);
    argumentss[`STRING${i + 1}`] = {
      type: ArgumentType.STRING,
      defaultValue: joinWords[i] + ((i === (amount - 1)) ? "" : " ")
    };
  }

  const opcode = `join${amount}`;
  return {
    opcode: opcode,
    text: translate({
      id: opcode,
      default: `join ${argumentTextArray.join(" ")}`
    }),
    blockType: BlockType.REPORTER,
    hideFromPalette: true,
    disableMonitor: true,
    arguments: argumentss
  };
}
function initMegaJoins(amount) {
  const joins = [];
  for (let i = 3; i < amount; i++) joins.push(generateJoin(i + 1));

  return joins.map((e, index) => {
    const switches = [];
    for (let i = 3; i < amount; i++) {
      if (i == index + 3) {
        switches.push({ isNoop: true });
        continue;
      }
      switches.push(`join${i + 1}`);
    }
    e["switchText"] = `join x${index + 4}`;
    e["switches"] = switches;
    return e;
  });
}

function generateJoinList(shown) {
  if (!shown) return "";

  let xml = "";
  for (let i = 2; i < 9; i++) {
    if (i === 2) xml += `<block type="operator_join">`;
    else if (i === 3) xml += `<block type="operator_join3">`;
    else xml += `<block type="pmOperatorsExpansion_join${i}">`;
    for (let j = 1; j <= i; j++) {
      xml += `<value name="STRING${j}">`;
      xml += `<shadow type="text"><field name="TEXT">${(joinWords[j - 1] ?? "...") + " "}</field></shadow>`;
      xml += `</value>`;
    }
    xml += `</block>`;
  }

  return xml;
}

/**
 * Operators Expansion Class
 * @constructor
 */
class pmOperatorsExpansion {
  /**
   * @returns {object} metadata for this extension and its blocks.
   */
  getInfo() {
    return {
      id: "pmOperatorsExpansion",
      name: "Operators Expansion",
      color1: "#59C059",
      color2: "#46B946",
      color3: "#389438",
      blocks: [
        {
          opcode: "shiftLeft",
          text: "[num1] << [num2]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            num1: {
              type: ArgumentType.NUMBER,
              defaultValue: 1
            },
            num2: {
              type: ArgumentType.NUMBER,
              defaultValue: 5
            }
          },
          switches: [
            { isNoop: true },
            "shiftRight",
            "binnaryAnd",
            "binnaryOr",
            "binnaryXor",
            "binnaryNot",
          ],
          switchText: "lshift"
        },
        {
          opcode: "shiftRight",
          text: "[num1] >> [num2]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            num1: {
              type: ArgumentType.NUMBER,
              defaultValue: 32
            },
            num2: {
              type: ArgumentType.NUMBER,
              defaultValue: 5
            }
          },
          switches: [
            { isNoop: true },
            "shiftLeft",
            "binnaryAnd",
            "binnaryOr",
            "binnaryXor",
            "binnaryNot",
          ],
          switchText: "rshift"
        },
        {
          opcode: "binnaryAnd",
          text: "[num1] & [num2]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            num1: {
              type: ArgumentType.NUMBER,
              defaultValue: 32
            },
            num2: {
              type: ArgumentType.NUMBER,
              defaultValue: 5
            }
          },
          switches: [
            { isNoop: true },
            "shiftLeft",
            "shiftRight",
            "binnaryOr",
            "binnaryXor",
            "binnaryNot",
          ],
          switchText: "and"
        },
        {
          opcode: "binnaryOr",
          text: "[num1] | [num2]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            num1: {
              type: ArgumentType.NUMBER,
              defaultValue: 7
            },
            num2: {
              type: ArgumentType.NUMBER,
              defaultValue: 8
            }
          },
          switches: [
            { isNoop: true },
            "shiftLeft",
            "shiftRight",
            "binnaryAnd",
            "binnaryXor",
            "binnaryNot",
          ],
          switchText: "or"
        },
        {
          opcode: "binnaryXor",
          text: "[num1] ^ [num2]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            num1: {
              type: ArgumentType.NUMBER,
              defaultValue: 7
            },
            num2: {
              type: ArgumentType.NUMBER,
              defaultValue: 2
            }
          },
          switches: [
            { isNoop: true },
            "shiftLeft",
            "shiftRight",
            "binnaryAnd",
            "binnaryOr",
            "binnaryNot",
          ],
          switchText: "xor"
        },
        {
          opcode: "binnaryNot",
          text: "~ [num1]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            num1: {
              type: ArgumentType.NUMBER,
              defaultValue: 2
            }
          },
          switches: [
            { isNoop: true },
            "shiftLeft",
            "shiftRight",
            "binnaryAnd",
            "binnaryOr",
            "binnaryXor",
          ],
          switchText: "not"
        },
        "---",
        {
          opcode: "orIfFalsey",
          text: "[ONE] or else [TWO]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          allowDropAnywhere: true,
          disableMonitor: true,
          arguments: {
            ONE: {
              type: ArgumentType.STRING,
              defaultValue: "a"
            },
            TWO: {
              type: ArgumentType.STRING,
              defaultValue: "b"
            }
          }
        },
        {
          opcode: "ifIsTruthy",
          text: "if [ONE] is true then [TWO]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          allowDropAnywhere: true,
          disableMonitor: true,
          arguments: {
            ONE: {
              type: ArgumentType.BOOLEAN
            },
            TWO: {
              type: ArgumentType.STRING,
              defaultValue: "perfect!"
            }
          }
        },
        "---",
        {
            opcode: 'operator_nand',
            ppm_final_opcode: true,
            text: '[OPERAND1] nand [OPERAND2]',
            blockType: BlockType.BOOLEAN,
            arguments: {
                OPERAND1: {type: ArgumentType.BOOLEAN},
                OPERAND2: {type: ArgumentType.BOOLEAN},
            }
        },
        {
            opcode: 'operator_nor',
            ppm_final_opcode: true,
            text: '[OPERAND1] nor [OPERAND2]',
            blockType: BlockType.BOOLEAN,
            arguments: {
                OPERAND1: {type: ArgumentType.BOOLEAN},
                OPERAND2: {type: ArgumentType.BOOLEAN},
            }
        },
        {
            opcode: 'operator_xor',
            ppm_final_opcode: true,
            text: '[OPERAND1] xor [OPERAND2]',
            blockType: BlockType.BOOLEAN,
            arguments: {
                OPERAND1: {type: ArgumentType.BOOLEAN},
                OPERAND2: {type: ArgumentType.BOOLEAN},
            }
        },
        {
            opcode: 'operator_xnor',
            ppm_final_opcode: true,
            text: '[OPERAND1] xnor [OPERAND2]',
            blockType: BlockType.BOOLEAN,
            arguments: {
                OPERAND1: {type: ArgumentType.BOOLEAN},
                OPERAND2: {type: ArgumentType.BOOLEAN},
            }
        },
        {
            opcode: 'operator_randomBoolean',
            ppm_final_opcode: true,
            text: 'random',
            blockType: BlockType.BOOLEAN,
        },
        "---",
        {
          opcode: "isNumberMultipleOf",
          text: "is [NUM] multiple of [MULTIPLE]?",
          blockType: BlockType.BOOLEAN,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            NUM: {
              type: ArgumentType.NUMBER,
              defaultValue: 20
            },
            MULTIPLE: {
              type: ArgumentType.NUMBER,
              defaultValue: 10
            }
          },
          switches: [
            { isNoop: true },
            "isInteger",
            "isPrime",
            "isEven"
          ],
          switchText: "is multiple of?"
        },
        {
          opcode: "isInteger",
          text: "is [NUM] an integer?",
          blockType: BlockType.BOOLEAN,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            NUM: {
              type: ArgumentType.NUMBER,
              defaultValue: 0.5
            }
          },
          switches: [
            { isNoop: true },
            "isNumberMultipleOf",
            "isPrime",
            "isEven"
          ],
          switchText: "is integer?"
        },
        {
          opcode: "isPrime",
          text: "is [NUM] a prime number?",
          blockType: BlockType.BOOLEAN,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            NUM: {
              type: ArgumentType.NUMBER,
              defaultValue: 13
            }
          },
          switches: [
            { isNoop: true },
            "isNumberMultipleOf",
            "isInteger",
            "isEven"
          ],
          switchText: "is prime?"
        },
        {
          opcode: "isEven",
          text: "is [NUM] even?",
          blockType: BlockType.BOOLEAN,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            NUM: {
              type: ArgumentType.NUMBER,
              defaultValue: 4
            }
          },
          switches: [
            { isNoop: true },
            "isNumberMultipleOf",
            "isInteger",
            "isPrime",
          ],
          switchText: "is even?"
        },
        {
          opcode: "betweenNumbers",
          text: "is [NUM] between [MIN] and [MAX]?",
          blockType: BlockType.BOOLEAN,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            NUM: {
              type: ArgumentType.NUMBER,
              defaultValue: 5
            },
            MIN: {
              type: ArgumentType.NUMBER,
              defaultValue: 0
            },
            MAX: {
              type: ArgumentType.NUMBER,
              defaultValue: 10
            }
          }
        },
        "---",
        {
          opcode: "evaluateMath",
          text: "answer to [EQUATION]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            EQUATION: {
              type: ArgumentType.STRING,
              defaultValue: "5 * 2"
            }
          }
        },
        {
          opcode: "partOfRatio",
          text: "[PART] part of ratio [RATIO]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            PART: {
              type: ArgumentType.STRING,
              menu: "part"
            },
            RATIO: {
              type: ArgumentType.STRING,
              defaultValue: "1:2"
            }
          },
          switches: [
            { isNoop: true },
            "simplifyRatio"
          ],
          switchText: "part of ratio"
        },
        {
          opcode: "simplifyRatio",
          text: "simplify ratio [RATIO]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            RATIO: {
              type: ArgumentType.STRING,
              defaultValue: "1:2"
            }
          },
          switches: [
            { isNoop: true },
            "partOfRatio",
          ],
          switchText: "simplify ratio"
        },
        {
          opcode: "pi",
          text: "π",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          switches: [
            { isNoop: true },
            "euler",
            "infinity"
          ]
        },
        {
          opcode: "euler",
          text: "e",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          switches: [
            { isNoop: true },
            "pi",
            "infinity"
          ]
        },
        {
          opcode: "infinity",
          text: "∞",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          switches: [
            { isNoop: true },
            "pi",
            "euler",
          ]
        },
        {
          opcode: "truncateNumber",
          text: "truncate number [NUM]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            NUM: {
              type: ArgumentType.NUMBER,
              defaultValue: 2.5
            }
          }
        },
        {
          opcode: "atan2",
          text: "atan2 of x [X] y [Y]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          arguments: {
            X: {
              type: ArgumentType.NUMBER,
              defaultValue: 45
            },
            Y: {
              type: ArgumentType.NUMBER,
              defaultValue: 90
            },
          }
        },
        "---",
        {
            opcode: 'operator_countAppearTimes',
            ppm_final_opcode: true,
            text: 'amount of times [TEXT1] appears in [TEXT2]',
            blockType: BlockType.REPORTER,
            arguments: {
                TEXT1: {
                    type: ArgumentType.STRING,
                    defaultValue: "a",
                },
                TEXT2: {
                    type: ArgumentType.STRING,
                    defaultValue: "abc abc abc",
                },
            },
        },
        {
            opcode: 'operator_readLineInMultilineText',
            ppm_final_opcode: true,
            text: 'read line [LINE] in [TEXT]',
            blockType: BlockType.REPORTER,
            arguments: {
                LINE: {
                    type: ArgumentType.STRING,
                    defaultValue: "1",
                },
                TEXT: {
                    type: ArgumentType.STRING,
                    defaultValue: "Text with multiple lines here",
                },
            },
        },
        {
            opcode: 'operator_textIncludesLetterFrom',
            ppm_final_opcode: true,
            text: '[TEXT1] includes a letter from [TEXT2] ?',
            blockType: BlockType.BOOLEAN,
            arguments: {
                TEXT1: {
                    type: ArgumentType.STRING,
                    defaultValue: "abcdef",
                },
                TEXT2: {
                    type: ArgumentType.STRING,
                    defaultValue: "fgh",
                },
            },
        },
        {
          opcode: "reverseChars",
          text: "reverse [TEXT]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            TEXT: {
              type: ArgumentType.STRING,
              defaultValue: "Hello!"
            }
          },
          switches: [
            { isNoop: true },
            "shuffleChars"
          ],
          switchText: "reverse text"
        },
        {
          opcode: "shuffleChars",
          text: "shuffle [TEXT]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            TEXT: {
              type: ArgumentType.STRING,
              defaultValue: "Hello!"
            }
          },
          switches: [
            { isNoop: true },
            "reverseChars",
          ],
          switchText: "shuffle text"
        },
        {
          opcode: "textAfter",
          text: "text after [TEXT] in [BASE]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            TEXT: {
              type: ArgumentType.STRING,
              defaultValue: "Hello"
            },
            BASE: {
              type: ArgumentType.STRING,
              defaultValue: "Hello world!"
            }
          },
          switches: [
            { isNoop: true },
            "textBefore"
          ],
          switchText: "text after"
        },
        {
          opcode: "textBefore",
          text: "text before [TEXT] in [BASE]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            TEXT: {
              type: ArgumentType.STRING,
              defaultValue: "world"
            },
            BASE: {
              type: ArgumentType.STRING,
              defaultValue: "Hello world!"
            }
          },
          switches: [
            { isNoop: true },
            "textAfter",
          ],
          switchText: "text before"
        },
        "---",
        {
          opcode: "exactlyEqual",
          text: "[ONE] exactly equals [TWO]?",
          blockType: BlockType.BOOLEAN,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            ONE: {
              type: ArgumentType.STRING,
              defaultValue: "a"
            },
            TWO: {
              type: ArgumentType.STRING,
              defaultValue: "b"
            }
          },
        },
        {
            opcode: 'operator_character_to_code',
            ppm_final_opcode: true,
            text: 'character [ONE] to id',
            blockType: BlockType.REPORTER,
            arguments: {
                ONE: {
                    type: ArgumentType.STRING,
                    defaultValue: "a",
                },
            },
        },
        {
            opcode: 'operator_code_to_character',
            ppm_final_opcode: true,
            text: 'id [ONE] to character',
            blockType: BlockType.REPORTER,
            arguments: {
                ONE: {
                    type: ArgumentType.STRING,
                    defaultValue: "97",
                },
            },
        },
        "---",
        {
          opcode: "setReplacer",
          text: "set replacer [REPLACER] to [TEXT]",
          blockType: BlockType.COMMAND,
          extensions: ["colours_operators"],
          arguments: {
            REPLACER: {
              type: ArgumentType.STRING,
              defaultValue: "${replacer}"
            },
            TEXT: {
              type: ArgumentType.STRING,
              defaultValue: "world"
            }
          },
          switches: [
            { isNoop: true },
            "resetReplacers"
          ],
          switchText: "set replacer"
        },
        {
          opcode: "resetReplacers",
          text: "reset replacers",
          blockType: BlockType.COMMAND,
          extensions: ["colours_operators"],
          switches: [
            { isNoop: true },
            "setReplacer",
          ],
          switchText: "reset replacers"
        },
        {
          opcode: "applyReplacers",
          text: "apply replacers to [TEXT]",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            TEXT: {
              type: ArgumentType.STRING,
              defaultValue: "Hello ${replacer}!"
            }
          }
        },
        "---",
        {
          opcode: "speedToPitch",
          text: "speed [SPEED] to pitch",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            SPEED: {
              type: ArgumentType.NUMBER,
              defaultValue: 2
            },
          },
          switches: [
            { isNoop: true },
            {
              opcode: "pitchToSpeed",
              remapArguments: {
                SPEED: "PITCH"
              }
            }
          ],
          switchText: "speed to pitch"
        },
        {
          opcode: "pitchToSpeed",
          text: "pitch [PITCH] to speed",
          blockType: BlockType.REPORTER,
          extensions: ["colours_operators"],
          disableMonitor: true,
          arguments: {
            PITCH: {
              type: ArgumentType.NUMBER,
              defaultValue: 120
            },
          },
          switches: [
            { isNoop: true },
            {
              opcode: "speedToPitch",
              remapArguments: {
                PITCH: "SPEED"
              }
            },
          ],
          switchText: "pitch to speed"
        },
        "---",
        {
          func: "toggleJoinVisibility",
          blockType: BlockType.BUTTON,
          text: this.showJoins ? "Hide Old Join Blocks" : "Show Old Join Blocks"
        },
        //...initMegaJoins(9), // replacement below:
        {
          "opcode": "join4",
          "text": "join [STRING1] [STRING2] [STRING3] [STRING4]",
          "hideFromPalette": true,
          "disableMonitor": true,
          "arguments": {
            "STRING1": {
              "defaultValue": "apple "
            },
            "STRING2": {
              "defaultValue": "banana "
            },
            "STRING3": {
              "defaultValue": "pear "
            },
            "STRING4": {
              "defaultValue": "orange"
            }
          },
          "switchText": "join x4",
          "switches": [
            {
              "isNoop": true
            },
            "join5",
            "join6",
            "join7",
            "join8",
            "join9"
          ]
        },
        {
          "opcode": "join5",
          "text": "join [STRING1] [STRING2] [STRING3] [STRING4] [STRING5]",
          "hideFromPalette": true,
          "disableMonitor": true,
          "arguments": {
            "STRING1": {
              "defaultValue": "apple "
            },
            "STRING2": {
              "defaultValue": "banana "
            },
            "STRING3": {
              "defaultValue": "pear "
            },
            "STRING4": {
              "defaultValue": "orange "
            },
            "STRING5": {
              "defaultValue": "mango"
            }
          },
          "switchText": "join x5",
          "switches": [
            "join4",
            {
              "isNoop": true
            },
            "join6",
            "join7",
            "join8",
            "join9"
          ]
        },
        {
          "opcode": "join6",
          "text": "join [STRING1] [STRING2] [STRING3] [STRING4] [STRING5] [STRING6]",
          "hideFromPalette": true,
          "disableMonitor": true,
          "arguments": {
            "STRING1": {
              "defaultValue": "apple "
            },
            "STRING2": {
              "defaultValue": "banana "
            },
            "STRING3": {
              "defaultValue": "pear "
            },
            "STRING4": {
              "defaultValue": "orange "
            },
            "STRING5": {
              "defaultValue": "mango "
            },
            "STRING6": {
              "defaultValue": "strawberry"
            }
          },
          "switchText": "join x6",
          "switches": [
            "join4",
            "join5",
            {
              "isNoop": true
            },
            "join7",
            "join8",
            "join9"
          ]
        },
        {
          "opcode": "join7",
          "text": "join [STRING1] [STRING2] [STRING3] [STRING4] [STRING5] [STRING6] [STRING7]",
          "hideFromPalette": true,
          "disableMonitor": true,
          "arguments": {
            "STRING1": {
              "defaultValue": "apple "
            },
            "STRING2": {
              "defaultValue": "banana "
            },
            "STRING3": {
              "defaultValue": "pear "
            },
            "STRING4": {
              "defaultValue": "orange "
            },
            "STRING5": {
              "defaultValue": "mango "
            },
            "STRING6": {
              "defaultValue": "strawberry "
            },
            "STRING7": {
              "defaultValue": "pineapple"
            }
          },
          "switchText": "join x7",
          "switches": [
            "join4",
            "join5",
            "join6",
            {
              "isNoop": true
            },
            "join8",
            "join9"
          ]
        },
        {
          "opcode": "join8",
          "text": "join [STRING1] [STRING2] [STRING3] [STRING4] [STRING5] [STRING6] [STRING7] [STRING8]",
          "hideFromPalette": true,
          "disableMonitor": true,
          "arguments": {
            "STRING1": {
              "defaultValue": "apple "
            },
            "STRING2": {
              "defaultValue": "banana "
            },
            "STRING3": {
              "defaultValue": "pear "
            },
            "STRING4": {
              "defaultValue": "orange "
            },
            "STRING5": {
              "defaultValue": "mango "
            },
            "STRING6": {
              "defaultValue": "strawberry "
            },
            "STRING7": {
              "defaultValue": "pineapple "
            },
            "STRING8": {
              "defaultValue": "grape"
            }
          },
          "switchText": "join x8",
          "switches": [
            "join4",
            "join5",
            "join6",
            "join7",
            {
              "isNoop": true
            },
            "join9"
          ]
        },
        {
          "opcode": "join9",
          "text": "join [STRING1] [STRING2] [STRING3] [STRING4] [STRING5] [STRING6] [STRING7] [STRING8] [STRING9]",
          "hideFromPalette": true,
          "disableMonitor": true,
          "arguments": {
            "STRING1": {
              "defaultValue": "apple "
            },
            "STRING2": {
              "defaultValue": "banana "
            },
            "STRING3": {
              "defaultValue": "pear "
            },
            "STRING4": {
              "defaultValue": "orange "
            },
            "STRING5": {
              "defaultValue": "mango "
            },
            "STRING6": {
              "defaultValue": "strawberry "
            },
            "STRING7": {
              "defaultValue": "pineapple "
            },
            "STRING8": {
              "defaultValue": "grape "
            },
            "STRING9": {
              "defaultValue": "kiwi"
            }
          },
          "switchText": "join x9",
          "switches": [
            "join4",
            "join5",
            "join6",
            "join7",
            "join8",
            {
              "isNoop": true
            }
          ]
        },
        //{
        //  blockType: BlockType.XML,
        //  xml: generateJoinList(this.showJoins)
        //}, // not needed, includes no additional information to above
      ],
      menus: {
        part: {
          acceptReporters: true,
          items: [
            { text: "first", value: "first" },
            { text: "last", value: "last" },
          ]
        }
      }
    };
  }
}

module.exports = pmOperatorsExpansion;