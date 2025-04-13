class FLComment:
    _grepr = True
    _grepr_fields = ["block_id", "x", "y", "width", "height", "minimized", "text"]
    
    block_id: str
    x: int | float
    y: int | float
    width: int | float
    height: int | float
    minimized: bool
    text: str
    
    @classmethod
    def from_data(cls, data):
        self = cls()
        self.block_id  = data["blockId"]
        self.x         = data["x"]
        self.y         = data["y"]
        self.width     = data["width"]
        self.height    = data["height"]
        self.minimized = data["minimized"]
        self.text      = data["text"]
        return self


{
    'blockId': None,
    'x': 158.51851851851856,
    'y': 591.8518518518517,
    'width': 200,
    'height': 200,
    'minimized': False,
    'text': 'hi'}
{
    'blockId': 'b',
    'x': 1031.0370407104492,
    'y': 348,
    'width': 200,
    'height': 200,
    'minimized': False,
    'text': 'as block: hi'}

