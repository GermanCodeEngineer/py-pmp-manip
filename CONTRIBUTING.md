# Contributing to py-pmp-manip

**Thanks for your interest in contributing! 🎉**
We welcome bug reports, feature requests, documentation improvements, and code contributions.
Do not be afraid to ask questions or create issues!

---

## 🐛 Reporting Issues
- Use the [GitHub Issues](https://github.com/GermanCodeEngineer/py-pmp-manip/issues).
- Include as much detail as possible:
  - Python version (`python --version`)
  - OS and environment (Linux, macOS, Windows, Docker, etc.)
  - Steps to reproduce the issue
  - Expected vs actual behavior

---

## 🛠 Development Setup
1. Fork the repository and clone your fork.
2. Make sure you’re using **Python 3.12+**.
3. Install dependencies (including dev tools):

   ```bash
   pip install -e ".[dev]"
   ```

This installs the project in editable mode plus testing tools.

---

## 🧪 Running Tests

We use **pytest**:

```bash
pytest
```

Add tests for any new functionality in the `tests/` folder.

---

## 🚀 Making Changes

* Create a new branch from `main`:

  ```bash
  git checkout -b feature/my-new-feature
  ```

* Write clear commit messages (e.g., `fix: handle missing pmp metadata`).

* Run tests before pushing:

  ```bash
  pytest
  ```

---

## 📦 Pull Requests

* Make sure your PR:

  * Passes all tests
  * Adds/updates documentation if needed
  * Targets the `main` branch
* Describe *why* you made the change and *what* it does.
* Draft PRs are welcome if you want early feedback.

---

## 💡 Style Guide

* Follow [PEP 8](https://peps.python.org/pep-0008/).

* Use [pytest naming conventions](https://docs.pytest.org/en/stable/goodpractices.html#test-discovery) (`test_*.py`).

---

## 📜 Licensing

By contributing, you agree that your contributions will be licensed under the project’s [GPL-3.0-or-later license](LICENSE).

---

## 🙌 Need Help?

If you get stuck:

* Open a [discussion](https://github.com/GermanCodeEngineer/py-pmp-manip/discussions)
* Or ask in the relevant issue
