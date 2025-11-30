# Publishing to PyPI

This guide explains how to publish the `matrix-coder-agent` package to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account at [https://pypi.org/](https://pypi.org/)
2. **Test PyPI Account** (optional but recommended): Create an account at [https://test.pypi.org/](https://test.pypi.org/)
3. **API Token**: Generate an API token from your PyPI account settings

## Installation

Install build and publishing tools:

```bash
pip install build twine
```

## Building the Package

1. Clean previous builds:
```bash
rm -rf build/ dist/ *.egg-info
```

2. Build the package:
```bash
python -m build
```

This creates two files in the `dist/` directory:
- A source distribution (`.tar.gz`)
- A wheel distribution (`.whl`)

## Testing Locally

Before publishing, test the package locally:

```bash
pip install dist/matrix_coder_agent-0.1.0-py3-none-any.whl
```

Run the CLI:
```bash
matrix-coder-agent
```

Or test the import:
```python
from matrix_coder_agent import StrandsFileAgent
agent = StrandsFileAgent()
```

## Publishing to Test PyPI (Recommended First Step)

1. Create `~/.pypirc` with Test PyPI credentials:
```ini
[testpypi]
  username = __token__
  password = pypi-YOUR_TEST_PYPI_TOKEN_HERE
```

2. Upload to Test PyPI:
```bash
python -m twine upload --repository testpypi dist/*
```

3. Test installation from Test PyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ matrix-coder-agent
```

## Publishing to PyPI

1. Update `~/.pypirc` with PyPI credentials:
```ini
[pypi]
  username = __token__
  password = pypi-YOUR_PYPI_TOKEN_HERE
```

2. Upload to PyPI:
```bash
python -m twine upload dist/*
```

3. Verify the upload at [https://pypi.org/project/matrix-coder-agent/](https://pypi.org/project/matrix-coder-agent/)

4. Install from PyPI:
```bash
pip install matrix-coder-agent
```

## Version Management

Before each release:

1. Update the version number in:
   - `src/matrix_coder_agent/__init__.py`
   - `setup.py`
   - `pyproject.toml`

2. Update the changelog in `README.md`

3. Create a git tag:
```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

## Troubleshooting

### Common Issues

**1. Package name already exists**
- Choose a unique package name or namespace

**2. Upload fails with 403 error**
- Verify your API token is correct
- Check that you have permission to upload

**3. Build fails**
- Ensure all required files are present
- Check `MANIFEST.in` includes necessary files

**4. Import errors after installation**
- Verify package structure with `pip show matrix-coder-agent`
- Check `__init__.py` exports

### Validation Before Publishing

Run these checks:

```bash
# Check package metadata
python setup.py check

# Validate README
python -m readme_renderer README.md

# Check distribution
twine check dist/*
```

## GitHub Actions (Optional)

Create `.github/workflows/publish.yml` for automated publishing:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: twine upload dist/*
```

Add your PyPI token as a GitHub secret named `PYPI_TOKEN`.

## Best Practices

1. **Always test on Test PyPI first**
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Keep a changelog** in README or separate CHANGELOG.md
4. **Tag releases** in git
5. **Write comprehensive documentation**
6. **Include LICENSE file**
7. **Add badges** to README (PyPI version, downloads, etc.)
8. **Test on multiple Python versions** before publishing

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
