# Packaging

The general advice [now seems](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html) to support using `pyproject.toml` over just `setup.py` for relativley simple builds.

- If the project is pure python and relatively straightforward, doesn't really matter how you package.
- As packages get more complex (e.g., C and other non-python dependencies), it becomes harder and `setup.py` or even conda-only packaging may be required.

Note that, like many topics touched on in this repo, packaging, building, and deploying are big topics. I recommend looking at the following resources for more info:

- Read the [python packaging guide](https://pypackaging-native.github.io/) for a high-level overview of this topic.
- Read [pyOpenSci's packaging guide](https://www.pyopensci.org/python-package-guide/package-structure-code/intro.html) for information about the possible choices you can make. We recommend one way of handling these choices, this guide provides information about the other possibilities.
- Refer to [PyPA's packaging overview](https://packaging.python.org/en/latest/overview/) for the most authorative (and detailed) information about this topic. [The "packaging and distributing projects" page](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/), in particular, covers a lot of details you may want to refer to.

## Background

The primary goal is to end up with an installation that can be completed with a single `pip install` command. If you're reading this guide, your end users are probably scientists, and they want to be able to install something and have it *just work*. So providing them with a simple installation procedure is critical: if users can't install your package, they won't use it. Unfortunately, as in many fields,  something that appears simple to the end user is generally not simple for the creator. Here, we do our best to provide a minimal working example that will cover most use-cases for writers of high-level scientific code.

Before we get started, it's important to understand that there are two types of files you can distribute via `pip`: source distribution (in python, often referred to as "sdist" and normally stored as `.tar.gz` archives) and binaries (in python, these are generally "wheel files", zip-format archives with extension `.whl`). Typically, you'll distribute both.

- Source distribution are the raw files, as stored on GitHub (or whatever platform you use), and will require the user's computer to build the package itself. For pure python packages, this is probably not a problem, as the user will need to have python anyway. However, if you have non-python compiled dependencies (called "native dependencies" for some reason), this will get more complicated. For example, if you cdepend on C or C++ code, the user will need to have a C compiler, which Windows machines do not have by default.
- Binary files are the already built / compiled source files. They include everything necessary and are ready to be installed directly. They're thus faster to install and less likely to run into user- or operating system-specific issues. However, this means that the developer might need to build and upload to PyPI separate wheels for each operating system they wish to support. However, if you have no compiled extensions, you can produce a "universal" or ["pure python" wheel](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#pure-python-wheels) (so-called because all of your code is in python), which will work on all operating systems.

In this note, we'll discuss how to build and upload your library using `deploy.yml`, a GitHub action which handles as much of this as possible for you: it will build the source distribution and wheel files, check that installation is possible, run some tests, and upload to PyPI.

## pyproject.toml

We follow the advice of [pyopensci](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html) and use `pyproject.toml` to specify build requirements and metadata (rather than `setup.py`), a template for which is included in this repo. Metadata includes the authors, a brief description, homepage url, etc. which will all be rendered in the PyPI sidebar, for example. Build requirements include, at a minimum, the dependencies, and potentially other installation instructions to pass to `pip`.

### Optional dependencies

We also make use of optional dependencies, as specified under the `[project.optional-dependencies]` header in the `pyproject.toml` file. Each of these is a python list, of the form:

```toml
dependency_bundle = [
    'python_package',
    'python_package_2 > 1.0'
]
```

This optional bundle of dependencies can be installed with bracket syntax: `pip install ccn-template[dependency_bundle]` (or `pip install .[dependency_bundle]` if we're installing from a local copy). See [docs](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#dependencies-optional-dependencies) for more info about how to specify dependencies.

We require the use of two optional dependency bundles: `dev` and `docs`. `docs` includes `mkdocs` and plugins required to build the documentation, as installed by `readthedocs` and described a bit more in [the documentation notes](03-documentation.md). `dev` includes `pytest` and the linters, as installed by `tox` and GitHub Actions for continuous integration; see [the testing notes](05-linters-and-tests.md) for more info.

## Build and deploy

In this template repo, we use python's `setuptools` to handle the building and deployment of the package. There are many other choices, such as [Poetry](https://python-poetry.org/), but `setuptools` is sufficient for our purposes here, and I find the others confusing. You can look at [PyOpenSci's packaging guide](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html#) for some more info on the other possibilities (note, however, that I'm not sure how they interact with `cibuildwheel`, if you'll be using that option).

We handle the building and deployment of our package with Github actions, which take advantage of the fact that Github actions are a PyPI [trusted publisher](https://docs.pypi.org/trusted-publishers/) and thus don't require us to set up API tokens or use username / password for authentication. You can do all the following manually from your local machine, but deploying to PyPI or Test PyPI will require using one of those two other methods for authentication (building does not).

The following will first describe how to do this locally, then describe the Github actions and how to use them yourself.

We provide two different Github actions for handling these steps: `deploy-pure-python.yml` and `deploy-cibw.yml` (`cibw` = "CI build wheel"). If your package is pure python, use `deploy-pure-python.yml`, otherwise use `deploy-cibw.yml`. If you're not sure, run `pip install build; python -m build --wheel` and then `ls dist/*.whl`. If your output looks like `package-version-py3-none-any.whl`, it's pure python. If it includes the name of your OS in the filename, it is package-specific and you should use `deploy-cibw.yml`.

### Build

Assuming your `pyproject.toml` is appropriately set up, you can build your package with the following lines:

```bash
pip install build # only run the first time
python -m build --outdir dist/ --sdist --wheel
```

This will build the source distribution and wheel for your system.

If using `deploy-cibw.yml`, you might want to be able to run `cibuildwheel` locally, in
order to check against what's happening in the Github action. To do so, see [the cibuildwheel documentation](https://cibuildwheel.readthedocs.io/en/stable/setup/#local) for how to install and run it. Note that you'll need [docker](https://www.docker.com/products/docker-desktop) installed to build the Linux wheel (which is possible from any OS); if you wish to build the macOS or Windows wheel, you'll need that operating system (see cibuildwheel docs for more info).

As mentioned above, if your package has no compiled extensions (like this `ccn-template` repo!), then you don't need a platform-specific wheel, only a pure python wheel. In this case, `cibuildwheel` will actually raise an exception (see [this issue](https://github.com/pypa/cibuildwheel/issues/255) for the initial idea, and [this issue](https://github.com/pypa/cibuildwheel/issues/1021) for a longer discussion), and locally you can just rely on the `python -m build --wheel` command above.

### Deploy

Finally, we deploy our projects to the [python packaging index](https://pypi.org/) so they can be installed easily with `pip`.

To manually upload your package to PyPI (and test PyPI), you would use [twine](https://twine.readthedocs.io/en/stable/) after building the source distribution and wheel files: `twine upload dist/*` for PyPI, `twine upload -r testpypi dist/*` for Test PyPI. However, we *strongly* recommend only using the Github action to upload to PyPI: once you upload a package with a specific version number to PyPI, you cannot overwrite it or re-upload the same package with the same version (you can "yank" a specific version, warning users about a version you don't want them to install). Therefore, we recommend being very careful around this.

### Github Actions

We deploy to PyPI every release, and we follow [semantic versioning](https://semver.org/) for release labeling (see [workflow notes](00-workflow.md) for more details on when to release and how this labeling works; this repo's `CONTRIBUTING.md` document also includes some suggested language for explaining the procedure to ccontributors). We do this by making use of continuous integration (CI) on github actions. See the [CI](07-ci.md) notes for more on CI and Github actions in general; in the following sections we discuss specifically how to use our `deploy` actions, which are defined in `.github/workflows/deploy-pure-python.yml` and `.github/workflows/deploy-cibw.yml` (see the [build](#build) section for guidance on which you should use).

#### Pure python

The following is based on [this guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/) from the python packaging authority and makes use of [their action](https://github.com/pypa/gh-action-pypi-publish) and the fact that Github actions is one of PyPI's [trusted publisher](https://docs.pypi.org/trusted-publishers/) (also discussed in [the action's readme](https://github.com/pypa/gh-action-pypi-publish#trusted-publishing)).

This action gets triggered on every github release and does the following:

1. Build the package, as above.
2. Check that the version number created by `setuptools_scm` matches the most recent git tag.
2. Test that the package can be installed from the wheel.
3. Run some tests.
4. Deploy to Test PyPI.

### Using this yourself

To use this action yourself:

1. Ensure `deploy.yml` is in your `.github/workflows` directory.
2. Create an account on both [PyPI](https://pypi.org/) and [Test PyPI](https://test.pypi.org/). 
3. Follow the steps on the [pypi docs](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) to create a PyPI project with a trusted publisher. **NOTE:** do this for both PyPI and Test PyPI --- we'll be using both!
    - Set the workflow name to `deploy.yml` and environment name to `pypi`.
    
I THINK there's something weird here where the github commit sha during a pull request is one off (but one triggered by release publishing wouldn't be ), see https://github.com/actions/checkout/issues/919#issue-1366203424. 
