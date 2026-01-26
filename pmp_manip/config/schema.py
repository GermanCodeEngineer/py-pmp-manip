from __future__  import annotations
from abc         import ABC
from datetime    import timedelta
from dataclasses import FrozenInstanceError
from typing      import Any, Callable

from pmp_manip.utility import (
    grepr_dataclass, field, is_valid_directory_path, 
    AbstractTreePath, HasGreprValidate,
    MANIP_InvalidDirPathError,
)


@grepr_dataclass()
class ConfigBase(ABC, HasGreprValidate):
    """
    The base class for a configuration
    """
    
    _frozen_: bool = field(init=False, default=False, grepr=False)
    
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

@grepr_dataclass(validate=True)
class ExtInfoGenConfig(ConfigBase):
    """
    The configuration for the extension info generator module
    """
    
    gen_opcode_info_dir: str
    js_fetch_interval: timedelta
    node_js_exec_timeout: float
    is_trusted_extension_origin_handler: Callable[[str], bool] | None
    
    def post_validate(self, path: AbstractTreePath) -> None:
        """
        Ensure an instance is valid, raise MANIPO_ValidationError if not
        
        Args:
            path: the path from the top of the config tree to itself. Used for better error messages
        
        Raises:
            MANIP_InvalidDirPathError: if the extension opcode info dir is invalid
        """
        if not is_valid_directory_path(self.gen_opcode_info_dir):
            raise MANIP_InvalidDirPathError(path, f"Invalid extension opcode info directory: {self.gen_opcode_info_dir}")

@grepr_dataclass()
class ValidationConfig(ConfigBase):
    """
    The configuration for the validation of a project or parts of it
    """

    raise_if_monitor_position_outside_stage: bool
    raise_if_monitor_bigger_then_stage: bool

@grepr_dataclass()
class PlatformMetaConfig(ConfigBase, HasGreprValidate):
    """
    You probably should NOT change this.
    The configuration containing the up to date version of Scratch and PenguinMod
    """

    scratch_semver: str # TODO:(OPT) possibly implement stricter validation
    scratch_vm: str
    penguinmod_vm: str

@grepr_dataclass()
class MasterConfig(ConfigBase):
    """
    The master configuration containing all subconfigurations for the pmp_manip project
    """

    ext_info_gen: ExtInfoGenConfig = field(call_subvalidate=True)
    validation: ValidationConfig = field(call_subvalidate=True)
    platform_meta: PlatformMetaConfig = field(call_subvalidate=True)


__all__ = ["ExtInfoGenConfig", "ValidationConfig", "PlatformMetaConfig", "MasterConfig"]

