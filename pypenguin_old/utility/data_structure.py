# -----------------------
# Data Structure Manipulation Functions
# -----------------------
def editDataStructure(obj, conditionFunc: callable, conversionFunc: callable):
    if isinstance(obj, dict):
        newObj = {}
        for key, value in obj.items():
            newKey = conversionFunc(key) if conditionFunc(key) else editDataStructure(key, conditionFunc, conversionFunc)
            newValue = conversionFunc(value) if conditionFunc(value) else editDataStructure(value, conditionFunc, conversionFunc)
            newObj[newKey] = newValue
        return newObj

    if isinstance(obj, (list, tuple, set)):
        newObj = type(obj)()
        for item in obj:
            newItem = conversionFunc(item) if conditionFunc(item) else editDataStructure(item, conditionFunc, conversionFunc)
            newObj.append(newItem)
        return newObj
    return obj

def getDataAtPath(data, path:list[str|int]):
    """
    Retrieve data from a nested structure (dictionaries/lists) using a path.
    """
    current = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return None
    return current
