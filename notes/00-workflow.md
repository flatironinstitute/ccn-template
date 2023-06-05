# Workflow

![Workflow](gitflow.jpg)



Use git flow: `main` branch is for releases, `development` for development, both should be stable (all tests must pass), but development branch gives an extra for fixing bugs.

1. Read [CaImAn CONTRIBUTING](https://github.com/flatironinstitute/CaImAn/blob/dev/CONTRIBUTING.md)
2. Create `development` branch.
3. Protect `main` and `development` branches so they can't be pushed to, see [docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)

## General workflow:
- pick an issue or feature to develop and create a new branch off of `development`.
- when ready, open a pull request (to `development`) and address any issues that come up, including ensuring that tests pass
- merge into `development`.
- after enough time or enough changes, merge into `main` and make a release.
- releases should follow [semantic versioning](https://semver.org/) and deploy to `pypi` (and optionally `conda`), see packaging and continuous integration: 

```
Given a version number MAJOR.MINOR.PATCH, increment the:
  -  MAJOR version when you make incompatible API changes
  -  MINOR version when you add functionality in a backward compatible manner
  -  PATCH version when you make backward compatible bug fixes
```

## Decision-making / gate-keeping

- Every repo should have a [CODEOWNER](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) who must approve any PR before merge into `development` and `main`.
- Code owner can decide whether they want secondary approval from someone, which can be enforced by Github through branch protection rules.

## Resources:
- [scikit-learn contributing](https://scikit-learn.org/stable/developers/contributing.html)
- [matplotlib contributing](https://matplotlib.org/stable/devel/index.html)
- [GitKraken](https://www.gitkraken.com/learn/git/git-flow)
- [Gitlab complex image](https://docs.gitlab.com/ee/topics/img/gitlab_flow_gitdashflow.png)
