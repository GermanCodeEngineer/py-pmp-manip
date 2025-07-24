# 🐧 PyPenguin

> A modular python tool for creating, editing and inspecting Penguinmod(.pmp) and Scratch(.sb3) project files.

---

## 🚀 Features

- [Creating ...]
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

---

🧰 Basic Usage

Before using most parts of pypenguin, you must initialize the configuration once:

```python
from pypenguin.config import init_config, get_default_config

# Start from defaults and override what you need
cfg = get_default_config()
cfg.ext_info_gen.gen_opcode_info_dir = "output/gen_opcode_info"
init_config(cfg)
```

For more config options, see [docs/config.md](docs/config.md)


---

📁 Project Structure

pypenguin/
├── pypenguin/
│   ├── core/              # Core functionality
│   ├── ext_info_gen/      # information generator for custom extensions
│   ├── config/            # Configuration schema and lifecycle
│   ├── opcode_info/       # Contains an API for and the information about all the blocks
│   └── utility/           # Utilities for other modukes
├── docs/              # Documentation
└── tests/             # Unit tests


🧪 Running Tests

```bash
pytest
```

---

📄 License

GPLv3

---

🤝 Contributing

Pull requests, issues, and feedback are welcome!
Please read the CONTRIBUTING.md guide before submitting code. 
# TODO

---
