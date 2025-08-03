((Scratch) => {
  "use strict";

  class DumbExample {
     getInfo() {
      return {
        id: "dumbExample",
        name: "Dumb Example",

        color1: "#e200ca",

        blocks: [
          {
            opcode: "last_used_base",
            blockType: Scratch.BlockType.REPORTER,
            text: "last used base",
            arguments: {},
          },
          {
            opcode: "last_two_inout_values",
            blockType: Scratch.BlockType.REPORTER,
            text: "last two [S1] and [S2] values",
            arguments: {
              S1: {
                type: Scratch.ArgumentType.STRING,
                menu: "in_out_menue"
              },
              S2: {
                type: Scratch.ArgumentType.STRING,
                menu: "in_out_menue"
              },
            },
          },
        ],
        menus: {
          in_out_menue: {
            acceptReporters: false,
            items: ["IN", "OUT"],
          },
        },
      };
    }

    last_used_base() {
      return "some base";
    }
    last_two_inout_values( {S1, S2} ) {
      return JSON.stringify(["HERE", S1, S2])
    }
  }

  Scratch.extensions.register(new DumbExample());
  console.log(Scratch)
})(Scratch);
