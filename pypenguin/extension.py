from utility import PypenguinClass

class SRExtension(PypenguinClass):
    _grepr = True
    _grepr_fields = ["id"]
    
    id: str
    
    def __init__(self, id: str):
        self.id  = id

class SRBuiltinExtension(SRExtension):
    pass # Builtin Extensions don't specify a url.

class SRCustomExtension(SRExtension):
    _grepr_fields = SRExtension._grepr_fields + ["url"]
    
    url: str # either "https://..." or "data:application/javascript,..."
    
    def __init__(self, id: str, url: str):
        super().__init__(id=id)
        self.url = url
        
