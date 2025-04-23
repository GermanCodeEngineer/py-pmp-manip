from pypenguin.validate.constants import validateSchema, formatError, variableSchema, listSchema
from pypenguin.validate.errors import missingVariableAttributeError

def validateVariable(path, data, isGlobal):    
    # Check variable format
    validateSchema(pathToData=path, data=data, schema=variableSchema)
    if isGlobal and "isCloudVariable" not in data:
        raise formatError(missingVariableAttributeError, path, "Global variables must have the 'isCloudVariable' attribute.")
        
def validateList(path, data):
    # Check list format
    validateSchema(pathToData=path, data=data, schema=listSchema)