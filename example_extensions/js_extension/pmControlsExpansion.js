((Scratch) => {
  "use strict";

  const AsyncIcon = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMSIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHByZXNlcnZlQXNwZWN0UmF0aW89Im5vbmUiIHg9IjBweCIgeT0iMHB4IiB3aWR0aD0iMjRweCIgaGVpZ2h0PSIyNHB4IiB2aWV3Qm94PSIwIDAgMjQgMjQiPgo8ZGVmcz4KPGcgaWQ9IkxheWVyMV8wX0ZJTEwiPgo8cGF0aCBmaWxsPSIjMDAwMDAwIiBmaWxsLW9wYWNpdHk9IjAuNDQ3MDU4ODIzNTI5NDExOCIgc3Ryb2tlPSJub25lIiBkPSIKTSAxMi4xIDEuNTUKUSAxMS41MTU0Mjk2ODc1IDEuNDk5NjA5Mzc1IDEwLjk1IDIuMTUKTCA3LjMgNi4xClEgNi42ODcxMDkzNzUgNi41NjI1IDYuNyA3LjIgNi43MjUgOC43NzUxOTUzMTI1IDguMyA4Ljc1CkwgOS4yNSA4Ljc1ClEgOS42MTA1NDY4NzUgMTIuMjU2MDU0Njg3NSA5LjI1IDE1LjMKTCA4LjEgMTUuMjUKUSA3LjE1MzkwNjI1IDE1LjI3MTY3OTY4NzUgNi44IDE2IDYuNjc2MzY3MTg3NSAxNi4yNjY3OTY4NzUgNi42NSAxNi42NSA2LjYxMjY5NTMxMjUgMTcuMTY3MTg3NSA3LjIgMTcuODUKTCAxMC45NSAyMS45ClEgMTEuNDQxMjEwOTM3NSAyMi42NTE5NTMxMjUgMTIuMSAyMi41NSAxMi42MDkxNzk2ODc1IDIyLjY0NDcyNjU2MjUgMTMuMiAyMi4wNQpMIDEzLjIgMjIuMDUgMTcuMDUgMTcuOQpRIDE3LjU1ODc4OTA2MjUgMTcuNDY4OTQ1MzEyNSAxNy41IDE2LjkgMTcuNTI1IDE1LjMyNDgwNDY4NzUgMTUuOTUgMTUuMwpMIDE0LjggMTUuMwpRIDE0LjUyODMyMDMxMjUgMTIuMTIxNjc5Njg3NSAxNC44NSA4LjgKTCAxNi4xNSA4LjgKUSAxNy4xOTg0Mzc1IDguODI4NzEwOTM3NSAxNy40NSA3LjkgMTcuNTIzNjMyODEyNSA3Ljc1MTE3MTg3NSAxNy41IDcuNiAxNy41MjUgNy41NSAxNy41IDcuNDUgMTcuNTQ3NDYwOTM3NSA2Ljg0NDUzMTI1IDE3LjA1IDYuMjUKTCAxMy4yIDIuMgpRIDEyLjc1NTA3ODEyNSAxLjQ5ODI0MjE4NzUgMTIuMSAxLjU1IFoiLz4KPC9nPgoKPGcgaWQ9IkxheWVyMF8wX0ZJTEwiPgo8cGF0aCBmaWxsPSIjRkZGRkZGIiBzdHJva2U9Im5vbmUiIGQ9IgpNIDE2LjM1IDYuODUKTCAxMi40NSAyLjc1ClEgMTIuMyAyLjUgMTIuMSAyLjUgMTEuOSAyLjUgMTEuNyAyLjc1CkwgNy44NSA2Ljg1ClEgNy42NSA3IDcuNjUgNy4yIDcuNjUgNy44NSA4LjMgNy44NQpMIDEwLjEgNy44NQpRIDEwLjY1IDEyLjQgMTAuMSAxNi4yNQpMIDguMSAxNi4yClEgNy43NSAxNi4yIDcuNjUgMTYuNSA3LjYgMTYuNTUgNy42IDE2LjY1IDcuNiAxNi45IDcuOSAxNy4yNQpMIDExLjc1IDIxLjQKUSAxMS45IDIxLjY1IDEyLjEgMjEuNjUgMTIuMyAyMS42NSAxMi41NSAyMS40CkwgMTYuNCAxNy4yNQpRIDE2LjYgMTcuMSAxNi42IDE2LjkgMTYuNiAxNi4yNSAxNS45NSAxNi4yNQpMIDE0IDE2LjI1ClEgMTMuNSAxMi4xNSAxNCA3LjkKTCAxNi4xNSA3LjkKUSAxNi41IDcuOSAxNi42IDcuNiAxNi42IDcuNTUgMTYuNiA3LjQ1IDE2LjYgNy4xNSAxNi4zNSA2Ljg1IFoiLz4KPC9nPgo8L2RlZnM+Cgo8ZyBpZD0iTGF5ZXJfMyI+CjxnIHRyYW5zZm9ybT0ibWF0cml4KCAxLCAwLCAwLCAxLCAwLDApICI+Cjx1c2UgeGxpbms6aHJlZj0iI0xheWVyMV8wX0ZJTEwiLz4KPC9nPgo8L2c+Cgo8ZyBpZD0iYXN5bmNfc3ZnIj4KPGcgdHJhbnNmb3JtPSJtYXRyaXgoIDEsIDAsIDAsIDEsIDAsMCkgIj4KPHVzZSB4bGluazpocmVmPSIjTGF5ZXIwXzBfRklMTCIvPgo8L2c+CjwvZz4KPC9zdmc+"

  const blockSeparator = '<sep gap="36"/>'; // At default scale, about 28px
  const pathToMedia = 'static/blocks-media'; // ScratchBlocks.mainWorkspace.options.pathToMedia

  const blocks = `
  <block type="control_repeatForSeconds">
      <value name="TIMES">
          <shadow type="math_number">
              <field name="NUM">1</field>
          </shadow>
      </value>
  </block>
  %block0>
  %block1>
  <block type="control_inline_stack_output">
      <value name="SUBSTACK">
          <block type="procedures_return">
              <value name="return">
                <shadow type="text">
                  <field name="TEXT">1</field>
                </shadow>
              </value>
          </block>
      </value>
  </block>
  <block type="control_waittick"/>
  %block3>
  ${blockSeparator}
  %block2>
  %block4>
  %block5>
  ${blockSeparator}
  <block type="control_get_counter"/>
  <block type="control_incr_counter"/>
  <block type="control_decr_counter"/>
  <block type="control_set_counter">
      <value name="VALUE">
          <shadow type="math_whole_number">
              <field name="NUM">10</field>
          </shadow>
      </value>
  </block>
  <block type="control_clear_counter"/>
  `;

  /**
   * Class of idk
   * @constructor
   */
  class pmControlsExpansion {
      constructor(runtime) {
          /**
           * The runtime instantiating this block package.
           * @type {runtime}
           */
          this.runtime = runtime;
          // register compiled blocks
          this.runtime.registerCompiledExtensionBlocks('pmControlsExpansion', this.getCompileInfo());
      }

      orderCategoryBlocks(extensionBlocks) {
          let categoryBlocks = blocks;

          let idx = 0;
          for (const block of extensionBlocks) {
              categoryBlocks = categoryBlocks.replace(`%block${idx}>`, block);
              idx++;
          }

          return [categoryBlocks];
      }

      /**
       * @returns {object} metadata for extension category NOT blocks
       * this extension only contains blocks defined elsewhere,
       * since we just want to seperate them rather than create
       * slow versions of them
       */
      getInfo() {
          return {
              id: 'pmControlsExpansion',
              name: 'Controls Expansion',
              color1: '#FFAB19',
              color2: '#EC9C13',
              color3: '#CF8B17',
              isDynamic: true,
              orderBlocks: this.orderCategoryBlocks,
              blocks: [
                  {
                      opcode: 'ifElseIf',
                      text: [
                          'if [CONDITION1] then',
                          'else if [CONDITION2] then'
                      ],
                      branchCount: 2,
                      BlockType: Scratch.BlockType.CONDITIONAL,
                      arguments: {
                          CONDITION1: { type: Scratch.ArgumentType.BOOLEAN },
                          CONDITION2: { type: Scratch.ArgumentType.BOOLEAN }
                      }
                  },
                  {
                      opcode: 'ifElseIfElse',
                      text: [
                          'if [CONDITION1] then',
                          'else if [CONDITION2] then',
                          'else'
                      ],
                      branchCount: 3,
                      BlockType: Scratch.BlockType.CONDITIONAL,
                      arguments: {
                          CONDITION1: { type: Scratch.ArgumentType.BOOLEAN },
                          CONDITION2: { type: Scratch.ArgumentType.BOOLEAN }
                      }
                  },
                  {
                      opcode: 'asNewBroadCast',
                      text: [
                          'new thread',
                          '[ICON]'
                      ],
                      branchCount: 1,
                      BlockType: Scratch.BlockType.CONDITIONAL,
                      alignments: [
                          null, // text
                          null, // SUBSTACK
                          Scratch.ArgumentAlignment.RIGHT // ICON
                      ],
                      arguments: {
                          ICON: {
                              type: Scratch.ArgumentType.IMAGE,
                              dataURI: AsyncIcon
                          }
                      }
                  },
                  {
                      opcode: 'restartFromTheTop',
                      text: 'restart from the top [ICON]',
                      BlockType: Scratch.BlockType.COMMAND,
                      isTerminal: true,
                      arguments: {
                          ICON: {
                              type: Scratch.ArgumentType.IMAGE,
                              dataURI: `${pathToMedia}/repeat.svg`
                          }
                      }
                  },
                  {
                      opcode: 'asNewBroadCastArgs',
                      text: [
                          'new thread with data [DATA]',
                          '[ICON]'
                      ],
                      branchCount: 1,
                      BlockType: Scratch.BlockType.CONDITIONAL,
                      alignments: [
                          null, // text
                          null, // SUBSTACK
                          Scratch.ArgumentAlignment.RIGHT // ICON
                      ],
                      arguments: {
                          DATA: {
                              type: Scratch.ArgumentType.STRING,
                              defaultValue: "abc",
                          },
                          ICON: {
                              type: Scratch.ArgumentType.IMAGE,
                              dataURI: AsyncIcon
                          }
                      }
                  },
                  {
                      opcode: 'asNewBroadCastArgBlock',
                      text: 'thread data',
                      BlockType: Scratch.BlockType.REPORTER,
                      disableMonitor: true
                  },
              ]
          };
      }

      /**
       * This function is used for any compiled blocks in the extension if they exist.
       * Data in this function is given to the IR & JS generators.
       * Data must be valid otherwise errors may occur.
       * @returns {object} functions that create data for compiled blocks.
       */
      getCompileInfo() {
          return {
              ir: {
                  ifElseIf: (generator, block) => ({
                      kind: 'stack',
                      condition1: generator.descendInputOfBlock(block, 'CONDITION1'),
                      condition2: generator.descendInputOfBlock(block, 'CONDITION2'),
                      whenTrue1: generator.descendSubstack(block, 'SUBSTACK'),
                      whenTrue2: generator.descendSubstack(block, 'SUBSTACK2')
                  }),
                  ifElseIfElse: (generator, block) => ({
                      kind: 'stack',
                      condition1: generator.descendInputOfBlock(block, 'CONDITION1'),
                      condition2: generator.descendInputOfBlock(block, 'CONDITION2'),
                      whenTrue1: generator.descendSubstack(block, 'SUBSTACK'),
                      whenTrue2: generator.descendSubstack(block, 'SUBSTACK2'),
                      whenTrue3: generator.descendSubstack(block, 'SUBSTACK3')
                  }),
                  restartFromTheTop: () => ({
                      kind: 'stack'
                  })
              },
              js: {
                  ifElseIf: (node, compiler, imports) => {
                      compiler.source += `if (${compiler.descendInput(node.condition1).asBoolean()}) {\n`;
                      compiler.descendStack(node.whenTrue1, new imports.Frame(false));
                      compiler.source += `} else if (${compiler.descendInput(node.condition2).asBoolean()}) {\n`;
                      compiler.descendStack(node.whenTrue2, new imports.Frame(false));
                      compiler.source += `}\n`;
                  },
                  ifElseIfElse: (node, compiler, imports) => {
                      compiler.source += `if (${compiler.descendInput(node.condition1).asBoolean()}) {\n`;
                      compiler.descendStack(node.whenTrue1, new imports.Frame(false));
                      compiler.source += `} else if (${compiler.descendInput(node.condition2).asBoolean()}) {\n`;
                      compiler.descendStack(node.whenTrue2, new imports.Frame(false));
                      compiler.source += `} else {\n`;
                      compiler.descendStack(node.whenTrue3, new imports.Frame(false));
                      compiler.source += `}\n`;
                  },
                  restartFromTheTop: (_, compiler) => {
                      compiler.source += `runtime._restartThread(thread);`;
                      compiler.source += `return;`;
                  }
              }
          };
      }

      ifElseIf (args, util) {
          const condition1 = Scratch.Cast.toBoolean(args.CONDITION1);
          const condition2 = Scratch.Cast.toBoolean(args.CONDITION2);
          if (condition1) {
              util.startBranch(1, false);
          } else if (condition2) {
              util.startBranch(2, false);
          }
      }
      
      ifElseIfElse (args, util) {
          const condition1 = Scratch.Cast.toBoolean(args.CONDITION1);
          const condition2 = Scratch.Cast.toBoolean(args.CONDITION2);
          if (condition1) {
              util.startBranch(1, false);
          } else if (condition2) {
              util.startBranch(2, false);
          } else {
              util.startBranch(3, false);
          }
      }
      
      restartFromTheTop() {
          return; // doesnt work in compat mode
      }

      // CubesterYT code probably
      asNewBroadCast(_, util) {
          if (util.thread.target.blocks.getBranch(util.thread.peekStack(), 0)) {
              util.sequencer.runtime._pushThread(
                  util.thread.target.blocks.getBranch(util.thread.peekStack(), 0),
                  util.target,
                  {}
              );
          }
      }
      asNewBroadCastArgs(args, util) {
          const data = Scratch.Cast.toString(args.DATA);
          if (util.thread.target.blocks.getBranch(util.thread.peekStack(), 0)) {
              const thread = util.sequencer.runtime._pushThread(
                  util.thread.target.blocks.getBranch(util.thread.peekStack(), 0),
                  util.target,
                  {}
              );

              thread.__controlx_asNewBroadCastArgs_data = data;
          }
      }
      asNewBroadCastArgBlock(_, util) {
          return util.thread.__controlx_asNewBroadCastArgs_data;
      }
  }

  Scratch.extensions.register(new pmControlsExpansion(Scratch.vm.runtime));
})(Scratch);