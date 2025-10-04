# 🐧 py-pmp-manip

> A modular python tool for creating, editing and inspecting Penguinmod(.pmp) and Scratch(.sb3) project files.

---

## 🚀 Features

- Loading and Creating Projects
- Editing Projects
- Inspecting Projects
--- 
For a **documentation overview** and a **broader usage tutorial**, see [docs/index.md](docs/index.md) 

---

## 📦 Installation

```bash
pip install py-pmp-manip
```
**Or clone** directly. Do not forget to **include submodules**:
```bash
git clone --recurse-submodules https://github.com/GermanCodeEngineer/py-pmp-manip.git
cd py-pmp-manip
pip install -e .
```

## 🧰 Basic Usage

Before using most parts of pmp_manip, you must initialize the configuration once:

```python
from pmp_manip import init_config, get_default_config

# Start from defaults and override what you need
cfg = get_default_config()
cfg.ext_info_gen.gen_opcode_info_dir = "output/gen_opcode_info"
init_config(cfg)
```
### References
* For more **config details**, see [docs/config.md](docs/config.md)
* For a **documentation overview** and a **broader usage tutorial**, see [docs/index.md](docs/index.md)

---

## 📁 Project Structure
```
py-pmp-manip/
├── pmp_manip/              # Source Code
│   ├── config/             # Configuration schema and lifecycle
│   ├── core/               # Core functionality
│   ├── ext_info_gen/       # Information generator for custom extensions
│   ├── important_consts.py # Common important constants
│   ├── opcode_info/        # Contains an API for and the information about all the blocks
│   │   ├── api/                 # Theoretical structure of the API
│   │   ├── data/                # Actual data for the API
│   │   └── doc_api/             # A seperate API, which gives information about blocks and monitors in a human-readable way 
│   ├── builtin_extension_source/ # Resource Submodule: Adapted Built-in PenguinMod Extensions
│   └── utility/            # Utilities for other modules
├── docs/              # Documentation
├── scripts/           # Independent project-related scripts for developers
│   ├── check_for_updates.py     # Checks for updates in foreign code files, from which e.g. constants are derived
│   ├── make_uml.py              # Generates a UML-Diagram for Second Representation
│   └── update_pyproject_toml.py # Updates pyproject.toml with version and dependencies
└── tests/             # Unit tests
```

## 🧪 Running Tests

Just run:
```bash
pytest tests/
```

---

## 📄 License

GPLv3

---

## 🤝 Contributing

Pull requests, issues, and feedback are welcome!
Please read the [CONTRIBUTING.md](CONTRIBUTING.md) guide before submitting code. 

---
