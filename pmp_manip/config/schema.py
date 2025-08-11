############################################################################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
#                            DOCUMENTATION HERE: docs/config.md                            #
############################################################################################


from abc         import ABC, abstractmethod
from datetime    import timedelta
from dataclasses import field, FrozenInstanceError
from typing      import Any, Callable

from pmp_manip.utility import grepr_dataclass, is_valid_directory_path, AA_TYPE, AA_NONE_OR_CALLABLE, MANIP_InvalidDirPathError


@grepr_dataclass(grepr_fields=[])
class ConfigBase(ABC):
    """
    The base class for a configuration
    """
    
    _frozen_: bool = field(init=False, default=False)
    
    def __setattr__(self, attr: str, value: Any) -> None:
        """
        Sets an attribute.
        Prevents modification if _frozen_ is True
        
        Args:
            attr: the attribute to set
            value: the value to set the attribute to
        
        Raises:
           dataclasses.FrozenInstanceError: if _frozen_ is True
        """
        if self._frozen_:
            raise FrozenInstanceError(f"cannot assign to field {attr!r}")
        super().__setattr__(attr, value)        
    
    @abstractmethod
    def validate(self, path: list) -> None:
        """
        Ensure a Config is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the top of the config tree to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the Config is invalid
        """

@grepr_dataclass(grepr_fields=["gen_opcode_info_dir", "js_fetch_interval", "node_js_exec_timeout", "is_trusted_extension_origin_handler"])
class ExtInfoGenConfig(ConfigBase):
    """
    The configuration for the extension info generator module
    """
    
    gen_opcode_info_dir: str
    js_fetch_interval: timedelta
    node_js_exec_timeout: float
    is_trusted_extension_origin_handler: Callable[[str], bool] | None
    
    def validate(self, path: list) -> None:
        """
        Ensure a ExtInfoGenConfig is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the top of the config tree to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the ExtInfoGenConfig is invalid
            MANIP_InvalidDirPathError: if the extension opcode info dir is invalid
        """
        AA_TYPE(self, path, "gen_opcode_info_dir", str) # TODO: possibly add check if path is valid
        if not is_valid_directory_path(self.gen_opcode_info_dir):
            raise MANIP_InvalidDirPathError("Invalid extension opcode info directory: {self.gen_opcode_info_dir}")
        AA_TYPE(self, path, "js_fetch_interval", timedelta)
        AA_TYPE(self, path, "node_js_exec_timeout", float)
        AA_NONE_OR_CALLABLE(self, path, "is_trusted_extension_origin_handler")

@grepr_dataclass(grepr_fields=["raise_if_monitor_position_outside_stage", "raise_if_monitor_bigger_then_stage"])
class ValidationConfig(ConfigBase):
    """
    The configuration for the validation of a project or parts of it
    """

    raise_if_monitor_position_outside_stage: bool
    raise_if_monitor_bigger_then_stage: bool

    def validate(self, path: list) -> None:
        """
        Ensure a ValidationConfig is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the top of the config tree to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the ValidationConfig is invalid
        """
        AA_TYPE(self, path, "raise_if_monitor_position_outside_stage", bool)
        AA_TYPE(self, path, "raise_if_monitor_bigger_then_stage", bool)

@grepr_dataclass(grepr_fields=["scratch_semver", "scratch_vm", "penguinmod_vm"])
class PlatformMetaConfig(ConfigBase):
    """
    You probably should NOT change this.
    The configuration containing the up to date version of Scratch and PenguinMod
    """

    scratch_semver: str
    scratch_vm: str
    penguinmod_vm: str

    def validate(self, path: list) -> None:
        """
        Ensure a PlatformMetaConfig is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the top of the config tree to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the PlatformMetaConfig is invalid
        """
        AA_TYPE(self, path, "scratch_semver", str) # TODO: possibly implement stricter validation
        AA_TYPE(self, path, "scratch_vm"    , str)
        AA_TYPE(self, path, "penguinmod_vm" , str)

@grepr_dataclass(grepr_fields=["ext_info_gen", "validation", "platform_meta"])
class MasterConfig(ConfigBase):
    """
    The master configuration containing all subconfigurations for the pmp_manip project
    """

    ext_info_gen: ExtInfoGenConfig
    validation: ValidationConfig
    platform_meta: PlatformMetaConfig

    def validate(self, path: list = []) -> None:
        """
        Ensure a MasterConfig is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the top of the config tree to itself. Used for better error messages
        
        Raises:
            MANIP_ValidationError: if the MasterConfig is invalid
        """
        AA_TYPE(self, path, "ext_info_gen" , ExtInfoGenConfig  )
        AA_TYPE(self, path, "validation"   , ValidationConfig  )
        AA_TYPE(self, path, "platform_meta", PlatformMetaConfig)
        
        self.ext_info_gen .validate(path+["ext_info_gen" ])
        self.validation   .validate(path+["validation"   ])
        self.platform_meta.validate(path+["platform_meta"])


__all__ = ["ExtInfoGenConfig", "ValidationConfig", "PlatformMetaConfig", "MasterConfig"]

