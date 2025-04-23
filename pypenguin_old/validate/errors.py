class ValidationError(Exception):
    pass


class blockTypeError(ValidationError):
    pass

class unknownOpcodeError(ValidationError):
    pass

class inputIdError(ValidationError):
    pass

class missingInputAttributeError(ValidationError):
    pass

class optionIdError(ValidationError):
    pass

class optionValueCategoryError(ValidationError):
    pass

class optionValueError(ValidationError):
    pass

class undefinedVariableError(ValidationError):
    pass

class undefinedListError(ValidationError):
    pass

class undefinedCustomOpcodeError(ValidationError):
    pass

class embeddedMenuError(ValidationError):
    pass

class commentSizeError(ValidationError):
    pass

class doubleVariableDefinitionError(ValidationError):
    pass

class doubleListDefinitionError(ValidationError):
    pass

class equalSpriteNameError(ValidationError):
    pass

class monitorSpriteNameError(ValidationError):
    pass

class missingMonitorAttributeError(ValidationError):
    pass

class monitorSliderRangeError(ValidationError):
    pass

class spriteNameError(ValidationError):
    pass

class layerOrderError(ValidationError):
    pass

class equalCostumeName(ValidationError):
    pass

class equalSoundName(ValidationError):
    pass

class currentCostumeError(ValidationError):
    pass

class doubleCustomBlockDefinitionError(ValidationError):
    pass

class missingVariableAttributeError(ValidationError):
    pass

