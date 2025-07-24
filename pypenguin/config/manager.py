############################################################################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
#                            DOCUMENTATION HERE: docs/config.md                            #
############################################################################################


from datetime import timedelta

from pypenguin.utility import ConfigurationError

from pypenguin.config.schema import *


_config_instance: MasterConfig|None = None

def init_config(config: MasterConfig) -> None:
    global _config_instance
    
    if _config_instance is not None:
        raise ConfigurationError("Configuration has already been initialized.")
    try:
        config.validate()
    except ValidationError as error:
        raise ConfigurationError("Invalid Configuration") from error
    
    config.ext_info_gen ._frozen_ = True
    config.validation   ._frozen_ = True
    config.conversion   ._frozen_ = True
    config.platform_meta._frozen_ = True
    config              ._frozen_ = True
    _config_instance = config

def get_config() -> MasterConfig:
    global _config_instance
    if _config_instance is None:
        raise ConfigurationError("Configuration has not been initialized.")
    return _config_instance

def get_default_config() -> "MasterConfig":
    return MasterConfig(
        ext_info_gen=ExtInfoGenConfig(
            gen_opcode_info_dir="example_extensions/gen_opcode_info/", # TODO: find perm solution
            js_fetch_interval=timedelta(days=3),
        ),
        validation=ValidationConfig(
            raise_if_monitor_position_outside_stage=True,
            raise_if_monitor_bigger_then_stage=True,
        ),
        conversion=ConversionConfig(
            stage_width=480,
            stage_height=360,
        ),
        platform_meta=PlatformMetaConfig(
            scratch_semver="3.0.0",
            scratch_vm="11.1.0",
            penguinmod_vm="0.2.0",
        ),
    )


__all__ = ["init_config", "get_config", "get_default_config"]


