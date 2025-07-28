# 🐧 PyPenguin

> A modular python tool for creating, editing and inspecting Penguinmod(.pmp) and Scratch(.sb3) project files.

---

## 🚀 Features

- [Creating ...](docs/creating.md)
- [Editing ...]
- [Inspecting ...]
... Project files

---

## 📦 Installation

```bash
pip install pypenguin
```
Or clone directly:
```bash
git clone https://github.com/Fritzforcode/pypenguin.git
cd pypenguin
pip install -e .
```

## 🛠️ Building Tree-sitter Parser

Before using custom extension info generator-related features, you must build the Tree-sitter language library:

python scripts/build_tree_sitter_lib.py

This builds the parser binary used internally by the extension info generator system.

---


## 🧰 Basic Usage

Before using most parts of pypenguin, you must initialize the configuration once:

```python
from pypenguin import init_config, get_default_config

# Start from defaults and override what you need
cfg = get_default_config()
cfg.ext_info_gen.gen_opcode_info_dir = "output/gen_opcode_info"
init_config(cfg)
```

For more config details, see [docs/config.md](docs/config.md)


---

## 📁 Project Structure
```
pypenguin/
├── pypenguin/         # Source Code
│   ├── config/               # Configuration schema and lifecycle
│   ├── core/                 # Core functionality
│   ├── ext_info_gen/         # information generator for custom extensions
│   ├── opcode_info/          # Contains an API for and the information about all the blocks
│   ├── utility/              # Utilities for other modules
│   ├── important_consts.py   # Common important constants
│   └── tree_sitter_loader.py # Interface for access to the tree sitter JavaScript library
├── docs/              # Documentation
├── tests/             # Unit tests
└── scripts/           # Independent project-related scripts
    └── build_tree_sitter_lib.py # Set up tree sitter JavaScript library
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
Please read the CONTRIBUTING.md guide before submitting code. 
\# TODO

---
