# dg-ignition-selenium

[![PyPI version](https://badge.fury.io/py/dg-ignition-selenium.svg)](https://pypi.org/project/dg-ignition-selenium/)

Automation library for Ignition Perspective, built on Inductive Automation's `ignition-automation-tools`. This package provides tools for automated testing of Perspective Sessions, including interactions with components, pages, and specialized helpers for Selenium integration.

**Note**: This package is not supported by Inductive Automation’s support plan. For questions, refer to the [Inductive Automation forums](https://forum.inductiveautomation.com/).

## Features

- Near 1:1 collection of Perspective components for automated testing (excluding pure SVG components and certain third-party libraries).
- Helpers for Selenium interactions, standardized assertions, and Perspective page handling.
- Support for navigating Perspective as a Single Page Application, avoiding direct HTTP requests.

## Requirements

- Python >= 3.8
- `selenium` >= 4.0.0
- WebDriver (e.g., ChromeDriver, managed via `webdriver-manager` for convenience)

## Installation

### Install from PyPI

Once published, install the package using pip:

```bash
pip install dg-ignition-selenium
```

### Setting Up Local PyPI Authentication

To authenticate with PyPI for private or test uploads (e.g., to TestPyPI), configure your PyPI credentials locally. Follow these steps:

#### Option 1: Using `~/.pypirc`

1. Create or edit the `~/.pypirc` file in your home directory.
2. Add the following configuration, replacing `<your-pypi-api-token>` with your PyPI API token (obtained from [PyPI Account Settings](https://pypi.org/manage/account/#api-tokens)):

   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = <your-pypi-api-token>

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = <your-testpypi-api-token>
   ```

3. Secure the file permissions (on Unix-like systems):

   ```bash
   chmod 600 ~/.pypirc
   ```

#### Option 2: Using Environment Variables

Alternatively, set environment variables for temporary or CI/CD use:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<your-pypi-api-token>
```

For TestPyPI, also set the repository URL:

```bash
export TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/
```

### Verify Installation

After installation, verify the package:

```bash
pip show dg-ignition-selenium
```

Test importing:

```bash
python -c "import dg_ignition_selenium; print(dg_ignition_selenium.__version__)"
```

This should output the installed version (e.g., `0.1.0`).

## Local Build Steps

To build the package locally for testing or manual uploads:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/design-group/dg-ignition-selenium.git
   cd dg-ignition-selenium
   ```

2. **Initialize Submodules**:

   The package depends on the `ignition-automation-tools` submodule:

   ```bash
   git submodule update --init --recursive
   ```

3. **Install Build Dependencies**:

   ```bash
   pip install build twine
   ```

4. **Create `__init__.py` Files**:

   Run the script to generate `__init__.py` files for the submodule:

   ```bash
   chmod +x scripts/create-init-files.sh
   ./scripts/create-init-files.sh
   ```

5. **Build the Package**:

   ```bash
   python -m build
   ```

   This creates `dist/dg_ignition_selenium-<version>-py3-none-any.whl` and `dist/dg_ignition_selenium-<version>.tar.gz`.

6. **Verify the Build**:

   ```bash
   twine check dist/*
   ```

7. **Install Locally (Optional)**:

   ```bash
   pip install dist/dg_ignition_selenium-<version>-py3-none-any.whl
   ```

8. **Upload to TestPyPI (Optional)**:

   If you’ve set up `~/.pypirc` or environment variables:

   ```bash
   twine upload --repository testpypi dist/*
   ```

   Install from TestPyPI to test:

   ```bash
   pip install --index-url https://test.pypi.org/simple/ dg-ignition-selenium
   ```

## Usage

```python
from dg_ignition_selenium import PerspectivePageObject

# Example: Initialize a Perspective page
page = PerspectivePageObject(driver=your_selenium_driver, path="/project-name/path/to/page")
page.wait_on_page_load()

# Interact with components
component = page.get_component("some_component_id")
component.set_value("new_value")
```

For detailed usage, refer to the [ignition-automation-tools documentation](https://github.com/inductiveautomation/ignition-automation-tools).

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Report issues at [GitHub Issues](https://github.com/design-group/dg-ignition-selenium/issues).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, contact [keith.gamble@bwdesigngroup.com](mailto:keith.gamble@bwdesigngroup.com).