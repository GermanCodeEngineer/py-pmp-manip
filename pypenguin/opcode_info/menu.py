class MenuInfo:
    """
    The information about a menu in an input.
    """
    _grepr = True
    _grepr_fields = ["opcode", "inner"]
    
    opcode: str
    inner : str
    
    def __init__(self, opcode: str, inner: str):
        self.opcode = opcode
        self.inner  = inner
