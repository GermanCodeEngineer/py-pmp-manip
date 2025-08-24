from dataclasses import FrozenInstanceError
from datetime    import timedelta
from pytest      import raises

from pmp_manip.utility import grepr_dataclass, AbstractTreePath, MANIP_TypeValidationError

from pmp_manip.config.manager import get_default_config
from pmp_manip.config.schema  import ConfigBase, MasterConfig, ExtInfoGenConfig, ValidationConfig, PlatformMetaConfig

from tests.utility import execute_attr_validation_tests


@grepr_dataclass(grepr_fields=["a"])
class TEST_Config(ConfigBase):
    a: int

    def validate(self, path: AbstractTreePath) -> None: # to fulfill abstractmethod
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
    handler = (lambda source: source == "https://raw.githubusercontent.com/Logise1123/FirebaseDB-/refs/heads/main/db.js")
    config = ExtInfoGenConfig(
        gen_opcode_info_dir=".",
        js_fetch_interval=timedelta(days=1),
        node_js_exec_timeout=1.0,
        is_trusted_extension_origin_handler=handler,
    )
    config.validate(path=AbstractTreePath())
    
    execute_attr_validation_tests(
        obj=config,
        attr_tests=[
            ("gen_opcode_info_dir", 5, MANIP_TypeValidationError),
            ("js_fetch_interval", {}, MANIP_TypeValidationError),
            ("node_js_exec_timeout", [], MANIP_TypeValidationError),
            ("is_trusted_extension_origin_handler", "https://raw.githubusercontent.com/Logise1123/FirebaseDB-/refs/heads/main/db.js", MANIP_TypeValidationError),

        ],
        validate_func=ExtInfoGenConfig.validate,
        func_args=[[]],
    )



def test_ValidationConfig_validate():
    config = ValidationConfig(
        raise_if_monitor_position_outside_stage=False, 
        raise_if_monitor_bigger_then_stage=False,
    )
    config.validate(path=AbstractTreePath())
    
    execute_attr_validation_tests(
        obj=config,
        attr_tests=[
            ("raise_if_monitor_position_outside_stage", set(), MANIP_TypeValidationError),
            ("raise_if_monitor_bigger_then_stage", None, MANIP_TypeValidationError),
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
    config.validate(path=AbstractTreePath())
    
    execute_attr_validation_tests(
        obj=config,
        attr_tests=[
            ("scratch_semver", 31, MANIP_TypeValidationError),
            ("scratch_vm", (11, 1, 0), MANIP_TypeValidationError),
            ("penguinmod_vm", 2.0, MANIP_TypeValidationError),
        ],
        validate_func=PlatformMetaConfig.validate,
        func_args=[AbstractTreePath()],
    )



def test_MasterConfig_validate():
    config = get_default_config()
    config.validate(path=AbstractTreePath())
    
    execute_attr_validation_tests(
        obj=config,
        attr_tests=[
            ("ext_info_gen", {}, MANIP_TypeValidationError),
            ("ext_info_gen", ExtInfoGenConfig(
                    gen_opcode_info_dir=".", 
                    js_fetch_interval=3,
                    node_js_exec_timeout=1.0,
                    is_trusted_extension_origin_handler=None,
                ), MANIP_TypeValidationError),
            ("validation", config.ext_info_gen, MANIP_TypeValidationError),
            ("platform_meta", [], MANIP_TypeValidationError),
        ],
        validate_func=MasterConfig.validate,
        func_args=[AbstractTreePath()],
    )


