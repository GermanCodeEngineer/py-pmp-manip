from pmp_manip.utility import grepr_dataclass, AA_TYPE, AA_ALNUM, is_valid_js_data_uri, is_valid_url, MANIP_InvalidValueError


@grepr_dataclass(
    grepr_fields=["id"], init=False, 
    forbid_init_only_subcls=True, suggested_subcls_names=["SRBuiltinExtension", "SRCustomExtension"],
)
class SRExtension:
    """
    The second representation for an extension.
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button
    """
    
    id: str

    def validate(self, path: list) -> None:
        """
        Ensure a SRExtension is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRExtension is invalid
        """
        AA_TYPE(self, path, "id", str) # TODO: possibly verify its one of PenguinMod's extension if not custom
        AA_ALNUM(self, path, "id")

@grepr_dataclass(grepr_fields=[])
class SRBuiltinExtension(SRExtension):
    """
    The second representation for a builtin extension.
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button.
    Builtin Extensions do not specify a url
    """

@grepr_dataclass(grepr_fields=["url"])
class SRCustomExtension(SRExtension):
    """
    The second representation for a custom extension. 
    Can be created either with url("https://...") or javascript data uri("data:application/javascript,...")
    Creating an extension and adding it to a project is equivalent to clicking the "add extension" button
    """
    
    url: str # either "https://..." or "data:application/javascript,..."
    # TODO: find a way to not show whole huge JS data URI's
    
    def validate(self, path: list):
        """
        Ensure a SRCustomExtension is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRCustomExtension is invalid
            MANIP_InvalidValueError(MANIP_ValidationError): if the url is invalid
        """
        super().validate(path)

        AA_TYPE(self, path, "url", str)
        if not (is_valid_url(self.url) or is_valid_js_data_uri(self.url)):
            raise MANIP_InvalidValueError(path, f"url of {self.__class__.__name__} must be either a valid url or a valid javascript data uri.")


__all__ = ["SRExtension", "SRCustomExtension"]

