class PP_ValidationError(Exception):
    pass


class blockTypeError(PP_ValidationError):
    pass

class unknownOpcodeError(PP_ValidationError):
    pass

class inputIdError(PP_ValidationError):
    pass

class missingInputAttributeError(PP_ValidationError):
    pass

class optionIdError(PP_ValidationError):
    pass

class optionValueCategoryError(PP_ValidationError):
    pass

class optionValueError(PP_ValidationError):
    pass

class undefinedVariableError(PP_ValidationError):
    pass

class undefinedListError(PP_ValidationError):
    pass

class undefinedCustomOpcodeError(PP_ValidationError):
    pass

class embeddedMenuError(PP_ValidationError):
    pass

class commentSizeError(PP_ValidationError):
    pass

class doubleVariableDefinitionError(PP_ValidationError):
    pass

class doubleListDefinitionError(PP_ValidationError):
    pass

class equalSpriteNameError(PP_ValidationError):
    pass

class monitorSpriteNameError(PP_ValidationError):
    pass

class missingMonitorAttributeError(PP_ValidationError):
    pass

class monitorSliderRangeError(PP_ValidationError):
    pass

class spriteNameError(PP_ValidationError):
    pass

class layerOrderError(PP_ValidationError):
    pass

class equalCostumeName(PP_ValidationError):
    pass

class equalSoundName(PP_ValidationError):
    pass

class currentCostumeError(PP_ValidationError):
    pass

class doubleCustomBlockDefinitionError(PP_ValidationError):
    pass

class missingVariableAttributeError(PP_ValidationError):
    pass

