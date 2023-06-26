# Packaging

The general advice [now seems](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html) to support using `pyproject.toml` over just `setup.py` for relativley simple builds.

- If the project is pure python and relatively straightforward, doesn't really matter how you package.
- As packages get more complex (e.g., C and other non-python dependencies), it becomes harder and `setup.py` or even conda-only packaging may be required.

## Build

TODO: Also need to have guidance on [build tools](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html)

## Deploy

Finally, we deploy our projects to the [python packaging index](https://pypi.org/) so they can be installed easily with `pip`. If the package is pure python, that's probably sufficient. If the project has extensive C or other non-python dependencies, `conda` deployment may be more appropriate.

We deploy to pypi every release, and we follow [semantic versioning](https://semver.org/) for release labeling (see [workflow notes](00-workflow.md) for more details on when to release and how this labeling works). We do this by making use of continuous integration (CI) on github actions. See the [CI](07-ci.md) notes for more on CI and Github actions in general; in the following section we discuss specifically how to use our `deploy` action, which is defined in `.github/workflows/deploy.yml`. The following is based on [this guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/) from the python packaging authority and makes use of [their action](https://github.com/pypa/gh-action-pypi-publish).

This action gets triggered on every github release and does the following:

1. Deploy the package to Test PyPI,

## Resources
Potentially useful decision tree image from Pyopensci     
![python-package-tools-decision-tree](https://github.com/flatironinstitute/ccn-template/assets/6643322/2bc2f9a0-c989-4b0a-92d1-ec52693400fc)
