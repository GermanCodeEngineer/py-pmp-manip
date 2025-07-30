# Configuration System – `pmp_manip.config`

This module handles centralized configuration for the `pmp_manip` project. It allows setting and validating all configuration parameters exactly once, after which they are **deeply frozen** to prevent further modification.

For field-specific documentation, refer to the table at the bottom.

---

## Overview

The configuration system is composed of several modular configuration dataclasses:

- `ExtInfoGenConfig`
- `ValidationConfig`
- `PlatformMetaConfig`

These are composed into a single root config: `MasterConfig`, which is initialized and accessed globally throughout the project.

---

## Initialization

### `init_config(config: MasterConfig) -> None`

Initializes the global configuration with a fully populated `MasterConfig`. This function **must only be called once**, ideally at application startup.

- Validates the full config tree via `.validate()`
- Sets all sub-configs and the master config as immutable
- Subsequent calls to `init_config()` will raise an error

**Raises:**  
`ConfigurationError` – if config has already been initialized

---

## Accessing Configuration

### `get_config() -> MasterConfig`

Returns the globally set, frozen configuration. Should be used by all internal modules to access config values.

**Raises:**  
`ConfigurationError` – if config hasn't been initialized yet

---

## Default Configuration

### `get_default_config() -> MasterConfig`

Returns a pre-built `MasterConfig` with safe, reasonable defaults. This can be used:

- As a base for testing
- To bootstrap the system with minimal input
- For default-based override logic

---

## Configuration Fields

| argument                                | type               | purpose                                                                                                              | default                               |
|-----------------------------------------|--------------------|----------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| gen_opcode_info_dir                     | directory path str | directory used to store the generated <br>extension opcode info files in                                             | "example_extensions/gen_opcode_info/" |
| js_fetch_interval                       | datetime.timedelta | if the extension is accessed through a link, <br>it will only be fetched again after this interval has passed        | timedelta(days=3)                     |
| raise_if_monitor_position_outside_stage | bool               | during validation an ValidationError will be raised <br>if a monitor's position is outside the stage edges           | True                                  |
| raise_if_monitor_bigger_then_stage      | bool               | during validation an ValidationError will be raised <br>if a list monitor's size is bigger then the stage            | True                                  |
| stage_width                             | int                | used to calculate the above two raise_if... and to calculate <br>monitor positions seen from the center of the stage | 480                                   |
| stage_height                            | int                | used to calculate the above two raise_if... and to calculate <br>monitor positions seen from the center of the stage | 360                                   |
| scratch_semver                          | version no. str    | holds up to date version of Scratch <br>for project meta generation                                                  | "3.0.0"                               |
| scratch_vm                              | version no. str    | holds up to date version of the Scratch VM.<br>"                                                                     | "11.1.0"                              |
| penguinmod_vm                           | version no. str    | holds up to date version of the PenguinMod VM.<br>"                                                                  | "0.2.0"                               |

---

## Example Usage

---

### Method 1: Override from Default Config (Recommended)

```python
from pmp_manip import (
    init_config, get_config, get_default_config,
)

# Start from defaults
cfg = get_default_config()

# Override only the fields you want to change
cfg.ext_info_gen.gen_opcode_info_dir = "my/overridden/path"
cfg.validation.raise_if_monitor_position_outside_stage = False


# Initialize with modified config
init_config(cfg)

# ... Use the pmp_manip module however you want from here
```

### Method 2: Full Manual Initialization

```python
from pmp_manip import (
    init_config, get_config,
    ExtInfoGenConfig, ValidationConfig,
    PlatformMetaConfig, MasterConfig,
)
from datetime import timedelta

# Initialize once, early in main
init_config(MasterConfig(
    ext_info_gen=ExtInfoGenConfig(
        gen_opcode_info_dir="my/output/dir",
        js_fetch_interval=timedelta(days=2),
    ),
    validation=ValidationConfig(
        raise_if_monitor_position_outside_stage=True,
        raise_if_monitor_bigger_then_stage=False,
    ),
    platform_meta=PlatformMetaConfig(
        scratch_semver="3.0.0",
        scratch_vm="11.1.0",
        penguinmod_vm="0.2.0",
    ),
))

# ... Use the pmp_manip module however you want from here
```

