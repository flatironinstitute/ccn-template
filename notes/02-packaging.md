# Packaging

The general advice [now seems](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html) to support using `pyproject.toml` over just `setup.py` for relativley simple builds.

- If the project is pure python and relatively straightforward, doesn't really matter how you package.
- As packages get more complex (e.g., C and other non-python dependencies), it becomes harder and `setup.py` or even conda-only packaging may be required.

## Resources

