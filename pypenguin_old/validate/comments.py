from pypenguin_old.validate.constants import validateSchema, formatError, commentSchema
from pypenguin_old.validate.errors import commentSizeError

def validateComment(path, data):
    validateSchema(pathToData=path, data=data, schema=commentSchema)
    if data != None:
        if data["size"][0] < 52:
            raise formatError(commentSizeError, path+["size"]+[0], f"Must be at least 52.")
        if data["size"][1] < 32:
            raise formatError(commentSizeError, path+["size"]+[1], f"Must be at least 32.")
