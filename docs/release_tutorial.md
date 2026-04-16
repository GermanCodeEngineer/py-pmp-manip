# Preparing a New Release

### **1. Core Functionality**

* ✅ All planned features for the initial release should be implemented.
* ✅ Features should work as expected; no critical bugs that break core functionality.
* ✅ Edge cases and error handling should be covered.

---

### **2. Code Quality**

* ✅ Code is clean, readable, and follows PEP 8 style conventions.
* ✅ Functions and classes are well-organized; modular design.
* ✅ Unused code, debug prints, and commented-out sections are removed.
* ✅ Temporary files and file calls are removed.
* ✅ Proper exception handling is in place.

---

### **3. Testing**

* ✅ Unit tests cover critical functionality.
* ✅ Optional: Integration tests to ensure components work together.
* ✅ All tests pass consistently.

---

### **4. Stability & Security**

* ✅ No hard-coded secrets (API keys, passwords) in the repo.
* ✅ Avoid known security vulnerabilities in dependencies.
* ✅ Graceful shutdown and resource cleanup (files, network connections).

---

# Next Steps
1. **View all changes in foreign code sources**, which this project derives information from:
    ```bash
    python -m scripts.check_source_updates
    ```
2. **Check for dependency updates** to see if newer versions are available:
    ```bash
    python -m scripts.check_dependency_updates
    ```
3. **Bundle required npm JS files** for pip distribution (if needed):
    ```bash
    python -m scripts.bundle_npm_package
    ```
   This will place the JS file in `pmp_manip/builtin_extension_source/` by default.
4. **Ensure all tests are successful** and generate coverage report:
    ```bash
    coverage run -m pytest tests/
    ```
    ```bash
    coverage html
    ```
5. View coverage report: **Are all critical code files covered?**
6. **Update UML-Graph** of Second Representation for documentation:
    ```bash
    python -m scripts.make_uml pmp_manip.core.project SRProject
    ```
7. **Review pyproject.toml** with the new dependencies:
    ```bash
    python -m scripts.review_pyproject_toml
    ```
8. **Follow suggested changes and increase version number**
9. **Build package locally**:
    ```bash
    pip install --upgrade build
    python -m build
    ```
10. **Commit and Push all changes** (Just an Example):
    ```bash
    git add -A
    git commit -m "prepare next release"
    git push
    ```
11. **Create a Git tag with the version number and Push** the tag to your remote:
    ```bash
    git tag v1.2.3
    git push origin v1.2.3
    ```
12. **Verify CI passes on the release tag** (GitHub Actions)
