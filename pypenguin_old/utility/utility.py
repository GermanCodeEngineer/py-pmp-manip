from enum import Enum
import pprint
import difflib

# -----------------------------------
# Other pypenguin_old.utility Classes and Functions
# -----------------------------------
class Platform(Enum):
    PENGUINMOD  = 0
    SCRATCH     = 1

class CostumeBitmapResolutionConst(Enum):
    AUTO_SCALE  = 0

class CostumeRotationCenterConst  (Enum):
    AUTO_CENTER = 0


class BlockSelector:
    count = 0
    def __init__(self):
        self.id = BlockSelector.count
        BlockSelector.count += 1
    def __eq__(self, other):
        if not isinstance(other, BlockSelector):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"BS::{self.id}"
    
    def copy(self):
        new = BlockSelector()
        new.id = self.id
        return new

def pformat(*objects, sep=" ", end="\n"):
    string = ""
    for i, object in enumerate(objects):
        string += pprint.pformat(object, sort_dicts=False)
        if i + 1 < len(objects):
            string += sep
    string += end
    return string

def pp(*objects, sep=" ", end="\n"):
    print(pformat(*objects, sep=sep, end=end))

def flipKeysAndValues(obj: dict):
    return dict(zip(obj.values(), obj.keys()))

def removeDuplicates(items):
    newItems = []
    [newItems.append(value) for value in items if value not in newItems]
    return newItems

def getListOfClosestStrings(string, possibleValues) -> str:
    similarityScores = [(item, difflib.SequenceMatcher(None, string, item).ratio()) for item in possibleValues]
    sortedMatches = sorted(similarityScores, key=lambda x: x[1], reverse=True)
    topTenMatches = [i[0] for i in sortedMatches[:10]]
    return "".join([f"\n- '{match}'" for match in topTenMatches])

def getSelectors(obj, depth=0):
    selectors = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(key, BlockSelector)  : selectors.append(key  )
            if isinstance(value, BlockSelector): selectors.append(value)
            else                               : selectors += getSelectors(value, depth=depth+1)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            if isinstance(item, BlockSelector): selectors.append(item)
            else                              : selectors += getSelectors(item, depth=depth+1)
    return selectors
