from dataclasses import dataclass

from utility import GreprClass, ValidationConfig
from utility import AA_TYPE, is_valid_js_data_uri, is_valid_url, InvalidValueError

@dataclass(repr=False)
class SRExtension(GreprClass):
    _grepr = True
    _grepr_fields = ["id"]
    
    id: str

    def validate(self, path: list, config: ValidationConfig) -> None:
        AA_TYPE(self, path, "id", str) # possibly verify its one of PenguinMod's extension if not custom
        if not self.id.isalnum():
            raise InvalidValueError(path, f"id of {self.__class__.__name__} may only contain alpha-numeric characters")

class SRBuiltinExtension(SRExtension):
    pass # Builtin Extensions don't specify a url.

@dataclass(repr=False)
class SRCustomExtension(SRExtension):
    _grepr_fields = SRExtension._grepr_fields + ["url"]
    
    url: str # either "https://..." or "data:application/javascript,..."
    
    def validate(self, path: list, config: ValidationConfig):
        super().validate(path, config)

        AA_TYPE(self, path, "url", str)
        if not (is_valid_url(self.url) or is_valid_js_data_uri(self.url)):
            raise InvalidValueError(path, f"url of {self.__class__.__name__} must be either a valid url or a valid javascript data uri.")
