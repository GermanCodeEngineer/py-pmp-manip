from __future__ import annotations

from pmp_manip.utility import (
    grepr_dataclass, 
    AA_TYPE, AA_ALNUM, is_valid_js_data_uri, is_valid_url, 
    AbstractTreePath, HasGreprValidate, MANIP_InvalidValueError,
)


@grepr_dataclass(init=False, forbid_init_only_subcls=True)
class SRExtension(HasGreprValidate):
    """
    The second representation for an extension.
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button
    """
    
    id: str

    def post_validate(self, path: AbstractTreePath) -> None:
        """
        Ensure an instance is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the instance is invalid
        """
        AA_ALNUM(self, path, "id") # TODO: possibly verify its one of PenguinMod's extension if not custom

@grepr_dataclass()
class SRBuiltinExtension(SRExtension):
    """
    The second representation for a builtin extension.
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button.
    Builtin Extensions do not specify a url
    """

@grepr_dataclass()
class SRCustomExtension(SRExtension):
    """
    The second representation for a custom extension. 
    Can be created either with url("https://...") or javascript data uri("data:application/javascript,...")
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button
    """
    
    url: str # either "https://..." or "data:application/javascript,..."
    # TODO:(OPT) find a way to not show whole huge JS data URI's
    
    def post_validate(self, path: AbstractTreePath):
        """
        Ensure an instance is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the instance is invalid
            MANIP_InvalidValueError(MANIP_ValidationError): if the url is invalid
        """
        super().post_validate(path)

        if not (is_valid_url(self.url) or is_valid_js_data_uri(self.url)):
            raise MANIP_InvalidValueError(path, f"url of {self.__class__.__name__} must be either a valid url or a valid javascript data uri.")


__all__ = ["SRExtension", "SRBuiltinExtension", "SRCustomExtension"]

