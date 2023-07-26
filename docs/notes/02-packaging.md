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

## pyproject.toml Configuration

### 1. `[build-system]` 

`[build-system]` defines the build system requirements for the project, specifying the dependencies and build backend used for building and packaging. You can provide the following details:

  - `requires`: A list of required dependencies for the build system.

  - `build-backend`: The build backend.

   **We recommend the following:**
    
   - [setuptools](https://setuptools.pypa.io/en/latest/): It is a fully-featured, widely-used library in Python that facilitates packaging, building, and installation of Python projects. It includes capabilities for dependency management, version management, and easy distribution of Python packages.
   - [setuptools-scm](https://pypi.org/project/setuptools-scm/): This plugin for setuptools handles managing your Python package versions using source control management (scm) metadata. It automatically derives the version of your package from the state of your version control system, such as Git or Mercurial.
   - [setuptools.build_meta](https://setuptools.pypa.io/en/latest/build_meta.html): This `setuptools` module allows you to define and configure the build system for your Python project.

   **Syntax example:**
   
   ```toml
   [build-system]
   requires = ["setuptools", "setuptools-scm"]  
   build-backend = "setuptools.build_meta"
   ```

   **Additional Informations on `setuptools-scm`:**

   How it works:

   - It examines the source code repository to determine the current version using scm metadata.
   - It simplifies versioning and release management by dynamically extracting version information from the scm system.
   - During package distribution, setuptools-scm retrieves the version number and incorporates it into the built package.
   
   What is it good for:
   
   - By using `setuptools-scm`, you can automate the versioning process and ensure accurate versioning based on the scm history. This eliminates the need for manual version specification in your project's configuration files. It will be automatically used by setuptools for managing versioning during package distribution.

   **Alternatives:**

   - [poetry](https://python-poetry.org/) or [flit](https://pypi.org/project/flit/)

### 2. `[project.optional-dependencies]`

`[project.optional-dependencies]` specifies the optional dependencies for documentation and testing/linting.

   **We recommend the following:**

   - `docs`: Documentation dependencies (see the [documentation](03-documentation.md) note for additional details).
     - [mkdocstrings[python]](https://mkdocstrings.github.io/): A MkDocs plugin that generates documentation from docstrings in Python code. It extracts information from docstrings of functions, classes, modules, and other objects.
     - [mkdocs_section_index](https://oprypin.github.io/mkdocs-section-index/): A MkDocs plugin that adds a navigation section index to the documentation sidebar. It enhances navigation by providing an index of the sections in the documentation.
     - [mkdocs_gen_files](https://oprypin.github.io/mkdocs-gen-files/): A MkDocs plugin that allows the generation of additional files during the documentation build process. It provides functionality to dynamically generate files that can be included in the documentation.
     - [mkdocs_literate_nav](https://oprypin.github.io/mkdocs-literate-nav/): A MkDocs plugin that enhances the navigation sidebar by providing collapsible sections. It improves the readability and organization of the documentation by allowing users to collapse and expand sections.
     - [mkdocs-gallery](https://smarie.github.io/mkdocs-gallery/): A MkDocs plugin that enables the creation of example galleries in the documentation. These examples are written as python scripts that are converted to jupyter notebooks when the docs are built. This combines the advantages of plain scripts (easy to version control and review) and notebooks (easy for users to run and experiment with).


   - `dev`: Developer dependencies.
     - [black](https://black.readthedocs.io/en/latest/): Code formatter. It automatically formats your Python code according to the Black code style.
     - [isort](https://isort.readthedocs.io/en/latest/): Import sorter. It automatically organizes and sorts import statements in your Python code.
     and maintain requirements.txt or pipfile.lock files.
     - [pytest](https://docs.pytest.org/en/7.3.x/): Testing framework. It is a popular testing framework for Python that allows you to write and execute tests easily.
     - [flake8](https://flake8.pycqa.org/en/latest/): Code linter. It checks your Python code for style, potential errors, and adherence to coding conventions.
     - [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/): Test coverage plugin for pytest. It integrates test coverage measurement into the pytest framework, providing coverage reports and analysis for your tests.
     - [pydocstyle](http://www.pydocstyle.org/en/latest/index.html): Docstrings linter. It checks that the docstrings in your Python code adhere to a specified convention. This is critical for maintaining a consistent style across your project's documentation, as well as ensuring that tools which automatically generate documentation from docstrings function correctly, see the [documentation note](03-documentation.md#generating-reference-documentation-from-docstrings-).     
  
  **Syntax example:**
  ```toml
    [project.optional-dependencies]
    docs = [
      'mkdocs',
      'mkdocstrings[python]',
      ...
    ]
    dev = [
      "black", 
      "isort",                       
      ...
    ]
  ```

### 3. `[tool.pytest.ini_options]` 

`[tool.pytest.ini_options]`: The additional command-line options for pytest. These options will be added by default when running `pytest`. You can provide the following details:

   - `addopts`: It defines which options are passed to pytest, run `pytest --help` for a complete list of available options.
   - `testpaths`: It specifies the directories to search for tests.
   
  **Syntax Example:**
  ```toml
  [tool.pytest.ini_options]
  addopts = "--cov=ccn_template"
  testpaths = ["tests"]
  ```

  **Additional Informations:**
  
  See the dedicated `pytest` [documentation](https://docs.pytest.org/en/latest/reference/reference.html#ini-options-ref) for detailed informations.

### 4. `[tool.pydocstyle]`

`[tool.pydocstyle]`: The additional command-line options for pydocstyle. These options will be added by default when running `pydocstyle`. We recommend to set:

   - `convention`: It defines which conventions should be followed by the docstrings. Option include [numpydoc](https://github.com/numpy/numpydoc), [google](https://google.github.io/styleguide/pyguide.html), and [pep257](http://www.python.org/dev/peps/pep-0257/).

**Syntax Example:**
```toml
[tool.pydocstyle]
convention = "numpy"                # Convention for linting (numpy, google, pep257)
```

## Resources
Potentially useful decision tree image from Pyopensci     
![python-package-tools-decision-tree](https://github.com/flatironinstitute/ccn-template/assets/6643322/2bc2f9a0-c989-4b0a-92d1-ec52693400fc)
