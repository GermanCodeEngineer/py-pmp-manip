class MenuInfo:
    _grepr = True
    _grepr_fields = ["opcode", "inner"]
    
    opcode: str
    inner : str
    
    def __init__(self, opcode: str, inner: str):
        self.opcode = opcode
        self.inner  = inner
