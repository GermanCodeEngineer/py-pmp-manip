from datetime import timedelta
from pytest   import raises, MonkeyPatch

from pypenguin.utility import PP_ConfigurationError

from pypenguin.config.manager import init_config, get_config, get_default_config
from pypenguin.config.schema  import MasterConfig, ExtInfoGenConfig, ValidationConfig, PlatformMetaConfig



def test_init_config(monkeypatch: MonkeyPatch):
    from pypenguin.config import manager as manager_mod
    monkeypatch.setattr(manager_mod, "_config_instance", None)
    
    init_config(get_default_config())
    assert manager_mod._config_instance is not None
    with raises(PP_ConfigurationError):
        init_config(get_default_config())

def test_init_config_invalid_type(monkeypatch: MonkeyPatch):
    from pypenguin.config import manager as manager_mod
    monkeypatch.setattr(manager_mod, "_config_instance", None)

    with raises(TypeError):
        init_config(5)

def test_init_config_validation_fail(monkeypatch: MonkeyPatch):
    from pypenguin.config import manager as manager_mod
    monkeypatch.setattr(manager_mod, "_config_instance", None)

    cfg = get_default_config()
    cfg.ext_info_gen = 6
    with raises(PP_ConfigurationError):
        init_config(cfg)



def test_get_config(monkeypatch: MonkeyPatch):
    from pypenguin.config import manager as manager_mod
    monkeypatch.setattr(manager_mod, "_config_instance", None)

    cfg = get_default_config()
    init_config(cfg)
    assert get_config() is cfg

def test_get_config_not_configured(monkeypatch: MonkeyPatch):
    from pypenguin.config import manager as manager_mod
    monkeypatch.setattr(manager_mod, "_config_instance", None)

    with raises(PP_ConfigurationError):
        get_config()
    


def test_get_default_config():
    assert get_default_config() == MasterConfig(
        ext_info_gen=ExtInfoGenConfig(
            gen_opcode_info_dir="example_extensions/gen_opcode_info/", 
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


