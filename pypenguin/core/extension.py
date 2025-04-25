from utility import PypenguinClass
from utility import AA_TYPE, is_valid_js_data_uri, is_valid_url, InvalidValueValidationError

class SRExtension(PypenguinClass):
    _grepr = True
    _grepr_fields = ["id"]
    
    id: str
    
    def __init__(self, id: str):
        self.id  = id

    def validate(self, path: list) -> None:
        AA_TYPE(self, path, "id", str)
        if not self.id.isalnum():
            raise InvalidValueValidationError(path, f"id of {self.__class__.__name__} may only contain alpha-numeric characters")

class SRBuiltinExtension(SRExtension):
    pass # Builtin Extensions don't specify a url.

class SRCustomExtension(SRExtension):
    _grepr_fields = SRExtension._grepr_fields + ["url"]
    
    url: str # either "https://..." or "data:application/javascript,..."
    
    def __init__(self, id: str, url: str):
        super().__init__(id=id)
        self.url = url
    
    def validate(self, path: list):
        super().validate(path)

        AA_TYPE(self, path, "url", str)
        if not (is_valid_url(self.url) or is_valid_js_data_uri(self.url)):
            raise InvalidValueValidationError(path, f"url of {self.__class__.__name__} must be either a valid url or a valid javascript data uri.")
