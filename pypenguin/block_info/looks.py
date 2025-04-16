from block_info.basis import *

looks = BlockInfoSet(name="looks", opcode_prefix="looks", block_infos={
    "sayforsecs": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="say (MESSAGE) for (SECONDS) seconds",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, old="MESSAGE"),
            "SECONDS": InputInfo(InputType.NUMBER, old="SECS"),
        },
    ),
    "say": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="say (MESSAGE)",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, old="MESSAGE"),
        },
    ),
    "thinkforsecs": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="think (MESSAGE) for (SECONDS) seconds",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, old="MESSAGE"),
            "SECONDS": InputInfo(InputType.NUMBER, old="SECS"),
        },
    ),
    "think": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="think (MESSAGE)",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, old="MESSAGE"),
        },
    ),
    "stoptalking": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="stop speaking",
    ),
    "setFont": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set font to (FONT) with font size (FONT-SIZE)",
        inputs={
            "FONT": InputInfo(InputType.TEXT, old="font"),
            "FONT-SIZE": InputInfo(InputType.NUMBER, old="size"),
        },
    ),
    "setColor": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [PROPERTY] color to (COLOR)",
        inputs={
            "COLOR": InputInfo(InputType.COLOR, old="color"),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.TEXT_BUBBLE_COLOR_PROPERTY, old="prop"),
        },
    ),
    "setShape": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set text bubble [PROPERTY] to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="color"),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.TEXT_BUBBLE_PROPERTY, old="prop"),
        },
    ),
    "sayWidth": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="bubble width",
        can_have_monitor="True",
    ),
    "sayHeight": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="bubble height",
        can_have_monitor="True",
    ),
    "switchcostumeto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="switch costume to ([COSTUME])",
        inputs={
            "COSTUME": InputInfo(InputType.COSTUME, old="COSTUME", menu=MenuInfo("looks_costume", inner="COSTUME")),
        },
    ),
    "nextcostume": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="next costume",
    ),
    "getinputofcostume": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="([PROPERTY]) of ([COSTUME])",
        inputs={
            "PROPERTY": InputInfo(InputType.COSTUME_PROPERTY, old="INPUT", menu=MenuInfo("looks_getinput_menu", inner="INPUT")),
            "COSTUME": InputInfo(InputType.COSTUME, old="COSTUME", menu=MenuInfo("looks_costume", inner="COSTUME")),
        },
    ),
    "switchbackdropto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="switch backdrop to ([BACKDROP])",
        inputs={
            "BACKDROP": InputInfo(InputType.BACKDROP, old="BACKDROP", menu=MenuInfo("looks_backdrops", inner="BACKDROP")),
        },
    ),
    "nextbackdrop": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="next backdrop",
    ),
    "changesizeby": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change size by (AMOUNT)",
        inputs={
            "AMOUNT": InputInfo(InputType.NUMBER, old="CHANGE"),
        },
    ),
    "setsizeto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set size to (SIZE)",
        inputs={
            "SIZE": InputInfo(InputType.NUMBER, old="SIZE"),
        },
    ),
    "setStretch": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set stretch to x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, old="X"),
            "Y": InputInfo(InputType.NUMBER, old="Y"),
        },
    ),
    "stretchGetX": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="x stretch",
        can_have_monitor="True",
    ),
    "stretchGetY": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="y stretch",
        can_have_monitor="True",
    ),
    "changeeffectby": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="change [EFFECT] sprite effect by (AMOUNT)",
        inputs={
            "AMOUNT": InputInfo(InputType.NUMBER, old="CHANGE"),
        },
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SPRITE_EFFECT, old="EFFECT"),
        },
    ),
    "seteffectto": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set [EFFECT] sprite effect to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="VALUE"),
        },
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SPRITE_EFFECT, old="EFFECT"),
        },
    ),
    "setTintColor": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="set tint color to (COLOR)",
        inputs={
            "COLOR": InputInfo(InputType.COLOR, old="color"),
        },
    ),
    "cleargraphiceffects": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="clear graphic effects",
    ),
    "getEffectValue": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="[EFFECT] sprite effect",
        can_have_monitor="True",
    ),
    "tintColor": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="tint color",
        can_have_monitor="True",
    ),
    "show": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="show",
    ),
    "hide": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="hide",
    ),
    "getSpriteVisible": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="visible?",
        can_have_monitor="True",
    ),
    "changeVisibilityOfSpriteShow": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="show ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="VISIBLE_OPTION", menu=MenuInfo("looks_changeVisibilityOfSprite_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "changeVisibilityOfSpriteHide": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="hide ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="VISIBLE_OPTION", menu=MenuInfo("looks_changeVisibilityOfSprite_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "getOtherSpriteVisible": BlockInfo(
        block_type=BlockType.BOOLEAN_REPORTER,
        new_opcode="is ([TARGET]) visible?",
        inputs={
            "TARGET": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="VISIBLE_OPTION", menu=MenuInfo("looks_getOtherSpriteVisible_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "gotofrontback": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go to [LAYER] layer",
    ),
    "goforwardbackwardlayers": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go [DIRECTION] (LAYERS) layers",
        inputs={
            "LAYERS": InputInfo(InputType.INTEGER, old="NUM"),
        },
        dropdowns={
            "DIRECTION": DropdownInfo(DropdownType.FORWARD_BACKWARD, old="FORWARD_BACKWARD"),
        },
    ),
    "layersSetLayer": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go to layer (LAYER)",
        inputs={
            "LAYER": InputInfo(InputType.INTEGER, old="NUM"),
        },
    ),
    "goTargetLayer": BlockInfo(
        block_type=BlockType.STATEMENT,
        new_opcode="go [DIRECTION] ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="VISIBLE_OPTION", menu=MenuInfo("looks_getOtherSpriteVisible_menu", inner="VISIBLE_OPTION")),
        },
        dropdowns={
            "DIRECTION": DropdownInfo(DropdownType.INFRONT_BEHIND, old="FORWARD_BACKWARD"),
        },
    ),
    "layersGetLayer": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="layer",
        can_have_monitor="True",
    ),
    "costumenumbername": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="costume [PROPERTY]",
        can_have_monitor="True",
    ),
    "backdropnumbername": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="backdrop [PROPERTY]",
        can_have_monitor="True",
    ),
    "size": BlockInfo(
        block_type=BlockType.STRING_REPORTER,
        new_opcode="size",
        can_have_monitor="True",
    ),
})