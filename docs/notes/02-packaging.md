# Packaging

The general advice [now seems](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html) to support using `pyproject.toml` over just `setup.py` for relativley simple builds.

- If the project is pure python and relatively straightforward, doesn't really matter how you package.
- As packages get more complex (e.g., C and other non-python dependencies), it becomes harder and `setup.py` or even conda-only packaging may be required.

## Build and deploy

In this template, we use python's `setuptools` to handle the building and deployment of the package. There are many others, such as [Poetry](https://python-poetry.org/), but `setuptools` is sufficient for our purposes here, and I find the others confusing. You can look at [PyOpenSci's packaging guide](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html#) for some more info on the other possibilities.

We handle the building and deployment of our package with Github actions, which take advantage of the fact that Github actions are a PyPI [trusted publisher](https://docs.pypi.org/trusted-publishers/) and thus don't require us to set up API tokens or use username / password for authentication. You can do all the following manually from your local machine, but deploying to PyPI or Test PyPI will require using one of those two other methods for authentication (building does not).

### Build

Assuming your `pyproject.toml` is appropriately set up, you can build your package with the following lines:

```bash
pip install build # only run the first time
python -m build --outdir dist/ --sdist
```

### Deploy

Finally, we deploy our projects to the [python packaging index](https://pypi.org/) so they can be installed easily with `pip`. If the package is pure python, that's probably sufficient. If the project has extensive C or other non-python dependencies, `conda` deployment may be more appropriate.

We deploy to pypi every release, and we follow [semantic versioning](https://semver.org/) for release labeling (see [workflow notes](00-workflow.md) for more details on when to release and how this labeling works). We do this by making use of continuous integration (CI) on github actions. See the [CI](07-ci.md) notes for more on CI and Github actions in general; in the following section we discuss specifically how to use our `deploy` action, which is defined in `.github/workflows/deploy.yml`. The following is based on [this guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/) from the python packaging authority and makes use of [their action](https://github.com/pypa/gh-action-pypi-publish) and the fact that Github actions is one of PyPI's [trusted publisher](https://docs.pypi.org/trusted-publishers/) (also discussed in the action's readme).

This action gets triggered on every github release and does the following:

1. Build the package, as above.
2. Deploy the package to Test PyPI.

### Using this yourself

When using this yourself, copy over the `deploy.yml` file to `.github/workflows`, update the `environment:url` to point to your project and remove the `test` subdomain, as noted in the comments. This action may also require you to already have an account on the [PyPI](https://pypi.org/) and [Test PyPI](https://test.pypi.org/), but I'm not sure.

