# Documentation

Two decisions need to be made: generator and host. We'll use [MkDocs](https://www.mkdocs.org/) (instead of sphinx) for generator and [readthedocs](https://readthedocs.org/) (instead of github pages) for host.

Prefer [mkdocs-gallery](https://smarie.github.io/mkdocs-gallery/generated/tutorials/plot_parse/#download_links) to .ipynb notebooks for examples/tutorials, because it's easier to version control and review, while still being downloadable / runnable on binder as a notebook. They should live under the root directory: `examples/` (not `docs/examples/`). However, `ipynb` files can still be included (though outputs should probably be cleared), because they're easier for contributors to write and work better with interactive visualization libraries -- look into both of these. See [this](https://docs.readthedocs.io/en/stable/guides/jupyter.html) readthedocs page.

Rationale:

- MkDocs supports markdown out-of-the-box, which is much better than ReST
- readthedocs supports building documentation for PRs, which is very helpful.

## Build documentation locally

To build the documentation on your local machine, install the necessary
dependencies with `pip install -e .[docs]`, and then run `mkdocs serve`. This
builds and serves the documentation, which you can then view in your browser at
`localhost:8000` (by default, change the port by e.g., `mkdocs serve -a
localhost:8001`).

## Readthedocs setup instructions

If you use our included `.readthedocs.yml` and follow the steps below, the
documentation will be built automatically and live at
`https://ccn-template.readthedocs.org/`. The documentation will be built off the
`main` branch, and also (temporarily) for each pull request, with the link to
the pull request documentation posted back as a status check on that PR.

The root directory of this repo contains the `.readthedocs.yml` file, which
includes the configuration to work with
[readthedocs.org](https://readthedocs.org/).

By default it:

- works with mkdocs, using the `mkdocs.yml` config file.
- builds on ubuntu 22.04 and python 3.10
- installs the package using the `pip install .[docs]` command (which includes
  the optional `docs` dependencies specified in `pyproject.toml`, as described
  in the note on [packaging](02-packaging.md)).
- builds the html and pdf formats (though note that the extra formats [won't be
  built](https://docs.readthedocs.io/en/stable/guides/pull-requests.html#limitations)
  on PR builds, which we'll enable below).

However, you need to link your repo to readthedocs in order for this config file
to do anything. The following only needs to be done once per project (the
following is up to date as of 2023-06-12).

1. [Connect](https://docs.readthedocs.io/en/stable/guides/connecting-git-account.html)
   your readthedocs account to github.
2. Optional, but recommended: If your repo lives under a github organization,
   you also need to give readthedocs.org permission to access it. To do so, on
   github go to `Settings > Applications > Authorized OAuth Apps` and click on
   "Read the Docs Community". At the bottom of the page, you should see the
   "Organization access" section with a list of your organizations. If your
   organization has a check mark, you've already given readthedocs access!
   Otherise, click on "Request" or "Grant" (depending on your access level).
   Once readthedocs has access, proceed to the next step (note that you don't
   need to give readthedocs access, but it will make things easier).
2. Sign in and go to [your projects](https://readthedocs.org/dashboard/). Click
   on "Import a project." If you have linked your accounts correctly, you should
   see a list of projects, both from your personal account and any organizations
   you are a part of. If you can find your project here, you're probably done!
   Otherwise, see the following steps.
3. If you don't see repos from a given organization, you can return to step 2.
   and try to grant readthedocs access or click on "Import manually" and enter
   the required information, clicking "Edit advanced project options." and
   entering "main" as the default branch name.
4. It will show you an example `.readthedocs.yaml` file, but we'll be using the
   one from this template repo, so you can ignore it (see
   [readthedocs](https://docs.readthedocs.io/en/stable/config-file/v2.html)
   documentation for more info on what can be included).
5. Fill out the extra details, selecting `Mkdocs` as the documentation type,
   `Python` as the programming language, and the github repo as the project
   homepage.
6. You will then most likely have to manually configure the webhook, following
   [these
   instructions](https://docs.readthedocs.io/en/latest/guides/setup/git-repo-manual.html#provider-specific-instructions)
7. Afterwards, go to your project, then `Admin > Advanced Settings` and check
   the "Build pull requests for this project" checkbox.
8. You should be good to go! If you had to manually add the github repo,
   readthedocs might not be able to post back to pull requests, so check on your
   builds (`https://readthedocs.org/projects/ccn-template/builds/`, replacing
   `ccn-template` with your project name) and post the link yourself! If you
   were able to give readthedocs access in step 2, it should be able to post.

If you were unable to give readthedocs access to your github documentation, you
can use readthedocs' [preview github
action](https://github.com/readthedocs/actions) to post the docs link to the PR.
