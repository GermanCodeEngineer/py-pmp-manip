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
    python -m scripts.check_for_updates
    ```
2. **Ensure all tests are successful** and generate coverage report:
    ```bash
    coverage run -m pytest tests/
    ```
    ```bash
    coverage html
    ```
3. View coverage report: **Are all critical code files covered?**
4. **Update UML-Graph** of Second Representation for documentation:
    ```bash
    python -m scripts.make_uml pmp_manip.core.project SRProject
    ```
5. **Update pyproject.toml** with the new **version number** and dependencies:
    ```bash
    python -m scripts.update_pyproject_toml --version 1.2.3
    ```
6. **Build package locally**:
    ```bash
    pip install --upgrade build
    python -m build
    ```
7. **Run docker install test**:
    ```bash
    docker build -f install_test/Dockerfile -t package-install-test .
    docker run --rm package-install-test
    ```
8. **Commit and Push all changes** (Just an Example):
    ```bash
    git add -A
    git commit -m "prepare next release"
    git push
    ``` 
9. **Create a Git tag with the version number and Push** the tag to your remote:
    ```bash
    git tag v1.2.3
    git push origin v1.2.3
    ```
10. **Verify CI passes on the release tag** (GitHub Actions)
