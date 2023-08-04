# CONTRIBUTING

This file is intended for contributors, so it should describe how they can get
involved, what type of involvement you are looking for, and the procedures you
follow (e.g., how do you decide whether to merge a pull request, how do you make
releases, etc.).

# Example contents

## Releases

We create releases on Github, deploy on / distribute via [pypi](https://pypi.org/), and try to follow [semantic versioning](https://semver.org/):

> Given a version number MAJOR.MINOR.PATCH, increment the:
> 1. MAJOR version when you make incompatible API changes
> 2. MINOR version when you add functionality in a backward compatible manner
> 3. PATCH version when you make backward compatible bug fixes

This is a goal and, in practice, it's difficult to determine what a "breaking change" may be. So in practice, major, minor, and patch versions can be more realistically interpreted as follows (proposed by Henry Schreiner):

> A more realistic form of SemVer, and a better way to think about it, is as an abbreviated changelog and author intent. In this form:
>  - Bumping a patch version means there’s nothing to see, just fixing things, you are probably fine.
>  - Bumping a minor version means that there might be interesting things to see, but nothing you have to see.
>  - Bumping a major version means you really should look, changes might even be needed for users.


When doing a new release, the following steps must be taken:
1. In a new PR:
  - Update all the [binder](https://mybinder.org) links, which are of the form `https://mybinder.org/v2/gh/flatironinstitute/ccn-template/X.Y.Z?filepath=examples`, which are found in `README.md` and `docs/index.md`, and some of the tutorial notebooks found in `examples/`. Note that the version tag must match the github tag (specified in the next step) or the link won't work.
2. After merging the above PR into the `main` branch, [create a Github release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) with a new tag matching that used in the binder link above: `X.Y.Z`. Creating the release will trigger the deployment to pypi, via our `deploy` action (found in `.github/workflows/deploy.yml`). The built version will grab the version tag from the Github release, using [setuptools_scm](https://github.com/pypa/setuptools_scm).

I have been unable to find a way to make binder use the latest github release tag directly (or make [binder](https://mybinder.org) use a `latest` tag, like [readthedocs](https://readthedocs.org/) does), so ensure they match!
