############################################################################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
#                            DOCUMENTATION HERE: docs/config.md                            #
############################################################################################


from colorama import init as colorama_init
from datetime import timedelta

from pmp_manip.utility import PP_ConfigurationError, PP_ValidationError

from pmp_manip.config.schema import *


_config_instance: MasterConfig | None = None

def init_config(config: MasterConfig) -> None:
    """
    Initializes the global configuration.
    This must be called exactly **once** at the beginning of your program.
    After initialization, the configuration becomes immutable
    Also initializes some required packages

    Args:
        config: The configuration object to initialize with

    Raises:
        PP_ConfigurationError: If configuration is already initialized or validation fails
        TypeError: If the provided config is not an instance of MasterConfig
    """
    global _config_instance
    
    if _config_instance is not None:
        raise PP_ConfigurationError("Configuration has already been initialized.")
    if not isinstance(config, MasterConfig):
        raise TypeError("Expected a MasterConfig instance")
    try:
        config.validate()
    except PP_ValidationError as error:
        raise PP_ConfigurationError("Invalid Configuration") from error
    
    config.ext_info_gen ._frozen_ = True
    config.validation   ._frozen_ = True
    config.platform_meta._frozen_ = True
    config              ._frozen_ = True
    _config_instance = config
    
    # Initialize required packages
    colorama_init()

def get_config() -> MasterConfig:
    """
    Returns the globally initialized configuration

    Returns:
        MasterConfig: The active project configuration

    Raises:
        PP_ConfigurationError: If configuration has not been initialized
    """
    global _config_instance
    if _config_instance is None:
        raise PP_ConfigurationError("Configuration has not been initialized.")
    return _config_instance

def get_default_config() -> "MasterConfig":
    """
    Returns the default project configuration

    Returns:
        MasterConfig: A default configuration with reasonable presets
    """
    return MasterConfig(
        ext_info_gen=ExtInfoGenConfig(
            gen_opcode_info_dir="example_extensions/gen_opcode_info/", # TODO: find perm solution
            js_fetch_interval=timedelta(days=3),
        ),
        validation=ValidationConfig(
            raise_if_monitor_position_outside_stage=True,
            raise_if_monitor_bigger_then_stage=True,
        ),
        platform_meta=PlatformMetaConfig(
            scratch_semver="3.0.0",
            scratch_vm="11.1.0",
            penguinmod_vm="0.2.0",
        ),
    )


__all__ = ["init_config", "get_config", "get_default_config"]


