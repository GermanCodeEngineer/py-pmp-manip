from block_info.basis import *

looks = CategoryOpcodesInfo(name="looks", opcode_prefix="looks", block_infos={
    "sayforsecs": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="say (MESSAGE) for (SECONDS) seconds",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, new="MESSAGE"),
            "SECS": InputInfo(InputType.NUMBER, new="SECONDS"),
        },
    ),
    "say": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="say (MESSAGE)",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, new="MESSAGE"),
        },
    ),
    "thinkforsecs": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="think (MESSAGE) for (SECONDS) seconds",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, new="MESSAGE"),
            "SECS": InputInfo(InputType.NUMBER, new="SECONDS"),
        },
    ),
    "think": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="think (MESSAGE)",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, new="MESSAGE"),
        },
    ),
    "stoptalking": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="stop speaking",
    ),
    "setFont": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set font to (FONT) with font size (FONT-SIZE)",
        inputs={
            "font": InputInfo(InputType.TEXT, new="FONT"),
            "size": InputInfo(InputType.NUMBER, new="FONT-SIZE"),
        },
    ),
    "setColor": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [PROPERTY] color to (COLOR)",
        inputs={
            "color": InputInfo(InputType.COLOR, new="COLOR"),
        },
        dropdowns={
            "prop": DropdownInfo(DropdownType.TEXT_BUBBLE_COLOR_PROPERTY, new="PROPERTY"),
        },
    ),
    "setShape": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set text bubble [PROPERTY] to (VALUE)",
        inputs={
            "color": InputInfo(InputType.NUMBER, new="VALUE"),
        },
        dropdowns={
            "prop": DropdownInfo(DropdownType.TEXT_BUBBLE_PROPERTY, new="PROPERTY"),
        },
    ),
    "sayWidth": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="bubble width",
        can_have_monitor="True",
    ),
    "sayHeight": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="bubble height",
        can_have_monitor="True",
    ),
    "switchcostumeto": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="switch costume to ([COSTUME])",
        inputs={
            "COSTUME": InputInfo(InputType.COSTUME, new="COSTUME", menu=MenuInfo("looks_costume", inner="COSTUME")),
        },
    ),
    "nextcostume": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="next costume",
    ),
    "getinputofcostume": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="([PROPERTY]) of ([COSTUME])",
        inputs={
            "INPUT": InputInfo(InputType.COSTUME_PROPERTY, new="PROPERTY", menu=MenuInfo("looks_getinput_menu", inner="INPUT")),
            "COSTUME": InputInfo(InputType.COSTUME, new="COSTUME", menu=MenuInfo("looks_costume", inner="COSTUME")),
        },
    ),
    "switchbackdropto": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="switch backdrop to ([BACKDROP])",
        inputs={
            "BACKDROP": InputInfo(InputType.BACKDROP, new="BACKDROP", menu=MenuInfo("looks_backdrops", inner="BACKDROP")),
        },
    ),
    "nextbackdrop": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="next backdrop",
    ),
    "changesizeby": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change size by (AMOUNT)",
        inputs={
            "CHANGE": InputInfo(InputType.NUMBER, new="AMOUNT"),
        },
    ),
    "setsizeto": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set size to (SIZE)",
        inputs={
            "SIZE": InputInfo(InputType.NUMBER, new="SIZE"),
        },
    ),
    "setStretch": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set stretch to x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, new="X"),
            "Y": InputInfo(InputType.NUMBER, new="Y"),
        },
    ),
    "stretchGetX": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="x stretch",
        can_have_monitor="True",
    ),
    "stretchGetY": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="y stretch",
        can_have_monitor="True",
    ),
    "changeeffectby": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change [EFFECT] sprite effect by (AMOUNT)",
        inputs={
            "CHANGE": InputInfo(InputType.NUMBER, new="AMOUNT"),
        },
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SPRITE_EFFECT, new="EFFECT"),
        },
    ),
    "seteffectto": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [EFFECT] sprite effect to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, new="VALUE"),
        },
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SPRITE_EFFECT, new="EFFECT"),
        },
    ),
    "setTintColor": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set tint color to (COLOR)",
        inputs={
            "color": InputInfo(InputType.COLOR, new="COLOR"),
        },
    ),
    "cleargraphiceffects": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="clear graphic effects",
    ),
    "getEffectValue": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[EFFECT] sprite effect",
        can_have_monitor="True",
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SPRITE_EFFECT, new="EFFECT"),
        },
    ),
    "tintColor": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="tint color",
        can_have_monitor="True",
    ),
    "show": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="show",
    ),
    "hide": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="hide",
    ),
    "getSpriteVisible": OpcodeInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="visible?",
        can_have_monitor="True",
    ),
    "changeVisibilityOfSpriteShow": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="show ([TARGET])",
        inputs={
            "VISIBLE_OPTION": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("looks_changeVisibilityOfSprite_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "changeVisibilityOfSpriteHide": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="hide ([TARGET])",
        inputs={
            "VISIBLE_OPTION": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("looks_changeVisibilityOfSprite_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "getOtherSpriteVisible": OpcodeInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="is ([TARGET]) visible?",
        inputs={
            "VISIBLE_OPTION": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("looks_getOtherSpriteVisible_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "gotofrontback": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go to [LAYER] layer",
        dropdowns={
            "FRONT_BACK": DropdownInfo(DropdownType.FRONT_BACK, new="LAYER"),
        },
    ),
    "goforwardbackwardlayers": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go [DIRECTION] (LAYERS) layers",
        inputs={
            "NUM": InputInfo(InputType.INTEGER, new="LAYERS"),
        },
        dropdowns={
            "FORWARD_BACKWARD": DropdownInfo(DropdownType.FORWARD_BACKWARD, new="DIRECTION"),
        },
    ),
    "layersSetLayer": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go to layer (LAYER)",
        inputs={
            "NUM": InputInfo(InputType.INTEGER, new="LAYER"),
        },
    ),
    "goTargetLayer": OpcodeInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go [DIRECTION] ([TARGET])",
        inputs={
            "VISIBLE_OPTION": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, new="TARGET", menu=MenuInfo("looks_getOtherSpriteVisible_menu", inner="VISIBLE_OPTION")),
        },
        dropdowns={
            "FORWARD_BACKWARD": DropdownInfo(DropdownType.INFRONT_BEHIND, new="DIRECTION"),
        },
    ),
    "layersGetLayer": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="layer",
        can_have_monitor="True",
    ),
    "costumenumbername": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="costume [PROPERTY]",
        can_have_monitor="True",
        dropdowns={
            "NUMBER_NAME": DropdownInfo(DropdownType.NUMBER_NAME, new="PROPERTY"),
        },
    ),
    "backdropnumbername": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="backdrop [PROPERTY]",
        can_have_monitor="True",
        dropdowns={
            "NUMBER_NAME": DropdownInfo(DropdownType.NUMBER_NAME, new="PROPERTY"),
        },
    ),
    "size": OpcodeInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="size",
        can_have_monitor="True",
    ),
})