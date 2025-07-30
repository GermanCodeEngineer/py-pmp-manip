from dataclasses import FrozenInstanceError
from datetime    import timedelta
from pytest      import raises

from pmp_manip.utility import grepr_dataclass, PP_TypeValidationError

from pmp_manip.config.manager import get_default_config
from pmp_manip.config.schema  import ConfigBase, MasterConfig, ExtInfoGenConfig, ValidationConfig, PlatformMetaConfig

from tests.utility import execute_attr_validation_tests


@grepr_dataclass(grepr_fields=["a"])
class TEST_Config(ConfigBase):
    a: int

    def validate(self, path: list) -> None: # to fulfill abstractmethod
        pass



def test_ConfigBase_setattr_not_frozen():
    config = TEST_Config(a=3)
    config.a = 5

def test_ConfigBase_setattr_frozen():
    config = TEST_Config(a=3)
    config._frozen_ = True
    with raises(FrozenInstanceError):
        config.a = 5
    with raises(FrozenInstanceError):
        config._frozen_ = False



def test_ExtInfoGenConfig_validate():
    config = ExtInfoGenConfig(
        gen_opcode_info_dir=".",
        js_fetch_interval=timedelta(days=1),
    )
    config.validate(path=[])
    
    execute_attr_validation_tests(
        obj=config,
        attr_tests=[
            ("gen_opcode_info_dir", 5, PP_TypeValidationError),
            ("js_fetch_interval", {}, PP_TypeValidationError),
        ],
        validate_func=ExtInfoGenConfig.validate,
        func_args=[[]],
    )



def test_ValidationConfig_validate():
    config = ValidationConfig(
        raise_if_monitor_position_outside_stage=False, 
        raise_if_monitor_bigger_then_stage=False,
    )
    config.validate(path=[])
    
    execute_attr_validation_tests(
        obj=config,
        attr_tests=[
            ("raise_if_monitor_position_outside_stage", set(), PP_TypeValidationError),
            ("raise_if_monitor_bigger_then_stage", None, PP_TypeValidationError),
        ],
        validate_func=ValidationConfig.validate,
        func_args=[[]],
    )



def test_PlatformMetaConfig_validate():
    config = PlatformMetaConfig(
        scratch_semver="3.0.0",
        scratch_vm="11.1.0",
        penguinmod_vm="0.2.0",
    )
    config.validate(path=[])
    
    execute_attr_validation_tests(
        obj=config,
        attr_tests=[
            ("scratch_semver", 31, PP_TypeValidationError),
            ("scratch_vm", (11, 1, 0), PP_TypeValidationError),
            ("penguinmod_vm", 2.0, PP_TypeValidationError),
        ],
        validate_func=PlatformMetaConfig.validate,
        func_args=[[]],
    )



def test_MasterConfig_validate():
    config = get_default_config()
    config.validate(path=[])
    
    execute_attr_validation_tests(
        obj=config,
        attr_tests=[
            ("ext_info_gen", {}, PP_TypeValidationError),
            ("ext_info_gen", ExtInfoGenConfig(gen_opcode_info_dir=".", js_fetch_interval=3), PP_TypeValidationError),
            ("validation", config.ext_info_gen, PP_TypeValidationError),
            ("platform_meta", [], PP_TypeValidationError),
        ],
        validate_func=MasterConfig.validate,
        func_args=[[]],
    )


