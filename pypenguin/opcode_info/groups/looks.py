from utility import DualKeyDict

from opcode_info import OpcodeInfoGroup, OpcodeInfo, OpcodeType, InputInfo, InputType, DropdownInfo, DropdownType, MenuInfo

looks = OpcodeInfoGroup(name="looks", opcode_info=DualKeyDict({
    ("looks_sayforsecs", "say (MESSAGE) for (SECONDS) seconds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("MESSAGE", "MESSAGE"): InputInfo(InputType.TEXT),
            ("SECS", "SECONDS"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("looks_say", "say (MESSAGE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("MESSAGE", "MESSAGE"): InputInfo(InputType.TEXT),
        }),
    ),
    ("looks_thinkforsecs", "think (MESSAGE) for (SECONDS) seconds"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("MESSAGE", "MESSAGE"): InputInfo(InputType.TEXT),
            ("SECS", "SECONDS"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("looks_think", "think (MESSAGE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("MESSAGE", "MESSAGE"): InputInfo(InputType.TEXT),
        }),
    ),
    ("looks_stoptalking", "stop speaking"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),
    ("looks_setFont", "set font to (FONT) with font size (FONT-SIZE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("font", "FONT"): InputInfo(InputType.TEXT),
            ("size", "FONT-SIZE"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("looks_setColor", "set [PROPERTY] color to (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("color", "COLOR"): InputInfo(InputType.COLOR),
        }),
        dropdowns=DualKeyDict({
            ("prop", "PROPERTY"): DropdownInfo(DropdownType.TEXT_BUBBLE_COLOR_PROPERTY),
        }),
    ),
    ("looks_setShape", "set text bubble [PROPERTY] to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("color", "VALUE"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("prop", "PROPERTY"): DropdownInfo(DropdownType.TEXT_BUBBLE_PROPERTY),
        }),
    ),
    ("looks_sayWidth", "bubble width"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
    ("looks_sayHeight", "bubble height"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
    ("looks_switchcostumeto", "switch costume to ([COSTUME])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COSTUME", "COSTUME"): InputInfo(InputType.COSTUME, menu=MenuInfo("looks_costume", inner="COSTUME")),
        }),
    ),
    ("looks_nextcostume", "next costume"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),
    ("looks_getinputofcostume", "([PROPERTY]) of ([COSTUME])"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("INPUT", "PROPERTY"): InputInfo(InputType.COSTUME_PROPERTY, menu=MenuInfo("looks_getinput_menu", inner="INPUT")),
            ("COSTUME", "COSTUME"): InputInfo(InputType.COSTUME, menu=MenuInfo("looks_costume", inner="COSTUME")),
        }),
    ),
    ("looks_switchbackdropto", "switch backdrop to ([BACKDROP])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("BACKDROP", "BACKDROP"): InputInfo(InputType.BACKDROP, menu=MenuInfo("looks_backdrops", inner="BACKDROP")),
        }),
    ),
    ("looks_nextbackdrop", "next backdrop"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),
    ("looks_changesizeby", "change size by (AMOUNT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CHANGE", "AMOUNT"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("looks_setsizeto", "set size to (SIZE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SIZE", "SIZE"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("looks_setStretch", "set stretch to x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("looks_stretchGetX", "x stretch"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
    ("looks_stretchGetY", "y stretch"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
    ("looks_changeeffectby", "change [EFFECT] sprite effect by (AMOUNT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("CHANGE", "AMOUNT"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(DropdownType.SPRITE_EFFECT),
        }),
    ),
    ("looks_seteffectto", "set [EFFECT] sprite effect to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VALUE", "VALUE"): InputInfo(InputType.NUMBER),
        }),
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(DropdownType.SPRITE_EFFECT),
        }),
    ),
    ("looks_setTintColor", "set tint color to (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("color", "COLOR"): InputInfo(InputType.COLOR),
        }),
    ),
    ("looks_cleargraphiceffects", "clear graphic effects"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),
    ("looks_getEffectValue", "[EFFECT] sprite effect"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
        dropdowns=DualKeyDict({
            ("EFFECT", "EFFECT"): DropdownInfo(DropdownType.SPRITE_EFFECT),
        }),
    ),
    ("looks_tintColor", "tint color"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
    ("looks_show", "show"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),
    ("looks_hide", "hide"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),
    ("looks_getSpriteVisible", "visible?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        can_have_monitor="True",
    ),
    ("looks_changeVisibilityOfSpriteShow", "show ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VISIBLE_OPTION", "TARGET"): InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, menu=MenuInfo("looks_changeVisibilityOfSprite_menu", inner="VISIBLE_OPTION")),
        }),
    ),
    ("looks_changeVisibilityOfSpriteHide", "hide ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VISIBLE_OPTION", "TARGET"): InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, menu=MenuInfo("looks_changeVisibilityOfSprite_menu", inner="VISIBLE_OPTION")),
        }),
    ),
    ("looks_getOtherSpriteVisible", "is ([TARGET]) visible?"): OpcodeInfo(
        opcode_type=OpcodeType.BOOLEAN_REPORTER,
        inputs=DualKeyDict({
            ("VISIBLE_OPTION", "TARGET"): InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, menu=MenuInfo("looks_getOtherSpriteVisible_menu", inner="VISIBLE_OPTION")),
        }),
    ),
    ("looks_gotofrontback", "go to [LAYER] layer"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("FRONT_BACK", "LAYER"): DropdownInfo(DropdownType.FRONT_BACK),
        }),
    ),
    ("looks_goforwardbackwardlayers", "go [DIRECTION] (LAYERS) layers"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("NUM", "LAYERS"): InputInfo(InputType.INTEGER),
        }),
        dropdowns=DualKeyDict({
            ("FORWARD_BACKWARD", "DIRECTION"): DropdownInfo(DropdownType.FORWARD_BACKWARD),
        }),
    ),
    ("looks_layersSetLayer", "go to layer (LAYER)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("NUM", "LAYER"): InputInfo(InputType.INTEGER),
        }),
    ),
    ("looks_goTargetLayer", "go [DIRECTION] ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VISIBLE_OPTION", "TARGET"): InputInfo(InputType.MYSELF_OR_OTHER_SPRITE, menu=MenuInfo("looks_getOtherSpriteVisible_menu", inner="VISIBLE_OPTION")),
        }),
        dropdowns=DualKeyDict({
            ("FORWARD_BACKWARD", "DIRECTION"): DropdownInfo(DropdownType.INFRONT_BEHIND),
        }),
    ),
    ("looks_layersGetLayer", "layer"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
    ("looks_costumenumbername", "costume [PROPERTY]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
        dropdowns=DualKeyDict({
            ("NUMBER_NAME", "PROPERTY"): DropdownInfo(DropdownType.NUMBER_NAME),
        }),
    ),
    ("looks_backdropnumbername", "backdrop [PROPERTY]"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
        dropdowns=DualKeyDict({
            ("NUMBER_NAME", "PROPERTY"): DropdownInfo(DropdownType.NUMBER_NAME),
        }),
    ),
    ("looks_size", "size"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        can_have_monitor="True",
    ),
}))