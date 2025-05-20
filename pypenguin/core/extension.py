from dataclasses import dataclass

from pypenguin.utility import GreprClass, ValidationConfig
from pypenguin.utility import AA_TYPE, AA_ALNUM, is_valid_js_data_uri, is_valid_url, InvalidValueError

@dataclass(repr=False)
class SRExtension(GreprClass):
    """
    The second representation for an extension.
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button.
    """
    _grepr = True
    _grepr_fields = ["id"]
    
    id: str

    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRExtension is valid, raise ValidationError if not.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        """
        AA_TYPE(self, path, "id", str) # TODO: possibly verify its one of PenguinMod's extension if not custom
        AA_ALNUM(self, path, "id")

class SRBuiltinExtension(SRExtension):
    """
    The second representation for a builtin extension.
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button.
    Builtin Extensions don't specify a url.
    """
    pass

@dataclass(repr=False)
class SRCustomExtension(SRExtension):
    """
    The second representation for a custom extension. 
    Can be created either with url("https://...") or javascript data uri("data:application/javascript,...")
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button.
    """
    _grepr_fields = SRExtension._grepr_fields + ["url"]
    
    url: str # either "https://..." or "data:application/javascript,..."
    
    def validate(self, path: list, config: ValidationConfig):
        """
        Ensure a SRCustomExtension is valid, raise ValidationError if not.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        """
        super().validate(path, config)

        AA_TYPE(self, path, "url", str)
        if not (is_valid_url(self.url) or is_valid_js_data_uri(self.url)):
            raise InvalidValueError(path, f"url of {self.__class__.__name__} must be either a valid url or a valid javascript data uri.")


__all__ = ["SRExtension", "SRCustomExtension"]

