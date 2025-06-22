from pypenguin.opcode_info.data_imports import *

scratch_pen = OpcodeInfoGroup(name="scratch_pen", opcode_info=DualKeyDict({
    ("pen_clear", "erase all"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("pen_stamp", "stamp"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("pen_setPrintFont", "set print font to ([FONT])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("FONT", "FONT"): InputInfo(InputType.FONT, menu=MenuInfo("pen_menu_FONT", inner="FONT")),
        }),
    ),

    ("pen_setPrintFontSize", "set print font size to (SIZE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SIZE", "SIZE"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_setPrintFontColor", "set print font color to (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR", "COLOR"): InputInfo(InputType.COLOR),
        }),
    ),

    ("pen_setPrintFontWeight", "set print font wheight to (WEIGHT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("WEIGHT", "WEIGHT"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_setPrintFontItalics", "set print font italics to [ON_OFF]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("OPTION", "ON_OFF"): DropdownInfo(DropdownType.ON_OFF),
        }),
    ),

    ("pen_printText", "print (TEXT) on x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEXT", "TEXT"): InputInfo(InputType.TEXT),
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_preloadUriImage", "preload image (URI) as (NAME)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("URI", "URI"): InputInfo(InputType.TEXT),
            ("NAME", "NAME"): InputInfo(InputType.TEXT),
        }),
    ),

    ("pen_unloadUriImage", "unload image (NAME)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("NAME", "NAME"): InputInfo(InputType.TEXT),
        }),
    ),

    ("pen_drawUriImage", "draw image (URI) at x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("URI", "URI"): InputInfo(InputType.TEXT),
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_drawUriImageWHR", "draw image (URI) at x: (X) y: (Y) width: (WIDTH) height: (HEIGHT) pointed at: (ROTATE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("URI", "URI"): InputInfo(InputType.TEXT),
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
            ("WIDTH", "WIDTH"): InputInfo(InputType.NUMBER),
            ("HEIGHT", "HEIGHT"): InputInfo(InputType.NUMBER),
            ("ROTATE", "ROTATE"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_drawUriImageWHCX1Y1X2Y2R", "draw image (URI) at x: (X) y: (Y) width: (WIDTH) height: (HEIGHT) cropping from x: (CROPX) y: (CROPY) width: (CROPWIDTH) height: (CROPHEIGHT) pointed at: (ROTATE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("URI", "URI"): InputInfo(InputType.TEXT),
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
            ("WIDTH", "WIDTH"): InputInfo(InputType.NUMBER),
            ("HEIGHT", "HEIGHT"): InputInfo(InputType.NUMBER),
            ("CROPX", "CROPX"): InputInfo(InputType.NUMBER),
            ("CROPY", "CROPY"): InputInfo(InputType.NUMBER),
            ("CROPW", "CROPWIDTH"): InputInfo(InputType.NUMBER),
            ("CROPH", "CROPHEIGHT"): InputInfo(InputType.NUMBER),
            ("ROTATE", "ROTATE"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_drawRect", "use (COLOR) to draw a square on x: (X) y: (Y) width: (WIDTH) height: (HEIGHT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR", "COLOR"): InputInfo(InputType.COLOR),
            ("X", "X"): InputInfo(InputType.NUMBER),
            ("Y", "Y"): InputInfo(InputType.NUMBER),
            ("WIDTH", "WIDTH"): InputInfo(InputType.NUMBER),
            ("HEIGHT", "HEIGHT"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_drawComplexShape", "draw triangle (TRIANGLE) with fill (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SHAPE", "TRIANGLE"): InputInfo(InputType.EMBEDDED_MENU),
            ("COLOR", "COLOR"): InputInfo(InputType.COLOR),
        }),
    ),

    ("pen_draw4SidedComplexShape", "draw quadrilateral (QUADRILATERAL) with fill (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SHAPE", "QUADRILATERAL"): InputInfo(InputType.EMBEDDED_MENU),
            ("COLOR", "COLOR"): InputInfo(InputType.COLOR),
        }),
    ),

    ("pen_drawArrayComplexShape", "draw polygon from points (POINTS) with fill (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SHAPE", "POINTS"): InputInfo(InputType.TEXT),
            ("COLOR", "COLOR"): InputInfo(InputType.COLOR),
        }),
    ),

    ("pen_penDown", "pen down"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("pen_penUp", "pen up"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("pen_setPenColorToColor", "set pen color to (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR", "COLOR"): InputInfo(InputType.COLOR),
        }),
    ),

    ("pen_changePenColorParamBy", "change pen ([PROPERTY]) by (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR_PARAM", "PROPERTY"): InputInfo(InputType.PEN_PROPERTY, menu=MenuInfo("pen_menu_colorParam", inner="colorParam")),
            ("VALUE", "VALUE"): InputInfo(InputType.TEXT),
        }),
    ),

    ("pen_setPenColorParamTo", "set pen ([PROPERTY]) to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR_PARAM", "PROPERTY"): InputInfo(InputType.PEN_PROPERTY, menu=MenuInfo("pen_menu_colorParam", inner="colorParam")),
            ("VALUE", "VALUE"): InputInfo(InputType.TEXT),
        }),
    ),

    ("pen_changePenSizeBy", "change pen size by (SIZE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SIZE", "SIZE"): InputInfo(InputType.TEXT),
        }),
    ),

    ("pen_setPenSizeTo", "set pen size to (SIZE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SIZE", "SIZE"): InputInfo(InputType.TEXT),
        }),
    ),

    ("pen_setPenShadeToNumber", "LEGACY - set pen shade to (SHADE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SHADE", "SHADE"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_changePenShadeBy", "LEGACY - change pen shade by (SHADE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SHADE", "SHADE"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_setPenHueToNumber", "LEGACY - set pen color to (HUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("HUE", "HUE"): InputInfo(InputType.NUMBER),
        }),
    ),

    ("pen_changePenHueBy", "LEGACY - change pen color by (HUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("HUE", "HUE"): InputInfo(InputType.NUMBER),
        }),
    ),

}))