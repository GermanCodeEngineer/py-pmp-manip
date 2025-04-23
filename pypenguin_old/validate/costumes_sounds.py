from pypenguin.validate.constants import validateSchema, costumeSchema, soundSchema

def validateCostume(path, data, isStage):
    # Check costume format
    validateSchema(pathToData=path, data=data, schema=costumeSchema)
    
def validateSound(path, data):
    # Check sound format
    validateSchema(pathToData=path, data=data, schema=soundSchema)

