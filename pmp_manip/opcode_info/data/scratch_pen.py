from pmp_manip.opcode_info.data_imports import *

ext_scratch_pen = OpcodeInfoGroup(name="scratch_pen", opcode_info=DualKeyDict({
    ("pen_clear", "erase all"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("pen_stamp", "stamp"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
    ),

    ("pen_setPrintFont", "set print font to ([FONT])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("FONT", "FONT"): InputInfo(BuiltinInputType.FONT, menu=MenuInfo("pen_menu_FONT", inner="FONT")),
        }),
    ),

    ("pen_setPrintFontSize", "set print font size to (SIZE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SIZE", "SIZE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_setPrintFontColor", "set print font color to (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
        }),
    ),

    ("pen_setPrintFontWeight", "set print font wheight to (WEIGHT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("WEIGHT", "WEIGHT"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_setPrintFontItalics", "set print font italics to [ON_OFF]"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        dropdowns=DualKeyDict({
            ("OPTION", "ON_OFF"): DropdownInfo(BuiltinDropdownType.ON_OFF),
        }),
    ),

    ("pen_printText", "print (TEXT) on x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TEXT", "TEXT"): InputInfo(BuiltinInputType.TEXT),
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_preloadUriImage", "preload image (URI) as (NAME)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("URI", "URI"): InputInfo(BuiltinInputType.TEXT),
            ("NAME", "NAME"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("pen_unloadUriImage", "unload image (NAME)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("NAME", "NAME"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("pen_drawUriImage", "draw image (URI) at x: (X) y: (Y)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("URI", "URI"): InputInfo(BuiltinInputType.TEXT),
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_drawUriImageWHR", "draw image (URI) at x: (X) y: (Y) width: (WIDTH) height: (HEIGHT) pointed at: (ROTATE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("URI", "URI"): InputInfo(BuiltinInputType.TEXT),
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
            ("WIDTH", "WIDTH"): InputInfo(BuiltinInputType.NUMBER),
            ("HEIGHT", "HEIGHT"): InputInfo(BuiltinInputType.NUMBER),
            ("ROTATE", "ROTATE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_drawUriImageWHCX1Y1X2Y2R", "draw image (URI) at x: (X) y: (Y) width: (WIDTH) height: (HEIGHT) cropping from x: (CROPX) y: (CROPY) width: (CROPWIDTH) height: (CROPHEIGHT) pointed at: (ROTATE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("URI", "URI"): InputInfo(BuiltinInputType.TEXT),
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
            ("WIDTH", "WIDTH"): InputInfo(BuiltinInputType.NUMBER),
            ("HEIGHT", "HEIGHT"): InputInfo(BuiltinInputType.NUMBER),
            ("CROPX", "CROPX"): InputInfo(BuiltinInputType.NUMBER),
            ("CROPY", "CROPY"): InputInfo(BuiltinInputType.NUMBER),
            ("CROPW", "CROPWIDTH"): InputInfo(BuiltinInputType.NUMBER),
            ("CROPH", "CROPHEIGHT"): InputInfo(BuiltinInputType.NUMBER),
            ("ROTATE", "ROTATE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_drawRect", "use (COLOR) to draw a square on x: (X) y: (Y) width: (WIDTH) height: (HEIGHT)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
            ("X", "X"): InputInfo(BuiltinInputType.NUMBER),
            ("Y", "Y"): InputInfo(BuiltinInputType.NUMBER),
            ("WIDTH", "WIDTH"): InputInfo(BuiltinInputType.NUMBER),
            ("HEIGHT", "HEIGHT"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

#    ("pen_drawComplexShape", "draw triangle (TRIANGLE) with fill (COLOR)"): OpcodeInfo(
#        opcode_type=OpcodeType.STATEMENT,
#        inputs=DualKeyDict({
#            ("SHAPE", "TRIANGLE"): InputInfo(BuiltinInputType.EMBEDDED_MENU),
#            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
#        }),
#    ),

#    ("pen_draw4SidedComplexShape", "draw quadrilateral (QUADRILATERAL) with fill (COLOR)"): OpcodeInfo(
#        opcode_type=OpcodeType.STATEMENT,
#        inputs=DualKeyDict({
#            ("SHAPE", "QUADRILATERAL"): InputInfo(BuiltinInputType.EMBEDDED_MENU),
#            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
#        }),
#    ),

    ("pen_drawArrayComplexShape", "draw polygon from points (POINTS) with fill (COLOR)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SHAPE", "POINTS"): InputInfo(BuiltinInputType.TEXT),
            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
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
            ("COLOR", "COLOR"): InputInfo(BuiltinInputType.COLOR),
        }),
    ),

    ("pen_changePenColorParamBy", "change pen ([PROPERTY]) by (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR_PARAM", "PROPERTY"): InputInfo(BuiltinInputType.PEN_PROPERTY, menu=MenuInfo("pen_menu_colorParam", inner="colorParam")),
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("pen_setPenColorParamTo", "set pen ([PROPERTY]) to (VALUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("COLOR_PARAM", "PROPERTY"): InputInfo(BuiltinInputType.PEN_PROPERTY, menu=MenuInfo("pen_menu_colorParam", inner="colorParam")),
            ("VALUE", "VALUE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("pen_changePenSizeBy", "change pen size by (SIZE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SIZE", "SIZE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("pen_setPenSizeTo", "set pen size to (SIZE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SIZE", "SIZE"): InputInfo(BuiltinInputType.TEXT),
        }),
    ),

    ("pen_setPenShadeToNumber", "LEGACY - set pen shade to (SHADE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SHADE", "SHADE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_changePenShadeBy", "LEGACY - change pen shade by (SHADE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("SHADE", "SHADE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_setPenHueToNumber", "LEGACY - set pen color to (HUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("HUE", "HUE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

    ("pen_changePenHueBy", "LEGACY - change pen color by (HUE)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("HUE", "HUE"): InputInfo(BuiltinInputType.NUMBER),
        }),
    ),

}))