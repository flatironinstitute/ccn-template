# Packaging

The general advice [now seems](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html) to support using `pyproject.toml` over just `setup.py` for relativley simple builds.

- If the project is pure python and relatively straightforward, doesn't really matter how you package.
- As packages get more complex (e.g., C and other non-python dependencies), it becomes harder and `setup.py` or even conda-only packaging may be required.

## pyproject.toml

We follow the advice of
[pyopensci](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html)
and use `pyproject.toml` to specify build requirements and metadata (rather than
`setup.py`), a template for which is included here. Metadata includes the
authors, a brief description, homepage url, etc. which will all be rendered in
the PyPI sidebar, for example. Build requirements include, at a minimum, the
dependencies, and potentially other installation instructions to pass to `pip`.

The primary goal is to end up with an installation that can be completed with a
single `pip install` command.

### Optional dependencies

We also make use of optional dependencies, as specified under the
`[project.optional-dependencies]` header in the `pyproject.toml` file. Each of
these is a python list, of the form: 

```toml
dependency_bundle = [
    'python_package',
    'python_package_2 > 1.0'
]
```

This optional bundle of dependencies can be installed with bracket syntax: `pip
install ccn-template[dependency_bundle]` (or `pip install .[dependency_bundle]`
if we're installing from a local copy). See
[docs](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#dependencies-optional-dependencies)
for more info about how to specify dependencies.

We require the use of two optional dependency bundles: `dev` and `docs`. `docs`
includes `mkdocs` and plugins required to build the documentation, as installed
by `readthedocs` and described a bit more in [the documentation
notes](03-documentation.md). `dev` includes `pytest` and the linters, as
installed by `tox` and GitHub Actions for continuous integration; see [the
testing notes](05-linters-and-tests.md) for more info.

## Build

TODO: Also need to have guidance on [build tools](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html)

## Resources
Potentially useful decision tree image from Pyopensci     
![python-package-tools-decision-tree](https://github.com/flatironinstitute/ccn-template/assets/6643322/2bc2f9a0-c989-4b0a-92d1-ec52693400fc)
