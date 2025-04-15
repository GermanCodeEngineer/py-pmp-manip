from block_info.basis import *

looks = BlockInfoSet(name="looks", opcode_prefix="looks", blocks={
    "looks_sayforsecs": BlockInfo(
        block_type="intruction",
        new_opcode="say (MESSAGE) for (SECONDS) seconds",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, old="MESSAGE"),
            "SECONDS": InputInfo(InputType.NUMBER, old="SECS"),
        },
    ),
    "looks_say": BlockInfo(
        block_type="instruction",
        new_opcode="say (MESSAGE)",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, old="MESSAGE"),
        },
    ),
    "looks_thinkforsecs": BlockInfo(
        block_type="intruction",
        new_opcode="think (MESSAGE) for (SECONDS) seconds",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, old="MESSAGE"),
            "SECONDS": InputInfo(InputType.NUMBER, old="SECS"),
        },
    ),
    "looks_think": BlockInfo(
        block_type="instruction",
        new_opcode="think (MESSAGE)",
        inputs={
            "MESSAGE": InputInfo(InputType.TEXT, old="MESSAGE"),
        },
    ),
    "looks_stoptalking": BlockInfo(
        block_type="instruction",
        new_opcode="stop speaking",
    ),
    "looks_setFont": BlockInfo(
        block_type="instruction",
        new_opcode="set font to (FONT) with font size (FONT-SIZE)",
        inputs={
            "FONT": InputInfo(InputType.TEXT, old="font"),
            "FONT-SIZE": InputInfo(InputType.NUMBER, old="size"),
        },
    ),
    "looks_setColor": BlockInfo(
        block_type="instruction",
        new_opcode="set [PROPERTY] color to (COLOR)",
        inputs={
            "COLOR": InputInfo(InputType.COLOR, old="color"),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.TEXT_BUBBLE_COLOR_PROPERTY, old="prop"),
        },
    ),
    "looks_setShape": BlockInfo(
        block_type="instruction",
        new_opcode="set text bubble [PROPERTY] to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="color"),
        },
        dropdowns={
            "PROPERTY": DropdownInfo(DropdownType.TEXT_BUBBLE_PROPERTY, old="prop"),
        },
    ),
    "looks_sayWidth": BlockInfo(
        block_type="stringReporter",
        new_opcode="bubble width",
        can_have_monitor="True",
    ),
    "looks_sayHeight": BlockInfo(
        block_type="stringReporter",
        new_opcode="bubble height",
        can_have_monitor="True",
    ),
    "looks_switchcostumeto": BlockInfo(
        block_type="instruction",
        new_opcode="switch costume to ([COSTUME])",
        inputs={
            "COSTUME": InputInfo(InputType.COSTUME, old="COSTUME", menu=MenuInfo("looks_costume", inner="COSTUME")),
        },
    ),
    "looks_nextcostume": BlockInfo(
        block_type="instruction",
        new_opcode="next costume",
    ),
    "looks_getinputofcostume": BlockInfo(
        block_type="stringReporter",
        new_opcode="([PROPERTY]) of ([COSTUME])",
        inputs={
            "PROPERTY": InputInfo(InputType.COSTUME_PROPERTY, old="INPUT", menu=MenuInfo("looks_getinput_menu", inner="INPUT")),
            "COSTUME": InputInfo(InputType.COSTUME, old="COSTUME", menu=MenuInfo("looks_costume", inner="COSTUME")),
        },
    ),
    "looks_switchbackdropto": BlockInfo(
        block_type="instruction",
        new_opcode="switch backdrop to ([BACKDROP])",
        inputs={
            "BACKDROP": InputInfo(InputType.BACKDROP, old="BACKDROP", menu=MenuInfo("looks_backdrops", inner="BACKDROP")),
        },
    ),
    "looks_nextbackdrop": BlockInfo(
        block_type="instruction",
        new_opcode="next backdrop",
    ),
    "looks_changesizeby": BlockInfo(
        block_type="instruction",
        new_opcode="change size by (AMOUNT)",
        inputs={
            "AMOUNT": InputInfo(InputType.NUMBER, old="CHANGE"),
        },
    ),
    "looks_setsizeto": BlockInfo(
        block_type="instruction",
        new_opcode="set size to (SIZE)",
        inputs={
            "SIZE": InputInfo(InputType.NUMBER, old="SIZE"),
        },
    ),
    "looks_setStretch": BlockInfo(
        block_type="instruction",
        new_opcode="set stretch to x: (X) y: (Y)",
        inputs={
            "X": InputInfo(InputType.NUMBER, old="X"),
            "Y": InputInfo(InputType.NUMBER, old="Y"),
        },
    ),
    "looks_stretchGetX": BlockInfo(
        block_type="stringReporter",
        new_opcode="x stretch",
        can_have_monitor="True",
    ),
    "looks_stretchGetY": BlockInfo(
        block_type="stringReporter",
        new_opcode="y stretch",
        can_have_monitor="True",
    ),
    "looks_changeeffectby": BlockInfo(
        block_type="instruction",
        new_opcode="change [EFFECT] sprite effect by (AMOUNT)",
        inputs={
            "AMOUNT": InputInfo(InputType.NUMBER, old="CHANGE"),
        },
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SPRITE_EFFECT, old="EFFECT"),
        },
    ),
    "looks_seteffectto": BlockInfo(
        block_type="instruction",
        new_opcode="set [EFFECT] sprite effect to (VALUE)",
        inputs={
            "VALUE": InputInfo(InputType.NUMBER, old="VALUE"),
        },
        dropdowns={
            "EFFECT": DropdownInfo(DropdownType.SPRITE_EFFECT, old="EFFECT"),
        },
    ),
    "looks_setTintColor": BlockInfo(
        block_type="instruction",
        new_opcode="set tint color to (COLOR)",
        inputs={
            "COLOR": InputInfo(InputType.COLOR, old="color"),
        },
    ),
    "looks_cleargraphiceffects": BlockInfo(
        block_type="instruction",
        new_opcode="clear graphic effects",
    ),
    "looks_getEffectValue": BlockInfo(
        block_type="stringReporter",
        new_opcode="[EFFECT] sprite effect",
        can_have_monitor="True",
    ),
    "looks_tintColor": BlockInfo(
        block_type="stringReporter",
        new_opcode="tint color",
        can_have_monitor="True",
    ),
    "looks_show": BlockInfo(
        block_type="instruction",
        new_opcode="show",
    ),
    "looks_hide": BlockInfo(
        block_type="instruction",
        new_opcode="hide",
    ),
    "looks_getSpriteVisible": BlockInfo(
        block_type="booleanReporter",
        new_opcode="visible?",
        can_have_monitor="True",
    ),
    "looks_changeVisibilityOfSpriteShow": BlockInfo(
        block_type="instruction",
        new_opcode="show ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="VISIBLE_OPTION", menu=MenuInfo("looks_changeVisibilityOfSprite_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "looks_changeVisibilityOfSpriteHide": BlockInfo(
        block_type="instruction",
        new_opcode="hide ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="VISIBLE_OPTION", menu=MenuInfo("looks_changeVisibilityOfSprite_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "looks_getOtherSpriteVisible": BlockInfo(
        block_type="booleanReporter",
        new_opcode="is ([TARGET]) visible?",
        inputs={
            "TARGET": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="VISIBLE_OPTION", menu=MenuInfo("looks_getOtherSpriteVisible_menu", inner="VISIBLE_OPTION")),
        },
    ),
    "looks_gotofrontback": BlockInfo(
        block_type="instruction",
        new_opcode="go to [LAYER] layer",
    ),
    "looks_goforwardbackwardlayers": BlockInfo(
        block_type="instruction",
        new_opcode="go [DIRECTION] (LAYERS) layers",
        inputs={
            "LAYERS": InputInfo(InputType.INTEGER, old="NUM"),
        },
        dropdowns={
            "DIRECTION": DropdownInfo(DropdownType.FORWARD_BACKWARD, old="FORWARD_BACKWARD"),
        },
    ),
    "looks_layersSetLayer": BlockInfo(
        block_type="instruction",
        new_opcode="go to layer (LAYER)",
        inputs={
            "LAYER": InputInfo(InputType.INTEGER, old="NUM"),
        },
    ),
    "looks_goTargetLayer": BlockInfo(
        block_type="instruction",
        new_opcode="go [DIRECTION] ([TARGET])",
        inputs={
            "TARGET": InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, old="VISIBLE_OPTION", menu=MenuInfo("looks_getOtherSpriteVisible_menu", inner="VISIBLE_OPTION")),
        },
        dropdowns={
            "DIRECTION": DropdownInfo(DropdownType.INFRONT_BEHIND, old="FORWARD_BACKWARD"),
        },
    ),
    "looks_layersGetLayer": BlockInfo(
        block_type="stringReporter",
        new_opcode="layer",
        can_have_monitor="True",
    ),
    "looks_costumenumbername": BlockInfo(
        block_type="stringReporter",
        new_opcode="costume [PROPERTY]",
        can_have_monitor="True",
    ),
    "looks_backdropnumbername": BlockInfo(
        block_type="stringReporter",
        new_opcode="backdrop [PROPERTY]",
        can_have_monitor="True",
    ),
    "looks_size": BlockInfo(
        block_type="stringReporter",
        new_opcode="size",
        can_have_monitor="True",
    ),
})